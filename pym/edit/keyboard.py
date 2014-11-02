"""Provide keys similar to vim's"""


vim_keys = {
    'h': 'left',
    'j': 'down',
    'k': 'up',
    'l': 'right',
}

home_row = {
    'a': 'add',
    's': 'search',
    'd': 'delete',
    'f': 'fix',
    'g': 'go',
    ';': 'mode',
}

home_row.update(vim_keys)

HOME_row = {
    'A': 'insert',
    'S': 'substitute',
    'D': 'destroy',
    'F': 'fuck',
    'G': 'debug',
    'H': 'home',
    'J': 'downer',
    'K': 'upper',
    'L': 'end',
    ':': 'command',  # TODO: ensure that <CAPS-;> == <:>
}

keys = {}
_ = map(keys.update, [home_row, HOME_row])


def call(methods, key):
    if key in keys:
        method = methods[keys[key]]
        return method()

move = call
