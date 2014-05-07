"""Visiting nodes of ASTs"""


import ast
import sys


from indent import Indenter
from nodes import Comment


class Punctuator(object):
    def __init__(self, renderer, punctuation):
        self.punctuated = False
        self.renderer = renderer
        self.punctuation = punctuation

    def dispatch(self, node):
        self.prefix()
        if isinstance(node, list):
            for item in node:
                self.renderer.dispatch(item)
        else:
            self.renderer.dispatch(node)

    def write(self, string):
        self.prefix()
        self.renderer.write(string)

    def prefix(self):
        if self.punctuated:
            self.renderer.write('%s ' % self.punctuation)
        else:
            self.punctuated = True


class Commas(Punctuator):
    def __init__(self, renderer):
        Punctuator.__init__(self, renderer, ',')


def line_after(body):
    result = None
    for node in body:
        if hasattr(node, 'lineno'):
            result = getattr(node, 'lineno')
    return result + 1


def has_import(string):
    return string.startswith('import ')


def infinity_string():
    """Large float and imaginary literals get turned into infinities in the AST

    Unparse them here
    """
    return '1e' + repr(sys.float_info.max_10_exp + 1)


class Renderer(ast.NodeVisitor):
    """Render an AST as nodal text

    This class just renders text snippets

    This class is based on the Unparser class, from
        http://hg.python.org/cpython/file/3f7d5c235d82/Tools/parser/unparse.py
    That file is license under the PSF License
        which is available in this directory as "PYTHONLICENSE.txt"
    """

    def __init__(self):
        ast.NodeVisitor.__init__(self)
        self.indenter = Indenter()
        self.line = ''
        self.lines = []
        self.importing = False
        self.future_imports = []

    def generic_visit(self, node):
        raise NotImplementedError('Cannot visit %s' % node.__class__.__name__)

    def dispatch(self, node):
        if isinstance(node, list):
            _ = [self.visit(n) for n in node]
        else:
            return self.visit(node)

    def visit_Module(self, node):
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

    def render_block(self, values, line_number):
        value = values[0]
        if isinstance(value, Comment) and value.lineno == line_number:
            string = ':  %s' % value.s
            values = values[1:]
        else:
            string = ':'
        self.write_line(string)
        self.indenter.indent()
        self.render_body(values)
        self.indenter.dedent()

    def render_body(self, node):
        for child in node:
            self.dispatch(child)
            self.write_line()

    def write_multiline_string(self, quotes, string):
        self.write(quotes)
        for line in string.splitlines():
            self.write_line(line)
        self.write(quotes)

    def visit_DocString(self, node):
        if '\n' in node.s:
            self.write_multiline_string('"""', node.s)
        else:
            self.write('"""%s"""' % node.s)

    def visit_Str(self, node):
        if '\n' in node.s:
            self.write_multiline_string("'''", node.s)
        else:
            self.write(repr(node.s))

    def visit_Comment(self, node):
        if node.prefix:
            self.dispatch(node.prefix)
            self.write('  ')
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
        self.render_block(node.body, node.lineno)
        while (node.orelse and len(node.orelse) == 1 and
               isinstance(node.orelse[0], ast.If)):
            node = node.orelse[0]
            self.write('elif ')
            self.dispatch(node.test)
            self.render_block(node.body, node.test.lineno)
        if node.orelse:
            self.write('else')
            self.render_block(node.orelse, line_after(node.body))

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
        self.render_block(node.body, node.lineno)

    def visit_ClassDef(self, node):
        self.render_decorators(node)
        self.write('class %s' % node.name)
        if node.bases:
            self.write('(')
            commas = Commas(self)
            for base in node.bases:
                commas.dispatch(base)
            self.write(')')
        self.render_block(node.body, node.lineno)

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
        loading = isinstance(node.ctx, ast.Load)
        if loading:
            self.write('(')
        if len(node.elts) == 1:
            (item,) = node.elts
            self.dispatch(item)
            self.write(',')
        else:
            commas = Commas(self)
            for item in node.elts:
                commas.dispatch(item)
        if loading:
            self.write(')')

    def visit_With(self, node):
        self.write('with ')
        self.dispatch(node.context_expr)
        if node.optional_vars:
            self.write(' as ')
            self.dispatch(node.optional_vars)
        self.render_block(node.body, node.lineno)

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
        self.render_block(node.body, node.lineno)
        for handler in node.handlers:
            self.dispatch(handler)
        if node.orelse:
            self.write('else')
            self.render_block(node.orelse, line_after(node.body))

    def visit_TryFinally(self, node):
        if len(node.body) == 1 and isinstance(node.body[0], ast.TryExcept):
            # try-except-finally
            self.dispatch(node.body)
        else:
            self.write('try')
            self.render_block(node.body, node.lineno)
        self.write('finally')
        self.render_block(node.finalbody, line_after(node.body))

    def visit_While(self, node):
        self.write('while ')
        self.dispatch(node.test)
        self.render_block(node.body, node.lineno)
        if node.orelse:
            self.write('else')
            self.render_block(node.orelse, line_after(node.body))

    def visit_Yield(self, node):
        self.write('yield')
        if node.value:
            self.write(' ')
            self.dispatch(node.value)

    def visit_ExceptHandler(self, node):
        self.write('except')
        if node.type:
            self.write(' ')
            self.dispatch(node.type)
        if node.name:
            self.write(' as ')
            self.dispatch(node.name)
        self.render_block(node.body, node.lineno)

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

    binary_operators = {
        'Add': '+', 'Sub': '-', 'Mult': '*', 'Div': '/', 'Mod': '%',
        'LShift': '<<', 'RShift': '>>', 'BitOr': '|', 'BitXor': '^',
        'BitAnd': '&', 'FloorDiv': '//', 'Pow': '**'
    }

    def visit_BinOp(self, node):
        operator_name = node.op.__class__.__name__
        self.dispatch(node.left)
        self.write(' %s ' % self.binary_operators[operator_name])
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

    def visit_Dict(self, node):
        self.write('{')
        items = zip(node.keys, node.values)
        commas = Commas(self)
        for key, value in items:
            commas.dispatch([key, ': ', value])
        self.write('}')

    def visit_str(self, string):
        self.write(string)

    def visit_List(self, node):
        self.write('[')
        commas = Commas(self)
        for item in node.elts:
            commas.dispatch(item)
        self.write(']')

    def visit_For(self, node):
        self.write('for ')
        self.dispatch(node.target)
        self.write(' in ')
        self.dispatch(node.iter)
        self.render_block(node.body, node.lineno)
        if node.orelse:
            self.write('else')
            self.render_block(node.orelse, line_after(node.body))

    def visit_Break(self, _node):
        self.write('break')

    def visit_Continue(self, _node):
        self.write('continue')

    def visit_Subscript(self, node):
        self.dispatch(node.value)
        self.write('[')
        self.dispatch(node.slice)
        self.write(']')

    def visit_Index(self, node):
        self.dispatch(node.value)

    def visit_AugAssign(self, node):
        self.dispatch(node.target)
        self.write(' %s= ' % self.binary_operators[node.op.__class__.__name__])
        self.dispatch(node.value)

    boolops = {ast.And: 'and', ast.Or: 'or'}

    def visit_BoolOp(self, node):
        punctuator = Punctuator(self, self.boolops[node.op.__class__])
        for value in node.values:
            punctuator.dispatch(value)

    def visit_Delete(self, node):
        self.write('del ')
        commas = Commas(self)
        for target in node.targets:
            commas.dispatch(target)

    def visit_Slice(self, node):
        if node.lower:
            self.dispatch(node.lower)
        self.write(':')
        if node.upper:
            self.dispatch(node.upper)
        if node.step:
            self.write(':')
            self.dispatch(node.step)

    def visit_Set(self, node):
        if not node.elts:
            raise ValueError(
                'Set should have at least one element: %r' % node.elts)
        self.write('{')
        commas = Commas(self)
        for element in node.elts:
            commas.dispatch(element)
        self.write('}')

    def visit_SetComp(self, node):
        self.write('{')
        self.dispatch(node.elt)
        for generator in node.generators:
            self.dispatch(generator)
        self.write('}')

    def visit_Repr(self, node):
        self.write('repr(')
        self.dispatch(node.value)
        self.write(')')

    def visit_ListComp(self, node):
        self.write('[')
        self.dispatch(node.elt)
        for generator in node.generators:
            self.dispatch(generator)
        self.write(']')

    def visit_Lambda(self, node):
        self.write('(')
        self.write('lambda ')
        self.dispatch(node.args)
        self.write(': ')
        self.dispatch(node.body)
        self.write(')')

    def visit_IfExp(self, node):
        self.write('(')
        self.dispatch(node.body)
        self.write(' if ')
        self.dispatch(node.test)
        self.write(' else ')
        self.dispatch(node.orelse)
        self.write(')')

    def visit_Global(self, node):
        self.write('global ')
        commas = Commas(self)
        for name in node.names:
            commas.dispatch(name)

    def visit_GeneratorExp(self, node):
        self.write('(')
        self.dispatch(node.elt)
        for generator in node.generators:
            self.dispatch(generator)
        self.write(')')

    def visit_ExtSlice(self, node):
        commas = Commas(self)
        for dimension in node.dims:
            commas.dispatch(dimension)

    def visit_Exec(self, node):
        self.write('exec ')
        self.dispatch(node.body)
        if node.globals:
            self.write(' in ')
            self.dispatch(node.globals)
        if node.locals:
            self.write(', ')
            self.dispatch(node.locals)

    def visit_Ellipsis(self, _node):
        self.write('...')

    def visit_DictComp(self, node):
        self.write('{')
        self.dispatch(node.key)
        self.write(': ')
        self.dispatch(node.value)
        for generator in node.generators:
            self.dispatch(generator)
        self.write('}')

    def visit_Assert(self, node):
        self.write('assert ')
        self.dispatch(node.test)
        if node.msg:
            self.write(', ')
            self.dispatch(node.msg)

    def visit_comprehension(self, node):
        self.write(' for ')
        self.dispatch(node.target)
        self.write(' in ')
        self.dispatch(node.iter)
        for if_clause in node.ifs:
            self.write(' if ')
            self.dispatch(if_clause)