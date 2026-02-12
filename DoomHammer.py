from moddb import character_level_range
from modtools.gamedata import PassiveData, Weapon
from modtools.replacers import Mod

import os


class DoomHammer(Mod):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="DoomHammer",
                         description="Level-up progression for the Doom Hammer.",
                         **kwds)

        self.add(character_level_range)

        bonus_damage_type = "Necrotic"

        lethal_weapon = self.make_name("LethalWeapon")

        self.loca[f"{lethal_weapon}_Description"] = f"""
            This weapon ignores Bludgeoning and {bonus_damage_type} <LSTag Tooltip="Resistant">Resistance</LSTag>.
            """

        self.add(PassiveData(
            lethal_weapon,
            using="MAG_IgnoreBludgeoningResistance_Passive",
            Description=self.loca[f"{lethal_weapon}_Description"],
            Boosts=[
                "IgnoreResistance(Bludgeoning,Resistant)",
                f"IgnoreResistance({bonus_damage_type},Resistant)",
            ],
        ))

        self.add(Weapon(
            "UNI_DoomHammer",
            using="UNI_DoomHammer",
            DefaultBoosts=[
                "WeaponProperty(Magical)",
                "IF(CharacterLevelRange(5,8)):WeaponEnchantment(1)",
                "IF(CharacterLevelRange(9,12)):WeaponEnchantment(2)",
                "IF(CharacterLevelRange(13,20)):WeaponEnchantment(3)",
                f"IF(CharacterLevelRange(5,8)):WeaponDamage(1d4,{bonus_damage_type})",
                f"IF(CharacterLevelRange(9,12)):WeaponDamage(1d6,{bonus_damage_type})",
                f"IF(CharacterLevelRange(13,16)):WeaponDamage(1d8,{bonus_damage_type})",
                f"IF(CharacterLevelRange(17,20)):WeaponDamage(1d10,{bonus_damage_type})",
            ],
            PassivesOnEquip=[
                "UNI_DoomAxe_Passive",
                lethal_weapon,
            ],
            Rarity="Legendary",
        ))


if __name__ == "__main__":
    doom_hammer = DoomHammer()
    doom_hammer.build()