"""Day 8: Resonant Collinearity"""

from typing import (
    Collection,
    Final,
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
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
    """Read the input file"""

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


dataset: str = read_dataset()
grid: Grid[str] = parse_dataset(dataset)

antenna_coords = tuple(find_antennas(grid))

# group antennas by frequency
af = group_antennas(antenna_coords)

# create all combinations of antennas (of the same frequency)
