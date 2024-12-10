"""Day 4: Ceres Search"""

import re
from enum import Enum, auto
from typing import Any, Iterable, MutableSequence, Sequence, Tuple, TypeAlias, TypeVar

# Typing
T = TypeVar("T")
Coord: TypeAlias = Tuple[int, int]
Grid: TypeAlias = Sequence[Sequence[T]]
MutableGrid: TypeAlias = MutableSequence[MutableSequence[T]]

# Constants
ROOT: Coord = (0, 0)


class DiagonalDirection(Enum):
    TL_TO_BR = auto()
    TR_TO_BL = auto()
    BL_TO_TR = auto()
    BR_TO_TL = auto()


def read_input() -> Grid[str]:
    """Read the input file"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return file.read().splitlines()


def get_grid_size(grid: Grid[Any], /) -> Tuple[int, int]:
    if not grid:
        return (0, 0)

    size_x: int = len(grid[0])
    size_y: int = len(grid)

    return (size_x, size_y)


def get_square_grid_size(grid: Grid[Any], /) -> int:
    size_x: int
    size_y: int
    size_x, size_y = get_grid_size(grid)

    assert size_x == size_y, f"Grid is not a square ({size_x}x{size_y})"

    return size_x


# todo: make generic, and accept a grid instead?
def get_diagonals(
    grid: Grid[T], /, direction: DiagonalDirection = DiagonalDirection.TL_TO_BR
) -> Sequence[Sequence[T]]:
    """
    Produce a sequence of diagonals from a given grid.

    WARN: The algorithm assumes the grid is a square.

    Example:
        Diagonals of:
            ABC
            DEF
            GHI
        Are:
            A, DB, GEC, HF, I
    """

    if not grid:
        return ()

    size: int = get_square_grid_size(grid)

    diagonals: MutableGrid[T] = []

    # depth: int
    # string_diagonal: str
    # x: int
    # y: int
    # true_x: int
    # true_y: int

    # for depth in range(size):
    #     string_diagonal = ""

    #     for y in range(depth + 1):
    #         x = depth - y

    #         true_x = abs(anchor[0] - x)
    #         true_y = abs(anchor[1] - y)

    #         string_diagonal += strings[true_x][true_y]

    #     strings_diagonal.append(string_diagonal)

    # for depth in range(size - 1):
    #     string_diagonal = ""

    #     for a in range(size - depth - 1):
    #         y = depth + a + 1
    #         x = size - a - 1

    #         true_x = abs(anchor[0] - x)
    #         true_y = abs(anchor[1] - y)

    #         string_diagonal += strings[true_x][true_y]

    #     strings_diagonal.append(string_diagonal)

    # return strings_diagonal

    return ()  # TEMP

def count_occurences(row: Sequence[T], subset: Sequence[T], /) -> int:
    value: T
    for value in row:
        

# def count_xmas_in_strings(strings: Sequence[str], /) -> int:
#     return sum(len(re.findall("XMAS", string)) for string in strings)


# Load the entire dataset into memory
dataset: Grid[str] = read_input()

# --- Part One ---

size: int = get_square_grid_size(dataset)

lines_horizontal: Sequence[str] = tuple("".join(line) for line in dataset)
lines_vertical: Sequence[str] = tuple("".join(line) for line in zip(*lines_horizontal))
# lines_diagonal_left: Sequence[str] = get_diagonals(lines_horizontal, anchor=(0, 0))
# lines_diagonal_right: Sequence[str] = get_diagonals(
#     lines_horizontal, anchor=(0, size - 1)
# )

# seq_of_lines: Sequence[Sequence[str]] = (
#     lines_horizontal,
#     lines_vertical,
#     lines_diagonal_left,
#     lines_diagonal_right,
# )

# total_xmas_occurences: int = 0

# lines: Sequence[str]
# for lines in seq_of_lines:
#     lines_inv: Sequence[str] = tuple(line[::-1] for line in lines)

#     total_xmas_occurences += count_xmas_in_strings(lines)
#     total_xmas_occurences += count_xmas_in_strings(lines_inv)

# print("Part 1:", total_xmas_occurences)
# assert total_xmas_occurences == 2468

# # --- Part Two ---


# def find_all_a_coords(letters: Sequence[Sequence[str]], /) -> Sequence[Tuple[int, int]]:
#     if not letters:
#         return ()

#     size_x: int = len(letters[0])
#     size_y: int = len(letters)

#     coords: MutableSequence[Tuple[int, int]] = []

#     x: int
#     for x in range(size_x):
#         y: int
#         for y in range(size_y):
#             letter: str = letters[x][y]

#             if letter == "A":
#                 coords.append((x, y))

#     return coords


# def get_cross_words_for_coord(
#     letters: Sequence[Sequence[str]], coord: Tuple[int, int], /
# ) -> Sequence[str]:
#     size: int = len(letters[0])
#     bounds: Tuple[int, int] = (0, size - 1)

#     x: int
#     y: int
#     x, y = coord

#     if x in bounds or y in bounds:
#         # Don't bother doing anything, as there can be at most two
#         # letters per diag as we're at a corner.
#         return ()

#     tl_to_br: str = "".join(
#         (
#             letters[x - 1][y - 1],
#             letters[x][y],
#             letters[x + 1][y + 1],
#         )
#     )
#     tr_to_bl: str = "".join(
#         (
#             letters[x + 1][y - 1],
#             letters[x][y],
#             letters[x - 1][y + 1],
#         )
#     )

#     return (tl_to_br, tr_to_bl)


# coords: Sequence[Tuple[int, int]] = find_all_a_coords(lines_horizontal)

# total_count_of_x_mas: int = 0

# coord: Tuple[int, int]
# for coord in coords:
#     cross_words: Sequence[str] = get_cross_words_for_coord(lines_horizontal, coord)

#     if not cross_words:
#         continue

#     cross_words_inv: Sequence[str] = tuple(
#         cross_word[::-1] for cross_word in cross_words
#     )

#     all_cross_words: Sequence[str] = (*cross_words, *cross_words_inv)
#     count_of_x_mas: int = sum(map(lambda line: line == "MAS", all_cross_words))

#     if count_of_x_mas == 2:
#         total_count_of_x_mas += 1

# print("Part 2:", total_count_of_x_mas)
# assert total_count_of_x_mas == 1864
