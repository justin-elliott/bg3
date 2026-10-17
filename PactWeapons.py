#!/usr/bin/env python3

from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar, Iterable
from uuid import UUID

from moddb import (
    Awareness,
    BattleMagic,
    Bolster,
    ElementalWeapon,
    Knowledge,
    storm_bolts,
)
from modtools.gamedata import (
    Armor,
    InterruptData,
    ObjectData,
    PassiveData,
    SpellData,
    StatusData,
    Weapon,
)
from modtools.lsx.game import GameObjects
from modtools.replacers import Mod
from modtools.text import ItemCombinations, TreasureTable

import os


class PactWeapons(Mod):
    __KATANA_TEMPLATE_ID: ClassVar[UUID] = UUID("7050c02e-f0e1-46b8-9400-2514805ecd2e")

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="PactWeapons",
                         description="Enhancements to Warlock Pact weapons.",
                         **kwds)

        for wpn in ["Battleaxe", "Glaive", "Greatsword", "Rapier", "Trident", "Warhammer", "Sickle", "Flail", "Maul"]:
            name = f"WPN_{wpn}_Pact"
            self.add(Weapon(
                name,
                using=name,
                RootTemplate=self.__KATANA_TEMPLATE_ID if wpn == "Greatsword" else None,
                Boosts=self._weapon_boosts(wpn),
            ))

    def _weapon_boosts(self, weapon: str) -> list[str]:
        return [
            f"Proficiency({weapon}s)",
            "IF(CharacterLevelGreaterThan(2) and not CharacterLevelGreaterThan(6)):WeaponEnchantment(1)",
            "IF(CharacterLevelGreaterThan(2) and not CharacterLevelGreaterThan(6)):WeaponDamage(1d4,Force)",
            "IF(CharacterLevelGreaterThan(6) and not CharacterLevelGreaterThan(10)):WeaponEnchantment(2)",
            "IF(CharacterLevelGreaterThan(6) and not CharacterLevelGreaterThan(10)):WeaponDamage(1d6,Force)",
            "IF(CharacterLevelGreaterThan(10)):WeaponEnchantment(3)",
            "IF(CharacterLevelGreaterThan(10)):WeaponDamage(1d8,Force)",
        ]

if __name__ == "__main__":
    pact_weapons = PactWeapons()
    pact_weapons.build()