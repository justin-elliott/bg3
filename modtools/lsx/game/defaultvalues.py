#!/usr/bin/env python3
"""
LSX definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType
from typing import Final


class PassivesDefaultValue(LsxNode):
    _id_: Final[str] = "DefaultValue"

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


class SkillsDefaultValue(LsxNode):
    _id_: Final[str] = "DefaultValue"

    Add: list[str] = LsxType.LSSTRING
    Level: int = LsxType.INT32
    SelectorId: str = LsxType.LSSTRING_VALUE
    TableUUID: str = LsxType.GUID
    UUID: str = LsxType.GUID

    def __init__(self,
                 *,
                 Add: list[str] = None,
                 Level: int = None,
                 SelectorId: str = None,
                 TableUUID: str = None,
                 UUID: str = None):
        super().__init__(
            Add=Add,
            Level=Level,
            SelectorId=SelectorId,
            TableUUID=TableUUID,
            UUID=UUID,
        )


class PassivesDefaultValues(LsxDocument):
    region: str = "DefaultValues"
    path: str = "Public/{folder}/DefaultValues/Passives.lsx"
    children: LsxChildren = (PassivesDefaultValue,)


class SkillsDefaultValues(LsxDocument):
    region: str = "DefaultValues"
    path: str = "Public/{folder}/DefaultValues/Skills.lsx"
    children: LsxChildren = (SkillsDefaultValue,)


Lsx.register(PassivesDefaultValues)
Lsx.register(SkillsDefaultValues)
