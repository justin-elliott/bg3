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


def add_asi(asi: int) -> None:
    feat_uuid = rare_feats.make_uuid(f"feat_ASI_{asi}")
    feat_description_uuid = rare_feats.make_uuid(f"feat_description_ASI_{asi}")

    loca[f"RareFeats_ASI_{asi}_DisplayName"] = {"en": f"Ability Improvement (+{asi})"}
    loca[f"RareFeats_ASI_{asi}_Description"] = {"en": f"""
        You have {asi} points to spend across your abilities, to a maximum of 20.
        """}

    rare_feats.add_feat_descriptions([
        Lsx.Node("FeatDescription", [
            Lsx.Attribute("DisplayName", "TranslatedString", handle=loca[f"RareFeats_ASI_{asi}_DisplayName"], version="1"),
            Lsx.Attribute("Description", "TranslatedString", handle=loca[f"RareFeats_ASI_{asi}_Description"], version="1"),
            Lsx.Attribute("ExactMatch", "FixedString", value=f"RareFeats_ASI_{asi}"),
            Lsx.Attribute("FeatId", "guid", value=str(feat_uuid)),
            Lsx.Attribute("UUID", "guid", value=str(feat_description_uuid)),
        ]),
    ])

    rare_feats.add_feats([
        Lsx.Node("Feat", [
            Lsx.Attribute("CanBeTakenMultipleTimes", "bool", value="true"),
            Lsx.Attribute("Name", "FixedString", value=f"RareFeats_ASI_{asi}"),
            Lsx.Attribute("Selectors", "LSString", value=f"SelectAbilities(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,{asi},{asi},FeatASI)"),
            Lsx.Attribute("UUID", "guid", value=str(feat_uuid)),
        ]),
    ])


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

# Ability Score Improvement (ASI) feats
for asi in range(4, 14, 2):
    add_asi(asi)

rare_feats.build()
