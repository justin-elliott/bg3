#!/usr/bin/env python3
"""
Progression definitions.
"""

from modtools.lsx_v3.node import LsxNode
from modtools.lsx_v3.type import LsxType


class SubClass(LsxNode):
    Object = LsxType.GUID


class SubClasses(LsxNode):
    children = (SubClass,)


class Progression(LsxNode):
    AllowImprovement = LsxType.BOOL
    Boosts = LsxType.LSSTRING
    IsMulticlass = LsxType.BOOL
    Level = LsxType.UINT8
    Name = LsxType.LSSTRING_VALUE
    PassivesAdded = LsxType.LSSTRING
    PassivesRemoved = LsxType.LSSTRING
    ProgressionType = LsxType.UINT8
    Selectors = LsxType.LSSTRING
    TableUUID = LsxType.GUID
    UUID = LsxType.GUID
    children = (SubClasses,)
