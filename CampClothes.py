#!/usr/bin/env python3
"""
Generates files for the "CampClothes" mod.
"""

import os

from modtools.gamedata import armor_data
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

camp_clothes.add(armor_data(
    "CampClothes_ComfortableBoots",
    using="ARM_Camp_Shoes",
    RootTemplate=str(comfortable_boots_game_objects_uuid),
))

camp_clothes.add_treasure_table("""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_CampClothes_ComfortableBoots",1,0,0,0,0,0,0,0
new subtable "10,1"
object category "I_OBJ_Dye_Ocean",1,0,0,0,0,0,0,0
""")

camp_clothes.build()
