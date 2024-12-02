""" Day 1: Historian Hysteria """

from typing import Collection, Generator, Iterable, Sequence, Tuple


def read_input() -> Generator[Tuple[int, int], None, None]:
    file: Iterable[str]
    with open("input") as file:
        line: str
        for line in file:
            lhs: int
            rhs: int
            lhs, rhs = map(int, line.split())

            yield lhs, rhs


# Load the entire input into memory
input: Collection[Tuple[int, int]] = tuple(read_input())

# Split into columns and sort
locations_lhs: Sequence[int]
locations_rhs: Sequence[int]
locations_lhs, locations_rhs = map(sorted, zip(*input))

# Total distance between all locations
total_distance: int = sum(
    abs(lhs - rhs) for lhs, rhs in zip(locations_lhs, locations_rhs)
)

print(total_distance)


# def main() -> None:
#     ...

# if __name__ == "__main__":
#     main()
