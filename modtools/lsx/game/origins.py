#!/usr/bin/env python3
"""
Origins definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class Origin(LsxNode):
    class ReallyTags(LsxNode):
        Object: str = LsxType.GUID

    class AppearanceTags(LsxNode):
        Object: str = LsxType.GUID

    AppearanceLocked: bool = LsxType.BOOL
    AvailableInCharacterCreation: int = LsxType.UINT8
    BackgroundUUID: str = LsxType.GUID
    BodyShape: int = LsxType.UINT8
    BodyType: int = LsxType.UINT8
    ClassEquipmentOverride: str = LsxType.FIXEDSTRING
    ClassUUID: str = LsxType.GUID
    CloseUpA: str = LsxType.LSSTRING_VALUE
    CloseUpB: str = LsxType.LSSTRING_VALUE
    DefaultsTemplate: str = LsxType.GUID
    Description: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    DisplayName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    ExcludesOriginUUID: str = LsxType.GUID
    GlobalTemplate: str = LsxType.GUID
    GodUUID: str = LsxType.GUID
    IntroDialogUUID: str = LsxType.GUID
    LockBody: bool = LsxType.BOOL
    LockClass: bool = LsxType.BOOL
    LockRace: bool = LsxType.BOOL
    Name: str = LsxType.FIXEDSTRING
    Passives: list[str] = LsxType.LSSTRING
    RaceUUID: str = LsxType.GUID
    SubClassUUID: str = LsxType.GUID
    SubRaceUUID: str = LsxType.GUID
    UUID: str = LsxType.GUID
    Unique: bool = LsxType.BOOL
    VoiceTableUUID: str = LsxType.GUID
    children: LsxChildren = (ReallyTags, AppearanceTags)


class Origins(LsxDocument):
    path = "Public/{folder}/Origins/Origins.lsx"
    children: LsxChildren = (Origin,)


Lsx.register(Origins)
