import io
import unittest
from tkinter import Tk, filedialog
from unittest import mock
from unittest.mock import MagicMock, Mock, patch
from user_dialog.user_dialog import UserDialog
from parsing.postfix_expression import PostfixExpression
import builtins
import os
from pathlib import Path


class PrintMock():
    def __init__(self):
        self.output = []

    def print(self, *args):
        self.output.extend(args)


class PostfixMock():
    def __init__(self, exp="2"):
        self.expression_string = exp

    def solve(self):
        return "solving"

    def show_solving_history(self):
        return "history"

    def import_from_xml(self, xml_path):
        if xml_path == "xml":
            raise ValueError
        print("import mock")
        return None


class TestMainHelp(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = MagicMock()

    def test_prints_correct_values(self):
        test_number_size = 19
        test_full_verbosity = False
        UserDialog.current_expression.max_number_size = test_number_size
        UserDialog.current_expression.full_verbosity = test_full_verbosity
        printer = PrintMock()
        with patch("builtins.print", printer.print):
            UserDialog.main_help()
        self.assertIn(str(test_number_size), printer.output[3])
        self.assertIn(str(test_full_verbosity), printer.output[4])

    def test_null_values(self):
        test_number_size = None
        test_full_verbosity = None
        PostfixExpression.max_number_size = test_number_size
        PostfixExpression.full_verbosity = test_full_verbosity
        printer = PrintMock()
        with patch("builtins.print", printer.print):
            UserDialog.main_help()
        self.assertIn(str(test_number_size), printer.output[3])
        self.assertIn(str(test_full_verbosity), printer.output[4])


class TestShowCurrentExpression(unittest.TestCase):

    def test_current_expression(self):
        UserDialog.current_expression = PostfixMock()
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            UserDialog.show_current_expression()

        self.assertEqual(fake_stdout.getvalue(), '2\n', msg="test_current_expression failed")
        UserDialog.current_expression = None

    def test_current_expression_none(self):
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            UserDialog.show_current_expression()

        self.assertEqual(fake_stdout.getvalue(), 'No current expression!\n', msg="test_current_expression_none failed")


class TestAutomaticMenu(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = MagicMock()
        self._orig_pathexists = os.path.exists
        os.path.exists = Mock(True)
        self.export_path = Path('/my/path/not/exists')

    @patch("builtins.input", return_value="import")
    @patch("tkinter.filedialog.askopenfilename", return_value='/my/path/not/exists')
    def test_correct_import_input(self, input, tkinter_filedialog):
        printer = PrintMock()
        with patch("builtins.print", printer.print):
            with patch('user_dialog.user_dialog.UserDialog.change_current_expression_through_xml',
                       unittest.mock.Mock()) as m:
                UserDialog.automatic_menu()
                m.assert_called_once_with(self.export_path)
        self.assertEqual(len(printer.output), 4)

    @patch("builtins.input", return_value="export")
    @patch("tkinter.filedialog.askopenfilename", return_value='/my/path/not/exists')
    def test_correct_export_input(self, input, tkinter_filedialog):
        printer = PrintMock()
        with patch("builtins.print", printer.print):
            with patch('user_dialog.user_dialog.UserDialog.export_current_expression_to_xml',
                       unittest.mock.Mock()) as m:
                UserDialog.automatic_menu()
                m.assert_called_once_with(self.export_path)
        self.assertEqual(len(printer.output), 4)

    @patch("builtins.input", return_value="back")
    @patch("tkinter.filedialog.askopenfilename", return_value='/my/path/not/exists')
    def test_correct_back_input(self, input, tkinter_filedialog):
        printer = PrintMock()
        with patch("builtins.print", printer.print):
            UserDialog.automatic_menu()
        self.assertEqual(len(printer.output), 4)

    @patch("builtins.input", side_effect=["blabla", "back"])
    @patch("tkinter.filedialog.askopenfilename", return_value='/my/path/not/exists')
    def test_incorrect_user_input(self, input, tkinter_filedialog):
        printer = PrintMock()
        with patch("builtins.print", printer.print):
            UserDialog.automatic_menu()
        self.assertEqual(len(printer.output), 8)


class TestChangeCurrentExpressionXML(unittest.TestCase):

    def test_manual_interaction(self):
        # SE CICLEAZA
        pass
        # UserDialog.current_expression = PostfixMock()
        # with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
        #     original_input = mock.builtins.input
        #     mock.builtins.input = lambda _: "4"
        #
        #     UserDialog.interactive_menu()
        #
        # target = "Enter a big number expression!\nBuilding expression . . .\nValidating expression . . .\n"
        #
        # self.assertEqual(fake_stdout.getvalue(), target, msg="test_manual_interaction failed")
        # UserDialog.current_expression = None


class TestExportCurrentExpressionSML(unittest.TestCase):
    def setUp(self) -> None:
        self._orig_pathexists = os.path.exists

        UserDialog.current_expression = MagicMock()
        UserDialog.current_expression.import_from_xml.return_value = None
        UserDialog.current_expression.export_to_xml.return_value = None
        os.path.exists = Mock(True)
        self.export_path = Path('/my/path/not/exists')

    def test_calls_correct_method(self):
        with patch("user_dialog.user_dialog.UserDialog.current_expression.export_to_xml", mock.Mock()) as m:
            UserDialog.export_current_expression_to_xml(self.export_path)
            m.assert_called_once_with(self.export_path)


class TestInteractiveMenu(unittest.TestCase):
    def test_current_expression(self):
        UserDialog.current_expression = PostfixMock()
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            UserDialog.show_current_expression()

        self.assertEqual(fake_stdout.getvalue(), '2\n', msg="test_current_expression failed")
        UserDialog.current_expression = None


class TestChangeNumberSize(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = MagicMock()

    @patch("builtins.input", side_effect=["15"])
    def test_correct_change(self, input):
        printer = PrintMock()
        with patch("builtins.print", printer.print):
            UserDialog.modify_number_size()
        self.assertEqual(1, len(printer.output))
        self.assertEqual(UserDialog.current_expression.max_number_size, 15)

    @patch("builtins.input", side_effect=["-15", "15"])
    def test_invalid_number_size(self, input):
        printer = PrintMock()
        with patch("builtins.print", printer.print):
            UserDialog.modify_number_size()
        self.assertEqual(2, len(printer.output))
        self.assertEqual(UserDialog.current_expression.max_number_size, 15)

    @patch("builtins.input", side_effect=[":!", "20"])
    def test_illegal_symbols(self, input):
        printer = PrintMock()
        with patch("builtins.print", printer.print):
            UserDialog.modify_number_size()
        self.assertEqual(2, len(printer.output))
        self.assertEqual(UserDialog.current_expression.max_number_size, 20)


class TestModifyVerbosity(unittest.TestCase):
    def test_verbosity_correct_interaction(self):
        UserDialog.current_expression = PostfixMock("2+2")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            original_input = mock.builtins.input
            mock.builtins.input = lambda _: "partial"

            UserDialog.modify_verbosity()

        target = "Change verbosity to full/partial!\n"

        self.assertEqual(fake_stdout.getvalue(), target, msg="test_verbosity_correct_interaction failed")
        UserDialog.current_expression = None


class TestSolveCurrentExpression(unittest.TestCase):
    def test_solve_expression(self):
        UserDialog.current_expression = PostfixMock("2+2")
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            original_input = mock.builtins.input
            mock.builtins.input = lambda _: "partial"

            UserDialog.solve_current_expression()

        target1 = "solving"
        target2 = "history"

        self.assertEqual(UserDialog.current_expression.solve(), target1, msg="test_solve_expression failed solving")
        self.assertEqual(UserDialog.current_expression.show_solving_history(), target2,
                         msg="test_solve_expression failed history")
        UserDialog.current_expression = None


TEST_CASES = [TestMainHelp, TestSolveCurrentExpression, TestModifyVerbosity, TestChangeCurrentExpressionXML,
              TestExportCurrentExpressionSML, TestInteractiveMenu, TestChangeNumberSize, TestShowCurrentExpression,
              TestAutomaticMenu]


def main():
    unittest.main()


if __name__ == '__main__':
    main()
