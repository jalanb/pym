#! /usr/bin/env python2
"""Script to """

import os
import sys
import argparse
from bdb import BdbQuit


from dotsite.getch import yield_asciis
from colours import colour_text


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
    parser.add_argument('-U', '--Use_debugger', action='store_true',
                        help='Run the script with pdb (or pudb if available)')
    args = parser.parse_args()
    if args.Use_debugger:
        start_debugging()
    return args


def show(items, i):
    saved = items[i]
    try:
        items[i] = colour_text(items[i], 'red')
        print ' '.join(items)
    finally:
        items[i] = saved


def edit(items, key_getter):

    def move(i, change, more, ok=None):
        i = change(i)
        if not more(i):
            raise StopIteration
        if ok:
            ok(i)
        show(items, i)
        return i

    def left(i):
        return move(i, lambda x: x - 1, lambda x: x >= 0)

    def right(i):
        return move(i, lambda x: x + 1, lambda x: x <= len(items))

    def down(i):
        def ok(i):
            items[i] = edit(items, key_getter)

        return move(i, lambda x: x, lambda x: ',' in items[i], ok)

    def up(_i):
        return None

    directions = {
        'h': left,
        'j': down,
        'k': up,
        'l': right,
    }
    i = 0
    show(items, i)
    for key in next(key_getter()):
        i = directions[key](i)
        if i is None:
            return items


def main():
    """Run the script"""
    try:
        args = parse_args()
        items = edit(args.items, yield_asciis)
        print items
    except (SystemExit, BdbQuit):
        pass
    #except Exception, e:
        #print >> sys.stderr, e
        #return not os.EX_OK
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
