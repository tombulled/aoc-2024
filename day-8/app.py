"""Day 8: Resonant Collinearity"""

from typing import Final, Iterable, MutableSequence, Sequence, Tuple, TypeAlias, TypeVar

# Typing
T = TypeVar("T")
Coord: TypeAlias = Tuple[int, int]
Grid: TypeAlias = Sequence[Sequence[T]]
MutableGrid: TypeAlias = MutableSequence[MutableSequence[T]]

# Constants
EMPTY: Final[str] = "."

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


dataset: str = read_dataset()
grid: Grid[str] = parse_dataset(dataset)

coord: Coord
value: str
for coord, value in grid_iter(grid):
    print(coord, value)