from moddb import character_level_range
from modtools.gamedata import PassiveData, SpellData, Weapon
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

        lethal_weapon = self.make_name("LethalWeapon")
        shockwave = self.make_name("Shockwave")

        self.add(PassiveData(
            lethal_weapon,
            using="MAG_IgnoreBludgeoningResistance_Passive",
            Description=self.loca(f"{lethal_weapon}_Description", """
                This weapon ignores Bludgeoning <LSTag Tooltip="Resistant">Resistance</LSTag>.
            """),
            Boosts=[
                "IgnoreResistance(Bludgeoning,Resistant)",
            ],
        ))

        self.add(PassiveData(
            shockwave,
            DisplayName=self.loca(f"{shockwave}_DisplayName", "Shockwave"),
            Description=self.loca(f"{shockwave}_Description", """
                You deal an additional [1] to nearby enemies, possibly knocking them
                <LSTag Type="Status" Tooltip="PRONE">Prone</LSTag>.
            """),
            DescriptionParams=["DealDamage(1d4,Bludgeoning)"],
            StatsFunctorContext="OnDamage",
            Conditions=[
                "AttackedWithPassiveSourceWeapon() " +
                "and not IsMiss() " +
                "and not IsCriticalMiss() " +
                "and Character() " +
                "and Enemy()",
            ],
            StatsFunctors=[f"CreateExplosion({shockwave}_Explosion)"],
        ))

        self.add(SpellData(
            f"{shockwave}_Explosion",
            SpellType="Projectile",
            using="Projectile_UND_DuergarRaft_Hammer_Explosion",
            SpellSuccess=["ApplyStatus(PRONE,100,2)", "DealDamage(1d4,Bludgeoning,Magical)"],
            SpellFail=["DealDamage(1d4,Bludgeoning,Magical)"],
        ))

        self.add(Weapon(
            "UNI_DoomHammer",
            using="UNI_DoomHammer",
            Damage="1d12",
            DefaultBoosts=[
                "WeaponProperty(Magical)",
                "IF(CharacterLevelRange(5,8)):WeaponEnchantment(1)",
                "IF(CharacterLevelRange(9,12)):WeaponEnchantment(2)",
                "IF(CharacterLevelRange(13,20)):WeaponEnchantment(3)",
            ],
            PassivesOnEquip=[
                "UNI_DoomAxe_Passive",
                "MAG_WYR_Orin_Bhaalist_Dagger_ImprovedCritical_Passive",
                lethal_weapon,
                shockwave,
            ],
            Rarity="Legendary",
        ))


if __name__ == "__main__":
    doom_hammer = DoomHammer()
    doom_hammer.build()