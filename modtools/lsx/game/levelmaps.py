#!/usr/bin/env python3
"""
Level map definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class LevelMapSeries(LsxNode):
    FallbackValue: str = LsxType.LSSTRING_VALUE
    Level1: str = LsxType.LSSTRING_VALUE
    Level2: str = LsxType.LSSTRING_VALUE
    Level3: str = LsxType.LSSTRING_VALUE
    Level4: str = LsxType.LSSTRING_VALUE
    Level5: str = LsxType.LSSTRING_VALUE
    Level6: str = LsxType.LSSTRING_VALUE
    Level7: str = LsxType.LSSTRING_VALUE
    Level8: str = LsxType.LSSTRING_VALUE
    Level9: str = LsxType.LSSTRING_VALUE
    Level10: str = LsxType.LSSTRING_VALUE
    Level11: str = LsxType.LSSTRING_VALUE
    Level12: str = LsxType.LSSTRING_VALUE
    Level13: str = LsxType.LSSTRING_VALUE
    Level14: str = LsxType.LSSTRING_VALUE
    Level15: str = LsxType.LSSTRING_VALUE
    Level16: str = LsxType.LSSTRING_VALUE
    Level17: str = LsxType.LSSTRING_VALUE
    Level18: str = LsxType.LSSTRING_VALUE
    Level19: str = LsxType.LSSTRING_VALUE
    Level20: str = LsxType.LSSTRING_VALUE
    Name: str = LsxType.FIXEDSTRING
    PreferredClassUUID: str = LsxType.GUID
    UUID: str = LsxType.GUID


class LevelMapValues(LsxDocument):
    path = "Public/{folder}/Levelmaps/LevelMapValues.lsx"
    children: LsxChildren = (LevelMapSeries,)


Lsx.register(LevelMapValues)
