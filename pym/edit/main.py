#! /usr/bin/env python2
"""Script to edit items as a tree"""

import os
import sys
import argparse
from bdb import BdbQuit

import dotsite as site
from pym.edit.tree import TreeEditor
from pym.edit.tree import Tundra
from pym.edit import keyboard
from pym.render import render


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
    """Edit items as a tree"""
    try:
        args = parse_args()
        items = eval(' '.join(args.items))  # pylint: disable=eval-used
        edit3 = TreeEditor(items)
        keys = iter(args.command) if args.command else site.getch.yield_asciis()
        for key in keys:
            try:
                edit3.edit(key, keyboard)
            except Tundra:
                print >> sys.stderr, "Don't go there"
                continue
            print render(edit3.climber.item())
    except (SystemExit, BdbQuit):
        pass
    #except Exception, e:
        #print >> sys.stderr, e
        #return not os.EX_OK
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
