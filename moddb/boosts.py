#!/usr/bin/env python3
"""
Boosts-related functionality for Baldur's Gate 3 mods.
"""

from collections.abc import Callable
from moddb.scripts import character_level_range
from modtools.mod import Mod


def _boosts_by_level(boost_fn: (Callable[[int], str]), lastLevel: int = 12) -> [str]:
    """Generate a list of boost values."""
    range_and_boost = [(1, 1, boost_fn(1))]

    for level in range(1, lastLevel + 1):
        boost = boost_fn(level)
        if boost != range_and_boost[-1][2]:
            range_and_boost.append((level, level, boost))
        else:
            range_and_boost[-1] = (range_and_boost[-1][0], level, boost)

    range_and_boost[-1] = (range_and_boost[-1][0], 20, range_and_boost[-1][2])  # End at level 20

    return [f"IF(CharacterLevelRange({first},{last})):{boost}" for first, last, boost in range_and_boost]


def boosts_by_level_for(mod: Mod) -> _boosts_by_level:
    mod.add_script(character_level_range)
    return _boosts_by_level
