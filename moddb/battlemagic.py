#!/usr/bin/env python3
"""
Battle Magic for Baldur's Gate 3 mods.
"""

from modtools.gamedata import passive_data, status_data
from modtools.mod import Mod


class BattleMagic:
    """Adds the Battle Magic passive to a Baldur's Gate 3 mod."""
    __name: str

    def __init__(self, mod: Mod):
        """Add the Battle Magic passive to the given mod."""
        self.__name = "".join(mod.get_name().split()) + "_BattleMagic"

        loca = mod.get_localization()
        loca[f"{self.__name}_DisplayName"] = {"en": "Battle Magic"}
        loca[f"{self.__name}_Description"] = {"en": """
            After making a melee attack, you can cast a spell as a
            <LSTag Type="ActionResource" Tooltip="BonusActionPoint">bonus action</LSTag>.
            """}

        mod.add(passive_data(
            self.__name,
            DisplayName=loca[f"{self.__name}_DisplayName"],
            Description=loca[f"{self.__name}_Description"],
            Icon="PassiveFeature_WarMagic",
            Properties="Highlighted",
            StatsFunctorContext="OnAttack",
            Conditions="IsWeaponAttack() or IsUnarmedAttack()",
            StatsFunctors=f"ApplyStatus(SELF,{self.__name.upper()},100,1)"
        ))

        mod.add(status_data(
            self.__name.upper(),
            StatusType="BOOST",
            DisplayName=loca[f"{self.__name}_DisplayName"],
            Description=loca[f"{self.__name}_Description"],
            Icon="PassiveFeature_WarMagic",
            Boosts=[
                "UnlockSpellVariant(QuickenedSpellCheck(),ModifyUseCosts(Replace,BonusActionPoint,1,0,ActionPoint))",
                "UnlockSpellVariant(RangedSpellAttackCheck(),ModifySpellRoll('AttackType.RangedSpellAttack','AttackType.MeleeSpellAttack'))"
            ],
            StackId=self.__name.upper(),
            StatusPropertyFlags=[
                "DisableOverhead",
                "DisableCombatlog",
                "DisablePortraitIndicator",
            ],
        ))

    def __str__(self) -> str:
        return self.__name
