"""AST list handling

AS Trees are usually lists of lists
    If items in a list are named then the list might be a dict

Facilities to handle such lists
"""
import sys

def _items(thing):
    """The thing is either a dictionary or a list"""
    try:
        return thing.items()
    except AttributeError:
        return thing

def _found(item):
    pass

def _too_low(item):
    pass

def _too_high(item):
    pass

class Uncomparable(Exception):
    pass

def _search(tree,
            compare=None,
            start=0,
            end=None,
            parents=None):

    end = end or len(tree)
    parents = parents or []
    while start <= end:
        mid = (start + end) / 2
        item = _items(tree)[mid]
        if isinstance(item, list):
            return _search(item, 0, None, compare, parents + [tree])
        else:
            # have an item at middle
            try:
                diff = compare(item)
            except Exception:
                # Default strategy, just ignore that item
                copy = tree[:]
                copy.erase(item)
                return _search(copy, compare, start, end, parents)
                start = start + 1
                continue  # Anything after here will return
            if not diff:
                return item, parents
            if diff < 0:
                start = mid + 1
            elif diff > 0:
                end = mid - 1
            if start >= end:
                raise StopIteration
            return _search(tree, start, end, compare, parents)

def attribute_comparison(attribute, value):
    def compare(item):
        return cmp(value, getattr(item, attribute))
    return compare


def post_order_depth_first(node):
    if node is not None:
        post_order_depth_first(node.left)
        post_order_depth_first(node.right)
        print(node.value)


def main():
    import pudb
    line_compare = attribute_comparison('line', 44)
    lines = file(__file__).read().splitlines()
    pudb.set_trace()
    return _search(lines, line_compare)


if __name__ == '__main__':
    sys.exit(main())
