#!/usr/bin/env python3
"""
Generates files for the "DaughterOfDarkness" mod.
"""

import os

from moddb.battlemagic import BattleMagic
from moddb.bolster import Bolster
from moddb.empoweredspells import EmpoweredSpells
from moddb.movement import Movement
from moddb.progression import allow_improvement, multiply_resources
from moddb.scripts import character_level_range
from modtools.gamedata import passive_data, spell_data, status_data, weapon_data
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
    GameObjects,
    LevelMapSeries,
)
from modtools.lsx import Lsx
from modtools.lsx.game import Progression, SpellList
from modtools.mod import Mod
from uuid import UUID

CLASS_DESCRIPTION_PATH = "Shared.pak/Public/Shared/ClassDescriptions/ClassDescriptions.lsx"

PROGRESSIONS_LSX_PATH = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
PROGRESSIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"

daughter_of_darkness = Mod(os.path.dirname(__file__),
                           author="justin-elliott",
                           name="DaughterOfDarkness",
                           mod_uuid=UUID("225bcb03-1c2f-4e01-a4e1-93ae05f14783"),
                           description="Upgrades the Cleric Trickery domain subclass.")

daughter_of_darkness.add_script(character_level_range)

loca = daughter_of_darkness.get_localization()

# Add passives and spells
battle_magic = BattleMagic(daughter_of_darkness).add_battle_magic()
bolster = Bolster(daughter_of_darkness).add_bolster()
empowered_spells = EmpoweredSpells(daughter_of_darkness).add_empowered_spells(CharacterAbility.WISDOM)

movement = Movement(daughter_of_darkness)
fast_movement = movement.add_fast_movement(3.0)
shadow_step = movement.add_shadow_step()

daughter_of_darkness.add(passive_data(
    "DaughterOfDarkness_PassWithoutTrace",
    DisplayName="h2b6ab85cg8d21g4c23g895eg6b8a61fdabab;1",
    Description="h5d1c1f49g43a6g44e0g807cgeb572b500fe2;6",
    Icon="Spell_Abjuration_PassWithoutTrace",
    Properties=["Highlighted", "IsToggled", "ToggledDefaultAddToHotbar"],
    ToggleOnFunctors=["ApplyStatus(SELF,PASS_WITHOUT_TRACE_AURA,100,-1)"],
    ToggleOffFunctors=["RemoveStatus(SELF,PASS_WITHOUT_TRACE_AURA)"],
))

daughter_of_darkness.add(spell_data(
    "DaughterOfDarkness_ViciousMockery",
    using="Target_ViciousMockery",
    SpellType="Target",
    SpellSuccess=[
        "ApplyStatus(VICIOUSMOCKERY,100,1)",
        "DealDamage(LevelMapValue(DaughterOfDarkness_ViciousMockeryValue),Psychic,Magical)",
    ],
    SpellFail=[
        "IF(HasPassive('PotentCantrip',context.Source)):"
        + "DealDamage((LevelMapValue(DaughterOfDarkness_ViciousMockeryValue)/2),Psychic,Magical)",
    ],
    TooltipDamageList=[
        "DealDamage(LevelMapValue(DaughterOfDarkness_ViciousMockeryValue),Psychic)",
    ],
))

daughter_of_darkness.add(LevelMapSeries(
    **{f"Level{level}": f"{level // 5 + 2}d4" for level in range(1, 21)},
    Name="DaughterOfDarkness_ViciousMockeryValue",
    UUID=daughter_of_darkness.make_uuid("DaughterOfDarkness_ViciousMockeryValue"),
))

# Add the Night's Edge
loca["DaughterOfDarkness_NightsEdge_DisplayName"] = {"en": "Night's Edge"}
loca["DaughterOfDarkness_NightsEdge_Description"] = {"en": """
    This blade is enveloped in shadow.
    """}

katana_uuid = UUID("7050c02e-f0e1-46b8-9400-2514805ecd2e")

nights_edge_game_objects_uuid = daughter_of_darkness.make_uuid("NightsEdge_GameObjects")
daughter_of_darkness.add(GameObjects(
    DisplayName=loca["DaughterOfDarkness_NightsEdge_DisplayName"],
    Description=loca["DaughterOfDarkness_NightsEdge_Description"],
    LevelName="",
    MapKey=nights_edge_game_objects_uuid,
    Name="DaughterOfDarkness_NightsEdge_Sword",
    ParentTemplateId=katana_uuid,
    Stats="DaughterOfDarkness_NightsEdge_Sword",
    Type="item",
    children=[
        GameObjects.StatusList(
            children=[
                GameObjects.StatusList.Status(
                    Object="DAUGHTEROFDARKNESS_NIGHTSEDGE",
                ),
            ],
        ),
    ],
))

daughter_of_darkness.add(status_data(
    "DAUGHTEROFDARKNESS_NIGHTSEDGE",
    using="SHADOW_BLADE",
    StatusType="EFFECT",
    Boosts=[],
    StatusEffect="ae580720-fde4-4596-b671-b5280cdbe9eb",  # UND_BOOOALSERVANT_WEAPON_StatusEffect
))

daughter_of_darkness.add(weapon_data(
    "DaughterOfDarkness_NightsEdge_Sword",
    using="WPN_Greatsword",
    RootTemplate=str(nights_edge_game_objects_uuid),
    Rarity="Legendary",
    BoostsOnEquipMainHand=[
        "UnlockSpell(Target_PommelStrike)",
        "UnlockSpell(Target_Slash_New)",
        "UnlockSpell(DaughterOfDarkness_NightsEdge_Cleave)",
    ],
    DefaultBoosts=[
        "IF(CharacterLevelRange(7,11)):ReduceCriticalAttackThreshold(1)",
        "IF(CharacterLevelRange(12,20)):ReduceCriticalAttackThreshold(2)",
        "IF(CharacterLevelRange(1,5)):WeaponEnchantment(1)",
        "IF(CharacterLevelRange(6,10)):WeaponEnchantment(2)",
        "IF(CharacterLevelRange(11,20)):WeaponEnchantment(3)",
        "WeaponDamage(1d4,Force,Magical)",
    ],
    PassivesOnEquip=["DaughterOfDarkness_NightsAegis"],
    Weapon_Properties=[
        "Dippable",
        "Heavy",
        "Magical",
        "Melee",
        "Twohanded",
    ],
    Unique="1",
))

loca["DaughterOfDarkness_NightsAegis_DisplayName"] = {"en": "Night's Aegis"}
loca["DaughterOfDarkness_NightsAegis_Description"] = {"en": """
    The magic of your blade forms a barrier around you that protects you from harm, and causes you to inflict additional
    force damage.
    """}
loca["DaughterOfDarkness_NightsAegis_StatusDescription"] = {"en": """
    Your barrier blocks damage equal to its charges and then loses 1 charge.

    While the barrier is active, you deal additional force damage equal to the number of charges remaining.
    Dealing damage with the Night's Edge adds 1 charge, up to half your level, rounded up.
    """}

daughter_of_darkness.add(passive_data(
    "DaughterOfDarkness_NightsAegis",
    DisplayName=loca["DaughterOfDarkness_NightsAegis_DisplayName"],
    Description=loca["DaughterOfDarkness_NightsAegis_Description"],
    Icon="PassiveFeature_ArcaneWard",
    PriorityOrder="2",
    Properties=["Highlighted", "OncePerAttack"],
    StatsFunctorContext=["OnDamage"],
    Conditions="AttackedWithPassiveSourceWeapon() and "
               "StatusDurationLessThan(context.Source,'DAUGHTEROFDARKNESS_NIGHTSAEGIS',context.Source.Level/2)",
    StatsFunctors=[
        "ApplyStatus(SELF,DAUGHTEROFDARKNESS_NIGHTSAEGIS,100,Target.DAUGHTEROFDARKNESS_NIGHTSAEGIS.Duration+1)",
    ],
))

daughter_of_darkness.add(passive_data(
    "DaughterOfDarkness_NightsAegis_Damaged",
    DisplayName=loca["DaughterOfDarkness_NightsAegis_DisplayName"],
    Properties="IsHidden",
    StatsFunctorContext=["OnDamaged", "OnDamagedPrevented"],
    Conditions=[
        "StatusDurationMoreThan(context.Target,'DAUGHTEROFDARKNESS_NIGHTSAEGIS',0)",
    ],
    StatsFunctors=[
        "ApplyStatus(DAUGHTEROFDARKNESS_NIGHTSAEGIS,100,Target.DAUGHTEROFDARKNESS_NIGHTSAEGIS.Duration-1)",
    ],
))

daughter_of_darkness.add(status_data(
    "DAUGHTEROFDARKNESS_NIGHTSAEGIS",
    StatusType="BOOST",
    DisplayName=loca["DaughterOfDarkness_NightsAegis_DisplayName"],
    Description=loca["DaughterOfDarkness_NightsAegis_StatusDescription"],
    Icon="Status_ArcaneWard",
    SoundLoop="Spell_Status_ArcaneWard_MO",
    SoundStop="Spell_Status_ArcaneWard_Depleted",
    StackId="DAUGHTEROFDARKNESS_NIGHTSAEGIS",
    StackType="Overwrite",
    Boosts=[
        "DamageBonus(1,Force)",
        "DamageReduction(All,Flat,1)",
    ],
    Passives="DaughterOfDarkness_NightsAegis_Damaged",
    StatusPropertyFlags=["MultiplyEffectsByDuration", "FreezeDuration", "DisableCombatlog"],
    StatusGroups="SG_RemoveOnRespec",
    StatusEffect="370b3339-9668-49e8-bdc6-ff0a4444f8dd",
))

daughter_of_darkness.add(spell_data(
    "DaughterOfDarkness_NightsEdge_Cleave",
    SpellType="Zone",
    using="Zone_Cleave",
    Cooldown="None",
))

loca["DaughterOfDarkness_NightsEdge_Summon_DisplayName"] = {"en": "Bind the Night"}
loca["DaughterOfDarkness_NightsEdge_Summon_Description"] = {"en": """
    Conjure the Night's Edge to your hands.
    """}

daughter_of_darkness.add(spell_data(
    "DaughterOfDarkness_NightsEdge_Summon",
    SpellType="Shout",
    Cooldown="OncePerCombat",
    TargetConditions="Self()",
    Icon="Action_PactOfTheBlade_Greatsword",
    DisplayName=loca["DaughterOfDarkness_NightsEdge_Summon_DisplayName"],
    Description=loca["DaughterOfDarkness_NightsEdge_Summon_Description"],
    SpellProperties=[
        f"SummonInInventory({nights_edge_game_objects_uuid},Permanent,1,true,true,true,,,"
        + "DaughterOfDarkness_NightsEdge_Summon,DAUGHTEROFDARKNESS_NIGHTSEDGE_SUMMON)",
    ],
    CastTextEvent="Cast",
    UseCosts="ActionPoint:1",
    SpellAnimation=[
        "f489d217-b699-4e8e-bf22-6ef539c5d65b,,",
        ",,",
        "7a343ea7-1330-428a-b0b1-9f6dc7f2a91c,,",
        "0f872585-3c6e-4493-a0b5-5acc882b7aaf,,",
        "f9414915-2da7-4f40-bcbd-90e956461246,,",
        ",,",
        "f2a62277-c87a-4ec7-b4f2-c3c37e6e30ae,,",
        ",,",
        ",,"
    ],
    VerbalIntent="Summon",
    SpellStyleGroup="Class",
    SpellAnimationIntentType="Aggressive",
    PrepareSound="Action_Prepare_Item_ShadowBlade",
    PrepareLoopSound="Action_Loop_Item_ShadowBlade",
    CastSound="Action_Cast_Item_ShadowBlade",
    TargetSound="Action_Impact_Item_ShadowBlade",
    VocalComponentSound="Vocal_Component_EnchantWeapon",
    PrepareEffect="3998daf3-8dd5-4b10-b33a-5ab51bb97860",
    CastEffect="514ecdc7-87b3-43f8-bd8a-69fb3b46f8da",
    Sheathing="Sheathed",
))

loca["DAUGHTEROFDARKNESS_NIGHTSEDGE_SUMMON_DisplayName"] = {"en": "Bound in Darkness"}
loca["DAUGHTEROFDARKNESS_NIGHTSEDGE_SUMMON_Description"] = {"en": """
    The cleric bound to this weapon is always <LSTag Tooltip="Proficiency">Proficient</LSTag> with it.
    The weapon's damage is magical.
    """}

daughter_of_darkness.add(status_data(
    "DAUGHTEROFDARKNESS_NIGHTSEDGE_SUMMON",
    StatusType="BOOST",
    DisplayName=loca["DAUGHTEROFDARKNESS_NIGHTSEDGE_SUMMON_DisplayName"],
    Description=loca["DAUGHTEROFDARKNESS_NIGHTSEDGE_SUMMON_Description"],
    Icon="Action_PactOfTheBlade_Greatsword",
    StackId="DAUGHTEROFDARKNESS_NIGHTSEDGE_SUMMON",
    Boosts=[
        "CannotBeDisarmed()",
        "WeaponProperty(Magical)",
        "IntrinsicSummonerProficiency()",
        "IntrinsicSourceProficiency()",
        "ItemReturnToOwner()",
        "Attribute(InventoryBound)",
        "WeaponAttackRollAbilityOverride(Wisdom)"
    ],
    StatusGroups="SG_RemoveOnRespec",
    IsUnique="1",
))

# Modify the game's Cleric class description
class_descriptions = Lsx.load(daughter_of_darkness.get_cache_path(CLASS_DESCRIPTION_PATH))
cleric_class_description: ClassDescription = class_descriptions.children.find(
    lambda progression: progression.Name == CharacterClass.CLERIC)

cleric_class_description.CanLearnSpells = True
cleric_class_description.BaseHp = 10
cleric_class_description.HpPerLevel = 6
cleric_class_description.MustPrepareSpells = True

daughter_of_darkness.add(cleric_class_description)

# Load the game's Sorcerer progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Lsx.load(daughter_of_darkness.get_cache_path(PROGRESSIONS_LSX_PATH))
progressions_dev_lsx = Lsx.load(daughter_of_darkness.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
progressions_lsx.children.update(progressions_dev_lsx.children, key=lambda progression: progression.UUID)

cleric_progression = progressions_lsx.children.keepall(
    lambda progression: progression.Name in CharacterSubclasses.CLERIC)

# Create spell lists
level_1_spelllist = str(daughter_of_darkness.make_uuid("level_1_spelllist"))
daughter_of_darkness.add(SpellList(
    Comment="Daughter of Darkness level 1 spells",
    Spells=[
        "Target_BlessingOfTheTrickster",
        bolster,
        "Target_CharmPerson",
        "Shout_DisguiseSelf",
        "DaughterOfDarkness_NightsEdge_Summon",
        "Shout_Shield_Wizard",
        "DaughterOfDarkness_ViciousMockery",
    ],
    UUID=level_1_spelllist,
))

level_2_spelllist = str(daughter_of_darkness.make_uuid("level_2_spelllist"))
daughter_of_darkness.add(SpellList(
    Comment="Daughter of Darkness level 2 spells",
    Spells=[
        "Target_Darkness",
        "Shout_Hide_ShadowArts",
        "Shout_MirrorImage",
        shadow_step,
    ],
    UUID=level_2_spelllist,
))

level_3_spelllist = str(daughter_of_darkness.make_uuid("level_3_spelllist"))
daughter_of_darkness.add(SpellList(
    Comment="Daughter of Darkness level 3 spells",
    Spells=["Target_Counterspell"],
    UUID=level_3_spelllist,
))


def trickery_level(level: int) -> Progression:
    progression = cleric_progression.find(lambda progression: (progression.Name == CharacterClass.CLERIC_TRICKERY
                                                               and progression.Level == level))
    if not progression:
        progression = Progression(
            Level=level,
            Name="TrickeryDomain",
            ProgressionType=1,
            TableUUID="044e4e07-6980-479f-80e5-3c4a84e691d1",
            UUID=daughter_of_darkness.make_uuid(f"TrickeryDomain_Level_{level}")
        )
        cleric_progression.append(progression)
    return progression


def level_1() -> None:
    """Add armor and weapon proficiencies, passives, skills, and spells."""
    progression = trickery_level(1)

    boosts = progression.Boosts or []
    boosts.extend([
        "ProficiencyBonus(SavingThrow,Constitution)",
    ])
    progression.Boosts = boosts

    passives_added = progression.PassivesAdded or []
    passives_added.extend([battle_magic, "SculptSpells"])
    progression.PassivesAdded = passives_added

    progression.Selectors = [f"AddSpells({level_1_spelllist},ClericTrickeryDomainSpells,,,AlwaysPrepared)"]

    progression = cleric_progression.find(lambda progression: (progression.Name == CharacterClass.CLERIC
                                                               and progression.Level == 1
                                                               and not (progression.IsMulticlass or False)))

    selectors = progression.Selectors or []
    selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
    selectors.extend([
        "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
        "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
    ])
    progression.Selectors = selectors


def level_2() -> None:
    progression = trickery_level(2)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["DevilsSight"]


def level_3() -> None:
    progression = trickery_level(3)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["DaughterOfDarkness_PassWithoutTrace"]
    progression.Selectors = [
        f"AddSpells({level_2_spelllist},ClericTrickeryDomainSpells,,,AlwaysPrepared)",
    ]


def level_4() -> None:
    progression = trickery_level(4)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]


def level_5() -> None:
    progression = trickery_level(5)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack", fast_movement]

    selectors = progression.Selectors or []
    selectors.extend([
        f"AddSpells({level_3_spelllist},ClericTrickeryDomainSpells,,,AlwaysPrepared)",
    ])
    progression.Selectors = selectors


def level_6() -> None:
    progression = trickery_level(6)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["PotentCantrip"]


def level_7() -> None:
    progression = trickery_level(7)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [
        "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]


def level_8() -> None:
    progression = trickery_level(8)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]


def level_9() -> None:
    progression = trickery_level(9)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]


def level_10() -> None:
    progression = trickery_level(10)
    progression.PassivesAdded = (progression.PassivesAdded or []) + [empowered_spells]


def level_11() -> None:
    progression = trickery_level(11)
    progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
    progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    selectors = progression.Selectors or []
    selectors.append("AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)")  # Fly
    progression.Selectors = selectors


def level_12() -> None:
    progression = trickery_level(12)
    selectors = progression.Selectors or []
    selectors.append("AddSpells(964e765d-5881-463e-b1b0-4fc6b8035aa8,,,,AlwaysPrepared)")  # Action Surge
    progression.Selectors = selectors


level_1()
level_2()
level_3()
level_4()
level_5()
level_6()
level_7()
level_8()
level_9()
level_10()
level_11()
level_12()

allow_improvement(cleric_progression, range(2, 13))
multiply_resources(cleric_progression, [ActionResource.SPELL_SLOTS, ActionResource.CHANNEL_DIVINITY_CHARGES], 2)

cleric_progression.sort(key=lambda progression: (CharacterClass(progression.Name).name,
                                                 progression.Level,
                                                 progression.IsMulticlass or False))

for progression in cleric_progression:
    daughter_of_darkness.add(progression)

daughter_of_darkness.build()
