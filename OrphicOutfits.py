#!/usr/bin/env python3
"""
Generates files for the "OrphicOutfits" mod.
"""

import os

from modtools.gamedata import armor_data, passive_data
from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",

orphic_outfits = Mod(os.path.dirname(__file__),
                     author="justin-elliott",
                     name="OrphicOutfits",
                     mod_uuid=UUID("143ff0cb-eccb-4775-91c4-68af77030bbc"),
                     description="Adds a selction of outfits to the tutorial chest.")

loca = orphic_outfits.get_localization()
loca.add_language("en", "English")

loca["OrphicOutfits_Camp_ComfortableBoots_DisplayName"] = {"en": "Comfortable Boots"}
loca["OrphicOutfits_Camp_ComfortableBoots_Description"] = {"en": """
    Made of soft, sheepskin-lined leather, these are the perfect boots to wear around the campfire on a chilly night.
    """}

boots_of_aid_and_comfort_uuid = UUID("bc090f4e-ff74-49f6-a3f2-7eb561f57436")
comfortable_boots_game_objects_uuid = UUID("09228143-3367-435d-acbb-a65a8e5255b1")

orphic_outfits.add_root_templates([
    Lsx.Node("GameObjects", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["OrphicOutfits_Camp_ComfortableBoots_DisplayName"], version=1),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["OrphicOutfits_Camp_ComfortableBoots_Description"], version=1),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(comfortable_boots_game_objects_uuid)),
        Lsx.Attribute("Name", "LSString", value="OrphicOutfits_Camp_ComfortableBoots"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value=str(boots_of_aid_and_comfort_uuid)),
        Lsx.Attribute("Stats", "FixedString", value="OrphicOutfits_Camp_ComfortableBoots"),
        Lsx.Attribute("Type", "FixedString", value="item"),
    ]),
])

orphic_outfits.add(armor_data(
    "OrphicOutfits_Camp_BlackFlareLeatherOutfit",
    using="ARM_Vanity_Body_Leather_Black",
))

orphic_outfits.add(armor_data(
    "OrphicOutfits_Camp_ComfortableBoots",
    using="ARM_Camp_Shoes",
    RootTemplate=str(comfortable_boots_game_objects_uuid),
    ValueLevel="3",
    ObjectCategory="ShoesCommon",
    MinAmount="1",
    MaxAmount="1",
    Priority="0",
    Rarity="Legendary",
    PassivesOnEquip=["OrphicOutfits_FleetOfFoot"],
))

orphic_outfits.add(armor_data(
    "OrphicOutfits_Underwear_HalfOrc",
    using="ARM_Underwear_HalfOrcs",
    Rarity="Legendary",
    PassivesOnEquip=["OrphicOutfits_LuckyUnderwear"],
))

orphic_outfits.add(armor_data(
    "OrphicOutfits_Underwear_Incubus",
    using="ARM_Underwear_Incubus",
    Rarity="Legendary",
    PassivesOnEquip=["OrphicOutfits_LuckyUnderwear"],
))

orphic_outfits.add(armor_data(
    "OrphicOutfits_Underwear_Tiefling",
    using="ARM_Underwear_Tieflings",
    Rarity="Legendary",
    PassivesOnEquip=["OrphicOutfits_LuckyUnderwear"],
))

loca["OrphicOutfits_FleetOfFoot_DisplayName"] = {"en": "Fleet of Foot"}
loca["OrphicOutfits_FleetOfFoot_Description"] = {"en": """
    <LSTag Tooltip="MovementSpeed">Movement speed</LSTag> increased by [1].
    """}

orphic_outfits.add(passive_data(
    "OrphicOutfits_FleetOfFoot",
    DisplayName=loca["OrphicOutfits_FleetOfFoot_DisplayName"],
    Description=loca["OrphicOutfits_FleetOfFoot_Description"],
    DescriptionParams=["Distance(1.5)"],
    Boosts=["ActionResource(Movement,1.5,0)"],
))

loca["OrphicOutfits_LuckyUnderwear_DisplayName"] = {"en": "Lucky Underwear"}
loca["OrphicOutfits_LuckyUnderwear_Description"] = {"en": """
    You don't know why, but you always seem to have good luck in this pair of underwear.
    """}

orphic_outfits.add(passive_data(
    "OrphicOutfits_LuckyUnderwear",
    DisplayName=loca["OrphicOutfits_LuckyUnderwear_DisplayName"],
    Description=loca["OrphicOutfits_LuckyUnderwear_Description"],
    Boosts=["RollBonus(SavingThrow,1)"],
))

orphic_outfits.add_treasure_table("""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_OrphicOutfits_Camp_BlackFlareLeatherOutfit",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_OrphicOutfits_Camp_ComfortableBoots",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_OrphicOutfits_Underwear_HalfOrc",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_OrphicOutfits_Underwear_Incubus",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_OrphicOutfits_Underwear_Tiefling",1,0,0,0,0,0,0,0
""")

orphic_outfits.build()
