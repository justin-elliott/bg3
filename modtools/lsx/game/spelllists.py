#!/usr/bin/env python3
"""
Spell list definitions.
"""

from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx.lsx import Lsx
from modtools.lsx.type import LsxType


class SpellList(LsxNode):
    Comment = LsxType.LSSTRING_VALUE
    Spells = LsxType.LSSTRING
    UUID = LsxType.GUID


class SpellLists(LsxDocument):
    path = "Public/{folder}/Lists/SpellLists.lsx"
    children = (SpellList,)


Lsx.register(SpellLists)
