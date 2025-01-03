"""Day 7: Bridge Repair"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Final, Iterable, Sequence

EXAMPLE_INPUT: Final[str] = (
    """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()
)


class Operator(str, Enum):
    ADD = "+"
    MULTIPLY = "*"


@dataclass
class Equation:
    test_value: int
    operands: Sequence[int]


def read_dataset() -> str:
    """Read the input file"""

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
    raise NotImplementedError # TODO

dataset: str = read_dataset()
equations: Iterable[Equation] = parse_dataset(dataset)
