#!/usr/bin/env python3
"""
Generates files for the "ArtfulDodger" mod.
"""

import os

from moddb.bolster import Bolster
from moddb.movement import Movement
from moddb.progression import allow_improvement
from modtools.gamedata_v2 import PassiveData, SpellData
from modtools.lsx.game import (
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
    SpellList,
)
from modtools.lsx import Lsx
from modtools.lsx.game import Progression
from modtools.mod import Mod
from uuid import UUID

CLASS_DESCRIPTION_PATH = "Shared.pak/Public/Shared/ClassDescriptions/ClassDescriptions.lsx"

PROGRESSIONS_LSX_PATH = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
PROGRESSIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"

artful_dodger = Mod(os.path.dirname(__file__),
                    author="justin-elliott",
                    name="ArtfulDodger",
                    mod_uuid=UUID("43e69217-76b5-4e1f-82a8-dd7f9aadaa6c"),
                    description="Upgrades the Rogue Thief subclass.")

loca = artful_dodger.get_localization()

# Add passives and spells
bolster = Bolster(artful_dodger).add_bolster()

movement = Movement(artful_dodger)
shadow_step = movement.add_shadow_step()
fast_movement_30 = movement.add_fast_movement(3.0)
fast_movement_45 = movement.add_fast_movement(4.5)
fast_movement_60 = movement.add_fast_movement(6.0)

loca["ArtfulDodger_ShadowStep_Hide_Description"] = {"en": """
    Step through the shadows and gain <LSTag Tooltip="Stealth">Stealth</LSTag>.
    """}

shadow_step_hide = SpellData(
    "ArtfulDodger_ShadowStep_Hide",
    using=shadow_step,
    SpellType="Target",
    Description=loca["ArtfulDodger_ShadowStep_Hide_Description"],
    SpellProperties="GROUND:TeleportSource();GROUND:ApplyStatus(SELF,SNEAKING,100,-1)",
)
artful_dodger.add(shadow_step_hide)

bolster_spelllist = str(artful_dodger.make_uuid("bolster_spelllist"))
artful_dodger.add(SpellList(
    Comment="Bolster",
    Spells=[bolster],
    UUID=bolster_spelllist,
))

shadow_step_hide_spelllist = str(artful_dodger.make_uuid("shadow_step_hide_spelllist"))
artful_dodger.add(SpellList(
    Comment="Shadow Step Hide",
    Spells=["ArtfulDodger_ShadowStep_Hide"],
    UUID=shadow_step_hide_spelllist,
))

# Modify the game's Rogue class description
class_descriptions = Lsx.load(artful_dodger.get_cache_path(CLASS_DESCRIPTION_PATH))
rogue_class_description: ClassDescription = class_descriptions.children.find(
    lambda child: child.Name == CharacterClass.ROGUE)

rogue_class_description.BaseHp = 10
rogue_class_description.HpPerLevel = 6

artful_dodger.add(rogue_class_description)

# Load the game's Rogue progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Lsx.load(artful_dodger.get_cache_path(PROGRESSIONS_LSX_PATH))
progressions_dev_lsx = Lsx.load(artful_dodger.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
progressions_lsx.children.update(progressions_dev_lsx.children, key=lambda child: child.UUID)

rogue_progression = progressions_lsx.children.keepall(lambda child: child.Name in CharacterSubclasses.ROGUE)

loca["ArtfulDodger_ShakeItOff_DisplayName"] = {"en": "Shake It Off"}
loca["ArtfulDodger_ShakeItOff_Description"] = {"en": """
    You haven't led the easiest of lives. You've had to learn how to take a hit, and then get back into the fight.
    When you take damage, you heal for [1].
    """}

artful_dodger.add(PassiveData(
    "ArtfulDodger_ShakeItOff",
    DisplayName=loca["ArtfulDodger_ShakeItOff_DisplayName"],
    Description=loca["ArtfulDodger_ShakeItOff_Description"],
    DescriptionParams=["RegainHitPoints(max(1, ClassLevel(Rogue)))"],
    Icon="PassiveFeature_Durable",
    Properties=["Highlighted"],
    StatsFunctorContext=["OnDamaged"],
    StatsFunctors=["RegainHitPoints(ClassLevel(Rogue))"],
))


def progression_level(level: int,
                      *,
                      character_class: CharacterClass = CharacterClass.ROGUE_THIEF,
                      is_multiclass: bool = False) -> Progression:
    progression = rogue_progression.find(lambda progression: (progression.Name == character_class
                                                              and progression.Level == level
                                                              and (progression.IsMulticlass or False) == is_multiclass))
    if progression is None:
        progression_type = 0 if character_class == CharacterClass.ROGUE else 1
        table_uuid = "9a44e828-92db-4d6c-acbc-a4f8ef340415" if character_class == CharacterClass.ROGUE else (
            "b19bc1ec-d7ee-4023-9f58-5056fd99be24")

        progression = Progression(
            Level=level,
            Name=str(character_class),
            ProgressionType=progression_type,
            TableUUID=table_uuid,
            UUID=artful_dodger.make_uuid(f"artful_dodger_{character_class}_{level}"),
        )
        rogue_progression.append(progression)

    return progression


def level_3() -> None:
    progression = progression_level(3)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [
        "ArtfulDodger_ShakeItOff",
        "Assassinate_Initiative",
        "Assassinate_Ambush",
        "Assassinate_Resource",
        fast_movement_30,
    ]

    selectors = progression.Selectors or []
    selectors.extend([
        "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
        "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        f"AddSpells({bolster_spelllist},,,,AlwaysPrepared)",
    ])
    progression.Selectors = selectors


def level_4() -> None:
    progression = progression_level(4)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [
        "Blindsight",
        "ImprovedCritical",
        "SuperiorDarkvision",
    ]


def level_5() -> None:
    progression = progression_level(5)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack"]

    selectors = progression.Selectors or []
    selectors.append(f"AddSpells({shadow_step_hide_spelllist},,,,AlwaysPrepared)")
    progression.Selectors = selectors


def level_6() -> None:
    progression = progression_level(6)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [fast_movement_45]
    progression.PassivesRemoved = (progression.PassivesRemoved or []) + [fast_movement_30]


def level_7() -> None:
    progression = progression_level(7)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [
        "LandsStride_DifficultTerrain",
        "LandsStride_Surfaces",
        "LandsStride_Advantage",
    ]


def level_8() -> None:
    progression = progression_level(8)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["FeralInstinct"]

    selectors = progression.Selectors or []
    selectors.extend([
        "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
        "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
    ])
    progression.Selectors = selectors


def level_9() -> None:
    progression = progression_level(9)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]


def level_10() -> None:
    progression = progression_level(10)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [fast_movement_60]
    progression.PassivesRemoved = (progression.PassivesRemoved or []) + [fast_movement_45]


def level_11() -> None:
    progression = progression_level(11)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
    progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    selectors = progression.Selectors or []
    selectors.append("AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a,,,,AlwaysPrepared)")  # Volley, Whirlwind
    progression.Selectors = selectors


def level_12() -> None:
    progression = progression_level(12)
    selectors = progression.Selectors or []
    selectors.append("AddSpells(964e765d-5881-463e-b1b0-4fc6b8035aa8,,,,AlwaysPrepared)")  # Action Surge
    progression.Selectors = selectors


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

allow_improvement(rogue_progression, range(2, 13, 2))

rogue_progression.sort(key=lambda child: (CharacterClass(child.Name).name, child.Level, child.IsMulticlass or False))
for child in rogue_progression:
    artful_dodger.add(child)

artful_dodger.build()
