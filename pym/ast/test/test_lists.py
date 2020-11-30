"""Test AST list handling"""

import unittest

from pym import lists


class TestPymLists(unittest.TestCase):
    def test_lists(self):
        line_compare = lists.attribute_comparison("line", 44)
        lines = [
            lists.Line(i, l)
            for i, l in enumerate(open(__file__).read().splitlines(), 1)
        ]
        actual = lists._search(lines, line_compare)
        expected = None
        try:
            self.assertEqual(actual, expected)
        except:  # pylint: disable=bare-except
            breakpoint()


if __name__ == "__main__":
    unittest.main()
