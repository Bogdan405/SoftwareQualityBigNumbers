import unittest
from user_dialog.user_dialog import UserDialog
from parsing.postfix_expression import PostfixExpression
from parsing import errors
from big_numbers import errors


class TestMainHelp(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")

    def test_prints_something(self):
        pass


class TestShowCurrentExpression(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


class TestAutomaticMenu(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


class TestChangeCurrentExpressionXML(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


class TestExportCurrentExpressionSML(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


class TestInteractiveMenu(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


class TestChangeNumberSize(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


class TestModifyVerbosity(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


class TestSolveCurrentExpression(unittest.TestCase):
    def setUp(self) -> None:
        UserDialog.current_expression = PostfixExpression("3+3")


TEST_CASES = [TestMainHelp, TestSolveCurrentExpression, TestModifyVerbosity, TestChangeCurrentExpressionXML,
              TestExportCurrentExpressionSML, TestInteractiveMenu, TestChangeNumberSize, TestShowCurrentExpression,
              TestAutomaticMenu]


def main():
    unittest.main()


if __name__ == '__main__':
    main()
