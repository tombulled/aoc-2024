"""Day 3: Mull It Over"""

from dataclasses import dataclass
import re
from enum import Enum
from typing import Final, Generator, Iterable, Optional, Sequence


class Operator(str, Enum):
    def __str__(self) -> str:
        return self.value

    MUL: str = "mul"
    DO: str = "do"
    DONT: str = "don't"


@dataclass
class Instruction:
    operator: Operator
    operands: Sequence[str]


def _build_instruction_pattern(operator: Operator, *operands: str) -> str:
    return rf"{operator}\({','.join(operands)}\)"


PATTERN_OPERATOR: Final[str] = rf"(?P<operator>{'|'.join(Operator)})"

OPERATOR: Final[str] = r"[a-z']+"
OPERAND: Final[str] = r"\d{1,3}"
# OPERANDS: Final[str] = rf"(?:{OPERAND},)*{OPERAND}?"

# NO_OPERANDS: Final[str] = ""
# OPERANDS_DO: Final[str] = NO_OPERANDS
# OPERANDS_DONT: Final[str] = NO_OPERANDS
# OPERANDS_MUL: Final[str] = r"(?P<lhs>\d{1,3}),(?P<rhs>\d{1,3})"

PATTERN_INSTRUCTION: Final[str] = r"(?P<operator>[a-z']+)\((?P<operands>.*)\)"
# PATTERN_MUL: Final[str] = r"mul\((?P<lhs>\d{1,3}),(?P<rhs>\d{1,3})\)"
# PATTERN_DO: Final[str] = r"do\(\)"
# PATTERN_DONT: Final[str] = r"don't\(\)"
# PATTERN_INSTRUCTION: Final[str] = f"{PATTERN_MUL}|{PATTERN_DO}|{PATTERN_DONT}"

PATTERN_MUL: Final[str] = _build_instruction_pattern(Operator.MUL, OPERAND, OPERAND)
PATTERN_DO: Final[str] = _build_instruction_pattern(Operator.DO)
PATTERN_DONT: Final[str] = _build_instruction_pattern(Operator.DONT)

PATTERN_INSTRUCTIONS: Final[str] = "|".join((PATTERN_MUL, PATTERN_DO, PATTERN_DONT))


def read_input() -> str:
    """Read the input file"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return file.read()


def find_instructions() -> Generator[Instruction, None, None]:
    instructions: Sequence[str] = re.findall(PATTERN_INSTRUCTIONS, dataset)

    instruction: str
    for instruction in instructions:
        instruction_match: Optional[re.Match] = re.match(
            PATTERN_INSTRUCTION, instruction
        )

        assert instruction_match is not None

        raw_operator: str
        raw_operands: str
        raw_operator, raw_operands = instruction_match.groups()

        operator: Operator = Operator(raw_operator)
        operands: Sequence[str] = raw_operands.split(",")

        yield Instruction(operator, operands)


"""Solution for AoC 2024, Day 3, Parts 1 & 2"""

# Load the entire dataset into memory
dataset: str = read_input()

# --- Part One ---
sum_of_multiplications: int = sum(
    int(lhs) * int(rhs)
    for lhs, rhs in re.findall(r"mul\((?P<lhs>\d{1,3}),(?P<rhs>\d{1,3})\)", dataset)
)
print("Sum of Multiplications:", sum_of_multiplications)
assert sum_of_multiplications == 175700056

# --- Part Two ---

do: bool = True

instruction: Instruction
for instruction in find_instructions():
    if instruction.operator is Operator.DO:
        do = True
    elif instruction.operator is Operator.DONT:
        do = False
    elif instruction.operator is Operator.MUL:
        print("mul", instruction.operands)
