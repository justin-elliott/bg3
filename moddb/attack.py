#!/usr/bin/env python3
"""
Attack-related functionality for Baldur's Gate 3 mods.
"""

from functools import cached_property
from modtools.gamedata import SpellData
from modtools.mod import Mod


class Attack:
    """Attack-related functionality for Baldur's Gate 3 mods."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize for the given Mod."""
        self._mod = mod

    @cached_property
    def _brutal_cleave_display_name(self):
        """Get the localization handle for the Brutal Cleave display name."""
        display_name = f"{self._mod.get_prefix()}_BrutalCleave_DisplayName"
        loca = self._mod.get_localization()
        loca[display_name] = {"en": "Brutal Cleave"}
        return loca[display_name]

    @cached_property
    def _brutal_cleave_description(self):
        """Get the localization handle for the Brutal Cleave description."""
        description = f"{self._mod.get_prefix()}_BrutalCleave_Description"
        loca = self._mod.get_localization()
        loca[description] = {"en": """
            Swing your weapon in a large arc to attack up to [1] enemies at once.
            """}
        return loca[description]

    def add_brutal_cleave(self, *,
                          display_name_handle: str = None,
                          description_handle: str = None,
                          icon: str = "Action_Cleave_New") -> None:
        """Add the Brutal Cleave attack, returning its name."""
        name = f"{self._mod.get_prefix()}_BrutalCleave"

        if not display_name_handle:
            display_name_handle = self._brutal_cleave_display_name
        if not description_handle:
            description_handle = self._brutal_cleave_description

        self._mod.add(SpellData(
            name,
            using="Zone_Cleave",
            SpellType="Zone",
            Cooldown="",
            DisplayName=display_name_handle,
            Description=description_handle,
            Icon=icon,
            SpellSuccess=[
                "DealDamage(MainMeleeWeapon,MainWeaponDamageType);GROUND:ExecuteWeaponFunctors(MainHand)",
            ],
            TooltipDamageList=[
                "DealDamage(MainMeleeWeapon,MainWeaponDamageType)",
            ],
        ))

        return name
