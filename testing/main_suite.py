import unittest

from testing.big_numbers_tests import TEST_CASES as BIG_NUMBER_TEST_CASES
from testing.parsing_tests import TEST_CASES as PARSING_TEST_CASES
from testing.user_dialog_tests import TEST_CASES as DIALOG_TEST_CASES
from testing.utils import get_test_suite


def main():
    cases = [BIG_NUMBER_TEST_CASES, PARSING_TEST_CASES, DIALOG_TEST_CASES]

    global_test_suite = unittest.TestSuite()
    for case in cases:
        for test_method in get_test_suite(case):
            global_test_suite.addTest(test_method)

    runner = unittest.TextTestRunner()
    runner.run(global_test_suite)


if __name__ == '__main__':
    main()
