import unittest
from parsing.postfix_expression import main as main_parsing_example, PostfixExpression
from parsing import errors as perrors
from big_numbers import errors as berrors
from big_numbers.big_number import BigNumber
from testing.utils import get_test_suite
from unittest.mock import MagicMock, Mock, patch
from pathlib import Path
import os
import builtins


class PrintMock():
    def __init__(self):
        self.output = []

    def print(self, *args):
        self.output.extend(args)


def special_init(self, exp_string: str):
    self.expression_string = exp_string


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

    def test_correct_operation(self):
        self.assertEqual("(3+3)", self.expression.restore_post_fixed_to_string([], 0))

    def test_misplaced_symbol_error(self):
        self.expression.post_fixed_expression = [3, 3, "+", "+"]
        try:
            self.assertRaises(perrors.MisplacedSymbol, self.expression.restore_post_fixed_to_string, [], 0)
        except Exception as e:
            self.fail(f"Generated another error")

    def test_misplaced_number_error(self):
        self.expression.post_fixed_expression = [3, 3, "+", "+"]
        try:
            self.assertRaises(perrors.MisplacedSymbol, self.expression.restore_post_fixed_to_string, [], 0)
        except Exception as e:
            self.fail(f"Generated another error")

    def test_null_expression_stack_error(self):
        self.expression.post_fixed_expression = []
        print(self.expression.post_fixed_expression)
        try:
            self.assertRaises(IndexError, self.expression.restore_post_fixed_to_string, [], 0)
        except Exception as e:
            self.fail(f"Generated another error")

    def test_already_processed_string(self):
        self.expression.post_fixed_expression = [3, 4, 5, "+", "+"]
        solved_stack = ["3", "4+5"]
        current_index = 4
        print(self.expression.post_fixed_expression)
        try:
            self.assertEqual("(3+(4+5))", self.expression.restore_post_fixed_to_string(solved_stack, current_index))
        except Exception as e:
            self.fail(f"Generated an error {e}")


class TestImportXML(unittest.TestCase):

    def test_correct_load(self):
        self.xml_path = MagicMock()
        self.xml_path.read_text.return_value = """
                <?xml version="1.0" encoding="UTF-8"?>
                <expr>
                    <number>3</number>
                    <op>+</op>
                    <number>3</number>
                </expr>
                """
        try:
            x = PostfixExpression.import_from_xml(self.xml_path)
            self.assertEqual(x.expression_string, "3+3")
        except Exception as e:
            self.fail(f"Generated an error")

    def test_error_on_invalid_syntax_in_input(self):
        self.xml_path = MagicMock()
        self.xml_path.read_text.return_value = """
                <?xml version="1.0" encoding="UTF-8"?>
                <expr>
                    <op>3</op>
                    <number>-</number>
                    <op>3</op>
                </expr>
                """
        with patch.object(PostfixExpression, "__init__", special_init):
            self.assertRaises(Exception, PostfixExpression.import_from_xml, self.xml_path)

    def test_error_on_empty_input(self):
        self.xml_path = MagicMock()
        self.xml_path.read_text.return_value = """
                <?xml version="1.0" encoding="UTF-8"?>
                <expr>
                </expr>
                """
        with patch.object(PostfixExpression, "__init__", special_init):
            self.assertRaises(Exception, PostfixExpression.import_from_xml, self.xml_path)


class TestExportXML(unittest.TestCase):
    def setUp(self):
        self._orig_pathexists = os.path.exists
        os.path.exists = Mock(True)
        self.export_path = '/my/path/not/exists'
        self.expression = PostfixExpression("3+3")

    def test_export_without_solve(self):
        with patch('builtins.open', unittest.mock.mock_open()) as m:
            try:
                self.expression.export_to_xml(
                    Path(self.export_path)
                )
            except Exception as e:
                self.fail(f"Generated an error {e}")

    def test_calls_system_write(self):
        self.expression.solve()
        with patch('builtins.open', unittest.mock.mock_open()) as m:
            self.expression.export_to_xml(
                Path(self.export_path)
            )
            m.assert_called_once_with(Path(self.export_path), 'w+')

    def test_correct_writing_output(self):
        self.expression.solve()
        expected_write_value = '<expr>\n<number>3</number>\n<op>+</op>\n<number>3</number>\n</expr>\n<equal-to>\n6\n</equal-to>'
        with patch('builtins.open', unittest.mock.mock_open()) as m:
            self.expression.export_to_xml(
                Path(self.export_path)
            )
            handle = m()
            handle.write.assert_called_once_with(expected_write_value)

    def test_error_when_null_expr(self):
        self.expression.expression_string = ""
        with patch('builtins.open', unittest.mock.mock_open()) as m:
            try:
                self.assertRaises(AttributeError, self.expression.export_to_xml,
                                  Path(self.export_path)
                                  )
            except Exception as e:
                self.fail(f"Generated another error {e}")


class TestShowSolvingHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")

    def test_shows_empty_history(self):
        self.assertEqual(self.expression.solve_output_history, [])

    def test_correct_history(self):
        correct_history = ['Analyzing expression 3+3:',
                           'Transformed expression to (3+3)',
                           'Now solving: (3+3)',
                           'Solving atomic operation: 3 + 3: 6\n',
                           'Result: 6']
        self.expression.solve()
        self.assertEqual(self.expression.solve_output_history, correct_history)

    def test_prints_correct_history(self):
        correct_history = ['Analyzing expression 3+3:',
                           'Transformed expression to (3+3)',
                           'Now solving: (3+3)',
                           'Solving atomic operation: 3 + 3: 6\n',
                           'Result: 6']
        print_mock = PrintMock()
        self.expression.solve()
        with patch("builtins.print", print_mock.print):
            self.expression.show_solving_history()
        self.assertEqual(print_mock.output, correct_history)

    def test_no_output_on_empty_history(self):
        print_mock = PrintMock()
        with patch("builtins.print", print_mock.print):
            self.expression.show_solving_history()
        self.assertEqual(print_mock.output, [])

    def test_output_with_no_verbosity(self):
        correct_history = ['Analyzing expression 3+3:',
                           'Transformed expression to (3+3)',
                           'Now solving: (3+3)',
                           'Result: 6']
        print_mock = PrintMock()
        self.expression.full_verbosity = False
        self.expression.solve()
        with patch("builtins.print", print_mock.print):
            self.expression.show_solving_history()
        self.assertEqual(print_mock.output, correct_history)

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
