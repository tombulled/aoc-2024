"""Day 3: Mull It Over"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Final, Generator, Iterable, Optional, Sequence


class Operator(str, Enum):
    """Known instruction operators"""

    def __str__(self) -> str:
        return self.value

    MUL: str = "mul"
    DO: str = "do"
    DONT: str = "don't"


@dataclass
class Instruction:
    """Container for the component parts of an instruction (operator & operands)"""

    operator: Operator
    operands: Sequence[str] = field(default_factory=tuple)


def _build_instruction_pattern(operator: Operator, *operands: str) -> str:
    """Build a composite instruction pattern from operator & operand patterns"""

    return rf"{operator}\({OPERAND_SEP.join(operands)}\)"


OPERATOR: Final[str] = r"[a-z']+"
OPERAND: Final[str] = r"\d{1,3}"
OPERAND_SEP: Final[str] = ","

PATTERN_MUL: Final[str] = _build_instruction_pattern(Operator.MUL, OPERAND, OPERAND)
PATTERN_DO: Final[str] = _build_instruction_pattern(Operator.DO)
PATTERN_DONT: Final[str] = _build_instruction_pattern(Operator.DONT)

PATTERN_INSTRUCTION: Final[str] = rf"(?P<operator>{OPERATOR}+)\((?P<operands>.*)\)"
PATTERN_INSTRUCTIONS: Final[str] = "|".join((PATTERN_MUL, PATTERN_DO, PATTERN_DONT))


def read_input() -> str:
    """Read the input file"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return file.read()


def find_instructions(string: str, /) -> Generator[Instruction, None, None]:
    """Find (and yield) all instructions in a given string"""

    instructions: Sequence[str] = re.findall(PATTERN_INSTRUCTIONS, string)

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
        operands: Sequence[str] = raw_operands.split(OPERAND_SEP)

        yield Instruction(operator, operands)


def main() -> None:
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
    sum_of_multiplications_conditional: int = 0

    instruction: Instruction
    for instruction in find_instructions(dataset):
        match instruction.operator:
            case Operator.DO:
                do = True
            case Operator.DONT:
                do = False
            case Operator.MUL:
                if not do:
                    continue

                lhs: int
                rhs: int
                lhs, rhs = map(int, instruction.operands)

                sum_of_multiplications_conditional += lhs * rhs

    print("Sum of Multiplications (Conditional):", sum_of_multiplications_conditional)
    assert sum_of_multiplications_conditional == 71668682


if __name__ == "__main__":
    main()
