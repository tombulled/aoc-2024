"""Day 6: Guard Gallivant"""

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property
from typing import (
    ClassVar,
    Collection,
    Final,
    Generic,
    Iterable,
    Mapping,
    MutableSequence,
    Protocol,
    Self,
    Sequence,
    Tuple,
    Type,
    TypeAlias,
    TypeVar,
)


### Exceptions ###
class MapError(Exception):
    pass


class SpriteError(Exception):
    pass


### Enums ###
class NoValueEnum(Enum):
    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.name}>"


class Direction(NoValueEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


# class SpriteType(NoValueEnum):
#     EMPTY = auto()
#     OBSTACLE = auto()
#     GUARD = auto()
#     TRAIL = auto()


### Constants ###
DIRECTION_TURN_LEFT: Final[Mapping[Direction, Direction]] = {
    Direction.UP: Direction.LEFT,
    Direction.DOWN: Direction.RIGHT,
    Direction.LEFT: Direction.DOWN,
    Direction.RIGHT: Direction.UP,
}
DIRECTION_TURN_RIGHT: Final[Mapping[Direction, Direction]] = {
    Direction.UP: Direction.RIGHT,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
    Direction.RIGHT: Direction.DOWN,
}

### Typing ###
T = TypeVar("T")
Coord: TypeAlias = Tuple[int, int]


class Sprite(Protocol):
    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.render()!r})"

    @abstractmethod
    def render(self: Self) -> str: ...

    @abstractmethod
    def has_costume(self: Self, costume: str, /) -> bool: ...

    @classmethod
    @abstractmethod
    def from_costume(cls: Type[Self], costume: str, /) -> Self: ...


class StaticSprite(Sprite):
    COSTUME: ClassVar[str] = NotImplemented

    @classmethod
    def render(cls: Type[Self], /) -> str:
        return cls.COSTUME

    @classmethod
    def has_costume(cls: Type[Self], costume: str, /) -> bool:
        return cls.COSTUME == costume

    @classmethod
    def from_costume(cls: Type[Self], costume: str, /) -> Self:
        assert cls.has_costume(costume)

        return cls()


class Empty(StaticSprite):
    COSTUME = "."


class Obstacle(StaticSprite):
    COSTUME = "#"


class Trail(StaticSprite):
    COSTUME = "X"


class Guard(Sprite):
    COSTUMES: ClassVar[Mapping[Direction, str]] = {
        Direction.UP: "^",
        Direction.DOWN: "v",
        Direction.LEFT: "<",
        Direction.RIGHT: ">",
    }

    _direction: Direction

    def __init__(self: Self, /, direction: Direction = Direction.UP) -> None:
        self._direction = direction

    def render(self: Self, /) -> str:
        return Guard.COSTUMES[self._direction]

    @classmethod
    def has_costume(cls: Type[Self], costume: str, /) -> bool:
        return costume in cls.COSTUMES.values()

    @classmethod
    def from_costume(cls: Type[Self], costume: str, /) -> Self:
        direction: Direction = cls._get_direction(costume)

        return cls(direction)

    def point(self, direction: Direction, /) -> None:
        self._direction = direction

    def turn_left(self: Self, /) -> None:
        new_direction: Direction = DIRECTION_TURN_LEFT[self.direction]

        self.point(new_direction)

    def turn_right(self: Self, /) -> None:
        new_direction: Direction = DIRECTION_TURN_RIGHT[self.direction]

        self.point(new_direction)

    @classmethod
    def _get_direction(cls: Type[Self], costume: str, /) -> Direction:
        costume_to_direction: Mapping[str, Direction] = {
            costume: direction for direction, costume in cls.COSTUMES.items()
        }

        return costume_to_direction[costume]

    @property
    def direction(self: Self, /) -> Direction:
        return self._direction


class Grid(Generic[T]):
    _grid: MutableSequence[MutableSequence[T]]

    def __init__(self: Self, grid: Sequence[Sequence[T]], /) -> None:
        self._grid = [[value for value in row] for row in grid]

        # todo: enforce grid is a rectangle

    def __repr__(self: Self, /) -> str:
        return f"{type(self).__name__}({self.size_x}x{self.size_y})"

    def __iter__(self: Self, /) -> Iterable[Tuple[Coord, T]]:
        y: int
        for y in range(self.size_y):
            x: int
            for x in range(self.size_x):
                value: T = self.get(x, y)

                yield ((x, y), value)

    @classmethod
    def of_size(cls: Type[Self], /, size_x: int, size_y: int, value: T) -> Self:
        row: Sequence[T] = (value,) * size_x
        grid: Sequence[Sequence[T]] = (row,) * size_y

        return cls(grid)

    @cached_property
    def size_x(self: Self, /) -> int:
        if not self._grid:
            return 0

        return len(self._grid[0])

    @cached_property
    def size_y(self: Self, /) -> int:
        return len(self._grid)

    @cached_property
    def size(self: Self, /) -> Tuple[int, int]:
        return (self.size_x, self.size_y)

    @property
    def rows(self: Self, /) -> Sequence[Sequence[T]]:
        return self._grid

    @property
    def columns(self: Self, /) -> Sequence[Sequence[T]]:
        return tuple(self.get_column(x) for x in range(self.size_x))

    def get(self: Self, /, x: int, y: int) -> T:
        return self._grid[y][x]

    def set(self: Self, /, x: int, y: int, value: T) -> None:
        self._grid[y][x] = value

    def get_row(self: Self, y: int, /) -> Sequence[T]:
        return self._grid[y]

    def get_column(self: Self, x: int, /) -> Sequence[T]:
        return tuple(row[x] for row in self._grid)


# @dataclass
# class Map:
#     grid: MutableGrid[Sprite]

#     def __init__(self, grid: Grid[Sprite]) -> None:
#         self.grid = [[sprite for sprite in row] for row in grid]

#     def render(self) -> str:
#         map_string: str = ""

#         index: int
#         row: Sequence[Sprite]
#         for index, row in enumerate(self.grid):
#             if index > 0:
#                 map_string += "\n"

#             sprite: Sprite
#             for sprite in row:
#                 map_string += sprite.render()

#         return map_string

#     def get(self, x: int, y: int, /) -> Sprite:
#         return self.grid[y][x]


# Sprites
EMPTY: Empty = Empty()
OBSTACLE: Obstacle = Obstacle()
GUARD: Guard = Guard()
TRAIL: Trail = Trail()

# STATIC_SPRITES: Mapping[str, Sprite] = {
#     EMPTY.costume: EMPTY,
#     OBSTACLE.costume: OBSTACLE,
#     TRAIL.costume: TRAIL,
# }

STATIC_SPRITES: Collection[Sprite] = (EMPTY, OBSTACLE, TRAIL)

# SPRITES: Mapping[SpriteType, Sprite] = {
#     SpriteType.EMPTY: EMPTY,
#     SpriteType.OBSTACLE: OBSTACLE,
#     SpriteType.GUARD: Guard(),
#     SpriteType.TRAIL: TRAIL,
# }

EXAMPLE: Final[str] = (
    """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()
)

# Map: TypeAlias = Sequence[Sequence[Sprite]]
# MutableMap: TypeAlias = MutableSequence[MutableSequence[Sprite]]

# EMPTY_MAP: Final[Map] = ()
# EMPTY_GRID: Final[Grid[Sprite]] = ()
# EMPTY_MAP: Final[Map] =

# def build_sprite(sprite_type: SpriteType, sprite_costume: )


def get_sprite(costume: str, /) -> Sprite:
    sprite: Sprite
    for sprite in STATIC_SPRITES:
        if sprite.has_costume(costume):
            return sprite

    if costume in Guard.COSTUMES.values():
        return Guard.from_costume(costume)

    raise SpriteError(f"No sprite has costume '{costume}'")


# def parse_grid(raw_grid: str, /) -> Grid[Sprite]:
#     raw_rows: Sequence[str] = raw_grid.splitlines()

#     if not raw_rows:
#         raise NotImplementedError  # TODO
#         # return EMPTY_MAP

#     # size_y: int = len(raw_rows)
#     # size_x: int = max(len(line) for line in lines)
#     # size_x: int = len(raw_rows[0])

#     grid: MutableGrid[Sprite] = []

#     raw_row: str
#     for raw_row in raw_rows:
#         # row_len: int = len(raw_row)

#         # The map is always a square, but let's be safe anyway!
#         # if row_len != size_x:
#         #     raise MapError(
#         #         f"Map is not a rectangle. Row has length {row_len}, expected {size_x}"
#         #     )

#         row: MutableSequence[Sprite] = [
#             get_sprite(raw_sprite) for raw_sprite in raw_row
#         ]

#         grid.append(row)

#     return grid


def parse_grid(raw_grid: str, /) -> Grid[str]:
    return Grid(raw_grid.splitlines())


# print(EXAMPLE)
# grid: Grid[Sprite] = parse_grid(EXAMPLE)
# map_: Map = Map(grid)

# map_: Map = read_map(EXAMPLE)
# map_: Map = Map(
#     (
#         (EMPTY, OBSTACLE, EMPTY, Guard(), EMPTY),
#         (EMPTY, OBSTACLE, OBSTACLE, EMPTY, OBSTACLE),
#     )
# )

# print(map_.render())

# g: Guard = Guard()

# g: Grid[Sprite] = Grid.of_size(10, 10, EMPTY)
# g: Grid[Sprite] = Grid(
#     (
#         (EMPTY, EMPTY, EMPTY),
#         (EMPTY, OBSTACLE, EMPTY),
#         (EMPTY, EMPTY, EMPTY),
#     )
# )
# g: Grid[str] = Grid(
#     (
#         ("A", "B", "C"),
#         ("D", "E", "F"),
#         ("G", "H", "I"),
#     )
# )

g: Grid[str] = parse_grid(EXAMPLE)

# Temp sprites
e: Empty = Empty()
o: Obstacle = Obstacle()
t: Trail = Trail()
