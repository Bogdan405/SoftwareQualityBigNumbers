from big_numbers.big_number import BigNumber
from pathlib import Path


class PostfixExpression:

    def __init__(self, expression_string: str):
        self.expression_stack = self.build_expression_stack(expression_string)
        self.current_result = None
        self.current_expression = None
        self.executed_expression = None

    def advance(self):
        pass

    def remaining_stack_to_expression_string(self):
        pass

    def export_to_xml(self, input_xml_path: Path):
        pass

    def import_from_xml(self, output_xml_path: Path):
        pass

    @staticmethod
    def build_expression_stack(expression_string: str) -> list:
        return []
