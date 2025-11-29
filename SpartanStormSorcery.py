
import os

from functools import cached_property
from moddb import character_level_range, Defense, EmpoweredSpells
from modtools.gamedata import Armor, ObjectData, PassiveData, SpellData, StatusData, Weapon
from modtools.lsx.game import CharacterAbility, Dependencies, GameObjects, Progression, ProgressionDescription, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)
from modtools.text import Equipment, TreasureTable


class SpartanStormSorcery(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="SpartanStormSorcery",
                         description="A class replacer for StormSorcery.",
                         **kwds)

        self._mod.add(Dependencies.ShortModuleDesc(
            Folder="SPRtnarmr_dc350aa5-ddc0-5d9a-07a9-65e77a7ac82f",
            MD5="33c5be4ed131380bbf5d0213c73b9323",
            Name="Spartan Warrior Set",
            PublishHandle=5219033,
            UUID="dc350aa5-ddc0-5d9a-07a9-65e77a7ac82f",
            Version64=36028797018963972,
        ))

        self.mod.add(character_level_range)
        self._add_starting_equipment()
        self._add_treasure_table()


    @cached_property
    def _empowered_spells(self) -> str:
        return EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.CHARISMA)

    @cached_property
    def _unarmored_defense(self) -> str:
        return Defense(self.mod).add_unarmored_defense(CharacterAbility.CHARISMA)

    def _weapon_boosts(self, damage_type: str, die_sides: int) -> list[str]:
        return [
            "WeaponProperty(Magical)",
            "CannotBeDisarmed()",
            "ItemReturnToOwner()",
            "IF(CharacterLevelRange(1,4)):WeaponEnchantment(1)",
            "IF(CharacterLevelRange(5,8)):WeaponEnchantment(2)",
            "IF(CharacterLevelRange(9,20)):WeaponEnchantment(3)",
            f"IF(CharacterLevelRange(5,8)):WeaponDamage(1d{die_sides},{damage_type},Magical)",
            f"IF(CharacterLevelRange(9,12)):WeaponDamage(2d{die_sides},{damage_type},Magical)",
            f"IF(CharacterLevelRange(13,16)):WeaponDamage(3d{die_sides},{damage_type},Magical)",
            f"IF(CharacterLevelRange(17,20)):WeaponDamage(4d{die_sides},{damage_type},Magical)",
        ]

    @cached_property
    def _armor_body(self) -> str:
        name = f"{self.mod.get_prefix()}_Body"
        self.mod.add(Armor(
            name,
            using="ARM_SPR_Body",
            PassivesOnEquip=[
                self._unarmored_defense,
            ],
        ))
        return name

    @cached_property
    def _armor_boots(self) -> str:
        name = f"{self.mod.get_prefix()}_Boots"
        self.mod.add(Armor(
            name,
            using="ARM_SPR_Boots",
        ))
        return name

    @cached_property
    def _armor_cloak(self) -> str:
        name = f"{self.mod.get_prefix()}_Cloak"
        self.mod.add(Armor(
            name,
            using="ARM_SPR_Cloak",
        ))
        return name

    @cached_property
    def _armor_gloves(self) -> str:
        name = f"{self.mod.get_prefix()}_Gloves"
        self.mod.add(Armor(
            name,
            using="ARM_SPR_Gloves",
        ))
        return name

    @cached_property
    def _armor_helm(self) -> str:
        name = f"{self.mod.get_prefix()}_Helm"
        self.mod.add(Armor(
            name,
            using="ARM_SPR_Headwear",
            ArmorType="Cloth",
            Proficiency_Group="",
        ))
        return name

    @cached_property
    def _camp_body(self) -> str:
        name = f"{self.mod.get_prefix()}_CampBody"
        self.mod.add(Armor(
            name,
            using="CAMP_SPR_Set_No_Cloak",
        ))
        return name

    @cached_property
    def _camp_body_cloak(self) -> str:
        name = f"{self.mod.get_prefix()}_CampBodyCloak"
        self.mod.add(Armor(
            name,
            using="CAMP_SPR_Set",
        ))
        return name

    @cached_property
    def _camp_boots(self) -> str:
        name = f"{self.mod.get_prefix()}_CampBoots"
        self.mod.add(Armor(
            name,
            using="CAMP_SPR_Boots",
        ))
        return name

    @cached_property
    def _camp_helm(self) -> str:
        name = f"{self.mod.get_prefix()}_CampHelm"
        self.mod.add(Armor(
            name,
            using="CAMP_SPR_Headwear",
        ))
        return name

    @cached_property
    def _shield(self) -> str:
        name = f"{self.mod.get_prefix()}_Shield"
        self.mod.add(Weapon(
            name,
            using="WPN_SPR_Shield",
            DefaultBoosts=self._weapon_boosts("Bludgeoning", 4),
        ))
        return name
    
    @cached_property
    def _shortsword(self) -> str:
        name = f"{self.mod.get_prefix()}_Shortsword"
        self.mod.add(Weapon(
            name,
            using="WPN_SPR_Shortsword",
            DefaultBoosts=self._weapon_boosts("Piercing", 4),
            PassivesOnEquip=[],
        ))
        return name

    @cached_property
    def _spear_instrument(self) -> str:
        name = f"{self.mod.get_prefix()}_SpearInstrument"
        self.mod.add(Armor(
            name,
            using="INS_SPR_Spear",
            Boosts=[
                "Proficiency(MusicalInstrument)",
                "UnlockSpell(Shout_Bard_Perform_Whistle)",
            ],
        ))
        return name

    def _add_starting_equipment(self) -> None:
        self.mod.add(Equipment(f"""
            new equipment "EQP_CC_Sorcerer_StormSorcery"
            add initialweaponset "Melee"
            add equipmentgroup
            add equipment entry "{self._shortsword}"
            add equipmentgroup
            add equipment entry "{self._shield}"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "{self._armor_body}"
            add equipmentgroup
            add equipment entry "{self._armor_boots}"
            add equipmentgroup
            add equipment entry "{self._armor_cloak}"
            add equipmentgroup
            add equipment entry "{self._armor_gloves}"
            add equipmentgroup
            add equipment entry "{self._spear_instrument}"
            add equipmentgroup
            add equipment entry "OBJ_Scroll_Revivify"
            add equipmentgroup
            add equipment entry "OBJ_Scroll_Revivify"
            add equipmentgroup
            add equipment entry "OBJ_Scroll_Revivify"
            add equipmentgroup
            add equipment entry "OBJ_Keychain"
            add equipmentgroup
            add equipment entry "OBJ_Bag_AlchemyPouch"
            add equipmentgroup
            add equipment entry "{self._camp_body_cloak}"
            add equipmentgroup
            add equipment entry "{self._camp_boots}"
            add equipmentgroup
            add equipment entry "OBJ_Backpack_CampSupplies"
        """))
    
    def _add_container(self, name: str, *, display_name: str, description: str) -> None:
        container_uuid = self.make_uuid(name)

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": display_name}
        loca[f"{name}_Description"] = {"en": description}

        self.mod.add(GameObjects(
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="Item_CONT_GEN_Chest_Travel_A_Small_A",
            LevelName="",
            MapKey=container_uuid,
            Name=name,
            ParentTemplateId="47805d79-88f1-4933-86eb-f78f67cbc33f",
            Stats=name,
            Type="item",
            children=[
                GameObjects.InventoryList(children=[
                    GameObjects.InventoryList.InventoryItem(
                        Object=f"{name}_TreasureTable",
                    ),
                ]),
            ],
        ))

        self.mod.add(ObjectData(
            name,
            using="_Container",
            RootTemplate=container_uuid,
            Weight=0.01,
        ))

    def _add_treasure_table(self) -> None:
        container_name = f"{self.mod.get_prefix()}_Chest"
        self._add_container(container_name,
                            display_name="Storm Sorcerer's Spartan Gear",
                            description="""
                                Forged from blackened steel and reinforced with storm-weathered oak, this heavy chest
                                bears the mark of a Spartan Storm Sorcerer. Its lid is secured by robust iron clasps,
                                etched with subtle, angular lightning bolts that hint at the raw power contained within.
                            """)

        self.mod.add(TreasureTable(f"""
            new treasuretable "TUT_Chest_Potions"
            CanMerge 1
            new subtable "1,1"
            object category "I_{container_name}",1,0,0,0,0,0,0,0
        """))

        self.mod.add(TreasureTable(f"""
            new treasuretable "{container_name}_TreasureTable"
            CanMerge 1
            new subtable "1,1"
            object category "I_{self._armor_helm}",1,0,0,0,0,0,0,0
            new subtable "1,1"
            object category "I_{self._camp_body}",1,0,0,0,0,0,0,0
            new subtable "1,1"
            object category "I_{self._camp_helm}",1,0,0,0,0,0,0,0
        """))

    @progression(CharacterClass.SORCERER_STORM, 1)
    def spartan_level_1(self, progress: Progression) -> None:
        hp_boost = "IncreaseMaxHP(ClassLevel(Sorcerer)*2)"

        progress.Boosts = [hp_boost]
        progress.PassivesAdded = ["DevilsSight"]
        progress.Selectors = [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d)",  # Fly
        ]

        hp_boost_name = f"{self.mod.get_prefix()}_HPBoost"
        loca = self.mod.get_localization()
        loca[f"{hp_boost_name}_DisplayName"] = {"en": "Storm Sorcery: Hit Points"}
        loca[f"{hp_boost_name}_Description"] = {"en": """
            Your <LSTag Tooltip="HitPoints">hit point</LSTag> maximum increases by 2 for each Sorcerer level.
        """}

        self.mod.add(ProgressionDescription(
            DisplayName=loca[f"{hp_boost_name}_DisplayName"],
            Description=loca[f"{hp_boost_name}_Description"],
            ExactMatch=hp_boost,
            ProgressionId=progress.UUID,
            UUID=self.make_uuid(hp_boost),
        ))

    @progression(CharacterClass.SORCERER_STORM, 2)
    def spartan_level_2(self, progress: Progression) -> None:
        progress.PassivesAdded = ["JackOfAllTrades", "SculptSpells"]
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.SORCERER_STORM, 3)
    def spartan_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ImprovedCritical"]

    @progression(CharacterClass.SORCERER_STORM, 4)
    def spartan_level_4(self, progress: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 5)
    def spartan_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["UncannyDodge"]

    @progression(CharacterClass.SORCERER_STORM, 6)
    def spartan_level_6(self, progress: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 7)
    def spartan_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = ["Evasion"]

    @progression(CharacterClass.SORCERER_STORM, 8)
    def spartan_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 9)
    def spartan_level_9(self, progress: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 10)
    def spartan_level_10(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._empowered_spells]

    @progression(CharacterClass.SORCERER_STORM, 11)
    def spartan_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded += ["ReliableTalent"]

    @progression(CharacterClass.SORCERER_STORM, 12)
    def spartan_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 13)
    def spartan_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 14)
    def spartan_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 15)
    def spartan_level_15(self, progress: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 16)
    def spartan_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 17)
    def spartan_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 18)
    def spartan_level_18(self, progress: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 19)
    def spartan_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 20)
    def spartan_level_20(self, progress: Progression) -> None:
        raise DontIncludeProgression()


def main() -> None:
    spartan = SpartanStormSorcery(
        classes=[CharacterClass.SORCERER_STORM],
    )
    spartan.build()


if __name__ == "__main__":
    main()
