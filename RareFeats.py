#!/usr/bin/env python3
"""
Generates files for the "RareFeats" mod.
"""

import os

from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",

rare_feats = Mod(os.path.dirname(__file__),
                 author="justin-elliott",
                 name="RareFeats",
                 mod_uuid=UUID("1bfebf94-20b2-4105-bd4f-4caeb8a1fe2a"),
                 description="Adds additional feats.")

loca = rare_feats.get_localization()
loca.add_language("en", "English")

# A feat for when you don't wish to select a feat
no_feat_uuid = rare_feats.make_uuid("RareFeats_Feat_NoFeat")

loca["RareFeats_NoFeat_DisplayName"] = {"en": "Rare Feats: No Feat"}
loca["RareFeats_NoFeat_Description"] = {"en": "Do not select a feat."}

rare_feats.add_feat_descriptions([
    Lsx.Node("FeatDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["RareFeats_NoFeat_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["RareFeats_NoFeat_Description"], version="1"),
        Lsx.Attribute("ExactMatch", "FixedString", value="RareFeats_NoFeat"),
        Lsx.Attribute("FeatId", "guid", value=str(no_feat_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(rare_feats.make_uuid("RareFeats_FeatDescription_NoFeat"))),
    ]),
])

rare_feats.add_feats([
    Lsx.Node("Feat", [
        Lsx.Attribute("CanBeTakenMultipleTimes", "bool", value="true"),
        Lsx.Attribute("Name", "FixedString", value="RareFeats_NoFeat"),
        Lsx.Attribute("UUID", "guid", value=str(no_feat_uuid)),
    ]),
])

# Add Ability Score Improvement (ASI) feats
for asi in [4, 8, 16, 32, 44]:
    feat_uuid = rare_feats.make_uuid(f"feat_ASI_{asi}")
    feat_description_uuid = rare_feats.make_uuid(f"feat_description_ASI_{asi}")

    loca[f"RareFeats_ASI_{asi}_DisplayName"] = {"en": f"Rare Feats: Ability Improvement (+{asi})"}
    loca[f"RareFeats_ASI_{asi}_Description"] = {"en": f"""
        You have {asi} points to spend across your abilities, to a maximum of 20.
        """}

    rare_feats.add_feat_descriptions([
        Lsx.Node("FeatDescription", [
            Lsx.Attribute("DisplayName", "TranslatedString", handle=loca[f"RareFeats_ASI_{asi}_DisplayName"], version="1"),
            Lsx.Attribute("Description", "TranslatedString", handle=loca[f"RareFeats_ASI_{asi}_Description"], version="1"),
            Lsx.Attribute("ExactMatch", "FixedString", value=f"AbilityScoreIncrease_{asi}"),
            Lsx.Attribute("FeatId", "guid", value=str(feat_uuid)),
            Lsx.Attribute("UUID", "guid", value=str(feat_description_uuid)),
        ]),
    ])

    rare_feats.add_feats([
        Lsx.Node("Feat", [
            Lsx.Attribute("CanBeTakenMultipleTimes", "bool", value="true"),
            Lsx.Attribute("Name", "FixedString", value=f"AbilityScoreIncrease_{asi}"),
            Lsx.Attribute("Selectors", "LSString", value=f"SelectAbilities(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,{asi},{asi},FeatASI)"),
            Lsx.Attribute("UUID", "guid", value=str(feat_uuid)),
        ]),
    ])

# Athlete without the ASI
athlete_uuid = rare_feats.make_uuid("RareFeats_Athlete")

loca["RareFeats_Athlete_DisplayName"] = {"en": "Rare Feats: Athlete"}
loca["RareFeats_Athlete_Description"] = {"en": """
    When you are Prone, standing up uses significantly less movement.
    Your <LSTag Type="Spell" Tooltip="Projectile_Jump">Jump</LSTag> distance also increases by 50%.
    """}

rare_feats.add_feat_descriptions([
    Lsx.Node("FeatDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["RareFeats_Athlete_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["RareFeats_Athlete_Description"], version="1"),
        Lsx.Attribute("ExactMatch", "FixedString", value="RareFeats_Athlete"),
        Lsx.Attribute("FeatId", "guid", value=str(athlete_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(rare_feats.make_uuid("RareFeats_FeatDescription_Athlete"))),
    ]),
])

rare_feats.add_feats([
    Lsx.Node("Feat", [
        Lsx.Attribute("Name", "FixedString", value="RareFeats_Athlete"),
        Lsx.Attribute("PassivesAdded", "LSString", value="Athlete_StandUp"),
        Lsx.Attribute("UUID", "guid", value=str(athlete_uuid)),
    ]),
])

# Lightly Armored without the ASI
lightly_armored_uuid = rare_feats.make_uuid("RareFeats_LightlyArmored")

loca["RareFeats_LightlyArmored_DisplayName"] = {"en": "Rare Feats: Lightly Armoured"}
loca["RareFeats_LightlyArmored_Description"] = {"en": """
    You gain <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Light Armour.
    """}

rare_feats.add_feat_descriptions([
    Lsx.Node("FeatDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["RareFeats_LightlyArmored_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["RareFeats_LightlyArmored_Description"], version="1"),
        Lsx.Attribute("ExactMatch", "FixedString", value="RareFeats_LightlyArmored"),
        Lsx.Attribute("FeatId", "guid", value=str(lightly_armored_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(rare_feats.make_uuid("RareFeats_FeatDescription_LightlyArmored"))),
    ]),
])

rare_feats.add_feats([
    Lsx.Node("Feat", [
        Lsx.Attribute("Name", "FixedString", value="RareFeats_LightlyArmored"),
        Lsx.Attribute("PassivesAdded", "LSString", value="LightlyArmored"),
        Lsx.Attribute("UUID", "guid", value=str(lightly_armored_uuid)),
    ]),
])

# ModeratelyArmored without the ASI
moderately_armored_uuid = rare_feats.make_uuid("RareFeats_ModeratelyArmored")

loca["RareFeats_ModeratelyArmored_DisplayName"] = {"en": "Rare Feats: Moderately Armoured"}
loca["RareFeats_ModeratelyArmored_Description"] = {"en": """
    You gain <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Medium Armour and shields.
    """}

rare_feats.add_feat_descriptions([
    Lsx.Node("FeatDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["RareFeats_ModeratelyArmored_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["RareFeats_ModeratelyArmored_Description"], version="1"),
        Lsx.Attribute("ExactMatch", "FixedString", value="RareFeats_ModeratelyArmored"),
        Lsx.Attribute("FeatId", "guid", value=str(moderately_armored_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(rare_feats.make_uuid("RareFeats_FeatDescription_ModeratelyArmored"))),
    ]),
])

rare_feats.add_feats([
    Lsx.Node("Feat", [
        Lsx.Attribute("Name", "FixedString", value="RareFeats_ModeratelyArmored"),
        Lsx.Attribute("PassivesAdded", "LSString", value="ModeratelyArmored"),
        Lsx.Attribute("Requirements", "LSString", value="FeatRequirementProficiency('LightArmor')"),
        Lsx.Attribute("UUID", "guid", value=str(moderately_armored_uuid)),
    ]),
])

# Performer without the ASI
performer_uuid = rare_feats.make_uuid("RareFeats_Performer")

loca["RareFeats_Performer_DisplayName"] = {"en": "Rare Feats: Performer"}
loca["RareFeats_Performer_Description"] = {"en": """
    You gain <LSTag Tooltip="MusicalInstrumentProficiency">Musical Instrument Proficiency</LSTag>.
    """}

rare_feats.add_feat_descriptions([
    Lsx.Node("FeatDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["RareFeats_Performer_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["RareFeats_Performer_Description"], version="1"),
        Lsx.Attribute("ExactMatch", "FixedString", value="RareFeats_Performer"),
        Lsx.Attribute("FeatId", "guid", value=str(performer_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(rare_feats.make_uuid("RareFeats_FeatDescription_Performer"))),
    ]),
])

rare_feats.add_feats([
    Lsx.Node("Feat", [
        Lsx.Attribute("Name", "FixedString", value="RareFeats_Performer"),
        Lsx.Attribute("PassivesAdded", "LSString", value="Performer"),
        Lsx.Attribute("UUID", "guid", value=str(performer_uuid)),
    ]),
])

# TavernBrawler without the ASI
tavern_brawler_uuid = rare_feats.make_uuid("RareFeats_TavernBrawler")

loca["RareFeats_TavernBrawler_DisplayName"] = {"en": "Rare Feats: Tavern Brawler"}
loca["RareFeats_TavernBrawler_Description"] = {"en": """
    When you make an unarmed attack, use an improvised weapon, or throw something, your Strength
    <LSTag Tooltip="AbilityModifier">Modifier</LSTag> is added twice to the damage and
    <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>.
    """}

rare_feats.add_feat_descriptions([
    Lsx.Node("FeatDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["RareFeats_TavernBrawler_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["RareFeats_TavernBrawler_Description"], version="1"),
        Lsx.Attribute("ExactMatch", "FixedString", value="RareFeats_TavernBrawler"),
        Lsx.Attribute("FeatId", "guid", value=str(tavern_brawler_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(rare_feats.make_uuid("RareFeats_FeatDescription_TavernBrawler"))),
    ]),
])

rare_feats.add_feats([
    Lsx.Node("Feat", [
        Lsx.Attribute("Name", "FixedString", value="RareFeats_TavernBrawler"),
        Lsx.Attribute("PassivesAdded", "LSString", value="TavernBrawler"),
        Lsx.Attribute("UUID", "guid", value=str(tavern_brawler_uuid)),
    ]),
])

# WeaponMaster without the ASI
weapon_master_uuid = rare_feats.make_uuid("RareFeats_WeaponMaster")

loca["RareFeats_WeaponMaster_DisplayName"] = {"en": "Rare Feats: Weapon Master"}
loca["RareFeats_WeaponMaster_Description"] = {"en": """
    You gain <LSTag Tooltip="Proficiency">Proficiency</LSTag> with four weapons of your choice.
    """}

rare_feats.add_feat_descriptions([
    Lsx.Node("FeatDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["RareFeats_WeaponMaster_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["RareFeats_WeaponMaster_Description"], version="1"),
        Lsx.Attribute("ExactMatch", "FixedString", value="RareFeats_WeaponMaster"),
        Lsx.Attribute("FeatId", "guid", value=str(weapon_master_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(rare_feats.make_uuid("RareFeats_FeatDescription_WeaponMaster"))),
    ]),
])

rare_feats.add_feats([
    Lsx.Node("Feat", [
        Lsx.Attribute("Name", "FixedString", value="RareFeats_WeaponMaster"),
        Lsx.Attribute("PassivesAdded", "LSString", value="WeaponMaster"),
        Lsx.Attribute("Selectors", "LSString", value="SelectPassives(f21e6b94-44e8-4ae0-a6f1-0c81abac03a2,4,WeaponMasterProficiencies)"),
        Lsx.Attribute("UUID", "guid", value=str(weapon_master_uuid)),
    ]),
])

rare_feats.build()
