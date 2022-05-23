from pathlib import Path
from tkinter import filedialog, Tk

from parsing.postfix_expression import PostfixExpression

root = Tk()
root.withdraw()
root.attributes('-topmost', True)


class PrintMock():
    def __init__(self):
        self.output = []

    def print(self, *args):
        self.output.extend(args)

class UserDialog:
    current_expression: PostfixExpression = None

    @classmethod
    def welcome(cls):
        print("Welcome to the Big Number Calculator!\n")

    @classmethod
    def main_help(cls):
        print("The main menu features the following commands:\n")
        print("automatic: gives the user the possibility to import the current expression"
              " or to export the current_expression and its results")
        print("interactive: gives the user the possibility to write by hand the big number expression"
              " that needs to be evaluated")
        print(
            f"number_size: change the maximum allowed big number size (currently: {PostfixExpression.max_number_size})")
        print(
            f"verbosity: change the current verbosity for the 'solve' commands (full: {PostfixExpression.full_verbosity})")
        print("current_expression: shows the current expression")
        print("solve: solves the current expression")
        print("quit: exist the program")

    @classmethod
    def show_current_expression(cls):
        if cls.current_expression:
            print(cls.current_expression.expression_string)
            return
        print("No current expression!")

    @classmethod
    def automatic_menu(cls):
        while True:
            try:
                file_path = filedialog.askopenfilename(title="Select an xml file for input/output")
                file_path = Path(file_path)
                break
            except:
                print("Invalid file path")

        valid_user_inputs = ("import", "export", "back")
        user_input = None

        while user_input not in valid_user_inputs:
            print("Possible commands:")
            for item in valid_user_inputs:
                print(item)
            user_input = input("input: ")

        match user_input:
            case "import":
                cls.change_current_expression_through_xml(file_path)
            case "export":
                cls.export_current_expression_to_xml(file_path)

    @classmethod
    def change_current_expression_through_xml(cls, xml_path: Path):
        try:
            assert len(xml_path)>1, "xml path too short"
            cls.current_expression = PostfixExpression.import_from_xml(xml_path)
        except Exception as e:
            print(e)

    @classmethod
    def export_current_expression_to_xml(cls, xml_path: Path):
        try:
            cls.current_expression.export_to_xml(xml_path)
        except Exception as e:
            print(e)

    @classmethod
    def interactive_menu(cls):
        print('Enter a big number expression!')
        while True:
            try:
                expression = input("input: ")
                expression = PostfixExpression(expression)
                break
            except Exception as e:
                print(e)
        cls.current_expression = expression

    @classmethod
    def modify_number_size(cls):
        print("Change number size to positive integer (>=1) input!")
        while True:
            try:
                user_input = int(input("input: "))
                if user_input < 1:
                    raise ValueError
                break
            except:
                print("Invalid integer value")
        PostfixExpression.max_number_size = user_input
        if cls.current_expression:
            cls.current_expression.max_number_size = user_input

    @classmethod
    def modify_verbosity(cls):
        print("Change verbosity to full/partial!")
        valid_inputs = ["full", "partial"]
        while True:
            user_input = input("input: ")
            if user_input in valid_inputs:
                break
            print("Invalid option!")

        match user_input:
            case "full":
                PostfixExpression.full_verbosity = True
                if cls.current_expression:
                    cls.current_expression.full_verbosity = True
            case "partial":
                PostfixExpression.full_verbosity = False
                if cls.current_expression:
                    cls.current_expression.full_verbosity = False

    @classmethod
    def solve_current_expression(cls):
        if not cls.current_expression:
            print("No expression has been found!")
            return
        try:
            cls.current_expression.solve()
            cls.current_expression.show_solving_history()
        except Exception as e:
            print(e)
