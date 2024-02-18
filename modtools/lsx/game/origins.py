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

        def __init__(self,
                     *,
                     Object: str = None):
            super().__init__(
                Object=Object,
            )

    class AppearanceTags(LsxNode):
        Object: str = LsxType.GUID

        def __init__(self,
                     *,
                     Object: str = None):
            super().__init__(
                Object=Object,
            )

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

    def __init__(self,
                 *,
                 AppearanceLocked: bool = None,
                 AvailableInCharacterCreation: int = None,
                 BackgroundUUID: str = None,
                 BodyShape: int = None,
                 BodyType: int = None,
                 ClassEquipmentOverride: str = None,
                 ClassUUID: str = None,
                 CloseUpA: str = None,
                 CloseUpB: str = None,
                 DefaultsTemplate: str = None,
                 Description: tuple[str, int] | str = None,
                 DisplayName: tuple[str, int] | str = None,
                 ExcludesOriginUUID: str = None,
                 GlobalTemplate: str = None,
                 GodUUID: str = None,
                 IntroDialogUUID: str = None,
                 LockBody: bool = None,
                 LockClass: bool = None,
                 LockRace: bool = None,
                 Name: str = None,
                 Passives: list[str] = None,
                 RaceUUID: str = None,
                 SubClassUUID: str = None,
                 SubRaceUUID: str = None,
                 UUID: str = None,
                 Unique: bool = None,
                 VoiceTableUUID: str = None,
                 children: LsxChildren = None):
        super().__init__(
            AppearanceLocked=AppearanceLocked,
            AvailableInCharacterCreation=AvailableInCharacterCreation,
            BackgroundUUID=BackgroundUUID,
            BodyShape=BodyShape,
            BodyType=BodyType,
            ClassEquipmentOverride=ClassEquipmentOverride,
            ClassUUID=ClassUUID,
            CloseUpA=CloseUpA,
            CloseUpB=CloseUpB,
            DefaultsTemplate=DefaultsTemplate,
            Description=Description,
            DisplayName=DisplayName,
            ExcludesOriginUUID=ExcludesOriginUUID,
            GlobalTemplate=GlobalTemplate,
            GodUUID=GodUUID,
            IntroDialogUUID=IntroDialogUUID,
            LockBody=LockBody,
            LockClass=LockClass,
            LockRace=LockRace,
            Name=Name,
            Passives=Passives,
            RaceUUID=RaceUUID,
            SubClassUUID=SubClassUUID,
            SubRaceUUID=SubRaceUUID,
            UUID=UUID,
            Unique=Unique,
            VoiceTableUUID=VoiceTableUUID,
            children=children,
        )


class Origins(LsxDocument):
    path = "Public/{folder}/Origins/Origins.lsx"
    children: LsxChildren = (Origin,)


Lsx.register(Origins)
