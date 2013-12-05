"""Methods to aid testing parsely grammars"""


def _try_all(target, tests, try_method):
	tests_result = True
	for test in tests:
		test_result = try_method(target, test)
		tests_result &= test_result
	return tests_result


def _actual_match(target, test):
	try:
		string, expected = test
	except ValueError:
		string = expected = test
	return string, expected, try_parse(target, string)


def _try_match_quietly(target, test):
	_, expected, actual = _actual_match(target, test)
	return actual == expected


def _parse(target, string):
	instance = instantiate(string)
	if not instance:
		raise KeyboardInterrupt('Call use_grammar() before try_parse()')
	method = getattr(instance, target, None)
	if not method:
		print 'No such target: %r' % target
	try:
		return method(), None
	except Exception, e:
		return None, str(e).splitlines()[-1]


def use_grammar(grammar):
	use_grammar.grammar = grammar


def instantiate(string):
	try:
		return use_grammar.grammar(string)
	except AttributeError:
		return None


def try_parse(target, string):
	result, error = _parse(target, string)
	if error:
		print error
	return result


def try_error(target, string):
	_, error = _parse(target, string)
	return bool(error)


def try_match(target, test):
	string, expected, actual = _actual_match(target, test)
	if actual != expected:
		print 'Not matched: %r -> %r, not %r' % (string, actual, expected)
		return False
	return True


def try_matches(target, tests):
	return _try_all(target, tests, try_match)


def try_non_matches(target, tests):
	tests_result = False
	for test in tests:
		test_result = _try_match_quietly(target, test)
		tests_result |= test_result
	return not tests_result


def try_errors(target, tests):
	return _try_all(target, tests, try_error)


def try_target(target, errors, matches):
	return try_errors(target, errors) and try_matches(target, matches)


def verify_target(target, errors, matches, non_matches):
	return try_errors(target, errors) and try_matches(target, matches) and try_non_matches(target, non_matches)
