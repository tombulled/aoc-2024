"""Day 9: Disk Fragmenter"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from typing import (
    Callable,
    Final,
    Generic,
    Iterable,
    MutableSequence,
    Optional,
    Self,
    Sequence,
    Type,
    TypeAlias,
    TypeVar,
)

# Typing
Disk: TypeAlias = Sequence["Block"]
MutableDisk: TypeAlias = MutableSequence["Block"]


class _CyclicalEnum(IntEnum):
    @classmethod
    def first(cls: Type[Self], /) -> Self:
        return cls(1)

    @classmethod
    def last(cls: Type[Self], /) -> Self:
        return cls(len(cls))

    def next(self: Self, /) -> Self:
        cls: Type[Self] = type(self)
        next_value: int = self.value % len(cls) + 1

        return cls(next_value)


class DiskMapEntryType(_CyclicalEnum):
    FILE = auto()
    SPACE = auto()


class Direction(Enum):
    LTR = auto()
    RTL = auto()


@dataclass
class Block(ABC):
    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


class Space(Block):
    # pass
    @staticmethod
    def render() -> str:
        return "."


@dataclass
class File(Block):
    id: int

    def render(self) -> str:
        return str(self.id)


SPACE: Final[Block] = Space()

B = TypeVar("B", bound=Block)


@dataclass
class Fragment(Generic[B]):
    index: int
    block: B
    size: int

    def render(self) -> str:
        return self.block.render() * self.size


def read_dataset() -> str:
    with open("input", encoding="utf-8") as file:
        return file.read().strip()


def parse_disk_map(disk_map: str, /) -> MutableDisk:
    entry_type: DiskMapEntryType = DiskMapEntryType.first()
    file_id: int = 0

    disk: MutableDisk = []

    raw_size: str
    for raw_size in disk_map:
        size: int = int(raw_size)

        block: Block

        match entry_type:
            case DiskMapEntryType.FILE:
                block = File(file_id)
                file_id += 1
            case DiskMapEntryType.SPACE:
                block = SPACE

        for _ in range(size):
            disk.append(block)

        entry_type = entry_type.next()

    return disk


def iter_fragments(
    disk: Disk,
    /,
    *,
    direction: Direction = Direction.LTR,
    predicate: Optional[Callable[[Block], bool]] = None,
    index_start: int = 0,
    index_end: Optional[int] = None,
) -> Iterable[Fragment[Block]]:
    if index_end is None:
        index_end = len(disk)

    block_indices: Iterable[int]

    match direction:
        case direction.LTR:
            block_indices = range(index_start, index_end)
        case direction.RTL:
            block_indices = range(index_end - 1, -1 + index_start, -1)

    fragment: Optional[Fragment[Block]] = None

    block_index: int
    for block_index in block_indices:
        block: Block = disk[block_index]

        # If there's an existing fragment
        if fragment is not None:
            # If this block is a part of the fragment, update
            # the fragment metadata
            if fragment.block is block:
                fragment.index = min(fragment.index, block_index)
                fragment.size += 1
            # Otherwise, yield what we have as the fragment is finished
            else:
                yield fragment
                fragment = None

        if predicate is not None and not predicate(block):
            fragment = None
        elif fragment is None:
            fragment = Fragment(index=block_index, block=block, size=1)

    if fragment is not None:
        yield fragment


def compact_disk(disk: MutableDisk, /, *, fragment: bool = True) -> None:
    file_fragments: Iterable[Fragment[Block]] = iter_fragments(
        disk,
        direction=Direction.RTL,
        predicate=lambda block: isinstance(block, File),
    )

    search_space_start: int = 0

    file_fragment: Fragment[Block]
    for file_fragment in file_fragments:
        assert isinstance(file_fragment.block, File)

        # file_index: int = file_fragment.index
        # file_size: int = file_fragment.size
        file: File = file_fragment.block

        search_space_end: int = file_fragment.index

        space_fragments: Iterable[Fragment[Block]] = iter_fragments(
            disk,
            direction=Direction.LTR,
            predicate=lambda block: isinstance(block, Space),
            index_start=search_space_start,
            index_end=search_space_end,
        )

        space_fragment_index: int
        space_fragment: Fragment[Block]
        for space_fragment_index, space_fragment in enumerate(space_fragments):
            if file_fragment.size == 0:
                break

            assert isinstance(space_fragment.block, Space)

            space_index: int = space_fragment.index
            space_size: int = space_fragment.size
            space: Space = space_fragment.block

            if space_fragment_index == 0:
                search_space_start = space_fragment.index

            # If we can't fragment the file and the free space doesn't
            # contain enough space to fit the file as-is, we can't
            # move it here, so skip this location.
            if not fragment and file_fragment.size > space_fragment.size:
                continue

            fragment_size: int = min(space_fragment.size, file_fragment.size)

            disk[space_index : space_index + fragment_size] = [file] * fragment_size
            disk[
                file_fragment.index
                + file_fragment.size
                - fragment_size : file_fragment.index
                + file_fragment.size
            ] = [space] * fragment_size

            file_fragment.size -= fragment_size


def calculate_filesystem_checksum(disk: Disk, /) -> int:
    checksum: int = 0

    block_index: int
    block: Block
    for block_index, block in enumerate(disk):
        if not isinstance(block, File):
            continue

        checksum += block_index * block.id

    return checksum


def render_disk(disk: Disk, /) -> str:
    return "".join(block.render() for block in disk)


def print_disk(disk: Disk, /) -> None:
    print(render_disk(disk))


# dataset: str = "2333133121414131402"
dataset: str = read_dataset()

disk: MutableDisk = parse_disk_map(dataset)

# print_disk(disk)

# print()
# for fragment in iter_fragments(disk, direction=Direction.RTL):
#     print(fragment.render(), fragment)
# print()

# # --- Part One ---

import time

t0 = time.time()
compact_disk(disk)
# print_disk(disk)
print("Took:", time.time() - t0)

checksum_part_1: int = calculate_filesystem_checksum(disk)
assert checksum_part_1 == 6435922584968

# # --- Part Two ---

# # print()
# print_disk(disk_2)
# t0 = time.time()
# compact_disk(disk_2, fragment=False)
# print("Took:", time.time() - t0)

# print_disk(disk_2)

# # 6450047797159 is too low
# checksum_part_2: int = calculate_filesystem_checksum(disk_2)
# # assert checksum_part_2 == ???

# print("Part 2:", checksum_part_2)
