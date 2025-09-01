# data/characters/ninja.py

class Symbols:
    MAP = {
        "sword": {1, 2, 3},
        "shuriken": {4, 5},
        "skull": {6},
    }


class Straights:
    MAP = {
        "small": [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}],
        "large": [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}],
    }


class Abilities:
    MAP = {
        "slash_1": {"pattern": ["sword", "sword", "sword"]},
        "slash_2": {"pattern": ["sword", "sword", "sword", "sword"]},
        "slash_3": {"pattern": ["sword", "sword", "sword", "sword", "sword"]},
        "walk_the_line": {"pattern": ["shuriken", "shuriken", "shuriken", "shuriken"]},
        "death_blossom": {"pattern": ["sword", "sword", "sword", "shuriken", "shuriken"]},
        "smoke_screen": {"pattern": ["sword", "shuriken", "shuriken", "skull"]},
        "poison_blade": {"straight": "small"},
        "shadow_fang": {"straight": "large"},
        "misdirect": {"pattern": ["sword", "sword", "skull", "skull"]},
        "shadewalk": {"pattern": ["skull", "skull", "skull", "skull"]},
        "jugulate": {"pattern": ["skull", "skull", "skull"]},
        "assassinate": {"pattern": ["skull", "skull", "skull", "skull", "skull"]},
    }
