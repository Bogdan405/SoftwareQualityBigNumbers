class MisplacedSymbol(ValueError):
    def __init__(self, invalid_character, current_expression):
        super(MisplacedSymbol, self).__init__(
            f"The expression could not be completely solved, misplaced symbol:"
            f" '{invalid_character}' near {current_expression}")


class IllegalSymbol(ValueError):
    def __init__(self, invalid_character, pos):
        super(MisplacedSymbol, self).__init__(
            f"The expression contains a misplaced or illegal character '{invalid_character}' at position {pos}")
