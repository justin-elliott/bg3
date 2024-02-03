#!/usr/bin/env python3
"""
Generates files for the "SorcererBattlemage" mod.
"""

import os

from moddb.battlemagic import BattleMagic
from moddb.bolster import Bolster
from moddb.empoweredspells import EmpoweredSpells
from moddb.movement import Movement
from moddb.progression import allow_improvement, multiply_resources, spells_always_prepared
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

sorcerer_battlemage = Mod(os.path.dirname(__file__),
                          author="justin-elliott",
                          name="SorcererBattlemage",
                          mod_uuid=UUID("aa8aa79d-c67e-4fd8-98f7-392f549abf7e"),
                          description="Upgrades the Sorcerer class to a Battlemage.")

loca = sorcerer_battlemage.get_localization()

# Add passives and spells
battle_magic = BattleMagic(sorcerer_battlemage).add_battle_magic()
bolster = Bolster(sorcerer_battlemage).add_bolster()
empowered_spells = EmpoweredSpells(sorcerer_battlemage).add_empowered_spells(CharacterAbility.CHARISMA)
fast_movement = Movement(sorcerer_battlemage).add_fast_movement(3.0)

# Modify the game's Sorcerer class description
class_descriptions = Lsx.load(sorcerer_battlemage.get_cache_path(CLASS_DESCRIPTION_PATH))
sorcerer_class_description: ClassDescription = class_descriptions.children.find(
    lambda child: child.Name == CharacterClass.SORCERER)

sorcerer_class_description.CanLearnSpells = True
sorcerer_class_description.BaseHp = 10
sorcerer_class_description.HpPerLevel = 6
sorcerer_class_description.MustPrepareSpells = True
sorcerer_class_description.children.append(ClassDescription.Tags(
    Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
))

sorcerer_battlemage.add(sorcerer_class_description)

# Load the game's Sorcerer progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Lsx.load(sorcerer_battlemage.get_cache_path(PROGRESSIONS_LSX_PATH))
progressions_dev_lsx = Lsx.load(sorcerer_battlemage.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
progressions_lsx.children.update(progressions_dev_lsx.children, key=lambda child: child.UUID)

sorcerer_progression = progressions_lsx.children.keepall(lambda child: child.Name in CharacterSubclasses.SORCERER)

loca["SorcererBattlemage_Warding_DisplayName"] = {"en": "Warding"}
loca["SorcererBattlemage_Warding_Description"] = {"en": """
    Your magic protects you from harm, making you resistant to all forms of damage. Incoming damage is reduced by [1].
    """}

sorcerer_battlemage.add(passive_data(
    "SorcererBattlemage_Warding",
    DisplayName=loca["SorcererBattlemage_Warding_DisplayName"],
    Description=loca["SorcererBattlemage_Warding_Description"],
    DescriptionParams=["RegainHitPoints(max(1, ClassLevel(Sorcerer)))"],
    Icon="PassiveFeature_ArcaneWard",
    Properties=["Highlighted"],
    Boosts=["DamageReduction(All,Flat,ClassLevel(Sorcerer))"],
))

level_1_spelllist = str(sorcerer_battlemage.make_uuid("level_1_spelllist"))
sorcerer_battlemage.add(SpellList(
    Comment="Sorcerer Battlemage level 1 spells",
    Spells=[bolster, "Target_CreateDestroyWater", "Target_Guidance"],
    UUID=level_1_spelllist,
))

level_2_spelllist = str(sorcerer_battlemage.make_uuid("level_2_spelllist"))
sorcerer_battlemage.add(SpellList(
    Comment="Sorcerer Battlemage level 2 spells",
    Spells=["Target_EnhanceAbility"],
    UUID=level_2_spelllist,
))


def progression_level(level: int,
                      *,
                      character_class: CharacterClass = CharacterClass.SORCERER,
                      is_multiclass: bool = False) -> Progression:
    return sorcerer_progression.find(lambda progression: (progression.Name == character_class
                                                          and progression.Level == level
                                                          and (progression.IsMulticlass or False) == is_multiclass))


def level_1() -> None:
    """Add armor and weapon proficiencies, passives, skills, and spells."""
    for is_multiclass in [False, True]:
        progression = progression_level(1, is_multiclass=is_multiclass)

        boosts = progression.Boosts or []
        boosts = [boost for boost in boosts if boost not in ["Proficiency(Daggers)",
                                                             "Proficiency(Quarterstaffs)",
                                                             "Proficiency(LightCrossbows)"]]
        boosts.extend([
            "Proficiency(LightArmor)",
            "Proficiency(MediumArmor)",
            "Proficiency(HeavyArmor)",
            "Proficiency(Shields)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
        ])
        progression.Boosts = boosts

        passives_added = progression.PassivesAdded or []
        passives_added.extend([
            battle_magic,
            "SculptSpells",
            "UnarmouredDefence_Barbarian",
            "SorcererBattlemage_Warding",
        ])
        progression.PassivesAdded = passives_added

        selectors = progression.Selectors or []
        selectors.append(f"AddSpells({level_1_spelllist},,,,AlwaysPrepared)")
        progression.Selectors = selectors

    # Remove Draconic Resilience, since we have Unarmored Defence instead
    progression = progression_level(1, character_class=CharacterClass.SORCERER_DRACONIC)
    passives_added = progression.PassivesAdded or []
    passives_added = [passive for passive in passives_added if passive != "DraconicResilience"]
    progression.PassivesAdded = passives_added

    # Progression when Sorcerer is the class selected at level one
    progression = progression_level(1)

    selectors = progression.Selectors or []
    selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
    selectors.extend([
        "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
        "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
    ])
    progression.Selectors = selectors


def level_2() -> None:
    progression = progression_level(2)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["Blindsight", "DevilsSight"]


def level_3() -> None:
    progression = progression_level(3)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["JackOfAllTrades"]

    selectors = progression.Selectors or []
    selectors.extend([
        f"AddSpells({level_2_spelllist},,,,AlwaysPrepared)",
    ])
    progression.Selectors = selectors


def level_4() -> None:
    progression = progression_level(4)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]


def level_5() -> None:
    progression = progression_level(5)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack", fast_movement]


def level_6() -> None:
    progression = progression_level(6)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["PotentCantrip"]


def level_7() -> None:
    progression = progression_level(7)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [
        "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]


def level_8() -> None:
    progression = progression_level(8)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]


def level_9() -> None:
    progression = progression_level(9)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]


def level_10() -> None:
    progression = progression_level(10)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [empowered_spells]


def level_11() -> None:
    progression = progression_level(11)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
    progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    selectors = progression.Selectors or []
    selectors.append("AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)")  # Fly
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

allow_improvement(sorcerer_progression, range(2, 13))
multiply_resources(sorcerer_progression, [ActionResource.SPELL_SLOTS, ActionResource.SORCERY_POINTS], 2)
spells_always_prepared(sorcerer_progression)

sorcerer_progression.sort(key=lambda child: (CharacterClass(child.Name).name, child.Level, child.IsMulticlass or False))
for child in sorcerer_progression:
    sorcerer_battlemage.add(child)

sorcerer_battlemage.build()
