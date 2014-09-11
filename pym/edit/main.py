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


class Index(object):
    """Map an index to a tree of lists

    Accepts messages like "left", "down", ... from some keys
    """
    def __init__(self, tree):
        self.i = 0
        self.items = tree
        self.length = len(self.items)
        self.keys = ['k']  # up from the root gets you out, allegedly
        self.retreat = False

    def _move(self, change, more, ok=None):
        self.i = change(self.i)
        if not more(self.i):
            raise StopIteration
        if ok:
            ok(self.i)
        return self.i

    @property
    def _item(self):
        return self.items[self.i]

    @_item.setter
    def _item(self, i):
        self.i = i

    def left(self):
        return self._move(lambda x: x - 1, lambda x: x >= 0)

    def down(self):
        def ok(i):
            self.items[i] = self.edit()

        return self._move(lambda x: x, lambda x: ',' in self._item, ok)

    def up(self):
        # pylint: disable=no-self-use
        raise StopIteration

    def right(self):
        return self._move(lambda x: x + 1, lambda x: x <= self.length)

    def render(self):
        return colour_text(self._item, 'red')

    def show(self):
        saved = self._item
        try:
            self._item = self.render()
            print ' '.join(self.items)
        finally:
            self._item = saved

    def edit(self, keys=None):
        """Read keys to move an index around a tree"""
        if keys:
            self.keys = keys
        self.show()
        for key in self.keys:
            vim.call(self, key)
            self.show()


def parse_args():
    """Parse out command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('items', nargs='*',
                        help='items to be editted')
    parser.add_argument('-v', '--hjkl',
                        help='act like vim for a string of hjkl keys',
                        nargs='+',
                        action="append",
                        default=list(),
                        type=str)
    parser.add_argument('-U', '--Use_debugger', action='store_true',
                        help='Run the script with pdb (or pudb if available)')
    args = parser.parse_args()
    if args.Use_debugger:
        start_debugging()
    return args


def main():
    """Run the script"""
    try:
        args = parse_args()
        i = Index(args.items)
        keys = args.hjkl if args.hjkl else yield_asciis
        args = i.edit(keys)
        print args
    except (SystemExit, BdbQuit):
        pass
    #except Exception, e:
        #print >> sys.stderr, e
        #return not os.EX_OK
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
