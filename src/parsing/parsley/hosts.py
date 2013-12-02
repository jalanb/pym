"""A module to provide methods to parse hosts files"""


import os
import sys
from pprint import pprint


import chimichurri


def read_hosts_grammar():
	"""Make a grammar for hosts files"""
	return chimichurri.read_grammar('hosts.parsley')


def parse_text(string):
	"""Parse the given string as a hosts file"""
	grammar = read_hosts_grammar()
	parser = grammar(string)
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
