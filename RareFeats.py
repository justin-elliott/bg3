#!/usr/bin/env python3
"""
Generates files for the "RareFeats" mod.
"""

import os

from moddb import (
    BattleMagic,
    CunningActions,
    Movement,
    character_level_range,
)
from modtools.gamedata import (
    InterruptData,
    PassiveData,
    StatusData,
)
from modtools.lsx.game import (
    FeatDescription,
    Feat,
    PassiveList,
)
from modtools.mod import Mod
from typing import Callable
from uuid import UUID

rare_feats = Mod(os.path.dirname(__file__),
                 author="justin-elliott",
                 name="RareFeats",
                 mod_uuid=UUID("1bfebf94-20b2-4105-bd4f-4caeb8a1fe2a"),
                 description="Adds additional feats.")

loca = rare_feats.get_localization()
loca.add_language("en", "English")


def iife(fn: Callable[[], None]) -> Callable[[], None]:
    """Immediate invoke our decorated function."""
    fn()


@iife
def no_feat() -> None:
    """A feat for when you don't wish to select a feat."""
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


@iife
def asi_feat() -> None:
    """Ability Score Improvement (ASI) feat."""
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


@iife
def athlete_feat() -> None:
    """Athlete without the ASI."""
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


@iife
def battle_magic_feat() -> None:
    """Battle Magic."""
    battle_magic = BattleMagic(rare_feats).add_battle_magic()
    battle_magic_uuid = rare_feats.make_uuid("RareFeats_BattleMagicFeat")

    loca["RareFeats_BattleMagicFeat_DisplayName"] = {"en": "Rare Feats: Battle Magic"}
    loca["RareFeats_BattleMagicFeat_Description"] = {"en": f"""
        Gain <LSTag Type="Passive" Tooltip="{battle_magic}">Battle Magic</LSTag>.
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
    cunning_actions = CunningActions(rare_feats)
    cunning_actions_uuid = rare_feats.make_uuid("RareFeats_CunningActions")

    loca["RareFeats_CunningActions_DisplayName"] = {"en": "Rare Feats: Cunning Actions"}
    loca["RareFeats_CunningActions_Description"] = {"en": f"""
        Gain <LSTag Type="Spell" Tooltip="{cunning_actions.cunning_action_dash}">Cunning Action: Dash</LSTag>,
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
        Selectors=[f"AddSpells({cunning_actions.spell_list().UUID},,,,AlwaysPrepared)"],
        UUID=cunning_actions_uuid,
    ))


@iife
def extra_attacks_feat() -> None:
    """Extra Attacks."""
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
        Properties=["Highlighted"],
    ))


@iife
def lands_stride_feat() -> None:
    """Land's Stride."""
    lands_stride_uuid = rare_feats.make_uuid("RareFeats_LandsStride")

    loca["RareFeats_LandsStride_DisplayName"] = {"en": "Rare Feats: Land's Stride"}
    loca["RareFeats_LandsStride_Description"] = {"en": """
        You gain additional movement speed, and
        <LSTag Type="Status" Tooltip="DIFFICULT_TERRAIN">Difficult Terrain</LSTag> no longer slows you down.
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


@iife
def lightly_armored_feat() -> None:
    """Lightly Armored without the ASI."""
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


@iife
def metamagic_feat() -> None:
    """Metamagic."""
    metamagic_uuid = rare_feats.make_uuid("RareFeats_Metamagic")

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
            "ActionResource(SorceryPoint,2,0)",
            *[f"IF(CharacterLevelRange({level},12)):ActionResource(SorceryPoint,2,0)" for level in range(2, 13)],
        ],
        Properties=["IsHidden"],
    ))

    loca["RareFeats_IntensifiedSpell_DisplayName"] = {"en": "Metamagic: Intensified Spell"}
    loca["RareFeats_IntensifiedSpell_Description"] = {"en": """
        When you deal damage with a spell of level 1 or higher, you can use your
        <LSTag Type="ActionResource" Tooltip="SorceryPoint">Sorcery Points</LSTag> to deal maximum damage instead.
        """}

    rare_feats.add(PassiveData(
        "RareFeats_IntensifiedSpell",
        DisplayName=loca["RareFeats_IntensifiedSpell_DisplayName"],
        Description=loca["RareFeats_IntensifiedSpell_Description"],
        TooltipUseCosts="SorceryPoint:3",
        Icon="Skill_Sorcerer_Passive_Metamagic_EmpoweredSpell",
        Boosts="UnlockInterrupt(RareFeats_IntensifiedSpellInterrupt)",
        Properties="IsHidden",
        StatsFunctorContext="OnCastResolved",
        StatsFunctors="RemoveStatus(RAREFEATS_INTENSIFIED_SPELL)",
    ))

    rare_feats.add(InterruptData(
        "RareFeats_IntensifiedSpellInterrupt",
        DisplayName=loca["RareFeats_IntensifiedSpell_DisplayName"],
        Description=loca["RareFeats_IntensifiedSpell_Description"],
        Icon="Skill_Sorcerer_Passive_Metamagic_EmpoweredSpell",
        InterruptContext="OnSpellCast",
        InterruptContextScope="Self",
        Container="YesNoDecision",
        Conditions=[
            "Self(context.Source,context.Observer) "
            "and HasFunctor(StatsFunctorType.DealDamage) "
            "and HasSpellFlag(SpellFlags.Spell) "
            "and not IsCantrip() "
            "and not AnyEntityIsItem()",
        ],
        Properties="ApplyStatus(OBSERVER_OBSERVER,RAREFEATS_INTENSIFIED_SPELL,100,1)",
        Cost="SorceryPoint:3",
        InterruptDefaultValue=["Ask", "Enabled"],
        EnableCondition="not HasStatus('SG_Polymorph') or Tagged('MINDFLAYER') or HasStatus('SG_Disguise')",
        EnableContext=["OnStatusApplied", "OnStatusRemoved"],
    ))

    rare_feats.add(StatusData(
        "RAREFEATS_INTENSIFIED_SPELL",
        StatusType="BOOST",
        DisplayName=loca["RareFeats_IntensifiedSpell_DisplayName"],
        StackId="RAREFEATS_INTENSIFIED_SPELL",
        Boosts="MinimumRollResult(Damage,20)",
        StatusPropertyFlags=["DisableOverhead", "DisableCombatlog", "DisablePortraitIndicator"],
    ))

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
        Selectors=[
            "AddSpells(979e37ad-05fa-466c-af99-9eb104a6e876,,,,AlwaysPrepared)",  # Create Sorcery, Spell Points
            f"SelectPassives({metamagic_passives_uuid},4,Metamagic)",
        ],
        UUID=metamagic_uuid,
    ))


@iife
def moderately_armored_feat() -> None:
    """Moderately Armored without the ASI."""
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


@iife
def performer_feat() -> None:
    """Performer without the ASI."""
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


@iife
def tavern_brawler_feat() -> None:
    """Tavern Brawler without the ASI."""
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


@iife
def weapon_master_feat() -> None:
    """Weapon Master without the ASI."""
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
