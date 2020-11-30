"""Visiting ASTs' nodes """


import re
import ast
import types
import linecache
from decimal import Decimal


class PymVisitor(ast.NodeVisitor):
    """ABC for all pym's Vistors"""

    def generic_visit(self, node):
        self.node = node
        for field, value in ast.iter_fields(node):
            self.field = field
            if isinstance(value, list):
                for item in value:
                    self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)


class Grepper(PymVisitor):
    def __init__(self, type_, regexp_):
        super().__init__()
        self.regexp = re.compile(regexp_)
        self.type = type_
        self.found = []
        setattr(self, f"visit_{type_}", self.grep)

    def grep(self, node):
        if not self.regexp.match(node.name):
            return
        self.found.append(node)


class Sourcer(PymVisitor):
    def __init__(self):
        super().__init__()

    def generic_visit(self, node):
        self.line_number = node.lineno
        breakpoint()
        filename, line_number = node.file, node.lineno
        self.line = linecache.getline(filename, line_number).rstrip()
        super().generic_visit(node)


class Liner(PymVisitor):
    def __init__(self):
        super().__init__()
        self._old = None
        self.lines = {}

    def generic_visit(self, node):
        number = node.lineno
        try:
            first = self.lines[number][0]
            self.lines[number] = (first, node)
        except KeyError:
            self.lines[number] = (node, node)


class VisitorMap(dict):
    """Maps Python types to visitors that know how to serialize them.

    A `VisitorMap` can be chained to a `parent_map` that it will
    fall-back to if it doesn't have a visitor registered for a
    specific type (or one of that types base classes).
    """

    def get_visitor(self, obj, use_default=True):
        """Return the visitor callable registered for `type(obj)`.

        If no exact match is found, it will look for a visitor
        registered on a base-type in `type(obj).__mro__`.  If that
        fails and the VisitorMap has a `parent_map`,
        `parent_map.get_visitor(obj, use_default=False)` will be
        called.

        If all of the above fails, it returns the `DEFAULT` visitor or
        `None`.
        """
        type_ = type(obj)
        result = self.get(type_) or self._get_parent_type_visitor(obj, type_)
        if result:
            return result
        elif self.parent_map is not None:
            result = self.parent_map.get_visitor(obj, False)
        if not result and use_default:
            result = self.get(DEFAULT)
            if not result and self.parent_map is not None:
                result = self.parent_map.get(DEFAULT)
        return result

    def _get_parent_type_visitor(self, obj, type_):
        try:
            from types import InstanceType  # support old-style classes

            if type_ is InstanceType:
                m = [t for t in self if isinstance(obj, t)]
                for i, t in enumerate(m):
                    j = i + i
                    if not any(t2 for t2 in m[j:] if t2 is not t and issubclass(t2, t)):
                        return self[t]
            return
        except ImportError:
            for base in type_.__mro__:
                if base in self:
                    return self[base]

    def copy(self):
        return self.__class__(super().copy())

    def as_context(self, walker, set_parent_map=True):
        """Returns as context manager for use with 'with' statements
        inside visitor functions.

        It allows you to define a set of visitor mappings that only
        apply within the current visitor's context and have all other
        mappings looked up in the exising visitor_map.  See
        `visit_xml_cdata` an example.
        """
        return _VisitorMapContextManager(self, walker, set_parent_map)

    def register(self, type_, visitor=None):
        """If both args are passed, this does `vmap[type_] = visitor`.
        If only `type_` is passed, it assumes you are decorating a
        visitor function definition:
          @vmap.register(some_type)
          def visit_some_type(o, w):
              ...
        """
        if visitor:
            self[type_] = visitor
        else:

            def decorator(f):
                self[type_] = f
                return f

            return decorator


class DEFAULT:
    ">>> visitor_map[DEFAULT] = visitor # sets default fallback visitor"


class _VisitorMapContextManager(object):
    """The `with` statement context manager returned by
    VisitorMap.as_context()"""

    def __init__(self, vmap, walker, set_parent_map=True):
        self.vmap = vmap
        self.original_map = None
        self.walker = walker
        self.set_parent_map = set_parent_map

    def __enter__(self):
        self.original_map = self.walker.visitor_map
        if self.set_parent_map:
            assert not self.vmap.parent_map
            self.vmap.parent_map = self.original_map
        self.walker.visitor_map = self.vmap

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.walker.visitor_map = self.original_map
        if self.set_parent_map:
            self.vmap.parent_map = None


# 4:  Default serialization visitors for standard Python types

# visitor signature = "f(obj_to_be_walked, walker)", return value ignored
# o = obj_to_be_walked, w = walker (aka serializer)
default_visitors_map = VisitorMap(
    {
        str: (lambda o, w: w.walk(bytes(o, w.input_encoding, "strict"))),
        bytes: (lambda o, w: w.emit(o)),
        type(None): (lambda o, w: None),
        bool: (lambda o, w: w.emit(str(o))),
        type: (lambda o, w: w.walk(bytes(o))),
        DEFAULT: (lambda o, w: w.walk(repr(o))),
    }
)
default_visitors_map.parent_map = None

number_types = (int, Decimal, float, complex)
func_types = (types.FunctionType, types.BuiltinMethodType, types.MethodType)
sequence_types = (tuple, list, set, frozenset, range, types.GeneratorType)

for typeset, visitor in (
    (number_types, (lambda o, w: w.emit(str(o)))),
    (sequence_types, (lambda o, w: [w.walk(i) for i in o])),
    (func_types, (lambda o, w: w.walk(o()))),
):
    for type_ in typeset:
        default_visitors_map[type_] = visitor
