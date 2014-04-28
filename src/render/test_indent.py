"""Test the indenter"""


from unittest import TestCase


import indent


class IndentTest(TestCase):
    def setUp(self):
        pass

    def test_render(self):
        indenter = indent.Indenter()
        text = indenter.indent_string
        for i in range(0, 4):
            rendered = indenter.render('text')
            expected = text * i
            self.assertTrue(rendered.startswith(expected))
            indenter.indent()
        for i in range(4, 0, -1):
            rendered = indenter.render('text')
            expected = text * i
            self.assertTrue(rendered.startswith(expected))
            indenter.dedent()

    def test_cannot_dedent_past_empty(self):
        indenter = indent.Indenter()
        self.assertRaises(ValueError, indenter.dedent)
        indenter.indent()
        indenter.dedent()
        self.assertRaises(ValueError, indenter.dedent)

    def tearDown(self):
        pass
