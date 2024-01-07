#!/usr/bin/env python3
"""
Generates files for the "InfernalBlade" mod.
"""

import os

from modtools.gamedata import passive_data, spell_data, status_data, weapon_data
from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",

infernal_blade = Mod(os.path.dirname(__file__),
                     author="justin-elliott",
                     name="InfernalBlade",
                     mod_uuid=UUID("ff0cba8e-a7f4-41f3-b836-0f0364b76f26"),
                     description="Adds the sword, the Infernal Blade.")

loca = infernal_blade.get_localization()
loca.add_language("en", "English")

loca["InfernalBlade_DisplayName"] = {"en": "Infernal Blade"}
loca["InfernalBlade_Description"] = {"en": """
    This blade burns with the heat of the Nine Hells.
    """}

infernal_blade_game_objects_uuid = UUID("5166e9d7-fbad-4406-a544-211a8eb3f151")
infernal_blade.add_root_templates([
    Lsx.Node("GameObjects", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["InfernalBlade_DisplayName"], version=1),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["InfernalBlade_Description"], version=1),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(infernal_blade_game_objects_uuid)),
        Lsx.Attribute("Name", "LSString", value="InfernalBlade_GreatSword"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value="81a83529-5bb6-4c72-b1af-6fc8f45c5706"),
        Lsx.Attribute("Stats", "FixedString", value="InfernalBlade_GreatSword"),
        Lsx.Attribute("Type", "FixedString", value="item"),
    ], children=[
        Lsx.Node("StatusList", children=[
            Lsx.Node("Status", [
                Lsx.Attribute("Object", "FixedString", value="InfernalBlade_EverBurning"),
            ]),
        ]),
    ])
])

infernal_blade.add(weapon_data(
    "InfernalBlade_GreatSword",
    using="WPN_Greatsword_1",
    RootTemplate=str(infernal_blade_game_objects_uuid),
    ItemGroup="",
    ValueUUID="86e7e503-a225-4b48-819e-2e24de1f904a",
    Rarity="Legendary",
    Boosts=[
        "Proficiency(Greatswords)",
        "UnlockSpell(InfernalBlade_InfernalDash)",
        "UnlockSpell(Projectile_FireBolt)",
    ],
    BoostsOnEquipMainHand=[
        "UnlockSpell(Target_PommelStrike)",
        "UnlockSpell(Target_Slash_New)",
        "UnlockSpell(InfernalBlade_Cleave)",
    ],
    DefaultBoosts=[
        "WeaponProperty(Magical)",
        "IF(CharacterLevelGreaterThan(3) and not CharacterLevelGreaterThan(6)):WeaponEnchantment(1)",
        "IF(CharacterLevelGreaterThan(6) and not CharacterLevelGreaterThan(9)):WeaponEnchantment(2)",
        "IF(CharacterLevelGreaterThan(9)):WeaponEnchantment(3)",
        "IF(not CharacterLevelGreaterThan(4)):WeaponDamage(1d4, Fire, Magical)",
        "IF(CharacterLevelGreaterThan(4) and not CharacterLevelGreaterThan(8)):WeaponDamage(1d6, Fire, Magical)",
        "IF(CharacterLevelGreaterThan(8)):WeaponDamage(1d8, Fire, Magical)",
        "IF(CharacterLevelGreaterThan(5) and not CharacterLevelGreaterThan(11)):ReduceCriticalAttackThreshold(1)",
        "IF(CharacterLevelGreaterThan(11)):ReduceCriticalAttackThreshold(2)",
    ],
    PassivesOnEquip=[
        "InfernalBlade_InfernalCorrupter",
        "InfernalBlade_InfernalMight",
        "InfernalBlade_InfernalResilience",
        "Blindsight",
        "RecklessAttack",
    ],
    Unique="1",
))

loca["InfernalBlade_InfernalCorrupter_DisplayName"] = {"en": "Infernal Corrupter"}
loca["InfernalBlade_InfernalCorrupter_Description"] = {"en": """
    Your attacks with the Infernal Blade ignore <LSTag Tooltip="Resistant">Resistance</LSTag> to Slashing and Fire
    damage.
    """}

infernal_blade.add(passive_data(
    "InfernalBlade_InfernalCorrupter",
    DisplayName=loca["InfernalBlade_InfernalCorrupter_DisplayName"],
    Description=loca["InfernalBlade_InfernalCorrupter_Description"],
    Icon="PassiveFeature_DraconicAncestry_Black",
    Boosts=[
        "IF(IsMeleeAttack() and IsWeaponAttack()):IgnoreResistance(Slashing, Resistant)",
        "IF(IsMeleeAttack() and IsWeaponAttack()):IgnoreResistance(Fire, Resistant)",
    ],
))

loca["InfernalBlade_InfernalDash_DisplayName"] = {"en": "Infernal Dash"}
loca["InfernalBlade_InfernalDash_Description"] = {"en": """
    Double your <LSTag Tooltip="MovementSpeed">Movement Speed</LSTag>. Jump no longer requires a
    <LSTag Type="ActionResource" Tooltip="BonusActionPoint">Bonus Action</LSTag>.
    """}

infernal_blade.add(spell_data(
    "InfernalBlade_InfernalDash",
    SpellType="Shout",
    using="Shout_Dash_BonusAction",
    DisplayName=loca["InfernalBlade_InfernalDash_DisplayName"],
    Description=loca["InfernalBlade_InfernalDash_Description"],
    TooltipStatusApply=[
        "ApplyStatus(DASH, 100, 1)",
        "ApplyStatus(InfernalBlade_FreeJump, 100, 1)",
    ],
    SpellFlags=[
        "IgnoreSilence",
        "Stealth",
        "Invisible",
        "NoCameraMove",
    ],
    SpellStyleGroup="Class",
))

loca["InfernalBlade_FreeJump_DisplayName"] = {"en": "Jump"}
loca["InfernalBlade_FreeJump_Description"] = {"en": """
    Jump no longer requires a <LSTag Type="ActionResource" Tooltip="BonusActionPoint">Bonus Action</LSTag>.
    """}

infernal_blade.add(status_data(
    "InfernalBlade_FreeJump",
    StatusType="BOOST",
    DisplayName=loca["InfernalBlade_FreeJump_DisplayName"],
    Description=loca["InfernalBlade_FreeJump_Description"],
    Icon="Action_Jump",
    StackId="InfernalBlade_FreeJump",
    TickType="EndTurn",
    Boosts=[
        "UnlockSpellVariant("
        + "SpellId('Projectile_Jump'), "
        + "ModifyUseCosts(Replace, BonusActionPoint, 0, 0, BonusActionPoint))",
    ],
    StatusGroups="SG_RemoveOnRespec",
))

loca["InfernalBlade_InfernalMight_DisplayName"] = {"en": "Infernal Might"}
loca["InfernalBlade_InfernalMight_Description"] = {"en": """
    Increases your <LSTag Tooltip="Strength">Strength</LSTag> to [1], and your jump distance by [2].
    """}

infernal_blade.add(passive_data(
    "InfernalBlade_InfernalMight",
    DisplayName=loca["InfernalBlade_InfernalMight_DisplayName"],
    Description=loca["InfernalBlade_InfernalMight_Description"],
    DescriptionParams=[
        "LevelMapValue(InfernalBlade_StrengthValue)",
        "Distance(4.5)",
    ],
    Icon="PassiveFeature_MindlessRage",
    Boosts=[
        "JumpMaxDistanceMultiplier(1.5)",
        # LevelMapValue() does not work for AbilityOverrideMinimum()
        "IF(not CharacterLevelGreaterThan(3)):AbilityOverrideMinimum(Strength, 18)",
        "IF(CharacterLevelGreaterThan(3) and not CharacterLevelGreaterThan(6)):AbilityOverrideMinimum(Strength, 20)",
        "IF(CharacterLevelGreaterThan(6) and not CharacterLevelGreaterThan(9)):AbilityOverrideMinimum(Strength, 22)",
        "IF(CharacterLevelGreaterThan(9)):AbilityOverrideMinimum(Strength, 24)",
    ],
))

loca["InfernalBlade_InfernalResilience_DisplayName"] = {"en": "Infernal Resilience"}
loca["InfernalBlade_InfernalResilience_Description"] = {"en": """
    You are <LSTag Tooltip="Resistant">Resistant</LSTag> to Fire damage, and all incoming damage is reduced by [1].
    """}

infernal_blade.add(passive_data(
    "InfernalBlade_InfernalResilience",
    DisplayName=loca["InfernalBlade_InfernalResilience_DisplayName"],
    Description=loca["InfernalBlade_InfernalResilience_Description"],
    DescriptionParams=["LevelMapValue(InfernalBlade_DamageReductionValue)"],
    Icon="PassiveFeature_Tough",
    Boosts=[
        "Resistance(Fire, Resistant)",
        "DamageReduction(All, Flat, LevelMapValue(InfernalBlade_DamageReductionValue))",
    ],
))

infernal_blade.add(spell_data(
    "InfernalBlade_Cleave",
    SpellType="Zone",
    using="Zone_Cleave",
    Cooldown="None",
))

infernal_blade.add(status_data(
    "InfernalBlade_EverBurning",
    StatusType="BOOST",
    DisplayName=loca["InfernalBlade_DisplayName"],
    Description=loca["InfernalBlade_Description"],
    Icon="statIcons_EverBurning",
    StatusEffectOverrideForItems="44d77ebf-fc9e-407d-b20f-257019351f2a",
    StatusPropertyFlags=[
        "DisableOverhead",
        "IgnoreResting",
        "DisableCombatlog",
        "DisablePortraitIndicator"
    ],
))

infernal_blade.add_level_maps([
    Lsx.Node("LevelMapSeries", [
        *[Lsx.Attribute(f"Level{level}", "LSString", value=f"{16 + int((level + 2) / 3) * 2}")
            for level in range(1, 13)],
        Lsx.Attribute("Name", "FixedString", value="InfernalBlade_StrengthValue"),
        Lsx.Attribute("UUID", "guid", value="bd94be18-3f34-401c-aaa2-5f18cbdac211"),
    ]),
    Lsx.Node("LevelMapSeries", [
        *[Lsx.Attribute(f"Level{level}", "LSString", value=f"{int((level + 2) / 3)}")
            for level in range(1, 13)],
        Lsx.Attribute("Name", "FixedString", value="InfernalBlade_DamageReductionValue"),
        Lsx.Attribute("UUID", "guid", value="56c0db94-9826-4646-a966-e8a1165319b4"),
    ]),
])

infernal_blade.add_treasure_table("""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_InfernalBlade_GreatSword",1,0,0,0,0,0,0,0
""")

infernal_blade.build()
