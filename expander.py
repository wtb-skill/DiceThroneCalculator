# expander.py

import itertools
from data.characters.ninja import Symbols, Straights, Abilities


class PatternExpander:
    @staticmethod
    def expand_pattern(pattern):
        free_slots = 5 - len(pattern)
        results = []
        for base in itertools.product(*[Symbols.MAP[sym] for sym in pattern]):
            if free_slots > 0:
                for extra in itertools.product(range(1, 7), repeat=free_slots):
                    results.append(tuple(sorted(base + extra)))
            else:
                results.append(tuple(sorted(base)))
        return set(results)

    @staticmethod
    def expand_straight(name):
        results = []
        for needed in Straights.MAP[name]:
            for combo in itertools.permutations(needed, 5 if len(needed) == 5 else 4):
                if len(needed) < 5:
                    for extra in itertools.product(range(1, 7), repeat=5 - len(needed)):
                        results.append(tuple(sorted(combo + extra)))
                else:
                    results.append(tuple(sorted(combo)))
        return set(results)

    @staticmethod
    def expand_ability(name):
        info = Abilities.MAP[name]
        if "pattern" in info:
            return PatternExpander.expand_pattern(info["pattern"])
        if "straight" in info:
            return PatternExpander.expand_straight(info["straight"])
        return set()

    @staticmethod
    def expand_selected(ability_names):
        target = set()
        for name in ability_names:
            target |= PatternExpander.expand_ability(name)
        return target
