#!/usr/bin/env python3
"""
Generates files for the "RareFeats" mod.
"""

import os

from modtools.gamedata import passive_data
from modtools.lsx.game import FeatDescription, Feat, PassiveList
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

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_NoFeat_DisplayName"],
    Description=loca["RareFeats_NoFeat_Description"],
    ExactMatch="RareFeats_NoFeat",
    FeatId=no_feat_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_NoFeat"),
))

rare_feats.add(Feat(
    CanBeTakenMultipleTimes=True,
    Name="RareFeats_NoFeat",
    UUID=no_feat_uuid,
))

# Add Ability Score Improvement (ASI) feats
for asi in [4, 8, 16, 32, 44]:
    feat_uuid = rare_feats.make_uuid(f"feat_ASI_{asi}")
    feat_description_uuid = rare_feats.make_uuid(f"feat_description_ASI_{asi}")

    loca[f"RareFeats_ASI_{asi}_DisplayName"] = {"en": f"Rare Feats: Ability Improvement (+{asi})"}
    loca[f"RareFeats_ASI_{asi}_Description"] = {"en": f"""
        You have {asi} points to spend across your abilities, to a maximum of 20.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca[f"RareFeats_ASI_{asi}_DisplayName"],
        Description=loca[f"RareFeats_ASI_{asi}_Description"],
        ExactMatch=f"RareFeats_ASI_{asi}",
        FeatId=feat_uuid,
        UUID=feat_description_uuid,
    ))

    rare_feats.add(Feat(
        CanBeTakenMultipleTimes=True,
        Name=f"RareFeats_ASI_{asi}",
        Selectors=f"SelectAbilities(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,{asi},{asi},FeatASI)",
        UUID=feat_uuid,
    ))

# Add Ability Score Improvement (ASI) Plus feats
abilities = [
    ("Strength",     "Spell_Transmutation_EnhanceAbility_BullsStrenght"),
    ("Dexterity",    "Spell_Transmutation_EnhanceAbility_CatsGrace"),
    ("Constitution", "Spell_Transmutation_EnhanceAbility_BearsEndurance"),
    ("Intelligence", "Spell_Transmutation_EnhanceAbility_FoxsCunning"),
    ("Wisdom",       "Spell_Transmutation_EnhanceAbility_OwlsWisdom"),
    ("Charisma",     "Spell_Transmutation_EnhanceAbility_EaglesSplendor"),
]

for bonus in [4]:
    asi_plus_passives = []

    for ability, ability_icon in abilities:
        loca[f"RareFeats_ASIPlus_{ability}_{bonus}_DisplayName"] = {"en": ability}
        loca[f"RareFeats_ASIPlus_{ability}_{bonus}_Description"] = {"en": f"""
            Increase your <LSTag Tooltip="{ability}">{ability}</LSTag> by {bonus}, to a maximum of 30.
            """}

        asi_plus_passive = f"RareFeats_ASIPlus_{ability}_{bonus}"
        asi_plus_passives.append(asi_plus_passive)
        rare_feats.add(passive_data(
            asi_plus_passive,
            DisplayName=loca[f"RareFeats_ASIPlus_{ability}_{bonus}_DisplayName"],
            Description=loca[f"RareFeats_ASIPlus_{ability}_{bonus}_Description"],
            Icon=ability_icon,
            Boosts=[f"Ability({ability},{bonus},30)"],
            Properties=["IsHidden"],
        ))

    asi_plus_feat_uuid = rare_feats.make_uuid(f"feat_ASIPlus_{bonus}")
    asi_plus_feat_description_uuid = rare_feats.make_uuid(f"feat_description_ASIPlus_{bonus}")
    asi_plus_passive_list_uuid = str(rare_feats.make_uuid(f"RareFeats_ASIPlus_{bonus}_PassiveList"))

    rare_feats.add(PassiveList(
        Passives=asi_plus_passives,
        UUID=asi_plus_passive_list_uuid,
    ))

    loca[f"RareFeats_ASIPlus_{bonus}_DisplayName"] = {"en": f"Rare Feats: Ability Improvement Plus (+{bonus})"}
    loca[f"RareFeats_ASIPlus_{bonus}_Description"] = {"en": f"""
        Improve one of your abilities by {bonus}, to a maximum of 30.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca[f"RareFeats_ASIPlus_{bonus}_DisplayName"],
        Description=loca[f"RareFeats_ASIPlus_{bonus}_Description"],
        ExactMatch=f"RareFeats_ASIPlus_{bonus}",
        FeatId=asi_plus_feat_uuid,
        UUID=asi_plus_feat_description_uuid,
    ))

    rare_feats.add(Feat(
        CanBeTakenMultipleTimes=True,
        Name=f"RareFeats_ASIPlus_{bonus}",
        Selectors=f"SelectPassives({asi_plus_passive_list_uuid},1,RareFeats_ASIPlus_{bonus})",
        UUID=asi_plus_feat_uuid,
    ))

# Athlete without the ASI
athlete_uuid = rare_feats.make_uuid("RareFeats_Athlete")

loca["RareFeats_Athlete_DisplayName"] = {"en": "Rare Feats: Athlete"}
loca["RareFeats_Athlete_Description"] = {"en": """
    When you are Prone, standing up uses significantly less movement.
    Your <LSTag Type="Spell" Tooltip="Projectile_Jump">Jump</LSTag> distance also increases by 50%.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_Athlete_DisplayName"],
    Description=loca["RareFeats_Athlete_Description"],
    ExactMatch="RareFeats_Athlete",
    FeatId=athlete_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_Athlete"),
))

rare_feats.add(Feat(
    Name="RareFeats_Athlete",
    PassivesAdded="Athlete_StandUp",
    UUID=athlete_uuid,
))

# Lightly Armored without the ASI
lightly_armored_uuid = rare_feats.make_uuid("RareFeats_LightlyArmored")

loca["RareFeats_LightlyArmored_DisplayName"] = {"en": "Rare Feats: Lightly Armoured"}
loca["RareFeats_LightlyArmored_Description"] = {"en": """
    You gain <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Light Armour.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_LightlyArmored_DisplayName"],
    Description=loca["RareFeats_LightlyArmored_Description"],
    ExactMatch="RareFeats_LightlyArmored",
    FeatId=lightly_armored_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_LightlyArmored"),
))

rare_feats.add(Feat(
    Name="RareFeats_LightlyArmored",
    PassivesAdded="LightlyArmored",
    UUID=lightly_armored_uuid,
))

# ModeratelyArmored without the ASI
moderately_armored_uuid = rare_feats.make_uuid("RareFeats_ModeratelyArmored")

loca["RareFeats_ModeratelyArmored_DisplayName"] = {"en": "Rare Feats: Moderately Armoured"}
loca["RareFeats_ModeratelyArmored_Description"] = {"en": """
    You gain <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Medium Armour and shields.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_ModeratelyArmored_DisplayName"],
    Description=loca["RareFeats_ModeratelyArmored_Description"],
    ExactMatch="RareFeats_ModeratelyArmored",
    FeatId=moderately_armored_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_ModeratelyArmored"),
))

rare_feats.add(Feat(
    Name="RareFeats_ModeratelyArmored",
    PassivesAdded="ModeratelyArmored",
    Requirements="FeatRequirementProficiency('LightArmor')",
    UUID=moderately_armored_uuid,
))

# Performer without the ASI
performer_uuid = rare_feats.make_uuid("RareFeats_Performer")

loca["RareFeats_Performer_DisplayName"] = {"en": "Rare Feats: Performer"}
loca["RareFeats_Performer_Description"] = {"en": """
    You gain <LSTag Tooltip="MusicalInstrumentProficiency">Musical Instrument Proficiency</LSTag>.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_Performer_DisplayName"],
    Description=loca["RareFeats_Performer_Description"],
    ExactMatch="RareFeats_Performer",
    FeatId=performer_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_Performer"),
))

rare_feats.add(Feat(
    Name="RareFeats_Performer",
    PassivesAdded="Performer",
    UUID=performer_uuid,
))

# TavernBrawler without the ASI
tavern_brawler_uuid = rare_feats.make_uuid("RareFeats_TavernBrawler")

loca["RareFeats_TavernBrawler_DisplayName"] = {"en": "Rare Feats: Tavern Brawler"}
loca["RareFeats_TavernBrawler_Description"] = {"en": """
    When you make an unarmed attack, use an improvised weapon, or throw something, your Strength
    <LSTag Tooltip="AbilityModifier">Modifier</LSTag> is added twice to the damage and
    <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_TavernBrawler_DisplayName"],
    Description=loca["RareFeats_TavernBrawler_Description"],
    ExactMatch="RareFeats_TavernBrawler",
    FeatId=tavern_brawler_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_TavernBrawler"),
))

rare_feats.add(Feat(
    Name="RareFeats_TavernBrawler",
    PassivesAdded="TavernBrawler",
    UUID=tavern_brawler_uuid,
))

# WeaponMaster without the ASI
weapon_master_uuid = rare_feats.make_uuid("RareFeats_WeaponMaster")

loca["RareFeats_WeaponMaster_DisplayName"] = {"en": "Rare Feats: Weapon Master"}
loca["RareFeats_WeaponMaster_Description"] = {"en": """
    You gain <LSTag Tooltip="Proficiency">Proficiency</LSTag> with four weapons of your choice.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_WeaponMaster_DisplayName"],
    Description=loca["RareFeats_WeaponMaster_Description"],
    ExactMatch="RareFeats_WeaponMaster",
    FeatId=weapon_master_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_WeaponMaster"),
))

rare_feats.add(Feat(
    Name="RareFeats_WeaponMaster",
    PassivesAdded="WeaponMaster",
    Selectors="SelectPassives(f21e6b94-44e8-4ae0-a6f1-0c81abac03a2,4,WeaponMasterProficiencies)",
    UUID=weapon_master_uuid,
))

rare_feats.build()
