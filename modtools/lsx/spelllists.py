#!/usr/bin/env python3
"""
Spell list definitions.
"""

from modtools.lsx.builders import LsxBuilder, NodeBuilder
from modtools.lsx.types import DataType, LsxCollection
from typing import Final


SpellList: Final = NodeBuilder("SpellList", {
    "Comment": DataType.LSSTRING_VALUE,
    "Spells": DataType.LSSTRING,
    "UUID": DataType.GUID,
})

SPELL_LISTS_LSX_PATH: Final = "Shared.pak/Public/Shared/Lists/SpellLists.lsx"
SPELL_LISTS_DEV_LSX_PATH: Final = "Shared.pak/Public/SharedDev/Lists/SpellLists.lsx"

SpellLists: Final = LsxBuilder("SpellLists", "root", SpellList, "Public/{0}/Lists/SpellLists.lsx")

LsxCollection.register(SpellList, SpellLists)
