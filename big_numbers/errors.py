class NegativeResult(ValueError):
    def __init__(self, value1, value2, operator):
        super(NegativeResult, self).__init__(f"The resulted big number would be negative: {value1} {operator} {value2}")


class InvalidCharInNumberString(ValueError):
    def __init__(self, invalid_character):
        super(InvalidCharInNumberString, self).__init__(
            f"The number string contains the invalid character '{invalid_character}'")


class ZeroStartingNumberString(ValueError):
    def __init__(self):
        super(ZeroStartingNumberString, self).__init__("The number string starts with zero")


class NumberSizeGreaterThanLimit(ValueError):
    def __init__(self, big_number_string, max_size):
        super(NumberSizeGreaterThanLimit, self).__init__(
            f"The number string {big_number_string} is bigger than the allowed limit {max_size}")


class DivisionByZero(ValueError):
    def __init__(self, a, b):
        super(DivisionByZero, self).__init__(
            f"Cannot divide by 0 in: {a} / {b}")


class NotASquareRoot(ValueError):
    def __init__(self, a):
        super(NotASquareRoot, self).__init__(
            f"Invalid root {a}. Application can only take square roots, for now...")
