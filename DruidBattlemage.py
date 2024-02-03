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
from modtools.gamedata import passive_data, status_data, weapon_data
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
)
from modtools.lsx import Lsx
from modtools.lsx.game import GameObjects, Progression, SpellList
from modtools.mod import Mod
from uuid import UUID

CLASS_DESCRIPTION_PATH = "Shared.pak/Public/Shared/ClassDescriptions/ClassDescriptions.lsx"

PROGRESSIONS_LSX_PATH = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
PROGRESSIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"

druid_battlemage = Mod(os.path.dirname(__file__),
                       author="justin-elliott",
                       name="DruidBattlemage",
                       mod_uuid=UUID("a5ffe54f-736e-44a1-8814-76c128875bbc"),
                       description="Upgrades the Druid class to a Battlemage.")

loca = druid_battlemage.get_localization()

# Add passives and spells
battle_magic = BattleMagic(druid_battlemage).add_battle_magic()
bolster = Bolster(druid_battlemage).add_bolster()
empowered_spells = EmpoweredSpells(druid_battlemage).add_empowered_spells(CharacterAbility.WISDOM)
fast_movement = Movement(druid_battlemage).add_fast_movement(3.0)

# Modify the game's Druid class description
class_descriptions = Lsx.load(druid_battlemage.get_cache_path(CLASS_DESCRIPTION_PATH))
druid_class_description: ClassDescription = class_descriptions.children.find(
    lambda child: child.Name == CharacterClass.DRUID)

druid_class_description.CanLearnSpells = True
druid_class_description.BaseHp = 10
druid_class_description.HpPerLevel = 6
druid_class_description.ClassEquipment = "EQP_CC_DruidBattlemage"
druid_class_description.children.append(ClassDescription.Tags(
    Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
))

druid_battlemage.add(druid_class_description)

# Load the game's Druid progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Lsx.load(druid_battlemage.get_cache_path(PROGRESSIONS_LSX_PATH))
progressions_dev_lsx = Lsx.load(druid_battlemage.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
progressions_lsx.children.update(progressions_dev_lsx.children, key=lambda child: child.UUID)

druid_progression = progressions_lsx.children.keepall(lambda child: child.Name in CharacterSubclasses.DRUID)

loca["DruidBattlemage_Regrowth_DisplayName"] = {"en": "Regrowth"}
loca["DruidBattlemage_Regrowth_Description"] = {"en": """
    On taking damage, you heal for [1].
    """}

druid_battlemage.add(passive_data(
    "DruidBattlemage_Regrowth",
    DisplayName=loca["DruidBattlemage_Regrowth_DisplayName"],
    Description=loca["DruidBattlemage_Regrowth_Description"],
    DescriptionParams=["RegainHitPoints(max(1, ClassLevel(Druid)))"],
    Icon="Action_Cleric_PreserveLife",
    Properties=["Highlighted"],
    StatsFunctorContext=["OnDamaged"],
    StatsFunctors=["RegainHitPoints(ClassLevel(Druid))"],
))

# Add scimitar
loca["DruidBattlemage_Scimitar_DisplayName"] = {"en": "Stormblade"}
loca["DruidBattlemage_Scimitar_Description"] = {"en": """
    This blade crackles with electrical energy.
    """}

druid_battlemage_scimitar_uuid = druid_battlemage.make_uuid("DruidBattlemage_Scimitar")
scimitar_a_0_uuid = UUID("868217db-9dcb-414c-bb88-e321ab3e0349")
scimitar_a_1_uuid = UUID("7cc7a0e1-d0b8-4569-afb2-d538e8941894")
scimitar_a_2_uuid = UUID("5193af64-48c1-406f-90bf-87f7f01b4684")
scimitar_momentum_on_attack = UUID("4456e2ec-ba1f-4f53-aab8-847249cabc09")
scimitar_the_clover = UUID("517231eb-e812-43ed-9ce3-482ba7ed31e6")

druid_battlemage.add(GameObjects(
    DisplayName=loca["DruidBattlemage_Scimitar_DisplayName"],
    Description=loca["DruidBattlemage_Scimitar_Description"],
    LevelName="",
    MapKey=druid_battlemage_scimitar_uuid,
    Name="DruidBattlemage_Scimitar",
    ParentTemplateId=scimitar_a_1_uuid,
    Stats="DruidBattlemage_Scimitar",
    Type="item",
    children=[
        GameObjects.StatusList(
            children=[
                GameObjects.StatusList.Status(Object="MAG_BYPASS_SLASHING_RESISTANCE_TECHNICAL"),
                GameObjects.StatusList.Status(Object="MAG_DIAMONDSBANE_TECHNICAL"),
                GameObjects.StatusList.Status(Object="DruidBattlemage_Scimitar_LightningEffect"),
            ],
        ),
    ],
))

druid_battlemage.add_script(character_level_range)

druid_battlemage.add(weapon_data(
    "DruidBattlemage_Scimitar",
    using="WPN_Scimitar",
    RootTemplate=str(druid_battlemage_scimitar_uuid),
    Rarity="Legendary",
    Damage="1d8",
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
        "DruidBattlemage_Scimitar_CriticalVsItems",
        "MAG_IgnoreSlashingResistance_Passive",
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

loca["DruidBattlemage_Scimitar_CriticalVsItems_Description"] = {"en": """
    If the Stormblade hits an object, the hit is always critical.
    """}

druid_battlemage.add(passive_data(
    "DruidBattlemage_Scimitar_CriticalVsItems",
    using="UNI_Adamantine_CriticalVsItems_Passive",
    Description=loca["DruidBattlemage_Scimitar_CriticalVsItems_Description"],
))

druid_battlemage.add(status_data(
    "DruidBattlemage_Scimitar_LightningEffect",
    StatusType="EFFECT",
    DisplayName="h363588c6g20b9g4407g91d8gebab0f1a5dca;1",
    StatusPropertyFlags=["IgnoreResting", "DisableCombatlog", "DisableOverhead", "DisablePortraitIndicator"],
    StatusEffect="7905bb82-0284-46b8-855b-24f17560fe4a",
))

druid_battlemage.add_equipment("""\
new equipment "EQP_CC_DruidBattlemage"
add initialweaponset "Melee"
add equipmentgroup
add equipment entry "DruidBattlemage_Scimitar"
add equipmentgroup
add equipment entry "DruidBattlemage_Scimitar"
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


# Add progressions
def progression_level(level: int,
                      *,
                      character_class: CharacterClass = CharacterClass.DRUID,
                      is_multiclass: bool = False) -> Progression:
    return druid_progression.find(lambda progression: (progression.Name == character_class
                                                       and progression.Level == level
                                                       and (progression.IsMulticlass or False) == is_multiclass))


def level_1() -> None:
    """Add armor and weapon proficiencies, passives, skills, and spells."""
    for is_multiclass in [False, True]:
        progression = progression_level(1, is_multiclass=is_multiclass)

        passives_added = progression.PassivesAdded or []
        passives_added.extend([
            battle_magic,
            "DruidBattlemage_Regrowth",
            "FightingStyle_TwoWeaponFighting",
        ])
        progression.PassivesAdded = passives_added

        level_1_spelllist = str(druid_battlemage.make_uuid("level_1_spelllist"))
        druid_battlemage.add(SpellList(
            Comment="Druid Battlemage level 1 spells",
            Spells=[bolster],
            UUID=level_1_spelllist,
        ))

        selectors = progression.Selectors or []
        selectors.append(f"AddSpells({level_1_spelllist},,,,AlwaysPrepared)")
        progression.Selectors = selectors

    # Progression when Druid is the class selected at level one
    progression = progression_level(1)

    selectors = progression.Selectors or []
    selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
    selectors.extend([
        "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
        "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
    ])
    progression.Selectors = selectors


def level_2() -> None:
    progression = progression_level(2)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["Blindsight", "DevilsSight", "WildShape_Combat"]

    progression = progression_level(2, character_class=CharacterClass.DRUID_SPORES)
    selectors = progression.Selectors or []
    selectors.remove("AddSpells(0f094e35-9675-464d-8cae-8e58c28de955,,,,AlwaysPrepared)")  # Wild Shapes
    selectors.extend([
        "AddSpells(2df1a00f-a66a-4240-a505-6a7835f2f1fa,,,,AlwaysPrepared)",  # Combat Wild Shapes
        "AddSpells(db963d3f-e0ba-4aba-a8e2-cf404dc54429,,,,AlwaysPrepared)",  # CWS: Polar Bear
    ])
    progression.Selectors = selectors


def level_3() -> None:
    progression = progression_level(3)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["JackOfAllTrades"]

    selectors = progression.Selectors or []
    selectors.extend([
        "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
        "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
    ])
    progression.Selectors = selectors


def level_4() -> None:
    progression = progression_level(4)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]

    progression = progression_level(4, character_class=CharacterClass.DRUID_SPORES)
    selectors = progression.Selectors or []
    selectors.remove("AddSpells(ef953742-69fa-4730-a289-bf9ce9629b1a,,,,AlwaysPrepared)")  # WS:  Deep Rothe
    selectors.append("AddSpells(94081296-f79b-4294-973e-111dabea22ca,,,,AlwaysPrepared)")  # CWS: Deep Rothe, Raven
    progression.Selectors = selectors


def level_5() -> None:
    progression = progression_level(5)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack", fast_movement]


def level_6() -> None:
    progression = progression_level(6)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["PotentCantrip", "PrimalStrike"]

    progression = progression_level(6, character_class=CharacterClass.DRUID_SPORES)
    selectors = progression.Selectors or []
    selectors.remove("AddSpells(c15f9224-a600-4a10-a5e7-642eed9c4222,,,,AlwaysPrepared)")  # WS:  Panther, Owlbear
    selectors.append("AddSpells(c3221a24-3bf7-4475-a675-1b5d87f650f0,,,,AlwaysPrepared)")  # CWS: Panther, Owlbear
    progression.Selectors = selectors


def level_7() -> None:
    progression = progression_level(7)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [
        "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]


def level_8() -> None:
    progression = progression_level(8)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]

    druid_progression.append(Progression(
        Level=8,
        Name=CharacterClass.DRUID_SPORES,
        ProgressionType=1,
        Selectors="AddSpells(dcdfdf72-16cd-473a-a15f-31a85381c3aa,,,,AlwaysPrepared)",  # CWS: Sabre-Toothed Tiger
        TableUUID="288c9d1e-ab18-46dd-8fa3-d4fcfa44147a",
        UUID=druid_battlemage.make_uuid("CircleOfSpores_Level_8")
    ))


def level_9() -> None:
    progression = progression_level(9)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]


def level_10() -> None:
    progression = progression_level(10)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [empowered_spells, "ExtraAttack_2", "NaturesWard"]
    progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    progression = progression_level(10, character_class=CharacterClass.DRUID_SPORES)
    selectors = progression.Selectors or []
    selectors.remove("AddSpells(e4d81321-c46f-4334-af8b-b6f4f87d811c)")  # WS: Dilophosaurus
    selectors.extend([
        "AddSpells(57d542ac-2d17-406c-90bd-b55920c94b95,,,,AlwaysPrepared)",  # CWS: Dilophosaurus
        "AddSpells(fa0b047d-4ff6-4ba0-8911-6c0f2f13be22,,,,AlwaysPrepared)",  # CWS: Myrmidons
    ]),
    progression.Selectors = selectors


def level_11() -> None:
    progression = progression_level(11)

    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]

    selectors = progression.Selectors or []
    selectors.append("AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a,,,,AlwaysPrepared)")  # Volley, Whirlwind
    progression.Selectors = selectors


def level_12() -> None:
    progression = progression_level(12)
    selectors = progression.Selectors or []
    selectors.append("AddSpells(964e765d-5881-463e-b1b0-4fc6b8035aa8,,,,AlwaysPrepared)")  # Action Surge
    progression.Selectors = selectors


level_1()
level_2()
level_3()
level_4()
level_5()
level_6()
level_7()
level_8()
level_9()
level_10()
level_11()
level_12()

allow_improvement(druid_progression, range(2, 13))
multiply_resources(druid_progression,
                   [ActionResource.SPELL_SLOTS, ActionResource.FUNGAL_INFESTATION_CHARGES,
                    ActionResource.NATURAL_RECOVERY_CHARGES, ActionResource.WILD_SHAPE_CHARGES],
                   2)

druid_progression.sort(key=lambda child: (CharacterClass(child.Name).name, child.Level, child.IsMulticlass or False))
for child in druid_progression:
    druid_battlemage.add(child)

druid_battlemage.build()
