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
    PassivesAdded: list[str] = LsxType.LSSTRING
    Requirements: str = LsxType.LSSTRING_VALUE
    Selectors: list[str] = LsxType.LSSTRING
    UUID: str = LsxType.GUID

    def __init__(self,
                 *,
                 CanBeTakenMultipleTimes: bool = None,
                 Name: str = None,
                 PassivesAdded: list[str] = None,
                 Requirements: str = None,
                 Selectors: list[str] = None,
                 UUID: str = None):
        super().__init__(
            CanBeTakenMultipleTimes=CanBeTakenMultipleTimes,
            Name=Name,
            PassivesAdded=PassivesAdded,
            Requirements=Requirements,
            Selectors=Selectors,
            UUID=UUID,
        )


class Feats(LsxDocument):
    path = "Public/{folder}/Feats/Feats.lsx"
    children: LsxChildren = (Feat,)


Lsx.register(Feats)
