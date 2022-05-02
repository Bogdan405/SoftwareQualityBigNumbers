from big_numbers import errors


class BigNumber:

    def __init__(self, big_number_string: str, max_size: int):
        self.validate_big_number_string(big_number_string, max_size)
        self.big_number_array = [int(c) for c in reversed(big_number_string)]
        self.max_size = max_size

    @property
    def value(self):
        return "".join([str(x) for x in reversed(self.big_number_array)])

    def __eq__(self, other):
        if len(self.big_number_array) != len(other.big_number_array):
            return False
        for index in range(len(self.big_number_array)):
            if self.big_number_array[index] != other.big_number_array[index]:
                return False
        return True

    def __le__(self, other):
        if len(self.big_number_array) > len(other.big_number_array):
            return False
        if len(self.big_number_array) < len(other.big_number_array):
            return True

        for index in reversed(range(len(self.big_number_array))):
            if self.big_number_array[index] > other.big_number_array[index]:
                return False
            if self.big_number_array[index] < other.big_number_array[index]:
                return True
        return True

    def __lt__(self, other):
        if len(self.big_number_array) > len(other.big_number_array):
            return False
        if len(self.big_number_array) < len(other.big_number_array):
            return True

        for index in reversed(range(len(self.big_number_array))):
            if self.big_number_array[index] > other.big_number_array[index]:
                return False
            if self.big_number_array[index] < other.big_number_array[index]:
                return True
        return False

    def __repr__(self):
        return self.value

    def __getitem__(self, key):
        return self.big_number_array[key]

    def __setitem__(self, key, value):
        self.big_number_array[key] = value

    def __copy__(self):
        return BigNumber(self.value, self.max_size)

    def __str__(self):
        return self.value

    def __add__(self, other: "BigNumber"):
        if len(self.big_number_array) < len(other.big_number_array):
            result = other.__copy__()
            b = self
        else:
            result = self.__copy__()
            b = other

        carry = 0

        for index in range(len(result.big_number_array)):
            result[index] += carry
            if index < len(b.big_number_array):
                result[index] += b[index]
            carry = result[index] // 10
            result[index] = result[index] % 10

        if carry:
            result.big_number_array.append(carry)

        if result.max_size < len(result.big_number_array):
            raise errors.NumberSizeGreaterThanLimit(result.value, result.max_size)

        return result

    def __sub__(self, other: "BigNumber"):
        if len(self.big_number_array) < len(other.big_number_array):
            raise errors.NegativeResult(self.value, other.value, "-")

        result = self.__copy__()
        b = other

        carry = 0
        for index in range(len(result.big_number_array)):
            result[index] += carry
            if index < len(b.big_number_array):
                result[index] -= b[index]
            carry = result[index] // 10
            result[index] = result[index] % 10

        if carry:
            raise errors.NegativeResult(self.value, other.value, "-")

        while not result[-1] and len(result.big_number_array) > 1:
            result.big_number_array = result[:-1]

        return result

    def __mul__(self, other: "BigNumber"):
        one = BigNumber("1", self.max_size)
        b = other.__copy__()
        result = BigNumber("0", self.max_size)
        while b.value != "0":
            result = result + self
            b = b - one
        return result

    def __truediv__(self, other: "BigNumber"):
        if len(self.big_number_array) < len(other.big_number_array):
            raise errors.NegativeResult(self.value, other.value, "-")

        if other.value == "0":
            raise errors.DivisionByZero(self, other)
        one = BigNumber("1", self.max_size)
        a = self.__copy__()
        result = BigNumber("0", self.max_size)
        while True:
            try:
                a = a - other
            except errors.NegativeResult:
                break
            result = result + one

        return result

    def __pow__(self, power: "BigNumber", modulo=None):
        one = BigNumber("1", self.max_size)
        b = power.__copy__()
        result = BigNumber("1", self.max_size)
        while b.value != "0":
            result = result * self
            b = b - one
        return result

    def root(self, root_number=2):

        if root_number != 2:
            raise errors.NotASquareRoot(root_number)

        zero = BigNumber("0", self.max_size)
        two = BigNumber("2", self.max_size)
        one = BigNumber("1", self.max_size)

        if self == zero:
            return zero

        left = one.__copy__()
        right = self.__copy__()
        v = one.__copy__()
        mid = zero.__copy__()

        while left <= right:
            mid = mid + left
            mid = mid + right

            mid = mid / two
            prod = mid * mid

            if prod <= self:
                v = mid.__copy__()
                mid = mid + one
                left = mid
            else:
                mid = mid - one
                right = mid

            mid = zero.__copy__()
        return v

    @staticmethod
    def validate_big_number_string(big_number_string: str, max_size: int):
        if big_number_string[0] == '0' and len(big_number_string) > 1:
            raise errors.ZeroStartingNumberString()

        valid_characters = "0123456789"
        for c in big_number_string:
            if c not in valid_characters:
                raise errors.InvalidCharInNumberString(c)

        if len(big_number_string) > max_size:
            raise errors.NumberSizeGreaterThanLimit(big_number_string, max_size)


def main():
    x = BigNumber("10000", 30)
    y = BigNumber("333", 30)
    print(x)
    print(x + y)
    print(x - y)
    print(x / y)
    print(x ** BigNumber("3", 30))
    print(x < y)
    print(x == x)
    print(x + BigNumber("0", 30))
    print(x.root())


if __name__ == '__main__':
    main()
