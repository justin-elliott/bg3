#!/usr/bin/env python3
"""
Generates files for the "Serenade" mod.
"""

import os

from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

serenade = Mod(os.path.dirname(__file__), "justin-elliott", "Serenade", UUID("fd8733d8-e1bd-4a41-9a54-40bc97ea99f0"),
               description="Adds the lute, Serenade.")

loca = serenade.get_localization()
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

loca["Virtuoso_DisplayName"] = {"en": "Virtuoso"}
loca["Virtuoso_Description"] = {"en": """
    You gain <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all
    <LSTag Tooltip="Charisma">Charisma</LSTag> Skills, and have
    <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in, and
    <LSTag Tooltip="Advantage">Advantage</LSTag> on, Charisma <LSTag Tooltip="AbilityCheck">Checks</LSTag>.
    """}

# Regex for data match:
# data "([^"]+)"\s*("[^"]+")
# $1=$2,

serenade.add_spell_data(
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

serenade.add_status_data(
    "SERENADE_MEDLEY",
    StatusType="BOOST",
    DisplayName=loca["Medley_DisplayName"],
    Description=loca["Medley_Boost_Description"],
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

serenade.add_armor(
    "ARM_Instrument_Lute_Serenade",
    using="ARM_Instrument_Lute_B",
    Flags="Unbreakable",
    Rarity="Legendary",
    RootTemplate="06b0b5a6-4f6c-4ee8-b4e1-6f65866b3ec5",
    Boosts=[
        "UnlockSpell(Serenade_Medley)",
        "UnlockSpell(Shout_Bard_Perform_Lute)",
    ],
    PassivesOnEquip="Serenade_Virtuoso",
    Weight="0.01",
)

serenade.add_passive_data(
    "Serenade_Virtuoso",
    DisplayName=loca["Virtuoso_DisplayName"],
    Description=loca["Virtuoso_Description"],
    Icon="Action_Song_SingForMe",
    Properties="Highlighted",
    Boosts=[
        "Proficiency(MusicalInstrument)",
        "ProficiencyBonus(SavingThrow,Charisma)",
        "Advantage(Ability,Charisma)",
        "ProficiencyBonus(Skill,Deception)",
        "ExpertiseBonus(Deception)",
        "ProficiencyBonus(Skill,Intimidation)",
        "ExpertiseBonus(Intimidation)",
        "ProficiencyBonus(Skill,Performance)",
        "ExpertiseBonus(Performance)",
        "ProficiencyBonus(Skill,Persuasion)",
        "ExpertiseBonus(Persuasion)",
    ],
)

serenade.add_level_maps([
    Lsx.Node("LevelMapSeries", [
        *[Lsx.Attribute(f"Level{level}", "LSString", value=f"{int(level * 2.5)}") for level in range(1, 21)],
        Lsx.Attribute("Name", "FixedString", value="Serenade_AidValue"),
        Lsx.Attribute("UUID", "guid", value="c0f41731-9b3b-4828-9092-3e104096938a"),
    ]),
    Lsx.Node("LevelMapSeries", [
        *[Lsx.Attribute(f"Level{level}", "LSString", value=f"1d{int((level + 3) / 4) * 2 + 2}")
            for level in range(1, 21)],
        Lsx.Attribute("Name", "FixedString", value="Serenade_HealValue"),
        Lsx.Attribute("UUID", "guid", value="803d7210-940d-4692-8178-436e3d711818"),
    ]),
])

serenade.add_root_templates([
    Lsx.Node("GameObjects", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["Serenade_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["Serenade_Description"], version="1"),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value="06b0b5a6-4f6c-4ee8-b4e1-6f65866b3ec5"),
        Lsx.Attribute("Name", "LSString", value="ARM_Instrument_Lute_Serenade"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value="f2487101-548f-4494-9ec8-b20fa3ad6f7b"),
        Lsx.Attribute("PhysicsTemplate", "FixedString", value="5d5007e5-cb6f-30ad-3d20-f762ea437673"),
        Lsx.Attribute("Type", "FixedString", value="item"),
        Lsx.Attribute("VisualTemplate", "FixedString", value="cfae4ff4-56ac-7bb8-9073-d732ef510c05"),
        Lsx.Attribute("_OriginalFileVersion_", "int64", value="1"),
    ])
])

serenade.set_treasure_table("""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_ARM_Instrument_Lute_Serenade",1,0,0,0,0,0,0,0
""")

serenade.build()
