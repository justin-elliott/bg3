#!/usr/bin/env python3
"""
Cunning action spells for Baldur's Gate 3 mods.
"""

from modtools.gamedata import PassiveData
from modtools.mod import Mod
from uuid import UUID


class CunningActions:
    """Adds the cunning actions spell list to a Baldur's Gate 3 mod."""
    SPELL_LIST = UUID("2dc120ff-903b-494b-8dc8-38721098ce38")

    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    def add_running_jump(self) -> str:
        """Add the Running Jump passive, returning its name."""
        running_jump = f"{self._mod.get_prefix()}_RunningJump"

        loca = self._mod.get_localization()
        loca[f"{running_jump}_Description"] = {"en": """
            Once per turn, after <LSTag Type="Spell" Tooltip="Shout_Dash">Dashing</LSTag> or taking a similar action,
            you can <LSTag Type="Spell" Tooltip="Projectile_Jump">Jump</LSTag> without using a bonus action.
            """}

        self._mod.add(PassiveData(
            running_jump,
            using="MAG_Mobility_JumpOnDash_Passive",
            Description=loca[f"{running_jump}_Description"],
        ))

        return running_jump
