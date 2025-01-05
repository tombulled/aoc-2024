"""Day 8: Resonant Collinearity"""

import itertools
from typing import (
    Collection,
    Final,
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
    Set,
    Tuple,
    TypeAlias,
    TypeVar,
)

# Typing
T = TypeVar("T")
Coord: TypeAlias = Tuple[int, int]
Grid: TypeAlias = Sequence[Sequence[T]]
MutableGrid: TypeAlias = MutableSequence[MutableSequence[T]]

# Constants
VALUE_EMPTY: Final[str] = "."
VALUE_ANTINODE: Final[str] = "#"

# Temp
EXAMPLE_INPUT: Final[str] = (
    """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()
)


def read_dataset() -> str:
    with open("input", encoding="utf-8") as file:
        return file.read()


def parse_dataset(dataset: str, /) -> Grid[str]:
    return dataset.splitlines()


def grid_get(grid: Grid[T], /, x: int, y: int) -> T:
    return grid[y][x]


def grid_size(grid: Grid[T], /) -> Tuple[int, int]:
    size_y: int = len(grid)
    size_x: int = len(grid[0]) if grid else 0

    return (size_x, size_y)


def grid_set(grid: MutableGrid[T], /, x: int, y: int, value: T) -> None:
    grid[y][x] = value


# def grid_row(grid: Grid[T], y: int, /) -> Sequence[T]:
#     return grid[y]


# def grid_column(grid: Grid[T], x: int, /) -> Sequence[T]:
#     return tuple(row[x] for row in grid)


# def grid_columns(grid: Grid[T], /) -> Sequence[Sequence[T]]:
#     size_x: int
#     size_x, _ = grid_size(grid)

#     return tuple(grid_column(grid, x) for x in range(size_x))


def grid_iter(grid: Grid[T], /) -> Iterable[Tuple[Coord, T]]:
    size_x: int
    size_y: int
    size_x, size_y = grid_size(grid)

    y: int
    for y in range(size_y):
        x: int
        for x in range(size_x):
            value: T = grid_get(grid, x, y)

            yield ((x, y), value)


def grid_contains(grid: Grid[T], /, x: int, y: int) -> bool:
    size_x: int
    size_y: int
    size_x, size_y = grid_size(grid)

    return x >= 0 and x < size_x and y >= 0 and y < size_y


def grid_print(grid: Grid[T], /) -> None:
    row: Sequence[T]
    for row in grid:
        value: T
        for value in row:
            print(value, end="")

        print()


def find_antennas(grid: Grid[str], /) -> Iterable[Tuple[Coord, str]]:
    coord: Coord
    value: str
    for coord, value in grid_iter(grid):
        if value == VALUE_EMPTY:
            continue

        yield (coord, value)


def group_antennas(
    antennas: Iterable[Tuple[Coord, str]], /
) -> Mapping[str, Collection[Coord]]:
    grouped_antennas: MutableMapping[str, MutableSequence[Coord]] = {}

    coord: Coord
    antenna: str
    for coord, antenna in antennas:
        grouped_antennas.setdefault(antenna, []).append(coord)

    return grouped_antennas


def pair_antennas(
    antennas: Iterable[Tuple[Coord, str]], /
) -> Iterable[Tuple[Coord, Coord]]:
    grouped_antennas: Mapping[str, Collection[Coord]] = group_antennas(antennas)

    coords: Collection[Coord]
    for coords in grouped_antennas.values():
        yield from itertools.combinations(coords, 2)


def calculate_translation(coord_1: Coord, coord_2: Coord, /) -> Coord:
    """Calculate the translation needed to translate coord_1 onto coord_2"""

    x_1: int
    y_1: int
    x_1, y_1 = coord_1

    x_2: int
    y_2: int
    x_2, y_2 = coord_2

    dx = x_2 - x_1
    dy = y_2 - y_1

    return (dx, dy)


def translate_coord(coord: Coord, translation: Coord, multiplier: int = 1) -> Coord:
    x: int
    y: int
    x, y = coord

    translation_x: int
    translation_y: int
    translation_x, translation_y = translation

    return (x + (translation_x * multiplier), y + (translation_y * multiplier))


def calculate_antinode_coords(coord_1: Coord, coord_2: Coord, /) -> Tuple[Coord, Coord]:
    dx: int
    dy: int
    dx, dy = calculate_translation(coord_1, coord_2)

    translation: Coord = (dx, dy)
    translation_inv: Coord = (-dx, -dy)

    # translation: Coord = calculate_translation(coord_1, coord_2)

    # all_coords: Set[Coord] = {
    #     translate_coord(coord_1, translation_pos, ),
    #     translate_coord(coord_1, translation_neg),
    #     translate_coord(coord_2, translation_pos),
    #     translate_coord(coord_2, translation_neg),
    # }

    # return all_coords - {coord_1, coord_2}

    return (
        # translate_coord(coord_1, translation, multiplier=-1),
        # translate_coord(coord_1, translation, multiplier=2),
        translate_coord(coord_1, translation_inv),
        translate_coord(coord_2, translation),
    )


dataset: str = read_dataset()
grid: Grid[str] = parse_dataset(dataset)

antenna_coords = tuple(find_antennas(grid))

# group antennas by frequency
# af = group_antennas(antenna_coords)

# create all combinations of antennas (of the same frequency)
pa = pair_antennas(antenna_coords)

antenna_1: Coord
antenna_2: Coord
for antenna_1, antenna_2 in pa:
    antinode_coords: Collection[Coord] = calculate_antinode_coords(antenna_1, antenna_2)
    print(antenna_1, antenna_2, "->", antinode_coords)
