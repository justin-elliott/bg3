#!/usr/bin/env python3
"""
Test code for modtools.lsx_v2.
"""

import modtools.valuelists_v2 as VL
from modtools.gamedata_v2 import GameData


class Armor(GameData):
    RootTemplate: VL.FixedString = VL.FixedString
    ItemGroup: VL.FixedString = VL.FixedString
    Level: VL.ConstantInt = VL.ConstantInt
    Slot: VL.Itemslot = VL.Itemslot
    Requirements: VL.Requirements = VL.Requirements
    UseConditions: VL.Conditions = VL.Conditions
    UseCosts: VL.FixedString = VL.FixedString
    ArmorClass: VL.ConstantInt = VL.ConstantInt
    Durability: VL.ConstantInt = VL.ConstantInt
    DurabilityDegradeSpeed: VL.Qualifier = VL.Qualifier
    ValueLevel: VL.ConstantInt = VL.ConstantInt
    ValueUUID: VL.Guid = VL.Guid
    ValueScale: VL.ConstantFloat = VL.ConstantFloat
    ValueRounding: VL.ConstantInt = VL.ConstantInt
    ValueOverride: VL.ConstantInt = VL.ConstantInt
    Rarity: VL.Rarity = VL.Rarity
    Weight: VL.ConstantFloat = VL.ConstantFloat
    GameSize: VL.FixedString = VL.FixedString
    SoundSize: VL.FixedString = VL.FixedString
    Spells: VL.FixedString = VL.FixedString
    Tags: VL.FixedString = VL.FixedString
    ExtraProperties: VL.FixedString = VL.FixedString
    Flags: VL.AttributeFlags = VL.AttributeFlags
    DefaultBoosts: VL.FixedString = VL.FixedString
    PersonalStatusImmunities: VL.StatusIDs = VL.StatusIDs
    Boosts: VL.FixedString = VL.FixedString
    PassivesOnEquip: VL.FixedString = VL.FixedString
    StatusOnEquip: VL.FixedString = VL.FixedString
    ComboCategory: VL.FixedString = VL.FixedString
    InventoryTab: VL.InventoryTabs = VL.InventoryTabs
    ArmorType: VL.ArmorType = VL.ArmorType
    ItemColor: VL.FixedString = VL.FixedString
    NeedsIdentification: VL.YesNo = VL.YesNo
    Charges: VL.ConstantInt = VL.ConstantInt
    MaxCharges: VL.ConstantInt = VL.ConstantInt
    ObjectCategory: VL.FixedString = VL.FixedString
    MinAmount: VL.ConstantInt = VL.ConstantInt
    MaxAmount: VL.ConstantInt = VL.ConstantInt
    Priority: VL.ConstantInt = VL.ConstantInt
    Unique: VL.ConstantInt = VL.ConstantInt
    MinLevel: VL.ConstantInt = VL.ConstantInt
    MaxLevel: VL.ConstantInt = VL.ConstantInt
    Shield: VL.YesNo = VL.YesNo
    Armor_Class_Ability: VL.Ability = VL.Ability
    Ability_Modifier_Cap: VL.ConstantInt = VL.ConstantInt
    FallingHitEffect: VL.FixedString = VL.FixedString
    FallingLandEffect: VL.FixedString = VL.FixedString
    ColorPresetResource: VL.FixedString = VL.FixedString
    Proficiency_Group: VL.ProficiencyGroupFlags
    InstrumentType: VL.InstrumentType = VL.InstrumentType
    StatusInInventory: VL.FixedString = VL.FixedString


armor = Armor("MyArmor")
armor.DurabilityDegradeSpeed = 5
armor.Shield = VL.YesNo.YES
print(armor)

armor = Armor(
    "AlsoMyArmor",
    using="MyArmor",
    DurabilityDegradeSpeed=5,
    Shield="No",
    Flags=[VL.AttributeFlags.GROUNDED, VL.AttributeFlags.BACKSTABIMMUNITY, VL.AttributeFlags.UNBREAKABLE]
)
print(armor)
