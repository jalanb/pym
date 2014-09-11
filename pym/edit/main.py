#! /usr/bin/env python2
"""Script to edit items"""

import os
import sys
import argparse
from bdb import BdbQuit


from dotsite.getch import yield_asciis
from pym.edit.index import Index


try:
    from colours import colour_text
except ImportError:
    colour_text = lambda x: x


def start_debugging():
    try:
        import pudb as pdb
    except ImportError:
        import pdb
    pdb.set_trace()


def parse_args():
    """Parse out command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('items', nargs='*',
                        help='items to be editted')
    parser.add_argument('-v', '--hjkl',
                        help='act like vim for a string of hjkl keys',
                        action='store',
                        default=list(),
                        type=str)
    parser.add_argument('-U', '--Use_debugger', action='store_true',
                        help='Run the script with pdb (or pudb if available)')
    args = parser.parse_args()
    if args.Use_debugger:
        start_debugging()
    return args


def highlight(item):
    return colour_text(item, 'red')


def main():
    """Run the script"""
    try:
        args = parse_args()
        i = Index(args.items)
        keys = args.hjkl if args.hjkl else yield_asciis
        args = i.edit(keys, highlight)
        print repr(args)
    except (SystemExit, BdbQuit):
        pass
    #except Exception, e:
        #print >> sys.stderr, e
        #return not os.EX_OK
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
