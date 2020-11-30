"""Test the AST nodes"""


from unittest import TestCase


from pym.ast import nodes


class MockAttributes(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class DocStringTest(TestCase):
    def setUp(self):
        pass

    def test_initialization(self):
        node = MockAttributes(lineno=22)
        string = "Hello World"
        docstring = nodes.DocString(node, string)
        self.assertEqual(docstring.s, string)
        self.assertEqual(docstring.lineno, node.lineno)
        self.assertEqual(docstring.col_offset, 0)

    def test_initialization_without_line(self):
        string = "Hello World"
        docstring = nodes.DocString(None, string)
        self.assertEqual(docstring.s, string)
        self.assertEqual(docstring.lineno, 0)
        self.assertEqual(docstring.col_offset, 0)

    def tearDown(self):
        pass


class CommentTest(TestCase):
    def setUp(self):
        self.data = (
            11,
            22,
            "That is the end of the interval. "
            "Will you kindly return to your seats? "
            "We will now proceed with the film as advertised",
        )

    def test_is_line_before_without_lineno(self):
        comment = nodes.Comment(self.data)
        self.assertFalse(comment.is_line_before(None))

    def test_same_line_without_lineno(self):
        comment = nodes.Comment(self.data)
        self.assertFalse(comment.same_line(None))

    def test_is_line_before(self):
        comment = nodes.Comment(self.data)
        node = MockAttributes(lineno=comment.lineno - 1)
        self.assertFalse(comment.is_line_before(node))
        node = MockAttributes(lineno=comment.lineno)
        self.assertFalse(comment.is_line_before(node))
        node = MockAttributes(lineno=comment.lineno + 1)
        self.assertTrue(comment.is_line_before(node))

    def test_is_before(self):
        c = nodes.Comment(self.data)
        node = MockAttributes(lineno=c.lineno - 1)
        self.assertFalse(c.is_before(node))
        node = MockAttributes(lineno=c.lineno, col_offset=c.col_offset - 1)
        self.assertFalse(c.is_before(node))
        node = MockAttributes(lineno=c.lineno, col_offset=c.col_offset)
        self.assertFalse(c.is_before(node))
        node = MockAttributes(lineno=c.lineno, col_offset=c.col_offset + 1)
        self.assertTrue(c.is_before(node))
        node = MockAttributes(lineno=c.lineno + 1)
        self.assertTrue(c.is_before(node))

    def test_set_prefix(self):
        comment = nodes.Comment(self.data)
        self.assertIsNone(comment.prefix)
        expected = "Oh, my nipples explode with delight!"
        comment.set_prefix(expected)
        self.assertEqual(expected, comment.prefix)
