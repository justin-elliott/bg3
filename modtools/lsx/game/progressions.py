#!/usr/bin/env python3
"""
Progression definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class Subclass(LsxNode):
    _id_ = "SubClass"
    Object: str = LsxType.GUID


class Subclasses(LsxNode):
    _id_ = "SubClasses"
    children: LsxChildren = (Subclass,)


class Progression(LsxNode):
    AllowImprovement: bool = LsxType.BOOL
    Boosts: LsxChildren = LsxType.LSSTRING
    IsMulticlass: bool = LsxType.BOOL
    Level: int = LsxType.UINT8
    Name: str = LsxType.LSSTRING_VALUE
    PassivesAdded: LsxChildren = LsxType.LSSTRING
    PassivesRemoved: LsxChildren = LsxType.LSSTRING
    ProgressionType: int = LsxType.UINT8
    Selectors: LsxChildren = LsxType.LSSTRING
    TableUUID: str = LsxType.GUID
    UUID: str = LsxType.GUID
    children: LsxChildren = (Subclasses,)


class Progressions(LsxDocument):
    path = "Public/{folder}/Progressions/Progressions.lsx"
    children: LsxChildren = (Progression,)


Lsx.register(Progressions)
