"""Day 5: Print Queue"""

from dataclasses import dataclass, field
from typing import (
    Collection,
    Final,
    Iterable,
    MutableMapping,
    NamedTuple,
    Sequence,
    Set,
    TypeAlias,
)

# Typing
Update: TypeAlias = Sequence[int]


class Rule(NamedTuple):
    x: int
    y: int


# Constants
RULE_SEP: Final[str] = "|"
UPDATE_SEP: Final[str] = ","
SECTION_SEP: Final[str] = "\n\n"


# Exceptions
@dataclass
class RuleValidationError(Exception):
    rule: Rule


@dataclass
class Dataset:
    rules: Collection[Rule] = ()
    updates: Sequence[Update] = ()


def read_input() -> str:
    """Read the input file"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return file.read()


def parse_rule(rule: str, /) -> Rule:
    x: int
    y: int
    x, y = map(int, rule.split(RULE_SEP))

    return Rule(x, y)


def parse_update(update: str, /) -> Update:
    return tuple(map(int, update.split(UPDATE_SEP)))


def parse_dataset(dataset: str, /) -> Dataset:
    raw_rules: str
    raw_updates: str
    raw_rules, raw_updates = dataset.strip().split(SECTION_SEP)

    rules: Collection[Rule] = tuple(map(parse_rule, raw_rules.split()))
    updates: Sequence[Update] = tuple(map(parse_update, raw_updates.split()))

    return Dataset(rules, updates)


def get_middle_page_number(update: Update, /) -> int:
    length: int = len(update)

    assert length % 2 == 1, "Update contains an even number of pages."

    return update[length // 2]


@dataclass
class RuleMachine:
    rules: MutableMapping[int, Set[int]] = field(default_factory=dict)

    def learn(self, rule: Rule, /) -> None:
        self.rules.setdefault(rule.x, set()).add(rule.y)

    def learn_all(self, rules: Iterable[Rule], /) -> None:
        rule: Rule
        for rule in rules:
            self.learn(rule)

    def validate(self, update: Update, /) -> None:
        page_index: int
        page_number: int
        for page_index, page_number in enumerate(update):
            # There are no rules for this page, it gets off scot free! woo!
            if page_number not in self.rules:
                continue

            later_pages: Set[int] = self.rules[page_number]

            later_page: int
            for later_page in later_pages:
                # This "later" page doesn't appear in the update, so this
                # specific rule doesn't apply.
                if later_page not in update:
                    continue

                later_page_index: int = update.index(later_page)

                # If this "later" page appears before the current page,
                # the rule has been broken and the update isn't valid.
                if later_page_index < page_index:
                    raise RuleValidationError(Rule(page_number, later_page))

    def is_valid(self, update: Update, /) -> bool:
        try:
            self.validate(update)
        except RuleValidationError:
            return False

        return True

    def get_valid_updates(self, updates: Iterable[Update], /) -> Iterable[Update]:
        return (update for update in updates if self.is_valid(update))

    def get_invalid_updates(self, updates: Iterable[Update], /) -> Iterable[Update]:
        return (update for update in updates if not self.is_valid(update))

    def fix(self, update: Update, /) -> Update:
        # index: int
        # for index in range(len(update)):
        #     # This page is valid, we don't need to fix it.
        #     if self._validate_page(update, index):
        #         continue

        return update  # TEMP


EXAMPLE_INPUT: Final[
    str
] = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".strip()
EXAMPLE_OUTPUT: Sequence[Sequence[int]] = (
    (75, 47, 61, 53, 29),
    (97, 61, 53, 29, 13),
    (75, 29, 13),
)
EXAMPLE_SCORE: int = 143

raw_dataset: str = read_input()
# dataset: Dataset = parse_dataset(EXAMPLE_INPUT)
dataset: Dataset = parse_dataset(raw_dataset)

# --- Part One ---

rule_machine: RuleMachine = RuleMachine()
# total: int = 0

# Learn all the rules
rule_machine.learn_all(dataset.rules)

total: int = sum(
    map(get_middle_page_number, rule_machine.get_valid_updates(dataset.updates))
)

print("Part 1:", total)
assert total == 4689

# --- Part Two ---

# invalid_updates: Iterable[Update] = rule_machine.get_invalid_updates(dataset.updates)
# fixed_updates: Iterable[Update] = map(rule_machine.fix, invalid_updates)
# total_2: int = sum(map(get_middle_page_number, fixed_updates))

# print("Part 2:", total_2)
# assert total_2 == ???
