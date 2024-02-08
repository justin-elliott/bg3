#!/usr/bin/env python3
"""
Generates files for the "DaughterOfDarkness" mod.
"""

import os

from moddb.battlemagic import BattleMagic
from moddb.bolster import Bolster
from moddb.empoweredspells import EmpoweredSpells
from moddb.movement import Movement
from moddb.progression import allow_improvement, multiply_resources
from moddb.scripts import character_level_range
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
    LevelMapSeries,
)
from modtools.lsx import Lsx
from modtools.lsx.game import Progression, SpellList
from modtools.mod import Mod
from uuid import UUID

CLASS_DESCRIPTION_PATH = "Shared.pak/Public/Shared/ClassDescriptions/ClassDescriptions.lsx"

PROGRESSIONS_LSX_PATH = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
PROGRESSIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"

daughter_of_darkness = Mod(os.path.dirname(__file__),
                           author="justin-elliott",
                           name="DaughterOfDarkness",
                           mod_uuid=UUID("225bcb03-1c2f-4e01-a4e1-93ae05f14783"),
                           description="Upgrades the Cleric Trickery domain subclass.")

daughter_of_darkness.add_script(character_level_range)

loca = daughter_of_darkness.get_localization()

# Add passives and spells
battle_magic = BattleMagic(daughter_of_darkness).add_battle_magic()
bolster = Bolster(daughter_of_darkness).add_bolster()
empowered_spells = EmpoweredSpells(daughter_of_darkness).add_empowered_spells(CharacterAbility.WISDOM)

movement = Movement(daughter_of_darkness)
fast_movement = movement.add_fast_movement(3.0)
shadow_step = movement.add_shadow_step()

daughter_of_darkness.add(PassiveData(
    "DaughterOfDarkness_PassWithoutTrace",
    DisplayName="h2b6ab85cg8d21g4c23g895eg6b8a61fdabab;1",
    Description="h5d1c1f49g43a6g44e0g807cgeb572b500fe2;6",
    Icon="Spell_Abjuration_PassWithoutTrace",
    Properties=["Highlighted", "IsToggled", "ToggledDefaultAddToHotbar"],
    ToggleOnFunctors=["ApplyStatus(SELF,PASS_WITHOUT_TRACE_AURA,100,-1)"],
    ToggleOffFunctors=["RemoveStatus(SELF,PASS_WITHOUT_TRACE_AURA)"],
))

daughter_of_darkness.add(SpellData(
    "DaughterOfDarkness_ViciousMockery",
    using="Target_ViciousMockery",
    SpellType="Target",
    SpellSuccess=[
        "ApplyStatus(VICIOUSMOCKERY,100,1)",
        "DealDamage(LevelMapValue(DaughterOfDarkness_ViciousMockeryValue),Psychic,Magical)",
    ],
    SpellFail=[
        "IF(HasPassive('PotentCantrip',context.Source)):"
        + "DealDamage((LevelMapValue(DaughterOfDarkness_ViciousMockeryValue)/2),Psychic,Magical)",
    ],
    TooltipDamageList=[
        "DealDamage(LevelMapValue(DaughterOfDarkness_ViciousMockeryValue),Psychic)",
    ],
))

daughter_of_darkness.add(LevelMapSeries(
    **{f"Level{level}": f"{level // 5 + 2}d4" for level in range(1, 21)},
    Name="DaughterOfDarkness_ViciousMockeryValue",
    UUID=daughter_of_darkness.make_uuid("DaughterOfDarkness_ViciousMockeryValue"),
))

# Modify the game's Cleric class description
class_descriptions = Lsx.load(daughter_of_darkness.get_cache_path(CLASS_DESCRIPTION_PATH))
cleric_class_description: ClassDescription = class_descriptions.children.find(
    lambda progression: progression.Name == CharacterClass.CLERIC)

cleric_class_description.CanLearnSpells = True
cleric_class_description.BaseHp = 10
cleric_class_description.HpPerLevel = 6
cleric_class_description.MustPrepareSpells = True

daughter_of_darkness.add(cleric_class_description)

# Load the game's Sorcerer progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Lsx.load(daughter_of_darkness.get_cache_path(PROGRESSIONS_LSX_PATH))
progressions_dev_lsx = Lsx.load(daughter_of_darkness.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
progressions_lsx.children.update(progressions_dev_lsx.children, key=lambda progression: progression.UUID)

cleric_progression = progressions_lsx.children.keepall(
    lambda progression: progression.Name in CharacterSubclasses.CLERIC)

# Create spell lists
level_1_spelllist = str(daughter_of_darkness.make_uuid("level_1_spelllist"))
daughter_of_darkness.add(SpellList(
    Comment="Daughter of Darkness level 1 spells",
    Spells=[
        "Target_BlessingOfTheTrickster",
        bolster,
        "Target_CharmPerson",
        "Shout_DisguiseSelf",
        "DaughterOfDarkness_NightsEdge_Summon",
        "Shout_Shield_Wizard",
        "DaughterOfDarkness_ViciousMockery",
    ],
    UUID=level_1_spelllist,
))

level_2_spelllist = str(daughter_of_darkness.make_uuid("level_2_spelllist"))
daughter_of_darkness.add(SpellList(
    Comment="Daughter of Darkness level 2 spells",
    Spells=[
        "Target_Darkness",
        "Shout_Hide_ShadowArts",
        "Shout_MirrorImage",
        shadow_step,
    ],
    UUID=level_2_spelllist,
))

level_3_spelllist = str(daughter_of_darkness.make_uuid("level_3_spelllist"))
daughter_of_darkness.add(SpellList(
    Comment="Daughter of Darkness level 3 spells",
    Spells=["Target_Counterspell"],
    UUID=level_3_spelllist,
))


def trickery_level(level: int) -> Progression:
    progression = cleric_progression.find(lambda progression: (progression.Name == CharacterClass.CLERIC_TRICKERY
                                                               and progression.Level == level))
    if not progression:
        progression = Progression(
            Level=level,
            Name="TrickeryDomain",
            ProgressionType=1,
            TableUUID="044e4e07-6980-479f-80e5-3c4a84e691d1",
            UUID=daughter_of_darkness.make_uuid(f"TrickeryDomain_Level_{level}")
        )
        cleric_progression.append(progression)
    return progression


def level_1() -> None:
    """Add armor and weapon proficiencies, passives, skills, and spells."""
    progression = trickery_level(1)

    boosts = progression.Boosts or []
    boosts.extend([
        "ProficiencyBonus(SavingThrow,Constitution)",
    ])
    progression.Boosts = boosts

    passives_added = progression.PassivesAdded or []
    passives_added.extend([battle_magic, "SculptSpells"])
    progression.PassivesAdded = passives_added

    progression.Selectors = [f"AddSpells({level_1_spelllist},ClericTrickeryDomainSpells,,,AlwaysPrepared)"]

    progression = cleric_progression.find(lambda progression: (progression.Name == CharacterClass.CLERIC
                                                               and progression.Level == 1
                                                               and not (progression.IsMulticlass or False)))

    selectors = progression.Selectors or []
    selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
    selectors.extend([
        "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
        "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
    ])
    progression.Selectors = selectors


def level_2() -> None:
    progression = trickery_level(2)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["DevilsSight"]


def level_3() -> None:
    progression = trickery_level(3)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["DaughterOfDarkness_PassWithoutTrace"]
    progression.Selectors = [
        f"AddSpells({level_2_spelllist},ClericTrickeryDomainSpells,,,AlwaysPrepared)",
    ]


def level_4() -> None:
    progression = trickery_level(4)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]


def level_5() -> None:
    progression = trickery_level(5)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack", fast_movement]

    selectors = progression.Selectors or []
    selectors.extend([
        f"AddSpells({level_3_spelllist},ClericTrickeryDomainSpells,,,AlwaysPrepared)",
    ])
    progression.Selectors = selectors


def level_6() -> None:
    progression = trickery_level(6)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["PotentCantrip"]


def level_7() -> None:
    progression = trickery_level(7)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [
        "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]


def level_8() -> None:
    progression = trickery_level(8)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]


def level_9() -> None:
    progression = trickery_level(9)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]


def level_10() -> None:
    progression = trickery_level(10)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [empowered_spells]


def level_11() -> None:
    progression = trickery_level(11)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
    progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    selectors = progression.Selectors or []
    selectors.append("AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)")  # Fly
    progression.Selectors = selectors


def level_12() -> None:
    progression = trickery_level(12)
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

allow_improvement(cleric_progression, range(2, 13))
multiply_resources(cleric_progression, [ActionResource.SPELL_SLOTS, ActionResource.CHANNEL_DIVINITY_CHARGES], 2)

cleric_progression.sort(key=lambda progression: (CharacterClass(progression.Name).name,
                                                 progression.Level,
                                                 progression.IsMulticlass or False))

for progression in cleric_progression:
    daughter_of_darkness.add(progression)

daughter_of_darkness.build()
