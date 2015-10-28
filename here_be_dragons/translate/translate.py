"""
A grammar for parsing a tiny HTML-like language, plus a transformer for it.
"""


import sys
import re
from mymeta.grammar import OMeta


from path import makepath
import rebrace


used_types = set()
class_name = 'class_for_testing'
bases = []
dynamic_attribute_initialisations = set()
static_attribute_initialisations = set()
write_file = 'header'
indent = ''
simple_types = [
        'void',
        'int',
        'long',
        'short',
        'unsigned',
        'char',
        'bool',
        'double',
]


known_headers = {
        'OC_ALTO_RGW': 'Rias1221Messages.h',
        'ADMIN_STATE_UNLOCKED': 'Rias1221Messages.h',
        'OC_BASEBAND_TRANSCEIVER': 'Rias1221Messages.h',
        'ATTRIBUTE_VALUE_CHANGE_EVENT': 'Rias1221Messages.h',
        'FINAL_SEGMENT': 'Rias1221Messages.h',
        'null': 'stdlib.h',
        'Math.min': 'min.h',
        'Math.sin': 'math.h',
        'Math.cos': 'math.h',
        'addAll': 'vector_all.h',
}


needed_headers = [
]


def as_string(i):
        return ''.join(i)


def use_type(t):
        if t:
                used_types.add(t)
        return t


def class_types():
        result = []
        for t in used_types:
                if t in simple_types:
                        continue
                result.append('class %s;' % t.replace('*', ''))
        return '\n'.join(result)


def known_includer(sought):
        known_inclusions = {
                'std::string': '<string>',
                'std::vector': '<vector>',
                'ACE_CString': '"ace/SString.h"',
                'RiasStatus::Rias': '"RiasStatus.h"',
                'RiasConfiguration': '"RiasConf.h"',
        }
        if sought in known_inclusions:
                return known_inclusions[sought]
        regexp_inclusions = [
                ('std::vector<.*>', '<vector>'),
        ]
        for regexp, inclusion in regexp_inclusions:
                if re.match(regexp, sought):
                        return inclusion
        return None


def not_to_be_included(changed):
        if changed == class_name:
                return True
        if changed in simple_types:
                return True
        if changed.endswith('[]'):
                changed = changed[:-2]
                return changed in simple_types
        if changed.endswith('*'):
                changed = changed[:-1]
                return changed in simple_types
        return False


def include_types():
        if write_file == 'cpp':
                included_headers = ['# include "%s.h"' % class_name]
                for header in needed_headers:
                        if not header:
                                continue
                        included_header = '# include "%s"' % header
                        if included_header not in included_headers:
                                included_headers.append(included_header)
                included_headers.append('# include "logger.h"')
                return '\n'.join(included_headers)

        result = []
        include_dir = makepath('../translated')
        missing = []
        for t in used_types:
                changed = change_type(t)
                if not_to_be_included(changed):
                        continue
                header = known_includer(changed)
                if not header:
                        header_file = '%s.h' % changed
                        header_path = include_dir / header_file
                        if not header_path.isfile():
                                missing.append('%s -> %s' % (changed, header_path))
                        assert '[]' not in changed, changed
                        header = '"%s.h"' % (changed)
                inclusion = '# include %s' % header
                if inclusion not in result:
                        result.append(inclusion)
        return '\n'.join(result)


def template_parts(t):
        template_re = re.compile('([^<]*)<([^>]*)>')
        match = template_re.match(t)
        if match:
                return match.groups()[0], match.groups()[1]
        return None, None


def change_to_pointer(t):
        t = change_type(t)
        if t in simple_types:
                return t
        if t == 'ACE_CString':
                return t
        try:
                if t[-1] == '*':
                        return t
        except IndexError:
                raise ValueError('Empty type: "%s"' % t)
        return '%s*' % t


def change_type(s):
        changes = {
                'String': 'ACE_CString',
                'Integer': 'int',
                'Double': 'double',
                'Vector': 'std::vector',
                'Throwable': 'Exception',
                'boolean': 'bool',
                'byte*': 'byte',
                'RiasStatus': 'RiasStatus::Rias',
        }
        t = changes.get(s, s)
        t1, t2 = template_parts(s)
        if t1:
                t = '%s<%s>' % (change_type(t1), change_type(t2))
        while t.endswith('[]'):
                t = '%s*' % t[:-2]
        use_type(t)
        return t


def write_dotted(parts):
        try:
                return '.'.join(parts)
        except:
                raise ValueError(str(parts))


def write_dynamic(cast, value):
        if cast:
                return '(%s) %s' % (cast, value)
        return value


def write_method(i, j):
        if not i or write_file == 'cpp':
                return j
        return '%s\n%s' % (i, j)


def write_formal_arg(typ, bricks, name):
        typ = change_to_pointer(typ+bricks)
        return '%s %s' % (typ, name)


def write_method_declaration(return_declaration, identifier, formal_args, throws_list):
        if write_file == 'header':
                return '%s %s %s' % (return_declaration, identifier, formal_args)
        for typ in throws_list:
                needed_headers.append('%s.h' % typ)
        return '%s %s::%s %s' % (return_declaration, class_name, identifier,
                                                        formal_args)


def write_return_declararation(return_qualifiers, return_type):
        try:
                return_type = change_to_pointer(return_type)
        except ValueError:
                pass
        if write_file == 'header':
                if return_qualifiers:
                        changes = {
                                'abstract': 'virtual',
                        }
                        qualifiers = [changes.get(q, q) for q in return_qualifiers]
                        ppp = ['private', 'public', 'protected']
                        pq = ' '.join([q for q in qualifiers if q in ppp])
                        others = ' '.join([q for q in qualifiers if q not in ppp])
                        return '%s: %s' % (pq, return_type)
        return return_type


def write_method_stub(method_declaration_text):
        if write_file == 'header':
                return '%s %s;\n' % (indent, method_declaration_text)
        return '/* %s */\n' % method_declaration_text


def change_cpp(text):
        result = []
        if class_name != 'Rias1221Messages':
                text = text.replace('ATTRIBUTE_VALUE_CHANGE_EVENT', 'Rias1221Messages::ATTRIBUTE_VALUE_CHANGE_EVENT')
        byte_class = re.compile(r'\bRiasStatus\b')
        if byte_class.search(text):
                text = byte_class.sub('RiasStatus::Rias', text)
        byte_class = re.compile(r'\bBytes\.')
        if byte_class.search(text):
                text = byte_class.sub('', text)
        constructor_above = re.compile(r'{\s*super(\(.*\));')
        if constructor_above.search(text):
                text = constructor_above.sub(r'\t:%s\1\n{'%bases[0], text)
        text = re.sub(r'\bboolean\b', 'bool', text)
        text = re.sub(r'\bMath\.', '', text)
        above = re.compile(r'\bsuper\b')
        null = re.compile(r'\bnull\b')
        string = re.compile(r'\bString\b')
        bricks = re.compile(r'^(\s+[a-zA-Z_]+\s*)\[\]')
        later_bricks = re.compile(r'^(\s+[a-zA-Z_]+\s+)([a-zA-Z_]+\s*)\[\]')
        array_length = re.compile(r'\b([a-zA-Z_]+)\.length\b')
        math_min = re.compile('Math.min')
        vector_set = re.compile('([a-zA-Z_]*)\.setElementAt.([^,]*), ([^)]*).')
        vector_get = re.compile('([a-zA-Z_]*)\.elementAt.([^)]*).')
        replace = None
        for line in text.splitlines():
                if above.search(line):
                        if not replace:
                                assert len(bases) == 1, str(bases)
                                replace = bases[0]
                        line = above.sub(replace, line)
                if null.search(line):
                        line = null.sub('NULL', line)
                if string.search(line):
                        line = string.sub('ACE_CString', line)
                if bricks.match(line):
                        line = bricks.sub(r'\1*', line)
                if later_bricks.match(line):
                        line = later_bricks.sub(r'\1*\2', line)
                match = array_length.search(line)
                if match:
                        if not line[match.end():].startswith('()'):
                                line = array_length.sub(r'(sizeof(\1)/sizeof(\1[0]))', line)
                if math_min.search(line):
                        line = math_min.sub(r'min', line)
                if vector_set.search(line):
                 line = vector_set.sub(r'\1->at(\2) = \3', line)
                if vector_get.search(line):
                 line = vector_get.sub(r'\1->at(\2)', line)
                result.append(line)
        return '\n'.join(result)


def find_used_symbols(text):
        global needed_headers
        for symbol, header in known_headers.iteritems():
                if symbol in text:
                        needed_headers.append(header)
        known_types = [
                'Bytes',
                'ByteBuffer',
                'WritableByteChannel',
                'ARFCN',
                'RiasEvents',
                'CsActions',
        ]
        for t in known_types:
                if t in text:
                        needed_headers.append('%s.h' % t)


def is_constructor(method_declaration_text):
        parts = method_declaration_text.split()
        if '::' not in parts[0]:
                return False
        name = parts[0]
        parts = name.split('::')
        return parts[0] == parts[1]


def change_constructor(method_declaration_text, block_text):
        if dynamic_attribute_initialisations:
                initialisations = ',\n\t'.join(dynamic_attribute_initialisations)
                return ':\t%s\n%s' % (initialisations, block_text)
        return block_text


def write_method_source(method_declaration_text, block_text):
        find_used_symbols(block_text)
        if write_file == 'header':
                return '%s%s;\n' % (indent, method_declaration_text)
        if is_constructor(method_declaration_text):
                block_text = change_constructor(method_declaration_text, block_text)
        block_text = change_cpp(block_text)
        if block_text.startswith(':'):
                return '%s :\n%s\n' % (method_declaration_text, block_text[1:])
        return '%s\n%s\n' % (method_declaration_text, block_text)


def write_text(i, j):
        global indent
        indent = ''
        return '%s\n%s\n%s;' % (i, include_types(), j)


def write_attribute_allocation(kind, name, qualifiers, dimensions):
        if name == 'logger':
                return ''
        ppp = ['private', 'public', 'protected']
        qualifier_list = qualifiers.split()
        if qualifier_list:
                ppp_string = ' '.join([q for q in qualifier_list if q in ppp])
                access_string = '%s: ' % ppp_string
        else:
                access_string = ''
        other_qualifiers = ' '.join([q for q in qualifier_list if q not in ppp])
        if other_qualifiers:
                other_string = '%s ' % other_qualifiers.replace('final', 'const')
        else:
                other_string = ''
        qualifier_string = '%s%s' % (access_string, other_string)
        kind = change_to_pointer(kind+dimensions)
        return '%s%s %s' % (qualifier_string, kind, name)


def write_attribute_declaration(i, j):
        global dynamic_attribute_initialisations
        if j:
                try:
                        attribute_parts = i.strip().split()
                        attribute = attribute_parts[-1]
                        if 'static' in attribute_parts:
                                attribute = 'static %s' % attribute
                        if attribute == '[]':
                                attribute = attribute_parts[-2]
                except IndexError:
                        if 'getLogger' in j:
                                return ''
                        if (i, j) == ('', ' = null'):
                                return ''
                        raise IndexError('Cannot split these: %r, %r' % (i, j))
                value_parts = j.strip().split()[1:]
                value = ' '.join(value_parts).replace('null', 'NULL')
                find_used_symbols(value)
                if  'static' in attribute_parts:
                        attribute_parts = [a for a in attribute_parts
                                                                if ':' not in a and a not in ['static']]
                        a_list = ';'.join(attribute_parts + [value])
                        static_attribute_initialisations.add(a_list)
                else:
                        initialisation = '%s(%s)' % (attribute, value)
                        dynamic_attribute_initialisations.add(initialisation)
        return '%s;' % i


def write_attribute(comment_text, attribute_declaration_text):
        global indent
        indent = '\t'
        if write_file == 'cpp' or 'getLogger(' in attribute_declaration_text:
                return ''
                return '/* %s */' % attribute_declaration_text
        return '%s\n\t%s' % (comment_text, attribute_declaration_text)


def write_comment(comment_lines):
        if not comment_lines:
                return ''
        joiner = '\n%s* ' % indent
        try:
                line_text = joiner.join(comment_lines)
        except TypeError:
                raise ValueError(str(comment_lines))
        return '%s/**\n%s* %s\n%s*/' % (indent, indent, line_text, indent)


def set_class(name, inheritance):
        global class_name
        class_name = name
        global bases
        if inheritance:
                bases = inheritance.split(', ')
                bases = [change_type(b) for b in bases]
        else:
                bases = []
        return ''


def write_class(name, class_lines, inheritance):
        set_class(name, inheritance)
        if inheritance:
                inheritance = ': %s' % ', '.join([str('public %s' % b) for b in bases])
        else:
                inheritance = ''
        if write_file == 'cpp':
                initialisations = []
                for attribute_initialisation in static_attribute_initialisations:
                        parts = attribute_initialisation.split(';')
                        value = parts[-1]
                        attribute_parts = parts[:-1]
                        attribute_name = '%s::%s' % (class_name, attribute_parts[-1])
                        initialisation = '%s %s = %s;' % (' '.join(attribute_parts[:-1]),
                                                                                        attribute_name, value)
                        initialisations.append(initialisation)
                return '%s\n%s' % ('\n'.join(initialisations), class_lines)
        return 'class %s %s \n{%s\n}' % (class_name, inheritance, class_lines)


def tree_like(l, indent=None):
        if indent is None:
                indent = ''
        if type(l) == type([]):
                print '%s[' % indent
                for item in l:
                        tree_like(item, indent + '\t')
                print '%s]' % indent
        else:
                print '%s%s,' % (indent, l)


class Klass:

        def __init__(self, name):
                self.name = name
                self.attrs = []
                self.methods = []

        def add_attr(self, name):
                self.attrs.append(name)

        def add_method(self, name):
                self.methods.append(name)


rias_cpp_grammar = file('cpp.g').read()
rias_cpp = OMeta.makeGrammar(rias_cpp_grammar, globals(), name="rias_cpp")


def formatAttrs(attrs):
        """
        Format a dictionary to HTML-ish attributes.
        """
        return ''.join([" %s='%s'" % (k, v) for (k, v) in attrs.iteritems()])


def make_header(java, header, name):
        global write_file
        write_file = 'header'
        fred_text = rias_cpp([java]).apply('cpp_text')
        out = file(header, 'w')
        print >> out, '# ifndef %s_H ' % name.upper()
        print >> out, '# define %s_H ' % name.upper()
        print >> out, fred_text
        print >> out, '# endif'
        out.close()


def make_cpp(java, cpp):
        global write_file
        write_file = 'cpp'
        fred_text = rias_cpp([java]).apply('cpp_text')
        out = file(cpp, 'w')
        print >> out, fred_text
        out.close()


def wanted(name):
        ignored = [
                'EarthArea',
        ]
        if name in ignored:
                return False
        if name.startswith('DigitalElevation'):
                return False
        if name.startswith('GTOPO30'):
                return False
        return True


def translate_one(sought):
        top_dir = makepath('../../java')
        java_files = [f for f in top_dir.walkfiles('%s.java' % sought)]
        assert java_files, 'No such file %s/**/%s.java' % (top_dir, sought)
        assert len(java_files) == 1, 'Too many files: %s' % '\n\t'.join(java_files)
        new_dir = makepath('./../translated')
        for f in java_files:
                name = f.namebase
                assert not name.endswith('Test')
                java_lines = rebrace.rebrace(f)
                java_source = '\n'.join(java_lines)
                java_ast = rias_cpp(java_source).apply('cpp_file')
                header = new_dir / str('%s.h' % name)
                cpp = new_dir / str('%s.cpp' % name)
                make_header(java_ast, header, name)
                make_cpp(java_ast, cpp)


def translate_all():
        top_dir = makepath('../java')
        java_files = [f for f in top_dir.walkfiles('*.java')]
        new_dir = makepath('./../translated')
        done = [
        ]
        names = []
        for f in java_files:
                name = f.namebase
                if not wanted(name):
                        continue
                if name in done:
                        continue
                if name.endswith('Test'):
                        continue
                java_lines = rebrace.rebrace(f)
                java_source = '\n'.join(java_lines)
                java_ast = rias_cpp(java_source).apply('cpp_file')
                header = new_dir / str('%s.h' % name)
                cpp = new_dir / str('%s.cpp' % name)
                try:
                        make_header(java_ast, header, name)
                        make_cpp(java_ast, cpp)
                        names.append(name)
                finally:
                        for name in names:
                                print "         '%s'," % name


def glom_cpp_file(l):
        global needed_headers
        needed_headers = []
        used_types.clear()
        dynamic_attribute_initialisations.clear()
        static_attribute_initialisations.clear()
        return l


def glom_return(i, j, k):
        if not j:
                j = ''
        else:
                if k:
                        j = '%s%s' % (j, ''.join(k))
        return [i, j]


def glom_attribute_source(i, j, k):
        comment_before = i
        attribute = j
        comment_after = k
        if comment_before:
                comment = comment_before
        else:
                if comment_after:
                        comment = comment_after
                else:
                        comment = []
        return [comment, attribute]


def main(args):
        for arg in args:
                name = makepath(arg).namebase
                translate_one(name)
        return 0


if __name__ == '__main__':
        sys.exit(main(sys.argv[1:]))
