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
from modtools.gamedata import passive_data
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
)
from modtools.lsx import Lsx
from modtools.lsx.game import Progression, SpellList
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
druid_class_description.children.append(ClassDescription.Tags(
    Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
))

druid_battlemage.add(druid_class_description)

# Load the game's Druid progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Lsx.load(druid_battlemage.get_cache_path(PROGRESSIONS_LSX_PATH))
progressions_dev_lsx = Lsx.load(druid_battlemage.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
progressions_lsx.children.update(progressions_dev_lsx.children, key=lambda child: child.UUID)

druid_progression = progressions_lsx.children.keepall(lambda child: child.Name in CharacterSubclasses.DRUID)
druid_progression.sort(key=lambda child: (CharacterClass(child.Name).name, child.Level, child.IsMulticlass or False))

loca["DruidBattlemage_NaturalResistance_DisplayName"] = {"en": "Natural Resistance"}
loca["DruidBattlemage_NaturalResistance_Description"] = {"en": """
    You are naturally resistant to all forms of damage. Incoming damage is reduced by [1].
    """}

druid_battlemage.add(passive_data(
    "DruidBattlemage_NaturalResistance",
    DisplayName=loca["DruidBattlemage_NaturalResistance_DisplayName"],
    Description=loca["DruidBattlemage_NaturalResistance_Description"],
    DescriptionParams=["ClassLevel(Druid)"],
    Icon="Spell_Transmutation_Barkskin",
    Properties=["Highlighted"],
    Boosts=["DamageReduction(All,Flat,ClassLevel(Druid))"],
))


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
        passives_added.extend([battle_magic, "DruidBattlemage_NaturalResistance", "FightingStyle_TwoWeaponFighting"])
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

    selectors = progression.Selectors or []
    selectors.extend([
        "AddSpells(2df1a00f-a66a-4240-a505-6a7835f2f1fa,,,,AlwaysPrepared)",
        "AddSpells(db963d3f-e0ba-4aba-a8e2-cf404dc54429,,,,AlwaysPrepared)",
    ])
    progression.Selectors = selectors


def level_3() -> None:
    progression = progression_level(3)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["JackOfAllTrades"]


def level_4() -> None:
    progression = progression_level(4)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]

    selectors = progression.Selectors or []
    selectors.append("AddSpells(94081296-f79b-4294-973e-111dabea22ca,,,,AlwaysPrepared)")
    progression.Selectors = selectors


def level_5() -> None:
    progression = progression_level(5)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack", fast_movement]


def level_6() -> None:
    progression = progression_level(6)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["PotentCantrip", "PrimalStrike"]

    selectors = progression.Selectors or []
    selectors.append("AddSpells(c3221a24-3bf7-4475-a675-1b5d87f650f0,,,,AlwaysPrepared)")
    progression.Selectors = selectors


def level_7() -> None:
    progression = progression_level(7)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [
        "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]


def level_8() -> None:
    progression = progression_level(8)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]

    selectors = progression.Selectors or []
    selectors.append("AddSpells(dcdfdf72-16cd-473a-a15f-31a85381c3aa,,,,AlwaysPrepared)")
    progression.Selectors = selectors


def level_9() -> None:
    progression = progression_level(9)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]


def level_10() -> None:
    progression = progression_level(10)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [empowered_spells, "ExtraAttack_2", "NaturesWard"]
    progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    selectors = progression.Selectors or []
    selectors.append("AddSpells(fa0b047d-4ff6-4ba0-8911-6c0f2f13be22,,,,AlwaysPrepared)")
    progression.Selectors = selectors


def level_11() -> None:
    progression = progression_level(11)
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

for child in druid_progression:
    druid_battlemage.add(child)

druid_battlemage.build()
