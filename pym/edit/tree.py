"""Provides an index to a tree which can be driven by keys"""


from pym.edit import vim_keys as vim


class Items(object):
    """Items are often a tree of lists"""
    def __init__(self, tree):
        self.items = tree

    def edit(self, keys, highlight):
        editor = IndexEditor(highlight)
        editor.index(self.items)
        return editor.edit(keys)


class IndexEditor(object):
    """Something which can a tree via an index into it

    Move around the tree, and redraws as needed, responding to keys
    """
    def __init__(self, highlight):
        self.i = 0
        self.highlight = highlight
        self._items = None

    def editor(self):
        changer = IndexEditor(self.highlight)
        changer.unused_keys = self.unused_keys
        return changer

    def index(self, items):
        """Start an index on those items"""
        self._items = items
        self.length = len(self.items)

    @property
    def items(self):
        if self._items is None:
            raise NotImplementedError('Please call index(items) first')
        if not self._items:
            return []
        return self._items

    @property
    def item(self):
        if self.i >= self.length:
            raise StopIteration
        return self.items[self.i]

    @item.setter
    def item(self, item):
        self.items[self.i] = item

    def render(self):
        return self.highlight(self.item)

    def show(self, i):
        assert self.i == i
        saved = self.item
        try:
            self.item = self.render()
            print ' '.join([i for i in self.items if i])
        finally:
            self.item = saved

    def edit(self, keys=None):
        """Read keys to move an index around a tree"""
        self.show(0)
        if keys:
            self.unused_keys = keys
        for key in self.unused_keys[:]:
            self.unused_keys = self.unused_keys[1:]
            i = vim.call(IndexMover(self), key)
            self.show(i)
        return self.items


class IndexMover(object):
    """Can move an index up/down/left/right"""
    def __init__(self, index):
        self.index = index
        self.editor = index.editor()

    def _move(self, change, keep_going, post_move):
        """RTFS"""
        if change:
            self.index.i = change(self.index.i)
        if not keep_going(self.index.i):
            raise StopIteration
        if post_move:
            self.index.item = post_move(self.index.item)
        return self.index.i

    def up(self):
        # pylint: disable=no-self-use
        raise StopIteration

    def left(self):
        return self._move(
            change=lambda x: x - 1,
            keep_going=lambda x: x >= 0,
            post_move=None)

    def right(self):
        return self._move(
            change=lambda x: x + 1,
            keep_going=lambda x: x <= self.index.length,
            post_move=None)

    def down(self):
        def post_move(item):
            self.editor.index(item.split(separator))
            return self.editor.edit()

        separator = ','
        return self._move(
            change=None,
            keep_going=lambda x: separator in self.index.item,
            post_move=post_move)
