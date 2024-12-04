"""Day 2: Red-Nosed Reports"""

from typing import Collection, Generator, Iterable, Optional, Sequence, TypeAlias

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


def is_pair_safe(x: int, y: int, /, *, expected_sign: Optional[int] = None) -> bool:
    """Determine whether a pair of levels from a report are considered safe"""

    # Safe if the levels are either all increasing or all decreasing
    current_sign: int = get_sign(y - x)
    if expected_sign is not None and (
        expected_sign == 0 or expected_sign != current_sign
    ):
        return False

    # Safe if any two adjacent levels differ by at least one and at most three.
    difference: int = abs(x - y)
    if difference == 0 or difference > 3:
        return False

    # The pair has not been deemed unsafe, and is therefore safe.
    return True


def is_report_safe(report: Report, /) -> bool:
    """Determine whether a report is considered safe"""

    sign: int

    index: int
    level: int
    for index, level in enumerate(report[:-1]):
        level2: int = report[index + 1]

        # Only if this is the first pair, set the expected sign of the report
        if index == 0:
            sign = get_sign(level2 - level)

        # If this pair is not safe, the report is not safe
        if not is_pair_safe(level, level2, expected_sign=sign):
            return False

    # The report has not been deemed unsafe, and is therefore safe.
    return True


def is_report_safe_2(
    report: Report, /, *, dampen: bool = True, expected_sign: Optional[int] = None
) -> bool:
    """Determine whether a report is considered safe (with dampening)"""

    index: int
    lhs: int
    for index, lhs in enumerate(report[:-1]):
        rhs: int = report[index + 1]

        # If the sign is unknown, calculate it.
        if expected_sign is None:
            expected_sign = get_sign(rhs - lhs)

        # If the pair is safe, great! Let's move on to the next one...
        if is_pair_safe(lhs, rhs, expected_sign=expected_sign):
            continue

        # Otherwise, the pair is unsafe, let's take a closer look.

        # If dampening is disabled, one bad pair means the entire report is unsafe.
        if not dampen:
            return False

        # See if the report is safe with the lhs removed
        report_with_lhs_removed: Report = (
            report[1:] if index == 0 else (report[index - 1], *report[index + 1 :])
        )
        sign_with_lhs_removed: Optional[int] = None if index < 2 else expected_sign
        safe_with_lhs_removed: bool = is_report_safe_2(
            report_with_lhs_removed, dampen=False, expected_sign=sign_with_lhs_removed
        )

        # See if the report is safe with the rhs removed
        report_with_rhs_removed: Report = (lhs, *report[index + 2 :])
        sign_with_rhs_removed: Optional[int] = None if index == 0 else expected_sign
        safe_with_rhs_removed: bool = is_report_safe_2(
            report_with_rhs_removed, dampen=False, expected_sign=sign_with_rhs_removed
        )

        # If the report is safe with either the lhs, or rhs removed, then the
        # report can be considered safe (through the power of dampening!)
        if safe_with_lhs_removed or safe_with_rhs_removed:
            return True

        # Otherwise, the report is most likely unsafe. *However*, if the second pair
        # is "bad", then this could be because the first level in the report is bad.
        # If the first level in the report is bad, then the sign will likely be wrong,
        # so we should test the safety of the report with the first level removed too.
        return index == 1 and is_report_safe_2(
            report[1:], dampen=False, expected_sign=None
        )

    # The report has not been deemed unsafe, and is therefore safe.
    return True


def main() -> None:
    """Solution for AoC 2024, Day 2, Parts 1 & 2"""

    # Load the entire dataset into memory
    inputs: Collection[Report] = tuple(read_input())

    # --- Part One ---
    total_safe_reports: int = sum(map(is_report_safe, inputs))
    print("Total Safe Reports:", total_safe_reports)
    assert total_safe_reports == 282

    # --- Part Two ---
    total_safe_reports_with_dampening: int = sum(map(is_report_safe_2, inputs))
    print("Total Safe Reports (With Dampening):", total_safe_reports_with_dampening)
    assert total_safe_reports_with_dampening == 349


if __name__ == "__main__":
    main()
