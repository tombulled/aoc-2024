"""Day 9: Disk Fragmenter"""

from abc import ABC, abstractmethod
import dataclasses
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import (
    Iterable,
    MutableSequence,
    MutableSet,
    Self,
    Sequence,
    Type,
    TypeAlias,
)

# Typing
Disk: TypeAlias = Sequence["Node"]
MutableDisk: TypeAlias = MutableSequence["Node"]


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


@dataclass
class Node(ABC):
    size: int

    def is_empty(self) -> bool:
        return self.size == 0

    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


class Space(Node):
    # pass
    def render(self) -> str:
        return "." * self.size


@dataclass
class File(Node):
    id: int

    def render(self) -> str:
        return str(self.id) * self.size


def read_dataset() -> str:
    with open("input", encoding="utf-8") as file:
        return file.read().strip()


def parse_disk_map(disk_map: str, /) -> Iterable[Node]:
    entry_type: DiskMapEntryType = DiskMapEntryType.first()
    file_id: int = 0

    character: str
    for character in disk_map:
        value: int = int(character)

        match entry_type:
            case DiskMapEntryType.FILE:
                yield File(size=value, id=file_id)
                file_id += 1
            case DiskMapEntryType.SPACE:
                yield Space(size=value)

        entry_type = entry_type.next()


def get_disk_size(disk: Disk, /) -> int:
    return sum(node.size for node in disk)


def clone_disk(disk: Disk, /) -> MutableDisk:
    return [dataclasses.replace(node) for node in disk]


def compact_disk_old(
    disk: MutableDisk, /, *, fragment: bool = True, attempt_once: bool = False
) -> MutableDisk:
    disk_size: int = get_disk_size(disk)
    considered_file_ids: MutableSet[int] = set()

    new_disk: MutableDisk = []

    block: Node
    for block in disk:
        if not isinstance(block, Space) or block.size == 0:
            if block.size > 0:
                new_disk.append(block)

            continue

        free_space: Space = block

        candidate_block: Node
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
            block_fragment: Node = dataclasses.replace(
                file, size=fragment_size
            )

            new_disk.append(block_fragment)

            free_space.size -= fragment_size
            file.size -= fragment_size

    free_space_padding: int = disk_size - get_disk_size(new_disk)

    if free_space_padding > 0:
        new_disk.append(Space(free_space_padding))

    return new_disk


def compact_disk(disk: MutableDisk, /, *, fragment: bool = True) -> None:
    space_padding: int = 0

    files: Sequence[File] = tuple(
        node
        for node in disk
        if isinstance(node, File) and not node.is_empty()
    )

    # node: Node
    # for node in reversed(disk):
    #     # This block isn't a file, or it's an empty file, so we don't need to try and move it.
    #     if not isinstance(node, File) or node.is_empty():
    #         continue

    #     file: File = node

    file: File
    for file in reversed(files):
        node2_index: int
        node2: Node
        for node2_index, node2 in enumerate(disk):
            # Don't go past ourselves!
            if node2 is file:
                break

            # We've already moved the whole file!
            if file.is_empty():
                break

            # Only consider non-empty free space as possible locations
            # to move our file.
            if not isinstance(node2, Space) or node2.is_empty():
                continue

            space_index: int = node2_index
            space: Space = node2

            # If we can't fragment the file and the free space doesn't
            # contain enough space to fit the file as-is, we can't
            # move it here, so skip this location.
            if not fragment and file.size > space.size:
                continue

            fragment_size: int = min(space.size, file.size)
            fragment_node: File = dataclasses.replace(file, size=fragment_size)

            disk.insert(space_index, fragment_node)

            space.size -= fragment_size
            file.size -= fragment_size
            space_padding += fragment_size

            if space.is_empty():
                disk.remove(space)

        if file.is_empty():
            disk.remove(file)

    # Right-pad the disk with free space
    if space_padding > 0:
        last_node: Node = disk[-1]

        if isinstance(last_node, Space):
            last_node.size += space_padding
        else:
            disk.append(Space(space_padding))


def calculate_filesystem_checksum(disk: Disk, /) -> int:
    position: int = 0
    checksum: int = 0

    node: Node
    for node in disk:
        if not isinstance(node, File):
            continue

        node_checksum: int = sum(
            (position + bit_index) * node.id for bit_index in range(node.size)
        )

        position += node.size
        checksum += node_checksum

    return checksum


def render_disk(disk: Disk, /) -> str:
    return "".join(node.render() for node in disk)


def print_disk(disk: Disk, /) -> None:
    print(render_disk(disk))


# dataset: str = "2333133121414131402"
dataset: str = read_dataset()
disk: MutableDisk = list(parse_disk_map(dataset))
# disk2: MutableDisk = clone_disk(disk)  # TEMP!!!

# print_disk(disk)

# --- Part One ---

# disk_part_1: MutableDisk = compact_disk(disk)
import time
t0 = time.time()
compact_disk(disk)
print("Took:", time.time()-t0)

# print_disk(disk_part_1)
# print_disk(disk)

# checksum_part_1: int = calculate_filesystem_checksum(disk_part_1)
checksum_part_1: int = calculate_filesystem_checksum(disk)
assert checksum_part_1 == 6435922584968
# assert checksum_part_1 == 1928

# --- Part Two ---

# print()
# disk_part_2: MutableDisk = compact_disk(disk2, fragment=False)

# print_disk(disk_part_2)

# checksum_part_2: int = calculate_filesystem_checksum(disk_part_2)
# assert checksum_part_2 == 6435922584968
