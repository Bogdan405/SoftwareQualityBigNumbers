class BigNumber:

    def __init__(self, big_number_string: str, max_size: int):
        self.big_number = big_number_string

    def __add__(self, other: "BigNumber"):
        pass

    def __sub__(self, other: "BigNumber"):
        pass

    def __mul__(self, other: "BigNumber"):
        pass

    def __truediv__(self, other: "BigNumber"):
        pass

    def __pow__(self, power: "BigNumber", modulo=None):
        pass

    def square_root(self):
        pass

    @staticmethod
    def is_valid_big_number_string(big_number_string: str):
        pass

    class NegativeResult(ValueError):
        pass

    class InvalidCharInNumberString(ValueError):
        pass
    