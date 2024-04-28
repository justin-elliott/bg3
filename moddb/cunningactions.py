#!/usr/bin/env python3
"""
Cunning action spells for Baldur's Gate 3 mods.
"""

from functools import cached_property
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import SpellList
from modtools.mod import Mod


class CunningActions:
    """Adds the cunning actions spell list to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    def spell_list(self, *, step_of_the_wind=True) -> SpellList:
        """Adds the cunning actions spell list, returning its name."""
        cunning_actions = SpellList(
            Comment="Cunning Actions",
            Spells=[
                "Shout_Dash_CunningAction",
                "Shout_Hide_BonusAction",
                "Shout_Disengage_CunningAction",
            ],
            UUID=self._mod.make_uuid(f"{self._mod.get_prefix()}_CunningActions_SpellList"),
        )
        self._mod.add(cunning_actions)
        return cunning_actions

    @cached_property
    def running_jump(self) -> str:
        running_jump = f"{self._mod.get_prefix()}_RunningJump"
        loca = self._mod.get_localization()
        loca[f"{running_jump}_DisplayName"] = {"en": "Running Jump"}
        loca[f"{running_jump}_Description"] = {"en": """
            Once per turn, after <LSTag Type="Spell" Tooltip="Shout_Dash">Dashing</LSTag> or taking a similar action,
            you can <LSTag Type="Spell" Tooltip="Projectile_Jump">Jump</LSTag> without using a bonus action.
            """}
        self._mod.add(PassiveData(
            running_jump,
            using="MAG_Mobility_JumpOnDash_Passive",
            DisplayName=loca[f"{running_jump}_DisplayName"],
            Description=loca[f"{running_jump}_Description"],
        ))
        return running_jump
