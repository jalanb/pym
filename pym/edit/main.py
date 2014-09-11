#! /usr/bin/env python2
"""Script to """

import os
import sys
import argparse
from bdb import BdbQuit


from dotsite.getch import yield_asciis
from colours import colour_text
from pym.edit import vim_keys as vim


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


class Index(object):
    """An integer to a tree (as lists)"""
    def __init__(self, items, key_getter):
        self.i = 0
        self.items = items
        self.length = len(items)
        self.key_getter = key_getter

    def _move(self, change, more, ok=None):
        self.i = change(self.i)
        if not more(self.i):
            raise StopIteration
        if ok:
            ok(self.i)
        return self.i

    def left(self):
        return self._move(lambda x: x - 1, lambda x: x >= 0)

    def down(self):
        def ok(i):
            self.items[i] = edit(items, key_getter)

        return self._move(lambda x: x, lambda x: ',' in items[self.i], ok)

    def up(self):
        return None

    def right(self):
        return self._move(lambda x: x + 1, lambda x: x <= len(items))


def edit(items, key_getter):

    methods = locals().copy()
    i = Index(len(items))
    show(items, i)
    for key in next(key_getter()):
        i = vim.call(i, key)
        show(items, i.i)
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
