import os
import sys

showed_the_warning = [False]

def save_source(source, modname):
	destination = f"./mymeta/generated/{modname}.py"
	try:
        file(destination,'w').write(source)
	except IOError:
		if showed_the_warning[0]:
			return
        path = os.path.abspath(destination)
        print(f"Warning - could not save debug info to {path}", file=sys.stderr)
		showed_the_warning[0] = True
