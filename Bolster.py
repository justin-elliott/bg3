#!/usr/bin/env python3
"""
Generates files for the "Bolster" mod.
"""

import os

from modtools.gamedata import spell_data, status_data
from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

bolster = Mod(os.path.dirname(__file__),
              "justin-elliott",
              "Bolster",
              UUID("fac099c8-f18b-4cd1-ad49-9653ded5cd86"),
              description="Adds the spell, Bolster.")

loca = bolster.get_localization()

loca["Bolster_DisplayName"] = {"en": "Bolster"}
loca["Bolster_Description"] = {"en": """
    Bolster your allies against the dangers that lie ahead.
    """}
loca["Bolster_StatusDescription"] = {"en": """
    Hit point maximum increased by [1].

    When you roll a 1 on an <LSTag Tooltip="AttackRoll">Attack Roll</LSTag>,
    <LSTag Tooltip="AbilityCheck">Ability Check</LSTag>, or
    <LSTag Tooltip="SavingThrow">Saving Throw</LSTag>,
    you can reroll the die and must use the new roll.

    You can see in the dark up to [2].
    """}

bolster.add(spell_data(
    "Bolster_Bolster",
    using="Shout_Aid",
    SpellType="Shout",
    AreaRadius="9",
    Cooldown="None",
    DisplayName=loca["Bolster_DisplayName"],
    Description=loca["Bolster_Description"],
    Level="",
    RequirementConditions="",
    Requirements="!Combat",
    SpellProperties=[
        "ApplyStatus(BOLSTER_BOLSTER,100,-1)",
        "ApplyStatus(LONGSTRIDER,100,-1)",
        "ApplyStatus(PETPAL,100,-1)",
        "IF(not WearingArmor()):ApplyStatus(MAGE_ARMOR,100,-1)",
    ],
    TargetConditions="Party() and not Dead()",
    TooltipStatusApply=[
        "ApplyStatus(BOLSTER_BOLSTER,100,-1)",
        "ApplyStatus(LONGSTRIDER,100,-1)",
        "ApplyStatus(PETPAL,100,-1)",
        "ApplyStatus(MAGE_ARMOR,100,-1)",
    ],
    UseCosts="ActionPoint:1",
    VerbalIntent="Buff",
))

bolster.add(status_data(
    "BOLSTER_BOLSTER",
    StatusType="BOOST",
    DisplayName=loca["Bolster_DisplayName"],
    Description=loca["Bolster_StatusDescription"],
    DescriptionParams=[
        "LevelMapValue(Bolster_AidValue)",
        "Distance(12)",
    ],
    Icon="Spell_Abjuration_Aid",
    StackId="AID",  # Mutually exclusive with AID stacks
    Boosts=[
        "IncreaseMaxHP(LevelMapValue(Bolster_AidValue))",
        "Reroll(Attack,1,true)",
        "Reroll(SkillCheck,1,true)",
        "Reroll(RawAbility,1,true)",
        "Reroll(SavingThrow,1,true)",
        "DarkvisionRangeMin(12)",
        "ActiveCharacterLight(051648e6-f05a-e41f-e398-ffd5cd148989)",
    ],
    StatusGroups="SG_RemoveOnRespec",
))

bolster.add_level_maps([
    Lsx.Node("LevelMapSeries", [
        *[Lsx.Attribute(f"Level{level}", "LSString", value=f"{int(level * 2.5)}") for level in range(1, 21)],
        Lsx.Attribute("Name", "FixedString", value="Bolster_AidValue"),
        Lsx.Attribute("UUID", "guid", value="942a69d7-b54c-47f6-b2bb-f145666110e6"),
    ]),
])

bolster.build()
