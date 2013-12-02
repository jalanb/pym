"""Chimichurri (IRL is a sauce which) uses parsley

This module provides support code for the parsley package

See http://www.simplyrecipes.com/recipes/chimichurri/ for the sauce
"""

import parsley


def read_grammar(path_to_grammar):
	"""Re read a grammar from the given file

	Look first in cached grammars in this function
	Then look in generated grammars (NotImplemented)
	Then make a grammar from the given path
	"""
	cached_grammars = getattr(read_grammar, 'cached_grammars', {})
	if not cached_grammars:
		setattr(read_grammar, 'cached_grammars', {})
	cached_grammar = cached_grammars.get(path_to_grammar, None)
	if not cached_grammar:
		cached_grammar = _read_grammar(path_to_grammar)
		cached_grammars[path_to_grammar] = cached_grammar
	setattr(read_grammar, 'cached_grammars', cached_grammars)
	return cached_grammar


def _read_grammar(path_to_grammar):
	"""Make a grammar from the text in that path"""
	grammar_text = file(path_to_grammar).read()
	return _make_grammar(grammar_text)


def _make_grammar(grammar_text):
	"""Make a parsley grammar from the given text

	Do not add any symbols to the made grammar
	"""
	return parsley.makeGrammar(grammar_text, {})


