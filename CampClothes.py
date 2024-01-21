#!/usr/bin/env python3
"""
Generates files for the "CampClothes" mod.
"""

import os

from modtools.gamedata import armor_data
from modtools.lsx import Lsx
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

boots_of_aid_and_comfort_uuid = UUID("bc090f4e-ff74-49f6-a3f2-7eb561f57436")
comfortable_boots_game_objects_uuid = UUID("ffda4777-7b6b-4582-b128-5f0175419b4a")

camp_clothes.add_root_templates([
    Lsx.Node("GameObjects", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["CampClothes_ComfortableBoots_DisplayName"], version=1),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["CampClothes_ComfortableBoots_Description"], version=1),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(comfortable_boots_game_objects_uuid)),
        Lsx.Attribute("Name", "LSString", value="CampClothes_ComfortableBoots"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value=str(boots_of_aid_and_comfort_uuid)),
        Lsx.Attribute("Stats", "FixedString", value="CampClothes_ComfortableBoots"),
        Lsx.Attribute("Type", "FixedString", value="item"),
    ]),
])

camp_clothes.add(armor_data(
    "CampClothes_ComfortableBoots",
    using="ARM_Camp_Shoes",
    RootTemplate=str(comfortable_boots_game_objects_uuid),
))

camp_clothes.add_treasure_table("""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_ARM_Vanity_Body_Leather_Black",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_CampClothes_ComfortableBoots",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_ARM_Underwear_HalfOrcs",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_ARM_Underwear_Incubus",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_ARM_Underwear_Tieflings",1,0,0,0,0,0,0,0
""")

camp_clothes.build()
