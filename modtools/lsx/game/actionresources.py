#!/usr/bin/env python3
"""
Spell and action resources.
"""

import re

from collections.abc import Container, Iterable
from enum import StrEnum
from typing import Callable, Final


class ActionResource(StrEnum):
    """Baldur's Gate 3 action resources."""
    ARCANE_RECOVERY_CHARGES = "ArcaneRecoveryPoint"
    ARCANE_SHOT_CHARGES = "ArcaneShot"
    BARDIC_INSPIRATION_CHARGES = "BardicInspiration"
    BLADESONG_CHARGES = "Bladesong"
    CHANNEL_DIVINITY_CHARGES = "ChannelDivinity"
    CHANNEL_OATH_CHARGES = "ChannelOath"
    COSMIC_OMEN_POINTS = "CosmicOmen"
    FUNGAL_INFESTATION_CHARGES = "FungalInfestationCharge"
    KI_POINTS = "KiPoint"
    LAY_ON_HANDS_CHARGES = "LayOnHandsCharge"
    NATURAL_RECOVERY_CHARGES = "NaturalRecoveryPoint"
    RAGE_CHARGES = "Rage"
    SORCERY_POINTS = "SorceryPoint"
    SPELL_SLOTS = "SpellSlot"
    STAR_MAP_POINTS = "StarMapPoint"
    SUPERIORITY_DICE = "SuperiorityDie"
    SWARM_CHARGES = "SwarmCharge"
    WARLOCK_SPELL_SLOTS = "WarlockSpellSlot"
    WAR_PRIEST_CHARGES = "WarPriestActionPoint"
    WILD_SHAPE_CHARGES = "WildShape"
    WRITHING_TIDE_POINTS = "WrithingTidePoint"


_ACTION_RESOURCE_REGEX: Final = re.compile(r"^\s*ActionResource\((\w+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*$")


def update_action_resources(iter: Iterable[str],
                            resources: Container[ActionResource],
                            apply: Callable[[str, int, int], int]) -> list[str]:
    """
    Update action resources.

    iter -- The iterable containing resources to be updated.
    resources -- The resources to match against.
    apply -- A callable that returns a new 'count' value when called with the (resource, count, level).
    """
    results = []
    for item in iter:
        if (match := _ACTION_RESOURCE_REGEX.match(item)) is not None:
            resource, count, level = match.groups()
            if resource in resources:
                updated_count = apply(resource, int(count), int(level))
                item = f"ActionResource({resource},{updated_count},{level})"
        results.append(item)
    return results
