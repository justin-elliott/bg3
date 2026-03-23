#!/usr/bin/env python3
"""
Movement-related spells and passives for Baldur's Gate 3 mods.
"""

from functools import cached_property
from modtools.gamedata import PassiveData, SpellData
from modtools.mod import Mod
from typing import Optional


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

    def add_fast_movement(self, meters_per_round: float, display_name: Optional[str] = None) -> str:
        """Add a fast movement passive, returning its name."""
        name = f"{self._mod.get_prefix()}_FastMovement_{int(meters_per_round*10)}"
        self._mod.add(PassiveData(
            name,
            DisplayName=display_name or self._fast_movement_display_name,
            Description=self._fast_movement_description,
            DescriptionParams=[f"Distance({meters_per_round})"],
            Icon="PassiveFeature_FastMovement",
            Properties=["Highlighted", "ForceShowInCC"],
            BoostContext=["OnEquip", "OnCreate"],
            Boosts=[f"ActionResource(Movement,{meters_per_round},0)"],
        ))
        return name

    def add_fire_walk(self, use_costs: str | list[str] = "BonusActionPoint:1") -> str:
        """Add the Fire Walk spell, returning its name."""
        name = f"{self._mod.get_prefix()}_FireWalk"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Fire Walk"}
        loca[f"{name}_Description"] = {"en": """
            You step through the hells, reappearing in another location.
            """}

        self._mod.add(SpellData(
            name,
            SpellType="Target",
            using="Target_MAG_Legendary_HellCrawler",
            Cooldown="",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams="",
            SpellProperties=["GROUND:TeleportSource()"],
            UseCosts=use_costs,
        ))

        return name

    def add_misty_step(self, use_costs: str | list[str] = "BonusActionPoint:1") -> str:
        """Add the Misty Step cantrip, returning its name."""
        name = f"{self._mod.get_prefix()}_MistyStep"
        self._mod.add(SpellData(
            name,
            using="Target_MistyStep",
            SpellType="Target",
            Level="",
            SpellStyleGroup="Class",
            UseCosts=use_costs,
        ))
        return name

    def add_shadow_step(self, use_costs: str | list[str] = "BonusActionPoint:1") -> str:
        """Add the Shadow Step cantrip, returning its name."""
        name = f"{self._mod.get_prefix()}_ShadowStep"
        self._mod.add(SpellData(
            name,
            using="Target_MAG_Shadow_Shadowstep",
            SpellType="Target",
            Cooldown="",
            DisplayName=self._mod.loca(f"{name}_DisplayName", "Shadow Step"),
            Description=self._mod.loca(f"{name}_Description", """
                Step through the shadows, teleporting to an unoccupied space you can see.
            """),
            Level="",
            TargetConditions="CanStand('') and not Character() and not Self()",
            UseCosts=use_costs,
        ))
        return name

    def add_shadow_step_monk(self, use_costs: str | list[str] = "BonusActionPoint:1") -> str:
        """Add the Shadow Step cantrip, returning its name. This variant is only suitable for the Monk class."""
        name = f"{self._mod.get_prefix()}_ShadowStepMonk"
        self._mod.add(SpellData(
            name,
            using="Target_ShadowStep",
            SpellType="Target",
            Level="",
            SpellProperties="GROUND:TeleportSource()",
            RequirementConditions="",
            RequirementEvents="",
            TargetConditions="CanStand('') and not Character() and not Self()",
            TooltipStatusApply="",
            UseCosts=use_costs,
        ))
        return name

    def add_wilderness_explorer(self, *, display_name: str | None = None, description: str | None = None) -> str:
        name = self._mod.make_name("WildernessExplorer")
        display_name = display_name or "Wilderness Explorer"
        description = description or """
            You have become an expert at moving through the wilderness.
            <LSTag Type="Status" Tooltip="DIFFICULT_TERRAIN">Difficult Terrain</LSTag> no longer slows you down, and
            you can't slip on grease or ice.
            """
        self._mod.add(PassiveData(
            name,
            DisplayName=self._mod.loca(f"{name}_DisplayName", display_name),
            Description=self._mod.loca(f"{name}_Description", description),
            Boosts=[
                "StatusImmunity(SG_DifficultTerrain)",
                "StatusImmunity(PRONE_GREASE)",
                "StatusImmunity(PRONE_ICE)",
            ],
            Icon="PassiveFeature_LandsStride_DifficultTerrain",
            Properties=["Highlighted", "ForceShowInCC"],
        ))
        return name
