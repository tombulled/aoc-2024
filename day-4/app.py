"""Day 4: Ceres Search"""

from typing import Iterable, MutableSequence, Sequence

size = 140  # TEMP


def read_input() -> str:
    """Read the input file"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return file.read()


def to_diagonal(strings: Sequence[str], /) -> Sequence[str]:
    # n.b. assumes a perfect square

    if not strings:
        return ()

    size: int = len(strings[0])

    strings_diagonal: MutableSequence[str] = []

    depth: int
    for depth in range(size):
        string_diagonal: str = ""

        x: int
        for x in range(depth+1):
            y: int = depth - x

            character: str = strings[x][y]

            string_diagonal += character

            print((x, y), character)

        print(string_diagonal)
        print()

        # strings_diagonal.append(string_diagonal)

    print("---")

    # d2: int
    # for d2 in range(size-1, 0, -1):
    #     print(d2)
    #     a: int
    #     for a in range(d2):
    #         x = a+1
    #         y = depth-a
    #         character: str = strings[x][y]
    #         print((x, y), character)
    #     print()
    depth: int
    for depth in range(size-1):
        # print("#" * (depth+1))
        dn = size-depth-2
        print(depth, dn)
        for a in range(size-depth-1):
            # x=depth-a+1
            x=depth+a+1
            # y=size-depth-a-1
            y=(dn-a)+depth+1
            character: str = strings[x][y]
            # y = (size-depth)-x
            print("\t", a, dn-a, (x,y)) # , size-depth-a, size-depth-a, ((dn-a)+depth+1)), character)
        #     print("#", end="")dn-a
        # print()

    return strings_diagonal


# Load the entire dataset into memory
# dataset: str = read_input()
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
dataset: str = """
ABCD
BCDE
CDEF
DEFG
""".strip()

lines_horizontal: Sequence[str] = dataset.splitlines()
lines_vertical: Sequence[str] = tuple("".join(line) for line in zip(*lines_horizontal))
lines_diagonal: Sequence[str] = to_diagonal(lines_horizontal)
