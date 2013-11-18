"""A module to provide methods to parse hosts files"""


import os
import sys
from pprint import pprint


import parsley


def make_hosts_grammar():
	path_to_grammar = 'hosts.parsley'
	grammar_text = file(path_to_grammar).read()
	make_parser = parsley.makeGrammar(grammar_text, {})
	return make_parser


def parse_text(string):
	"""Parse the given string as a hosts file"""
	make_parser = getattr(parse_text, 'make_parser', None)
	if not make_parser:
		make_parser = make_hosts_grammar()
		setattr(parse_text, 'make_parser', make_parser)
	parser = make_parser(string)
	return parser.hosts()


def parse_path(hosts_file):
	if not os.path.isfile(hosts_file):
		raise ValueError('%r is not a file' % hosts_file)
	return parse_text(file(hosts_file).read())


def main(args):
	for arg in args:
		parsed = parse_path(arg)
		pprint(parsed)
	return os.EX_OK

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
