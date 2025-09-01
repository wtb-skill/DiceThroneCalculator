# advisor.py

import itertools
import math
from typing import List, Set, Tuple
from functools import lru_cache
from create_set import expand_selected

SIDES = 6
NUM_DICE = 5


def unique_rolls_with_weights(num_dice: int):
    """
    Generate all unique sorted outcomes of `num_dice` dice,
    together with their multiplicity (how many permutations they represent).
    """
    if num_dice == 0:
        yield tuple(), 1
        return

    for outcome in itertools.combinations_with_replacement(range(1, SIDES + 1), num_dice):
        counts = {}
        for v in outcome:
            counts[v] = counts.get(v, 0) + 1
        mult = math.factorial(num_dice)
        for c in counts.values():
            mult //= math.factorial(c)
        yield outcome, mult


@lru_cache(maxsize=None)
def prob_after_reroll(roll: Tuple[int, ...], target_set: frozenset) -> float:
    """
    Maximum probability of success with exactly one reroll left.
    """
    best = 0.0
    for k in range(NUM_DICE + 1):
        for idxs in itertools.combinations(range(NUM_DICE), k):
            kept = [roll[i] for i in idxs]
            m = NUM_DICE - k
            total_weight = 0
            succ_weight = 0
            for outcome, weight in unique_rolls_with_weights(m):
                total_weight += weight
                new_roll = tuple(sorted(kept + list(outcome)))
                if new_roll in target_set:
                    succ_weight += weight
            prob = succ_weight / total_weight if total_weight > 0 else 0.0
            if prob > best:
                best = prob
    return best


def exact_prob_for_keep(
    initial_roll: List[int],
    keep_indices: Tuple[int, ...],
    target_set: Set[Tuple[int, ...]],
    last_reroll: bool = False,
) -> float:
    """
    Compute exact probability of ending in target_set,
    keeping dice at keep_indices and rerolling optimally.
    last_reroll=True → only one final reroll
    last_reroll=False → up to two rerolls
    """
    kept = [initial_roll[i] for i in keep_indices]

    if last_reroll:
        # Only one final reroll: roll remaining dice once
        m = NUM_DICE - len(kept)
        total_weight, succ_weight = 0, 0
        for outcome, weight in unique_rolls_with_weights(m):
            total_weight += weight
            roll = tuple(sorted(kept + list(outcome)))
            if roll in target_set:
                succ_weight += weight
        return succ_weight / total_weight if total_weight > 0 else 0.0

    # Two rerolls left → simulate first reroll, then optimize second
    m1 = NUM_DICE - len(kept)
    total_weight, succ_weight = 0, 0
    for outcome1, weight1 in unique_rolls_with_weights(m1):
        total_weight += weight1
        roll1 = tuple(sorted(kept + list(outcome1)))

        if roll1 in target_set:
            succ_weight += weight1
        else:
            best_second = prob_after_reroll(roll1, frozenset(target_set))
            succ_weight += weight1 * best_second

    return succ_weight / total_weight if total_weight > 0 else 0.0


def best_keep(
    initial_roll: List[int],
    selected: List[str],
    last_reroll: bool = False,
) -> Tuple[List[int], float]:
    """
    Return best dice to keep and probability for the selected abilities.
    """
    target_set = expand_selected(selected)
    n = len(initial_roll)
    best = ([], 0.0)
    for k in range(n + 1):
        for idxs in itertools.combinations(range(n), k):
            prob = exact_prob_for_keep(initial_roll, idxs, target_set, last_reroll)
            if prob > best[1]:
                best = ([initial_roll[i] for i in idxs], prob)
    return best


if __name__ == "__main__":
    # 1st test
    # roll = [3, 3, 3, 3, 5]
    # abilities = ["shadow_fang", "slash_3"]
    #
    # keep, prob = best_keep(roll, abilities, last_reroll=True)
    # print(f"Initial roll: {roll}")
    # print(f"Aiming for any of the selected abilities: {abilities}")
    # print(f"Last reroll only → Best keep: {keep}, Probability: {prob:.2%}")
    #
    # keep2, prob2 = best_keep(roll, abilities, last_reroll=False)
    # print(f"\nTwo rerolls allowed → Best keep: {keep2}, Probability: {prob2:.2%}")

    # # 2nd test
    # roll = [1, 2, 1, 6, 6]
    # abilities = [
    #     "walk_the_line",
    #     "death_blossom",
    #     "poison_blade",
    #     "shadow_fang",
    #     "shadewalk",
    #     "assassinate",
    # ]
    #
    # # Last reroll only
    # keep, prob = best_keep(roll, abilities, last_reroll=True)
    # print(f"Initial roll: {roll}")
    # print(f"Target abilities: {abilities}")
    # print(f"Last reroll only → Best keep: {keep}, Probability: {prob:.2%}")
    #
    # # Two rerolls allowed
    # keep2, prob2 = best_keep(roll, abilities, last_reroll=False)
    # print(f"\nTwo rerolls allowed → Best keep: {keep2}, Probability: {prob2:.2%}")

    # gaining smoke bomb
    roll = [1, 2, 1, 5, 6]
    abilities = [
        "smoke_screen",
        "shadow_fang",
        "shadewalk",
        "misdirect",
        "assassinate",
    ]

    # Last reroll only
    keep, prob = best_keep(roll, abilities, last_reroll=True)
    print(f"Initial roll: {roll}")
    print(f"Target abilities: {abilities}")
    print(f"Last reroll only → Best keep: {keep}, Probability: {prob:.2%}")

    # Two rerolls allowed
    keep2, prob2 = best_keep(roll, abilities, last_reroll=False)
    print(f"\nTwo rerolls allowed → Best keep: {keep2}, Probability: {prob2:.2%}")