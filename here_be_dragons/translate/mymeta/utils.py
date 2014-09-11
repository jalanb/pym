import os
import sys

showed_the_warning = [False]
def save_source(source,modname):
	mymeta_directory = './mymeta'
	destination = os.path.join(mymeta_directory,'generated','%s.py' % modname)
	try: file(destination,'w').write(source)
	except IOError:
		if showed_the_warning[0]:
			return
		print >> sys.stderr, 'Warning - could not save debug info to', os.path.abspath(destination)
		showed_the_warning[0] = True
