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

    def __init__(self,
                 *,
                 FallbackValue: str = None,
                 Level1: str = None,
                 Level2: str = None,
                 Level3: str = None,
                 Level4: str = None,
                 Level5: str = None,
                 Level6: str = None,
                 Level7: str = None,
                 Level8: str = None,
                 Level9: str = None,
                 Level10: str = None,
                 Level11: str = None,
                 Level12: str = None,
                 Level13: str = None,
                 Level14: str = None,
                 Level15: str = None,
                 Level16: str = None,
                 Level17: str = None,
                 Level18: str = None,
                 Level19: str = None,
                 Level20: str = None,
                 Name: str = None,
                 PreferredClassUUID: str = None,
                 UUID: str = None):
        super().__init__(
            FallbackValue=FallbackValue,
            Level1=Level1,
            Level2=Level2,
            Level3=Level3,
            Level4=Level4,
            Level5=Level5,
            Level6=Level6,
            Level7=Level7,
            Level8=Level8,
            Level9=Level9,
            Level10=Level10,
            Level11=Level11,
            Level12=Level12,
            Level13=Level13,
            Level14=Level14,
            Level15=Level15,
            Level16=Level16,
            Level17=Level17,
            Level18=Level18,
            Level19=Level19,
            Level20=Level20,
            Name=Name,
            PreferredClassUUID=PreferredClassUUID,
            UUID=UUID,
        )


class LevelMapValues(LsxDocument):
    path = "Public/{folder}/Levelmaps/LevelMapValues.lsx"
    children: LsxChildren = (LevelMapSeries,)


Lsx.register(LevelMapValues)
