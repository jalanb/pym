"""Provides an index to a tree which can be driven by keys"""


try:
    from colours import colour_text
except ImportError:
    colour_text = lambda x: x


from pym.edit import vim_keys as vim


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
