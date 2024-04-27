#!/usr/bin/env python3
"""
Generates files for the "Serenade" mod.
"""

import os

from dataclasses import dataclass
from modtools.gamedata import Armor, PassiveData
from modtools.lsx.game import CharacterAbility, GameObjects
from modtools.mod import Mod
from modtools.text import TreasureTable


@dataclass
class ProficiencyGroup:
    name: str
    ability: CharacterAbility
    skills: list[str]


proficiency_groups: list[ProficiencyGroup] = [
    ProficiencyGroup("Strong",
                     CharacterAbility.STRENGTH,
                     ["Athletics"]),
    ProficiencyGroup("Agile",
                     CharacterAbility.DEXTERITY,
                     ["Acrobatics", "SleightOfHand", "Stealth"]),
    ProficiencyGroup("Hardy",
                     CharacterAbility.CONSTITUTION,
                     []),
    ProficiencyGroup("Intelligent",
                     CharacterAbility.INTELLIGENCE,
                     ["Arcana", "History", "Investigation", "Nature", "Religion"]),
    ProficiencyGroup("Wise",
                     CharacterAbility.WISDOM,
                     ["AnimalHandling", "Insight", "Medicine", "Perception", "Survival"]),
    ProficiencyGroup("Charismatic",
                     CharacterAbility.CHARISMA,
                     ["Deception", "Intimidation", "Performance", "Persuasion"]),
]

serenade = Mod(os.path.dirname(__file__),
               author="justin-elliott",
               name="Serenade",
               description="Adds the lute, Serenade.")

loca = serenade.get_localization()

loca[f"{serenade.get_prefix()}_DisplayName"] = {"en": "Serenade"}
loca[f"{serenade.get_prefix()}_Description"] = {"en": """
    Curved wood and strings of gold,
    a treasure to behold.
    Fingertips on frets alight,
    awaken day or starry night.
    Sweet notes dance and gracefully soar,
    through halls and chambers, evermore.
    A tapestry of sound so fine,
    the lute's melody, truly divine.
    """}

serenade_name = f"{serenade.get_prefix()}_ARM_Instrument_Lute"
serenade_game_objects_uuid = serenade.make_uuid("Serenade Game Objects")

serenade.add(GameObjects(
    DisplayName=loca[f"{serenade.get_prefix()}_DisplayName"],
    Description=loca[f"{serenade.get_prefix()}_Description"],
    LevelName="",
    MapKey=serenade_game_objects_uuid,
    Name=serenade_name,
    ParentTemplateId="f2487101-548f-4494-9ec8-b20fa3ad6f7b",
    PhysicsTemplate="5d5007e5-cb6f-30ad-3d20-f762ea437673",
    Type="item",
    VisualTemplate="cfae4ff4-56ac-7bb8-9073-d732ef510c05",
))

proficiency_passives = []

for proficiency_group in proficiency_groups:
    ability_name = CharacterAbility(proficiency_group.ability).name.title()
    passive_name = f"{serenade.get_prefix()}_{ability_name}Expertise"
    proficiency_passives.append(passive_name)

    loca[f"{passive_name}_DisplayName"] = {"en": proficiency_group.name}
    loca[f"{passive_name}_Description"] = {"en": f"""
        You gain <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all
        <LSTag Tooltip="{ability_name}">{ability_name}</LSTag> Skills, and have
        <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in
        {ability_name} <LSTag Tooltip="AbilityCheck">Checks</LSTag>.
        """}

    serenade.add(PassiveData(
        passive_name,
        DisplayName=loca[f"{passive_name}_DisplayName"],
        Description=loca[f"{passive_name}_Description"],
        Icon="Action_Song_SingForMe",
        Properties=["IsHidden"],
        Boosts=[
            f"ProficiencyBonus(SavingThrow,{ability_name})",
            *[f"ProficiencyBonus(Skill,{skill})" for skill in proficiency_group.skills],
            *[f"ExpertiseBonus({skill})" for skill in proficiency_group.skills],
        ],
    ))

virtuoso = f"{serenade.get_prefix()}_Virtuoso"

loca[f"{virtuoso}_DisplayName"] = {"en": "Virtuoso"}
loca[f"{virtuoso}_Description"] = {"en": """
    You gain <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all skills, and
    <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in
    all <LSTag Tooltip="AbilityCheck">ability checks</LSTag>.
    """}

serenade.add(PassiveData(
    virtuoso,
    DisplayName=loca[f"{virtuoso}_DisplayName"],
    Description=loca[f"{virtuoso}_Description"],
    Icon="Action_Song_SingForMe",
    Properties=["Highlighted"],
))

serenade.add(Armor(
    serenade_name,
    using="ARM_Instrument_Lute_B",
    Flags=["Unbreakable"],
    Rarity="Legendary",
    RootTemplate=serenade_game_objects_uuid,
    Boosts=[
        "Proficiency(MusicalInstrument)",
        "UnlockSpell(Shout_Bard_Perform_Lute)",
    ],
    PassivesOnEquip=[virtuoso, *proficiency_passives],
    Weight="0.01",
))

serenade.add(TreasureTable(f"""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_{serenade_name}",1,0,0,0,0,0,0,0
"""))

serenade.build()
