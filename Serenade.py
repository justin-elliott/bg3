#!/usr/bin/env python3
"""
Generates files for the "Serenade" mod.
"""

import os

from modtools.mod import Mod
from uuid import UUID

serenade = Mod(os.path.dirname(__file__), "justin-elliott", "Serenade", UUID("a1c3d65c-3c00-4c7e-8aab-3ef7dd1593f1"),
               description="Adds the lute, Serenade.")

loca = serenade.localization
loca.add_language("en", "English")

loca["Serenade_DisplayName"] = {"en": "Serenade"}
loca["Serenade_Description"] = {"en": """
    Curved wood and strings of gold,
    a treasure to behold.
    Fingertips on frets alight,
    awaken day or starry night.
    Sweet notes dance and gracefully soar,
    through halls and chambers, evermore.
    A tapestry of sound so fine,
    the lute's melody, truly divine.
    """}

loca["Virtuoso_DisplayName"] = {"en": "Virtuoso"}
loca["Virtuoso_Description"] = {"en": """
    You gain <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all
    <LSTag Tooltip="Charisma">Charisma</LSTag> Skills, and have
    <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in, and
    <LSTag Tooltip="Advantage">Advantage</LSTag> on, Charisma <LSTag Tooltip="AbilityCheck">Checks</LSTag>.
    """}

loca["Medley_DisplayName"] = {"en": "Medley"}
loca["Medley_Description"] = {"en": "Perform a medley of songs to inspire and fortify your allies."}
loca["Medley_Boost_Description"] = {"en": """
    Hit point maximum increased by [1].

    Each turn, restore [2].

    When you roll a 1 on an <LSTag Tooltip="AttackRoll">Attack Roll</LSTag>,
    <LSTag Tooltip="AbilityCheck">Ability Check</LSTag>, or
    <LSTag Tooltip="SavingThrow">Saving Throw</LSTag>,
    you can reroll the die and must use the new roll.

    You can see in the dark up to [3].
    """}

# Regex for data match:
# data "([^"]+)"\s*("[^"]+")
# $1=$2,

serenade.SpellData(
    "Serenade_Medley",
    SpellType="Shout",
    using="Shout_SongOfRest",
    AreaRadius="9",
    Cooldown="None",
    DisplayName=loca["Medley_DisplayName"],
    Description=loca["Medley_Description"],
    Icon="Action_Song_SingForMe",
    Level="0",
    RequirementConditions="",
    SpellProperties=[
        "ApplyStatus(SERENADE_MEDLEY,100,-1)",
        "ApplyStatus(LONGSTRIDER,100,-1)",
        "ApplyStatus(PETPAL,100,-1)",
        "IF(not WearingArmor()):ApplyStatus(MAGE_ARMOR,100,-1)",
    ],
    TargetConditions="Party() and not Dead()",
    TooltipStatusApply=[
        "ApplyStatus(SERENADE_MEDLEY,100,-1)",
        "ApplyStatus(LONGSTRIDER,100,-1)",
        "ApplyStatus(PETPAL,100,-1)",
        "ApplyStatus(MAGE_ARMOR,100,-1)",
    ],
    VerbalIntent="Buff",
)

serenade.StatusData(
    "SERENADE_MEDLEY",
    StatusType="BOOST",
    DisplayName="Serenade_Medley_DisplayName",
    Description="Serenade_MedleyBoost_Description",
    DescriptionParams=[
        "LevelMapValue(Serenade_AidValue)",
        "RegainHitPoints(LevelMapValue(Serenade_HealValue))",
        "Distance(18)",
    ],
    Icon="Action_Song_SingForMe",
    StackId="AID",  # Mutually exclusive with AID stacks
    Boosts=[
        "IncreaseMaxHP(LevelMapValue(Serenade_AidValue))",
        "Reroll(Attack,1,true)",
        "Reroll(SkillCheck,1,true)",
        "Reroll(RawAbility,1,true)",
        "Reroll(SavingThrow,1,true)",
        "DarkvisionRangeMin(18)",
        "ActiveCharacterLight(c46e7ba8-e746-7020-5146-287474d7b9f7)",
    ],
    TickType="StartTurn",
    TickFunctors="IF(HasHPPercentageLessThan(100) and not IsDowned() and not Dead()):" +
                 "RegainHitPoints(LevelMapValue(Serenade_HealValue))",
    StatusGroups="SG_RemoveOnRespec",
)

serenade.build()
