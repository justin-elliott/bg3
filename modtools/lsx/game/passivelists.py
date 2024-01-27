#!/usr/bin/env python3
"""
Passive Lists definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class PassiveList(LsxNode):
    Passives: list[str] = LsxType.LSSTRING_COMMA
    UUID: str = LsxType.GUID


class PassiveLists(LsxDocument):
    path = "Public/{folder}/Lists/PassiveLists.lsx"
    children: LsxChildren = (PassiveList,)


Lsx.register(PassiveLists)
