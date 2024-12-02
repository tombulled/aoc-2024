"""Day 1: Historian Hysteria"""

from typing import Collection, Counter, Generator, Iterable, Sequence, Tuple


def read_input() -> Generator[Tuple[int, int], None, None]:
    """Lazily read and parse the input file into (x, y) pairs"""
    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        line: str
        for line in file:
            lhs: int
            rhs: int
            lhs, rhs = map(int, line.split())

            yield lhs, rhs


def main() -> None:
    """Solution for AoC 2024, Day 1, Parts 1 & 2"""

    # Load the entire dataset into memory
    inputs: Collection[Tuple[int, int]] = tuple(read_input())

    # Split into columns and sort
    locations_lhs: Sequence[int]
    locations_rhs: Sequence[int]
    locations_lhs, locations_rhs = map(sorted, zip(*inputs))

    # --- Part One ---

    # Total distance between all locations
    total_distance: int = sum(
        abs(lhs - rhs) for lhs, rhs in zip(locations_lhs, locations_rhs)
    )

    print("Total Distance:", total_distance)

    # --- Part Two ---

    # Count the number of occurences of each value in the rhs column
    location_counts: Counter[int] = Counter(locations_rhs)

    # Compute the total "similarity score" of values in the lhs column
    similarity_score: int = sum(
        value * location_counts[value] for value in locations_lhs
    )

    print("Similarity Score:", similarity_score)


if __name__ == "__main__":
    main()
