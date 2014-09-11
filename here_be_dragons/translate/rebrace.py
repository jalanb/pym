from path import path
import sys
import re

def read_lines(filename):
	return [ l.rstrip() for l in path(filename).lines() ]

def read_indent(line):
	indent = ''
	for c in line:
		if not c.isspace(): break
		indent += c
	return indent


empty = re.compile('\{([^\}]*)\}(.*)')

def start(lines):
	result = []
	for line in lines:
		parts = line.split('//')
		if len(parts) > 1:
			if not parts[0]: continue
			if parts[0][-1] != ':':
				line = parts[0]
		if empty.search(line):
			indent = read_indent(line)
			groups = empty.search(line).groups()
			content = groups[0].strip()
			rest = groups[1].strip()
			result += [ empty.sub('{',line) ]
			if content:
				result += [ '%s\t%s' % (indent,content) ]
			line = '%s}%s' % (indent,rest)
		result += [ line.rstrip() ]
	return result

def one(lines):
	result = []
	for line in lines:
		if line and line[-1] == '{' and not line[:-1].isspace():
			result += [ line[:-1].rstrip() ]
			indent = read_indent(line)
			line = '%s{' % indent
		result += [ line.rstrip() ]
	return result

def two(lines):
	result = []
	for line in lines:
		if '}' in line[:-2]:
			indent = read_indent(line)
			splitter = '%s}' % indent
			joiner = '%s}\n\t' % indent
			line = joiner.join(line.split(splitter))
		result += [ line.rstrip() ]
	return result

def three(lines):
	copyright = [
		'/**',
		' * (c) Altobridge, 2009',
		' */',
	]
	result = []
	prev = ''
	comments = 0
	for line in lines:
		words = line.split()
		try:
			if not line[0].isspace():
				if 'class' in words[:3] or 'interface' in words[:3]:
					if comments < 1:
						result[:0] = copyright[:]
					if comments < 2:
						result.extend([ '/* ', ' * describe this class here', ' */' ])
					comments = 3
		except IndexError: pass
		if line.startswith('/*'):
			comments += 1
		result.append(line)
	return result

def rebrace(filename):
	lines = read_lines(filename)
	for word in [ 'package', 'import' ]:
		lines = [ l for l in lines if not l.startswith('%s ' % word) ]
	for word,repl in [ ('final','const ') ]:
		regex = re.compile(r'\b%s\b\s*' % word)
		lines = [ regex.sub(repl,l) for l in lines ]
	for method in [ start, one, two, three ]:
		lines = method(lines)
	return [ l.rstrip() for l in lines if l.strip() ]

def main(filename):
	lines = rebrace(filename)
	path(filename).write_lines(lines)
	path(filename.replace('.java','.cpp')).write_lines(lines)
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1]))
