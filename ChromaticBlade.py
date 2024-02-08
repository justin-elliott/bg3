#!/usr/bin/env python3
"""
Generates files for the "ChromaticBlade" mod.
"""

import os

from moddb.scripts import character_level_range
from modtools.gamedata import PassiveData, SpellData, StatusData, Weapon
from modtools.lsx.game import GameObjects, LevelMapSeries
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
chromatic_blade.add_script(character_level_range)

loca = chromatic_blade.get_localization()
loca["ChromaticBlade_DisplayName"] = {"en": "Chromatic Blade"}
loca["ChromaticBlade_Description"] = {"en": """
    This blade shimmers with elemental force.
    """}

everburn_blade_uuid = UUID("81a83529-5bb6-4c72-b1af-6fc8f45c5706")
katana_uuid = UUID("7050c02e-f0e1-46b8-9400-2514805ecd2e")
phalar_aluve_uuid = UUID("6d0d3206-50b5-48ed-af92-a146ed6b98f2")

chromatic_blade_game_objects_uuid = UUID("05b4b0c3-44cc-41da-a50b-a8cba6787e16")
chromatic_blade.add(GameObjects(
    DisplayName=loca["ChromaticBlade_DisplayName"],
    Description=loca["ChromaticBlade_Description"],
    LevelName="",
    MapKey=chromatic_blade_game_objects_uuid,
    Name="ChromaticBlade_Sword",
    ParentTemplateId=katana_uuid,
    Stats="ChromaticBlade_Sword",
    Type="item",
    children=[
        GameObjects.StatusList(
            children=[
                GameObjects.StatusList.Status(Object="MAG_BYPASS_SLASHING_RESISTANCE_TECHNICAL"),
                GameObjects.StatusList.Status(Object="MAG_DIAMONDSBANE_TECHNICAL"),
            ],
        ),
    ],
))

chromatic_blade.add(Weapon(
    "ChromaticBlade_Sword",
    using="WPN_Longsword",
    RootTemplate=str(chromatic_blade_game_objects_uuid),
    Rarity="Legendary",
    BoostsOnEquipMainHand=[
        "CannotBeDisarmed()",
        "Proficiency(Longswords)",
        "UnlockSpell(Target_PommelStrike)",
        "UnlockSpell(Target_Slash_New)",
        "UnlockSpell(ChromaticBlade_Charge)",
        "UnlockSpell(ChromaticBlade_Cleave)",
        "UnlockSpell(ChromaticBlade_ChromaticWeapon)",
    ],
    DefaultBoosts=[
        "IF(CharacterLevelRange(7,11)):ReduceCriticalAttackThreshold(1)",
        "IF(CharacterLevelRange(12,20)):ReduceCriticalAttackThreshold(2)",
        "IF(CharacterLevelRange(1,5)):WeaponEnchantment(1)",
        "IF(CharacterLevelRange(6,10)):WeaponEnchantment(2)",
        "IF(CharacterLevelRange(11,20)):WeaponEnchantment(3)",
    ],
    PassivesOnEquip=[
        "ChromaticBlade_CriticalVsItems_Passive",
        "MAG_IgnoreSlashingResistance_Passive",
    ],
    Weapon_Properties=[
        "Dippable",
        "Finesse",
        "Magical",
        "Melee",
        "Versatile",
    ],
    Unique="1",
))

loca["ChromaticBlade_CriticalVsItems_Description"] = {"en": """
    If the blade hits an object, the hit is always critical.
    """}

chromatic_blade.add(PassiveData(
    "ChromaticBlade_CriticalVsItems_Passive",
    using="UNI_Adamantine_CriticalVsItems_Passive",
    Description=loca["ChromaticBlade_CriticalVsItems_Description"],
))

loca["ChromaticBlade_ChromaticWeapon_DisplayName"] = {"en": "Chromatic Weapon"}
loca["ChromaticBlade_ChromaticWeapon_Description"] = {"en": """
    Imbue the blade with elemental power. It deals an additional [1] damage of your choice.
    """}

chromatic_blade.add(SpellData(
    "ChromaticBlade_ChromaticWeapon",
    SpellType="Shout",
    Level="",
    SpellSchool="Transmutation",
    ContainerSpells=[
        f"ChromaticBlade_ChromaticWeapon_{element}" for element in [
            "Acid", "Cold", "Fire", "Force", "Lightning", "Poison", "Thunder"
        ]
    ],
    TargetConditions="Self() and HasWeaponInMainHand()",
    Icon="Spell_Transmutation_ElementalWeapon",
    DisplayName=loca["ChromaticBlade_ChromaticWeapon_DisplayName"],
    Description=loca["ChromaticBlade_ChromaticWeapon_Description"],
    DescriptionParams=["LevelMapValue(ChromaticBlade_DamageDice)"],
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

chromatic_blade.add(LevelMapSeries(
    **{f"Level{level}": int((level + 4) / 5) for level in range(1, 13)},
    **{f"Level{level}": 3 for level in range(13, 21)},
    Name="ChromaticBlade_AttackRollBonus",
    UUID=chromatic_blade.make_uuid("ChromaticBlade_AttackRollBonus"),
))
chromatic_blade.add(LevelMapSeries(
    **{f"Level{level}": f"{int((level + 4) / 5)}d4" for level in range(1, 13)},
    **{f"Level{level}": "3d4" for level in range(13, 21)},
    Name="ChromaticBlade_DamageDice",
    UUID=chromatic_blade.make_uuid("ChromaticBlade_DamageDice"),
))


def add_chromatic_weapon_element(element: str,
                                 icon: str,
                                 PrepareSound: str,
                                 PrepareLoopSound: str,
                                 CastSound: str,
                                 TargetSound: str,
                                 PrepareEffect: str,
                                 CastEffect: str,
                                 TargetEffect: str,
                                 StatusEffect: str) -> None:
    title = element.title()
    lower = element.lower()
    upper = element.upper()

    loca[f"ChromaticBlade_ChromaticWeapon_{title}_DisplayName"] = {"en": f"Chromatic Weapon: {title}"}
    loca[f"ChromaticBlade_ChromaticWeapon_{title}_Description"] = {"en": """
        Imbue the blade to deal an additional [1].
        """}
    loca[f"ChromaticBlade_ChromaticWeapon_{title}_StatusDescription"] = {"en": f"""
        Deals additional {lower} damage.
        """}

    chromatic_blade.add(SpellData(
        f"ChromaticBlade_ChromaticWeapon_{title}",
        using="ChromaticBlade_ChromaticWeapon",
        SpellType="Shout",
        SpellContainerID="ChromaticBlade_ChromaticWeapon",
        ContainerSpells="",
        SpellProperties=f"ApplyEquipmentStatus(MeleeMainHand,CHROMATICBLADE_CHROMATICWEAPON_{upper},100,-1)",
        Icon=icon,
        DisplayName=loca[f"ChromaticBlade_ChromaticWeapon_{title}_DisplayName"],
        Description=loca[f"ChromaticBlade_ChromaticWeapon_{title}_Description"],
        DescriptionParams=[f"DealDamage(LevelMapValue(ChromaticBlade_DamageDice),{title})"],
        TooltipStatusApply=f"ApplyStatus(CHROMATICBLADE_CHROMATICWEAPON_{upper},100,-1)",
        PrepareSound=PrepareSound,
        PrepareLoopSound=PrepareLoopSound,
        CastSound=CastSound,
        TargetSound=TargetSound,
        SpellFlags=[
            "HasVerbalComponent",
            "HasSomaticComponent",
            "IsSpell",
            "IsMelee",
        ],
        PrepareEffect=PrepareEffect,
        CastEffect=CastEffect,
        TargetEffect=TargetEffect,
    ))

    chromatic_blade.add(StatusData(
        f"CHROMATICBLADE_CHROMATICWEAPON_{upper}",
        StatusType="BOOST",
        DisplayName=loca[f"ChromaticBlade_ChromaticWeapon_{title}_DisplayName"],
        Description=loca[f"ChromaticBlade_ChromaticWeapon_{title}_StatusDescription"],
        Icon=icon,
        StackId="ELEMENTAL_WEAPON",
        Boosts=[
            f"IF(CharacterLevelRange(1,5)):WeaponDamage(1d4,{title},Magical)",
            f"IF(CharacterLevelRange(6,10)):WeaponDamage(2d4,{title},Magical)",
            f"IF(CharacterLevelRange(11,20)):WeaponDamage(3d4,{title},Magical)",
        ],
        StatusGroups="SG_RemoveOnRespec",
        StatusEffect=StatusEffect,
        StatusPropertyFlags=["IgnoreResting"],
    ))


add_chromatic_weapon_element("Acid",
                             "Spell_Evocation_ChromaticOrb_Acid",
                             PrepareSound="Spell_Prepare_Buff_ElementalWeaponAcid_L1to3",
                             PrepareLoopSound="Spell_Loop_Buff_ElementalWeaponAcid_L1to3",
                             CastSound="Spell_Cast_Buff_ElementalWeaponAcid_L1to3",
                             TargetSound="Spell_Impact_Buff_ElementalWeaponAcid_L1to3",
                             PrepareEffect="803e65f9-b27c-4e9c-af2a-8cf0e8e8564d",
                             CastEffect="dfb57578-dafa-4c39-9f6e-238b9e2c237d",
                             TargetEffect="89018ece-411e-4c00-94ec-6cb3743f4af5",
                             StatusEffect="3798c69d-e202-4323-b660-2e1778dafafc")
add_chromatic_weapon_element("Cold",
                             "Spell_Evocation_ChromaticOrb_Cold",
                             PrepareSound="Spell_Prepare_Buff_ElementalWeaponCold_L1to3",
                             PrepareLoopSound="Spell_Loop_Buff_ElementalWeaponCold_L1to3",
                             CastSound="Spell_Cast_Buff_ElementalWeaponCold_L1to3",
                             TargetSound="Spell_Impact_Buff_ElementalWeaponCold_L1to3",
                             PrepareEffect="743b0439-4d13-4988-acd3-43318fb97536",
                             CastEffect="43efb4cc-023f-43c6-91a1-9383d754f31a",
                             TargetEffect="37848e95-b5cb-4184-a3c2-33780787694d",
                             StatusEffect="e92003cd-6622-4a82-a3c7-69d6222f0ba0")
add_chromatic_weapon_element("Fire",
                             "Spell_Evocation_ChromaticOrb_Fire",
                             PrepareSound="Spell_Prepare_Buff_ElementalWeaponFire_L1to3",
                             PrepareLoopSound="Spell_Loop_Buff_ElementalWeaponFire_L1to3L1to3",
                             CastSound="Spell_Cast_Buff_ElementalWeaponFire_L1to3",
                             TargetSound="Spell_Impact_Buff_ElementalWeaponFire_L1to3",
                             PrepareEffect="6e0c79d5-f724-4628-8669-da3d766e9b83",
                             CastEffect="d8ed1647-82eb-4079-a914-1b2c2a89f153",
                             TargetEffect="e4d6914d-1a62-41b4-8932-eee907f2c200",
                             StatusEffect="8a4c7e6e-a629-4765-9c5d-d354838703d8")
add_chromatic_weapon_element("Force",
                             "Spell_Evocation_ChromaticOrb",
                             PrepareSound="Spell_Prepare_Buff_ElementalWeaponThunder_L1to3",
                             PrepareLoopSound="Spell_Loop_Buff_ElementalWeaponThunder_L1to3",
                             CastSound="Spell_Cast_Buff_ElementalWeaponThunder_L1to3",
                             TargetSound="Spell_Impact_Buff_ElementalWeaponThunder_L1to3",
                             PrepareEffect="9b6f51df-22cc-49cf-9ae9-a0e0ac0f8882",
                             CastEffect="bfeec9c4-0287-4a24-a104-b2ae38d85b4f",
                             TargetEffect="5e3997ae-d2f5-4b97-96e3-c987e6b9584d",
                             StatusEffect="ae580720-fde4-4596-b671-b5280cdbe9eb")
add_chromatic_weapon_element("Lightning",
                             "Spell_Evocation_ChromaticOrb_Lightning",
                             PrepareSound="Spell_Prepare_Buff_ElementalWeaponLightning_L1to3",
                             PrepareLoopSound="Spell_Loop_Buff_ElementalWeaponLightning_L1to3",
                             CastSound="Spell_Cast_Buff_ElementalWeaponLightning_L1to3",
                             TargetSound="Spell_Impact_Buff_ElementalWeaponLightning_L1to3",
                             PrepareEffect="460e98c4-4e94-47b9-bd21-75088d0d8e52",
                             CastEffect="da768bec-1f51-4d6f-8617-a3a6c2c01a58",
                             TargetEffect="7547b944-e3e5-4b6d-b2e9-8320425b4f12",
                             StatusEffect="7905bb82-0284-46b8-855b-24f17560fe4a")
add_chromatic_weapon_element("Poison",
                             "Spell_Evocation_ChromaticOrb_Poison",
                             PrepareSound="Spell_Prepare_Buff_ElementalWeaponAcid_L1to3",
                             PrepareLoopSound="Spell_Loop_Buff_ElementalWeaponAcid_L1to3",
                             CastSound="Spell_Cast_Buff_ElementalWeaponAcid_L1to3",
                             TargetSound="Spell_Impact_Buff_ElementalWeaponAcid_L1to3",
                             PrepareEffect="803e65f9-b27c-4e9c-af2a-8cf0e8e8564d",
                             CastEffect="dfb57578-dafa-4c39-9f6e-238b9e2c237d",
                             TargetEffect="89018ece-411e-4c00-94ec-6cb3743f4af5",
                             StatusEffect="3798c69d-e202-4323-b660-2e1778dafafc")
add_chromatic_weapon_element("Thunder",
                             "Spell_Evocation_ChromaticOrb_Thunder",
                             PrepareSound="Spell_Prepare_Buff_ElementalWeaponThunder_L1to3",
                             PrepareLoopSound="Spell_Loop_Buff_ElementalWeaponThunder_L1to3",
                             CastSound="Spell_Cast_Buff_ElementalWeaponThunder_L1to3",
                             TargetSound="Spell_Impact_Buff_ElementalWeaponThunder_L1to3",
                             PrepareEffect="9b6f51df-22cc-49cf-9ae9-a0e0ac0f8882",
                             CastEffect="bfeec9c4-0287-4a24-a104-b2ae38d85b4f",
                             TargetEffect="5e3997ae-d2f5-4b97-96e3-c987e6b9584d",
                             StatusEffect="ca0b3ab3-dac0-47f7-b313-7ca69c85b5b4")

loca["ChromaticBlade_Charge_DisplayName"] = {"en": "Charge"}
loca["ChromaticBlade_Charge_Description"] = {"en": """
    Charge forward and attack the first enemy in your way.
    """}

chromatic_blade.add(SpellData(
    "ChromaticBlade_Charge",
    SpellType="Zone",
    using="Rush_SpringAttack",
    DisplayName=loca["ChromaticBlade_Charge_DisplayName"],
    Description=loca["ChromaticBlade_Charge_Description"],
    TooltipDamageList=["DealDamage(MainMeleeWeapon/2,MainWeaponDamageType)"],
    TooltipAttackSave="",
    TooltipStatusApply="",
    Cooldown="None",
    SpellSuccess=[
        "DealDamage(MainMeleeWeapon/2,MainWeaponDamageType)",
        "GROUND:ExecuteWeaponFunctors(MainHand)",
    ],
    UseCosts="BonusActionPoint:1",
))

chromatic_blade.add(SpellData(
    "ChromaticBlade_Cleave",
    SpellType="Zone",
    using="Zone_Cleave",
    Cooldown="None",
))

chromatic_blade.add_treasure_table("""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_ChromaticBlade_Sword",1,0,0,0,0,0,0,0
""")

chromatic_blade.build()
