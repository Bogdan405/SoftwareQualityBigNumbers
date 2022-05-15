import unittest
from big_numbers import errors
from big_numbers.big_number import BigNumber
from testing.utils import get_test_suite


class TestBigNumberInit(unittest.TestCase):

    def test_accepts_null(self):
        number_size = 5
        self.assertRaises(IndexError, BigNumber, "", number_size)

    def test_doesnt_accept_extra_chars(self):
        number_size = 14
        self.assertRaises(errors.InvalidCharInNumberString, BigNumber, "-14", number_size)

    def test_proper_init_chars(self):
        number_size = 22
        number = BigNumber("11112222", number_size)
        self.assertEqual(number.value, "11112222", "Value not saved")


class TestBigNumberOperations(unittest.TestCase):
    number1 = BigNumber("1000000000", 10)
    number2 = BigNumber("1000000000", 10)
    number3 = BigNumber("9000000000", 10)

    def test_equal(self):
        number1 = BigNumber("1000000000", 10)
        number2 = BigNumber("1000000000", 10)
        number3 = BigNumber("9000000000", 10)
        self.assertTrue(number1 == number2, "Equal failed for equals")
        self.assertFalse(number1 == number3, "Equal failed for non-equals")

    def test_comparison(self):
        number1 = BigNumber("1000000000", 10)
        number2 = BigNumber("9000000000", 10)
        self.assertTrue(number2 > number1, "Comparison > failed")
        self.assertTrue(number1 < number2, "Comparison < failed")

    def test_item_getter(self):
        number = BigNumber("951", 10)
        self.assertEqual(number[1], 5, "Item Getter failed")

    def test_item_setter(self):
        number = BigNumber("951", 10)
        number[1] = 0
        self.assertEqual(number[1], 0, "Item Setter failed")

    def test_copy(self):
        number = BigNumber("11112222", 10)
        copyOfNumber = number
        self.assertEqual(copyOfNumber.value, number.value, "Number copy of value failed")
        self.assertEqual(copyOfNumber.max_size, number.max_size, "Number size of value failed")

    def test_str(self):
        number = BigNumber("11112222", 10)
        self.assertEqual(type(str(number)), type("string"), "Number to str failed")

    def test_add_simple(self):
        number1 = BigNumber("1000000000", 10)
        number2 = BigNumber("1000000000", 10)
        number3 = BigNumber("2000000000", 10)
        self.assertEqual(number1 + number2, number3, "Number add simple failed")

    def test_add_overflow(self):
        number1 = BigNumber("9000000000", 10)
        number2 = BigNumber("9000000000", 10)

        with self.assertRaises(errors.NumberSizeGreaterThanLimit,msg="Add overflow result failed"):
            number1+number2

    def test_sub_simple(self):
        number1 = BigNumber("9000000300", 10)
        number2 = BigNumber("3000000100", 10)
        number3 = BigNumber("6000000200", 10)

        self.assertEqual(number1 - number2, number3, "Number sub simple failed")

    def test_sub_negative(self):
        number1 = BigNumber("3000000000", 10)
        number2 = BigNumber("3000000100", 10)

        with self.assertRaises(errors.NegativeResult,msg="Sub negative result failed"):
            number1 - number2

    def test_mul_simple(self):
        number1 = BigNumber("1111", 10)
        number2 = BigNumber("1111", 10)
        number3 = BigNumber("1234321", 10)

        self.assertEqual(number1 * number2, number3, "Number mul simple failed")

    def test_mul_overflow(self):
        number1 = BigNumber("3000000000", 10)
        number2 = BigNumber("3000000100", 10)

        with self.assertRaises(errors.NumberSizeGreaterThanLimit,msg="Mul overflow result failed"):
            number1 * number2

    def test_div_simple(self):
        number1 = BigNumber("10000000", 10)
        number2 = BigNumber("100", 10)
        number3 = BigNumber("100000", 10)

        self.assertEqual(number1 / number2, number3, "Number div simple failed")

    def test_div_0(self):
        number1 = BigNumber("30000000", 10)
        number2 = BigNumber("0", 10)

        with self.assertRaises(errors.DivisionByZero, msg="Div 0 result failed"):
            number1 / number2

    def test_pow_simple(self):
        number1 = BigNumber("100", 10)
        number2 = BigNumber("3", 10)
        number3 = BigNumber("1000000", 10)

        self.assertEqual(pow(number1,number2), number3, "Number pow simple failed")

    def test_pow_overflow(self):
        number1 = BigNumber("100", 10)
        number2 = BigNumber("6", 10)

        with self.assertRaises(errors.NumberSizeGreaterThanLimit, msg="pow overflow result failed"):
            pow(number1,number2)

    def test_root_simple(self):
        number1 = BigNumber("10000", 10)
        number2 = BigNumber("2", 10)
        number3 = BigNumber("100", 10)

        self.assertEqual(number1.root(number2), number3, "Number root simple failed")

    def test_root_aprox(self):
        number1 = BigNumber("5", 10)
        number2 = BigNumber("2", 10)
        number3 = BigNumber("2", 10)

        self.assertEqual(number1.root(number2), number3, "Number root aprox failed")

    def test_root_3(self):
        number1 = BigNumber("100", 10)
        number2 = BigNumber("6", 10)

        with self.assertRaises(errors.NotASquareRoot, msg="Non square root error raise failed"):
            number1.root(number2)

    def test_string_valid(self):
        number1 = BigNumber("123123000123123", 100)

        self.assertEqual(number1.value, "123123000123123", "Number string valid failed")

    def test_string_null(self):

        try:
            with self.assertRaises(errors.InvalidCharInNumberString, msg="null string verification failed"):
                number1 = BigNumber("", 100)
        except Exception as e:
            self.fail(f"null string verification failed wrong error")


TEST_CASES = [TestBigNumberInit, TestBigNumberOperations]


def main():
    local_test_suite = unittest.TestSuite()
    for case in TEST_CASES:
        for test_method in get_test_suite(case):
            local_test_suite.addTest(test_method)

    runner = unittest.TextTestRunner()
    runner.run(local_test_suite)


if __name__ == '__main__':
    main()
