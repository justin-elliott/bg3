#!/usr/bin/env python3
"""
Cunning action spells for Baldur's Gate 3 mods.
"""

from modtools.gamedata import PassiveData, StatusData
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
        loca[f"{running_jump}_DisplayName"] = {"en": "Running Jump"}
        loca[f"{running_jump}_Description"] = {"en": """
            After <LSTag Type="Spell" Tooltip="Shout_Dash">Dashing</LSTag> or taking a similar action, you can
            <LSTag Type="Spell" Tooltip="Projectile_Jump">Jump</LSTag> once that turn without using a bonus action.
            """}

        self._mod.add(PassiveData(
            running_jump,
            DisplayName=loca[f"{running_jump}_DisplayName"],
            Description=loca[f"{running_jump}_Description"],
            Icon="Action_AoEDamageOnJump",
            Properties=["Highlighted"],
            StatsFunctorContext="OnCast",
            Conditions="SpellCategoryIs(SpellCategory.Dash)",
            StatsFunctors=f"ApplyStatus(SELF,{running_jump.upper()},100,1)",
        ))
        self._mod.add(PassiveData(
            f"{running_jump}_Remove",
            DisplayName=loca[f"{running_jump}_DisplayName"],
            Description=loca[f"{running_jump}_Description"],
            Icon="Action_AoEDamageOnJump",
            Properties=["IsHidden"],
            StatsFunctorContext="OnCast",
            Conditions="SpellId('Projectile_Jump')",
            StatsFunctors=f"RemoveStatus(SELF,{running_jump.upper()})",
        ))
        self._mod.add(StatusData(
            running_jump.upper(),
            StatusType="BOOST",
            DisplayName=loca[f"{running_jump}_DisplayName"],
            Description=loca[f"{running_jump}_Description"],
            Icon="Action_AoEDamageOnJump",
            StackId=running_jump.upper(),
            TickType="EndTurn",
            Boosts=[
                "UnlockSpellVariant(SpellId('Projectile_Jump'),"
                + "ModifyUseCosts(Replace,BonusActionPoint,0,0,BonusActionPoint))"
            ],
            Passives=[f"{running_jump}_Remove"],
            StatusGroups="SG_RemoveOnRespec",
        ))

        return running_jump
