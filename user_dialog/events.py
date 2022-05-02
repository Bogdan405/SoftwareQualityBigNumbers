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

    for x in expr.post_fixed_expression:
        if type(x) is BigNumber:
            print("element is: ", x.big_number)
        else:
            print("element op", x)


def modify_number_size():
    pass


def modify_verbosity()
