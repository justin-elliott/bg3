#!/usr/bin/env python3
"""
Generates files for the "RareFeats" mod.
"""

import os

from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",

rare_feats = Mod(os.path.dirname(__file__),
                 author="justin-elliott",
                 name="RareFeats",
                 mod_uuid=UUID("1bfebf94-20b2-4105-bd4f-4caeb8a1fe2a"),
                 description="Adds additional feats.")

loca = rare_feats.get_localization()
loca.add_language("en", "English")

# A feat for when you don't wish to select a feat
no_feat_uuid = rare_feats.make_uuid("RareFeats_Feat_NoFeat")

loca["RareFeats_NoFeat_DisplayName"] = {"en": "No Feat"}
loca["RareFeats_NoFeat_Description"] = {"en": "Do not select a feat."}

rare_feats.add_feat_descriptions([
    Lsx.Node("FeatDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["RareFeats_NoFeat_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["RareFeats_NoFeat_Description"], version="1"),
        Lsx.Attribute("ExactMatch", "FixedString", value="RareFeats_NoFeat"),
        Lsx.Attribute("FeatId", "guid", value=str(no_feat_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(rare_feats.make_uuid("RareFeats_FeatDescription_NoFeat"))),
    ]),
])

rare_feats.add_feats([
    Lsx.Node("Feat", [
        Lsx.Attribute("CanBeTakenMultipleTimes", "bool", value="true"),
        Lsx.Attribute("Name", "FixedString", value="RareFeats_NoFeat"),
        Lsx.Attribute("UUID", "guid", value=str(no_feat_uuid)),
    ]),
])

# Attribute bonuses
attributes = [
    ("Strength",     "Spell_Transmutation_EnhanceAbility_BullsStrenght"),
    ("Dexterity",    "Spell_Transmutation_EnhanceAbility_CatsGrace"),
    ("Constitution", "Spell_Transmutation_EnhanceAbility_BearsEndurance"),
    ("Intelligence", "Spell_Transmutation_EnhanceAbility_FoxsCunning"),
    ("Wisdom",       "Spell_Transmutation_EnhanceAbility_OwlsWisdom"),
    ("Charisma",     "Spell_Transmutation_EnhanceAbility_EaglesSplendor"),
]

ability_improvement_feat_uuid = rare_feats.make_uuid("AbilityImprovementFeat")
ability_improvement_feat_description_uuid = rare_feats.make_uuid("AbilityImprovementFeatDescription")

loca["RareFeats_AbilityImprovement_DisplayName"] = {"en": "Ability Improvement"}
loca["RareFeats_AbilityImprovement_Description"] = {"en": """
    Add a bonus to each of your abilities, to a maximum of 30.
    """}

rare_feats.add_feat_descriptions([
    Lsx.Node("FeatDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["RareFeats_AbilityImprovement_DisplayName"], version="1"),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["RareFeats_AbilityImprovement_Description"], version="1"),
        Lsx.Attribute("ExactMatch", "FixedString", value="RareFeats_AbilityImprovement"),
        Lsx.Attribute("FeatId", "guid", value=str(ability_improvement_feat_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(ability_improvement_feat_description_uuid)),
    ]),
])

passive_selectors = Lsx.Attribute("Selectors", "LSString", value=[])
rare_feats.add_feats([
    Lsx.Node("Feat", [
        Lsx.Attribute("CanBeTakenMultipleTimes", "bool", value="true"),
        Lsx.Attribute("Name", "FixedString", value="RareFeats_AbilityImprovement"),
        passive_selectors,
        Lsx.Attribute("UUID", "guid", value=str(ability_improvement_feat_uuid)),
    ]),
])

loca["RareFeats_NoBonus_DisplayName"] = {"en": "No Bonus"}

for attribute, attribute_icon in attributes:
    loca[f"RareFeats_AbilityImprovement_{attribute}_DisplayName"] = {"en": attribute}
    loca[f"RareFeats_AbilityImprovement_{attribute}_Description"] = {"en": f"""
        Add a bonus to your <LSTag Tooltip="{attribute}">{attribute}</LSTag>.
        """}

    passive_list = Lsx.Attribute("Passives", "LSString", value=[], list_joiner=",")
    passive_list_uuid = str(rare_feats.make_uuid(f"AbilityImprovement_{attribute}"))
    rare_feats.add_passive_lists([
        Lsx.Node("PassiveList", [
            passive_list,
            Lsx.Attribute("UUID", "guid", value=passive_list_uuid)
        ]),
    ])
    passive_selectors.get_value().append(f"SelectPassives({passive_list_uuid},1,RareFeats_AbilityImprovement)")

    loca[f"RareFeats_{attribute}_NoBonus_Description"] = {"en": f"""
        No bonus to your <LSTag Tooltip="{attribute}">{attribute}</LSTag>.
        """}

    rare_feats.add_passive_data(
        f"RareFeats_{attribute}_0",
        DisplayName=loca["RareFeats_NoBonus_DisplayName"],
        Description=loca[f"RareFeats_{attribute}_NoBonus_Description"],
        Icon=attribute_icon,
        Properties=["IsHidden"],
    )
    passive_list.get_value().append(f"RareFeats_{attribute}_0")

    for bonus in range(2, 22, 2):
        loca[f"RareFeats_{attribute}_{bonus}_DisplayName"] = {"en": f"{attribute} +{bonus}"}
        loca[f"RareFeats_{attribute}_{bonus}_Description"] = {"en": f"""
            Increase your <LSTag Tooltip="{attribute}">{attribute}</LSTag> by {bonus}, to a maximum of 30.
            """}

        rare_feats.add_passive_data(
            f"RareFeats_{attribute}_{bonus}",
            DisplayName=loca[f"RareFeats_{attribute}_{bonus}_DisplayName"],
            Description=loca[f"RareFeats_{attribute}_{bonus}_Description"],
            Icon=attribute_icon,
            Boosts=[f"Ability({attribute},{bonus},30)"],
            Properties=["IsHidden"],
        )
        passive_list.get_value().append(f"RareFeats_{attribute}_{bonus}")

rare_feats.build()
