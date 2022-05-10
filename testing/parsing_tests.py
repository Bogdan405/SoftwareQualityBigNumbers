import unittest
from parsing.postfix_expression import main as main_parsing_example, PostfixExpression
from parsing import errors as perrors
from big_numbers import errors as berrors
from testing.utils import get_test_suite


class TestBuildPostFixedExpression(unittest.TestCase):

    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")

    def test_correct_operation(self):
        try:
            self.expression.post_fixed_expression = []
            self.expression.build_post_fixed_expression(self.expression.expression_string)
        except Exception as e:
            self.fail(f"Generated another error")

    def test_doesnt_accepts_null(self):
        self.expression.post_fixed_expression = []
        self.assertRaises(ValueError, self.expression.build_post_fixed_expression, "")

    def test_doesnt_accept_illegal_symbols(self):
        try:
            self.expression.post_fixed_expression = []
            self.assertRaises(berrors.InvalidCharInNumberString, self.expression.build_post_fixed_expression, "3+4*(&)")
        except Exception as e:
            self.fail(f"Generated another error")

    def test_accepts_incorrect_operations_syntax(self):
        try:
            self.expression.post_fixed_expression = []
            self.expression.build_post_fixed_expression("3+(4*5)*3--4")
            self.expression.post_fixed_expression = []
            self.expression.build_post_fixed_expression("3+((4*5)*3--4++")
        except Exception as e:
            self.fail(f"Generated another error")


class TestSolveExpression(unittest.TestCase):
    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")

    def test_correct_operation(self):
        self.expression.solve()
        self.assertEqual(self.expression.result.value, "6")
        self.assertIsNotNone(self.expression.solve_output_history)

    def test_fails_on_incorrect_operations_syntax(self):
        try:
            self.expression.post_fixed_expression = []
            self.expression.build_post_fixed_expression("3+((4*5)*3--4++")
            self.assertRaises(ValueError, self.expression.solve)
        except Exception as e:
            self.fail(f"Generated another error")

    def test_doesnt_solve_expressions_past_limit_size(self):
        try:
            PostfixExpression.max_number_size = 1
            self.expression = PostfixExpression("5*5")
            self.assertRaises(berrors.NumberSizeGreaterThanLimit, self.expression.solve)
        except Exception as e:
            self.fail(f"Generated another error")


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

    def test_main_example_import_case(self):
        try:
            PostfixExpression.max_number_size = 30
            main_parsing_example()
        except Exception as e:
            self.fail(f"Generated another error")


class TestInitExpression(unittest.TestCase):

    def test_doesnt_accept_illegal_symbols(self):
        try:
            self.assertRaises(berrors.InvalidCharInNumberString, PostfixExpression, "3+4*(&)")
        except Exception as e:
            self.fail(f"Generated another error")

    def test_doesnt_accept_misplaced_symbols(self):
        try:
            self.assertRaises(perrors.MisplacedSymbol, PostfixExpression, "3+(4*5)*3--4")
        except Exception as e:
            self.fail(f"Generated another error")

    def test_doesnt_accept_numbers_past_limit_size(self):
        try:
            PostfixExpression.max_number_size = 2
            self.assertRaises(berrors.NumberSizeGreaterThanLimit, PostfixExpression, "103+33")
        except Exception as e:
            self.fail(f"Generated another error")

    def test_accepts_expressions_past_limit_size(self):
        try:
            PostfixExpression.max_number_size = 2
            PostfixExpression("99+33")
        except Exception as e:
            self.fail(f"Generated another error")


TEST_CASES = [TestBuildPostFixedExpression, TestSolveExpression, TestImportXML, TestExportXML,
              TestShowSolvingHistory, TestMainExample, TestInitExpression, TestRestorePostfixedToString]


def main():
    local_test_suite = unittest.TestSuite()
    for case in TEST_CASES:
        for test_method in get_test_suite(case):
            local_test_suite.addTest(test_method)

    runner = unittest.TextTestRunner()
    runner.run(local_test_suite)


if __name__ == '__main__':
    main()
