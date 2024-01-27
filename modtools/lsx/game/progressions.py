#!/usr/bin/env python3
"""
Progressions definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class Progression(LsxNode):
    class Subclasses(LsxNode):
        _id_ = "SubClasses"

        class Subclass(LsxNode):
            _id_ = "SubClass"
            Object: str = LsxType.GUID

        children: LsxChildren = (Subclass,)

    AllowImprovement: bool = LsxType.BOOL
    Boosts: list[str] = LsxType.LSSTRING
    IsMulticlass: bool = LsxType.BOOL
    Level: int = LsxType.UINT8
    Name: str = LsxType.LSSTRING_VALUE
    PassivesAdded: list[str] = LsxType.LSSTRING
    PassivesRemoved: list[str] = LsxType.LSSTRING
    ProgressionType: int = LsxType.UINT8
    Selectors: list[str] = LsxType.LSSTRING
    TableUUID: str = LsxType.GUID
    UUID: str = LsxType.GUID
    children: LsxChildren = (Subclasses,)


class Progressions(LsxDocument):
    path = "Public/{folder}/Progressions/Progressions.lsx"
    children: LsxChildren = (Progression,)


Lsx.register(Progressions)
