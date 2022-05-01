from big_numbers.big_number import BigNumber
from pathlib import Path


class PostfixExpression:

    def __init__(self, expression_string: str):
        self.expression_stack = self.build_expression_stack(expression_string)
        self.current_result = None
        self.current_expression = None
        self.executed_expression = None

    def advance(self):
        pass

    def remaining_stack_to_expression_string(self):
        pass

    def export_to_xml(self, input_xml_path: Path):
        pass

    def import_from_xml(self, output_xml_path: Path):
        pass

    @staticmethod
    def build_expression_stack(expression_string: str) -> list:
        Operators = set(['+', '-', '*', '/', '(', ')', '^'])  # collection of Operators

        Priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # dictionary having priorities of Operators

        def infixToPostfix(expression):

            stack = []  # initialization of empty stack

            output = ''
            same_number_flag = 1
            expr_list = []

            for character in expression:

                if character not in Operators:  # if an operand append in postfix expression
                    if same_number_flag == 1:
                        output += character
                    else:
                        expr_list.append(BigNumber(output, 999999))
                        output = ''
                        same_number_flag = 1
                        output += character

                elif character == '(':  # else Operators push onto stack
                    same_number_flag = 0
                    stack.append('(')

                elif character == ')':
                    same_number_flag = 0
                    while stack and stack[-1] != '(':
                        expr_list.append(stack.pop())

                    stack.pop()

                else:
                    same_number_flag = 0
                    while stack and stack[-1] != '(' and Priority[character] <= Priority[stack[-1]]:
                        expr_list.append(stack.pop())
                    stack.append(character)

            while stack:
                #output += stack.pop()
                expr_list.append(stack.pop())

            return expr_list

        return infixToPostfix(expression_string)
