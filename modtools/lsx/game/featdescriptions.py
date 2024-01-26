#!/usr/bin/env python3
"""
LSX definitions.
"""

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


class FeatDescriptions(LsxDocument):
    path = "Public/{folder}/Feats/FeatDescriptions.lsx"
    children = (FeatDescription,)


Lsx.register(FeatDescriptions)
