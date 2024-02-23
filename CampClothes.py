#!/usr/bin/env python3
"""
Generates files for the "CampClothes" mod.
"""

import os

from modtools.gamedata import Armor
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

shoes = [
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
    "ARM_Vanity_Deva_Shoes",
    "ARM_Vanity_Shoes_Circus",
]

underwear = [
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
    "ARM_Underwear",
]

clothes = [
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

dyes = [
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

outfit_template = """\
new subtable "1,1"
object category I_{},1,0,0,0,0,0,0,0
"""

outfit_entries = "".join(outfit_template.format(outfit) for outfit in shoes + underwear + clothes).rstrip()

dye_template = """\
new subtable "10,1"
object category I_{},1,0,0,0,0,0,0,0
"""

dye_entries = "".join(dye_template.format(dye) for dye in dyes).rstrip()

camp_clothes.add(TreasureTable(f"""
new treasuretable "TUT_Chest_Potions"
CanMerge 1
{outfit_entries}
{dye_entries}
new subtable "1600,1"
object category "Gold",1,0,0,0,0,0,0,0
"""))

camp_clothes.build()
