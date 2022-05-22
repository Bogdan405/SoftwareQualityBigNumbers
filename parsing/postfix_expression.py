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
    full_verbosity = True

    def __init__(self, expression_string: str):
        self.expression_string = expression_string
        self.result = None
        self.post_fixed_expression = []
        self.solve_output_history = []
        self.init_expression()
        assert len(self.post_fixed_expression) != 0
        assert len([x for x in self.post_fixed_expression if type(x) == BigNumber]) != 0

    def solve(self):
        self.solve_output_history = []
        self.solve_output_history.append(f"Analyzing expression {self.expression_string}:")
        number_stack = []
        current_expression = self.restore_post_fixed_to_string(copy.deepcopy(number_stack), 0)
        self.solve_output_history.append(f"Transformed expression to {current_expression}")
        self.solve_output_history.append(f"Now solving: {current_expression}")
        assert len(self.post_fixed_expression) != 0
        for index, item in enumerate(self.post_fixed_expression):

            if item in self.operator_mapping.keys():
                number2 = number_stack.pop()
                number1 = number_stack.pop()

                assert type(number1) == BigNumber
                assert type(number2) == BigNumber
                operator = self.operator_mapping[item]
                result = operator(number1, number2)
                assert type(result) == BigNumber
                assert str(result) != ""
                number_stack.append(result)
                current_expression = self.restore_post_fixed_to_string(copy.deepcopy(number_stack), index + 1)
                assert current_expression is not None
                self.solve_output_history.append(f"Solving atomic operation: {number1} {item} {number2}: {result}\n")
                if index + 1 != len(self.post_fixed_expression):
                    self.solve_output_history.append(f"Now solving: {current_expression}")
            else:
                number_stack.append(item)
        assert len(number_stack) == 1
        self.result = number_stack[0]
        self.solve_output_history.append(f"Result: {self.result}")

    def show_solving_history(self):
        if not self.full_verbosity:
            print(self.solve_output_history[0])
            print(self.solve_output_history[1])
            print(self.solve_output_history[2])
            print(self.solve_output_history[-1])
            return

        for item in self.solve_output_history:
            print(item)

    def init_expression(self):
        print("Building expression . . .")
        self.build_post_fixed_expression(self.expression_string)
        assert len(self.post_fixed_expression) > 0
        print("Validating expression . . .")
        self.restore_post_fixed_to_string([], 0)
        assert len(self.post_fixed_expression) > 0

    def restore_post_fixed_to_string(self, expression_stack, current_index):
        for index in range(current_index, len(self.post_fixed_expression)):
            if self.post_fixed_expression[index] in self.operator_mapping.keys():
                if len(expression_stack) < 2:
                    raise errors.MisplacedSymbol(self.post_fixed_expression[index], expression_stack[-1])

                number2 = expression_stack.pop()
                number1 = expression_stack.pop()
                assert type(self.post_fixed_expression[index]) == str
                assert type(number1) == BigNumber
                assert type(number2) == BigNumber
                expression_stack.append(f"({number1}{self.post_fixed_expression[index]}{number2})")

            elif self.post_fixed_expression[index] in self.precedence.keys():
                raise errors.MisplacedSymbol(self.post_fixed_expression[index], expression_stack[-1])

            else:
                expression_stack.append(self.post_fixed_expression[index])
        assert len(expression_stack) == 1
        return expression_stack[0]

    @staticmethod
    def import_from_xml(input_xml_path: Path) -> "PostfixExpression":
        data = input_xml_path.read_text()
        assert data is not None
        bs_data = BeautifulSoup(data, "xml")
        expr_parts = bs_data.find('expr').findChildren()
        decoded = ''

        for part in expr_parts:
            decoded += part.string
        assert decoded is not None
        return PostfixExpression(decoded)

    def export_to_xml(self, output_xml_path: Path):
        translator = self.expression_string
        translator = translator.replace("/", "<op>/</op>\n")
        translator = translator.replace("-", "<op>-</op>\n")
        translator = translator.replace("+", "<op>+</op>\n")
        translator = translator.replace("*", "<op>*</op>\n")
        translator = translator.replace("#", "<op>#</op>\n")
        translator = translator.replace("^", "<op>^</op>\n")
        translator = translator.replace("(", "<symbol>(</symbol>\n")
        translator = translator.replace(")", "<symbol>)</symbol>\n")

        final = translator
        index = 0
        while index < len(translator):
            number = ""
            if index < len(translator) and translator[index] in "0123456789":
                number += translator[index]
                index += 1
                while index < len(translator) and translator[index] in "0123456789":
                    number += translator[index]
                    index += 1
                final = final.replace(">\n" + number, ">\n<number>" + number + "</number>\n")
                final = final.replace(number + "<op", "<number>" + number + "</number>\n<op")
                assert translator[index] not in "0123456789"
            else:
                assert translator[index] in self.operator_mapping.keys()
                index += 1
        print("<expr>\n" + final + "</expr>\n<equal-to>\n" + self.result.value + "\n</equal-to>")

        assert len(final) != 0
        assert "<number>" in final
        assert "<op>" in final
        assert f"<op>{number}</op>" not in final
        assert "<op>(</op>" not in final
        assert "<op>)</op>" not in final
        assert "<number>(</number>" not in final
        assert "<number>(</number>" not in final
        for operator in self.operator_mapping.keys():
            assert f"<number>{operator}</number>" not in final

        with open(output_xml_path, "w+") as out_file:
            if self.result:
                out_file.write("<expr>\n" + final + "</expr>\n<equal-to>\n" + self.result.value + "\n</equal-to>")
            else:
                out_file.write("<expr>\n" + final + "</expr>")

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
                assert len(output) > 0
                assert len(self.post_fixed_expression) > 0
                self.post_fixed_expression.pop()

            elif expression_string[index] not in self.precedence.keys():
                number = ""
                while index < len(expression_string) \
                        and expression_string[index] not in self.precedence.keys():
                    number += expression_string[index]
                    index += 1
                index -= 1
                for key in self.precedence.keys():
                    assert key not in number
                for digit in number:
                    assert digit in "0123456789"
                assert len(number) != 0
                output.append(BigNumber(number, self.max_number_size))

            else:
                while len(self.post_fixed_expression) != 0 and \
                        self.precedence[expression_string[index]] <= self.precedence[self.post_fixed_expression[-1]]:
                    output.append(self.post_fixed_expression.pop())
                self.post_fixed_expression.append(expression_string[index])
            index += 1
        while len(self.post_fixed_expression):
            output.append(self.post_fixed_expression.pop())
        assert len(self.post_fixed_expression) == 0
        self.post_fixed_expression = output


def main():
    # complex expression
    exp = "(33+0#2^2^2)*4#2+(555/2)+1"
    postfix_exp = PostfixExpression(exp)

    # expression from xml
    PostfixExpression.max_number_size = 30
    my_path = Path(os.path.join(os.getcwd(), 'in.xml'))
    a = PostfixExpression.import_from_xml(my_path)
    a.solve()
    a.show_solving_history()

    print("We have:  ", a.expression_string)
    print("Equal to: ", a.result)

    my_path_out = Path(os.path.join(os.getcwd(), 'out.xml'))
    print("OUT:", a.export_to_xml(my_path_out))


if __name__ == '__main__':
    main()
