import unittest

from parsing.postfix_expression import PostfixExpression
from parsing import errors as perrors
from big_numbers import errors as berrors


class TestBuildPostFixedExpression(unittest.TestCase):

    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")

    def test_doesnt_accepts_null(self):
        self.failUnlessRaises(ValueError, self.expression.build_post_fixed_expression, "")

    def test_doesnt_accept_illegal_symbols(self):
        try:
            self.failUnlessRaises(ValueError, self.expression.build_post_fixed_expression("3+$4"))
        except Exception as e:
            self.fail(f"Generated error {e.__class__} {e}")

    def test_accepts_incorrect_operations_syntax(self):
        self.expression.build_post_fixed_expression("3+(4*5)*3-4")
        # self.failUnlessRaises()


class TestSolveExpression(unittest.TestCase):
    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")


class TestRestorePostfixedToString(unittest.TestCase):
    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")


class TestImportXML(unittest.TestCase):
    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")


class TestExportXML(unittest.TestCase):
    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")


class TestShowSolvingHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")


class TestMainExample(unittest.TestCase):
    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")


class TestInitExpression(unittest.TestCase):
    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")


TEST_CASES = [TestBuildPostFixedExpression, TestSolveExpression, TestImportXML, TestExportXML,
              TestShowSolvingHistory, TestMainExample, TestInitExpression, TestRestorePostfixedToString]


def main():
    unittest.main()


if __name__ == '__main__':
    main()
