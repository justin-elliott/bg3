#!/usr/bin/env python3
"""
Once per rest Elemental Weapon for Baldur's Gate 3 mods.
"""

from modtools.gamedata import SpellData
from modtools.mod import Mod
from typing import ClassVar

class ElementalWeapon:
    """Adds the Elemental Weapon spell to a Baldur's Gate 3 mod."""
    _ELEMENTS: ClassVar[list[str]] = ["Acid", "Cold", "Fire", "Lightning", "Thunder"]

    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    def add_elemental_weapon(self) -> str:
        name = self._mod.make_name("ElementalWeapon")
        self._mod.add(SpellData(
            name,
            using="Target_ElementalWeapon",
            SpellType="Target",
            ContainerSpells=[f"{name}_{element}" for element in self._ELEMENTS],
            Cooldown="OncePerRestPerItem",
            UseCosts="ActionPoint:1",
            SpellFlags=["HasVerbalComponent", "HasSomaticComponent", "IsSpell", "IsMelee", "IsLinkedSpellContainer"],
        ))
        for element in self._ELEMENTS:
            self._mod.add(SpellData(
                f"{name}_{element}",
                using=f"Target_ElementalWeapon_{element}",
                SpellType="Target",
                SpellContainerID=name,
                SpellProperties=[
                    f"IF(Item()):ApplyStatus(ELEMENTAL_WEAPON_{element.upper()},100,-1)",
                    f"IF(not Item()):ApplyEquipmentStatus(MainHand,ELEMENTAL_WEAPON_{element.upper()},100,-1)",
                    f"IF(not Item()):ApplyEquipmentStatus(OffHand,ELEMENTAL_WEAPON_{element.upper()},100,-1)",
                ],
                Cooldown="OncePerRestPerItem",
                UseCosts="ActionPoint:1",
                SpellFlags=["HasVerbalComponent", "HasSomaticComponent", "IsSpell", "IsMelee"],
            ))
        return name
