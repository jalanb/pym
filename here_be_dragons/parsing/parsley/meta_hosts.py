"""A script to parse the hosts.parsley file"""


import os
import sys
from pprint import pprint

import chimichurri


def read_parsley_grammar():
    """Make a grammar for hosts grammar"""
    symbols = {}
    return chimichurri.read_grammar_with_symbols('parsley.parsley', symbols)


def parse_text(input_string):
    """Parse the given input_string as a parsley file"""
    grammar = read_parsley_grammar()
    grammar_wrapper = grammar(input_string)
    return grammar_wrapper.grammar()


def parse_path(parsley_file):
    if not os.path.isfile(parsley_file):
        raise ValueError('%r is not a file' % parsley_file)
    input_string = file(parsley_file).read()
    return parse_text(input_string)


def main(args):
    parsed = parse_path('hosts.parsley')
    pprint(parsed, args)
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
