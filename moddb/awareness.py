#!/usr/bin/env python3
"""
Awareness for Baldur's Gate 3 mods.
"""

from modtools.gamedata import PassiveData, StatusData
from modtools.mod import Mod


class Awareness:
    """Adds the Awareness passive to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    def add_awareness(self, initiative: int = 3) -> str:
        """The Awareness passive, a variant of Alert."""
        name = f"{self._mod.get_prefix()}_Awareness"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Awareness"}
        loca[f"{name}_Description"] = {"en": """
            You have honed your senses to the utmost degree. You gain a +[1] bonus to Initiative, can't be
            <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>, and attackers can't land
            <LSTag Tooltip="CriticalHit">Critical Hits</LSTag> against you.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=[str(initiative)],
            Icon="Action_Barbarian_MagicAwareness",
            Properties=["ForceShowInCC", "Highlighted"],
            Boosts=[
                f"Initiative({initiative})",
                "StatusImmunity(SURPRISED)",
                "CriticalHit(AttackTarget,Success,Never)",
            ],
        ))

        return name
