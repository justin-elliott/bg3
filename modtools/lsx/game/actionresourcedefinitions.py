#!/usr/bin/env python3
"""
LSX definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class ActionResourceDefinition(LsxNode):
    Description: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    DiceType: int = LsxType.UINT32
    DisplayName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    Error: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    IsHidden: bool = LsxType.BOOL
    IsSpellResource: bool = LsxType.BOOL
    MaxLevel: int = LsxType.UINT32
    MaxValue: int = LsxType.UINT32
    Name: str = LsxType.FIXEDSTRING
    PartyActionResource: bool = LsxType.BOOL
    ReplenishType: str = LsxType.FIXEDSTRING
    ShowOnActionResourcePanel: bool = LsxType.BOOL
    UUID: str = LsxType.GUID
    UpdatesSpellPowerLevel: bool = LsxType.BOOL

    def __init__(self,
                 *,
                 Description: tuple[str, int] | str = None,
                 DiceType: int = None,
                 DisplayName: tuple[str, int] | str = None,
                 Error: tuple[str, int] | str = None,
                 IsHidden: bool = None,
                 IsSpellResource: bool = None,
                 MaxLevel: int = None,
                 MaxValue: int = None,
                 Name: str = None,
                 PartyActionResource: bool = None,
                 ReplenishType: str = None,
                 ShowOnActionResourcePanel: bool = None,
                 UUID: str = None,
                 UpdatesSpellPowerLevel: bool = None):
        super().__init__(
            Description=Description,
            DiceType=DiceType,
            DisplayName=DisplayName,
            Error=Error,
            IsHidden=IsHidden,
            IsSpellResource=IsSpellResource,
            MaxLevel=MaxLevel,
            MaxValue=MaxValue,
            Name=Name,
            PartyActionResource=PartyActionResource,
            ReplenishType=ReplenishType,
            ShowOnActionResourcePanel=ShowOnActionResourcePanel,
            UUID=UUID,
            UpdatesSpellPowerLevel=UpdatesSpellPowerLevel,
        )


class ActionResourceDefinitions(LsxDocument):
    path = "Public/{folder}/ActionResourceDefinitions/ActionResourceDefinitions.lsx"
    children: LsxChildren = (ActionResourceDefinition,)


Lsx.register(ActionResourceDefinitions)
