import ast
import operator
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ToolResult:
    name: str
    content: str


class SafeCalculator:
    """
    Safe arithmetic calculator.

    Supports:
    - addition
    - subtraction
    - multiplication
    - division
    - power
    - parentheses

    Does NOT use eval().
    """

    _allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def calculate(self, expression: str) -> float:
        if len(expression) > 100:
            raise ValueError("Expression is too long.")

        parsed = ast.parse(expression, mode="eval")
        return self._eval_node(parsed.body)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)

            if operator_type not in self._allowed_operators:
                raise ValueError("Operator is not allowed.")

            left_value = self._eval_node(node.left)
            right_value = self._eval_node(node.right)

            return self._allowed_operators[operator_type](left_value, right_value)

        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)

            if operator_type not in self._allowed_operators:
                raise ValueError("Operator is not allowed.")

            operand_value = self._eval_node(node.operand)
            return self._allowed_operators[operator_type](operand_value)

        raise ValueError("Invalid expression.")


class ToolService:
    """
    Tool service for the AI character agent.

    Current tools:
    - calculator tool triggered by: calculate: 2 + 2 or calc: 2 + 2
    - action guide for fake animation states
    """

    def __init__(self) -> None:
        self._calculator = SafeCalculator()

    def run_tool_if_needed(self, user_message: str) -> Optional[ToolResult]:
        calculator_match = re.search(
            r"(?:calculate|calc):\s*(.+)",
            user_message,
            re.IGNORECASE,
        )

        if calculator_match:
            expression = calculator_match.group(1).strip()

            try:
                result = self._calculator.calculate(expression)

                if isinstance(result, float) and result.is_integer():
                    formatted_result = str(int(result))
                else:
                    formatted_result = str(result)

                return ToolResult(
                    name="calculator",
                    content=f"Calculator result for '{expression}' is {formatted_result}.",
                )
            except Exception as error:
                return ToolResult(
                    name="calculator",
                    content=f"Calculator error: {error}",
                )

        return None

    def get_action_guide(self) -> str:
        return """
Available fake animation actions:
- wave: greeting or welcoming the user
- smile: friendly or positive response
- think: reasoning or considering options
- explain: teaching or technical explanation
- encourage: motivating the user
- idle: no special action needed
"""
