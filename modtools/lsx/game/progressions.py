#!/usr/bin/env python3
"""
Progression definitions.
"""

from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx.lsx import Lsx
from modtools.lsx.type import LsxType


class Subclass(LsxNode):
    id = "SubClass"
    Object = LsxType.GUID


class Subclasses(LsxNode):
    id = "SubClasses"
    children = (Subclass,)


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
    children = (Subclasses,)


class Progressions(LsxDocument):
    path = "Public/{folder}/Progressions/Progressions.lsx"
    children = (Progression,)


Lsx.register(Progressions)
