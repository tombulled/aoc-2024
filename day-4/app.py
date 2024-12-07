"""Day 4: Ceres Search"""

import re
from typing import Iterable, MutableSequence, Sequence, Tuple

size = 140  # TEMP


def read_input() -> str:
    """Read the input file"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return file.read()


def to_diagonal(
    strings: Sequence[str], /, *, anchor: Tuple[int, int] = (0, 0)
) -> Sequence[str]:
    # n.b. assumes a perfect square

    if not strings:
        return ()

    size: int = len(strings[0])

    strings_diagonal: MutableSequence[str] = []

    depth: int
    for depth in range(size):
        string_diagonal: str = ""

        y: int
        for y in range(depth + 1):
            x: int = depth - y

            # true_x: int = abs(anchor[0] - x)
            # true_y: int = abs(anchor[1] - y)

            character: str = strings[x][y]

            string_diagonal += character

        strings_diagonal.append(string_diagonal)

    depth: int
    for depth in range(size - 1):
        dn = size - depth - 2

        string_diagonal: str = ""

        for a in range(size - depth - 1):
            y = depth + a + 1
            x = (dn - a) + depth + 1
            character: str = strings[x][y]
            string_diagonal += character

        strings_diagonal.append(string_diagonal)

    return strings_diagonal


# def to_diagonal_inv(strings: Sequence[str], /) -> Sequence[str]:
#     # n.b. assumes a perfect square

#     if not strings:
#         return ()

#     size: int = len(strings[0])

#     strings_diagonal: MutableSequence[str] = []

#     depth: int
#     for depth in range(size):
#         string_diagonal: str = ""

#         y: int
#         for y in range(depth+1):
#             x: int = depth - y

#             character: str = strings[size-x-1][size-y-1]

#             string_diagonal += character

#         strings_diagonal.append(string_diagonal)

#     depth: int
#     for depth in range(size-1):
#         dn = size-depth-2

#         string_diagonal: str = ""

#         for a in range(size-depth-1):
#             y=depth+a+1
#             x=(dn-a)+depth+1
#             character: str = strings[size-x-1][size-y-1]
#             string_diagonal += character

#         strings_diagonal.append(string_diagonal)

#     return strings_diagonal


def count_xmas_in_string(string: str, /) -> int:
    return len(re.findall("XMAS", string))


def count_xmas_in_strings(strings: Sequence[str], /) -> int:
    return sum(map(count_xmas_in_string, strings))


# Load the entire dataset into memory
dataset: str = read_input()
# dataset: str = (
#     """
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX""".strip()
# )

# dataset: str = """
# ABC
# BCD
# CDE
# """.strip()
# dataset: str = """
# ABCD
# BCDE
# CDEF
# DEFG
# """.strip()
# dataset: str = """
# ABCDE
# BCDEF
# CDEFG
# DEFGH
# EFGHI
# """.strip()

lines_horizontal: Sequence[str] = dataset.splitlines()
lines_vertical: Sequence[str] = tuple("".join(line) for line in zip(*lines_horizontal))
lines_diagonal: Sequence[str] = to_diagonal(lines_horizontal)
lines_diagonal_inv: Sequence[str] = to_diagonal_inv(lines_horizontal)

seq_of_lines: Sequence[Sequence[str]] = (
    lines_horizontal,
    lines_vertical,
    lines_diagonal,
    lines_diagonal_inv,
)

total_xmas_occurences: int = 0

lines: Sequence[str]
for lines in seq_of_lines:
    lines_inv: Sequence[str] = tuple(line[::-1] for line in lines)

    total_xmas_occurences += count_xmas_in_strings(lines)
    total_xmas_occurences += count_xmas_in_strings(lines_inv)

print("Part 1:", total_xmas_occurences)
