# data/characters/__init__.py
from .ninja import Symbols as NinjaSymbols, Straights as NinjaStraights, Abilities as NinjaAbilities
from .paladin import Symbols as PaladinSymbols, Straights as PaladinStraights, Abilities as PaladinAbilities
from .pyromancer import Symbols as PyromancerSymbols, Straights as PyromancerStraights, Abilities as PyromancerAbilities
from .barbarian import Symbols as BarbarianSymbols, Straights as BarbarianStraights, Abilities as BarbarianAbilities
from .moon_elf import Symbols as MoonElfSymbols, Straights as MoonElfStraights, Abilities as MoonElfAbilities
from .shadow_thief import Symbols as ShadowThiefSymbols, Straights as ShadowThiefStraights, Abilities as ShadowThiefAbilities
from .monk import Symbols as MonkSymbols, Straights as MonkStraights, Abilities as MonkAbilities
from .treant import Symbols as TreantSymbols, Straights as TreantStraights, Abilities as TreantAbilities

CHARACTERS = {
    "Ninja": {
        "symbols": NinjaSymbols,
        "straights": NinjaStraights,
        "abilities": NinjaAbilities,
    },
    "Paladin": {
        "symbols": PaladinSymbols,
        "straights": PaladinStraights,
        "abilities": PaladinAbilities,
    },
    "Pyromancer": {
        "symbols": PyromancerSymbols,
        "straights": PyromancerStraights,
        "abilities": PyromancerAbilities,
    },
    "Barbarian": {
        "symbols": BarbarianSymbols,
        "straights": BarbarianStraights,
        "abilities": BarbarianAbilities,
    },
    "Moon Elf": {
        "symbols": MoonElfSymbols,
        "straights": MoonElfStraights,
        "abilities": MoonElfAbilities,
    },
    "Shadow Thief": {
        "symbols": ShadowThiefSymbols,
        "straights": ShadowThiefStraights,
        "abilities": ShadowThiefAbilities,
    },
    "Monk": {
        "symbols": MonkSymbols,
        "straights": MonkStraights,
        "abilities": MonkAbilities,
    },
    "Treant": {
        "symbols": TreantSymbols,
        "straights": TreantStraights,
        "abilities": TreantAbilities,
    },
}
