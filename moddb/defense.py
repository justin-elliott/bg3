#!/usr/bin/env python3
"""
Defense-related functionality for Baldur's Gate 3 mods.
"""

from functools import cached_property
from modtools.gamedata import PassiveData
from modtools.mod import Mod


class Defense:
    """Defense-related functionality for Baldur's Gate 3 mods."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize for the given Mod."""
        self._mod = mod

    @cached_property
    def _warding_display_name(self):
        """Get the localization handle for the Warding display name."""
        display_name = f"{self._mod.get_prefix()}_Warding_DisplayName"
        loca = self._mod.get_localization()
        loca[display_name] = {"en": "Warding"}
        return loca[display_name]

    @cached_property
    def _warding_description(self):
        """Get the localization handle for the Warding description."""
        description = f"{self._mod.get_prefix()}_Warding_Description"
        loca = self._mod.get_localization()
        loca[description] = {"en": """
            Your magic protects you from harm, making you resistant to all forms of damage.
            Incoming damage is reduced by [1].
            """}
        return loca[description]

    def add_warding(self, *,
                    display_name_handle: str = None,
                    description_handle: str = None,
                    icon: str = "PassiveFeature_ArcaneWard") -> None:
        """Add the Warding passive, returning its name."""
        name = f"{self._mod.get_prefix()}_Warding"

        if not display_name_handle:
            display_name_handle = self._warding_display_name
        if not description_handle:
            description_handle = self._warding_description

        self._mod.add(PassiveData(
            name,
            DisplayName=display_name_handle,
            Description=description_handle,
            DescriptionParams=["RegainHitPoints(max(1,Level))"],
            Icon=icon,
            Properties=["Highlighted"],
            Boosts=["DamageReduction(All,Flat,Level)"],
        ))

        return name
