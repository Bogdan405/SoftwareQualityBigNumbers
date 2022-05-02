import copy
import os
from pathlib import Path

from bs4 import BeautifulSoup

from big_numbers.big_number import BigNumber
from parsing import errors


class PostfixExpression:
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '#': 3, '(': 0, ')': 0}
    operator_mapping = {'+': BigNumber.__add__, '-': BigNumber.__sub__, '*': BigNumber.__mul__,
                        '/': BigNumber.__truediv__, '^': BigNumber.__pow__, '#': BigNumber.root}
    max_number_size = 5

    def __init__(self, expression_string: str):
        self.expression_string = expression_string
        self.result = None
        self.post_fixed_expression = []
        self.init_expression()

    def solve(self):
        print(f"Analyzing expression {self.expression_string}:")
        number_stack = []
        current_expression = self.restore_post_fixed_to_string(copy.deepcopy(number_stack), 0)
        print(f"Transformed expression to {current_expression}")

        print(f"Now solving: {current_expression}")
        for index, item in enumerate(self.post_fixed_expression):

            if item in self.operator_mapping.keys():
                number2 = number_stack.pop()
                number1 = number_stack.pop()
                operator = self.operator_mapping[item]
                result = operator(number1, number2)
                number_stack.append(result)
                current_expression = self.restore_post_fixed_to_string(copy.deepcopy(number_stack), index + 1)
                print(f"Solving atomic operation: {number1} {item} {number2}: {result}\n")
                print(f"Now solving: {current_expression}")
            else:
                number_stack.append(item)
        self.result = number_stack[0]

    def init_expression(self):
        print("Building expression . . .")
        self.build_post_fixed_expression(self.expression_string)
        print("Validating expression . . .")
        self.restore_post_fixed_to_string([], 0)

    def restore_post_fixed_to_string(self, expression_stack, current_index):
        for index in range(current_index, len(self.post_fixed_expression)):
            if self.post_fixed_expression[index] in self.operator_mapping.keys():
                if len(expression_stack) < 2:
                    raise errors.MisplacedSymbol(self.post_fixed_expression[index], expression_stack[-1])

                number2 = expression_stack.pop()
                number1 = expression_stack.pop()
                expression_stack.append(f"({number1}{self.post_fixed_expression[index]}{number2})")

            elif self.post_fixed_expression[index] in self.precedence.keys():
                raise errors.MisplacedSymbol(self.post_fixed_expression[index], expression_stack[-1])

            else:
                expression_stack.append(self.post_fixed_expression[index])
        return expression_stack[0]

    def export_to_xml(self, input_xml_path: Path):
        pass

    @staticmethod
    def import_from_xml(output_xml_path: Path) -> "PostfixExpression":
        data = output_xml_path.read_text()
        bs_data = BeautifulSoup(data, "xml")
        expr_parts = bs_data.find('expr').findChildren()
        decoded = ''

        for part in expr_parts:
            decoded += part.string
        return PostfixExpression(decoded)

    def build_post_fixed_expression(self, expression_string: str):
        output = []
        index = 0
        while index < len(expression_string):
            if expression_string[index] == '(':
                self.post_fixed_expression.append(expression_string[index])

            elif expression_string[index] == ')':
                while len(self.post_fixed_expression) != 0 and self.post_fixed_expression[-1] != '(':
                    output.append(self.post_fixed_expression.pop())
                if not len(self.post_fixed_expression):
                    raise errors.AdditionalClosingBracket()
                self.post_fixed_expression.pop()

            elif expression_string[index] not in self.precedence.keys():
                number = ""
                while index < len(expression_string) \
                        and expression_string[index] not in self.precedence.keys():
                    number += expression_string[index]
                    index += 1
                index -= 1
                output.append(BigNumber(number, self.max_number_size))

            else:
                while len(self.post_fixed_expression) != 0 and \
                        self.precedence[expression_string[index]] <= self.precedence[self.post_fixed_expression[-1]]:
                    output.append(self.post_fixed_expression.pop())
                self.post_fixed_expression.append(expression_string[index])
            index += 1
        while len(self.post_fixed_expression):
            output.append(self.post_fixed_expression.pop())
        self.post_fixed_expression = output


def main():
    # complex expression
    exp = "(33+0#2^2^2)*4#2+(555/2)+1"
    postfix_exp = PostfixExpression(exp)
    postfix_exp.solve()

    # expression from xml
    my_path = Path(os.path.join(os.getcwd(), 'testing.xml'))
    a = PostfixExpression.import_from_xml(my_path)
    a.solve()


if __name__ == '__main__':
    main()
