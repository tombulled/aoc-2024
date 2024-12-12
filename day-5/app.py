"""Day 5: Print Queue"""

from dataclasses import dataclass, field
from typing import (
    Collection,
    Final,
    Iterable,
    MutableMapping,
    MutableSequence,
    NamedTuple,
    Sequence,
    Set,
    TypeAlias,
)

# Typing
Update: TypeAlias = Sequence[int]
MutableUpdate: TypeAlias = MutableSequence[int]


# Constants
RULE_SEP: Final[str] = "|"
UPDATE_SEP: Final[str] = ","
SECTION_SEP: Final[str] = "\n\n"


# Models
class Rule(NamedTuple):
    """
    Page Ordering Rule

    if both page number X and page number Y are to be produced as part of an update,
    page number X must be printed at some point before page number Y.
    """

    x: int
    y: int


@dataclass
class Dataset:
    """Contents of a parsed dataset"""

    rules: Collection[Rule] = ()
    updates: Sequence[Update] = ()


# Exceptions
@dataclass
class RuleValidationError(Exception):
    """Exception thrown when update validation fails due to a specific rule"""

    rule: Rule


def read_input() -> str:
    """Read the input file"""

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return file.read()


def parse_rule(rule: str, /) -> Rule:
    """Parse a rule, e.g. "x|y", into a (named) tuple of (x, y)"""

    x: int
    y: int
    x, y = map(int, rule.split(RULE_SEP))

    return Rule(x, y)


def parse_update(update: str, /) -> Update:
    """Parse an update, e.g. "75,47,61,53,29", into a sequence of page numbers"""

    return tuple(map(int, update.split(UPDATE_SEP)))


def parse_dataset(string: str, /) -> Dataset:
    """Parse a raw dataset string into updates & rules"""

    raw_rules: str
    raw_updates: str
    raw_rules, raw_updates = string.strip().split(SECTION_SEP)

    rules: Collection[Rule] = tuple(map(parse_rule, raw_rules.split()))
    updates: Sequence[Update] = tuple(map(parse_update, raw_updates.split()))

    return Dataset(rules, updates)


def get_middle_page_number(update: Update, /) -> int:
    """Get the middle page number in an update"""

    length: int = len(update)

    assert length % 2 == 1, "Update contains an even number of pages (no middle)."

    return update[length // 2]


@dataclass
class RuleMachine:
    """Rule machine capable of learning rules and validating updates against learnt rules."""

    rules: MutableMapping[int, Set[int]] = field(default_factory=dict)

    def learn(self, rule: Rule, /) -> None:
        """Learn a given rule (affects all future update validations)"""

        self.rules.setdefault(rule.x, set()).add(rule.y)

    def learn_all(self, rules: Iterable[Rule], /) -> None:
        """Learn all given rules (affects all future update validations)"""

        rule: Rule
        for rule in rules:
            self.learn(rule)

    def validate(self, update: Update, /) -> None:
        """Validate an update against all learnt rules"""

        page_index: int
        page_number: int
        for page_index, page_number in enumerate(update):
            # There are no rules for this page, it gets off scott free! woo!
            if page_number not in self.rules:
                continue

            # Fetch the set of "later" pages that *must* come after the current
            # page (if they are present in the update)
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
        """Check whether the provided update is valid"""

        try:
            self.validate(update)
        except RuleValidationError:
            return False

        return True

    def get_valid_updates(self, updates: Iterable[Update], /) -> Iterable[Update]:
        """Filter `updates` into an iterable of only *valid* updates"""

        return (update for update in updates if self.is_valid(update))

    def get_invalid_updates(self, updates: Iterable[Update], /) -> Iterable[Update]:
        """Filter `updates` into an iterable of only *invalid* updates"""

        return (update for update in updates if not self.is_valid(update))

    def fix(self, update: Update, /) -> Update:
        """Recursively fix the given update to make it valid (if applicable)"""

        rule: Rule

        # Validate the update, and if it's invalid, store a reference to
        # the specific rule that causes the update to fail validation.
        try:
            self.validate(update)

            return update
        except RuleValidationError as error:
            rule = error.rule

        # Create a (mutable) copy of the update so that we can move
        # the contentious page.
        new_update: MutableUpdate = [*update]

        # Determine the locations of the x & y pages
        x_index: int = update.index(rule.x)
        y_index: int = update.index(rule.y)

        # Remove the problematic `x` page
        new_update.pop(x_index)

        # Re-insert the problematic `x` page at a location that conforms
        # to the specific failing rule.
        new_update.insert(y_index, rule.x)

        # Now that we've moved the contentious page, attempt to fix the update again.
        return self.fix(new_update)


def main() -> None:
    """Solution for AoC 2024, Day 5, Parts 1 & 2"""

    # Load the input (dataset) into memory and parse it.
    raw_dataset: str = read_input()
    dataset: Dataset = parse_dataset(raw_dataset)

    # Create a rule machine!
    rule_machine: RuleMachine = RuleMachine()

    # Learn all the rules...
    rule_machine.learn_all(dataset.rules)

    # --- Part One ---

    # Find only the valid updates
    valid_updates: Iterable[Update] = rule_machine.get_valid_updates(dataset.updates)

    # Sum the middle page numbers of all valid updates
    part_1: int = sum(map(get_middle_page_number, valid_updates))

    print("Part 1:", part_1)
    assert part_1 == 4689

    # --- Part Two ---

    # Find only the invalid updates
    invalid_updates: Iterable[Update] = rule_machine.get_invalid_updates(
        dataset.updates
    )

    # Fix the invalid updates
    fixed_updates: Iterable[Update] = map(rule_machine.fix, invalid_updates)

    # Sum the middle page numbers of all fixed (formerly invalid) updates
    total_2: int = sum(map(get_middle_page_number, fixed_updates))

    print("Part 2:", total_2)
    assert total_2 == 6336


if __name__ == "__main__":
    main()
