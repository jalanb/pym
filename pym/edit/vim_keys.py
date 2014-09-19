"""Provide keys similar to vim's"""


keys = {
    'h': 'left',
    'j': 'down',
    'k': 'up',
    'l': 'right',
}


def call(index, key):
    if key in keys:
        method = getattr(index, keys[key])
        return method()
