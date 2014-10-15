

from itertools import chain


class Tundra(StopIteration):
    """A Tundra is a "treeless mountain tract"
        [Aapala, Kirsti. "Tunturista jängälle". Kieli-ikkunat](http://www.kotus.fi/julkaisut/ikkunat/1999/kielii1999_19.shtml)

    No place for a TreeClimber to be.
    """
    pass


def as_list(self, item):
    """Make item a list from types which can index, have items, or can pop"""
    try:
        item.index
        return item
    except AttributeError:
        try:
            return item.items()
        except AttributeError:
            try:
                item.pop
                return list(item)
            except AttributeError:
                raise Tundra


class Brancher(object):
    """Walks right / left along a list of items"""
    def __init__(self, thing):
        self._try(0, as_list(thing))

    def _try(self, j, items = None):
        try:
            if items:
                self.items = items
            assert j >= 0
            self.items[j]
        except (AssertionError, TypeError, IndexError):
            raise Tundra
        self.i = j

    def indices(self):
        return [self.i]

    def item(self):
        items = self.items
        for i in self.indices():
            items = items[i]
        return items

    def right(self):
        self._try(self.i + 1)

    def left(self):
        self._try(self.i - 1)


class Climber(Brancher):
    """Climbs up / down a list of lists"""

    def up(self):
        self.older = self.climber
        del self.climber

    def down(self):
        try:
            self.climber = self.older
        except AttributeError:
            self.climber = Climber(self.item())

    def indices(self):
        indices = super(Climber. self).indices()
        try:
            return indices + self.climber.indices()
        except AttributeError:
            return indices


class TreeEditor(object):
    def __init__(self, tree):
        self.climber = Climber(tree)
        self.keys = []

    def edit(self, keys, keyboard):
        self.keys = chain([self.keys, keys])
        keyboard.move(self.climber, self.keys.next())
