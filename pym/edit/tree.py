

class Tundra(StopIteration):
    """A Tundra is a "treeless mountain tract"
        [Aapala, Kirsti. "Tunturista jangalle". Kieli-ikkunat](http://www.kotus.fi/julkaisut/ikkunat/1999/kielii1999_19.shtml)  # noqa

    No place for a Climber to be.
    """
    pass


def as_list(item):
    """Make item a list from types which can index, have items, or can pop"""
    # pylint: disable=pointless-statement
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


def tree_editor(tree, keyboard):

    def tree_edit(keys):
        keyboard.move(climber, keys.next())
        return keys, climber

    climber = Climber(tree)
    return tree_edit
