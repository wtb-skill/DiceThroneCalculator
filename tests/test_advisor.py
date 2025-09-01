import pytest
from advisor import ProbabilityAdvisor
from expander import PatternExpander

def test_unique_rolls_with_weights_counts_sum():
    total = 0
    for _, weight in ProbabilityAdvisor.unique_rolls_with_weights(2):
        total += weight
    # For 2 dice with 6 sides → 36 total permutations
    assert total == 36


def test_prob_after_reroll_simple():
    # Target: any 5 ones
    target = {tuple([1, 1, 1, 1, 1])}
    roll = (1, 1, 1, 1, 1)
    prob = ProbabilityAdvisor.prob_after_reroll(roll, frozenset(target))
    assert prob == 1.0  # already satisfied


def test_exact_prob_for_keep_last_reroll():
    target = {tuple([1, 1, 1, 1, 1])}
    roll = [1, 1, 1, 1, 6]
    # Keep first 4 ones, reroll the 6
    prob = ProbabilityAdvisor.exact_prob_for_keep(roll, (0, 1, 2, 3), target, last_reroll=True)
    # Chance to roll a 1 with one die
    assert prob == pytest.approx(1 / 6)


def test_best_keep_smoke_screen():
    roll = [1, 2, 1, 5, 6]
    abilities = [
        "smoke_screen",
        "shadow_fang",
        "shadewalk",
        "misdirect",
        "assassinate",
    ]
    keep, prob = ProbabilityAdvisor.best_keep(roll, abilities, last_reroll=True)
    assert isinstance(keep, list)
    assert isinstance(prob, float)
    assert 0.0 <= prob <= 1.0

def test_exact_prob_last_reroll_single_die():
    target = {tuple([1, 1, 1, 1, 1])}
    roll = [1, 1, 1, 1, 6]
    prob = ProbabilityAdvisor.exact_prob_for_keep(roll, (0, 1, 2, 3), target, last_reroll=True)
    assert prob == pytest.approx(1 / 6)


def test_exact_prob_last_reroll_three_dice():
    target = {tuple([6, 6, 6, 6, 6])}
    roll = [6, 6, 1, 2, 3]
    prob = ProbabilityAdvisor.exact_prob_for_keep(roll, (0, 1), target, last_reroll=True)
    assert prob == pytest.approx(1 / 216)


def test_exact_prob_two_rerolls():
    target = {tuple([1, 1, 1, 1, 1])}
    roll = [1, 1, 1, 1, 6]
    prob = ProbabilityAdvisor.exact_prob_for_keep(roll, (0, 1, 2, 3), target, last_reroll=False)
    assert prob == pytest.approx(11 / 36)

def test_assassinate_last_reroll():
    roll = [6, 6, 1, 2, 3]
    abilities = ["assassinate"]
    target_set = PatternExpander.expand_selected(abilities)
    prob = ProbabilityAdvisor.exact_prob_for_keep(roll, (0, 1), target_set, last_reroll=True)
    assert prob == pytest.approx(1 / 216)


def test_jugulate_two_rerolls():
    roll = [6, 6, 1, 2, 3]
    abilities = ["jugulate"]
    keep = (0, 1)  # keep the two skulls
    target_set = PatternExpander.expand_selected(abilities)
    prob = ProbabilityAdvisor.exact_prob_for_keep(roll, keep, target_set, last_reroll=False)
    expected = 1 - (25 / 36) ** 3
    assert prob == pytest.approx(expected)


def test_poison_blade_last_reroll():
    roll = [1, 2, 3, 3, 5]
    abilities = ["poison_blade"]
    # Keep 1,2,3,5 → reroll the extra 3
    keep = (0, 1, 2, 4)
    target_set = PatternExpander.expand_selected(abilities)
    prob = ProbabilityAdvisor.exact_prob_for_keep(roll, keep, target_set, last_reroll=True)
    assert prob == pytest.approx(1 / 6)