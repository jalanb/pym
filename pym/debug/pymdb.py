"""Debug a method"""



def _read_line_from_path(path):
    import linecache # Import as late as possible

    def read(i):
        return linecache.getline(path, i).rstrip()

    return read

def _lines_before_at_same_indentation(read, end):
    """This method could not work on itself

    because it sub-defines other methods within itself
        and could have indentation in the main body
        "deeper" than one of the sub-defines
        so would only give lines back that far
        not the full block

    Gonna need a parsing solution
    """
    def extract_match(regexp, string):
        match = regexp.match(string)
        try:
            return match.string[:match.end()]
        except AttributeError as e:
            return ''

    def make_finder(regexp):
        def finder(string):
            return extract_match(regexp, string)
        return finder

    def make_find(regexp, string):
        finder = make_finder(regexp)
        first_find = finder(string)
        def find(text):
            return finder(text) == first_find
        return find

    import re
    from itertools import takewhile

    starts_with_spaces = re.compile('(^$)|(^ +)')
    find = make_find(starts_with_spaces, read(end))
    lines = takewhile(lambda i: find(read(i)), range(end, 0, -1))
    return reversed([read(i) for i in lines])

def lines_in_frame(path, line):
    pudb.set_trace()
    from pym.edit.tree import Climber
    from pym.ast.parse import parse_path
    climber = Climber(parse_path(path))
    climber.to_line(line)


def set_trace():
    from pprintpp import pprint as pp
    def ppd(_):
        return pp(dir(_))

    def ppv(_):
        return pp(vars(_))

    import pudb
    import inspect
    sources = [(path, line) for _, path, line, _, _, _ inspect.stack()]
    path, line = sources[-1]
    read = _read_line_from_path(path)
    lines = lines_in_frame(path, line)
    text = '\n'.join(lines)
    print text
    pudb.set_trace()
