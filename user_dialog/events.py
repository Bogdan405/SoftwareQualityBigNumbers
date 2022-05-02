from abc import ABC, abstractmethod
from big_numbers.big_number import BigNumber
from parsing.postfix_expression import PostfixExpression


def help():
    print("No help coming...")


def automatic():
    pass


def interactive():
    expression = input('Enter infix expression ')

    print('infix notation: ', expression)

    expr = PostfixExpression(expression)
    print(expr.expression_stack)
    # for x in expr.expression_stack:
    #     if type(x) is BigNumber:
    #         print("element is: ", x.big_number)
    #     else:
    #         print("element op", x)


def modify_number_size():
    pass
