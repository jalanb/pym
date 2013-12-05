"""A script to parse hosts files"""


import os
import sys
from pprint import pprint


import chimichurri


def read_hosts_grammar():
	"""Make a grammar for hosts files"""
	return chimichurri.read_grammar('hosts.parsley')


def parse_text(input_string):
	"""Parse the given input_string as a hosts file"""
	parser_maker = read_hosts_grammar()
	grammar_wrapper = parser_maker(input_string)
	return grammar_wrapper.hosts()


def require_file(path_to_file):
	"""If the given path is not a file then raise ValueError"""
	if not os.path.isfile(path_to_file):
		raise ValueError('%r is not a file' % path_to_file)


def parse_path(path_to_hosts):
	"""Parse the hosts file at the given path"""
	require_file(path_to_hosts)
	input_string = file(path_to_hosts).read()
	return parse_text(input_string)


def main(args):
	"""Run the program"""
	for arg in args:
		parsed = parse_path(arg)
		pprint(parsed)
	return os.EX_OK


if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
