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

# FREE: Final[str] = "."  # WARN: NOT USED??


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

    block: Block
    for block in disk:
        if not isinstance(block, FreeSpace):
            if block.size > 0:
                new_disk.append(block)

            continue

        free_space: FreeSpace = block

        candidate_block: Block
        for candidate_block in reversed(disk):
            if isinstance(candidate_block, FreeSpace) or candidate_block.size == 0:
                continue

            chunk_size: int = min(free_space.size, candidate_block.size)
            block_chunk: Block = dataclasses.replace(candidate_block, size=chunk_size)

            new_disk.append(block_chunk)
            free_space.size -= chunk_size

        if free_space.size > 0:
            new_disk.append(free_space)

    return new_disk

def render_disk(disk: Disk, /) -> str:
    return "".join(block.render() for block in disk)

def print_disk(disk: Disk, /) -> None:
    print(render_disk(disk))

# dataset: str = read_dataset()
dataset: str = EXAMPLE_INPUT
disk: MutableDisk = list(parse_disk_map(dataset))

# for block in blocks:
#     print(block)

compacted_disk: MutableDisk = compact_disk(disk)

print_disk(disk)
print_disk(compacted_disk)