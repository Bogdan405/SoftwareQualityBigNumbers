from pathlib import Path

from big_numbers.big_number import BigNumber


class PostfixExpression:
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '#': 3, '(': 0, ')': 0}
    operator_mapping = {'+': BigNumber.__add__, '-': BigNumber.__sub__, '*': BigNumber.__mul__,
                        '/': BigNumber.__truediv__, '^': BigNumber.__pow__, '#': BigNumber.root}
    max_number_size = 5

    def __init__(self, expression_string: str):
        self.current_result = None
        self.current_expression = None
        self.executed_expression = None
        self.expression_stack = []
        self.build_expression_stack(expression_string)

    def advance(self):
        pass

    def remaining_stack_to_expression_string(self):
        pass

    def export_to_xml(self, input_xml_path: Path):
        pass

    def import_from_xml(self, output_xml_path: Path):
        pass

    def build_expression_stack(self, expression_string: str):
        output = []
        index = 0
        while index < len(expression_string):
            if expression_string[index] == '(':
                self.expression_stack.append(expression_string[index])

            elif expression_string[index] == ')':
                while len(self.expression_stack) != 0 and self.expression_stack[-1] != '(':
                    output.append(self.expression_stack.pop())
                if len(self.expression_stack) != 0 and self.expression_stack[-1] != '(':
                    raise ValueError
                else:
                    self.expression_stack.pop()
            elif expression_string[index] not in self.precedence.keys():
                number = ""
                while index < len(expression_string) \
                        and expression_string[index] not in self.precedence.keys():
                    number += expression_string[index]
                    index += 1
                index -= 1
                output.append(BigNumber(number, self.max_number_size))

            else:
                while len(self.expression_stack) != 0 and \
                        self.precedence[expression_string[index]] <= self.precedence[self.expression_stack[-1]]:
                    output.append(self.expression_stack.pop())
                self.expression_stack.append(expression_string[index])
            index += 1
        while len(self.expression_stack):
            output.append(self.expression_stack.pop())
        self.expression_stack = output


def main():
    exp = "(33+0#2^2^2)*4#2+(555/2)"
    postfix_exp = PostfixExpression(exp)
    print(postfix_exp.expression_stack)


if __name__ == '__main__':
    main()
