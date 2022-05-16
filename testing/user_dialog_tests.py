import io
import unittest
from unittest import mock
from user_dialog.user_dialog import UserDialog
from parsing.postfix_expression import PostfixExpression


class PrintMock():
    def __init__(self):
        self.output = []

    def print(self, *args):
        self.output.extend(args)

class PostfixMock():
    def __init__(self, exp = "2"):
        self.expression_string = exp

    def solve(self):
        return "solving"

    def show_solving_history(self):
        return "history"

    def import_from_xml(self,xml_path):
        if xml_path == "xml":
            raise ValueError
        print("import mock")
        return None

class TestMainHelp(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")

    def test_prints_something(self):
        pass



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
        UserDialog.current_expression = PostfixExpression("3+3")


class TestChangeCurrentExpressionXML(unittest.TestCase):

    def test_manual_interaction(self):
        UserDialog.current_expression = PostfixMock()
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            original_input = mock.builtins.input
            mock.builtins.input = lambda _: "4"

            UserDialog.interactive_menu()

        target = "Enter a big number expression!\nBuilding expression . . .\nValidating expression . . .\n"

        self.assertEqual(fake_stdout.getvalue(), target, msg="test_manual_interaction failed")
        UserDialog.current_expression = None


class TestExportCurrentExpressionSML(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


class TestInteractiveMenu(unittest.TestCase):
    def test_current_expression(self):
        UserDialog.current_expression = PostfixMock()
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            UserDialog.show_current_expression()

        self.assertEqual(fake_stdout.getvalue(), '2\n', msg="test_current_expression failed")
        UserDialog.current_expression = None

class TestChangeNumberSize(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


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
        self.assertEqual(UserDialog.current_expression.show_solving_history(), target2, msg="test_solve_expression failed history")
        UserDialog.current_expression = None


TEST_CASES = [TestMainHelp, TestSolveCurrentExpression, TestModifyVerbosity, TestChangeCurrentExpressionXML,
              TestExportCurrentExpressionSML, TestInteractiveMenu, TestChangeNumberSize, TestShowCurrentExpression,
              TestAutomaticMenu]


def main():
    unittest.main()


if __name__ == '__main__':
    main()
