"""Day 2: Red-Nosed Reports"""

from typing import Final, Generator, Iterable, Optional, Sequence, TypeAlias

# MAX_BAD_LEVELS: Final[int] = 1

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
    # 1. Safe if the levels are either all increasing or all decreasing
    current_sign: int = get_sign(y - x)
    if expected_sign is not None and (
        expected_sign == 0 or expected_sign != current_sign
    ):
        return False

    # 2. Safe if any two adjacent levels differ by at least one and at most three.
    difference: int = abs(x - y)
    if difference == 0 or difference > 3:
        return False

    # The pair has not been deemed unsafe, and is therefore safe.
    return True


# ans is 282
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


# wrong: 323, 328, 329, 315, 334, 344
# ans: 349
# def is_safe_with_dampening(
#     report: Report, / #, *, expected_sign: Optional[int] = None
# ) -> bool:
#     """Determine whether a report is considered safe (with dampening)"""

#     # print(report)

#     # If the report contains too few levels to be considered unsafe, it is safe.
#     if len(report) < 2:
#         return True

#     # if expected_sign is None:
#     #     expected_sign = get_sign(report[1] - report[0])

#     # previous_lhs: Optional[int] = None

#     # index: int
#     # lhs: int
#     # for index, lhs in enumerate(report[:-1]):
#     #     is_first_pair: bool = index == 0
#     #     rhs: int = report[index + 1]

#     #     print(
#     #         index,
#     #         (lhs, rhs),
#     #         dict(expected_sign=expected_sign, previous_level=previous_lhs),
#     #     )

#     #     if not is_pair_safe(lhs, rhs, expected_sign=expected_sign):
#     #         return is_safe_with_dampening(
#     #             (
#     #                 *((previous_lhs,) if previous_lhs is not None else ()),
#     #                 rhs,
#     #                 *report[index + 1 :],
#     #             ),
#     #             expected_sign=(
#     #                 None if is_first_pair else expected_sign
#     #             )
#     #         )

#     #     previous_lhs = lhs

#     # return False # TEMP!

#     # has_bad_level: bool = False  # we haven't (yet) seen any bad levels
#     # lhs: int = report[0]  # the first level in the report is the first pair's lhs
#     # sign: Optional[int] = None
#     # is_previous_pair_unsafe: bool = False
#     # total_bad_levels: int = 0
#     has_bad_level: bool = False
#     sign: Optional[int] = None
#     previous_lhs: Optional[int] = None

#     # index: int
#     # rhs: int
#     # for index, rhs in enumerate(report[1:]):
#     index: int
#     lhs: int
#     for index, lhs in enumerate(report[:-1]):
#         rhs: int = report[index + 1]

#         # print(index, (lhs, rhs))

#         if sign is None:
#             sign = get_sign(rhs - lhs)

#         if not is_pair_safe(lhs, rhs, expected_sign=sign):
#             if has_bad_level:
#                 return False

#             has_bad_level = True

#             if previous_lhs is not None:
#                 # try and fix (might need to recalc sign)
#                 if index == 1:
#                     sign = get_sign(rhs - previous_lhs)

#                 if not is_pair_safe(previous_lhs, rhs, expected_sign=sign):
#                     if index == 1:
#                         sign = None
#                     # the rhs is bad, promote the lhs
#                     # (don't change the lhs)
#                     continue
#                 ...

#         previous_lhs = lhs
#         lhs = rhs


#         # # If the previous pair was unsafe (and couldn't be fixed), the current lhs is bad,
#         # # so replace it with the previous lhs
#         # if is_previous_pair_unsafe:
#         #     lhs = previous_lhs
#         #     # if sign is None:
#         #     #     sign = get_sign(rhs - previous_lhs)

#         #     # if not is_pair_safe(previous_lhs, rhs, expected_sign=sign):
#         #     #     return False

#         #     # # Our lhs is the bad level, so don't bother checking it.
#         #     # is_previous_pair_unsafe = False
#         # # else:
#         # if sign is None:
#         #     sign = get_sign(rhs - lhs)

#         # if not is_pair_safe(lhs, rhs, expected_sign=sign):
#         #     is_previous_pair_unsafe = True
#         #     # total_bad_levels += 1

#         #     if total_bad_levels > MAX_BAD_LEVELS:
#         #         return False

#         #     if index == 0:
#         #         sign = None

#         #     if previous_lhs is not None:
#         #         if sign is None:
#         #             sign = get_sign(rhs - previous_lhs)

#         #         if is_pair_safe(previous_lhs, rhs, expected_sign=sign):
#         #             is_previous_pair_unsafe = False


#         # # print(index, (lhs, rhs))
#         # # Only if this is the first pair, or the first pair was unsafe, set
#         # # the expected sign of the report
#         # # if index == 0: # or index == 1 and has_bad_level:
#         # if sign is None:
#         #     sign = get_sign(rhs - lhs)

#         # # if sign is None:
#         # #     sign = get_sign(rhs - lhs)

#         # # If the pair is not safe, then suspect the lhs is bad.
#         # # If it's the first bad level, let's try and remove the lhs to see if
#         # # that makes the report safe (otherwise the report is unsafe)
#         # if not is_pair_safe(lhs, rhs, expected_sign=sign):
#         #     # We've seen two unsafe levels, therefore the report is unsafe.
#         #     if has_bad_level:
#         #         # print()
#         #         return False

#         #     # Mark that we've seen a bad level
#         #     has_bad_level = True

#         #     # if index == 0:
#         #     #     sign = None

#         #     # # Test the values either side of the bad level
#         #     # es2 = sign
#         #     # if index == 1:
#         #     #     es2 = get_sign(rhs - previous_lhs)

#         #     # if index == 1:
#         #     #     sign =

#         #     if index == 0:
#         #         sign = None
#         #     elif index == 1:
#         #         sign = get_sign(rhs - previous_lhs)

#         #     if previous_lhs is not None and not is_pair_safe(
#         #         previous_lhs, rhs, expected_sign=sign
#         #     ):
#         #         # The levels either side of the bad level aren't safe, so the report
#         #         # isn't safe even with this problematic level removed.
#         #         return False
#         # # else:
#         #     # Only set the next pair's lhs to our rhs if the pair was safe.
#         #     # This promotes our lhs to be the next pair's lhs if the pair is
#         #     # unsafe and effectively skips the current bad (rhs) level.
#         #     # lhs = rhs


#     # print()

#     # The report has at most one bad level, and is therefore safe.
#     return True


# ans: 349
def is_report_safe_2(
    report: Report, /, *, dampen: bool = True, expected_sign: Optional[int] = None
) -> bool:
    """Determine whether a report is considered safe (with dampening)"""
    
    # print(report)

    # If the report contains too few levels to be considered unsafe, it is safe.
    # if len(report) < 2:
    #     return True

    index: int
    lhs: int
    for index, lhs in enumerate(report[:-1]):
        rhs: int = report[index + 1]

        # print(index, (lhs, rhs)) # TEMP
        # input()

        if expected_sign is None:
            expected_sign = get_sign(rhs - lhs)
            # print("sign not set, detected", expected_sign)

        # If the pair is safe, great! Let's move on to the next one...
        if is_pair_safe(lhs, rhs, expected_sign=expected_sign):
            # print("pair is safe, on to next.")
            continue

        # print("pair not safe")
        if not dampen:
            # print("dampening disabled, report is unsafe.")
            return False
        # print("dampening enabled, will try removal.")

        # try and remove previous lhs
        # safe_with_plhs_removed: bool = True
        # if index != 0:
        #     report_with_plhs_removed: Report = report[1:] if index == 1
        #     sign_with_plhs_removed: Optional[int] = None if index < 2 else expected_sign
        #     print("report is", report_with_plhs_removed, "with plhs removed, and sign", sign_with_plhs_removed)
        #     safe_with_plhs_removed = is_report_safe_2(report_with_plhs_removed, dampen=False, expected_sign=sign_with_plhs_removed)

        safe_with_plhs_removed: bool = True
        if index == 1:
            # try removing first value
            safe_with_plhs_removed = is_report_safe_2(report[1:], dampen=False, expected_sign=None)

        # try and remove lhs
        report_with_lhs_removed: Report = report[1:] if index == 0 else (report[index-1], *report[index+1:])
        sign_with_lhs_removed: Optional[int] = None if index < 2 else expected_sign
        # print("report is", report_with_lhs_removed, "with lhs removed, and sign", sign_with_lhs_removed)
        safe_with_lhs_removed: bool = is_report_safe_2(report_with_lhs_removed, dampen=False, expected_sign=sign_with_lhs_removed)

        # try and remove rhs
        report_with_rhs_removed: Report = (lhs, *report[index+2:])
        sign_with_rhs_removed: Optional[int] = None if index == 0 else expected_sign
        # print("report is", report_with_rhs_removed, "with rhs removed, and sign", sign_with_rhs_removed)
        safe_with_rhs_removed: bool = is_report_safe_2(report_with_rhs_removed, dampen=False, expected_sign=sign_with_rhs_removed)

        if index == 1:
            return safe_with_plhs_removed or safe_with_lhs_removed or safe_with_rhs_removed
        else:
            return safe_with_lhs_removed or safe_with_rhs_removed

    # The report has not been deemed unsafe, and is therefore safe.
    # print("report deemed safe")
    return True


# --- Part One ---
total_safe_reports: int = sum(map(is_report_safe, read_input()))
print("Total Safe Reports:", total_safe_reports)

# --- Part Two ---
total_safe_reports_with_dampening: int = sum(map(is_report_safe_2, read_input()))
print("Total Safe Reports (With Dampening):", total_safe_reports_with_dampening)

# i = """7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9""".splitlines()
# d = [list(map(int, x.split())) for x in i]

# # r = next(read_input())
# # print(r)
# # print(is_safe_with_dampening(r))

# v = [is_report_safe_2(r) for r in d]
# print(v)


# assert is_report_safe_2([100, 1, 2, 3])
# assert is_report_safe_2([1, 100, 2, 3])
# assert is_report_safe_2([1, 2, 100, 3])
# assert is_report_safe_2([1, 2, 3, 100])

# assert is_report_safe_2((57, 54, 55, 57, 59, 61))
# assert is_report_safe_2((85, 86, 85, 82, 79))
# assert is_report_safe_2((88, 86, 88, 90, 91, 94))
# assert is_report_safe_2((75, 78, 75, 73, 70))
# assert is_report_safe_2((91, 94, 93, 92, 90))
