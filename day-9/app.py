"""Day 9: Disk Fragmenter"""

import dataclasses
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Iterable, MutableSequence, Self, Sequence, Type, TypeAlias

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
        return file.read().strip()


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
    disk_size: int = get_disk_size(disk)

    new_disk: MutableDisk = []

    block: Block
    for block in disk:
        if not isinstance(block, FreeSpace) or block.size == 0:
            if block.size > 0:
                new_disk.append(block)

            continue

        free_space: FreeSpace = block

        candidate_block: Block
        for candidate_block in reversed(disk):
            if free_space.size == 0 or candidate_block is block:
                break
            if isinstance(candidate_block, FreeSpace) or candidate_block.size == 0:
                continue

            chunk_size: int = min(free_space.size, candidate_block.size)
            block_chunk: Block = dataclasses.replace(candidate_block, size=chunk_size)

            new_disk.append(block_chunk)
            free_space.size -= chunk_size
            candidate_block.size -= chunk_size

    free_space_padding: int = disk_size - get_disk_size(new_disk)

    if free_space_padding > 0:
        new_disk.append(FreeSpace(free_space_padding))

    return new_disk


def calculate_filesystem_checksum(disk: Disk, /) -> int:
    position: int = 0
    checksum: int = 0

    block: Block
    for block in disk:
        if not isinstance(block, File):
            continue

        block_checksum: int = sum(
            (position + bit_index) * block.id for bit_index in range(block.size)
        )

        position += block.size
        checksum += block_checksum

    return checksum


dataset: str = read_dataset()

disk: MutableDisk = list(parse_disk_map(dataset))
compacted_disk: MutableDisk = compact_disk(disk)

part_1: int = calculate_filesystem_checksum(compacted_disk)
assert part_1 == 6435922584968
