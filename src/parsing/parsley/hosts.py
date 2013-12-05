"""A script to parse hosts files"""


import os
import sys
from pprint import pprint


import chimichurri


def require_file(path_to_file):
	"""If the given path is not a file then raise ValueError"""
	if os.path.isfile(path_to_file):
		return
	raise ValueError('%r is not a file' % path_to_file)


def read_hosts_grammar():
	"""Make a grammar for hosts files"""
	return chimichurri.read_grammar('hosts.parsley')


def parse_text(text):
	"""Parse the given text as a hosts file"""
	parser_maker = read_hosts_grammar()
	grammar_wrapper = parser_maker(text)
	return grammar_wrapper.hosts()


def parse_path(path_to_hosts):
	"""Parse the hosts file at the given path"""
	require_file(path_to_hosts)
	text = file(path_to_hosts).read()
	return parse_text(text)


def show_parsed_hosts(path_to_hosts):
	"""Parse a hosts file and show the result"""
	parsed = parse_path(path_to_hosts)
	pprint(parsed)


def main(args):
	"""Run the program"""
	for arg in args:
		show_parsed_hosts(arg)
	return os.EX_OK


if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
