#!/usr/bin/env python3
"""
Generates files for the "ChromaticBlade" mod.
"""

import os

from collections.abc import Callable, Iterable
from moddb.battlemagic import BattleMagic
from moddb.bolster import Bolster
from moddb.movement import Movement
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
    update_action_resources
)
from modtools.lsx import Lsx
from modtools.lsx.game import Progression, SpellList
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",

CLASS_DESCRIPTION_PATH = "Shared.pak/Public/Shared/ClassDescriptions/ClassDescriptions.lsx"

PROGRESSIONS_LSX_PATH = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
PROGRESSIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"

sorcerer_battlemage = Mod(os.path.dirname(__file__),
                          author="justin-elliott",
                          name="SorcererBattlemage",
                          mod_uuid=UUID("aa8aa79d-c67e-4fd8-98f7-392f549abf7e"),
                          description="Upgrades the Sorcerer class to a Battlemage.")

# Add passives and spells
battle_magic = BattleMagic(sorcerer_battlemage).add_battle_magic()
bolster = Bolster(sorcerer_battlemage).add_bolster()
fast_movement = Movement(sorcerer_battlemage).add_fast_movement(3.0)

# Modify the game's Sorcerer class description
class_descriptions = Lsx.load(sorcerer_battlemage.get_cache_path(CLASS_DESCRIPTION_PATH))
sorcerer_class_description: ClassDescription = class_descriptions.children.find(
    lambda child: child.Name == CharacterClass.SORCERER)

sorcerer_class_description.CanLearnSpells = True
sorcerer_class_description.BaseHp = 10
sorcerer_class_description.HpPerLevel = 6
sorcerer_class_description.MustPrepareSpells = True

sorcerer_battlemage.add(sorcerer_class_description)

# Load the game's Sorcerer progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Lsx.load(sorcerer_battlemage.get_cache_path(PROGRESSIONS_LSX_PATH))
progressions_dev_lsx = Lsx.load(sorcerer_battlemage.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
progressions_lsx.children.update(progressions_dev_lsx.children, key=lambda child: child.UUID)

sorcerer_progression = progressions_lsx.children.keepall(lambda child: child.Name in CharacterSubclasses.SORCERER)
sorcerer_progression.sort(key=lambda child: (CharacterClass(child.Name).name, child.Level, child.IsMulticlass or False))

level_1_spelllist = str(sorcerer_battlemage.make_uuid("level_1_spelllist"))
sorcerer_battlemage.add(SpellList(
    Comment="Sorcerer Battlemage level 1 spells",
    Spells=[bolster, "Target_CreateDestroyWater", "Projectile_EldritchBlast", "Target_Guidance"],
    UUID=level_1_spelllist,
))

level_2_spelllist = str(sorcerer_battlemage.make_uuid("level_2_spelllist"))
sorcerer_battlemage.add(SpellList(
    Comment="Sorcerer Battlemage level 2 spells",
    Spells=["Target_EnhanceAbility"],
    UUID=level_2_spelllist,
))


def sorcerer_level(level: int, *, is_multiclass: bool = False) -> Callable[[Progression], bool]:
    def predicate(child: Progression) -> bool:
        return (child.Name == CharacterClass.SORCERER
                and child.Level == level
                and (child.IsMulticlass or False) == is_multiclass)
    return predicate


def level_1() -> None:
    """Add armor and weapon proficiencies, passives, skills, and spells."""
    child: Progression

    for is_multiclass in [False, True]:
        child = sorcerer_progression.find(sorcerer_level(1, is_multiclass=is_multiclass))

        boosts = child.Boosts or []
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
        child.Boosts = boosts

        passives_added = child.PassivesAdded or []
        passives_added.extend([battle_magic, "SculptSpells"])
        child.PassivesAdded = passives_added

        selectors = child.Selectors or []
        selectors.append(f"AddSpells({level_1_spelllist},,,,AlwaysPrepared)")
        child.Selectors = selectors

    # Progression when Sorcerer is the class selected at level one
    child = sorcerer_progression.find(sorcerer_level(1))

    selectors = child.Selectors or []
    selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
    selectors.extend([
        "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
        "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
    ])
    child.Selectors = selectors


def level_2() -> None:
    child: Progression = sorcerer_progression.find(sorcerer_level(2))
    child.PassivesAdded = (child.PassivesAdded or []) + ["AgonizingBlast", "DevilsSight", "RepellingBlast"]

    index = child.Selectors.index("AddSpells(979e37ad-05fa-466c-af99-9eb104a6e876)")
    child.Selectors[index] = "AddSpells(979e37ad-05fa-466c-af99-9eb104a6e876,,,,AlwaysPrepared)"


def level_3() -> None:
    child: Progression = sorcerer_progression.find(sorcerer_level(3))
    child.PassivesAdded = (child.PassivesAdded or []) + ["ImprovedCritical"]

    selectors = child.Selectors or []
    selectors.append(f"AddSpells({level_2_spelllist},,,,AlwaysPrepared)")
    child.Selectors = selectors


def level_5() -> None:
    child: Progression = sorcerer_progression.find(sorcerer_level(5))
    child.PassivesAdded = (child.PassivesAdded or []) + ["ExtraAttack", fast_movement]


def level_7() -> None:
    child: Progression = sorcerer_progression.find(sorcerer_level(7))
    child.PassivesAdded = (child.PassivesAdded or []) + [
        "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]


def level_8() -> None:
    child: Progression = sorcerer_progression.find(sorcerer_level(8))
    child.PassivesAdded = (child.PassivesAdded or []) + ["FastHands"]


def level_9() -> None:
    child: Progression = sorcerer_progression.find(sorcerer_level(9))
    child.PassivesAdded = (child.PassivesAdded or []) + ["BrutalCritical"]


def level_11() -> None:
    child: Progression = sorcerer_progression.find(sorcerer_level(11))
    child.PassivesAdded = (child.PassivesAdded or []) + ["ExtraAttack_2"]
    child.PassivesRemoved = (child.PassivesRemoved or []) + ["ExtraAttack"]


def increase_resources(multiplier: int):
    # Double spell slots and sorcery points
    child: Progression
    for child in sorcerer_progression:
        if (boosts := child.Boosts) is not None:
            child.Boosts = update_action_resources(boosts,
                                                   [ActionResource.SPELL_SLOTS, ActionResource.SORCERY_POINTS],
                                                   lambda _resource, count, _level: count * multiplier)


def allow_improvement(levels: Iterable[int]) -> None:
    levels = set(levels)
    for level in range(1, 13):
        child: Progression = sorcerer_progression.find(sorcerer_level(level))
        child.AllowImprovement = True if level in levels else None


level_1()
level_2()
level_3()
level_5()
level_7()
level_8()
level_9()
level_11()
increase_resources(2)
allow_improvement([level for level in range(2, 13)])

for child in sorcerer_progression:
    sorcerer_battlemage.add(child)

sorcerer_battlemage.build()
