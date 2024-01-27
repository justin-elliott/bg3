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

    BaseHp: int = LsxType.INT32
    CanLearnSpells: bool = LsxType.BOOL
    CharacterCreationPose: str = LsxType.GUID
    ClassEquipment: str = LsxType.FIXEDSTRING
    ClassHotbarColumns: int = LsxType.INT32
    CommonHotbarColumns: int = LsxType.INT32
    Description: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    DisplayName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    HasGod: bool = LsxType.BOOL
    HpPerLevel: int = LsxType.INT32
    IsDefaultForUseSpellAction: bool = LsxType.BOOL
    IsSomaticWithInstrument: bool = LsxType.BOOL
    ItemsHotbarColumns: int = LsxType.INT32
    LearningStrategy: int = LsxType.UINT8
    MulticlassSpellcasterModifier: float = LsxType.DOUBLE
    MustPrepareSpells: bool = LsxType.BOOL
    Name: str = LsxType.FIXEDSTRING
    ParentGuid: str = LsxType.GUID
    PrimaryAbility: int = LsxType.UINT8
    ProgressionTableUUID: str = LsxType.GUID
    ShortName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    SoundClassType: str = LsxType.FIXEDSTRING
    SpellCastingAbility: int = LsxType.UINT8
    SpellList: str = LsxType.GUID
    SubclassTitle: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    UUID: str = LsxType.GUID
    children = (Tags,)


class ClassDescriptions(LsxDocument):
    path = "Public/{folder}/ClassDescriptions/ClassDescriptions.lsx"
    children = (ClassDescription,)


Lsx.register(ClassDescriptions)
