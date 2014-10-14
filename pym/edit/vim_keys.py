"""Provide keys similar to vim's"""


keys = {
    'h': 'left',
    'j': 'down',
    'k': 'up',
    'l': 'right',
}


def call(methods, key):
    if key in keys:
        method = methods[keys[key]]
        return method()

move = call
