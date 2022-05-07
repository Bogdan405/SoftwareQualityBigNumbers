import unittest
from big_numbers import errors
from big_numbers.big_number import BigNumber


class TestBigNumberInit(unittest.TestCase):

    def test_accepts_null(self):
        number_size = 5
        self.assertRaises(ValueError, BigNumber, "", number_size)

    def test_doesnt_accept_extra_chars(self):
        number_size = 14
        self.assertRaises(errors.InvalidCharInNumberString, BigNumber, "-14", number_size)


TEST_CASES = [TestBigNumberInit]


def main():
    unittest.main()


if __name__ == '__main__':
    main()
