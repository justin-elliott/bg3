#!/usr/bin/env python3
"""
Generates files for the "CampClothes" mod.
"""

import os

from modtools.gamedata import Armor
from modtools.lsx.game import GameObjects
from modtools.mod import Mod
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

outfits = [
    "I_CampClothes_ComfortableBoots",
    "I_ARM_Camp_Sandals_A1_Black",
    "I_ARM_Camp_Sandals_A1",
    "I_ARM_Camp_Sandals_B_Red",
    "I_ARM_Camp_Sandals_B",
    "I_ARM_Camp_Sandals_Blue",
    "I_ARM_Camp_Sandals_C",
    "I_ARM_Camp_Sandals",
    "I_ARM_Camp_Shoes_B",
    "I_ARM_Camp_Shoes_C",
    "I_ARM_Camp_Shoes_E",
    "I_ARM_Camp_Shoes_F",
    "I_ARM_Camp_Shoes",
    "I_ARM_Vanity_Deva_Shoes",
    "I_ARM_Vanity_Shoes_Circus",
    "I_ARM_Underwear_Dragonborn_Bronze",
    "I_ARM_Underwear_Dragonborn",
    "I_ARM_Underwear_Dwarves_Green",
    "I_ARM_Underwear_Dwarves",
    "I_ARM_Underwear_Elves_Blue",
    "I_ARM_Underwear_Elves_Purple",
    "I_ARM_Underwear_Elves",
    "I_ARM_Underwear_Githyanki_Black",
    "I_ARM_Underwear_Githyanki",
    "I_ARM_Underwear_Gnomes_Blue",
    "I_ARM_Underwear_Gnomes",
    "I_ARM_Underwear_Halflings",
    "I_ARM_Underwear_HalfOrcs_Orange",
    "I_ARM_Underwear_HalfOrcs",
    "I_ARM_Underwear_Humans_B",
    "I_ARM_Underwear_Humans_C",
    "I_ARM_Underwear_Humans",
    "I_ARM_Underwear_Incubus",
    "I_ARM_Underwear_Tieflings",
    "I_ARM_Underwear",
    "I_ARM_Vanity_Body_Aristocrat_Brown",
    "I_ARM_Vanity_Body_Aristocrat_White",
    "I_ARM_Vanity_Body_Aristocrat",
    "I_ARM_Vanity_Body_Circus_B",
    "I_ARM_Vanity_Body_Circus",
    "I_ARM_Vanity_Body_Citizen_B_Teal",
    "I_ARM_Vanity_Body_Citizen_B",
    "I_ARM_Vanity_Body_Citizen_Black",
    "I_ARM_Vanity_Body_Citizen_C_Blue",
    "I_ARM_Vanity_Body_Citizen_C_Green",
    "I_ARM_Vanity_Body_Citizen_C_Red",
    "I_ARM_Vanity_Body_Citizen_C",
    "I_ARM_Vanity_Body_Citizen_Purple",
    "I_ARM_Vanity_Body_Citizen",
    "I_ARM_Vanity_Body_Cultist",
    "I_ARM_Vanity_Body_Deva",
    "I_ARM_Vanity_Body_Drow",
    "I_ARM_Vanity_Body_Leather_Black",
    "I_ARM_Vanity_Body_Leather_Bright",
    "I_ARM_Vanity_Body_Leather_Rich_Blue",
    "I_ARM_Vanity_Body_Leather_Rich_Green",
    "I_ARM_Vanity_Body_Leather_Rich",
    "I_ARM_Vanity_Body_Leather",
    "I_ARM_Vanity_Body_Pants",
    "I_ARM_Vanity_Body_Patriars_Black",
    "I_ARM_Vanity_Body_Patriars_Blue",
    "I_ARM_Vanity_Body_Patriars_Green",
    "I_ARM_Vanity_Body_Patriars_Red",
    "I_ARM_Vanity_Body_Patriars",
    "I_ARM_Vanity_Body_Prison",
    "I_ARM_Vanity_Body_Refugee_Gray",
    "I_ARM_Vanity_Body_Refugee_Green",
    "I_ARM_Vanity_Body_Refugee",
    "I_ARM_Vanity_Body_Rich_B_Purple",
    "I_ARM_Vanity_Body_Rich_B",
    "I_ARM_Vanity_Body_Rich_B1_Beige",
    "I_ARM_Vanity_Body_Rich_B1",
    "I_ARM_Vanity_Body_Rich_C_Blue",
    "I_ARM_Vanity_Body_Rich_C_Red",
    "I_ARM_Vanity_Body_Rich_C",
    "I_ARM_Vanity_Body_Rich_D_Blue",
    "I_ARM_Vanity_Body_Rich_D_Green",
    "I_ARM_Vanity_Body_Rich_D_Purple",
    "I_ARM_Vanity_Body_Rich_D_White",
    "I_ARM_Vanity_Body_Rich_D",
    "I_ARM_Vanity_Body_Rich_E_GreenPink",
    "I_ARM_Vanity_Body_Rich_E_Teal",
    "I_ARM_Vanity_Body_Rich_E",
    "I_ARM_Vanity_Body_Rich_F_Blue",
    "I_ARM_Vanity_Body_Rich_F",
    "I_ARM_Vanity_Body_Rich_G_Black",
    "I_ARM_Vanity_Body_Rich_G_Bright",
    "I_ARM_Vanity_Body_Rich_G_Brown",
    "I_ARM_Vanity_Body_Rich_G_Red",
    "I_ARM_Vanity_Body_Rich_G",
    "I_ARM_Vanity_Body_Rich_G2_Blue",
    "I_ARM_Vanity_Body_Rich_G2_Green",
    "I_ARM_Vanity_Body_Rich_G2_Purple",
    "I_ARM_Vanity_Body_Rich_G2_White",
    "I_ARM_Vanity_Body_Rich_G2",
    "I_ARM_Vanity_Body_Rich_Gold",
    "I_ARM_Vanity_Body_Rich_Green",
    "I_ARM_Vanity_Body_Rich_Teal",
    "I_ARM_Vanity_Body_Rich",
    "I_ARM_Vanity_Body_Shar",
    "I_ARM_Vanity_Body_Shirt_Black",
    "I_ARM_Vanity_Body_Shirt_Blue",
    "I_ARM_Vanity_Body_Shirt_Green",
    "I_ARM_Vanity_Body_Shirt_Purple",
    "I_ARM_Vanity_Body_Shirt_Red",
    "I_ARM_Vanity_ElegantRobe",
    "I_ARM_Vanity_Prison_Poor",
    "I_UNI_DaisyPlaysuit",
]

outfit_template = """\
new subtable "1,1"
object category {},1,0,0,0,0,0,0,0
"""

outfit_entries = "".join(outfit_template.format(outfit) for outfit in outfits).rstrip()

camp_clothes.add_treasure_table(f"""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
{outfit_entries}
new subtable "10,1"
object category "I_OBJ_Dye_Ocean",1,0,0,0,0,0,0,0
""")

camp_clothes.build()
