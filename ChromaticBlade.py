#!/usr/bin/env python3
"""
Generates files for the "ChromaticBlade" mod.
"""

import os

from moddb.boosts import Boosts
from modtools.gamedata import passive_data, spell_data, status_data, weapon_data
from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",


chromatic_blade = Mod(os.path.dirname(__file__),
                      author="justin-elliott",
                      name="ChromaticBlade",
                      mod_uuid=UUID("ae8399a2-3445-4c0b-b9c4-4d77f3daf46c"),
                      description="Adds the sword, the Chromatic Blade.")

loca = chromatic_blade.get_localization()

loca["ChromaticBlade_DisplayName"] = {"en": "Chromatic Blade"}
loca["ChromaticBlade_Description"] = {"en": """
    This blade shimmers with elemental force.
    """}

everburn_blade_uuid = UUID("81a83529-5bb6-4c72-b1af-6fc8f45c5706")
katana_uuid = UUID("7050c02e-f0e1-46b8-9400-2514805ecd2e")
phalar_aluve_uuid = UUID("6d0d3206-50b5-48ed-af92-a146ed6b98f2")

chromatic_blade_game_objects_uuid = UUID("05b4b0c3-44cc-41da-a50b-a8cba6787e16")
chromatic_blade.add_root_templates([
    Lsx.Node("GameObjects", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["ChromaticBlade_DisplayName"], version=1),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["ChromaticBlade_Description"], version=1),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(chromatic_blade_game_objects_uuid)),
        Lsx.Attribute("Name", "LSString", value="ChromaticBlade_Sword"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value=str(katana_uuid)),
        Lsx.Attribute("Stats", "FixedString", value="ChromaticBlade_Sword"),
        Lsx.Attribute("Type", "FixedString", value="item"),
    ])
])

chromatic_blade.add(weapon_data(
    "ChromaticBlade_Sword",
    using="WPN_Longsword",
    RootTemplate=str(chromatic_blade_game_objects_uuid),
    Rarity="Legendary",
    BoostsOnEquipMainHand=[
        "CannotBeDisarmed()",
        "Proficiency(Longswords)",
        "UnlockSpell(Target_PommelStrike)",
        "UnlockSpell(Target_Slash_New)",
        "UnlockSpell(Rush_SpringAttack)",
        "UnlockSpell(ChromaticBlade_ChromaticWeapon)",
    ],
    DefaultBoosts=[
        "IF(CharacterLevelRange(7,11)):ReduceCriticalAttackThreshold(1)",
        "IF(CharacterLevelRange(12,20)):ReduceCriticalAttackThreshold(2)",
    ],
    PassivesOnEquip=[],
    Weapon_Properties=[
        "Dippable",
        "Finesse",
        "Magical",
        "Melee",
        "Versatile",
    ],
    Unique="1",
))

loca["ChromaticBlade_ChromaticWeapon_DisplayName"] = {"en": "Chromatic Weapon"}
loca["ChromaticBlade_ChromaticWeapon_Description"] = {"en": """
    Imbue a weapon with elemental power. It receives a +1 bonus to <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>,
    and deals an additional 1d4 damage of your choice.
    """}
loca["ChromaticBlade_ChromaticWeapon_StatusDescription"] = {"en": """
    Has a +1 bonus to <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag> and deals an additional [1].
    """}

chromatic_blade.add(spell_data(
    "ChromaticBlade_ChromaticWeapon",
    SpellType="Shout",
    Level="",
    SpellSchool="Transmutation",
    ContainerSpells=[
        "ChromaticBlade_ChromaticWeapon_Acid",
    ],
    TargetConditions="Self() and HasWeaponInMainHand()",
    Icon="Spell_Transmutation_ElementalWeapon",
    DisplayName=loca["ChromaticBlade_ChromaticWeapon_DisplayName"],
    Description=loca["ChromaticBlade_ChromaticWeapon_Description"],
    PreviewCursor="Cast",
    CastTextEvent="Cast",
    UseCosts="ActionPoint:1",
    SpellAnimation=[
        "dd86aa43-8189-4d9f-9a5c-454b5fe4a197,,",
        ",,",
        "89b3c338-a117-454c-b34a-2473e5a8bcc5,,",
        "b3253cb1-b621-4c3b-a93d-efb5ed6b2af1,,",
        "cc5b0caf-3ed1-4711-a50d-11dc3f1fdc6a,,",
        ",,",
        "1715b877-4512-472e-9bd0-fd568a112e90,,",
        ",,",
        ",,",
    ],
    VerbalIntent="Utility",
    SpellFlags=[
        "HasSomaticComponent",
        "HasVerbalComponent",
        "IsDefaultWeaponAction",
        "IsLinkedSpellContainer",
        "IsMelee",
        "IsSpell",
    ],
    HitAnimationType="MagicalNonDamage",
))

loca["ChromaticBlade_ChromaticWeapon_Acid_DisplayName"] = {"en": "Chromatic Weapon: Acid"}
loca["ChromaticBlade_ChromaticWeapon_Acid_Description"] = {"en": """
    Imbue a weapon with a corrosive might. It receives a +1 bonus to <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>,
    and deals an additional [1].
    """}

chromatic_blade.add(spell_data(
    "ChromaticBlade_ChromaticWeapon_Acid",
    using="ChromaticBlade_ChromaticWeapon",
    SpellType="Shout",
    SpellContainerID="ChromaticBlade_ChromaticWeapon",
    ContainerSpells="",
    SpellProperties="ApplyEquipmentStatus(MainHand,CHROMATICBLADE_CHROMATICWEAPON_ACID,100,-1)",
    Icon="Spell_Transmutation_ElementalWeapon_Acid",
    DisplayName=loca["ChromaticBlade_ChromaticWeapon_Acid_DisplayName"],
    Description=loca["ChromaticBlade_ChromaticWeapon_Acid_Description"],
    DescriptionParams="DealDamage(1d4,Acid)",
    TooltipStatusApply="ApplyStatus(CHROMATICBLADE_CHROMATICWEAPON_ACID,100,-1)",
    PrepareSound="Spell_Prepare_Buff_ElementalWeaponAcid_L1to3",
    PrepareLoopSound="Spell_Loop_Buff_ElementalWeaponAcid_L1to3",
    CastSound="Spell_Cast_Buff_ElementalWeaponAcid_L1to3",
    TargetSound="Spell_Impact_Buff_ElementalWeaponAcid_L1to3",
    SpellFlags=[
        "HasVerbalComponent",
        "HasSomaticComponent",
        "IsSpell",
        "IsMelee",
    ],
    PrepareEffect="803e65f9-b27c-4e9c-af2a-8cf0e8e8564d",
    CastEffect="dfb57578-dafa-4c39-9f6e-238b9e2c237d",
    TargetEffect="89018ece-411e-4c00-94ec-6cb3743f4af5",
))

chromatic_blade.add(status_data(
    "CHROMATICBLADE_CHROMATICWEAPON_ACID",
    StatusType="BOOST",
    DisplayName=loca["ChromaticBlade_ChromaticWeapon_DisplayName"],
    Description=loca["ChromaticBlade_ChromaticWeapon_StatusDescription"],
    DescriptionParams="DealDamage(1d4,Acid)",
    Icon="Spell_Transmutation_ElementalWeapon_Acid",
    StackId="ELEMENTAL_WEAPON",
    Boosts=[
        "WeaponEnchantment(1)",
        "WeaponDamage(1d4,Acid)",
    ],
    StatusGroups="SG_RemoveOnRespec",
    StatusEffect="3798c69d-e202-4323-b660-2e1778dafafc",
    StatusPropertyFlags=["IgnoreResting"],
))

chromatic_blade.add_treasure_table("""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_ChromaticBlade_Sword",1,0,0,0,0,0,0,0
""")

chromatic_blade.build()
