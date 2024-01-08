#!/usr/bin/env python3
"""
Generates files for the "PaladinLearnFromScrolls" mod.
"""

import os

from collections.abc import Callable
from modtools.gamedata import passive_data, spell_data, status_data, weapon_data
from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",


paladin_scrolls = Mod(os.path.dirname(__file__),
                      author="justin-elliott",
                      name="PaladinLearnFromScrolls",
                      mod_uuid=UUID("af82740a-9a71-4b23-b0a8-2fc84eb8845a"),
                      description="Allows Paladins to learn from scrolls.")

paladin_scrolls.add_class_descriptions([
    Lsx.Node("ClassDescription", [
        Lsx.Attribute("BaseHp", "int32", value="10"),
        Lsx.Attribute("CanLearnSpells", "bool", value="true"),
        Lsx.Attribute("CharacterCreationPose", "guid", value="0f07ec6e-4ef0-434e-9a51-1353260ccff8"),
        Lsx.Attribute("Description", "TranslatedString", handle="h9fca63d9gfc1fg48c3g8ae9g01bbddae1ec3", version="1"),
        Lsx.Attribute("DisplayName", "TranslatedString", handle="h3ddc9a75ge59cg466eg8243gcde4e8d4f95d", version="1"),
        Lsx.Attribute("HasGod", "bool", value="false"),
        Lsx.Attribute("HpPerLevel", "int32", value="6"),
        Lsx.Attribute("LearningStrategy", "uint8", value="1"),
        Lsx.Attribute("MulticlassSpellcasterModifier", "double", value="0.5"),
        Lsx.Attribute("MustPrepareSpells", "bool", value="true"),
        Lsx.Attribute("Name", "FixedString", value="Paladin"),
        Lsx.Attribute("PrimaryAbility", "uint8", value="1"),
        Lsx.Attribute("ProgressionTableUUID", "guid", value="ba2afe85-acba-4ea1-a238-2b4543f47821"),
        Lsx.Attribute("SoundClassType", "FixedString", value="Paladin"),
        Lsx.Attribute("SpellCastingAbility", "uint8", value="6"),
        Lsx.Attribute("SpellList", "guid", value="4ed41a6d-19fd-4ca8-940a-072314b71e43"),
        Lsx.Attribute("UUID", "guid", value="ff4d9497-023c-434a-bd14-82fc367e991c"),
    ], children=[
        Lsx.Node("Tags", [
            Lsx.Attribute("Object", "guid", value="6d85ab2d-5c23-498c-a61e-98f05a00177a"),
        ]),
    ]),
])

paladin_scrolls.build()
