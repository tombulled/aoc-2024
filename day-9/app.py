"""Day 9: Disk Fragmenter"""

from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Final, Iterable, Self, Type

EXAMPLE_INPUT: Final[str] = "2333133121414131402"

FREE: Final[str] = "."  # WARN: NOT USED??


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
class Block:
    size: int


class FreeSpace(Block):
    pass


@dataclass
class File(Block):
    id: int


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


# dataset: str = read_dataset()
dataset: str = EXAMPLE_INPUT
blocks: Iterable[Block] = parse_disk_map(dataset)

for block in blocks:
    print(block)
