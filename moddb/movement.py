#!/usr/bin/env python3
"""
Movement-related spells and passives for Baldur's Gate 3 mods.
"""

from functools import cached_property
from modtools.gamedata import passive_data, spell_data
from modtools.mod import Mod


class Movement:
    """Adds movement-related spells and passives to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    @cached_property
    def _fast_movement_display_name(self):
        """Get the localization handle for the Fast Movement display name."""
        display_name = f"{self._mod.get_prefix()}_FastMovement_DisplayName"
        loca = self._mod.get_localization()
        loca[display_name] = {"en": "Fast Movement"}
        return loca[display_name]

    @cached_property
    def _fast_movement_description(self):
        """Get the localization handle for the Fast Movement description."""
        description = f"{self._mod.get_prefix()}_FastMovement_Description"
        loca = self._mod.get_localization()
        loca[description] = {"en": """
            <LSTag Tooltip="MovementSpeed">Movement speed</LSTag> increased by [1].
            """}
        return loca[description]

    def add_fast_movement(self, meters_per_round: float) -> str:
        """Add a fast movement passive, returning its name."""
        name = f"{self._mod.get_prefix()}_FastMovement_{int(meters_per_round*10)}"
        self._mod.add(passive_data(
            name,
            DisplayName=self._fast_movement_display_name,
            Description=self._fast_movement_description,
            DescriptionParams=[f"Distance({meters_per_round})"],
            Icon="PassiveFeature_FastMovement",
            Properties=["Highlighted", "ForceShowInCC"],
            BoostContext=["OnEquip", "OnCreate"],
            Boosts=[f"ActionResource(Movement,{meters_per_round},0)"],
        ))
        return name

    def add_misty_step(self, use_costs: str | list[str] = "Movement:Distance*0.5") -> str:
        """Add a fast movement passive, returning its name."""
        name = f"{self._mod.get_prefix()}_MistyStep"
        self._mod.add(spell_data(
            name,
            using="Target_MistyStep",
            SpellType="Target",
            Level="",
            SpellSchool="None",
            Sheathing="Sheathed",
            SpellStyleGroup="Class",
            UseCosts=use_costs,
        ))
        return name
