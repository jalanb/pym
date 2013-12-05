"""A module to provide methods to parse hosts files"""


import os
import sys
from pprint import pprint


import chimichurri


def read_hosts_grammar():
	"""Make a grammar for hosts files"""
	return chimichurri.read_makeParser('hosts.parsley')


def parse_text(input_string):
	"""Parse the given input_string as a hosts file"""
	parser_maker = read_hosts_grammar()
	grammar_wrapper = parser_maker(input_string)
	return grammar_wrapper.hosts()


def parse_path(hosts_file):
	if not os.path.isfile(hosts_file):
		raise ValueError('%r is not a file' % hosts_file)
	input_string = file(hosts_file).read()
	return parse_text(input_string)


def main(args):
	for arg in args:
		parsed = parse_path(arg)
		pprint(parsed)
	return os.EX_OK

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
