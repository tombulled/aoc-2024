"""Day 9: Disk Fragmenter"""

from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Final, Iterable, Self, Type

EXAMPLE_INPUT: Final[str] = "2333133121414131402"

FREE: Final[str] = "."


class _ChainedEnum(IntEnum):
    @classmethod
    def first(cls: Type[Self], /) -> Self:
        return cls(1)

    def next(self: Self, /) -> Self:
        cls: Type[Self] = type(self)
        next_value: int = self.value % len(cls) + 1

        return cls(next_value)


class DiskMapEntryType(_ChainedEnum):
    FILE_SIZE = auto()
    FREE_SPACE = auto()


@dataclass
class DiskMapEntry:
    type: DiskMapEntryType
    value: int


def read_dataset() -> str:
    with open("input", encoding="utf-8") as file:
        return file.read()


def parse_disk_map(disk_map: str, /) -> Iterable[DiskMapEntry]:
    entry_type: DiskMapEntryType = DiskMapEntryType.first()

    character: str
    for character in disk_map:
        value: int = int(character)

        yield DiskMapEntry(entry_type, value)

        entry_type = entry_type.next()


# dataset: str = read_dataset()
dataset: str = EXAMPLE_INPUT
disk_map_entries: Iterable[DiskMapEntry] = parse_disk_map(dataset)

for entry in disk_map_entries:
    print(entry)
