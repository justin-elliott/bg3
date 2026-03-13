#!/usr/bin/env python3
"""
Once per rest Elemental Weapon for Baldur's Gate 3 mods.
"""

from modtools.gamedata import SpellData, StatusData
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
        status_name = self._mod.make_name("ELEMENTAL_WEAPON")

        self._mod.loca[f"{name}_Description"] = """
            Imbue a weapon with elemental power. It receives a +[1] bonus to
            <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>, and deals an additional 1d4 damage of your choice.
            The weapon can't be knocked out of the wielder's hand, and automatically returns to the wielder when
            <LSTag Type="Spell" Tooltip="Throw_Throw">Thrown</LSTag>.
        """
        self._mod.add(SpellData(
            name,
            using="Target_ElementalWeapon",
            Description=self._mod.loca[f"{name}_Description"],
            SpellType="Target",
            ContainerSpells=[f"{name}_{element}" for element in self._ELEMENTS],
            Cooldown="",
            UseCosts="ActionPoint:1",
            SpellFlags=["HasVerbalComponent", "HasSomaticComponent", "IsSpell", "IsMelee", "IsLinkedSpellContainer"],
        ))

        self._mod.loca[f"{status_name}_Description"] = """
            Has a +[1] bonus to <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag> and deals an additional [2].
            The weapon can't be knocked out of the wielder's hand, and automatically returns to the wielder when
            <LSTag Type="Spell" Tooltip="Throw_Throw">Thrown</LSTag>.
        """

        for element in self._ELEMENTS:
            self._mod.loca[f"{name}_{element}_Description"] = """
                Imbue a weapon with elemental power. It receives a +[1] bonus to
                <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>, and deals an additional [2].
                The weapon can't be knocked out of the wielder's hand, and automatically returns to the wielder when
                <LSTag Type="Spell" Tooltip="Throw_Throw">Thrown</LSTag>.
            """
            self._mod.add(SpellData(
                f"{name}_{element}",
                using=f"Target_ElementalWeapon_{element}",
                Description=self._mod.loca[f"{name}_{element}_Description"],
                DescriptionParams=["1", f"DealDamage(1d4,{element})"],
                SpellType="Target",
                SpellContainerID=name,
                SpellProperties=[
                    f"IF(Item()):ApplyStatus({status_name}_{element.upper()}_MAIN,100,-1)",
                    f"IF(not Item()):ApplyEquipmentStatus(MainHand,{status_name}_{element.upper()}_MAIN,100,-1)",
                    f"IF(not Item()):ApplyEquipmentStatus(OffHand,{status_name}_{element.upper()}_OFF,100,-1)",
                ],
                Cooldown="OncePerRestPerItem",
                UseCosts="ActionPoint:1",
                SpellFlags=["HasVerbalComponent", "HasSomaticComponent", "IsSpell", "IsMelee"],
            ))

            self._mod.add(StatusData(
                f"{status_name}_{element.upper()}_MAIN",
                using=f"ELEMENTAL_WEAPON_{element.upper()}",
                StatusType="BOOST",
                Description=self._mod.loca[f"{status_name}_Description"],
                Boosts=[
                    "WeaponProperty(Magical)",
                    "CannotBeDisarmed()",
                    "ItemReturnToOwner()",
                    "Attribute(InventoryBound)",
                    "WeaponAttackRollBonus(1)",
                    f"WeaponDamage(1d4,{element})",
                ],
                StackId=f"{status_name}_MAIN",
                IsUnique="1",
            ))

            self._mod.add(StatusData(
                f"{status_name}_{element.upper()}_OFF",
                using=f"{status_name}_{element.upper()}_MAIN",
                StatusType="BOOST",
                StackId=f"{status_name}_OFF",
            ))

        return name
