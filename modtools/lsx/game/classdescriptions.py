#!/usr/bin/env python3
"""
Class Descriptions definitions.
"""

from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class ClassDescription(LsxNode):
    class Tags(LsxNode):
        Object: str = LsxType.GUID

    CharacterCreationPose: str = LsxType.GUID
    ClassEquipment: str = LsxType.FIXEDSTRING
    Description: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    DisplayName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    LearningStrategy: int = LsxType.UINT8
    MustPrepareSpells: bool = LsxType.BOOL
    Name: str = LsxType.FIXEDSTRING
    ParentGuid: str = LsxType.GUID
    PrimaryAbility: int = LsxType.UINT8
    ProgressionTableUUID: str = LsxType.GUID
    ShortName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    SoundClassType: str = LsxType.FIXEDSTRING
    SpellCastingAbility: int = LsxType.UINT8
    SpellList: str = LsxType.GUID
    UUID: str = LsxType.GUID
    children = (Tags,)


class ClassDescriptions(LsxDocument):
    path = "Public/{folder}/ClassDescriptions/ClassDescriptions.lsx"
    children = (ClassDescription,)


Lsx.register(ClassDescriptions)
