#!/usr/bin/env python3
"""
Generates files for the "RareFeats" mod.
"""

import os

from functools import cache
from moddb import (
    BattleMagic,
    CunningActions,
    Movement,
    character_level_range,
)
from modtools.gamedata import (
    PassiveData,
    StatusData,
)
from modtools.lsx.game import (
    CharacterAbility,
    FeatDescription,
    Feat,
    PassiveList,
    ProgressionDescription,
)
from modtools.mod import Mod
from modtools.text import Script
from typing import Callable
from uuid import UUID

rare_feats = Mod(os.path.dirname(__file__),
                 author="justin-elliott",
                 name="RareFeats",
                 mod_uuid=UUID("1bfebf94-20b2-4105-bd4f-4caeb8a1fe2a"),
                 description="Adds additional feats.")

loca = rare_feats.get_localization()
loca.add_language("en", "English")

cunning_actions = CunningActions(rare_feats)
running_jump = cunning_actions.add_running_jump()


def iife(fn: Callable[[], None]) -> Callable[[], None]:
    """Immediate invoke our decorated function."""
    fn()


@cache
def boost_ability_none_passive() -> str:
    """Return the name of a passive for no ability increase."""
    boost_ability_none = f"{rare_feats.get_prefix()}_BoostAbility_None"

    loca[f"{boost_ability_none}_DisplayName"] = {"en": "None"}
    loca[f"{boost_ability_none}_Description"] = {"en": "No ability increase."}

    rare_feats.add(PassiveData(
        boost_ability_none,
        DisplayName=loca[f"{boost_ability_none}_DisplayName"],
        Description=loca[f"{boost_ability_none}_Description"],
        Icon="Spell_Transmutation_EnhanceAbility",
        Properties=["IsHidden"],
    ))

    return boost_ability_none


@cache
def boost_ability_passive(feat: str, ability: CharacterAbility | None, boost: int) -> str:
    """Return the name of a passive to increase an ability by the given boost."""
    if ability is None:
        return boost_ability_none_passive()

    ability_name = CharacterAbility(ability).name.title()
    boost_ability = f"{rare_feats.get_prefix()}_{feat}_BoostAbility_{ability_name}_{boost}"

    loca[f"{boost_ability}_DisplayName"] = {"en": f"{ability_name} +{boost}"}
    loca[f"{boost_ability}_Description"] = {"en": f"Increase your {ability_name} by {boost}, to a maximum of 30."}

    rare_feats.add(PassiveData(
        boost_ability,
        DisplayName=loca[f"{boost_ability}_DisplayName"],
        Description=loca[f"{boost_ability}_Description"],
        Icon="Spell_Transmutation_EnhanceAbility",
        Boosts=[f"Ability({ability_name},{boost},30)"],
        Properties=["IsHidden"],
    ))

    return boost_ability


def boost_abilities_passive_list(feat: str, abilities: list[CharacterAbility | None], boost: int) -> UUID:
    """Create a PassiveList to boost the given abilities, returning its UUID."""
    passive_list = PassiveList(
        Passives=[boost_ability_passive(feat, ability, boost) for ability in abilities],
        UUID=rare_feats.make_uuid(f"RareFeats Boost Abilities Passive List {feat} {abilities}"),
    )
    rare_feats.add(passive_list)
    return passive_list.UUID


@iife
def ability_boost_feat() -> None:
    """Ability Boost feat."""
    ability_boost_passive_list = PassiveList(
        Passives=[],
        UUID=rare_feats.make_uuid("RareFeats_AbilityBoost_PassiveList"),
    )
    rare_feats.add(ability_boost_passive_list)

    for bonus in range(1, 18):
        ability_boost_passive = f"RareFeats_AbilityBoost_{bonus}"
        ability_boost_passive_list.Passives.append(ability_boost_passive)

        loca[f"{ability_boost_passive}_DisplayName"] = {"en": f"Rare Feats: Abilities +{bonus}"}
        loca[f"{ability_boost_passive}_Description"] = {"en": f"""
            Increase all of your abilities by {bonus}, to a maximum of 30.
            """}

        rare_feats.add(PassiveData(
            ability_boost_passive,
            DisplayName=loca[f"{ability_boost_passive}_DisplayName"],
            Description=loca[f"{ability_boost_passive}_Description"],
            Icon="Spell_Transmutation_EnhanceAbility",
            Boosts=[f"Ability({ability.name.title()},{bonus},30)" for ability in CharacterAbility],
            Properties=["IsHidden"],
        ))

    ability_boost_feat_uuid = rare_feats.make_uuid("RareFeats_AbilityBoost")

    loca["RareFeats_AbilityBoost_DisplayName"] = {"en": "Rare Feats: Abilities Boost"}
    loca["RareFeats_AbilityBoost_Description"] = {"en": """
        Increase all of your abilities by a selected amount, to a maximum of 30.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_AbilityBoost_DisplayName"],
        Description=loca["RareFeats_AbilityBoost_Description"],
        ExactMatch="RareFeats_AbilityBoost",
        FeatId=ability_boost_feat_uuid,
        UUID=rare_feats.make_uuid("RareFeats_AbilityBoost_FeatDescription"),
    ))

    rare_feats.add(Feat(
        Name="RareFeats_AbilityBoost",
        Selectors=f"SelectPassives({ability_boost_passive_list.UUID},1,RareFeats_AbilityBoost)",
        UUID=ability_boost_feat_uuid,
    ))


@iife
def asi_feat() -> None:
    """Ability Score Improvement (ASI) feat."""
    BONUS = 2

    asi_uuid = rare_feats.make_uuid("RareFeats_ASI")
    asi_passive_list = boost_abilities_passive_list(
        "ASI", [*[ability for ability in CharacterAbility], None], BONUS)

    loca["RareFeats_ASI_DisplayName"] = {"en": "Rare Feats: Ability Improvement"}
    loca["RareFeats_ASI_Description"] = {"en": f"""
        Increase one of your abilities by {BONUS}, to a maximum of 30.
        """}
    
    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_ASI_DisplayName"],
        Description=loca["RareFeats_ASI_Description"],
        ExactMatch="RareFeats_ASI",
        FeatId=asi_uuid,
        UUID=rare_feats.make_uuid("RareFeats_ASI_FeatDescription"),
    ))

    rare_feats.add(Feat(
        CanBeTakenMultipleTimes=True,
        Name="RareFeats_ASI",
        Selectors=f"SelectPassives({asi_passive_list},1,RareFeats_ASI)",
        UUID=asi_uuid,
    ))


@iife
def athlete_feat() -> None:
    """Athlete with additional movement speed and land's stride."""
    athlete_uuid = rare_feats.make_uuid("RareFeats_Athlete")
    fast_movement_30 = Movement(rare_feats).add_fast_movement(3.0)

    athlete_passive_list = boost_abilities_passive_list(
        "Athlete", [CharacterAbility.STRENGTH, CharacterAbility.DEXTERITY, None], 2)

    loca["RareFeats_Athlete_DisplayName"] = {"en": "Rare Feats: Athlete"}
    loca["RareFeats_Athlete_Description"] = {"en": """
        You gain additional movement speed, and
        <LSTag Type="Status" Tooltip="DIFFICULT_TERRAIN">Difficult Terrain</LSTag> no longer slows you down.
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
        PassivesAdded=[
            "Athlete_StandUp",
            fast_movement_30,
            "FOR_NightWalkers_WebImmunity",
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
        ],
        Selectors=f"SelectPassives({athlete_passive_list},1,RareFeats_Athlete)",
        UUID=athlete_uuid,
    ))


@iife
def battle_magic_feat() -> None:
    """Battle Magic."""
    battle_magic = BattleMagic(rare_feats).add_battle_magic()
    battle_magic_uuid = rare_feats.make_uuid("RareFeats_BattleMagicFeat")

    loca["RareFeats_BattleMagicFeat_DisplayName"] = {"en": "Rare Feats: Battle Magic"}
    loca["RareFeats_BattleMagicFeat_Description"] = {"en": f"""
        You gain <LSTag Type="Passive" Tooltip="{battle_magic}">Battle Magic</LSTag>.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_BattleMagicFeat_DisplayName"],
        Description=loca["RareFeats_BattleMagicFeat_Description"],
        ExactMatch="RareFeats_BattleMagicFeat",
        FeatId=battle_magic_uuid,
        UUID=rare_feats.make_uuid("RareFeats_BattleMagicFeatDescription"),
    ))

    rare_feats.add(Feat(
        Name="RareFeats_BattleMagicFeat",
        PassivesAdded=[battle_magic],
        UUID=battle_magic_uuid,
    ))


@iife
def cunning_actions_feat() -> None:
    """Cunning actions."""
    cunning_actions_uuid = rare_feats.make_uuid("RareFeats_CunningActions")

    loca["RareFeats_CunningActions_DisplayName"] = {"en": "Rare Feats: Cunning Actions"}
    loca["RareFeats_CunningActions_Description"] = {"en": f"""
        Gain <LSTag Type="Spell" Tooltip="Shout_Dash_CunningAction">Cunning Action: Dash</LSTag>,
        <LSTag Type="Spell" Tooltip="Shout_Hide_BonusAction">Cunning Action: Hide</LSTag>,
        <LSTag Type="Spell" Tooltip="Shout_Disengage_CunningAction">Cunning Action: Disengage</LSTag>,
        <LSTag Type="Passive" Tooltip="{running_jump}">Running Jump</LSTag>, and
        <LSTag Type="Passive" Tooltip="FastHands">Fast Hands</LSTag>.
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
        PassivesAdded=["FastHands", "RareFeats_CunningActions_Unlock", running_jump],
        UUID=cunning_actions_uuid,
    ))

    rare_feats.add(PassiveData(
        "RareFeats_CunningActions_Unlock",
        DisplayName=loca["RareFeats_CunningActions_DisplayName"],
        Description=loca["RareFeats_CunningActions_Description"],
        Icon="Action_Dash_Bonus",
        Boosts=[
            "UnlockSpell(Shout_Dash_CunningAction)",
            "UnlockSpell(Shout_Hide_BonusAction)",
            "UnlockSpell(Shout_Disengage_CunningAction)",
        ],
        Properties=["IsHidden"],
    ))


@iife
def evasive_feat() -> None:
    """Evasive."""
    evasive_uuid = rare_feats.make_uuid("RareFeats_EvasiveFeat")

    loca["RareFeats_EvasiveFeat_DisplayName"] = {"en": "Rare Feats: Evasive"}
    loca["RareFeats_EvasiveFeat_Description"] = {"en": """
        You gain <LSTag Type="Passive" Tooltip="Evasion">Evasion</LSTag> and
        <LSTag Type="Passive" Tooltip="UncannyDodge">Uncanny Dodge</LSTag>.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_EvasiveFeat_DisplayName"],
        Description=loca["RareFeats_EvasiveFeat_Description"],
        ExactMatch="RareFeats_EvasiveFeat",
        FeatId=evasive_uuid,
        UUID=rare_feats.make_uuid("RareFeats_EvasiveFeatDescription"),
    ))

    rare_feats.add(Feat(
        Name="RareFeats_EvasiveFeat",
        PassivesAdded=["Evasion", "UncannyDodge"],
        UUID=evasive_uuid,
    ))


@iife
def expert_feat() -> None:
    """Gain expertise in skills."""
    expert_uuid = rare_feats.make_uuid("RareFeats_Expert")

    NUMBER_OF_SKILLS = 2

    loca["RareFeats_Expert_DisplayName"] = {"en": "Rare Feats: Expert"}
    loca["RareFeats_Expert_Description"] = {"en": f"""
        You gain <LSTag Tooltip="Expertise">Expertise</LSTag> in {NUMBER_OF_SKILLS}
        <LSTag Tooltip="Skill">Skills</LSTag> of your choice that you are
        <LSTag Tooltip="Proficiency">Proficient</LSTag> in.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_Expert_DisplayName"],
        Description=loca["RareFeats_Expert_Description"],
        ExactMatch="RareFeats_Expert",
        FeatId=expert_uuid,
        UUID=rare_feats.make_uuid("RareFeats_FeatDescription_Expert"),
    ))

    rare_feats.add(Feat(
        CanBeTakenMultipleTimes=True,
        Name="RareFeats_Expert",
        Selectors=[
            f"SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,{NUMBER_OF_SKILLS})",
        ],
        UUID=expert_uuid,
    ))


@iife
def extra_attacks_feat() -> None:
    """Extra Attacks."""
    extra_attacks_uuid = rare_feats.make_uuid("RareFeats_ExtraAttacks")

    loca["RareFeats_ExtraAttacks_DisplayName"] = {"en": "Rare Feats: Extra Attacks"}
    loca["RareFeats_ExtraAttacks_Description"] = {"en": """
        You gain <LSTag Type="Spell" Tooltip="Shout_ActionSurge">Action Surge</LSTag>. At <LSTag>Level 5</LSTag> you can
        make a second <LSTag Type="Passive" Tooltip="ExtraAttack">attack</LSTag> after making an unarmed or weapon
        attack. You gain additional attacks at <LSTag>Level 11</LSTag> and <LSTag>Level 20</LSTag>.
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
        PassivesAdded=["RareFeats_ExtraAttack", "RareFeats_ActionSurge_Unlock"],
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

    rare_feats.add(PassiveData(
        "RareFeats_ExtraAttack",
        DisplayName=loca["RareFeats_ExtraAttacks_DisplayName"],
        Description=loca["RareFeats_ExtraAttacks_Description"],
        StatsFunctorContext=["OnCreate", "OnLongRest", "OnShortRest", "OnAttack"],
        StatsFunctors=[
            "IF(CharacterLevelRange(5,10)):ApplyStatus(SELF,RARE_FEATS_EXTRA_ATTACK_1,100,-1)",
            "IF(CharacterLevelRange(11,19)):ApplyStatus(SELF,RARE_FEATS_EXTRA_ATTACK_2,100,-1)",
            "IF(CharacterLevelRange(20,20)):ApplyStatus(SELF,RARE_FEATS_EXTRA_ATTACK_3,100,-1)",
        ],
    ))

    rare_feats.add(StatusData(
        "RARE_FEATS_EXTRA_ATTACK_1",
        StatusType="BOOST",
        DisplayName=loca["RareFeats_ExtraAttacks_DisplayName"],
        Icon="PassiveFeature_ExtraAttack",
        Passives=["ExtraAttack"],
        StackId="RARE_FEATS_EXTRA_ATTACK",
        StatusPropertyFlags=["DisableOverhead", "IgnoreResting", "DisableCombatlog", "DisablePortraitIndicator"],
    ))

    rare_feats.add(StatusData(
        "RARE_FEATS_EXTRA_ATTACK_2",
        using="RARE_FEATS_EXTRA_ATTACK_1",
        StatusType="BOOST",
        Passives=["ExtraAttack_2"],
    ))

    rare_feats.add(StatusData(
        "RARE_FEATS_EXTRA_ATTACK_3",
        using="RARE_FEATS_EXTRA_ATTACK_1",
        StatusType="BOOST",
        Passives=["ExtraAttack_3"],
    ))


@iife
def fighting_style_feat() -> None:
    """Fighting Style."""
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


@iife
def jack_of_all_trades_feat() -> None:
    """Jack of all Trades."""
    jack_of_all_trades_uuid = rare_feats.make_uuid("RareFeats_JackOfAllTrades")

    loca["RareFeats_JackOfAllTrades_DisplayName"] = {"en": "Rare Feats: Jack of All Trades"}
    loca["RareFeats_JackOfAllTrades_Description"] = {"en": """
        You gain <LSTag Type="Passive" Tooltip="JackOfAllTrades">Jack of All Trades</LSTag> and
        <LSTag Type="Passive" Tooltip="ReliableTalent">Reliable Talent</LSTag>.
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
        PassivesAdded=["JackOfAllTrades", "ReliableTalent"],
        UUID=jack_of_all_trades_uuid,
    ))


@iife
def heavily_armored_feat() -> None:
    """Heavily Armored with +2 Strength ASI."""
    heavily_armored_uuid = rare_feats.make_uuid("RareFeats_HeavilyArmored")

    loca["RareFeats_HeavilyArmored_DisplayName"] = {"en": "Rare Feats: Heavily Armoured"}
    loca["RareFeats_HeavilyArmored_Description"] = {"en": """
        You gain <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Heavy Armour and your
        <LSTag Tooltip="Strength">Strength</LSTag> increases by 2, to a maximum of 30.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_HeavilyArmored_DisplayName"],
        Description=loca["RareFeats_HeavilyArmored_Description"],
        ExactMatch="RareFeats_HeavilyArmored",
        FeatId=heavily_armored_uuid,
        UUID=rare_feats.make_uuid("RareFeats_FeatDescription_HeavilyArmored"),
    ))

    rare_feats.add(Feat(
        Name="RareFeats_HeavilyArmored",
        PassivesAdded="RareFeats_HeavilyArmored",
        Requirements="FeatRequirementProficiency('MediumArmor')",
        UUID=heavily_armored_uuid,
    ))

    rare_feats.add(PassiveData(
        "RareFeats_HeavilyArmored",
        DisplayName=loca["RareFeats_HeavilyArmored_DisplayName"],
        Description=loca["RareFeats_HeavilyArmored_Description"],
        Icon="PassiveFeature_HeavilyArmored",
        Boosts=["Ability(Strength,2,30)", "Proficiency(HeavyArmor)"],
        Properties=["Highlighted"],
    ))


@iife
def heavy_armor_master_feat() -> None:
    """Heavy Armor Master with +2 Strength ASI."""
    heavy_armor_master_uuid = rare_feats.make_uuid("RareFeats_HeavyArmorMaster")

    loca["RareFeats_HeavyArmorMaster_DisplayName"] = {"en": "Rare Feats: Heavy Armor Master"}
    loca["RareFeats_HeavyArmorMaster_Description"] = {"en": """
        Your <LSTag Tooltip="Strength">Strength</LSTag> increases by 2, to a maximum of 30.
        
        Incoming damage from non-magical attacks also decreases by 3 while you're wearing heavy armour.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_HeavyArmorMaster_DisplayName"],
        Description=loca["RareFeats_HeavyArmorMaster_Description"],
        ExactMatch="RareFeats_HeavyArmorMaster",
        FeatId=heavy_armor_master_uuid,
        UUID=rare_feats.make_uuid("RareFeats_FeatDescription_HeavyArmorMaster"),
    ))

    rare_feats.add(Feat(
        Name="RareFeats_HeavyArmorMaster",
        PassivesAdded="RareFeats_HeavyArmorMaster",
        Requirements="FeatRequirementProficiency('HeavyArmor')",
        UUID=heavy_armor_master_uuid,
    ))

    rare_feats.add(PassiveData(
        "RareFeats_HeavyArmorMaster",
        DisplayName=loca["RareFeats_HeavyArmorMaster_DisplayName"],
        Description=loca["RareFeats_HeavyArmorMaster_Description"],
        Icon="PassiveFeature_HeavyArmorMaster",
        Boosts=[
            "Ability(Strength,2,30)",
            "IF(HasHeavyArmor() and not HasDamageEffectFlag(DamageFlags.Magical)):DamageReduction(Bludgeoning,Flat,3)",
            "IF(HasHeavyArmor() and not HasDamageEffectFlag(DamageFlags.Magical)):DamageReduction(Piercing,Flat,3)",
            "IF(HasHeavyArmor() and not HasDamageEffectFlag(DamageFlags.Magical)):DamageReduction(Slashing,Flat,3)",
        ],
        Properties=["Highlighted"],
    ))


@iife
def lightly_armored_feat() -> None:
    """Lightly Armored with optional ASI."""
    lightly_armored_uuid = rare_feats.make_uuid("RareFeats_LightlyArmored")
    lightly_armored_passive_list = boost_abilities_passive_list(
        "LightlyArmored", [CharacterAbility.STRENGTH, CharacterAbility.DEXTERITY, None], 2)

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
        Selectors=f"SelectPassives({lightly_armored_passive_list},1,RareFeats_LightlyArmored)",
        UUID=lightly_armored_uuid,
    ))


@iife
def martial_adept_feat() -> None:
    """Martial Adept."""
    martial_adept_uuid = rare_feats.make_uuid("RareFeats_MartialAdept")

    loca["RareFeats_MartialAdept_DisplayName"] = {"en": "Rare Feats: Martial Adept"}
    loca["RareFeats_MartialAdept_Description"] = {"en": """
        You learn five manoeuvres from the Battle Master subclass and gain a
        <LSTag Type="ActionResource" Tooltip="SuperiorityDie">Superiority Die</LSTag> to fuel them. You regain expended
        Superiority Dice after a <LSTag Tooltip="ShortRest">Short</LSTag> or
        <LSTag Tooltip="LongRest">Long Rest</LSTag>.
        """}
    loca["RareFeats_SuperiorityDice_Description"] = {"en": """
        You receive an (additional) superiority die each level.
        """}

    rare_feats.add(PassiveData(
        "RareFeats_SuperiorityDice",
        DisplayName=loca["RareFeats_MartialAdept_DisplayName"],
        Description=loca["RareFeats_SuperiorityDice_Description"],
        Icon="PassiveFeature_MartialAdept",
        Properties=["Highlighted"],
        Boosts=[
            f"ActionResource(SuperiorityDie,1,0)",
            *[
                f"IF(CharacterLevelRange({level},20)):ActionResource(SuperiorityDie,1,0)"
                for level in range(2, 21)
            ],
        ],
    ))

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_MartialAdept_DisplayName"],
        Description=loca["RareFeats_MartialAdept_Description"],
        ExactMatch="RareFeats_MartialAdept",
        FeatId=martial_adept_uuid,
        UUID=rare_feats.make_uuid("RareFeats_MartialAdeptFeatDescription"),
    ))

    rare_feats.add(Feat(
        Name="RareFeats_MartialAdept",
        PassivesAdded=["RareFeats_SuperiorityDice"],
        Selectors=[f"SelectPassives(e51a2ef5-3663-43f9-8e74-5e28520323f1,5,MAManeuvers)"],
        UUID=martial_adept_uuid,
    ))


@iife
def metamagic_feat() -> None:
    """Metamagic."""
    metamagic_uuid = rare_feats.make_uuid("RareFeats_Metamagic")

    POINTS_PER_LEVEL = 2

    loca["RareFeats_SorceryPoints_DisplayName"] = {"en": "Sorcery Points"}
    loca["RareFeats_SorceryPoints_Description"] = {"en": """
        You gain <LSTag Type="ActionResource" Tooltip="SorceryPoint">Sorcery Points</LSTag>,
        which can be used to alter spells.
        """}

    rare_feats.add(character_level_range)
    rare_feats.add(PassiveData(
        "RareFeats_SorceryPoints",
        DisplayName=loca["RareFeats_SorceryPoints_DisplayName"],
        Description=loca["RareFeats_SorceryPoints_Description"],
        Icon="statIcons_WildMagic_SorceryPoints",
        Boosts=[
            f"ActionResource(SorceryPoint,{POINTS_PER_LEVEL},0)",
            *[
                f"IF(CharacterLevelRange({level},20)):ActionResource(SorceryPoint,{POINTS_PER_LEVEL},0)"
                for level in range(2, 21)
            ],
        ],
        Properties=["IsHidden"],
    ))

    loca["RareFeats_IntensifiedSpell_DisplayName"] = {"en": "Metamagic: Intensified Spell"}
    loca["RareFeats_IntensifiedSpell_Description"] = {"en": """
        When you deal damage with a spell of level 1 or higher, you can use your
        <LSTag Type="ActionResource" Tooltip="SorceryPoint">Sorcery Points</LSTag> to deal maximum damage instead.

        Costs 1 Sorcery Point per <LSTag Tooltip="SpellSlot">spell slot</LSTag> level used.
        """}

    rare_feats.add(PassiveData(
        "RareFeats_IntensifiedSpell",
        DisplayName=loca["RareFeats_IntensifiedSpell_DisplayName"],
        Description=loca["RareFeats_IntensifiedSpell_Description"],
        Icon="Skill_Sorcerer_Passive_Metamagic_EmpoweredSpell",
        EnabledConditions=["HasActionResource('SorceryPoint',1,0,false,false,context.Source)"],
        EnabledContext=["OnCastResolved", "OnLongRest", "OnActionResourcesChanged"],
        Properties=["IsToggled", "ToggledDefaultAddToHotbar", "MetaMagic"],
        Boosts=[
            "MinimumRollResult(Damage,20)",
            "UnlockSpellVariant(RareFeats_IntensifiedSpellCheck(),"
            + "ModifyUseCosts(Add,SorceryPoint,SpellPowerLevel,0),"
            + "ModifyIconGlow(),"
            + "ModifyTooltipDescription())",
        ],
        ToggleOnEffect="VFX_Spells_Cast_Sorcerer_Metamagic_Empowered_HeadFX_01:Dummy_HeadFX",
        ToggleOffContext="OnCastResolved",
        ToggleGroup="Metamagic",
    ))

    rare_feats.add(ProgressionDescription(
        Hidden=True,
        PassivePrototype="RareFeats_IntensifiedSpell",
        Type="UnlockSpellVariant",
        UUID=rare_feats.make_uuid("RareFeats_IntensifiedSpell_ProgressionDescription"),
    ))

    rare_feats.add(Script("""
        -- Check that the current action represents a spell that can be intensified.
        function RareFeats_IntensifiedSpellCheck()
            return HasSpellFlag(SpellFlags.Spell) &
                   (HasFunctor(StatsFunctorType.DealDamage) | SpellId('Projectile_ChromaticOrb')) &
                   ~HasFunctor(StatsFunctorType.Summon) &
                   ~IsCantrip()
        end
        """))

    metamagic_passives_uuid = rare_feats.make_uuid("RareFeats_Metamagic_Passives")
    rare_feats.add(PassiveList(
        Passives=[
            "Metamagic_Careful",
            "Metamagic_Distant",
            "Metamagic_Extended",
            "Metamagic_Heightened",
            "RareFeats_IntensifiedSpell",
            "Metamagic_Quickened",
            "Metamagic_Subtle",
            "Metamagic_Twinned",
        ],
        UUID=metamagic_passives_uuid,
    ))

    loca["RareFeats_Metamagic_DisplayName"] = {"en": "Rare Feats: Metamagic"}
    loca["RareFeats_Metamagic_Description"] = {"en": """
        You gain Metamagic abilities, which can be used to alter spells.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_Metamagic_DisplayName"],
        Description=loca["RareFeats_Metamagic_Description"],
        ExactMatch="RareFeats_Metamagic",
        FeatId=metamagic_uuid,
        UUID=rare_feats.make_uuid("RareFeats_MetamagicFeatDescription"),
    ))

    rare_feats.add(Feat(
        Name="RareFeats_Metamagic",
        PassivesAdded=["RareFeats_SorceryPoints"],
        Selectors=[f"SelectPassives({metamagic_passives_uuid},4,Metamagic)"],
        UUID=metamagic_uuid,
    ))


@iife
def moderately_armored_feat() -> None:
    """Moderately Armored with optional ASI."""
    moderately_armored_uuid = rare_feats.make_uuid("RareFeats_ModeratelyArmored")
    moderately_armored_passive_list = boost_abilities_passive_list(
        "ModeratelyArmored", [CharacterAbility.STRENGTH, CharacterAbility.DEXTERITY, None], 2)

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
        Selectors=f"SelectPassives({moderately_armored_passive_list},1,RareFeats_ModeratelyArmored)",
        UUID=moderately_armored_uuid,
    ))


@iife
def performer_feat() -> None:
    """Performer with optional ASI."""
    performer_uuid = rare_feats.make_uuid("RareFeats_Performer")
    performer_passive_list = boost_abilities_passive_list(
        "Performer", [CharacterAbility.CHARISMA, None], 2)

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
        Selectors=f"SelectPassives({performer_passive_list},1,RareFeats_Performer)",
        UUID=performer_uuid,
    ))


@iife
def running_jump_feat() -> None:
    """Cunning actions."""
    running_jump_uuid = rare_feats.make_uuid("RareFeats_RunningJump")

    loca["RareFeats_RunningJump_DisplayName"] = {"en": "Rare Feats: Running Jump"}
    loca["RareFeats_RunningJump_Description"] = {"en": f"""
        You gain <LSTag Type="Passive" Tooltip="{running_jump}">Running Jump</LSTag>.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_RunningJump_DisplayName"],
        Description=loca["RareFeats_RunningJump_Description"],
        ExactMatch="RareFeats_RunningJump",
        FeatId=running_jump_uuid,
        UUID=rare_feats.make_uuid("RareFeats_FeatDescription_RunningJump"),
    ))

    rare_feats.add(Feat(
        Name="RareFeats_RunningJump",
        PassivesAdded=[running_jump],
        UUID=running_jump_uuid,
    ))


@iife
def skilled_feat() -> None:
    """Skilled with additional selections."""
    skilled_uuid = rare_feats.make_uuid("RareFeats_Skilled")

    NUMBER_OF_SKILLS = 4

    loca["RareFeats_Skilled_DisplayName"] = {"en": "Rare Feats: Skilled"}
    loca["RareFeats_Skilled_Description"] = {"en": f"""
        You gain <LSTag Tooltip="Proficiency">Proficiency</LSTag> in {NUMBER_OF_SKILLS}
        <LSTag Tooltip="Skill">Skills</LSTag> of your
        choice.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_Skilled_DisplayName"],
        Description=loca["RareFeats_Skilled_Description"],
        ExactMatch="RareFeats_Skilled",
        FeatId=skilled_uuid,
        UUID=rare_feats.make_uuid("RareFeats_FeatDescription_Skilled"),
    ))

    rare_feats.add(Feat(
        CanBeTakenMultipleTimes=True,
        Name="RareFeats_Skilled",
        Selectors=[
            f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{NUMBER_OF_SKILLS},SkilledSkills)",
        ],
        UUID=skilled_uuid,
    ))


@iife
def tavern_brawler_feat() -> None:
    """Tavern Brawler with optional ASI."""
    tavern_brawler_uuid = rare_feats.make_uuid("RareFeats_TavernBrawler")

    tavern_brawler_passive_list = boost_abilities_passive_list(
        "TavernBrawler", [CharacterAbility.STRENGTH, CharacterAbility.CONSTITUTION, None], 2)

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
        Selectors=f"SelectPassives({tavern_brawler_passive_list},1,RareFeats_TavernBrawler)",
        UUID=tavern_brawler_uuid,
    ))


@iife
def volley_feat() -> None:
    """Volley and Whirlwind from the Ranger Hunter subclass."""
    volley_uuid = rare_feats.make_uuid("RareFeats_Volley")

    loca["RareFeats_Volley_DisplayName"] = {"en": "Rare Feats: Volley"}
    loca["RareFeats_Volley_Description"] = {"en": """
        You gain the <LSTag Type="Spell" Tooltip="Target_Volley">Volley</LSTag> and
        <LSTag Type="Spell" Tooltip="Shout_Whirlwind">Whirlwind</LSTag> abilities.
        """}

    rare_feats.add(FeatDescription(
        DisplayName=loca["RareFeats_Volley_DisplayName"],
        Description=loca["RareFeats_Volley_Description"],
        ExactMatch="RareFeats_Volley",
        FeatId=volley_uuid,
        UUID=rare_feats.make_uuid("RareFeats_FeatDescription_Volley"),
    ))

    rare_feats.add(Feat(
        Name="RareFeats_Volley",
        Selectors=["AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a,,,,AlwaysPrepared)"],
        UUID=volley_uuid,
    ))


@iife
def weapon_master_feat() -> None:
    """Weapon Master with optional ASI."""
    weapon_master_uuid = rare_feats.make_uuid("RareFeats_WeaponMaster")
    weapon_master_passive_list = boost_abilities_passive_list(
        "WeaponMaster", [CharacterAbility.STRENGTH, CharacterAbility.DEXTERITY, None], 2)

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
        Selectors=[
            "SelectPassives(f21e6b94-44e8-4ae0-a6f1-0c81abac03a2,4,WeaponMasterProficiencies)",
            f"SelectPassives({weapon_master_passive_list},1,RareFeats_WeaponMaster)",
        ],
        UUID=weapon_master_uuid,
    ))


rare_feats.build()
