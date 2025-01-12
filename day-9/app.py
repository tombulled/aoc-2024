"""Day 9: Disk Fragmenter"""

from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from typing import (
    Callable,
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


class _CyclicalEnum(IntEnum):
    """Enum with sequential, cyclical members"""

    @classmethod
    def first(cls: Type[Self], /) -> Self:
        """Get the first member of this enum"""

        return cls(1)

    @classmethod
    def last(cls: Type[Self], /) -> Self:
        """Get the last member of this enum"""

        return cls(len(cls))

    def next(self: Self, /) -> Self:
        """Get the next member of this enum"""

        cls: Type[Self] = type(self)
        next_value: int = self.value % len(cls) + 1

        return cls(next_value)


class DiskMapEntryType(_CyclicalEnum):
    """Enum representing the entry types in a disk-map"""

    FILE: int = auto()
    SPACE: int = auto()


class Direction(Enum):
    """Enum representing horizontal direction"""

    LTR: int = auto()
    RTL: int = auto()


@dataclass
class Block:
    """Base block class"""

    pass


@dataclass
class Space(Block):
    """Block representing 'free space'"""

    pass


@dataclass
class File(Block):
    """Block representing a file with the given id"""

    id: int


# Constants
SPACE: Final[Block] = Space()

# Typing
B = TypeVar("B", bound=Block)
Disk: TypeAlias = Sequence[Block]
MutableDisk: TypeAlias = MutableSequence[Block]


@dataclass
class Fragment(Generic[B]):
    """Class representing a fragment of blocks"""

    index: int
    block: B
    size: int


def read_dataset() -> str:
    with open("input", encoding="utf-8") as file:
        return file.read().strip()


def parse_disk_map(disk_map: str, /) -> MutableDisk:
    """Parse a disk-map string into a mutable disk"""

    entry_type: DiskMapEntryType = DiskMapEntryType.first()
    file_id: int = 0

    disk: MutableDisk = []

    # Iterate every character in the disk map
    raw_size: str
    for raw_size in disk_map:
        # The character represents a size, so parse it as an integer
        size: int = int(raw_size)

        block: Block

        # Build the appropriate block depending on what disk-map entry-type
        # we're currently at
        match entry_type:
            case DiskMapEntryType.FILE:
                block = File(file_id)

                # We've just created a file, so increment the file ID ready
                # for the next file
                file_id += 1
            case DiskMapEntryType.SPACE:
                block = SPACE

        # Add all of the blocks created by this disk-map entry to the disk
        for _ in range(size):
            disk.append(block)

        # Move to the next disk-map entry-type
        # (as there are only two, this toggles between them)
        entry_type = entry_type.next()

    return disk


def iter_fragments(
    disk: Disk,
    /,
    *,
    direction: Direction = Direction.LTR,
    predicate: Optional[Callable[[Block], bool]] = None,
    index_start: int = 0,
    index_stop: Optional[int] = None,
) -> Iterable[Fragment[Block]]:
    """
    Iterate fragments in a disk

    Parameters:
        disk: The disk to iterate fragments from
        direction: The direction in which to move along the disk (LTR or RTL)
        predicate: An optional predicate blocks must match for fragments to be yielded
        index_start: The index at which to start iterating the disk
        index_stop: The index at which to stop iterating the disk

    Example:
        The disk "00...111...2" has fragments "00", "...", "111", "..." and "2"
    """

    if index_stop is None:
        index_stop = len(disk)

    block_indices: Iterable[int]

    match direction:
        case direction.LTR:
            block_indices = range(index_start, index_stop)
        case direction.RTL:
            block_indices = range(index_stop - 1, -1 + index_start, -1)

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
    processed_files: MutableSet[int] = set()

    search_space_start: int = 0

    file_fragment: Fragment[Block]
    for file_fragment in file_fragments:
        assert isinstance(file_fragment.block, File)

        if file_fragment.index <= search_space_start:
            break

        if file_fragment.block.id in processed_files:
            continue

        search_space_end: int = file_fragment.index

        space_fragments: Iterable[Fragment[Block]] = iter_fragments(
            disk,
            direction=Direction.LTR,
            predicate=lambda block: isinstance(block, Space),
            index_start=search_space_start,
            index_stop=search_space_end,
        )

        space_fragment_index: int
        space_fragment: Fragment[Block]
        for space_fragment_index, space_fragment in enumerate(space_fragments):
            if file_fragment.size == 0:
                break

            assert isinstance(space_fragment.block, Space)

            if space_fragment_index == 0:
                search_space_start = space_fragment.index

            # If we can't fragment the file and the free space doesn't
            # contain enough space to fit the file as-is, we can't
            # move it here, so skip this location.
            if not fragment and file_fragment.size > space_fragment.size:
                continue

            fragment_size: int = min(space_fragment.size, file_fragment.size)

            disk[space_fragment.index : space_fragment.index + fragment_size] = [
                file_fragment.block
            ] * fragment_size
            disk[
                file_fragment.index
                + file_fragment.size
                - fragment_size : file_fragment.index
                + file_fragment.size
            ] = [space_fragment.block] * fragment_size

            file_fragment.size -= fragment_size

        processed_files.add(file_fragment.block.id)


def clone_disk(disk: Disk, /) -> MutableDisk:
    return list(disk)


def calculate_filesystem_checksum(disk: Disk, /) -> int:
    checksum: int = 0

    block_index: int
    block: Block
    for block_index, block in enumerate(disk):
        if not isinstance(block, File):
            continue

        checksum += block_index * block.id

    return checksum


def main() -> None:
    dataset: str = read_dataset()

    disk_1: MutableDisk = parse_disk_map(dataset)
    disk_2: MutableDisk = clone_disk(disk_1)

    # --- Part One ---

    compact_disk(disk_1)

    part_1: int = calculate_filesystem_checksum(disk_1)

    print("Part 1:", part_1)
    assert part_1 == 6435922584968

    # --- Part Two ---

    compact_disk(disk_2, fragment=False)

    checksum_part_2: int = calculate_filesystem_checksum(disk_2)

    print("Part 2:", checksum_part_2)
    assert checksum_part_2 == 6469636832766


if __name__ == "__main__":
    main()
