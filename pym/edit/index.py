"""Provides an index to a tree which can be driven by keys"""


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

    def edit(self, keys, highlight):
        editor = IndexChanger(self, highlight)
        return editor.edit(keys)

    @property
    def item(self):
        return self.items[self.i]

    @item.setter
    def item(self, i):
        self.items[self.i] = i


class IndexChanger(object):
    """Something which can change an index"""
    def __init__(self, index, highlight):
        self.index = index
        self.highlight = highlight

    def _move(self, change, more, ok=None):
        self.index.i = change(self.index.i)
        if not more(self.index.i):
            raise StopIteration
        if ok:
            ok(self.index.i)
        return self.index.i

    def left(self):
        return self._move(lambda x: x - 1, lambda x: x >= 0)

    def down(self):
        def ok(_i):
            self.index.item = self.edit(self.index.item.split(separator))

        separator = ','
        return self._move(
            lambda x: x,
            lambda x: separator in self.index.item,
            ok)

    def up(self):
        # pylint: disable=no-self-use
        raise StopIteration

    def right(self):
        return self._move(lambda x: x + 1, lambda x: x <= self.index.length)

    def render(self):
        return self.highlight(self.index.item)

    def show(self):
        saved = self.index.item
        try:
            self.index.item = self.render()
            print ' '.join(self.index.items)
        finally:
            self.index.item = saved

    def edit(self, keys=None):
        """Read keys to move an index around a tree"""
        if keys:
            self.index.keys = keys
        self.show()
        for key in keys:
            vim.call(self, key)
            self.show()
