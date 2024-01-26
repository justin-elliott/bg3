#!/usr/bin/env python3
"""
Spell list definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class SpellList(LsxNode):
    Comment: str = LsxType.LSSTRING_VALUE
    Spells: LsxChildren = LsxType.LSSTRING
    UUID: str = LsxType.GUID


class SpellLists(LsxDocument):
    path = "Public/{folder}/Lists/SpellLists.lsx"
    children: LsxChildren = (SpellList,)


Lsx.register(SpellLists)
