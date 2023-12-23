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
loca["MEDLEY_Description"] = {"en": """
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
    Description=loca["MEDLEY_Description"],
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
    PassivesOnEquip=[
        "Serenade_Boost_Abilities",
        "Serenade_Virtuoso",
    ],
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


def spell_boost_ability(ability: str, icon: str, cast_sound: str, target_sound: str, prepare_effect: str,
                        cast_effect: str, target_effect: str, boost_range: range = range(2, 22, 2)) -> None:
    loca[f"Serenade_Boost_{ability}_DisplayName"] = {"en": f"Serenade: Boost {ability}"}
    loca[f"Serenade_Boost_{ability}_Description"] = {
        "en": f"""Increase your <LSTag Tooltip="{ability}">{ability}</LSTag> by a selected amount."""
    }
    loca[f"Serenade_Boost_{ability}_00_DisplayName"] = {"en": f"Reset {ability}"}
    loca[f"Serenade_Boost_{ability}_00_Description"] = {
        "en": f"""Reset your <LSTag Tooltip="{ability}">{ability}</LSTag> to its unboosted value."""
    }

    serenade.add_spell_data(
        f"Serenade_Boost_{ability}",
        SpellType="Shout",
        ContainerSpells=[
            f"Serenade_Boost_{ability}_00",
            *[f"Serenade_Boost_{ability}_{boost:02}" for boost in boost_range]
        ],
        CycleConditions="Self()",
        TargetConditions="Self()",
        DisplayName=loca[f"Serenade_Boost_{ability}_DisplayName"],
        Description=loca[f"Serenade_Boost_{ability}_Description"],
        Icon=icon,
        CastTextEvent="Cast",
        SpellAnimation=[
            "03496c4a-49e0-4132-b585-3e5ecd1ad8e5,,",
            ",,",
            "8252328a-66dd-4dc0-bbe0-00eea3204922,,",
            "982d842b-5d44-4ef6-ab33-14d5ae514a50,,",
            "a9682ef9-5d9e-4ac0-8144-2c7fe6eb868c,,",
            ",,",
            "32fb4d91-7fde-4b05-9144-ea87b9a4284a,,",
            "dada6495-752c-4f30-a503-f05b8c811e2b,,",
            "8ce53f9b-b559-49cd-9607-1991545060d7,,",
        ],
        SpellFlags=[
            "IgnorePreviouslyPickedEntities",
            "IsLinkedSpellContainer",
            "Temporary",
            "UnavailableInDialogs",
        ],
        HitAnimationType="MagicalNonDamage",
        CastSound=cast_sound,
        TargetSound=target_sound,
        PrepareEffect=prepare_effect,
        CastEffect=cast_effect,
        TargetEffect=target_effect,
        UseCosts="",
        VerbalIntent="Buff",
    )

    serenade.add_spell_data(
        f"Serenade_Boost_{ability}_00",
        SpellType="Shout",
        using=f"Serenade_Boost_{ability}",
        DisplayName=loca[f"Serenade_Boost_{ability}_00_DisplayName"],
        Description=loca[f"Serenade_Boost_{ability}_00_Description"],
        Icon="PassiveFeature_Portent",
        ContainerSpells="",
        SpellContainerID=f"Serenade_Boost_{ability}",
        SpellProperties=f"RemoveStatus(SERENADE_BOOST_{ability.upper()})",
    )

    for boost in boost_range:
        loca[f"Serenade_Boost_{ability}_{boost:02}_DisplayName"] = {"en": f"Boost {ability} by {boost}"}
        loca[f"Serenade_Boost_{ability}_{boost:02}_Description"] = {
            "en": f"""Increase your <LSTag Tooltip="{ability}">{ability}</LSTag> by {boost}."""
        }

        serenade.add_spell_data(
            f"Serenade_Boost_{ability}_{boost:02}",
            SpellType="Shout",
            using=f"Serenade_Boost_{ability}",
            DisplayName=loca[f"Serenade_Boost_{ability}_{boost:02}_DisplayName"],
            Description=loca[f"Serenade_Boost_{ability}_{boost:02}_Description"],
            Icon=f"PassiveFeature_Portent_{boost}",
            ContainerSpells="",
            SpellContainerID=f"Serenade_Boost_{ability}",
            SpellProperties=f"ApplyStatus(SERENADE_BOOST_{ability.upper()},100,{boost})",
        )

    serenade.add_status_data(
        f"SERENADE_BOOST_{ability.upper()}",
        StatusType="BOOST",
        DisplayName=loca[f"Serenade_Boost_{ability}_DisplayName"],
        Description=loca[f"Serenade_Boost_{ability}_Description"],
        Icon=icon,
        StackId=f"SERENADE_BOOST_{ability.upper()}",
        StackType="Overwrite",
        Boosts=f"Ability({ability},1,30)",
        StatusPropertyFlags=[
            "DisableCombatlog",
            "DisableImmunityOverhead",
            "DisableOverhead",
            "DisablePortraitIndicator",
            "FreezeDuration",
            "IgnoreResting",
            "MultiplyEffectsByDuration",
        ],
    )


spell_boost_ability("Strength",
                    icon="Spell_Transmutation_EnhanceAbility_BullsStrenght",
                    cast_sound="Spell_Cast_Buff_EnhanceAbilityBullsStrength_L1to3",
                    target_sound="Spell_Impact_Buff_EnhanceAbilityBullsStrength_L1to3",
                    prepare_effect="5ea8f8f4-ba5f-4417-82f6-ed2ce4ffe264",
                    cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
                    target_effect="fbb955f8-a644-451b-89bd-7950ad4cebad")
spell_boost_ability("Dexterity",
                    icon="Spell_Transmutation_EnhanceAbility_CatsGrace",
                    cast_sound="Spell_Cast_Buff_EnhanceAbilityCatsGrace_L1to3",
                    target_sound="Spell_Impact_Buff_EnhanceAbilityCatsGrace_L1to3",
                    prepare_effect="fbce561c-fd42-4626-bf04-8461f46dfbc8",
                    cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
                    target_effect="474d55bf-bce6-401b-872a-1922c8d54d99")
spell_boost_ability("Constitution",
                    icon="Spell_Transmutation_EnhanceAbility_BearsEndurance",
                    cast_sound="Spell_Cast_Buff_EnhanceAbilityBearsEndurance_L1to3",
                    target_sound="Spell_Impact_Buff_EnhanceAbilityBearsEndurance_L1to3",
                    prepare_effect="15908bab-2ec3-4abc-a282-c3bf5f2b1387",
                    cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
                    target_effect="4d80e719-6b5a-4a77-829c-f9b7f38fd966")
spell_boost_ability("Intelligence",
                    icon="Spell_Transmutation_EnhanceAbility_FoxsCunning",
                    cast_sound="Spell_Cast_Buff_EnhanceAbilityFoxsCunning_L1to3",
                    target_sound="Spell_Impact_Buff_EnhanceAbilityFoxsCunning_L1to3",
                    prepare_effect="1ee00587-5c1a-4068-aba3-6bfd5cb8f92f",
                    cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
                    target_effect="587df9a6-10c6-4125-ab0a-73c477018a4b")
spell_boost_ability("Wisdom",
                    icon="Spell_Transmutation_EnhanceAbility_OwlsWisdom",
                    cast_sound="Spell_Cast_Buff_EnhanceAbilityOwlsWisdom_L1to3",
                    target_sound="Spell_Impact_Buff_EnhanceAbilityOwlsWisdom_L1to3",
                    prepare_effect="1082b19d-920d-423f-b787-3c66da153f47",
                    cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
                    target_effect="b01d8d96-abb3-4e88-8e41-ce12c7dbf30a")
spell_boost_ability("Charisma",
                    icon="Spell_Transmutation_EnhanceAbility_EaglesSplendor",
                    cast_sound="Spell_Cast_Buff_EnhanceAbilityEaglesSplendor_L1to3",
                    target_sound="Spell_Impact_Buff_EnhanceAbilityEaglesSplendor_L1to3",
                    prepare_effect="fa18f4ad-7f12-47fc-9fe7-3a157e0ee260",
                    cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
                    target_effect="70d8d0dc-e4ff-42ed-8503-09bbf2fbbeda")

loca["Serenade_Boost_Abilities_DisplayName"] = {"en": "Serenade: Boost Abilities"}
loca["Serenade_Boost_Abilities_Description"] = {"en": "Unlock the boost ability spells."}

serenade.add_passive_data(
    "Serenade_Boost_Abilities",
    DisplayName=loca["Serenade_Boost_Abilities_DisplayName"],
    Description=loca["Serenade_Boost_Abilities_Description"],
    Icon="Spell_Transmutation_EnhanceAbility",
    Properties=[
        "IsToggled",
        "ToggledDefaultAddToHotbar",
        "ToggleForParty",
    ],
    Boosts=[
        "UnlockSpell(Serenade_Boost_Strength)",
        "UnlockSpell(Serenade_Boost_Dexterity)",
        "UnlockSpell(Serenade_Boost_Constitution)",
        "UnlockSpell(Serenade_Boost_Intelligence)",
        "UnlockSpell(Serenade_Boost_Wisdom)",
        "UnlockSpell(Serenade_Boost_Charisma)",
    ],
    ToggleGroup="Serenade_Boost_Abilities",
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
