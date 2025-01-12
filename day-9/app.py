"""Day 9: Disk Fragmenter"""

import dataclasses
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import (
    Final,
    Generic,
    Iterable,
    MutableSequence,
    MutableSet,
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


@dataclass
class Block(ABC):
    # size: int

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


# def get_disk_size(disk: Disk, /) -> int:
#     return sum(node.size for node in disk)


# def clone_disk(disk: Disk, /) -> MutableDisk:
#     return [dataclasses.replace(node) for node in disk]


# def compact_disk(disk: MutableDisk, /, *, fragment: bool = True) -> None:
#     space_padding: int = 0

#     files: Sequence[File] = tuple(
#         node for node in disk if isinstance(node, File) and not node.is_empty()
#     )

#     file: File
#     for file in reversed(files):
#         node2_index: int
#         node2: Node
#         for node2_index, node2 in enumerate(disk):
#             # Don't go past ourselves!
#             if node2 is file:
#                 break

#             # We've already moved the whole file!
#             if file.is_empty():
#                 break

#             # Only consider non-empty free space as possible locations
#             # to move our file.
#             if not isinstance(node2, Space) or node2.is_empty():
#                 continue

#             space_index: int = node2_index
#             space: Space = node2

#             # If we can't fragment the file and the free space doesn't
#             # contain enough space to fit the file as-is, we can't
#             # move it here, so skip this location.
#             if not fragment and file.size > space.size:
#                 continue

#             fragment_size: int = min(space.size, file.size)
#             fragment_node: File = dataclasses.replace(file, size=fragment_size)

#             disk.insert(space_index, fragment_node)

#             space.size -= fragment_size
#             file.size -= fragment_size
#             space_padding += fragment_size

#             if space.is_empty():
#                 disk.remove(space)

#         if file.is_empty():
#             disk.remove(file)

#     # Right-pad the disk with free space
#     if space_padding > 0:
#         last_node: Node = disk[-1]

#         if isinstance(last_node, Space):
#             last_node.size += space_padding
#         else:
#             disk.append(Space(space_padding))


def iter_fragments(disk: Disk, /) -> Iterable[Fragment[File]]:
    fragment: Optional[Fragment] = None

    block_index: int
    for block_index in range(len(disk) - 1, -1, -1):
        block: Block = disk[block_index]

        # If there's an existing fragment
        if fragment is not None:
            # If this block is a part of the fragment, update
            # the fragment metadata
            if fragment.block is block:
                fragment.index = block_index
                fragment.size += 1
            # Otherwise, yield what we have as the fragment is finished
            else:
                yield fragment
                fragment = None
        
        if not isinstance(block, File):
            fragment = None
        elif fragment is None:
            fragment = Fragment(index=block_index, block=block, size=1)

    if fragment is not None:
        yield fragment


def compact_disk(disk: MutableDisk, /, *, fragment: bool = True) -> None:
    search_space_start: int = 0
    # search_space_stop: int = 0

    block_index: int
    for block_index in range(len(disk) - 1, -1, -1):
        block: Block = disk[block_index]

        if not isinstance(block, File):
            continue

        file_index: int = block_index
        file: File = block

        print(block_index, block)

        # seen_space: bool = False

        # block2_index: int
        # for block2_index in range(search_space_start, block_index):
        #     block2: Block = disk[block2_index]

        #     if not isinstance(block2, Space):
        #         continue

        #     if not seen_space:
        #         search_space_start = block2_index

        #     seen_space = True

        #     space_index: int = block2_index
        #     space: Space = block2


# def calculate_filesystem_checksum(disk: Disk, /) -> int:
#     position: int = 0
#     checksum: int = 0

#     node: Node
#     for node in disk:
#         if not isinstance(node, File):
#             continue

#         node_checksum: int = sum(
#             (position + bit_index) * node.id for bit_index in range(node.size)
#         )

#         position += node.size
#         checksum += node_checksum

#     return checksum


def render_disk(disk: Disk, /) -> str:
    return "".join(block.render() for block in disk)


def print_disk(disk: Disk, /) -> None:
    print(render_disk(disk))


dataset: str = "2333133121414131402"
# dataset: str = read_dataset()

disk: MutableDisk = parse_disk_map(dataset)

print_disk(disk)

for fragment in iter_fragments(disk):
    print(fragment)

# # --- Part One ---

# import time

# t0 = time.time()
# compact_disk(disk)
# print_disk(disk)
# print("Took:", time.time() - t0)

# # checksum_part_1: int = calculate_filesystem_checksum(disk_1)
# # assert checksum_part_1 == 6435922584968

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
