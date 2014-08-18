"""Test the Pym Transformers"""


from unittest import TestCase


from pym.ast.transform.transformers import PymTransformerBase, TreeChanger
from pym.render import render


class PymTransformerBaseTest(TestCase):

    def test_transformer_base(self):
        """Test that the base transformer doesn't actually change anything"""
        expected = render.parse('i = 0\nj = i = 1')
        transformer = PymTransformerBase()
        actual = transformer.visit(expected)
        self.assertEqual(expected, actual)

    def test_handle_items(self):
        transformer = PymTransformerBase()
        actual = transformer.handle_values(1, [1,2,3])
        self.assertIsNone(actual)

    def test_handle_item(self):
        transformer = PymTransformerBase()
        actual = transformer.handle_value(1, 2, 3)
        self.assertIsNone(actual)

    def test_handle_old_values(self):
        transformer = PymTransformerBase()
        actual = transformer.handle_old_values(1, [1,2,3])
        self.assertIsNone(actual)


class TestTreeChanger(TestCase):
    def test_pass_removal(self):
        class PassRemover(TreeChanger):
            def visit_Pass(self, _node):
                # pylint: disable-msg=no-self-use
                return None

        transformer = PassRemover()
        ast = render.parse('pass')
        ast = transformer.visit(ast)
        actual = render.render(ast)
        self.assertEqual('', actual)

    def test_string_emptying(self):
        class StringBlanker(TreeChanger):
            def visit_Str(self, _node):
                # pylint: disable-msg=no-self-use
                return 'pass'

        transformer = StringBlanker()
        ast = render.parse('"contents"')
        ast = transformer.visit(ast)
        actual = render.render(ast)
        self.assertEqual('pass', actual)

    def test_string_removal_from_module(self):
        class StringBlanker(TreeChanger):
            def visit_Expr(self, _node):
                # pylint: disable-msg=no-self-use
                return None

        transformer = StringBlanker()
        ast = render.parse('"contents"')
        ast = transformer.visit(ast)
        actual = render.render(ast)
        self.assertEqual('', actual)

    def test_string_removal_from_expression(self):
        class StringBlanker(TreeChanger):
            def visit_Expr(self, _node):
                # pylint: disable-msg=no-self-use
                return None

        transformer = StringBlanker()
        ast = render.parse('i=0\n"contents"')
        ast = transformer.visit(ast)
        actual = render.render(ast)
        self.assertEqual('i = 0', actual)
