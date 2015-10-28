"""This module handles lines of text"""


def remove_empty_tail(items):
    if not items or items[-1]:
        return items
    for i, item in enumerate(items[::-1]):
        if item:
            return items[:-i]
    return items



