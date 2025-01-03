"""Day 7: Bridge Repair"""

import itertools
import math
from dataclasses import dataclass
from operator import add as operator_add
from operator import mul as operator_mul
from typing import Collection, Final, Iterable, Protocol, Sequence


def concatenate(a: int, b: int, /) -> int:
    shift: int = math.floor(math.log(abs(b), 10) + 1)

    return a * 10**shift + b


class Operator(Protocol):
    def __call__(self, x: int, y: int, /) -> int: ...


OPERATOR_ADD: Final[Operator] = operator_add
OPERATOR_MUL: Final[Operator] = operator_mul
OPERATOR_CON: Final[Operator] = concatenate


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
    return tuple(map(parse_line, dataset.splitlines()))


def validate_equation(
    equation: Equation, /, *, operators: Collection[Operator]
) -> bool:
    operators_product: Iterable[Sequence[Operator]] = itertools.product(
        operators, repeat=len(equation.operands) - 1
    )

    operators_combo: Sequence[Operator]
    for operators_combo in operators_product:
        value: int = 0

        index: int
        operator: Operator
        for index, operator in enumerate(operators_combo):
            lhs: int = equation.operands[0] if index == 0 else value
            rhs: int = equation.operands[index + 1]

            value = operator(lhs, rhs)

        if value == equation.test_value:
            return True

    return False


def calculate_total_calibration_result(
    equations: Iterable[Equation], /, *, operators: Collection[Operator]
) -> int:
    total_calibration_result: int = 0

    equation: Equation
    for equation in equations:
        if validate_equation(equation, operators=operators):
            total_calibration_result += equation.test_value

    return total_calibration_result


def main() -> None:
    raw_dataset: str = read_dataset()
    all_equations: Iterable[Equation] = parse_dataset(raw_dataset)

    part_1: int = calculate_total_calibration_result(
        all_equations, operators=(OPERATOR_ADD, OPERATOR_MUL)
    )
    print("Part 1:", part_1)
    assert part_1 == 1985268524462

    part_2: int = calculate_total_calibration_result(
        all_equations, operators=(OPERATOR_ADD, OPERATOR_MUL, OPERATOR_CON)
    )
    print("Part 2:", part_2)
    assert part_2 == 150077710195188


if __name__ == "__main__":
    main()
