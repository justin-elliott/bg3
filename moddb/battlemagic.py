#!/usr/bin/env python3
"""
Battle Magic for Baldur's Gate 3 mods.
"""

from modtools.gamedata import passive_data, status_data
from modtools.mod import Mod


class BattleMagic:
    """Adds the Battle Magic passive to a Baldur's Gate 3 mod."""
    __mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self.__mod = mod

    def add_battle_magic(self) -> str:
        """Add the Battle Magic passive, returning its name."""
        name = f"{self.__mod.get_prefix()}_BattleMagic"

        loca = self.__mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Battle Magic"}
        loca[f"{name}_Description"] = {"en": """
            After making a melee attack, you can cast a spell as a
            <LSTag Type="ActionResource" Tooltip="BonusActionPoint">bonus action</LSTag>.
            """}

        self.__mod.add(passive_data(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_WarMagic",
            Properties="Highlighted",
            StatsFunctorContext="OnAttack",
            Conditions="IsWeaponAttack() or IsUnarmedAttack()",
            StatsFunctors=f"ApplyStatus(SELF,{name.upper()},100,1)"
        ))

        self.__mod.add(status_data(
            name.upper(),
            StatusType="BOOST",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_WarMagic",
            Boosts=[
                "UnlockSpellVariant(QuickenedSpellCheck(),ModifyUseCosts(Replace,BonusActionPoint,1,0,ActionPoint))",
                "UnlockSpellVariant(RangedSpellAttackCheck(),ModifySpellRoll('AttackType.RangedSpellAttack','AttackType.MeleeSpellAttack'))"
            ],
            StackId=name.upper(),
            StatusPropertyFlags=[
                "DisableOverhead",
                "DisableCombatlog",
                "DisablePortraitIndicator",
            ],
        ))

        return name