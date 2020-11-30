"""Provide keys based on vim's"""


vim_keys = {
    "h": "left",
    "j": "down",
    "k": "up",
    "l": "right",
}

home_row = {
    "a": "add",
    "s": "search",
    "d": "delete",
    "f": "fix",
    "g": "go",
    ";": "mode",
}

home_row.update(vim_keys)

HOME_row = {
    "A": "insert",
    "S": "substitute",
    "D": "destroy",
    "F": "fuck",
    "G": "debug",
    "H": "home",
    "J": "downer",
    "K": "upper",
    "L": "end",
    ":": "command",  # TODO: ensure that <CAPS-;> == <:>
}

keys = {}
_ = map(keys.update, [home_row, HOME_row])


def move(instance, key):
    if key in keys:
        method = getattr(instance, keys[key], None)
        if method:
            return method()
