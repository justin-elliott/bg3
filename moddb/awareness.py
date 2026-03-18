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

    def add_awareness(self, initiative: int = 0, *, icon: str = "PassiveFeature_Generic_Threat") -> str:
        """The Awareness passive, a variant of Alert."""
        name = self._mod.make_name("Awareness")

        if initiative > 0:
            description = """
                You gain a +[1] bonus to Initiative and can't be 
                <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>.
            """
            initiative_boosts = [f"Initiative({initiative})"]
        else:
            description = """
                Your <LSTag Tooltip="ProficiencyBonus">Proficiency Bonus</LSTag> is added to your Initiative rolls,
                and you can't be <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>.
            """
            levels = [5, 9, 12] if not self._mod.level_20 else [5, 9, 13, 17]  # ensure parity with Alert if not L20
            initiative_boosts = [
                "Initiative(2)",
                *[f"IF(CharacterLevelGreaterThan({level - 1})):Initiative(1)" for level in levels],
            ]

        self._mod.add(PassiveData(
            name,
            DisplayName=self._mod.loca(f"{name}_DisplayName", "Awareness"),
            Description=self._mod.loca(f"{name}_Description", description),
            DescriptionParams=[initiative] if initiative > 0 else None,
            Icon=icon,
            Properties=["ForceShowInCC", "Highlighted"],
            Boosts=[
                *initiative_boosts,
                "StatusImmunity(SURPRISED)",
            ],
        ))

        return name
