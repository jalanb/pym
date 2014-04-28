"""Module to render Python ASTs to text"""


import sys
import ast
import tokenize
from cStringIO import StringIO


from indent import Indenter


def has_import(string):
    return string.startswith('import ')


def render_docstring(string):
    if '\n' in string:
        return '"""%s\n"""' % string
    else:
        return '"""%s"""' % string


def render_multiline_string(string):
    return "'''%s'''" % string


def extract_docstring(node):
    docstring = ast.get_docstring(node)
    if docstring:
        del node.body[0]
    return docstring


class Commas(object):
    def __init__(self, renderer):
        self.comma = False
        self.renderer = renderer

    def dispatch(self, node):
        self.prefix()
        self.renderer.dispatch(node)

    def write(self, string):
        self.prefix()
        self.renderer.write(string)

    def prefix(self):
        if self.comma:
            self.renderer.write(', ')
        else:
            self.comma = True


def get_comments(string):
    """Hold equivalent tokens for a tree being rendered"""
    stream = StringIO(string)
    tokens = list(tokenize.generate_tokens(stream.readline))
    comments = [
        (start_line, start_column, string)
        for type_, string, (start_line, start_column), _, _,
        in tokens
        if type_ == tokenize.COMMENT
    ]
    return sorted(comments)


def as_comment_nodes(comments):
    return [Comment(string, lineno=line, col_offset=column)
            for line, column, _, string
            in comments]


class Renderer(ast.NodeVisitor):
    """Render an AST as nodal text

    This class just renders text snippets

    This class is based on the Unparser class, from
        http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser/unparse.py
    That file is license under the PSF License
        which is avialable in this directory as "PYTHONLICENSE.txt"
    """
    # pylint: disable-msg=R0921
    # TODO R0921: "Abstract class not referenced"

    def __init__(self):
        ast.NodeVisitor.__init__(self)
        self.indenter = Indenter()
        self.line = ''
        self.lines = []
        self.importing = False

    def generic_visit(self, node):
        raise NotImplementedError('Cannot visit %s' % node.__class__.__name__)

    def dispatch(self, node):
        if isinstance(node, list):
            _ = [self.visit(n) for n in node]
        else:
            return self.visit(node)

    def visit_Module(self, node):
        docstring = extract_docstring(node)
        self.write_line(render_docstring(docstring))
        self.render_body(node.body)

    def write(self, string):
        if not self.line:
            self.new_line(string)
            self.line = self.indenter.render(string)
        else:
            self.line = '%s%s' % (self.line, string)

    def new_line(self, string):
        if string and self.lines and not self.indenter.indentation:
            self.importing = has_import(string)
        self.line = self.indenter.render(string)

    def write_line(self, string=''):
        self.write(string)
        if not self.line.isspace():
            self.lines.append(self.line)
        self.line = ''

    def render_block(self, node):
        self.write_line(':')
        self.indenter.indent()
        self.render_body(node)
        self.indenter.dedent()

    def render_body(self, node):
        for child in node:
            self.dispatch(child)
            self.write_line()

    def visit_Str(self, node):
        if '\n' in node.s:
            self.write("'''")
            for line in node.s.splitlines():
                self.write_line(line)
            self.write("'''")
        else:
            self.write(repr(node.s))

    def visit_Comment(self, node):
        self.write(node.s)

    def visit_Expr(self, node):
        self.dispatch(node.value)

    def visit_Import(self, node):
        self.write('import ')
        self.dispatch(node.names[0])
        for name in node.names[1:]:
            self.write(', ')
            self.dispatch(name)

    def visit_alias(self, node):
        self.write(node.name)
        if node.asname:
            self.write('as %s' % node.asname)

    def visit_If(self, node):
        self.write('if ')
        self.dispatch(node.test)
        self.render_block(node.body)
        while (node.orelse and len(node.orelse) == 1 and
               isinstance(node.orelse[0], ast.If)):
            node = node.orelse[0]
            self.write('elif ')
            self.dispatch(node.test)
            self.render_block(node.body)
        if node.orelse:
            self.write('else')
            self.render_block(node.orelse)

    def render_decorators(self, node):
        if not node.decorator_list:
            return
        for decorator in node.decorator_list:
            self.write('@')
            self.dispatch(decorator)
        self.write_line()

    def visit_FunctionDef(self, node):
        self.render_decorators(node)
        self.write('def %s(' % node.name)
        self.dispatch(node.args)
        self.write(')')
        self.render_block(node.body)

    def visit_ClassDef(self, node):
        self.render_decorators(node)
        self.write('class %s' % node.name)
        if node.bases:
            self.write('(')
            commas = Commas(self)
            for base in node.bases:
                commas.dispatch(base)
            self.write(')')
        self.render_block(node.body)

    def visit_ImportFrom(self, node):
        if node.module and node.module == '__future__':
            self.future_imports.extend(n.name for n in node.names)
        self.write('from ')
        self.write('.' * node.level)
        if node.module:
            self.write(node.module)
        self.write(' import ')
        commas = Commas(self)
        for name in node.names:
            commas.dispatch(name)

    def visit_Assign(self, node):
        for target in node.targets:
            self.dispatch(target)
            self.write(' = ')
        self.dispatch(node.value)

    def visit_Name(self, node):
        self.write(node.id)

    def visit_Call(self, node):
        self.dispatch(node.func)
        self.write('(')
        commas = Commas(self)
        for arg in node.args + node.keywords:
            commas.dispatch(arg)
        if node.starargs:
            commas.write('*')
            self.dispatch(node.starargs)
        if node.kwargs:
            commas.write('**')
            self.dispatch(node.kwargs)
        self.write(')')

    def visit_Attribute(self, node):
        self.dispatch(node.value)
        if isinstance(node.value, ast.Num) and isinstance(node.value.n, int):
            self.write(' ')
        self.write('.')
        self.write(node.attr)

    def visit_Return(self, node):
        self.write('return')
        if node.value:
            self.write(' ')
            self.dispatch(node.value)

    def visit_Tuple(self, node):
        if node.ctx == ast.Load:
            self.write('(')
        if len(node.elts) == 1:
            (item,) = node.elts
            self.dispatch(item)
            self.write(',')
        else:
            commas = Commas(self)
            for item in node.elts:
                commas.dispatch(item)
        if node.ctx == ast.Load:
            self.write(')')

    def visit_With(self, node):
        self.write('with ')
        self.dispatch(node.context_expr)
        if node.optional_vars:
            self.write(' as ')
            self.dispatch(node.optional_vars)
        self.render_block(node.body)

    def visit_Print(self, node):
        self.write('print ')
        commas = Commas(self)
        if node.dest:
            commas.write('>> ')
            self.dispatch(node.dest)
        for value in node.values:
            commas.dispatch(value)
        stay_on_line = ',' if not node.nl else ''
        self.write(stay_on_line)

    def visit_keyword(self, node):
        self.write(node.arg)
        self.write('=')
        self.dispatch(node.value)

    def visit_TryExcept(self, node):
        self.write('try')
        self.render_block(node.body)
        for handler in node.handlers:
            self.dispatch(handler)
        if node.orelse:
            self.write('else')
            self.render_block(node.orelse)

    def visit_ExceptHandler(self, node):
        self.write('except')
        if node.type:
            self.write(' ')
            self.dispatch(node.type)
        if node.name:
            self.write(' as ')
            self.dispatch(node.name)
        self.render_block(node.body)

    def visit_arguments(self, node):
        if node.defaults:
            i = len(node.defaults)
            plain_args = node.args[:-i]
            defaulted_args = zip(node.args[i:], node.defaults)
        else:
            plain_args = node.args
            defaulted_args = []
        commas = Commas(self)
        for arg in plain_args:
            commas.dispatch(arg)
        for arg, default in defaulted_args:
            commas.dispatch(arg)
            self.write('=')
            self.dispatch(default)
        if node.vararg:
            commas.write('*')
            self.dispatch(node.vararg)
        if node.kwarg:
            commas.write('**')
            self.dispatch(node.kwarg)

    def visit_UnaryOp(self, node):
        operators = {'Invert': '~', 'Not': 'not', 'UAdd': '+', 'USub': '-'}
        operator_name = node.op.__class__.__name__
        self.write('%s ' % operators[operator_name])
        if operator_name == 'USub' and isinstance(node.operand, ast.Num):
            self.write('(')
            self.dispatch(node.operand)
            self.write(')')
        else:
            self.dispatch(node.operand)

    def visit_BinOp(self, node):
        operators = {
            'Add': '+', 'Sub': '-', 'Mult': '*', 'Div': '/', 'Mod': '%',
            'LShift': '<<', 'RShift': '>>', 'BitOr': '|', 'BitXor': '^',
            'BitAnd': '&', 'FloorDiv': '//', 'Pow': '**'
        }
        operator_name = node.op.__class__.__name__
        self.dispatch(node.left)
        self.write(' %s ' % operators[operator_name])
        self.dispatch(node.right)

    def visit_Compare(self, node):
        operators = {
            'Eq': '==', 'NotEq': '!=', 'Lt': '<', 'LtE': '<=',
            'Gt': '>', 'GtE': '>=', 'Is': 'is', 'IsNot': 'is not',
            'In': 'in', 'NotIn': 'not in'
        }
        self.dispatch(node.left)
        for operator_node, comparator in zip(node.ops, node.comparators):
            operator_name = operator_node.__class__.__name__
            operator = operators[operator_name]
            self.write(' %s ' % operator)
            self.dispatch(comparator)

    def visit_Raise(self, node):
        self.write('raise ')
        if node.type:
            self.dispatch(node.type)
        if node.inst:
            self.write(', ')
            self.dispatch(node.inst)
        if node.tback:
            self.write(', ')
            self.dispatch(node.tback)

    def visit_Pass(self, _node):
        self.write('pass')

    def visit_Num(self, node):
        string = repr(node.n)
        string = string.replace("inf", infinity_string())
        self.write(string)


def infinity_string():
    """Large float and imaginary literals get turned into infinities in the AST

    Unparse them here
    """
    return '1e' + repr(sys.float_info.max_10_exp + 1)


def parse(source, path=None):
    path = path if path else '<unknown>'
    return ast.parse(source, path)


class Comment(ast.Str):
    def __init__(self, comment):
        ast.Str.__init__(self)
        line, column, string = comment
        self.lineno = line
        self.col_offset = column
        self.s = string

    def is_before(self, node):
        if not hasattr(node, 'lineno'):
            return False
        if self.lineno < node.lineno:
            return True
        if self.lineno == node.lineno:
            return self.col_offset < node.col_offset
        return False


class NoComment(Comment):
    def is_before(self, _):
        return False


class Commenter(ast.NodeVisitor):
    """Add comments into an AST"""
    def __init__(self, comments):
        ast.NodeVisitor.__init__(self)
        self.comments = comments
        self.next_comment()

    def next_comment(self):
        try:
            self.comment = Comment(self.comments.pop(0))
        except IndexError:
            self.comment = NoComment((-1, -1, ''))

    def generic_visit(self, node):
        """Visit a node and add any needed comments

        Based on the equivalent method in ast.NodeTransformer which states:
            :copyright: Copyright 2008 by Armin Ronacher
            :license: Python License.
        That license file is in this directory as "PYTHONLICENSE.txt"
        """
        for field, old_value in ast.iter_fields(node):
            old_value = getattr(node, field, None)
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, ast.AST):
                        while self.comment.is_before(value):
                            new_values.append(self.comment)
                            self.next_comment()
                        value = self.visit(value)
                        if value is None:
                            continue
                        if not isinstance(value, ast.AST):
                            new_values.extend(value)
                            continue
                    new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, ast.AST):
                new_node = self.visit(old_value)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node


def add_comments(tree, string):
    """Add comments into the tree"""
    comments = get_comments(string)
    commenter = Commenter(comments)
    commenter.visit(tree)


def render(node):
    renderer = Renderer()
    renderer.visit(node)
    return '\n'.join(renderer.lines)


def re_render(string, path=None):
    tree = parse(string, path)
    add_comments(tree, string)
    return render(tree)
