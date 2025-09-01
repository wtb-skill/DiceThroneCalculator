# advisor.py

import itertools
import math
from functools import lru_cache
from typing import List, Set, Tuple
from expander import PatternExpander

SIDES = 6
NUM_DICE = 5


class ProbabilityAdvisor:
    @staticmethod
    def unique_rolls_with_weights(num_dice: int):
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

    @staticmethod
    @lru_cache(maxsize=None)
    def prob_after_reroll(roll: Tuple[int, ...], target_set: frozenset) -> float:
        best = 0.0
        for k in range(NUM_DICE + 1):
            for idxs in itertools.combinations(range(NUM_DICE), k):
                kept = [roll[i] for i in idxs]
                m = NUM_DICE - k
                total_weight = 0
                succ_weight = 0
                for outcome, weight in ProbabilityAdvisor.unique_rolls_with_weights(m):
                    total_weight += weight
                    new_roll = tuple(sorted(kept + list(outcome)))
                    if new_roll in target_set:
                        succ_weight += weight
                prob = succ_weight / total_weight if total_weight > 0 else 0.0
                if prob > best:
                    best = prob
        return best

    @staticmethod
    def exact_prob_for_keep(
        initial_roll: List[int],
        keep_indices: Tuple[int, ...],
        target_set: Set[Tuple[int, ...]],
        last_reroll: bool = False,
    ) -> float:
        kept = [initial_roll[i] for i in keep_indices]

        if last_reroll:
            m = NUM_DICE - len(kept)
            total_weight, succ_weight = 0, 0
            for outcome, weight in ProbabilityAdvisor.unique_rolls_with_weights(m):
                total_weight += weight
                roll = tuple(sorted(kept + list(outcome)))
                if roll in target_set:
                    succ_weight += weight
            return succ_weight / total_weight if total_weight > 0 else 0.0

        m1 = NUM_DICE - len(kept)
        total_weight, succ_weight = 0, 0
        for outcome1, weight1 in ProbabilityAdvisor.unique_rolls_with_weights(m1):
            total_weight += weight1
            roll1 = tuple(sorted(kept + list(outcome1)))

            if roll1 in target_set:
                succ_weight += weight1
            else:
                best_second = ProbabilityAdvisor.prob_after_reroll(roll1, frozenset(target_set))
                succ_weight += weight1 * best_second

        return succ_weight / total_weight if total_weight > 0 else 0.0

    @staticmethod
    def best_keep(
        initial_roll: List[int],
        selected: List[str],
        last_reroll: bool = False,
    ) -> Tuple[List[int], float]:
        target_set = PatternExpander.expand_selected(selected)
        n = len(initial_roll)
        best = ([], 0.0)
        for k in range(n + 1):
            for idxs in itertools.combinations(range(n), k):
                prob = ProbabilityAdvisor.exact_prob_for_keep(initial_roll, idxs, target_set, last_reroll)
                if prob > best[1]:
                    best = ([initial_roll[i] for i in idxs], prob)
        return best

