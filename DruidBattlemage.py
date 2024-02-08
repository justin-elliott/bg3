#!/usr/bin/env python3
"""
Generates files for the "DruidBattlemage" mod.
"""

import os

from moddb.battlemagic import BattleMagic
from moddb.bolster import Bolster
from moddb.empoweredspells import EmpoweredSpells
from moddb.movement import Movement
from moddb.progression import allow_improvement, multiply_resources
from moddb.scripts import character_level_range
from modtools.gamedata import PassiveData, StatusData, Weapon
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
)
from modtools.lsx.game import GameObjects, Progression, SpellList
from modtools.mod import Mod
from modtools.progressionreplacer import class_description, class_level, ProgressionReplacer
from typing import Iterable
from uuid import UUID


def natural_resistance(mod: Mod) -> str:
    """Add the Natural Resistance passive, returning its name."""
    name = f"{mod.get_prefix()}_NaturalResistance"

    loca = mod.get_localization()
    loca[f"{name}_DisplayName"] = {"en": "Natural Resistance"}
    loca[f"{name}_Description"] = {"en": """
        You are naturally resistant to all forms of damage. Incoming damage is reduced by [1].
        """}

    mod.add(PassiveData(
        name,
        DisplayName=loca[f"{name}_DisplayName"],
        Description=loca[f"{name}_Description"],
        DescriptionParams=["RegainHitPoints(max(1,ClassLevel(Druid)))"],
        Icon="PassiveFeature_Durable",
        Properties=["Highlighted"],
        Boosts=["DamageReduction(All,Flat,ClassLevel(Druid))"],
    ))

    return name


def add_equipment(mod: Mod, equipment_set_name: str) -> None:
    prefix = mod.get_prefix()
    loca = mod.get_localization()

    # Weapon effect
    mod.add(StatusData(
        f"{prefix}_Scimitar_LightningEffect",
        StatusType="EFFECT",
        DisplayName="h363588c6g20b9g4407g91d8gebab0f1a5dca;1",
        StatusPropertyFlags=["IgnoreResting", "DisableCombatlog", "DisableOverhead", "DisablePortraitIndicator"],
        StatusEffect="7905bb82-0284-46b8-855b-24f17560fe4a",
    ))

    # scimitar_a_0_uuid = UUID("868217db-9dcb-414c-bb88-e321ab3e0349")
    scimitar_a_1_uuid = UUID("7cc7a0e1-d0b8-4569-afb2-d538e8941894")
    # scimitar_a_2_uuid = UUID("5193af64-48c1-406f-90bf-87f7f01b4684")
    # scimitar_momentum_on_attack = UUID("4456e2ec-ba1f-4f53-aab8-847249cabc09")
    # scimitar_the_clover = UUID("517231eb-e812-43ed-9ce3-482ba7ed31e6")

    tempest_uuid = mod.make_uuid(f"{prefix}_Tempest")

    loca[f"{prefix}_Tempest_DisplayName"] = {"en": "Tempest"}
    loca[f"{prefix}_Tempest_Description"] = {"en": """
        Sparks of electrical energy dance along the length of the blade.
        """}

    mod.add(GameObjects(
        DisplayName=loca[f"{prefix}_Tempest_DisplayName"],
        Description=loca[f"{prefix}_Tempest_Description"],
        LevelName="",
        MapKey=tempest_uuid,
        Name=f"{prefix}_Tempest",
        ParentTemplateId=scimitar_a_1_uuid,
        Stats=f"{prefix}_Tempest",
        Type="item",
        children=[
            GameObjects.StatusList(
                children=[
                    GameObjects.StatusList.Status(Object=f"{prefix}_Scimitar_LightningEffect"),
                ],
            ),
        ],
    ))

    thunder_uuid = mod.make_uuid(f"{prefix}_Thunder")

    loca[f"{prefix}_Thunder_DisplayName"] = {"en": "Thunder"}
    loca[f"{prefix}_Thunder_Description"] = {"en": """
        Sparks of electrical energy crash along the length of the blade.
        """}

    mod.add(GameObjects(
        DisplayName=loca[f"{prefix}_Thunder_DisplayName"],
        Description=loca[f"{prefix}_Thunder_Description"],
        LevelName="",
        MapKey=thunder_uuid,
        Name=f"{prefix}_Thunder",
        ParentTemplateId=scimitar_a_1_uuid,
        Stats=f"{prefix}_Thunder",
        Type="item",
        children=[
            GameObjects.StatusList(
                children=[
                    GameObjects.StatusList.Status(Object=f"{prefix}_Scimitar_LightningEffect"),
                ],
            ),
        ],
    ))

    mod.add_script(character_level_range)

    mod.add(Weapon(
        f"{prefix}_Tempest",
        using="WPN_Scimitar",
        RootTemplate=tempest_uuid,
        Rarity="Legendary",
        Damage="1d6",
        DefaultBoosts=[
            "CannotBeDisarmed()",
            "WeaponProperty(Magical)",
            "IF(CharacterLevelRange(1,5)):WeaponEnchantment(1)",
            "IF(CharacterLevelRange(6,10)):WeaponEnchantment(2)",
            "IF(CharacterLevelRange(11,20)):WeaponEnchantment(3)",
            "IF(CharacterLevelRange(1,5)):WeaponDamage(1d4,Lightning,Magical)",
            "IF(CharacterLevelRange(6,10)):WeaponDamage(2d4,Lightning,Magical)",
            "IF(CharacterLevelRange(11,20)):WeaponDamage(3d4,Lightning,Magical)",
        ],
        PassivesOnEquip=[
            "MAG_ChargedLightning_Charge_OnDamage_Passive",
            "MAG_TheClover_Rearrangement_Passive",
        ],
        Weapon_Properties=[
            "Dippable",
            "Finesse",
            "Light",
            "Magical",
            "Melee",
        ],
    ))

    mod.add(Weapon(
        f"{prefix}_Thunder",
        using="WPN_Scimitar",
        RootTemplate=thunder_uuid,
        Rarity="Legendary",
        Damage="1d6",
        DefaultBoosts=[
            "CannotBeDisarmed()",
            "WeaponProperty(Magical)",
            "IF(CharacterLevelRange(1,5)):WeaponEnchantment(1)",
            "IF(CharacterLevelRange(6,10)):WeaponEnchantment(2)",
            "IF(CharacterLevelRange(11,20)):WeaponEnchantment(3)",
            "IF(CharacterLevelRange(1,5)):WeaponDamage(1d4,Thunder,Magical)",
            "IF(CharacterLevelRange(6,10)):WeaponDamage(2d4,Thunder,Magical)",
            "IF(CharacterLevelRange(11,20)):WeaponDamage(3d4,Thunder,Magical)",
        ],
        PassivesOnEquip=[
            f"{prefix}_Clash",
            "MAG_ArcaneEnchantment_Lesser_Passive",
        ],
        Weapon_Properties=[
            "Dippable",
            "Finesse",
            "Light",
            "Magical",
            "Melee",
        ],
    ))

    loca[f"{prefix}_Clash_DisplayName"] = {"en": "Clash"}
    loca[f"{prefix}_Clash_Description"] = {"en": """
        When the wielder deals damage using this weapon, they inflict [1] turns of
        <LSTag Type="Status" Tooltip="MAG_THUNDER_REVERBERATION">Reverberation</LSTag> upon the target(s).
        """}

    mod.add(PassiveData(
        f"{prefix}_Clash",
        DisplayName=loca[f"{prefix}_Clash_DisplayName"],
        Description=loca[f"{prefix}_Clash_Description"],
        DescriptionParams=["2"],
        Properties=["OncePerAttack"],
        StatsFunctorContext=["OnDamage"],
        Conditions=["AttackedWithPassiveSourceWeapon()"],
        StatsFunctors=[
            "ApplyStatus(MAG_THUNDER_REVERBERATION,100,2)",
            "ApplyStatus(MAG_THUNDER_REVERBERATION_DURATION_TECHNICAL,100,1)",
        ],
    ))

    mod.add_equipment(f"""\
    new equipment "{equipment_set_name}"
    add initialweaponset "Melee"
    add equipmentgroup
    add equipment entry "{prefix}_Tempest"
    add equipmentgroup
    add equipment entry "{prefix}_Thunder"
    add equipmentgroup
    add equipment entry "ARM_Leather_Body_Druid"
    add equipmentgroup
    add equipment entry "ARM_Boots_Leather_Druid"
    add equipmentgroup
    add equipment entry "OBJ_Potion_Healing"
    add equipmentgroup
    add equipment entry "OBJ_Potion_Healing"
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
    """)


class DruidBattlemage(ProgressionReplacer):
    _EQUIPMENT_SET_NAME = "EQP_CC_DruidBattlemage"

    _battle_magic: str
    _bolster: str
    _empowered_spells: str
    _fast_movement: str
    _natural_resistance: str
    _level_1_spelllist: str
    _level_5_spelllist: str

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="DruidBattlemage",
                         mod_uuid=UUID("a5ffe54f-736e-44a1-8814-76c128875bbc"),
                         description="Upgrades the Druid class to a Battlemage.",
                         classes=CharacterSubclasses.DRUID)

        # Passives and skills
        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._bolster = Bolster(self.mod).add_bolster()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)
        self._fast_movement = Movement(self.mod).add_fast_movement(3.0)
        self._natural_resistance = natural_resistance(self.mod)

        # Add scimitars and equipment set
        add_equipment(self.mod, self._EQUIPMENT_SET_NAME)

        # Create spelllists
        self._level_1_spelllist = str(self.make_uuid("level_1_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Druid level 1",
            Spells=[self._bolster],
            UUID=self._level_1_spelllist,
        ))

        self._level_5_spelllist = str(self.make_uuid("level_5_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Druid level 5",
            Spells=["Target_Counterspell"],
            UUID=self._level_5_spelllist,
        ))

    @class_description(CharacterClass.DRUID)
    def druid_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6
        class_description.ClassEquipment = self._EQUIPMENT_SET_NAME
        class_description.children.append(
            ClassDescription.Tags(Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"),  # WIZARD
        )

    @class_level(CharacterClass.DRUID, 1)
    def level_1(self, progression: Progression) -> None:
        # Add common features
        self.level_1_multiclass(progression)

        selectors = progression.Selectors or []
        selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
        selectors.extend([
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @class_level(CharacterClass.DRUID, 1, is_multiclass=True)
    def level_1_multiclass(self, progression: Progression) -> None:
        passives_added = progression.PassivesAdded or []
        passives_added.extend([
            self._battle_magic,
            self._natural_resistance,
            "FightingStyle_TwoWeaponFighting",
        ])
        progression.PassivesAdded = passives_added

        selectors = progression.Selectors or []
        selectors.append(f"AddSpells({self._level_1_spelllist},,,,AlwaysPrepared)")
        progression.Selectors = selectors

    @class_level(CharacterClass.DRUID, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["Blindsight", "SuperiorDarkvision"]

    @class_level(CharacterClass.DRUID, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["JackOfAllTrades"]

        selectors = progression.Selectors or []
        selectors.extend([
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @class_level(CharacterClass.DRUID, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]

    @class_level(CharacterClass.DRUID, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack", self._fast_movement]

        selectors = progression.Selectors or []
        selectors.append(f"AddSpells({self._level_5_spelllist},,,,AlwaysPrepared)")
        progression.Selectors = selectors

    @class_level(CharacterClass.DRUID, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["PotentCantrip"]

    @class_level(CharacterClass.DRUID, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]

    @class_level(CharacterClass.DRUID, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]

    @class_level(CharacterClass.DRUID, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]

    @class_level(CharacterClass.DRUID, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._empowered_spells, "ExtraAttack_2", "NaturesWard"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    @class_level(CharacterClass.DRUID, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]

        selectors = progression.Selectors or []
        selectors.append("AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a,,,,AlwaysPrepared)")  # Volley, Whirlwind
        progression.Selectors = selectors

    @class_level(CharacterClass.DRUID, 12)
    def level_12(self, progression: Progression) -> None:
        selectors = progression.Selectors or []
        selectors.append("AddSpells(964e765d-5881-463e-b1b0-4fc6b8035aa8,,,,AlwaysPrepared)")  # Action Surge
        progression.Selectors = selectors

    def postprocess(self, progressions: Iterable[Progression]) -> None:
        allow_improvement(progressions, range(2, 13))
        multiply_resources(progressions,
                           [ActionResource.SPELL_SLOTS,
                            ActionResource.FUNGAL_INFESTATION_CHARGES,
                            ActionResource.NATURAL_RECOVERY_CHARGES],
                           2)
        multiply_resources(progressions, [ActionResource.WILD_SHAPE_CHARGES], 4)


def main():
    druid_battlemage = DruidBattlemage()
    druid_battlemage.build()


if __name__ == "__main__":
    main()
