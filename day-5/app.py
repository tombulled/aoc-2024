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

# Constants
RULE_SEP: Final[str] = "|"
UPDATE_SEP: Final[str] = ","
SECTION_SEP: Final[str] = "\n\n"


class Rule(NamedTuple):
    x: int
    y: int


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

    def validate(self, update: Update, /) -> bool:
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
                    return False

        # The update has not been deemed invalid, and is therefore valid.
        return True


EXAMPLE_INPUT: Final[str] = (
    """
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
)
EXAMPLE_OUTPUT: Sequence[Sequence[int]] = (
    (75, 47, 61, 53, 29),
    (97, 61, 53, 29, 13),
    (75, 29, 13),
)
EXAMPLE_SCORE: int = 143

raw_dataset: str = read_input()
dataset: Dataset = parse_dataset(raw_dataset)
rule_machine: RuleMachine = RuleMachine()

total: int = 0

rule: Rule
for rule in dataset.rules:
    rule_machine.learn(rule)

update: Update
for update in dataset.updates:
    is_valid: bool = rule_machine.validate(update)

    # This report isn't valid, eww.
    if not is_valid:
        continue

    middle_page: int = get_middle_page_number(update)

    total += middle_page

print("Part 1:", total)
assert total == 4689