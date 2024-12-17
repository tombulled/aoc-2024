"""Day 6: Guard Gallivant"""

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import (
    ClassVar,
    Collection,
    Final,
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


# Exceptions
class MapError(Exception):
    pass


class SpriteError(Exception):
    pass


class NoValueEnum(Enum):
    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.name}>"

class Direction(NoValueEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class SpriteType(NoValueEnum):
    EMPTY = auto()
    OBSTACLE = auto()
    GUARD = auto()
    TRAIL = auto()


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


@dataclass
class StaticSprite(Sprite):
    costume: str

    def render(self: Self) -> str:
        return self.costume

    def has_costume(self: Self, costume: str, /) -> bool:
        return self.costume == costume

    @classmethod
    def from_costume(cls: Type[Self], costume: str, /) -> Self:
        return cls(costume)


@dataclass
class Guard(Sprite):
    COSTUMES: ClassVar[Mapping[Direction, str]] = {
        Direction.UP: "^",
        Direction.DOWN: "v",
        Direction.LEFT: "<",
        Direction.RIGHT: ">",
    }

    direction: Direction = Direction.UP

    def render(self) -> str:
        return Guard.COSTUMES[self.direction]

    @classmethod
    def has_costume(cls: Type[Self], costume: str, /) -> bool:
        return costume in cls.COSTUMES.values()

    @classmethod
    def from_costume(cls: Type[Self], costume: str, /) -> Self:
        direction: Direction = cls._get_direction(costume)

        return cls(direction)

    def turn(self, direction: Direction, /) -> None:
        self.direction = direction

    @classmethod
    def _get_direction(cls: Type[Self], costume: str, /) -> Direction:
        costume_to_direction: Mapping[str, Direction] = {
            costume: direction for direction, costume in cls.COSTUMES.items()
        }

        return costume_to_direction[costume]


T = TypeVar("T")

Coord: TypeAlias = Tuple[int, int]
Grid: TypeAlias = Sequence[Sequence[T]]
MutableGrid: TypeAlias = MutableSequence[MutableSequence[T]]


# @dataclass
class Map:
    grid: MutableGrid[Sprite]

    def __init__(self, grid: Grid[Sprite]) -> None:
        self.grid = [[sprite for sprite in row] for row in grid]

    def render(self) -> str:
        map_string: str = ""

        index: int
        row: Sequence[Sprite]
        for index, row in enumerate(self.grid):
            if index > 0:
                map_string += "\n"

            sprite: Sprite
            for sprite in row:
                map_string += sprite.render()

        return map_string
    
    def get(self, x: int, y: int, /) -> Sprite:
        return self.grid[y][x]


# Sprites
EMPTY: StaticSprite = StaticSprite(".")
OBSTACLE: StaticSprite = StaticSprite("#")
# GUARD: Guard = Guard()
TRAIL: StaticSprite = StaticSprite("X")

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


# class MapObject(str, Enum):
#     EMPTY: str = "."
#     OBSTACLE: str = "#"
#     GUARD: str = "^"
#     TRAIL: str = "X"


# OBJ_OBSTACLE: Final[str] = "#"

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

    raise SpriteError(f"Uknown sprite '{costume}'")


def parse_grid(raw_grid: str, /) -> Grid[Sprite]:
    raw_rows: Sequence[str] = raw_grid.splitlines()

    if not raw_rows:
        raise NotImplementedError # TODO
        # return EMPTY_MAP

    # size_y: int = len(raw_rows)
    # size_x: int = max(len(line) for line in lines)
    # size_x: int = len(raw_rows[0])

    grid: MutableGrid[Sprite] = []

    raw_row: str
    for raw_row in raw_rows:
        # row_len: int = len(raw_row)

        # The map is always a square, but let's be safe anyway!
        # if row_len != size_x:
        #     raise MapError(
        #         f"Map is not a rectangle. Row has length {row_len}, expected {size_x}"
        #     )

        row: MutableSequence[Sprite] = [
            get_sprite(raw_sprite) for raw_sprite in raw_row
        ]

        grid.append(row)

    return grid


# print(EXAMPLE)
grid: Grid[Sprite] = parse_grid(EXAMPLE)
map_: Map = Map(grid)

# map_: Map = read_map(EXAMPLE)
# map_: Map = Map(
#     (
#         (EMPTY, OBSTACLE, EMPTY, Guard(), EMPTY),
#         (EMPTY, OBSTACLE, OBSTACLE, EMPTY, OBSTACLE),
#     )
# )

print(map_.render())