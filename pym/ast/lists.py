"""AST list handling

AS Trees are usually lists of lists
    If items in a list are named then the list might be a dict

Facilities to handle such lists
"""


def _items(thing):
    """The thing is either a dictionary or a list"""
    try:
        return thing.items()
    except AttributeError:
        return thing


def _found(_item):
    pass


def _too_low(_item):
    pass


def _too_high(_item):
    pass


class Uncomparable(Exception):
    pass


def _search(tree, compare, start=0, end=None, parents=None):

    end = end or len(tree)
    parents = parents or []
    while start <= end:
        mid = (start + end) / 2
        item = _items(tree)[mid]
        parents.append(item)
        if isinstance(item, list):
            return _search(item, compare, 0, None, parents)
        else:
            # have an item at middle
            try:
                diff = compare(item)
            except Exception:  # pylint: disable=broad-except
                # Default strategy, just ignore that item
                copy = tree[:]
                copy.remove(item)
                if not copy:
                    return -1
                return _search(copy, compare, start, end - 1, parents)
                start = start + 1  # pylint: disable=unreachable
                continue  # Anything after here will return
            if not diff:
                return item, parents
            if diff > 0:
                start = mid + 1
            elif diff < 0:
                end = mid - 1
            if start >= end:
                raise StopIteration
            return _search(tree, compare, start, end, parents)


def attribute_comparison(attribute, value):
    def compare(item):
        attr_value = getattr(item, attribute)
        return cmp(value, attr_value)  # pylint: disable=undefined-variable

    return compare


def post_order_depth_first(node):
    if node is not None:
        post_order_depth_first(node.left)
        post_order_depth_first(node.right)
        print(node.value)


class Line(object):
    def __init__(self, i, s):
        self.line = i
        self.string = s

    def __str__(self):
        return self.string

    def __int__(self):
        return self.line
