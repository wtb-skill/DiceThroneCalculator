import pytest
from expander import PatternExpander

# Test individual pattern expansion
def test_expand_pattern_jugulate():
    # jugulate = ["skull", "skull", "skull"] → skull = 6
    expected_unsorted = {(6, 6, 6, a, b) for a in range(1, 7) for b in range(1, 7)}
    # sort each tuple
    expected = {tuple(sorted(t)) for t in expected_unsorted}

    result = PatternExpander.expand_pattern(["skull", "skull", "skull"])
    assert expected == result


def test_expand_pattern_slash_1():
    # slash_1 = ["sword", "sword", "sword"] → sword = 1,2,3
    result = PatternExpander.expand_pattern(["sword", "sword", "sword"])
    # All values should be from 1,2,3 for first 3 dice
    for tup in result:
        assert all(die in {1,2,3} for die in tup[:3])

def test_expand_straight_small():
    # small straight = [{1,2,3,4},{2,3,4,5},{3,4,5,6}]
    result = PatternExpander.expand_straight("small")
    # Every tuple should contain at least 4 numbers from 1-6
    for tup in result:
        assert all(1 <= die <= 6 for die in tup)
        assert len(tup) == 5  # Always 5 dice after filling

def test_expand_ability_pattern():
    # smoke_screen = ["sword","shuriken","shuriken","skull"]
    result = PatternExpander.expand_ability("smoke_screen")
    for tup in result:
        # first die in sword values
        assert tup[0] in {1,2,3} or tup[1] in {1,2,3} or tup[2] in {1,2,3} \
               or tup[3] in {1,2,3} or tup[4] in {1,2,3}

def test_expand_selected_multiple():
    abilities = ["slash_1","jugulate"]
    result = PatternExpander.expand_selected(abilities)
    # Result should contain both jugulate patterns (with skull) and slash_1 patterns (with swords)
    contains_skull = any(6 in tup for tup in result)
    contains_sword = any(any(d in {1,2,3} for d in tup) for tup in result)
    assert contains_skull
    assert contains_sword
