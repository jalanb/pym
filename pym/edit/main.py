#! /usr/bin/env python2
"""Script to edit items"""

import os
import sys
import argparse
from bdb import BdbQuit


from dotsite.getch import yield_asciis
from pym.edit.tree import TreeEditor
from pym.edit.tree import Tundra
from pym.edit import keyboard


def start_debugging():
    try:
        import pudb as pdb
    except ImportError:
        import pdb
    pdb.set_trace()


def parse_args():
    """Parse out command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    pa = parser.add_argument
    pa('items', nargs='*', help='items to be editted')
    pa('-c', '--command', action='store', default=list(), type=str,
       help='act like vim for a string of hjkl commands',)
    pa('-q', '--quiet', action='store_true', help='Show less output')
    pa('-U', '--Use_debugger', action='store_true',
       help='Run the script with pdb (or pudb if available)')
    args = parser.parse_args()
    if args.Use_debugger:
        start_debugging()
    return args


def main():
    """Run the script"""
    try:
        args = parse_args()
        edit3 = TreeEditor(args.items)
        keys = iter(args.command) if args.command else yield_asciis()
        for key in keys:
            try:
                edit3.edit(key, keyboard)
            except Tundra:
                print >> sys.stderr, "Don't go there"
                continue
            print repr(edit3.climber.item())
    except (SystemExit, BdbQuit):
        pass
    #except Exception, e:
        #print >> sys.stderr, e
        #return not os.EX_OK
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
