#!/usr/bin/env python3
"""
Progression Descriptions definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class ProgressionDescription(LsxNode):
    Description: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    DisplayName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    ExactMatch: str = LsxType.FIXEDSTRING
    Hidden: bool = LsxType.BOOL
    ParamMatch: str = LsxType.FIXEDSTRING
    PassivePrototype: str = LsxType.FIXEDSTRING
    ProgressionId: str = LsxType.GUID
    ProgressionTableId: str = LsxType.GUID
    SelectorId: str = LsxType.FIXEDSTRING
    Type: str = LsxType.FIXEDSTRING
    UUID: str = LsxType.GUID

    def __init__(self,
                 *,
                 Description: tuple[str, int] | str = None,
                 DisplayName: tuple[str, int] | str = None,
                 ExactMatch: str = None,
                 Hidden: bool = None,
                 ParamMatch: str = None,
                 PassivePrototype: str = None,
                 ProgressionId: str = None,
                 ProgressionTableId: str = None,
                 SelectorId: str = None,
                 Type: str = None,
                 UUID: str = None):
        super().__init__(
            Description=Description,
            DisplayName=DisplayName,
            ExactMatch=ExactMatch,
            Hidden=Hidden,
            ParamMatch=ParamMatch,
            PassivePrototype=PassivePrototype,
            ProgressionId=ProgressionId,
            ProgressionTableId=ProgressionTableId,
            SelectorId=SelectorId,
            Type=Type,
            UUID=UUID,
        )


class ProgressionDescriptions(LsxDocument):
    path = "Public/{folder}/Progressions/ProgressionDescriptions.lsx"
    children: LsxChildren = (ProgressionDescription,)


Lsx.register(ProgressionDescriptions)
