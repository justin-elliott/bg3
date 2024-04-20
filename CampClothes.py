#!/usr/bin/env python3
"""
Generates files for the "CampClothes" mod.
"""

import os

from moddb import Bolster, Defense, PackMule
from modtools.gamedata import Armor, ObjectData, StatusData
from modtools.lsx.game import GameObjects
from modtools.mod import Mod
from modtools.text import TreasureTable
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",


camp_clothes = Mod(os.path.dirname(__file__),
                   author="justin-elliott",
                   name="CampClothes",
                   mod_uuid=UUID("a93f92ad-5b31-4c9c-ac66-41082788e567"),
                   description="Adds a selection of outfits to the tutorial chest.")

loca = camp_clothes.get_localization()

loca["CampClothes_ComfortableBoots_DisplayName"] = {"en": "Comfortable Boots"}
loca["CampClothes_ComfortableBoots_Description"] = {"en": """
    Made of soft, sheepskin-lined leather, these are the perfect boots to wear around the campfire on a chilly night.
    """}

arm_boots_leather_a = UUID("cf987856-1381-477e-88db-6b359f7e19e8")
comfortable_boots_game_objects_uuid = UUID("ffda4777-7b6b-4582-b128-5f0175419b4a")

camp_clothes.add(GameObjects(
    DisplayName=loca["CampClothes_ComfortableBoots_DisplayName"],
    Description=loca["CampClothes_ComfortableBoots_Description"],
    LevelName="",
    MapKey=comfortable_boots_game_objects_uuid,
    Name="CampClothes_ComfortableBoots",
    ParentTemplateId=arm_boots_leather_a,
    Stats="CampClothes_ComfortableBoots",
    Type="item",
))

camp_clothes.add(Armor(
    "CampClothes_ComfortableBoots",
    using="ARM_Camp_Shoes",
    RootTemplate=comfortable_boots_game_objects_uuid,
))

loot_gen_backpack_a_posed_a = UUID("47805d79-88f1-4933-86eb-f78f67cbc33f")


def camp_clothes_container(name: str) -> None:
    container_uuid = camp_clothes.make_uuid(name)

    camp_clothes.add(GameObjects(
        DisplayName=loca[f"{name}_DisplayName"],
        Description=loca[f"{name}_Description"],
        Icon="Item_CONT_GEN_Chest_Travel_A_Small_A",
        LevelName="",
        MapKey=container_uuid,
        Name=name,
        ParentTemplateId=loot_gen_backpack_a_posed_a,
        Stats=name,
        Type="item",
        children=[
            GameObjects.InventoryList(children=[
                GameObjects.InventoryList.InventoryItem(
                    Object=f"{name}_TreasureTable",
                ),
            ]),
        ],
    ))

    camp_clothes.add(ObjectData(
        name,
        using="_Container",
        RootTemplate=container_uuid,
        Weight=0.01,
    ))


base_potion_name = f"{camp_clothes.get_prefix()}_BasePotion"
camp_clothes.add(ObjectData(
    base_potion_name,
    using="OBJ_Bottle",
    ValueUUID="4c5217d8-0232-4592-9e32-2fd729123f53",
    ValueOverride="3",
    Rarity="Legendary",
    ObjectCategory="",
))

potion_parent_template_id = UUID("8e660fd9-489d-42ff-a762-e4392e826666")
POTION_STATUS_PROPERTY_FLAGS = [
    "DisableOverhead",
    "IgnoreResting",
    "DisableCombatlog",
    "DisablePortraitIndicator",
]


def add_potion(
        name: str,
        *,
        uuid: UUID,
        display_name: str,
        description: str,
        icon: str,
        status_duration: int = -1,
        boosts: list[str] = None,
        passives: list[str] = None,
        status_property_flags: list[str] = POTION_STATUS_PROPERTY_FLAGS) -> None:
    camp_clothes.add(GameObjects(
        DisplayName=display_name,
        Description=description,
        Flag_int32=0,
        Icon=icon,
        LevelName="",
        MapKey=uuid,
        Name=name,
        OnUseDescription=("hc857245cg5f9dg4f90g88d4g604f596d85ca", 1),
        ParentTemplateId=potion_parent_template_id,
        Stats=name,
        Type="item",
        VisualTemplate="a93bcc13-e31b-f6a6-7076-e64fe7771d9e",
        children=[
            GameObjects.Bounds(children=[
                GameObjects.Bounds.Bound(
                    Height=0.418184,
                    Max="0.21 0.62 0.2",
                    Min="-0.21 0 -0.2",
                    Radius=0.114147,
                    Shape=1,
                    Type=1,
                ),
                GameObjects.Bounds.Bound(
                    Height=0.418184,
                    Max="0.21 0.62 0.2",
                    Min="-0.21 0 -0.2",
                    Radius=0.114147,
                    Shape=1,
                    Type=2,
                ),
                GameObjects.Bounds.Bound(
                    Height=0.418184,
                    Max="0.21 0.62 0.2",
                    Min="-0.21 0 -0.2",
                    Radius=0.114147,
                    Shape=1,
                    Type=0,
                ),
            ]),
            GameObjects.InventoryList(),
            GameObjects.OnDestroyActions(children=[
                GameObjects.OnDestroyActions.Action(
                    ActionType=26,
                    children=[
                        GameObjects.OnDestroyActions.Action.Attributes(
                            ActivateSoundEvent="3ea82655-5140-4287-9ab8-794559f182d3",
                            Animation="",
                            Conditions="",
                            PlayOnHUD=False,
                        ),
                    ],
                ),
                GameObjects.OnDestroyActions.Action(
                    ActionType=5,
                    children=[
                        GameObjects.OnDestroyActions.Action.Attributes(
                            Animation="",
                            Conditions="",
                            ExplodeFX="df744de3-fb7f-4808-6881-fd466107d27f",
                            FadeOutDelay=0,
                            FadeOutFX="",
                            SnapToGround=True,
                            TargetItemState=0,
                            VisualWithDynamicPhysics="",
                            templateAfterDestruction="",
                            visualDestruction="00000000-0000-0000-0000-000000000000",
                        ),
                    ],
                ),
            ]),
            GameObjects.OnUsePeaceActions(children=[
                GameObjects.OnUsePeaceActions.Action(
                    ActionType=7,
                    children=[
                        GameObjects.OnUsePeaceActions.Action.Attributes(
                            Animation="",
                            Conditions="",
                            Consume=True,
                            IsHiddenStatus=True,
                            StatsId=name.upper(),
                            StatusDuration=status_duration,
                        ),
                    ],
                ),
            ]),
        ],
    ))

    camp_clothes.add(ObjectData(
        name,
        using=base_potion_name,
        RootTemplate=uuid,
    ))

    camp_clothes.add(StatusData(
        name.upper(),
        StatusType="BOOST",
        DisplayName=display_name,
        Description=description,
        Icon=icon,
        Boosts=boosts,
        Passives=passives,
        StatusPropertyFlags=status_property_flags,
    ))


def add_agility_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_AgilityPotion"
    agility_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Agility"}
    loca[f"{name}_Description"] = {"en": """
        Drinking this elixir grants you <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all
        <LSTag Tooltip="Dexterity">Dexterity</LSTag> Skills, and
        <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in, and
        <LSTag Tooltip="Advantage">Advantage</LSTag> on, Dexterity <LSTag Tooltip="AbilityCheck">Checks</LSTag>.
        """}

    add_potion(
        name,
        uuid=agility_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_ALCH_Solution_Remedy",
        boosts=[
            "ProficiencyBonus(SavingThrow,Dexterity)",
            "Advantage(Ability,Dexterity)",
            "ProficiencyBonus(Skill,Acrobatics)",
            "ExpertiseBonus(Acrobatics)",
            "ProficiencyBonus(Skill,SleightOfHand)",
            "ExpertiseBonus(SleightOfHand)",
            "ProficiencyBonus(Skill,Stealth)",
            "ExpertiseBonus(Stealth)",
        ],
    )

    return name


def add_bolster_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_BolsterPotion"
    bolster = Bolster(camp_clothes).add_bolster()
    bolster_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Bolstering"}
    loca[f"{name}_Description"] = {"en": f"""
        Drinking this elixir grants the <LSTag Type="Spell" Tooltip="{bolster}">Bolster</LSTag> spell.
        """}

    add_potion(
        name,
        uuid=bolster_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_CONS_Drink_Potion_B",
        boosts=[f"UnlockSpell({bolster})"],
    )

    return name


def add_overpowering_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_OverpoweringPotion"
    persuasion_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Potion of Overpowering"}
    loca[f"{name}_Description"] = {"en": """
        Temporarily gain a significant boost to your health, armor class, attack rolls, damage rolls, and saving throws.
        """}

    add_potion(
        name,
        uuid=persuasion_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_CONS_Drug_Dreammist_A",
        status_duration=16,
        boosts=[
            "AC(20)",
            "DamageBonus(20)",
            "IncreaseMaxHP(50)",
            "RollBonus(Attack,20)",
            "RollBonus(SavingThrow,20)",
            "IgnoreResistance(Bludgeoning,Resistant)",
            "IgnoreResistance(Piercing,Resistant)",
            "IgnoreResistance(Slashing,Resistant)",
        ],
        status_property_flags=None,
    )

    return name


def add_pack_mule_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_PackMulePotion"
    pack_mule = PackMule(camp_clothes).add_pack_mule(2.0)
    pack_mule_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of the Pack Mule"}
    loca[f"{name}_Description"] = {"en": f"""
        Drinking this elixir grants the <LSTag Type="Passive" Tooltip="{pack_mule}">Pack Mule</LSTag> passive.
        """}

    add_potion(
        name,
        uuid=pack_mule_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_CONS_Drink_Potion_A",
        passives=[pack_mule],
    )

    return name


def add_persuasion_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_PersuasionPotion"
    persuasion_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Persuasion"}
    loca[f"{name}_Description"] = {"en": """
        Drinking this elixir grants you <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all
        <LSTag Tooltip="Charisma">Charisma</LSTag> Skills, and
        <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in, and
        <LSTag Tooltip="Advantage">Advantage</LSTag> on, Charisma <LSTag Tooltip="AbilityCheck">Checks</LSTag>.
        """}

    add_potion(
        name,
        uuid=persuasion_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_CONS_ElixirOfHealth",
        boosts=[
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

    return name


def add_warding_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_WardingPotion"
    warding = Defense(camp_clothes).add_warding()
    warding_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Warding"}
    loca[f"{name}_Description"] = {"en": f"""
        Drinking this elixir grants the <LSTag Type="Passive" Tooltip="Tough">Tough</LSTag>,
        <LSTag Type="Passive" Tooltip="UnarmouredDefence_Barbarian">Unarmoured Defence</LSTag>, and
        <LSTag Type="Passive" Tooltip="{warding}">Warding</LSTag> passives.

        You gain <LSTag Tooltip="Advantage">Advantage</LSTag> on <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>
        to maintain <LSTag Tooltip="Concentration">Concentration</LSTag> on a spell, and
        <LSTag Tooltip="Proficiency">Proficiency</LSTag> in Constitution
        <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>.
        """}

    add_potion(
        name,
        uuid=warding_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_UNI_Apprentice_Antidote",
        boosts=[
            "Advantage(Concentration)",
            "ProficiencyBonus(SavingThrow,Constitution)",
        ],
        passives=[
            "Tough",
            "UnarmouredDefence_Barbarian",
            warding,
        ],
    )

    return name


def reduce_weight(items: list[str]) -> list[str]:
    new_items = []
    for item in items:
        name = "CampClothes" + item.removeprefix("ARM")
        camp_clothes.add(Armor(
            name,
            using=item,
            Weight=0.01,
        ))
        new_items.append(name)
    return new_items


loca["CampClothes_Clothing_DisplayName"] = {"en": "Camp Clothes"}
loca["CampClothes_Clothing_Description"] = {"en": """
    Contains a selection of camp clothing.
    """}
camp_clothes_container("CampClothes_Clothing")

loca["CampClothes_Dyes_DisplayName"] = {"en": "Dyes"}
loca["CampClothes_Dyes_Description"] = {"en": """
    Contains a selection of dyes.
    """}
camp_clothes_container("CampClothes_Dyes")

loca["CampClothes_Shoes_DisplayName"] = {"en": "Camp Shoes"}
loca["CampClothes_Shoes_Description"] = {"en": """
    Contains a selection of camp shoes.
    """}
camp_clothes_container("CampClothes_Shoes")

loca["CampClothes_Underwear_DisplayName"] = {"en": "Underwear"}
loca["CampClothes_Underwear_Description"] = {"en": """
    Contains a selection of underwear.
    """}
camp_clothes_container("CampClothes_Underwear")

base_clothing = [
    "ARM_Camp_Body_Astarion",
    "ARM_Camp_Body_Gale",
    "ARM_Camp_Body_Halsin",
    "ARM_Camp_Body_Jaheira",
    "ARM_Camp_Body_Karlach",
    "ARM_Camp_Body_Laezel",
    "ARM_Camp_Body_Minsc",
    "ARM_Camp_Body_Minthara",
    "ARM_Camp_Body_Shadowheart",
    "ARM_Camp_Body_Wyll",
    "ARM_Vanity_Body_Aristocrat_Brown",
    "ARM_Vanity_Body_Aristocrat_White",
    "ARM_Vanity_Body_Aristocrat",
    "ARM_Vanity_Body_Circus_B",
    "ARM_Vanity_Body_Circus",
    "ARM_Vanity_Body_Citizen_B_Teal",
    "ARM_Vanity_Body_Citizen_B",
    "ARM_Vanity_Body_Citizen_Black",
    "ARM_Vanity_Body_Citizen_C_Blue",
    "ARM_Vanity_Body_Citizen_C_Green",
    "ARM_Vanity_Body_Citizen_C_Red",
    "ARM_Vanity_Body_Citizen_C",
    "ARM_Vanity_Body_Citizen_Purple",
    "ARM_Vanity_Body_Citizen",
    "ARM_Vanity_Body_Cultist",
    "ARM_Vanity_Body_Deva",
    "ARM_Vanity_Body_Drow",
    "ARM_Vanity_Body_Leather_Black",
    "ARM_Vanity_Body_Leather_Bright",
    "ARM_Vanity_Body_Leather_Rich_Blue",
    "ARM_Vanity_Body_Leather_Rich_Green",
    "ARM_Vanity_Body_Leather_Rich",
    "ARM_Vanity_Body_Leather",
    "ARM_Vanity_Body_Pants",
    "ARM_Vanity_Body_Patriars_Black",
    "ARM_Vanity_Body_Patriars_Blue",
    "ARM_Vanity_Body_Patriars_Green",
    "ARM_Vanity_Body_Patriars_Red",
    "ARM_Vanity_Body_Patriars",
    "ARM_Vanity_Body_Prison",
    "ARM_Vanity_Body_Refugee_Gray",
    "ARM_Vanity_Body_Refugee_Green",
    "ARM_Vanity_Body_Refugee",
    "ARM_Vanity_Body_Rich_B_Purple",
    "ARM_Vanity_Body_Rich_B",
    "ARM_Vanity_Body_Rich_B1_Beige",
    "ARM_Vanity_Body_Rich_B1",
    "ARM_Vanity_Body_Rich_C_Blue",
    "ARM_Vanity_Body_Rich_C_Red",
    "ARM_Vanity_Body_Rich_C",
    "ARM_Vanity_Body_Rich_D_Blue",
    "ARM_Vanity_Body_Rich_D_Green",
    "ARM_Vanity_Body_Rich_D_Purple",
    "ARM_Vanity_Body_Rich_D_White",
    "ARM_Vanity_Body_Rich_D",
    "ARM_Vanity_Body_Rich_E_GreenPink",
    "ARM_Vanity_Body_Rich_E_Teal",
    "ARM_Vanity_Body_Rich_E",
    "ARM_Vanity_Body_Rich_F_Blue",
    "ARM_Vanity_Body_Rich_F",
    "ARM_Vanity_Body_Rich_G_Black",
    "ARM_Vanity_Body_Rich_G_Bright",
    "ARM_Vanity_Body_Rich_G_Brown",
    "ARM_Vanity_Body_Rich_G_Red",
    "ARM_Vanity_Body_Rich_G",
    "ARM_Vanity_Body_Rich_G2_Blue",
    "ARM_Vanity_Body_Rich_G2_Green",
    "ARM_Vanity_Body_Rich_G2_Purple",
    "ARM_Vanity_Body_Rich_G2_White",
    "ARM_Vanity_Body_Rich_G2",
    "ARM_Vanity_Body_Rich_Gold",
    "ARM_Vanity_Body_Rich_Green",
    "ARM_Vanity_Body_Rich_Teal",
    "ARM_Vanity_Body_Rich",
    "ARM_Vanity_Body_Shar",
    "ARM_Vanity_Body_Shirt_Black",
    "ARM_Vanity_Body_Shirt_Blue",
    "ARM_Vanity_Body_Shirt_Green",
    "ARM_Vanity_Body_Shirt_Purple",
    "ARM_Vanity_Body_Shirt_Red",
    "ARM_Vanity_ElegantRobe",
    "ARM_Vanity_Prison_Poor",
    "UNI_DaisyPlaysuit",
]

base_dyes = [
    "OBJ_Dye_Azure",
    "OBJ_Dye_BlackBlue",
    "OBJ_Dye_BlackGreen",
    "OBJ_Dye_BlackPink",
    "OBJ_Dye_BlackRed",
    "OBJ_Dye_BlackTeal",
    "OBJ_Dye_Blue",
    "OBJ_Dye_BlueGreen",
    "OBJ_Dye_BluePurple",
    "OBJ_Dye_BlueYellow",
    "OBJ_Dye_BlueYellow_02",
    "OBJ_Dye_Golden",
    "OBJ_Dye_Green",
    "OBJ_Dye_Green_02",
    "OBJ_Dye_GreenSage",
    "OBJ_Dye_GreenSwamp",
    "OBJ_Dye_GreenPink",
    "OBJ_Dye_IceCream",
    "OBJ_Dye_IceCream_02",
    "OBJ_Dye_IceCream_03",
    "OBJ_Dye_IceCream_04",
    "OBJ_Dye_Maroon",
    "OBJ_Dye_Ocean",
    "OBJ_Dye_Orange",
    "OBJ_Dye_OrangeBlue",
    "OBJ_Dye_Pink",
    "OBJ_Dye_Purple",
    "OBJ_Dye_Purple_02",
    "OBJ_Dye_Purple_03",
    "OBJ_Dye_Purple_04",
    "OBJ_Dye_PurpleRed",
    "OBJ_Dye_Red",
    "OBJ_Dye_RedBrown",
    "OBJ_Dye_RedWhite",
    "OBJ_Dye_RichRed",
    "OBJ_Dye_RoyalBlue",
    "OBJ_Dye_Teal",
    "OBJ_Dye_WhiteBlack",
    "OBJ_Dye_WhiteBrown",
    "OBJ_Dye_WhiteRed",
    "OBJ_Dye_Remover",
]

base_shoes = [
    "CampClothes_ComfortableBoots",
    "ARM_Camp_Sandals_A1_Black",
    "ARM_Camp_Sandals_A1",
    "ARM_Camp_Sandals_B_Red",
    "ARM_Camp_Sandals_B",
    "ARM_Camp_Sandals_Blue",
    "ARM_Camp_Sandals_C",
    "ARM_Camp_Sandals",
    "ARM_Camp_Shoes_B",
    "ARM_Camp_Shoes_C",
    "ARM_Camp_Shoes_E",
    "ARM_Camp_Shoes_F",
    "ARM_Camp_Shoes",
    "ARM_Camp_Shoes_Astarion",
    "ARM_Camp_Shoes_Gale",
    "ARM_Camp_Shoes_Halsin",
    "ARM_Camp_Shoes_Jaheira",
    "ARM_Camp_Shoes_Karlach",
    "ARM_Camp_Shoes_Laezel",
    "ARM_Camp_Shoes_Minsc",
    "ARM_Camp_Shoes_Minthara",
    "ARM_Camp_Shoes_Shadowheart",
    "ARM_Camp_Shoes_Wyll",
    "ARM_Vanity_Deva_Shoes",
    "ARM_Vanity_Shoes_Circus",
]

base_underwear = [
    "ARM_Underwear_Dragonborn_Bronze",
    "ARM_Underwear_Dragonborn",
    "ARM_Underwear_Dwarves_Green",
    "ARM_Underwear_Dwarves",
    "ARM_Underwear_Elves_Blue",
    "ARM_Underwear_Elves_Purple",
    "ARM_Underwear_Elves",
    "ARM_Underwear_Githyanki_Black",
    "ARM_Underwear_Githyanki",
    "ARM_Underwear_Gnomes_Blue",
    "ARM_Underwear_Gnomes",
    "ARM_Underwear_Halflings",
    "ARM_Underwear_HalfOrcs_Orange",
    "ARM_Underwear_HalfOrcs",
    "ARM_Underwear_Humans_B",
    "ARM_Underwear_Humans_C",
    "ARM_Underwear_Humans",
    "ARM_Underwear_Incubus",
    "ARM_Underwear_Tieflings",
    "ARM_Underwear_Astarion",
    "ARM_Underwear_Gale",
    "ARM_Underwear_Halsin",
    "ARM_Underwear_Jaheira",
    "ARM_Underwear_Karlach",
    "ARM_Underwear_Laezel",
    "ARM_Underwear_Minsc",
    "ARM_Underwear_Minthara",
    "ARM_Underwear_Shadowheart",
    "ARM_Underwear_Wyll",
]

dyes = [dye for dye in base_dyes]
agility_potion = add_agility_potion()
bolster_potion = add_bolster_potion()
overpowering_potion = add_overpowering_potion()
pack_mule_potion = add_pack_mule_potion()
persuasion_potion = add_persuasion_potion()
warding_potion = add_warding_potion()

clothing = reduce_weight(base_clothing)
shoes = reduce_weight(base_shoes)
underwear = reduce_weight(base_underwear)

outfit_template = """\
new subtable "1,1"
object category I_{},1,0,0,0,0,0,0,0
"""

dye_template = """\
new subtable "10,1"
object category I_{},1,0,0,0,0,0,0,0
"""

dye_entries = "".join(dye_template.format(dye) for dye in dyes).rstrip()

camp_clothes.add(TreasureTable(f"""
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_CampClothes_Clothing",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_CampClothes_Dyes",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_CampClothes_Shoes",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_CampClothes_Underwear",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_{agility_potion}",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_{bolster_potion}",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_{overpowering_potion}",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_{pack_mule_potion}",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_{persuasion_potion}",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_{warding_potion}",1,0,0,0,0,0,0,0
new subtable "1600,1"
object category "Gold",1,0,0,0,0,0,0,0
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Clothing_TreasureTable"
CanMerge 1
{"".join(outfit_template.format(outfit) for outfit in clothing).rstrip()}
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Dyes_TreasureTable"
CanMerge 1
{"".join(dye_template.format(dye) for dye in dyes).rstrip()}
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Shoes_TreasureTable"
CanMerge 1
{"".join(outfit_template.format(outfit) for outfit in shoes).rstrip()}
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Underwear_TreasureTable"
CanMerge 1
{"".join(outfit_template.format(outfit) for outfit in underwear).rstrip()}
"""))

camp_clothes.build()
