"""Day 9: Disk Fragmenter"""

from abc import ABC, abstractmethod
import dataclasses
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Iterable, MutableSequence, MutableSet, Self, Sequence, Type, TypeAlias

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


def compact_disk(
    disk: MutableDisk, /, *, fragment: bool = True, attempt_once: bool = False
) -> MutableDisk:
    disk_size: int = get_disk_size(disk)
    considered_file_ids: MutableSet[int] = set()

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
            if not isinstance(candidate_block, File) or candidate_block.size == 0:
                continue

            file: File = candidate_block

            if attempt_once and file.id in considered_file_ids:
                continue

            considered_file_ids.add(file.id)

            if not fragment and file.size > free_space.size:
                continue

            fragment_size: int = min(free_space.size, file.size)
            block_fragment: Block = dataclasses.replace(
                file, size=fragment_size
            )

            new_disk.append(block_fragment)

            free_space.size -= fragment_size
            file.size -= fragment_size

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


def print_disk(disk: Disk, /) -> None:
    print("".join(block.render() for block in disk))


dataset: str = "2333133121414131402"
# dataset: str = read_dataset()
disk: MutableDisk = list(parse_disk_map(dataset))
disk2: MutableDisk = [dataclasses.replace(block) for block in disk]  # TEMP!!!

print_disk(disk)

# --- Part One ---

disk_part_1: MutableDisk = compact_disk(disk)

print_disk(disk_part_1)

checksum_part_1: int = calculate_filesystem_checksum(disk_part_1)
# assert checksum_part_1 == 6435922584968

# --- Part Two ---

print()
disk_part_2: MutableDisk = compact_disk(disk2, fragment=False)

print_disk(disk_part_2)

checksum_part_2: int = calculate_filesystem_checksum(disk_part_2)
# assert checksum_part_2 == 6435922584968
