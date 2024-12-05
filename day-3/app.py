"""Day 3: Mull It Over"""

from enum import Enum
import operator
import re
from typing import Final, Iterable, Optional, Sequence


class Operator(str, Enum):
    def __str__(self) -> str:
        return self.value

    MUL: str = "mul"
    DO: str = "do"
    DONT: str = "don't"


def _build_instruction_pattern(
    # operator: Operator, operands: Optional[str] = None, /
    operator: Operator, *operands: str
) -> str:
    # return f"(?P<instruction>(?P<{operator}>[a-z]+)\({operands}\))"
    # return f"(?P<operator>{operator})\({operands or ''}\)"
    return f"{operator}\({','.join(operands)}\)"


PATTERN_OPERATOR: Final[str] = f"(?P<operator>{'|'.join(Operator)})"

OPERATOR: Final[str] = r"[a-z]+"
OPERAND: Final[str] = r"\d{1,3}"
OPERANDS: Final[str] = f"(?:{OPERAND},)*{OPERAND}?"

NO_OPERANDS: Final[str] = ""
OPERANDS_DO: Final[str] = NO_OPERANDS
OPERANDS_DONT: Final[str] = NO_OPERANDS
OPERANDS_MUL: Final[str] = r"(?P<lhs>\d{1,3}),(?P<rhs>\d{1,3})"

PATTERN_INSTRUCTION: Final[str] = r"(?P<instruction>)\((?P<operands>.*?)\)"
PATTERN_MUL: Final[str] = r"mul\((?P<lhs>\d{1,3}),(?P<rhs>\d{1,3})\)"
# PATTERN_DO: Final[str] = r"do\(\)"
# PATTERN_DONT: Final[str] = r"don't\(\)"
# PATTERN_INSTRUCTION: Final[str] = f"{PATTERN_MUL}|{PATTERN_DO}|{PATTERN_DONT}"


def read_input() -> str:
    """Read the input file"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return file.read()


"""Solution for AoC 2024, Day 3, Parts 1 & 2"""

# Load the entire dataset into memory
input: str = read_input()

# --- Part One ---
sum_of_multiplications: int = sum(
    operator.mul(int(lhs), int(rhs))
    for lhs, rhs in re.findall(r"mul\((?P<lhs>\d{1,3}),(?P<rhs>\d{1,3})\)", input)
)
print("Sum of Multiplications:", sum_of_multiplications)
assert sum_of_multiplications == 175700056

# --- Part Two ---

# def find_instructions() -> Sequence[str]:

# p = _build_instruction_pattern(Operator.MUL, OPERANDS_MUL)
# p=PATTERN_OPERATOR
p = "|".join(
    (
        _build_instruction_pattern(Operator.MUL, OPERAND, OPERAND),
        _build_instruction_pattern(Operator.DO),
    )
)

instructions: Sequence[str] = re.findall(p, input)

d = instructions
