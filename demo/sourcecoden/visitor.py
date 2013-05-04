import sys

from compiler import ast

from cStringIO import StringIO

version = sys.version_info[:3]

def triple_quote(doc):
    return '"""%s"""' % doc.replace('"""', '\"\"\"')

def format_argnames(argnames):
    return ", ".join(
        isinstance(name, tuple) and "(%s)" % format_argnames(name) or name \
        for name in argnames)

def format_ass(node):
    if isinstance(node, ast.AssTuple):
        return "(%s)" % ", ".join(format_ass(ass) for ass in node)
    return node.name

class prioritized(object):
    def __init__(self, generator, priority):
        self.generator = generator
        self.priority = priority

    def __iter__(self):
        return self.generator

def prioritize(priority):
    def decorator(func):
        def visit(self, node):
            return prioritized(func(self, node), priority)
        return visit
    return decorator

def unary(symbol, priority):
    @prioritize(prioritize)
    def visit(self, node):
        yield symbol
        child = self.visit(node.expr)
        if child.priority < priority:
            yield '('
            yield child
            yield ')'
        else:
            yield child
    return visit

def binary(symbol, priority):
    @prioritize(prioritize)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left.priority < priority and right.priority < priority:
            yield '('
            yield left
            yield ' %s ' % symbol
            yield right
            yield ')'
        else:
            yield left
            yield ' %s ' % symbol
            yield right
            
    return visit

def n_ary(symbol, priority):
    @prioritize(prioritize)
    def visit(self, node):
        yield '('
        for condition in tuple(node)[:-1]:
            yield self.visit(condition)
            yield ' %s ' % symbol
        yield self.visit(tuple(node)[-1])
        yield ')'
    return visit

class CodeStream(object):
    def __init__(self, indentation_string="\t"):
        self.indentation_string = indentation_string
        self.indentation = 0
        self.stream = StringIO()
        self.clear = True

    def __call__(self, value):
        if value is None:
            return self.write(None)

        if isinstance(value, basestring):
            return self.out(value)

        if isinstance(value, tuple) and self.clear is False:
            self.write()
            self.clear = True
            self.indentation += 1
            self(value)
            self.indentation -= 1
        else:
            for part in value:
                self(part)

    def write(self, text=None):
        if text or self.clear == False:
            self.out(text)
            self.stream.write('\n')
        self.clear = True
    
    def out(self, text):
        if self.clear is True:
            indentation = self.indentation_string * self.indentation
            self.stream.write(indentation)
            self.clear = False
        self.stream.write(text or "")

    def getvalue(self):
        return self.stream.getvalue()
    
class ASTVisitor(object):
    def __init__(self, tree):
        self.tree = tree

    def __call__(self):
        stream = CodeStream()
        stream(self.visit(self.tree))            
        return stream.getvalue()
        
    def visit(self, node):
        name = node.__class__.__name__

        try:
            func = getattr(self, 'visit%s' % name)
        except AttributeError:
            raise NotImplementedError(
                "Unable to visit `%s`." % repr(node))

        gen = func(node)

        if isinstance(gen, prioritized):
            return gen

        return prioritized(gen, 0)

    def visitModule(self, node):
        if node.doc is not None:
            yield triple_quote(node.doc)
            yield None

        for node in self.visit(node.node):
            yield node

    def visitStmt(self, node):
        yield tuple(self.visit(child) for child in node.nodes if child is not None)
        
    def visitIf(self, node):
        for index, test in enumerate(node.tests):
            if index == 0:
                yield "if "
            else:
                yield "elif "

            condition, statement = test

            yield self.visit(condition)
            yield ":"
            yield self.visit(statement),
            
        if node.else_:
            yield "else:"
            yield self.visit(node.else_),

    @prioritize(-3)
    def visitName(self, node):
        yield node.name

    def visitPass(self, node):
        yield "pass"
        yield None

    def visitDiscard(self, node):
        yield self.visit(node.expr)
        yield None

    def visitAssign(self, node):
        for index, ass in enumerate(tuple(node.nodes)):
            yield self.visit(ass)
                
            if index < len(tuple(node.nodes)) - 1:
                yield " = "
        yield " = "
        yield self.visit(node.expr)
        yield None

    def visitAssName(self, node):
        if node.flags == 'OP_DELETE':
            yield "del "
        yield node.name
        if node.flags == 'OP_DELETE':
            yield None

    def visitFunction(self, node):
        if node.decorators:
            yield self.visit(node.decorators)

        yield "def %s(" % node.name

        argnames = list(node.argnames)
        if argnames:
            if node.kwargs:
                kwargs = argnames.pop()
            if node.varargs:
                varargs = argnames.pop()

            if node.defaults:
                yield format_argnames(argnames[:-len(node.defaults)])
                for index, default in enumerate(node.defaults):
                    name = argnames[index-len(node.defaults)]
                    if len(argnames) > len(node.defaults) or index > 0:
                        yield ", %s=" % name
                    else:
                        yield "%s=" % name
                    yield self.visit(default)
            else:
                yield format_argnames(argnames)

        if node.varargs:
            if len(node.argnames) > 1:
                yield ", "
            yield "*%s" % varargs

        if node.kwargs:
            if len(node.argnames) > 1 or node.varargs:
                yield ", "
            yield "**%s" % kwargs

        yield "):"

        if node.doc:
            yield triple_quote(node.doc),

        yield self.visit(node.code),

    @prioritize(0)
    def visitConst(self, node):
        yield repr(node.value)

    def visitDecorators(self, node):
        for decorator in tuple(node):
            yield '@'
            yield self.visit(decorator)
            yield None

    def visitCallFunc(self, node):
        yield self.visit(node.node)
        yield '('
        for arg in tuple(node.args)[:-1]:
            yield self.visit(arg)
            yield ", "
        if node.args:
            yield self.visit(node.args[-1])
        if node.star_args:
            if node.args:
                yield ", *"
            else:
                yield "*"
            yield self.visit(node.star_args)
        if node.dstar_args:
            if node.args:
                yield ", **"
            else:
                yield "**"
            yield self.visit(node.dstar_args)
        yield ")"

    def visitKeyword(self, node):
        yield "%s=" % node.name
        yield self.visit(node.expr)

    def visitAssTuple(self, node):
        first = node
        while isinstance(first, ast.AssTuple):
            first = first.nodes[0]
        if first.flags == 'OP_DELETE':
            yield "del "
        yield format_ass(node)
        if first.flags == 'OP_DELETE':
            yield None

    @prioritize(0)
    def visitTuple(self, node):
        yield "("
        for index, item in enumerate(tuple(node)):
            yield self.visit(item)
            if index < len(tuple(node)) - 1:
                yield ", "
        if len(node.nodes) == 1:
            yield ", "
        yield ")"

    def visitGenExpr(self, node):
        yield "("
        yield self.visit(node.code)
        yield ")"

    def visitListComp(self, node):
        yield "["
        yield self.visitGenExprInner(node)
        yield "]"

    def visitGenExprInner(self, node):
        yield self.visit(node.expr)
        for qual in node.quals:
            yield self.visit(qual)

    def visitGenExprFor(self, node):
        yield " for "
        yield self.visit(node.assign)
        yield " in "
        yield self.visit(node.iter)
        for _if in node.ifs:
            yield self.visit(_if)

    def visitGenExprIf(self, node):
        yield " if "
        yield self.visit(node.test)

    def visitListCompFor(self, node):
        yield " for "
        yield self.visit(node.assign)
        yield " in "
        yield self.visit(node.list)
        for _if in node.ifs:
            yield self.visit(_if)
            
    def visitListCompIf(self, node):
        yield " if "
        yield self.visit(node.test)

    def visitCompare(self, node):
        yield self.visit(node.expr)
        for op, expr in node.ops:
            yield ' %s ' % op
            yield self.visit(expr)

    def visitImport(self, node):
        yield "import "
        for index, (name, alias) in enumerate(node.names):
            yield name
            if alias is not None:
                yield " as %s" % alias
            if index < len(node.names) - 1:
                yield ", "
        yield None

    def visitFrom(self, node):
        yield "from %s import " % node.modname
        for index, (name, alias) in enumerate(node.names):
            yield name
            if alias is not None:
                yield " as %s" % alias
            if index < len(node.names) - 1:
                yield ", "
        yield None

    def visitReturn(self, node):
        yield "return "
        yield self.visit(node.value)
        yield None

    def visitBreak(self, node):
        yield "break"
        yield None

    def visitContinue(self, node):
        yield "continue"
        yield None

    def visitWhile(self, node):
        yield "while "
        yield self.visit(node.test)
        yield ":"
 
        yield self.visit(node.body),

        if node.else_ is not None:
            yield "else:"
            yield self.visit(node.else_),

    def visitTryExcept(self, node):
        yield "try:"
        yield self.visit(node.body),
        for cls, var, body in node.handlers:
            yield "except"
            if cls is not None:
                yield " "
                yield self.visit(cls)
            if var is not None:
                if cls is None:
                    yield " "
                else:
                    yield ", "
                yield self.visit(var)
            yield ":"
            yield self.visit(body),

        if node.else_:
            yield "else:"
            yield self.visit(node.else_),
    
    def visitTryFinally(self, node):
        if version < (2,5):
            yield "try:"
            yield self.visit(node.body),
            yield "finally:"
            yield self.visit(node.final),
        else:
            yield self.visit(node.body)
            yield "finally:"
            yield self.visit(node.final),

    def visitClass(self, node):
        yield "class %s" % node.name

        if node.bases:
            yield "("
            for index, base in enumerate(node.bases):
                yield self.visit(base)
                if index < len(node.bases) - 1:
                    yield ", "
            yield ")"
        yield ":"
        
        if node.doc:
            yield triple_quote(node.doc), self.visit(node.code)
        else:
            yield self.visit(node.code)

    @prioritize(-2)
    def visitLambda(self, node):
        yield "lambda"
        argnames = list(node.argnames)
        if argnames:
            yield " "
            if node.kwargs:
                kwargs = argnames.pop()
            if node.varargs:
                varargs = argnames.pop()

            if node.defaults:
                yield format_argnames(argnames[:-len(node.defaults)])
                for index, default in enumerate(node.defaults):
                    name = argnames[index-len(node.defaults)]
                    yield ", %s=" % name
                    yield self.visit(default)
            else:
                yield format_argnames(argnames)

        offset = (node.varargs or 0) + (node.kwargs or 0)

        if node.varargs:
            if len(node.argnames) > offset:
                yield ", "
            yield "*%s" % varargs

        if node.kwargs:
            if node.varargs or len(node.argnames) > offset:
                yield ", "
            yield "**%s" % kwargs

        yield ": "
        yield self.visit(node.code)

    def visitGetattr(self, node):
        yield self.visit(node.expr)
        yield ".%s" % node.attrname

    def visitAssAttr(self, node):
        if node.flags == 'OP_DELETE':
            yield "del "
        yield self.visit(node.expr)
        yield ".%s" % node.attrname
        if node.flags == 'OP_DELETE':
            yield None

    def visitSubscript(self, node):
        if node.flags == 'OP_DELETE':
            yield "del "
        yield self.visit(node.expr)
        yield '['
        for index, sub in enumerate(node.subs):
            if isinstance(sub, ast.Sliceobj):
                for i, slice in enumerate(tuple(sub)):
                    yield self.visit(slice)
                    if i < len(tuple(sub)) - 1:
                        yield ":"
            else:
                yield self.visit(sub)
            if index < len(node.subs) - 1:
                yield ', '
        yield ']'
        if node.flags == 'OP_DELETE':
            yield None

    def visitSlice(self, node):
        if node.flags == 'OP_DELETE':
            yield "del "
        yield self.visit(node.expr)
        yield '['
        if node.lower:
            yield self.visit(node.lower)
        yield ':'
        if node.upper:
            yield self.visit(node.upper)
        yield ']'
        if node.flags == 'OP_DELETE':
            yield None

    def visitSliceobj(self, node):
        yield 'slice('
        for index, item in enumerate(tuple(node)):
            yield self.visit(item)
            if index < len(tuple(node)) - 1:
                yield ", "
        yield ')'

    def visitExec(self, node):
        yield "exec "
        yield self.visit(node.expr)
        if node.locals:
            yield " in "
            yield self.visit(node.locals)
        if node.globals:
            yield ", "
            yield self.visit(node.globals)
        yield None

    def visitAssert(self, node):
        yield "assert "
        yield self.visit(node.test)
        if node.fail is not None:
            yield ", "
            yield self.visit(node.fail)
        yield None

    def visitRaise(self, node):
        yield "raise "
        yield self.visit(node.expr1)
        if node.expr2:
            yield ", "
            yield self.visit(node.expr2)
        if node.expr3:
            yield ", "
            yield self.visit(node.expr3)

    def visitPrintnl(self, node):
        yield "print "
        if node.dest is not None:
            yield ">> "
            yield self.visit(node.dest)
            yield ", "
        for index, expr in enumerate(tuple(node.nodes)):
            if expr is None:
                continue
            yield self.visit(expr)
            if index < len(tuple(node.nodes)) - 1 and node.nodes[index+1] is not None:
                yield ", "
        yield None

    def visitIfExp(self, node):
        yield self.visit(node.then)
        yield " if "
        yield self.visit(node.test)
        yield " else "
        yield self.visit(node.else_)

    def visitWith(self, node):
        raise NotImplementedError(
            "The `with` keyword is not supported.")

    def visitAugAssign(self, node):
        yield self.visit(node.node)
        yield " %s " % node.op
        yield self.visit(node.expr)
        yield None

    def visitList(self, node):
        yield '['
        for index, item in enumerate(node.nodes):
            yield self.visit(item)
            if index < len(node.nodes) - 1:
                yield ", "
        yield ']'

    def visitDict(self, node):
        yield '{'
        for index, (expr, value) in enumerate(node.items):
            yield self.visit(expr)
            yield ': '
            yield self.visit(value)
            if index < len(node.items) - 1:
                yield ", "
        yield '}'

    def visitFor(self, node):
        yield "for %s in " % format_ass(node.assign)
        yield self.visit(node.list)
        yield ":"
        yield self.visit(node.body)
        if node.else_ is not None:
            yield "else:"
            yield self.visit(node.else_)

    def visitYield(self, node):
        yield "yield "
        yield self.visit(node.value)
        yield None

    visitPower = binary('**', 10)
    visitInvert = unary('~', 9)
    visitUnaryAdd = unary('+', 8)
    visitUnarySub = unary('-', 8)
    visitMul = binary('*', 7)
    visitMod = binary('%', 7)    
    visitDiv = binary('/', 7)

    visitAdd = binary('+', 6)
    visitSub = binary('-', 6)

    visitLeftShift = binary('<<', 5)
    visitRightShift = binary('>>', 5)

    visitBitand = n_ary('&', 4)
    visitBitxor = n_ary('^', 3)
    visitBitor = n_ary('|', 2)
    
    visitNot = unary('not ', 1)
    visitAnd = n_ary('and', 0)
    visitOr = n_ary('or', -1)

    

