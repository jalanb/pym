"""Methods to aid testing parsely grammars"""


def _try_all(target, tests, try_method):
    """Accumulate results for that target against all those tests"""
    return all([try_method(target, test) for test in tests])


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
    target_method = getattr(instance, target)
    try:
        return target_method(), None
    except Exception as e:
        return None, str(e).splitlines()[-1]


def use_grammar(grammar):
    """Use that grammar in subsequent tests"""

    def invalidate():
        delattr(use_grammar, "grammar")

    use_grammar.grammar = grammar
    use_grammar.invalidate = invalidate


def instantiate(string):
    """Instantiate the current grammar with that string"""
    try:
        return use_grammar.grammar(string)
    except AttributeError:
        raise KeyboardInterrupt("Call use_grammar() before try_parse()")


def try_parse(target, string):
    """Try to parse for that target in that string

    Show any errors on stdout
    """
    result, error = _parse(target, string)
    if error:
        print(error)
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
        print("Not matched: %r -> %r, not %r" % (string, actual, expected))
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
    return not any([_try_match_quietly(target, test) for test in tests])


def try_errors(target, tests):
    """Try to generate an error from parsing that target with those tests"""
    return _try_all(target, tests, try_error)


def try_target(target, errors, matches):
    """Try to match that target, giving thos errors and those matches"""
    return try_errors(target, errors) and try_matches(target, matches)


def verify_target(target, errors, matches, non_matches):
    """Verify that target with the other arguments"""
    if not try_errors(target, errors):
        return False
    if not try_matches(target, matches):
        return False
    if not try_non_matches(target, non_matches):
        return False
    return True
