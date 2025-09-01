# create_set.py

import itertools
from data.characters.ninja import SYMBOLS, STRAIGHTS, ABILITIES

def expand_pattern(pattern):
    """Expand symbol-based pattern into all valid 5-dice outcomes."""
    free_slots = 5 - len(pattern)
    results = []
    for base in itertools.product(*[SYMBOLS[sym] for sym in pattern]):
        if free_slots > 0:
            for extra in itertools.product(range(1, 7), repeat=free_slots):
                results.append(tuple(sorted(base + extra)))
        else:
            results.append(tuple(sorted(base)))
    return set(results)

def expand_straight(name):
    """Expand straight into all valid outcomes."""
    results = []
    for needed in STRAIGHTS[name]:
        for combo in itertools.permutations(needed, 5 if len(needed) == 5 else 4):
            # Fill up with ANY if small straight < 5 dice
            if len(needed) < 5:
                for extra in itertools.product(range(1, 7), repeat=5-len(needed)):
                    results.append(tuple(sorted(combo + extra)))
            else:
                results.append(tuple(sorted(combo)))
    return set(results)

def expand_ability(name):
    info = ABILITIES[name]
    if "pattern" in info:
        return expand_pattern(info["pattern"])
    if "straight" in info:
        return expand_straight(info["straight"])
    return set()

def expand_selected(ability_names):
    target = set()
    for name in ability_names:
        target |= expand_ability(name)
    return target
