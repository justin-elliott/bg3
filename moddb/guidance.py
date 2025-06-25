#!/usr/bin/env python3
"""
Awareness for Baldur's Gate 3 mods.
"""

from modtools.gamedata import SpellData, StatusData
from modtools.mod import Mod


class Guidance:
    """Adds an enhanced guidance spell to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    def add_arcane_guidance(self) -> str:
        """An enhanced guidance spell."""
        arcane_guidance = f"{self._mod.get_name()}_ArcaneGuidance"

        loca = self._mod.get_localization()
        loca[f"{arcane_guidance}_DisplayName"] = {"en": "Arcane Guidance"}
        loca[f"{arcane_guidance}_Description"] = {"en": """
            The target gains a +1d4 bonus to <LSTag Tooltip="AbilityCheck">Ability Checks</LSTag> and
            <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>, and has <LSTag Tooltip="Advantage">Advantage</LSTag> on
            <LSTag Tooltip="Charisma">Charisma</LSTag> checks.
            """}

        self._mod.add(SpellData(
            arcane_guidance,
            SpellType="Target",
            using="Target_Guidance",
            DisplayName=loca[f"{arcane_guidance}_DisplayName"],
            Description=loca[f"{arcane_guidance}_Description"],
            SpellProperties=[f"ApplyStatus({arcane_guidance.upper()},100,10)"],
            TooltipStatusApply=[f"ApplyStatus({arcane_guidance.upper()},100,10)"],
        ))
        self._mod.add(StatusData(
            arcane_guidance.upper(),
            StatusType="BOOST",
            using="GUIDANCE",
            DisplayName=loca[f"{arcane_guidance}_DisplayName"],
            Description=loca[f"{arcane_guidance}_Description"],
            Boosts=[
                "RollBonus(SkillCheck,1d4)",
                "RollBonus(RawAbility,1d4)",
                "RollBonus(SavingThrow,1d4)",
                "RollBonus(DeathSavingThrow,1d4)",
                "Advantage(Ability,Charisma)",
            ],
            StackId=arcane_guidance.upper(),
        ))

        return arcane_guidance
