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

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (Subclass,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

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

    def __init__(self,
                 *,
                 AllowImprovement: bool = None,
                 Boosts: list[str] = None,
                 IsMulticlass: bool = None,
                 Level: int = None,
                 Name: str = None,
                 PassivesAdded: list[str] = None,
                 PassivesRemoved: list[str] = None,
                 ProgressionType: int = None,
                 Selectors: list[str] = None,
                 TableUUID: str = None,
                 UUID: str = None,
                 children: LsxChildren = None):
        super().__init__(
            AllowImprovement=AllowImprovement,
            Boosts=Boosts,
            IsMulticlass=IsMulticlass,
            Level=Level,
            Name=Name,
            PassivesAdded=PassivesAdded,
            PassivesRemoved=PassivesRemoved,
            ProgressionType=ProgressionType,
            Selectors=Selectors,
            TableUUID=TableUUID,
            UUID=UUID,
            children=children,
        )


class Progressions(LsxDocument):
    path = "Public/{folder}/Progressions/Progressions.lsx"
    children: LsxChildren = (Progression,)


Lsx.register(Progressions)
