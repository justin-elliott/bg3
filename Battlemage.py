#!/usr/bin/env python3
"""
Generates files for the "Battlemage" mod.
"""

import os

from collections.abc import Callable, Iterable
from moddb.battlemagic import BattleMagic
from moddb.bolster import Bolster
from moddb.movement import Movement
from modtools.gamedata import spell_data
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
    update_action_resources
)
from modtools.lsx import Lsx
from modtools.lsx.game import Progression, SpellList, Tags
from modtools.mod import Mod
from uuid import UUID

battlemage = Mod(os.path.dirname(__file__),
                 author="justin-elliott",
                 name="Battlemage",
                 mod_uuid=UUID("61f080fa-fda0-4a7a-933b-a27ce3f380f1"),
                 description="Adds the Battlemage class.")

loca = battlemage.get_localization()

BATTLEMAGE_CLASS_UUID = battlemage.make_uuid("BATTLEMAGE_CLASS")
BATTLEMAGE_PROGRESSION_TABLE_UUID = battlemage.make_uuid("BATTLEMAGE_PROGRESSION_TABLE")
BATTLEMAGE_SPELLLIST_UUID = battlemage.make_uuid("BATTLEMAGE_SPELLLIST")
BATTLEMAGE_TAG_UUID = battlemage.make_uuid("BATTLEMAGE_TAG")

FIGHTER_TAG_UUID = UUID("1ae7017c-4884-4a43-bc4a-742fa0d201c0")
SORCERER_TAG_UUID = UUID("18266c0b-efbc-4c80-8784-ada4a37218d7")

# Add the class description
loca["Battlemage_Class_DisplayName"] = {"en": "Battlemage"}
loca["Battlemage_Class_Description"] = {"en": """
    A natural spellcaster, you seek to augment your burgeoning power with study in both the arcane and mundane.
    """}

battlemage.add(ClassDescription(
    BaseHp=10,
    CanLearnSpells=True,
    CharacterCreationPose="0f07ec6e-4ef0-434e-9a51-1353260ccff8",
    ClassEquipment="EQP_CC_Warlock",
    DisplayName=loca["Battlemage_Class_DisplayName"],
    Description=loca["Battlemage_Class_Description"],
    HpPerLevel=6,
    LearningStrategy=1,
    MustPrepareSpells=True,
    Name="Battlemage",
    PrimaryAbility=CharacterAbility.CHARISMA,
    ProgressionTableUUID=BATTLEMAGE_PROGRESSION_TABLE_UUID,
    SoundClassType="Fighter",
    SpellCastingAbility=CharacterAbility.CHARISMA,
    SpellList=BATTLEMAGE_SPELLLIST_UUID,
    UUID=BATTLEMAGE_CLASS_UUID,
    children=[
        ClassDescription.Tags(Object=BATTLEMAGE_TAG_UUID),
        ClassDescription.Tags(Object=FIGHTER_TAG_UUID),
        ClassDescription.Tags(Object=SORCERER_TAG_UUID),
    ],
))

battlemage.add(Tags.Tags(
    Description="A natural spellcaster who studies arms and magic.",
    DisplayDescription=loca["Battlemage_Class_Description"],
    DisplayName=loca["Battlemage_Class_DisplayName"],
    Icon="",
    Name="BATTLEMAGE",
    UUID=BATTLEMAGE_TAG_UUID,
    children=[
        Tags.Tags.Categories(
            children=[
                Tags.Tags.Categories.Category(Name="CharacterSheet"),
                Tags.Tags.Categories.Category(Name="Class"),
                Tags.Tags.Categories.Category(Name="Code"),
                Tags.Tags.Categories.Category(Name="Dialog"),
            ],
        ),
    ],
))

battlemage.build()
