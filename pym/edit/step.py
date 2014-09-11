"""Walk a tree in small steps

Often in response to a keyboard
"""


from pym.edit import vim_keys as vim


class Keys(object):
    """Provide attributes which match names known by given translators

    The default translators include only vim so far
    """
    def __init__(self, translators=None):
        """

        >>> my_keys = { 'space' : ' ' }
        >>> keys = Keys(my_keys)
        >>> ' ' in keys.space
        True
        """
        import pudb
        pudb.set_trace()
        if translators is None:
            translators = [vim.keys]
        for translator in translators:
            for key, value in translator.items():
                if not hasattr(self, value):
                    setattr(self, value, [])
                keys = getattr(self, value)
                keys.append(key)


class Node(object):
    def __init__(self, parent, items):
        self.parent = parent
        self.child = items[0]
        self.next = items[1:]


class Tree(object):
    def __init__(self, items):
        self.parent = None
        self.next = Node(self, items)


node = Tree([1, 2, 3])


def step_(direction):
    keys = Keys()
    if direction in keys.up:
        yield node.parent
    elif direction in keys.right:
        yield node.next
    elif direction in keys.down:
        yield node.branch
    else:
        raise NotImplementedError

right = step_('l')
print list(right)[0]
