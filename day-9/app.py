"""Day 9: Disk Fragmenter"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import dataclasses
from enum import IntEnum, auto
from typing import Final, Iterable, MutableSequence, Self, Sequence, Type, TypeAlias

# Typing
Disk: TypeAlias = Sequence["Block"]
MutableDisk: TypeAlias = MutableSequence["Block"]

EXAMPLE_INPUT: Final[str] = "2333133121414131402"


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
    FILE_SIZE = auto()
    FREE_SPACE = auto()


@dataclass
class Block(ABC):
    size: int

    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


class FreeSpace(Block):
    # pass
    def render(self) -> str:
        return "." * self.size


@dataclass
class File(Block):
    id: int

    def render(self) -> str:
        return str(self.id) * self.size


def read_dataset() -> str:
    with open("input", encoding="utf-8") as file:
        return file.read()


def parse_disk_map(disk_map: str, /) -> Iterable[Block]:
    entry_type: DiskMapEntryType = DiskMapEntryType.first()
    file_id: int = 0

    character: str
    for character in disk_map:
        value: int = int(character)

        match entry_type:
            case DiskMapEntryType.FILE_SIZE:
                yield File(size=value, id=file_id)
                file_id += 1
            case DiskMapEntryType.FREE_SPACE:
                yield FreeSpace(size=value)

        entry_type = entry_type.next()


def get_disk_size(disk: Disk, /) -> int:
    return sum(block.size for block in disk)


def compact_disk(disk: MutableDisk, /) -> MutableDisk:
    new_disk: MutableDisk = []

    disk_size_before: int = get_disk_size(disk)

    block: Block
    for block in disk:
        if not isinstance(block, FreeSpace) or block.size == 0:
            if block.size > 0:
                new_disk.append(block)

            print("Adding block as-is:", block)

            continue

        free_space: FreeSpace = block

        print("Found free space, will find files to fill it:", free_space)

        candidate_block: Block
        for candidate_block in reversed(disk):
            if free_space.size == 0:
                print("Free space has been filled, will stop there")
                break
            if candidate_block is block:
                break
            if isinstance(candidate_block, FreeSpace) or candidate_block.size == 0:
                print("Candidate is free space or empty, skipping:", candidate_block)
                continue

            print("Found suitable candidate block:", candidate_block)

            chunk_size: int = min(free_space.size, candidate_block.size)
            block_chunk: Block = dataclasses.replace(candidate_block, size=chunk_size)

            print("Will fill free space with chunk:", block_chunk)

            new_disk.append(block_chunk)
            free_space.size -= chunk_size
            candidate_block.size -= chunk_size

        print("New disk currently:", render_disk(new_disk))
        print("Old disk currently:", render_disk(disk))
        print()

        # if free_space.size > 0:
        #     new_disk.append(free_space)

    disk_size_after: int = get_disk_size(new_disk)
    free_space_padding: int = disk_size_before - disk_size_after

    print("Before:", disk_size_before)
    print("After:", disk_size_after)
    print("Padding:", free_space_padding)

    if free_space_padding > 0:
        new_disk.append(FreeSpace(free_space_padding))

    return new_disk


# def calculate_filesystem_checksum(disk: Disk, /) -> int:
#     position: int = 0

#     index: int
#     for index, block in enumerate(disk):
#         print(position, index, block)

#         # block_checksum: int =

#     return 0  # TEMP


def render_disk(disk: Disk, /) -> str:
    return "".join(block.render() for block in disk)


def print_disk(disk: Disk, /) -> None:
    print(render_disk(disk))


# dataset: str = read_dataset()
dataset: str = EXAMPLE_INPUT
disk: MutableDisk = list(parse_disk_map(dataset))

disk_render_expected: str = "00...111...2...333.44.5555.6666.777.888899"
disk_render_actual: str = render_disk(disk)
print("Expected:", disk_render_expected)
print("Actual:  ", disk_render_actual)
print("Correct: ", disk_render_actual == disk_render_expected)

compacted_disk: MutableDisk = compact_disk(disk)

compacted_disk_render_expected: str = "0099811188827773336446555566.............."
compacted_disk_render_actual: str = render_disk(compacted_disk)
print("Expected:", compacted_disk_render_expected)
print("Actual:  ", compacted_disk_render_actual)
print("Correct: ", compacted_disk_render_actual == compacted_disk_render_expected)

# print(calculate_filesystem_checksum(compacted_disk))
