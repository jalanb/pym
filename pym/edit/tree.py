import re

from pysyte.types.lists import as_list


class Tundra(StopIteration):
    """A Tundra is a "treeless mountain tract"
        Aapala, Kirsti. "Tunturista jangalle". Kieli-ikkunat
        http://www.kotus.fi/julkaisut/ikkunat/1999/kielii1999_19.shtml

    No place for a Climber to be.
    """

    pass


class Brancher(object):
    """Walks right / left along a list of items"""

    def __init__(self, thing):
        self._try(0, as_list(thing))

    def _try(self, j, items=None):
        try:
            if items:
                self.items = items
            assert j >= 0
            # pylint: disable=pointless-statement
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

    def home(self):
        self._try(0)

    def end(self):
        self._try(len(self.items) - 1)


class Climber(Brancher):
    """Climbs up / down a list of lists"""

    def __init__(self, thing, parent=None):
        self.parent = parent
        super(Climber, self).__init__(thing)

    def up(self):
        if not self.parent:
            raise Tundra
        return self.parent

    def down(self):
        item = self.item()
        try:
            if re.match("^.$", item):
                raise Tundra
        except TypeError:
            pass
        return Climber(self.item(), self)

    def indices(self):
        indices = super(Climber, self).indices()
        try:
            return indices + self.climber.indices()
        except AttributeError:
            return indices


class TreeEditor(object):
    def __init__(self, tree):
        self.climber = Climber(tree)

    def edit(self, key, keyboard):
        climber = keyboard.move(self.climber, key)
        if climber:
            self.climber = climber
        return self.climber.item()
