"""Day 7: Bridge Repair"""

import itertools
import operator
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Protocol, Sequence


class OperatorFn(Protocol):
    def __call__(self, x: int, y: int, /) -> int: ...


class Operator(Enum):
    symbol: str
    func: OperatorFn

    ADD = ("+", operator.add)
    MULTIPLY = ("*", operator.mul)

    def __init__(self, symbol: str, func: OperatorFn, /) -> None:
        self.symbol = symbol
        self.func = func

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.name}>"


@dataclass
class Equation:
    test_value: int
    operands: Sequence[int]


def read_dataset() -> str:
    with open("input", encoding="utf-8") as file:
        return file.read()


def parse_line(line: str, /) -> Equation:
    raw_test_value: str
    raw_operands: str
    raw_test_value, raw_operands = line.split(": ", 1)

    return Equation(
        test_value=int(raw_test_value),
        operands=tuple(map(int, raw_operands.split())),
    )


def parse_dataset(dataset: str, /) -> Iterable[Equation]:
    return map(parse_line, dataset.splitlines())


def validate_equation(equation: Equation, /) -> bool:
    operators_product: Iterable[Sequence[Operator]] = itertools.product(
        iter(Operator), repeat=len(equation.operands) - 1
    )

    operators: Sequence[Operator]
    for operators in operators_product:
        value: int = 0

        index: int
        operator: Operator
        for index, operator in enumerate(operators):
            lhs: int = equation.operands[0] if index == 0 else value
            rhs: int = equation.operands[index + 1]

            value = operator.func(lhs, rhs)

        if value == equation.test_value:
            return True

    return False


dataset: str = read_dataset()
equations: Iterable[Equation] = parse_dataset(dataset)

total_calibration_result: int = 0

equation: Equation
for equation in equations:
    if validate_equation(equation):
        total_calibration_result += equation.test_value

print("Part 1:", total_calibration_result)
assert total_calibration_result == 1985268524462
