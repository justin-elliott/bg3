#!/usr/bin/env python3
"""
Class Descriptions definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class ClassDescription(LsxNode):
    class Tags(LsxNode):
        Object: str = LsxType.GUID

        def __init__(self,
                     *,
                     Object: str = None):
            super().__init__(
                Object=Object,
            )

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
    children: LsxChildren = (Tags,)

    def __init__(self,
                 *,
                 BaseHp: int = None,
                 CanLearnSpells: bool = None,
                 CharacterCreationPose: str = None,
                 ClassEquipment: str = None,
                 ClassHotbarColumns: int = None,
                 CommonHotbarColumns: int = None,
                 Description: tuple[str, int] | str = None,
                 DisplayName: tuple[str, int] | str = None,
                 HasGod: bool = None,
                 HpPerLevel: int = None,
                 IsDefaultForUseSpellAction: bool = None,
                 IsSomaticWithInstrument: bool = None,
                 ItemsHotbarColumns: int = None,
                 LearningStrategy: int = None,
                 MulticlassSpellcasterModifier: float = None,
                 MustPrepareSpells: bool = None,
                 Name: str = None,
                 ParentGuid: str = None,
                 PrimaryAbility: int = None,
                 ProgressionTableUUID: str = None,
                 ShortName: tuple[str, int] | str = None,
                 SoundClassType: str = None,
                 SpellCastingAbility: int = None,
                 SpellList: str = None,
                 SubclassTitle: tuple[str, int] | str = None,
                 UUID: str = None,
                 children: LsxChildren = None):
        super().__init__(
            BaseHp=BaseHp,
            CanLearnSpells=CanLearnSpells,
            CharacterCreationPose=CharacterCreationPose,
            ClassEquipment=ClassEquipment,
            ClassHotbarColumns=ClassHotbarColumns,
            CommonHotbarColumns=CommonHotbarColumns,
            Description=Description,
            DisplayName=DisplayName,
            HasGod=HasGod,
            HpPerLevel=HpPerLevel,
            IsDefaultForUseSpellAction=IsDefaultForUseSpellAction,
            IsSomaticWithInstrument=IsSomaticWithInstrument,
            ItemsHotbarColumns=ItemsHotbarColumns,
            LearningStrategy=LearningStrategy,
            MulticlassSpellcasterModifier=MulticlassSpellcasterModifier,
            MustPrepareSpells=MustPrepareSpells,
            Name=Name,
            ParentGuid=ParentGuid,
            PrimaryAbility=PrimaryAbility,
            ProgressionTableUUID=ProgressionTableUUID,
            ShortName=ShortName,
            SoundClassType=SoundClassType,
            SpellCastingAbility=SpellCastingAbility,
            SpellList=SpellList,
            SubclassTitle=SubclassTitle,
            UUID=UUID,
            children=children,
        )


class ClassDescriptions(LsxDocument):
    path = "Public/{folder}/ClassDescriptions/ClassDescriptions.lsx"
    children: LsxChildren = (ClassDescription,)


Lsx.register(ClassDescriptions)
