"""Methods to aid testing parsely grammars"""


def _try_all(target, tests, try_method):
	"""Accumulate results for that target against all those tests"""
	tests_result = True
	for test in tests:
		test_result = try_method(target, test)
		tests_result &= test_result
	return tests_result


def _actual_match(target, test):
	"""Try to parse that target to that test

	test is either a tuple of (actual, expected) results
		or a single actual result (which == expected)
	"""
	try:
		string, expected = test
	except ValueError:
		string = expected = test
	return string, expected, try_parse(target, string)


def _try_match_quietly(target, test):
	"""Try to match that target aginst that test, do not show fails"""
	_, expected, actual = _actual_match(target, test)
	return actual == expected


def _parse(target, string):
	"""Try to match that string against that target in the current grammar"""
	instance = instantiate(string)
	if not instance:
		raise KeyboardInterrupt('Call use_grammar() before try_parse()')
	method = getattr(instance, target, None)
	if not method:
		raise ValueError('No such target: %r' % target)
	try:
		return method(), None
	except Exception, e:
		return None, str(e).splitlines()[-1]


def use_grammar(grammar):
	"""Use that grammar in subsequent tests"""
	use_grammar.grammar = grammar


def instantiate(string):
	"""Instantiate the current grammar with that string"""
	try:
		return use_grammar.grammar(string)
	except AttributeError:
		return None


def try_parse(target, string):
	"""Try to parse for that target in that string

	Show any errors on stdout
	"""
	result, error = _parse(target, string)
	if error:
		print error
	return result


def try_error(target, string):
	"""Try to generate an error from parsing for that target in that string"""
	_, error = _parse(target, string)
	return bool(error)


def try_match(target, test):
	"""Try to match that target against that test

	The test is a tuple of (actual, expected) results
	If the test fails show failure on stdout
	"""
	string, expected, actual = _actual_match(target, test)
	if actual != expected:
		print 'Not matched: %r -> %r, not %r' % (string, actual, expected)
		return False
	return True


def try_matches(target, tests):
	"""Try to match that target to all those tests

	Each test is a tuple of (actual, expected) results
	"""
	return _try_all(target, tests, try_match)


def try_non_matches(target, tests):
	"""Try to not match that target against those tests

	Each test is a tuple of (actual, expected) results
	"""
	tests_result = False
	for test in tests:
		test_result = _try_match_quietly(target, test)
		tests_result |= test_result
	return not tests_result


def try_errors(target, tests):
	"""Try to generate an error from parsing for that target with those tests"""
	return _try_all(target, tests, try_error)


def try_target(target, errors, matches):
	"""Try to match that target, giving thos errors and those matches"""
	return try_errors(target, errors) and try_matches(target, matches)


def verify_target(target, errors, matches, non_matches):
	"""Verify that target with the other arguments"""
	return try_errors(target, errors) and try_matches(target, matches) and try_non_matches(target, non_matches)
