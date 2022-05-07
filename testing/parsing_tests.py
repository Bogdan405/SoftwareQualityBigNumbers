import unittest

from parsing.postfix_expression import PostfixExpression


class TestBuildPostFixedExpression(unittest.TestCase):

    def setUp(self) -> None:
        self.expression = PostfixExpression("3+3")

    def test_accepts_null(self):
        self.expression.build_post_fixed_expression("")


TEST_CASES = [TestBuildPostFixedExpression]


def main():
    unittest.main()


if __name__ == '__main__':
    main()
