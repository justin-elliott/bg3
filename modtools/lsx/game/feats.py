#!/usr/bin/env python3
"""
Feats definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class Feat(LsxNode):
    CanBeTakenMultipleTimes: bool = LsxType.BOOL
    Name: str = LsxType.FIXEDSTRING
    PassivesAdded: LsxChildren = LsxType.LSSTRING
    Requirements: str = LsxType.LSSTRING_VALUE
    Selectors: LsxChildren = LsxType.LSSTRING
    UUID: str = LsxType.GUID


class Feats(LsxDocument):
    path = "Public/{folder}/Feats/Feats.lsx"
    children = (Feat,)


Lsx.register(Feats)
