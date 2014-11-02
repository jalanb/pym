#! /usr/bin/env python2
"""Script to edit items"""

import os
import sys
import argparse
from bdb import BdbQuit


from dotsite.getch import yield_asciis
from pym.edit.tree import tree_editor
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
       help='keys to use for editting',)
    pa('-U', '--Use_debugger', action='store_true',
       help='Run the script with pdb (or pudb if available)')
    args = parser.parse_args()
    if args.Use_debugger:
        start_debugging()
    return args


def edit(items, command):
    """Use keys to edit the items

    If the command yields chars, take keys from that
        otherwise from a keyboard
    """
    editor = tree_editor(items, keyboard)
    keys = []
    keys[0] = [command if command else yield_asciis]

    def print_editor():
        keys[0], cursor = editor(keys[0])
        print repr(cursor.items)
    return print_editor


def main():
    """Run the script"""
    try:
        args = parse_args()
        editor = edit(args.items, args.command)
        while True:
            editor()
    except (SystemExit, BdbQuit):
        pass
    #except Exception, e:
        #print >> sys.stderr, e
        #return not os.EX_OK
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
