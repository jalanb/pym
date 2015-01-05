"""Provide keys similar to vim's"""


keys = {
    'h': 'left',
    'j': 'down',
    'k': 'up',
    'l': 'right',
}


def call(thing, key):
    if key in keys:
        method = getattr(thing, keys[key])
        return method()

move = call
