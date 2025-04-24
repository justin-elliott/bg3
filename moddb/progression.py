#!/usr/bin/env python3
"""
Progression-related functions for Baldur's Gate 3 mods.
"""

import re

from collections.abc import Container
from modtools.lsx.game import ActionResource, Progression, update_action_resources

# AddSpells(UUID[,a][,b][,c][,d])
_ADD_SPELLS_REGEX = re.compile(r"AddSpells\(([^,)]+)(?:,([^,)]*))?(?:,([^,)]*))?(?:,([^,)]*))?(?:,([^,)]*))?\)")


def multiply_resources(progression: Progression,
                       resources: Container[ActionResource],
                       multiplier: int) -> None:
    """Increase class resources."""
    if boosts := progression.Boosts:
        progression.Boosts = update_action_resources(boosts, resources,
                                                     lambda _resource, count, _level: count * multiplier)


def spells_always_prepared(progression: Progression) -> bool:
    """Ensure that spells gained with AddSpells() are AlwaysPrepared."""
    was_updated = False

    if progression.Selectors:
        selectors = []
        for selector in progression.Selectors:
            if match := _ADD_SPELLS_REGEX.match(selector):
                args = match.groups("")
                selector = f"AddSpells({args[0]},{args[1]},{args[2]},{args[3]},{args[4] or "AlwaysPrepared"})"
                was_updated = True
            selectors.append(selector)
        progression.Selectors = selectors

    return was_updated
