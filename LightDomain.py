
from functools import cached_property
import os

from moddb import BattleMagic, Bolster, Movement
from modtools.gamedata import Armor, PassiveData, SpellData
from modtools.lsx.game import (
    ClassDescription,
    GameObjects,
    Progression,
    SpellList,
)
from modtools.replacers import (
    CharacterClass,
    class_description,
    DontIncludeProgression,
    progression,
    Replacer,
)
from modtools.text import Equipment, Script


class LightDomain(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="LightDomain",
                         description="A class replacer for LightDomain.",
                         **kwds)

        self.mod.add(Script(f"""
            -- Test for a Cleric cantrip.
            function IsClericCantrip()
                return SpellId('Target_SacredFlame')
                | SpellId('Target_TollTheDead')
                | SpellId('Target_BurstingSinew')
                | SpellId('{self._twinned_firebolt}')
            end
        """))

    @cached_property
    def _equipment(self) -> str:
        name = f"{self.mod.get_prefix()}_Equipment"

        self.mod.add(Equipment(f"""
            new equipment "EQP_CC_Cleric_LightDomain"
            add initialweaponset "Melee"
            add equipmentgroup
            add equipment entry "WPN_Mace"
            add equipmentgroup
            add equipment entry "OBJ_Scroll_Revivify"
            add equipmentgroup
            add equipment entry "ARM_Shield"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "ARM_Boots_Leather"
            add equipmentgroup
            add equipment entry "ARM_ChainShirt_Body"
            add equipmentgroup
            add equipment entry "{self._ring_of_hill_giant_strength}"
            add equipmentgroup
            add equipment entry "OBJ_Scroll_Revivify"
            add equipmentgroup
            add equipment entry "OBJ_Keychain"
            add equipmentgroup
            add equipment entry "OBJ_Bag_AlchemyPouch"
            add equipmentgroup
            add equipment entry "ARM_Camp_Body"
            add equipmentgroup
            add equipment entry "ARM_Camp_Shoes"
            add equipmentgroup
            add equipment entry "OBJ_Backpack_CampSupplies"
        """))

        return name

    @cached_property
    def _ring_of_hill_giant_strength(self) -> str:
        name = f"{self.mod.get_prefix()}_RingOfHillGiantStrength"

        strength = "22"
        damage_bonus = "DamageBonus(1d4,Bludgeoning)"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Ring of Hill Giant Strength"}
        loca[f"{name}_Description"] = {"en": f"""
            This crudely hammered bronze band is surprisingly heavy, resonating with a faint, earthy tremor that grants
            the wearer the raw, unrefined might of a hill giant.
        """}

        ring_uuid = self.mod.make_uuid(name)
        self.mod.add(GameObjects(
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            LevelName="",
            MapKey=ring_uuid,
            ParentTemplateId="1abd032b-c138-45ee-b85e-62b5bbb6ea2d",
            Name=name,
            Stats=name,
            Type="item",
        ))

        hill_giant_strength = f"{self.mod.get_prefix()}_HillGiantStrength"
        heavy_blows = f"{self.mod.get_prefix()}_HeavyBlows"

        self.mod.add(Armor(
            name,
            using="_Ring_Magic",
            PassivesOnEquip=[hill_giant_strength, heavy_blows],
            Rarity="VeryRare",
        ))

        loca[f"{hill_giant_strength}_DisplayName"] = {"en": "Hill Giant Strength"}
        loca[f"{hill_giant_strength}_Description"] = {"en": f"""
            Your <LSTag Tooltip="Strength">Strength</LSTag> increases to [1].
        """}

        self.mod.add(PassiveData(
            hill_giant_strength,
            DisplayName=loca[f"{hill_giant_strength}_DisplayName"],
            Description=loca[f"{hill_giant_strength}_Description"],
            DescriptionParams=[strength],
            Boosts=[f"AbilityOverrideMinimum(Strength,{strength})"]
        ))

        loca[f"{heavy_blows}_DisplayName"] = {"en": "Heavy Blows"}
        loca[f"{heavy_blows}_Description"] = {"en": f"""
            Your melee weapon and unarmed attacks deal an additional [1].
        """}

        self.mod.add(PassiveData(
            heavy_blows,
            DisplayName=loca[f"{heavy_blows}_DisplayName"],
            Description=loca[f"{heavy_blows}_Description"],
            DescriptionParams=[damage_bonus],
            Boosts=[f"IF(IsMeleeWeaponAttack() or IsMeleeUnarmedAttack()):{damage_bonus}"]
        ))

        return name

    @cached_property
    def _battle_magic(self) -> str:
        return BattleMagic(self.mod).add_battle_magic()

    @cached_property
    def _bolster(self) -> str:
        return Bolster(self.mod).add_bolster()

    @cached_property
    def _misty_step(self) -> str:
        return Movement(self.mod).add_misty_step()

    @cached_property
    def _twinned_firebolt(self) -> str:
        name = f"{self.mod.get_prefix()}_TwinnedFireBolt"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Twinned Fire Bolt"}
        loca[f"{name}_Description"] = {"en": "Hurl two motes of fire."}

        self.mod.add(SpellData(
            name,
            using="Projectile_FireBolt",
            SpellType="Projectile",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            AmountOfTargets="2",
        ))
        return name

    @cached_property
    def _level_1_spell_list(self) -> str:
        name = "Light Domain Cleric Additional Level 1 Spell List"
        uuid = self.make_uuid(name)
        self.mod.add(SpellList(
            Name=name,
            Spells=[self._bolster, self._twinned_firebolt],
            UUID=uuid,
        ))
        return uuid

    @cached_property
    def _level_5_spell_list(self) -> str:
        name = "Light Domain Cleric Additional Level 5 Spell List"
        uuid = self.make_uuid(name)
        self.mod.add(SpellList(
            Name=name,
            Spells=["Target_Counterspell", self._misty_step],
            UUID=uuid,
        ))
        return uuid

    @class_description(CharacterClass.CLERIC_LIGHT)
    def lightdomain_class_description(self, desc: ClassDescription) -> None:
        desc.ClassEquipment = self._equipment

    @progression(CharacterClass.CLERIC_LIGHT, 1)
    def lightdomain_level_1(self, progress: Progression) -> None:
        progress.Boosts = [
            "ProficiencyBonus(SavingThrow,Constitution)",
            "Proficiency(HeavyArmor)",
            "Proficiency(MartialWeapons)",
        ]
        progress.PassivesAdded += [self._battle_magic]
        progress.Selectors += [
            f"AddSpells({self._level_1_spell_list},ClericLightDomainSpells,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_LIGHT, 2)
    def lightdomain_level_2(self, progress: Progression) -> None:
        progress.PassivesAdded = ["JackOfAllTrades", "SculptSpells"]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.CLERIC_LIGHT, 3)
    def lightdomain_level_3(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 4)
    def lightdomain_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 5)
    def lightdomain_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack"]
        progress.Selectors += [
            f"AddSpells({self._level_5_spell_list},ClericLightDomainSpells,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_LIGHT, 6)
    def lightdomain_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 7)
    def lightdomain_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 8)
    def lightdomain_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 9)
    def lightdomain_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 10)
    def lightdomain_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 11)
    def lightdomain_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2"]
        progress.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.CLERIC_LIGHT, 12)
    def lightdomain_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 13)
    def lightdomain_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 14)
    def lightdomain_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 15)
    def lightdomain_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 16)
    def lightdomain_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 17)
    def lightdomain_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 18)
    def lightdomain_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 19)
    def lightdomain_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 20)
    def lightdomain_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]


def main() -> None:
    light_domain = LightDomain(
        classes=[CharacterClass.CLERIC_LIGHT],
        feats=2,
        spells=2,
        actions=2,
    )
    light_domain.build()


if __name__ == "__main__":
    main()
