#!/usr/bin/env python3
"""
Feat Descriptions definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class FeatDescription(LsxNode):
    Description: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    DisplayName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    ExactMatch: str = LsxType.FIXEDSTRING
    FeatId: str = LsxType.GUID
    UUID: str = LsxType.GUID

    def __init__(self,
                 *,
                 Description: tuple[str, int] | str = None,
                 DisplayName: tuple[str, int] | str = None,
                 ExactMatch: str = None,
                 FeatId: str = None,
                 UUID: str = None):
        super().__init__(
            Description=Description,
            DisplayName=DisplayName,
            ExactMatch=ExactMatch,
            FeatId=FeatId,
            UUID=UUID,
        )


class FeatDescriptions(LsxDocument):
    path = "Public/{folder}/Feats/FeatDescriptions.lsx"
    children: LsxChildren = (FeatDescription,)


Lsx.register(FeatDescriptions)
