#!/usr/bin/env python3
"""
Generates files for the "OrphicOutfits" mod.
"""

import os

from moddb.boosts import Boosts
from modtools.gamedata import armor_data, passive_data
from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",


def ability_increase(level) -> int:
    """Return the ability increase for a given level."""
    return int((level + 5) / 6) * 2


orphic_outfits = Mod(os.path.dirname(__file__),
                     author="justin-elliott",
                     name="OrphicOutfits",
                     mod_uuid=UUID("143ff0cb-eccb-4775-91c4-68af77030bbc"),
                     description="Adds a selction of outfits to the tutorial chest.")

loca = orphic_outfits.get_localization()
loca.add_language("en", "English")

boosts = Boosts(orphic_outfits)

loca["OrphicOutfits_Camp_TrespassersTreads_DisplayName"] = {"en": "Trespasser's Treads"}
loca["OrphicOutfits_Camp_TrespassersTreads_Description"] = {"en": """
    The perfect boots to be wearing when you're someplace that you're not welcome.
    """}

boots_of_aid_and_comfort_uuid = UUID("bc090f4e-ff74-49f6-a3f2-7eb561f57436")
comfortable_boots_game_objects_uuid = UUID("09228143-3367-435d-acbb-a65a8e5255b1")

orphic_outfits.add_root_templates([
    Lsx.Node("GameObjects", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["OrphicOutfits_Camp_TrespassersTreads_DisplayName"], version=1),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["OrphicOutfits_Camp_TrespassersTreads_Description"], version=1),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(comfortable_boots_game_objects_uuid)),
        Lsx.Attribute("Name", "LSString", value="OrphicOutfits_Camp_TrespassersTreads"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value=str(boots_of_aid_and_comfort_uuid)),
        Lsx.Attribute("Stats", "FixedString", value="OrphicOutfits_Camp_TrespassersTreads"),
        Lsx.Attribute("Type", "FixedString", value="item"),
    ]),
])

orphic_outfits.add(armor_data(
    "OrphicOutfits_Camp_BlackFlareLeatherOutfit",
    using="ARM_Vanity_Body_Leather_Black",
    Rarity="Legendary",
    PassivesOnEquip=["OrphicOutfits_SeductiveGrace"],
))

orphic_outfits.add(armor_data(
    "OrphicOutfits_Camp_TrespassersTreads",
    using="ARM_Camp_Shoes",
    RootTemplate=str(comfortable_boots_game_objects_uuid),
    ValueLevel="3",
    ObjectCategory="ShoesCommon",
    MinAmount="1",
    MaxAmount="1",
    Priority="0",
    Rarity="Legendary",
    PassivesOnEquip=["OrphicOutfits_Transgressor"],
))

orphic_outfits.add(armor_data(
    "OrphicOutfits_Underwear_HalfOrc",
    using="ARM_Underwear_HalfOrcs",
    Rarity="Legendary",
    PassivesOnEquip=["OrphicOutfits_Dependable"],
))

orphic_outfits.add(armor_data(
    "OrphicOutfits_Underwear_Incubus",
    using="ARM_Underwear_Incubus",
    Rarity="Legendary",
    PassivesOnEquip=["OrphicOutfits_Dependable"],
))

orphic_outfits.add(armor_data(
    "OrphicOutfits_Underwear_Tiefling",
    using="ARM_Underwear_Tieflings",
    Rarity="Legendary",
    PassivesOnEquip=["OrphicOutfits_Dependable"],
))

loca["OrphicOutfits_SeductiveGrace_DisplayName"] = {"en": "Seductive Grace"}
loca["OrphicOutfits_SeductiveGrace_Description"] = {"en": """
    Increases your <LSTag Tooltip="Charisma">Charisma</LSTag> and <LSTag Tooltip="Dexterity">Dexterity</LSTag> by [1].
    """}

orphic_outfits.add(passive_data(
    "OrphicOutfits_SeductiveGrace",
    DisplayName=loca["OrphicOutfits_SeductiveGrace_DisplayName"],
    Description=loca["OrphicOutfits_SeductiveGrace_Description"],
    DescriptionParams=["LevelMapValue(OrphicOutfits_AbilityValue)"],
    Boosts=[
        *boosts.by_level(lambda level: f"Ability(Charisma,{ability_increase(level)},30)"),
        *boosts.by_level(lambda level: f"Ability(Dexterity,{ability_increase(level)},30)"),
    ],
))

loca["OrphicOutfits_Transgressor_DisplayName"] = {"en": "Transgressor"}
loca["OrphicOutfits_Transgressor_Description"] = {"en": """
    You have <LSTag Tooltip="Advantage">Advantage</LSTag> on <LSTag Tooltip="SleightOfHand">Sleight of Hand</LSTag> and
    <LSTag Tooltip="Stealth">Stealth</LSTag> <LSTag Tooltip="AbilityCheck">Checks</LSTag>.
    """}

orphic_outfits.add(passive_data(
    "OrphicOutfits_Transgressor",
    DisplayName=loca["OrphicOutfits_Transgressor_DisplayName"],
    Description=loca["OrphicOutfits_Transgressor_Description"],
    Boosts=["Advantage(Skill,SleightOfHand)", "Advantage(Skill,Stealth)"],
))

loca["OrphicOutfits_Dependable_DisplayName"] = {"en": "Dependable"}
loca["OrphicOutfits_Dependable_Description"] = {"en": """
    Increases your <LSTag Tooltip="Constitution">Constitution</LSTag> by [1], and you gain
    <LSTag Tooltip="Advantage">Advantage</LSTag> on <LSTag Tooltip="Concentration">Concentration</LSTag>
    <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>.
    """}

orphic_outfits.add(passive_data(
    "OrphicOutfits_Dependable",
    DisplayName=loca["OrphicOutfits_Dependable_DisplayName"],
    Description=loca["OrphicOutfits_Dependable_Description"],
    DescriptionParams=["LevelMapValue(OrphicOutfits_AbilityValue)"],
    Boosts=[
        *boosts.by_level(lambda level: f"Ability(Constitution,{ability_increase(level)},30)"),
        "Advantage(Concentration)",
    ],
))

orphic_outfits.add_level_maps([
    Lsx.Node("LevelMapSeries", [
        *[Lsx.Attribute(f"Level{level}", "LSString", value=f"{ability_increase(level)}")
            for level in range(1, 13)],
        *[Lsx.Attribute(f"Level{level}", "LSString", value=f"{ability_increase(12)}")
            for level in range(13, 21)],
        Lsx.Attribute("Name", "FixedString", value="OrphicOutfits_AbilityValue"),
        Lsx.Attribute("UUID", "guid", value="bfc5329e-9fec-4fec-834f-e25baa6bd350"),
    ]),
])

orphic_outfits.add_treasure_table("""\
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_OrphicOutfits_Camp_BlackFlareLeatherOutfit",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_OrphicOutfits_Camp_TrespassersTreads",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_OrphicOutfits_Underwear_HalfOrc",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_OrphicOutfits_Underwear_Incubus",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_OrphicOutfits_Underwear_Tiefling",1,0,0,0,0,0,0,0
""")

orphic_outfits.build()
