#!/usr/bin/env python3
"""
Generates files for the "ComfortableBoots" mod.
"""

import os

from modtools.gamedata import Armor
from modtools.lsx.game import GameObjects
from modtools.mod import Mod
from modtools.text import Text, TreasureTable
from uuid import UUID


class ItemCombinations(Text):
    @property
    def path(self) -> str:
        return "Public/{folder}/Stats/Generated/ItemCombos.txt"


comfortable_boots = Mod(os.path.dirname(__file__),
                        author="justin-elliott",
                        name="ComfortableBoots",
                        description="Adds Comfortable Boots to the tutorial chest.")

loca = comfortable_boots.get_localization()

loca[f"{comfortable_boots.get_prefix()}_DisplayName"] = {"en": "Comfortable Boots"}
loca[f"{comfortable_boots.get_prefix()}_Description"] = {"en": """
    Made of soft, sheepskin-lined leather, these are the perfect boots to wear around the campfire on a chilly night.
    """}

arm_boots_leather_a = UUID("cf987856-1381-477e-88db-6b359f7e19e8")
comfortable_boots_game_objects_uuid = comfortable_boots.make_uuid("Comfortable Boots")

comfortable_boots.add(GameObjects(
    DisplayName=loca[f"{comfortable_boots.get_prefix()}_DisplayName"],
    Description=loca[f"{comfortable_boots.get_prefix()}_Description"],
    LevelName="",
    MapKey=comfortable_boots_game_objects_uuid,
    Name=comfortable_boots.get_prefix(),
    ParentTemplateId=arm_boots_leather_a,
    Stats=comfortable_boots.get_prefix(),
    Type="item",
))

comfortable_boots.add(Armor(
    comfortable_boots.get_prefix(),
    using="ARM_Camp_Shoes",
    RootTemplate=comfortable_boots_game_objects_uuid,
))

comfortable_boots.add(TreasureTable(f"""
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_{comfortable_boots.get_prefix()}",1,0,0,0,0,0,0,0
"""))

comfortable_boots.build()
