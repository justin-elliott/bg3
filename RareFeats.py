#!/usr/bin/env python3
"""
Generates files for the "RareFeats" mod.
"""

import os

from moddb import CunningActions, Movement
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    FeatDescription,
    Feat,
    PassiveList,
)
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

# Add Ability Score Improvement (ASI) feat
ABILITIES = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

asi_passive_list = PassiveList(
    Passives=[],
    UUID=rare_feats.make_uuid("RareFeats_ASI_PassiveList"),
)
rare_feats.add(asi_passive_list)

for bonus in range(2, 18, 2):
    asi_passive = f"RareFeats_ASI_{bonus}"
    asi_passive_list.Passives.append(asi_passive)

    loca[f"{asi_passive}_DisplayName"] = {"en": f"Rare Feats: Abilities +{bonus}"}
    loca[f"{asi_passive}_Description"] = {"en": f"""
        Increase all of your abilities by {bonus}, to a maximum of 30.
        """}

    rare_feats.add(PassiveData(
        asi_passive,
        DisplayName=loca[f"{asi_passive}_DisplayName"],
        Description=loca[f"{asi_passive}_Description"],
        Icon="Spell_Transmutation_EnhanceAbility",
        Boosts=[f"Ability({ability},{bonus},30)" for ability in ABILITIES],
        Properties=["IsHidden"],
    ))

asi_feat_uuid = rare_feats.make_uuid("RareFeats_ASI")

loca["RareFeats_ASI_DisplayName"] = {"en": "Rare Feats: Ability Improvement"}
loca["RareFeats_ASI_Description"] = {"en": """
    Increase all of your abilities by a selected amount, to a maximum of 30.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_ASI_DisplayName"],
    Description=loca["RareFeats_ASI_Description"],
    ExactMatch="RareFeats_ASI",
    FeatId=asi_feat_uuid,
    UUID=rare_feats.make_uuid("RareFeats_ASI_FeatDescription"),
))

rare_feats.add(Feat(
    Name="RareFeats_ASI",
    Selectors=f"SelectPassives({asi_passive_list.UUID},1,RareFeats_ASI)",
    UUID=asi_feat_uuid,
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
    PassivesAdded=["Athlete_StandUp"],
    UUID=athlete_uuid,
))

# Cunning actions
cunning_actions = CunningActions(rare_feats)
cunning_actions_uuid = rare_feats.make_uuid("RareFeats_CunningActions")

loca["RareFeats_CunningActions_DisplayName"] = {"en": "Rare Feats: Cunning Actions"}
loca["RareFeats_CunningActions_Description"] = {"en": f"""
    Adds <LSTag Type="Spell" Tooltip="{cunning_actions.cunning_action_dash}">Cunning Action: Dash</LSTag>,
    <LSTag Type="Spell" Tooltip="Shout_Hide_BonusAction">Cunning Action: Hide</LSTag>, and
    <LSTag Type="Spell" Tooltip="Shout_Disengage_CunningAction">Cunning Action: Disengage</LSTag>.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_CunningActions_DisplayName"],
    Description=loca["RareFeats_CunningActions_Description"],
    ExactMatch="RareFeats_CunningActions",
    FeatId=cunning_actions_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_CunningActions"),
))

rare_feats.add(Feat(
    Name="RareFeats_CunningActions",
    Selectors=[f"AddSpells({cunning_actions.spell_list()},,,,AlwaysPrepared)"],
    UUID=cunning_actions_uuid,
))

# Extra Attacks
extra_attacks_uuid = rare_feats.make_uuid("RareFeats_ExtraAttacks")

loca["RareFeats_ExtraAttacks_DisplayName"] = {"en": "Rare Feats: Extra Attacks"}
loca["RareFeats_ExtraAttacks_Description"] = {"en": """
    Gain <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>,
    <LSTag Type="Passive" Tooltip="FastHands">Fast Hands</LSTag>, and
    <LSTag Type="Spell" Tooltip="Shout_ActionSurge">Action Surge</LSTag>.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_ExtraAttacks_DisplayName"],
    Description=loca["RareFeats_ExtraAttacks_Description"],
    ExactMatch="RareFeats_ExtraAttacks",
    FeatId=extra_attacks_uuid,
    UUID=rare_feats.make_uuid("RareFeats_ExtraAttacks_FeatDescription"),
))

rare_feats.add(Feat(
    Name="RareFeats_ExtraAttacks",
    PassivesAdded=["ExtraAttack", "FastHands", "RareFeats_ActionSurge_Unlock"],
    UUID=extra_attacks_uuid,
))

rare_feats.add(PassiveData(
    "RareFeats_ActionSurge_Unlock",
    DisplayName="ha19696e1gf837g4665g86feg7e149abcfa12;1",
    Description="h0ef20d23g3616g4c1cg8300gb41624ac5de7;7",
    Icon="Skill_Fighter_ActionSurge",
    Boosts=["UnlockSpell(Shout_ActionSurge)"],
    Properties=["IsHidden"],
))

# Fighting Style
fighting_style_uuid = rare_feats.make_uuid("RareFeats_FightingStyle")

loca["RareFeats_FightingStyle_DisplayName"] = {"en": "Rare Feats: Fighting Style"}
loca["RareFeats_FightingStyle_Description"] = {"en": """
    Adopt a particular style of fighting as your specialty.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_FightingStyle_DisplayName"],
    Description=loca["RareFeats_FightingStyle_Description"],
    ExactMatch="RareFeats_FightingStyle",
    FeatId=fighting_style_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_FightingStyle"),
))

rare_feats.add(Feat(
    CanBeTakenMultipleTimes=True,
    Name="RareFeats_FightingStyle",
    Selectors=["SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)"],
    UUID=fighting_style_uuid,
))

# Jack of all Trades
jack_of_all_trades_uuid = rare_feats.make_uuid("RareFeats_JackOfAllTrades")

loca["RareFeats_JackOfAllTrades_DisplayName"] = {"en": "Rare Feats: Jack of All Trades"}
loca["RareFeats_JackOfAllTrades_Description"] = {"en": """
    Your vast experiences make you more likely to succeed in any undertaking. Add your
    <LSTag Tooltip="ProficiencyBonus">Proficiency Bonus</LSTag> to all
    <LSTag Tooltip="AbilityCheck">Ability Checks</LSTag>.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_JackOfAllTrades_DisplayName"],
    Description=loca["RareFeats_JackOfAllTrades_Description"],
    ExactMatch="RareFeats_JackOfAllTrades",
    FeatId=jack_of_all_trades_uuid,
    UUID=rare_feats.make_uuid("RareFeats_FeatDescription_JackOfAllTrades"),
))

rare_feats.add(Feat(
    Name="RareFeats_JackOfAllTrades",
    PassivesAdded=["RareFeats_JackOfAllTrades"],
    UUID=jack_of_all_trades_uuid,
))

rare_feats.add(PassiveData(
    "RareFeats_JackOfAllTrades",
    DisplayName=loca["RareFeats_JackOfAllTrades_DisplayName"],
    Description=loca["RareFeats_JackOfAllTrades_Description"],
    Icon="PassiveFeature_JackOfAllTrades",
    Boosts=[
        "RollBonus(SkillCheck,ProficiencyBonus)",
        "RollBonus(RawAbility,ProficiencyBonus)",
    ],
))

# Land's Stride
lands_stride_uuid = rare_feats.make_uuid("RareFeats_LandsStride")

loca["RareFeats_LandsStride_DisplayName"] = {"en": "Rare Feats: Land's Stride"}
loca["RareFeats_LandsStride_Description"] = {"en": """
    You gain additional movement speed, and <LSTag Type="Status" Tooltip="DIFFICULT_TERRAIN">Difficult Terrain</LSTag>
    no longer slows you down.
    """}

rare_feats.add(FeatDescription(
    DisplayName=loca["RareFeats_LandsStride_DisplayName"],
    Description=loca["RareFeats_LandsStride_Description"],
    ExactMatch="RareFeats_LandsStride",
    FeatId=lands_stride_uuid,
    UUID=rare_feats.make_uuid("RareFeats_LandsStride_FeatDescription"),
))

fast_movement_30 = Movement(rare_feats).add_fast_movement(3.0)

rare_feats.add(Feat(
    Name="RareFeats_LandsStride",
    PassivesAdded=[
        fast_movement_30,
        "LandsStride_DifficultTerrain",
        "LandsStride_Surfaces",
        "LandsStride_Advantage",
    ],
    UUID=lands_stride_uuid,
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
