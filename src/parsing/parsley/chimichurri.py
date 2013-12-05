"""Chimichurri (IRL is a sauce which) uses parsley

This module provides support code for the parsley package

See https://en.wikipedia.org/wiki/Chimichurri for the sauce
"""


import parsley


def _memoized(method, key):
	"""Call that method once with the given key

	Memoize the returned value for subsequent calls
	"""
	try:
		_memoized.cache[key] = _memoized.cache.get(key, None) or method(key)
	except AttributeError:
		_memoized.cache = {key:method(key)}
	return _memoized.cache[key]


def _read_grammar(path_to_grammar):
	"""Make a grammar from the text in that path"""
	grammar_text = file(path_to_grammar).read()
	return _make_grammar(grammar_text)


def _make_grammar(grammar_text):
	"""Make a parsley grammar from the given text

	Do not add any symbols to the made grammar
	"""
	return parsley.makeGrammar(grammar_text, {})


def read_grammar(path_to_grammar):
	"""Re read a grammar from the given file

	Look first in cached grammars in this function
	Then look in generated grammars (NotImplemented)
	Then make a grammar from the given path
	"""
	return _memoized(_read_grammar, path_to_grammar)


