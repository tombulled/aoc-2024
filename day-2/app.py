"""Day 2: Red-Nosed Reports"""

from typing import Generator, Iterable, Optional, Sequence, TypeAlias

Report: TypeAlias = Sequence[int]


def read_input() -> Generator[Report, None, None]:
    """Lazily read and parse the input file into reports"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        line: str
        for line in file:
            yield tuple(map(int, line.split()))


def get_sign(x: int, /) -> int:
    """
    Get the sign of `x`

    Example:
        >>> assert sign(1234) == 1
        >>> assert sign(-1234) == -1
        >>> assert sign(0) == 0
    """

    if x == 0:
        return x

    return x // abs(x)


def is_safe(report: Report, /) -> bool:
    """Determine whether a record is considered safe"""

    sign: Optional[int] = None

    index: int
    level: int
    for index, level in enumerate(report[:-1]):
        level2: int = report[index + 1]
        current_sign: int = get_sign(level2 - level)

        # Only if this is the first pair, set the desired sign of the report
        if index == 0:
            sign = current_sign

        # 1. Safe if the levels are either all increasing or all decreasing
        if sign != current_sign:
            return False

        # 2. Safe if any two adjacent levels differ by at least one and at most three.
        difference: int = abs(level - level2)
        if difference == 0 or difference > 3:
            return False

    # The record has not been deemed unsafe, and is therefore safe.
    return True


# --- Part One ---

total_safe_reports: int = sum(map(is_safe, read_input()))

print("Total Safe Reports:", total_safe_reports)

# --- Part Two ---
# ...
