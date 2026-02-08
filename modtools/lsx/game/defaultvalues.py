#!/usr/bin/env python3
"""
LSX definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class DefaultValue(LsxNode):
    Add: list[str] = LsxType.LSSTRING
    Level: int = LsxType.INT32
    RaceUUID: str = LsxType.GUID
    SelectorId: str = LsxType.LSSTRING_VALUE
    TableUUID: str = LsxType.GUID
    UUID: str = LsxType.GUID

    def __init__(self,
                 *,
                 Add: list[str] = None,
                 Level: int = None,
                 RaceUUID: str = None,
                 SelectorId: str = None,
                 TableUUID: str = None,
                 UUID: str = None):
        super().__init__(
            Add=Add,
            Level=Level,
            RaceUUID=RaceUUID,
            SelectorId=SelectorId,
            TableUUID=TableUUID,
            UUID=UUID,
        )


class DefaultValues(LsxDocument):
    path = "Public/{folder}/DefaultValues/Passives.lsx"
    children: LsxChildren = (DefaultValue,)


Lsx.register(DefaultValues)
