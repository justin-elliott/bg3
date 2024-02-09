#!/usr/bin/env python3
"""
Carrying capacity passive for Baldur's Gate 3 mods.
"""

from functools import cached_property
from modtools.gamedata import PassiveData
from modtools.mod import Mod


class PackMule:
    """Adds a carrying capacity passive to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    @cached_property
    def _pack_mule_display_name(self):
        """Get the localization handle for the Pack Mule display name."""
        display_name = f"{self._mod.get_prefix()}_PackMule_DisplayName"
        loca = self._mod.get_localization()
        loca[display_name] = {"en": "Pack Mule"}
        return loca[display_name]

    @cached_property
    def _pack_mule_description(self):
        """Get the localization handle for the Pack Mule description."""
        description = f"{self._mod.get_prefix()}_PackMule_Description"
        loca = self._mod.get_localization()
        loca[description] = {"en": """
            Your carrying capacity is increased by [1]%.
            """}
        return loca[description]

    def add_pack_mule(self, multiplier: float = 1.25) -> str:
        """Add the Pack Mule passive, returning its name."""
        assert multiplier >= 1.0
        percent_increase = int((multiplier - 1.0) * 100.0)
        name = f"{self._mod.get_prefix()}_PackMule_{percent_increase}"
        self._mod.add(PassiveData(
            name,
            DisplayName=self._pack_mule_display_name,
            Description=self._pack_mule_description,
            DescriptionParams=[percent_increase],
            Icon="Spell_Transmutation_EnhanceAbility_BullsStrenght",
            Properties=["Highlighted", "ForceShowInCC"],
            BoostContext=["OnEquip", "OnCreate"],
            Boosts=[f"CarryCapacityMultiplier({multiplier})"],
        ))
        return name
