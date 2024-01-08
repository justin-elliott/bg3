#!/usr/bin/env python3
"""
Generates files for the "SorcererLearnFromScrolls" mod.
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


sorcerer_scrolls = Mod(os.path.dirname(__file__),
                       author="justin-elliott",
                       name="SorcererLearnFromScrolls",
                       mod_uuid=UUID("d353c77e-7d6b-4a3d-b7fa-9a4529ec0313"),
                       description="Allows Sorcerers to learn from scrolls.")

sorcerer_scrolls.add_class_descriptions([
    Lsx.Node("ClassDescription", [
        Lsx.Attribute("BaseHp", "int32", value="6"),
        Lsx.Attribute("CanLearnSpells", "bool", value="true"),
        Lsx.Attribute("CharacterCreationPose", "guid", value="0f07ec6e-4ef0-434e-9a51-1353260ccff8"),
        Lsx.Attribute("ClassEquipment", "FixedString", value="EQP_CC_Sorcerer"),
        Lsx.Attribute("Description", "TranslatedString", handle="h23997f5eg91f5g499bgac88gda4f6f2dfcc9", version="2"),
        Lsx.Attribute("DisplayName", "TranslatedString", handle="h6eca29f5g747eg40c1gb3f0g6425335d294b", version="1"),
        Lsx.Attribute("HpPerLevel", "int32", value="4"),
        Lsx.Attribute("LearningStrategy", "uint8", value="1"),
        Lsx.Attribute("MulticlassSpellcasterModifier", "double", value="1"),
        Lsx.Attribute("MustPrepareSpells", "bool", value="true"),
        Lsx.Attribute("Name", "FixedString", value="Sorcerer"),
        Lsx.Attribute("PrimaryAbility", "uint8", value="6"),
        Lsx.Attribute("ProgressionTableUUID", "guid", value="e2416b02-953a-4ce8-aa8f-eb98d549d86d"),
        Lsx.Attribute("SoundClassType", "FixedString", value="Sorcerer"),
        Lsx.Attribute("SpellCastingAbility", "uint8", value="6"),
        Lsx.Attribute("SpellList", "guid", value="2ba5248a-f014-409d-ab26-b50116f7e477"),
        Lsx.Attribute("UUID", "guid", value="784001e2-c96d-4153-beb6-2adbef5abc92"),
    ], children=[
        Lsx.Node("Tags", [
            Lsx.Attribute("Object", "guid", value="18266c0b-efbc-4c80-8784-ada4a37218d7"),
        ]),
    ]),
])

sorcerer_scrolls.build()
