"""Chimichurri (IRL is a sauce which) uses parsley

This module provides support code for the parsley package

See https://en.wikipedia.org/wiki/Chimichurri for the sauce
"""


import parsley


def _memoized(method, args):
    """Call that method once with the given args

    Memoize the returned value for subsequent calls
    """
    key = repr(args)
    try:
        _memoized.cache[key] = _memoized.cache.get(key, None) or method(key)
    except AttributeError:
        _memoized.cache = {key:method(args)}
    return _memoized.cache[key]


def _read_grammar(key):
    """Make a grammar from the text in that path"""
    path_to_grammar, symbols = key
    grammar_text = file(path_to_grammar).read()
    return _make_grammar(grammar_text, symbols)


def _make_grammar(grammar_text, symbols):
    """Make a parsley grammar from the given text

    Do not add any symbols to the made grammar
    """
    return parsley.makeGrammar(grammar_text, symbols)


def read_grammar(path_to_grammar):
    """Re read a grammar from the given file"""
    return read_grammar_with_symbols(path_to_grammar, {})


def read_grammar_with_symbols(path_to_grammar, symbols):
    """Re read a grammar from the given file

    Look first in cached grammars in this function
    Then look in generated grammars (NotImplemented)
    Then make a grammar from the given path
    """
    return _memoized(_read_grammar, (path_to_grammar, symbols))



def minimal_grammar():
    """Make a tiny grammar, especially for testing"""
    return _make_grammar('target = letter', {})
