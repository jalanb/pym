"""Debug a method"""
import os
import json

import ipdb

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
    ipdb.set_trace()
    from pym.edit.tree import Climber
    from pym.ast.parse import parse_path
    climber = Climber(parse_path(path))
    climber.to_line(line)


def path_to_breakpoints():
    return os.path.expanduser('~/.config/pym/breaks.json')


def save_breaks(breakpoints):
    with open(path_to_breakpoints(), 'w') as stream:
        return json.dump(breakpoints, stream)

def break_here():
    with open(path_to_breakpoints()) as stream:
        return json.load(stream)


def continue_(_frame):
    raise NotImplementedError('To do: running in Pym')


def set_trace():
    class SourceFrame(object):
        import linecache # lazy import
        def __init__(self, path, i):
            self.path = path
            self.i = i

        def __str__(self):
            linecache.getline(self.path, self.i).rstrip()

    sources = [(path, line) for _, path, line, _, _, _ in inspect.stack()]
    read = _line_reader(path)
    lines = lines_in_frame(path, line)
    text = '\n'.join(lines)
    print(text)
    ipdb.set_trace()
