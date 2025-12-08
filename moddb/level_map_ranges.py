#!/usr/bin/env python3
"""
LevelMapSeries operations for Baldur's Gate 3 mods.
"""

from typing import Any
from modtools.mod import Mod
from modtools.lsx.game import LevelMapSeries

from .scripts import character_level_range

def level_map_ranges(level_map: LevelMapSeries) -> list[(int, int, Any)]:
    """
    Return a list of tuples containing the ranges and corresponding values from a LevelMapSeries
    (first, last, value). The range is right-exclusive, [first, last).
    """
    ranges = []
    first = 0
    value = None

    for i in range(0, 21):
        if (new_value := getattr(level_map, f"Level{i}", None)) is not None:
            if first != 0:
                ranges.append((first, i, value))
            first = i
            value = new_value
    if first != 0:
        ranges.append((first, 21, value))

    return ranges

def level_map_ranges_format(mod: Mod, level_map: LevelMapSeries, template: str) -> list[str]:
    """
    For each range in a LevelMapSeries, generate a CharacterLevelRange combined with the template string formatted with
    the range's value.
    """
    mod.add(character_level_range)

    formatted_values = []
    for (first, last, value) in level_map_ranges(level_map):
        formatted_values.append(f"IF(CharacterLevelRange({first},{last - 1})):{template.format(value)}")
    return formatted_values
