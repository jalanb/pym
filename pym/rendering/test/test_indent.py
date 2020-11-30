"""Test the indenter"""


from unittest import TestCase


from pym.rendering import indent


class IndentTest(TestCase):
    def setUp(self):
        pass

    def test_render(self):
        indenter = indent.Indenter()
        text = indenter.indent_string
        for i in range(0, 4):
            rendered = indenter.render("text")
            expected = text * i
            self.assertTrue(rendered.startswith(expected))
            indenter.indent()
        for i in range(4, 0, -1):
            rendered = indenter.render("text")
            expected = text * i
            self.assertTrue(rendered.startswith(expected))
            indenter.dedent()

    def test_cannot_dedent_past_empty(self):
        indenter = indent.Indenter()
        self.assertRaises(ValueError, indenter.dedent)
        indenter.indent()
        indenter.dedent()
        self.assertRaises(ValueError, indenter.dedent)

    def test_reset_to_0_on_indent(self):
        indenter = indent.Indenter()
        indenter.indentation = -5
        self.assertRaises(ValueError, indenter.indent)
        self.assertEqual(indenter.indentation, 0)

    def test_reset_to_0_on_dedent(self):
        indenter = indent.Indenter()
        indenter.indentation = -5
        self.assertRaises(ValueError, indenter.dedent)
        self.assertEqual(indenter.indentation, 0)

    def test_reset_limit_on_indent(self):
        """Before indenting the current level should be 0 or greater"""
        indenter = indent.Indenter()
        indenter.indentation = -2
        self.assertRaises(ValueError, indenter.indent)
        indenter.indentation = -1
        self.assertRaises(ValueError, indenter.indent)
        indenter.indentation = 0
        indenter.indent()
        indenter.indentation = +1
        indenter.indent()
        indenter.indentation = +2
        indenter.indent()

    def test_reset_limit_on_dedent(self):
        """Before dedenting the current level should be 1 or greater"""
        indenter = indent.Indenter()
        indenter.indentation = -2
        self.assertRaises(ValueError, indenter.dedent)
        indenter.indentation = -1
        self.assertRaises(ValueError, indenter.dedent)
        indenter.indentation = 0
        self.assertRaises(ValueError, indenter.dedent)
        indenter.indentation = +1
        indenter.dedent()
        indenter.indentation = +2
        indenter.dedent()

    def tearDown(self):
        pass
