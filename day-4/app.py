"""Day 4: Ceres Search"""

import re
from typing import Final, Iterable, MutableSequence, Sequence, Tuple

SIZE: Final[int] = 140


def read_input() -> str:
    """Read the input file"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return file.read()


def to_diagonal(
    strings: Sequence[str], /, *, anchor: Tuple[int, int] = (0, 0)
) -> Sequence[str]:
    """Produce a sequence of diagonal strings from a given sequence (assuming a perfect square)"""

    if not strings:
        return ()

    size: int = len(strings[0])

    strings_diagonal: MutableSequence[str] = []

    depth: int
    string_diagonal: str
    x: int
    y: int
    true_x: int
    true_y: int

    depth
    for depth in range(size):
        string_diagonal = ""

        for y in range(depth + 1):
            x = depth - y

            true_x = abs(anchor[0] - x)
            true_y = abs(anchor[1] - y)

            string_diagonal += strings[true_x][true_y]

        strings_diagonal.append(string_diagonal)

    depth
    for depth in range(size - 1):
        true_depth = size - depth - 2

        string_diagonal = ""

        for a in range(size - depth - 1):
            y = depth + a + 1
            x = (true_depth - a) + depth + 1

            true_x = abs(anchor[0] - x)
            true_y = abs(anchor[1] - y)

            string_diagonal += strings[true_x][true_y]

        strings_diagonal.append(string_diagonal)

    return strings_diagonal


def count_xmas_in_string(string: str, /) -> int:
    return len(re.findall("XMAS", string))


def count_xmas_in_strings(strings: Sequence[str], /) -> int:
    return sum(map(count_xmas_in_string, strings))


# Load the entire dataset into memory
dataset: str = read_input()

# --- Part One ---

lines_horizontal: Sequence[str] = dataset.splitlines()
lines_vertical: Sequence[str] = tuple("".join(line) for line in zip(*lines_horizontal))
lines_diagonal_left: Sequence[str] = to_diagonal(lines_horizontal, anchor=(0, 0))
lines_diagonal_right: Sequence[str] = to_diagonal(
    lines_horizontal, anchor=(0, SIZE - 1)
)

seq_of_lines: Sequence[Sequence[str]] = (
    lines_horizontal,
    lines_vertical,
    lines_diagonal_left,
    lines_diagonal_right,
)

total_xmas_occurences: int = 0

lines: Sequence[str]
for lines in seq_of_lines:
    lines_inv: Sequence[str] = tuple(line[::-1] for line in lines)

    total_xmas_occurences += count_xmas_in_strings(lines)
    total_xmas_occurences += count_xmas_in_strings(lines_inv)

print("Part 1:", total_xmas_occurences)
assert total_xmas_occurences == 2468

# --- Part Two ---

# ...
