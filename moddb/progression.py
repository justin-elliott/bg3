#!/usr/bin/env python3
"""
Progression-related functions for Baldur's Gate 3 mods.
"""

import re

from collections.abc import Callable, Container, Iterable
from modtools.lsx.game import ActionResource, Progression, update_action_resources

# AddSpells(UUID[,a][,b][,c][,d])
_ADD_SPELLS_REGEX = re.compile(r"AddSpells\(([^,)]*)(?:,([^,)]*))?(?:,([^,)]*))?(?:,([^,)]*))?(?:,([^,)]*))?\)")


def allow_improvement(progressions: Iterable[Progression],
                      levels: Container[int]) -> None:
    """Add additional feats."""
    for progression in progressions:
        if progression.ProgressionType == 0:  # Parent classes only; subclasses don't allow improvement
            progression.AllowImprovement = True if progression.Level in levels else None


def multiply_resources(progressions: Iterable[Progression],
                       resources: Container[ActionResource],
                       multiplier: int) -> None:
    """Increase class resources."""
    for progression in progressions:
        if (boosts := progression.Boosts) is not None:
            progression.Boosts = update_action_resources(boosts, resources,
                                                         lambda _resource, count, _level: count * multiplier)


def spells_always_prepared(progressions: Iterable[Progression]) -> None:
    """Ensure that spells gained with AddSpells() are AlwaysPrepared."""
    for progression in progressions:
        if progression.Selectors:
            selectors = []
            for selector in progression.Selectors:
                if match := _ADD_SPELLS_REGEX.match(selector):
                    args = match.groups("")
                    selector = f"AddSpells({args[0]},{args[1]},{args[2]},{args[3]},{args[4] or "AlwaysPrepared"})"
                selectors.append(selector)
            progression.Selectors = selectors
