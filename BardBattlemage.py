#!/usr/bin/env python3
"""
Generates files for the "BardBattlemage" mod.
"""

import os

from collections.abc import Callable
from moddb.battlemagic import BattleMagic
from moddb.bolster import Bolster
from moddb.movement import Movement
from moddb.progression import allow_improvement, multiply_resources, spells_always_prepared
from modtools.gamedata import spell_data
from modtools.lsx.game import (
    ActionResource,
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

bard_battlemage = Mod(os.path.dirname(__file__),
                      author="justin-elliott",
                      name="BardBattlemage",
                      mod_uuid=UUID("8f62881b-fc98-4e1a-8bff-23863405bb82"),
                      description="Upgrades the Bard class to a Battlemage.")

# Add passives and spells
battle_magic = BattleMagic(bard_battlemage).add_battle_magic()
bolster = Bolster(bard_battlemage).add_bolster()

movement = Movement(bard_battlemage)
fast_movement = movement.add_fast_movement(3.0)
misty_step = movement.add_misty_step()

# Modify the game's Bard class description
class_descriptions = Lsx.load(bard_battlemage.get_cache_path(CLASS_DESCRIPTION_PATH))
bard_class_description: ClassDescription = class_descriptions.children.find(
    lambda child: child.Name == CharacterClass.BARD)

bard_class_description.CanLearnSpells = True
bard_class_description.BaseHp = 10
bard_class_description.HpPerLevel = 6
bard_class_description.MustPrepareSpells = True
bard_class_description.children.append(ClassDescription.Tags(
    Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
))

bard_battlemage.add(bard_class_description)

# Load the game's Bard progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Lsx.load(bard_battlemage.get_cache_path(PROGRESSIONS_LSX_PATH))
progressions_dev_lsx = Lsx.load(bard_battlemage.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
progressions_lsx.children.update(progressions_dev_lsx.children, key=lambda child: child.UUID)

bard_progression = progressions_lsx.children.keepall(lambda child: child.Name in CharacterSubclasses.BARD)
bard_progression.sort(key=lambda child: (CharacterClass(child.Name).name, child.Level, child.IsMulticlass or False))

level_1_spelllist = str(bard_battlemage.make_uuid("level_1_spelllist"))
bard_battlemage.add(SpellList(
    Comment="Bard Battlemage level 1 spells",
    Spells=[bolster, "Target_Guidance", misty_step],
    UUID=level_1_spelllist,
))

# Upgrade the Vicious Mockery cantrip
bard_battlemage.add(spell_data(
    "Target_ViciousMockery",
    using="Target_ViciousMockery",
    SpellType="Target",
    SpellSuccess=[
        "ApplyStatus(VICIOUSMOCKERY,100,1)",
        "DealDamage(LevelMapValue(D10Cantrip),Psychic,Magical)",
    ],
    SpellFail=[
        "IF(HasPassive('PotentCantrip',context.Source)):DealDamage((LevelMapValue(D10Cantrip))/2,Psychic,Magical)",
    ],
    TooltipDamageList=["DealDamage(LevelMapValue(D10Cantrip),Psychic)"],
))


def bard_level(level: int, *,
               character_class: CharacterClass = CharacterClass.BARD,
               is_multiclass: bool = False) -> Callable[[Progression], bool]:
    def predicate(child: Progression) -> bool:
        return (child.Name == character_class
                and child.Level == level
                and (child.IsMulticlass or False) == is_multiclass)
    return predicate


def level_1() -> None:
    """Add armor and weapon proficiencies, passives, skills, and spells."""
    child: Progression

    for is_multiclass in [False, True]:
        child = bard_progression.find(bard_level(1, is_multiclass=is_multiclass))

        boosts = child.Boosts or []
        boosts = [boost for boost in boosts if boost not in ["Proficiency(HandCrossbows)",
                                                             "Proficiency(Longswords)",
                                                             "Proficiency(Rapiers)",
                                                             "Proficiency(Shortswords)"]]
        boosts.extend([
            "Proficiency(MediumArmor)",
            "Proficiency(HeavyArmor)",
            "Proficiency(Shields)",
            "Proficiency(MartialWeapons)",
        ])
        child.Boosts = boosts

        passives_added = child.PassivesAdded or []
        passives_added.extend([battle_magic, "SculptSpells"])
        child.PassivesAdded = passives_added

    # Progression when Bard is the class selected at level one
    child = bard_progression.find(bard_level(1))

    selectors = child.Selectors or []
    index = child.Selectors.index("SelectSkills(ed664663-93b9-4070-a54b-3c7b19c0e7b4,3)")
    child.Selectors[index] = "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)"
    selectors.append(f"AddSpells({level_1_spelllist},,,,AlwaysPrepared)")
    child.Selectors = selectors


def level_2() -> None:
    child: Progression = bard_progression.find(bard_level(2))
    child.PassivesAdded = (child.PassivesAdded or []) + ["DevilsSight"]


def level_3() -> None:
    child: Progression = bard_progression.find(bard_level(3))
    child.PassivesAdded = (child.PassivesAdded or []) + ["ImprovedCritical"]


def level_5() -> None:
    child: Progression = bard_progression.find(bard_level(5))
    child.PassivesAdded = (child.PassivesAdded or []) + ["ExtraAttack", fast_movement]


def level_7() -> None:
    child: Progression = bard_progression.find(bard_level(7))
    child.PassivesAdded = (child.PassivesAdded or []) + [
        "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]


def level_8() -> None:
    child: Progression = bard_progression.find(bard_level(8))
    child.PassivesAdded = (child.PassivesAdded or []) + ["FastHands"]


def level_9() -> None:
    child: Progression = bard_progression.find(bard_level(9))
    child.PassivesAdded = (child.PassivesAdded or []) + ["BrutalCritical"]


def level_11() -> None:
    child: Progression = bard_progression.find(bard_level(11))
    child.PassivesAdded = (child.PassivesAdded or []) + ["ExtraAttack_2"]
    child.PassivesRemoved = (child.PassivesRemoved or []) + ["ExtraAttack"]


level_1()
level_2()
level_3()
level_5()
level_7()
level_8()
level_9()
level_11()

spells_always_prepared(bard_progression)
multiply_resources(bard_progression, [ActionResource.SPELL_SLOTS, ActionResource.BARDIC_INSPIRATION_CHARGES], 2)
allow_improvement(bard_progression, range(2, 13))

for child in bard_progression:
    bard_battlemage.add(child)

bard_battlemage.build()
