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
    Name: str = LsxType.LSSTRING_VALUE
    Spells: list[str] = LsxType.LSSTRING
    UUID: str = LsxType.GUID

    def __init__(self,
                 *,
                 Name: str = None,
                 Spells: list[str] = None,
                 UUID: str = None):
        super().__init__(
            Name=Name,
            Spells=Spells,
            UUID=UUID,
        )


class SpellLists(LsxDocument):
    path = "Public/{folder}/Lists/SpellLists.lsx"
    children: LsxChildren = (SpellList,)


Lsx.register(SpellLists)
