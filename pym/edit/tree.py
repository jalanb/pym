

from itertools import chain


class Brancher(object):
    """Walks right / left along a list of items"""
    def __init__(self, items):
        self._try(0, items)

    def _try(self, j, items = None):
        try:
            if items:
                self.items = items
            self.items[j]
        except (TypeError, IndexError):
            raise StopIteration
        self.i = j

    @property
    def item(self):
        return self.items[self.i]

    def right(self):
        self._try(self.i + 1)

    def left(self):
        self._try(self.i - 1)


class Climber(Brancher):
    """Climbs up / down a list of lists"""

    def up(self):
        # pylint: disable=no-self-use
        raise StopIteration

    def down(self):
        self.climber = Climber(self.item)

    def item(self):
        try:
            return self.climber.item()
        except AttributeError:
            return super(Climber, self).item()


class TreeEditor(object):
    def __init__(self, tree):
        self.climber = Climber(tree)
        self.keys = []

    def edit(self, keys, keyboard):
        self.keys = chain([self.keys, keys])
        keyboard.move(self.climber, self.keys.next())
