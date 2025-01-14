"""Day 6: Guard Gallivant"""

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from functools import cached_property
from typing import (
    ClassVar,
    Final,
    Generic,
    Iterable,
    Mapping,
    MutableSequence,
    NamedTuple,
    Protocol,
    Self,
    Sequence,
    Tuple,
    Type,
    TypeAlias,
    TypeVar,
)

### Typing ###
T = TypeVar("T")
Coord: TypeAlias = Tuple[int, int]


class Coordinate(NamedTuple):
    x: int
    y: int


### Exceptions ###
# class MapError(Exception):
#     pass


class SpriteError(Exception):
    pass


### Enums ###
# class NoValueEnum(Enum):
#     def __repr__(self) -> str:
#         return f"<{type(self).__name__}.{self.name}>"


class _CyclicalEnum(Enum):
    """Enum with sequential, cyclical members"""

    @classmethod
    def first(cls: Type[Self], /) -> Self:
        """Get the first member of this enum"""

        return next(iter(cls))

    @classmethod
    def last(cls: Type[Self], /) -> Self:
        """Get the last member of this enum"""

        return next(reversed(cls))

    @property
    def _index(self: Self, /) -> int:
        cls: Type[Self] = type(self)
        members: Sequence[Self] = tuple(cls)

        return members.index(self)

    @classmethod
    def _members(cls: Type[Self], /) -> Sequence[Self]:
        return tuple(cls)

    def prev(self: Self, /) -> Self:
        """Get the previous member of this enum"""

        index: int = (self._index - 1) % len(self._members())

        return self._members()[index]

    def next(self: Self, /) -> Self:
        """Get the next member of this enum"""

        index: int = (self._index + 1) % len(self._members())

        return self._members()[index]


class Direction(_CyclicalEnum):
    UP: Coordinate = Coordinate(0, 1)
    LEFT: Coordinate = Coordinate(-1, 0)
    DOWN: Coordinate = Coordinate(0, -1)
    RIGHT: Coordinate = Coordinate(1, 0)

    def left(self: Self, /) -> Self:
        return self.next()

    def right(self: Self, /) -> Self:
        return self.prev()


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


class Obstruction(StaticSprite):
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

        # TODO: Enforce grid is a rectangle?

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


def move_in_direction(
    grid: Grid, coord: Coord, direction: Direction, amount: int = 1
) -> Coord:
    size_x: int
    size_y: int
    size_x, size_y = grid.size

    x: int
    y: int
    x, y = coord

    translation_x: int
    translation_y: int
    translation_x, translation_y = direction.value

    x += translation_x * amount
    y += translation_y * amount

    if x < 0 or x >= size_x or y < 0 or y >= size_y:
        raise Exception  # TODO

    return (x, y)


@dataclass
class Map:
    grid: Grid[Sprite]

    # _guard_position

    def render(self) -> str:
        map_string: str = ""

        index: int
        row: Sequence[Sprite]
        for index, row in enumerate(self.grid.rows):
            if index > 0:
                map_string += "\n"

            sprite: Sprite
            for sprite in row:
                map_string += sprite.render()

        return map_string

    def print(self) -> None:
        print(self.render())

    # @cached_property
    @property
    def guard(self: Self, /) -> Tuple[Coord, Guard]:
        coord: Coord
        sprite: Sprite
        for coord, sprite in self.grid:  # FIXME
            if isinstance(sprite, Guard):
                return (coord, sprite)

        raise Exception  # TODO

    def move_guard(self: Self, /) -> Coord:
        position: Coord
        guard: Guard
        position, guard = self.guard

        direction: Direction = guard.direction

        new_position: Coord = move_in_direction(
            grid=self.grid, coord=position, direction=direction
        )

        sprite: Sprite = self.grid.get(new_position.x, new_position.y)

        return (-1, -1)  # TEMP


# Sprites
EMPTY: Final[Empty] = Empty()
OBSTACLE: Final[Obstruction] = Obstruction()
TRAIL: Final[Trail] = Trail()

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


def get_sprite(costume: str, /) -> Sprite:
    sprite: Sprite
    for sprite in (EMPTY, OBSTACLE, TRAIL):
        if sprite.has_costume(costume):
            return sprite

    if costume in Guard.COSTUMES.values():
        return Guard.from_costume(costume)

    raise SpriteError(f"No sprite has costume '{costume}'")


def parse_grid(raw_grid: str, /) -> Grid[Sprite]:
    raw_rows: Sequence[str] = raw_grid.splitlines()

    grid: MutableSequence[MutableSequence[Sprite]] = []

    raw_row: str
    for raw_row in raw_rows:
        row: MutableSequence[Sprite] = [
            get_sprite(raw_sprite) for raw_sprite in raw_row
        ]

        grid.append(row)

    return Grid(grid)


g: Grid[Sprite] = parse_grid(EXAMPLE)
m: Map = Map(g)

# guard: Guard = g.get(4, 6)
# guard: Guard = m.guard
# assert guard is not None
