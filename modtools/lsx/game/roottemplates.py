#!/usr/bin/env python3
"""
Root Template definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class GameObjects(LsxNode):
    class Bounds(LsxNode):
        class Bound(LsxNode):
            Height: float = LsxType.FLOAT
            IsIgnoringScale: bool = LsxType.BOOL
            Max: str = LsxType.FVEC3
            Min: str = LsxType.FVEC3
            Radius: float = LsxType.FLOAT
            Shape: int = LsxType.UINT8
            Type: int = LsxType.UINT8

            def __init__(self,
                         *,
                         Height: float = None,
                         IsIgnoringScale: bool = None,
                         Max: str = None,
                         Min: str = None,
                         Radius: float = None,
                         Shape: int = None,
                         Type: int = None):
                super().__init__(
                    Height=Height,
                    IsIgnoringScale=IsIgnoringScale,
                    Max=Max,
                    Min=Min,
                    Radius=Radius,
                    Shape=Shape,
                    Type=Type,
                )

        children: LsxChildren = (Bound,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class OnDestroyActions(LsxNode):
        class Action(LsxNode):
            class Attributes(LsxNode):
                ActivateSoundEvent: str = LsxType.FIXEDSTRING
                Animation: str = LsxType.FIXEDSTRING
                ApplyDeathTypeBloodCheck: bool = LsxType.BOOL
                CellAtGrow: int = LsxType.INT32
                Conditions: str = LsxType.LSSTRING_VALUE
                ExplodeFX: str = LsxType.FIXEDSTRING
                ExternalCauseAsSurfaceOwner: bool = LsxType.BOOL
                FadeOutDelay: float = LsxType.FLOAT
                FadeOutFX: str = LsxType.FIXEDSTRING
                GrowTimer: float = LsxType.FLOAT
                LifeTime: float = LsxType.FLOAT
                PlayOnHUD: bool = LsxType.BOOL
                Radius: float = LsxType.FLOAT
                SnapToGround: bool = LsxType.BOOL
                SurfaceType: str = LsxType.FIXEDSTRING
                TargetItemState: int = LsxType.UINT8
                Timeout: float = LsxType.FLOAT
                TotalCells: int = LsxType.INT32
                VisualWithDynamicPhysics: str = LsxType.FIXEDSTRING
                templateAfterDestruction: str = LsxType.FIXEDSTRING
                visualDestruction: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             ActivateSoundEvent: str = None,
                             Animation: str = None,
                             ApplyDeathTypeBloodCheck: bool = None,
                             CellAtGrow: int = None,
                             Conditions: str = None,
                             ExplodeFX: str = None,
                             ExternalCauseAsSurfaceOwner: bool = None,
                             FadeOutDelay: float = None,
                             FadeOutFX: str = None,
                             GrowTimer: float = None,
                             LifeTime: float = None,
                             PlayOnHUD: bool = None,
                             Radius: float = None,
                             SnapToGround: bool = None,
                             SurfaceType: str = None,
                             TargetItemState: int = None,
                             Timeout: float = None,
                             TotalCells: int = None,
                             VisualWithDynamicPhysics: str = None,
                             templateAfterDestruction: str = None,
                             visualDestruction: str = None):
                    super().__init__(
                        ActivateSoundEvent=ActivateSoundEvent,
                        Animation=Animation,
                        ApplyDeathTypeBloodCheck=ApplyDeathTypeBloodCheck,
                        CellAtGrow=CellAtGrow,
                        Conditions=Conditions,
                        ExplodeFX=ExplodeFX,
                        ExternalCauseAsSurfaceOwner=ExternalCauseAsSurfaceOwner,
                        FadeOutDelay=FadeOutDelay,
                        FadeOutFX=FadeOutFX,
                        GrowTimer=GrowTimer,
                        LifeTime=LifeTime,
                        PlayOnHUD=PlayOnHUD,
                        Radius=Radius,
                        SnapToGround=SnapToGround,
                        SurfaceType=SurfaceType,
                        TargetItemState=TargetItemState,
                        Timeout=Timeout,
                        TotalCells=TotalCells,
                        VisualWithDynamicPhysics=VisualWithDynamicPhysics,
                        templateAfterDestruction=templateAfterDestruction,
                        visualDestruction=visualDestruction,
                    )

            ActionType: int = LsxType.INT32
            children: LsxChildren = (Attributes,)

            def __init__(self,
                         *,
                         ActionType: int = None,
                         children: LsxChildren = None):
                super().__init__(
                    ActionType=ActionType,
                    children=children,
                )

        children: LsxChildren = (Action,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class PrefabChildrenGroup(LsxNode):
        class PrefabChildren(LsxNode):
            Object: str = LsxType.FIXEDSTRING

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (PrefabChildren,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class PrefabChildrenTransformGroup(LsxNode):
        class PrefabChildrenTransforms(LsxNode):
            Position: str = LsxType.FVEC3
            RotationQuat: str = LsxType.FVEC4
            Scale: float = LsxType.FLOAT

            def __init__(self,
                         *,
                         Position: str = None,
                         RotationQuat: str = None,
                         Scale: float = None):
                super().__init__(
                    Position=Position,
                    RotationQuat=RotationQuat,
                    Scale=Scale,
                )

        children: LsxChildren = (PrefabChildrenTransforms,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class LocomotionParams(LsxNode):
        IsMovementEnabled: bool = LsxType.BOOL
        IsWorldClimbingEnabled: bool = LsxType.BOOL
        LadderBlendspace_Attach_Down: str = LsxType.FIXEDSTRING
        LadderBlendspace_Attach_Up: str = LsxType.FIXEDSTRING
        LadderBlendspace_Detach_Down: str = LsxType.FIXEDSTRING
        LadderBlendspace_Detach_Up: str = LsxType.FIXEDSTRING
        MaxDashDistance: float = LsxType.FLOAT
        MovementAcceleration: float = LsxType.FLOAT
        MovementSpeedDash: float = LsxType.FLOAT
        MovementSpeedRun: float = LsxType.FLOAT
        MovementSpeedSprint: float = LsxType.FLOAT
        MovementSpeedStroll: float = LsxType.FLOAT
        MovementSpeedWalk: float = LsxType.FLOAT
        MovementStepUpHeight: float = LsxType.FLOAT
        MovementTiltToRemap: str = LsxType.FIXEDSTRING
        ProbeSpineBOffset: float = LsxType.FLOAT
        SteeringSpeedCurveWithoutTransitions: str = LsxType.FIXEDSTRING
        SteeringSpeed_CastingCurve: str = LsxType.FIXEDSTRING
        SteeringSpeed_MovingCurve: str = LsxType.FIXEDSTRING
        UseStandAtDestination: bool = LsxType.BOOL
        WorldClimbingBlendspace_DownA: str = LsxType.FIXEDSTRING
        WorldClimbingBlendspace_DownB: str = LsxType.FIXEDSTRING
        WorldClimbingBlendspace_DownBHeight: float = LsxType.FLOAT
        WorldClimbingBlendspace_UpA: str = LsxType.FIXEDSTRING
        WorldClimbingBlendspace_UpB: str = LsxType.FIXEDSTRING
        WorldClimbingBlendspace_UpBHeight: float = LsxType.FLOAT
        WorldClimbingHeight: float = LsxType.FLOAT
        WorldClimbingRadius: float = LsxType.FLOAT
        WorldClimbingSpeed: float = LsxType.FLOAT

        def __init__(self,
                     *,
                     IsMovementEnabled: bool = None,
                     IsWorldClimbingEnabled: bool = None,
                     LadderBlendspace_Attach_Down: str = None,
                     LadderBlendspace_Attach_Up: str = None,
                     LadderBlendspace_Detach_Down: str = None,
                     LadderBlendspace_Detach_Up: str = None,
                     MaxDashDistance: float = None,
                     MovementAcceleration: float = None,
                     MovementSpeedDash: float = None,
                     MovementSpeedRun: float = None,
                     MovementSpeedSprint: float = None,
                     MovementSpeedStroll: float = None,
                     MovementSpeedWalk: float = None,
                     MovementStepUpHeight: float = None,
                     MovementTiltToRemap: str = None,
                     ProbeSpineBOffset: float = None,
                     SteeringSpeedCurveWithoutTransitions: str = None,
                     SteeringSpeed_CastingCurve: str = None,
                     SteeringSpeed_MovingCurve: str = None,
                     UseStandAtDestination: bool = None,
                     WorldClimbingBlendspace_DownA: str = None,
                     WorldClimbingBlendspace_DownB: str = None,
                     WorldClimbingBlendspace_DownBHeight: float = None,
                     WorldClimbingBlendspace_UpA: str = None,
                     WorldClimbingBlendspace_UpB: str = None,
                     WorldClimbingBlendspace_UpBHeight: float = None,
                     WorldClimbingHeight: float = None,
                     WorldClimbingRadius: float = None,
                     WorldClimbingSpeed: float = None):
            super().__init__(
                IsMovementEnabled=IsMovementEnabled,
                IsWorldClimbingEnabled=IsWorldClimbingEnabled,
                LadderBlendspace_Attach_Down=LadderBlendspace_Attach_Down,
                LadderBlendspace_Attach_Up=LadderBlendspace_Attach_Up,
                LadderBlendspace_Detach_Down=LadderBlendspace_Detach_Down,
                LadderBlendspace_Detach_Up=LadderBlendspace_Detach_Up,
                MaxDashDistance=MaxDashDistance,
                MovementAcceleration=MovementAcceleration,
                MovementSpeedDash=MovementSpeedDash,
                MovementSpeedRun=MovementSpeedRun,
                MovementSpeedSprint=MovementSpeedSprint,
                MovementSpeedStroll=MovementSpeedStroll,
                MovementSpeedWalk=MovementSpeedWalk,
                MovementStepUpHeight=MovementStepUpHeight,
                MovementTiltToRemap=MovementTiltToRemap,
                ProbeSpineBOffset=ProbeSpineBOffset,
                SteeringSpeedCurveWithoutTransitions=SteeringSpeedCurveWithoutTransitions,
                SteeringSpeed_CastingCurve=SteeringSpeed_CastingCurve,
                SteeringSpeed_MovingCurve=SteeringSpeed_MovingCurve,
                UseStandAtDestination=UseStandAtDestination,
                WorldClimbingBlendspace_DownA=WorldClimbingBlendspace_DownA,
                WorldClimbingBlendspace_DownB=WorldClimbingBlendspace_DownB,
                WorldClimbingBlendspace_DownBHeight=WorldClimbingBlendspace_DownBHeight,
                WorldClimbingBlendspace_UpA=WorldClimbingBlendspace_UpA,
                WorldClimbingBlendspace_UpB=WorldClimbingBlendspace_UpB,
                WorldClimbingBlendspace_UpBHeight=WorldClimbingBlendspace_UpBHeight,
                WorldClimbingHeight=WorldClimbingHeight,
                WorldClimbingRadius=WorldClimbingRadius,
                WorldClimbingSpeed=WorldClimbingSpeed,
            )

    class SkillList(LsxNode):
        class Skill(LsxNode):
            class SourceConditions(LsxNode):
                class Tags(LsxNode):
                    class Tag(LsxNode):
                        Object: str = LsxType.GUID

                        def __init__(self,
                                     *,
                                     Object: str = None):
                            super().__init__(
                                Object=Object,
                            )

                    children: LsxChildren = (Tag,)

                    def __init__(self,
                                 *,
                                 children: LsxChildren = None):
                        super().__init__(
                            children=children,
                        )

                MaximumHealthPercentage: int = LsxType.INT32
                MinimumHealthPercentage: int = LsxType.INT32
                children: LsxChildren = (Tags,)

                def __init__(self,
                             *,
                             MaximumHealthPercentage: int = None,
                             MinimumHealthPercentage: int = None,
                             children: LsxChildren = None):
                    super().__init__(
                        MaximumHealthPercentage=MaximumHealthPercentage,
                        MinimumHealthPercentage=MinimumHealthPercentage,
                        children=children,
                    )

            class TargetConditions(LsxNode):
                class Tags(LsxNode):
                    class Tag(LsxNode):
                        Object: str = LsxType.GUID

                        def __init__(self,
                                     *,
                                     Object: str = None):
                            super().__init__(
                                Object=Object,
                            )

                    children: LsxChildren = (Tag,)

                    def __init__(self,
                                 *,
                                 children: LsxChildren = None):
                        super().__init__(
                            children=children,
                        )

                MaximumHealthPercentage: int = LsxType.INT32
                MinimumHealthPercentage: int = LsxType.INT32
                children: LsxChildren = (Tags,)

                def __init__(self,
                             *,
                             MaximumHealthPercentage: int = None,
                             MinimumHealthPercentage: int = None,
                             children: LsxChildren = None):
                    super().__init__(
                        MaximumHealthPercentage=MaximumHealthPercentage,
                        MinimumHealthPercentage=MinimumHealthPercentage,
                        children=children,
                    )

            class OnlyInNPCLoadout(LsxNode):
                Object: str = LsxType.GUID

                def __init__(self,
                             *,
                             Object: str = None):
                    super().__init__(
                        Object=Object,
                    )

            class ExcludeInNPCLoadout(LsxNode):
                Object: str = LsxType.GUID

                def __init__(self,
                             *,
                             Object: str = None):
                    super().__init__(
                        Object=Object,
                    )

            AIFlags: int = LsxType.UINT16
            CasualExplorer: bool = LsxType.BOOL
            Classic: bool = LsxType.BOOL
            FallbackStartRound: int = LsxType.INT32
            HonorHardcore: bool = LsxType.BOOL
            LearningStrategy: int = LsxType.UINT8
            MinimumImpact: int = LsxType.INT32
            OnlyCastOnSelf: bool = LsxType.BOOL
            ScoreModifier: float = LsxType.FLOAT
            Skill: str = LsxType.FIXEDSTRING
            SpellCastingAbility: int = LsxType.UINT8
            StartRound: int = LsxType.INT32
            TacticianHardcore: bool = LsxType.BOOL
            children: LsxChildren = (
                SourceConditions,
                TargetConditions,
                OnlyInNPCLoadout,
                ExcludeInNPCLoadout,
            )

            def __init__(self,
                         *,
                         AIFlags: int = None,
                         CasualExplorer: bool = None,
                         Classic: bool = None,
                         FallbackStartRound: int = None,
                         HonorHardcore: bool = None,
                         LearningStrategy: int = None,
                         MinimumImpact: int = None,
                         OnlyCastOnSelf: bool = None,
                         ScoreModifier: float = None,
                         Skill: str = None,
                         SpellCastingAbility: int = None,
                         StartRound: int = None,
                         TacticianHardcore: bool = None,
                         children: LsxChildren = None):
                super().__init__(
                    AIFlags=AIFlags,
                    CasualExplorer=CasualExplorer,
                    Classic=Classic,
                    FallbackStartRound=FallbackStartRound,
                    HonorHardcore=HonorHardcore,
                    LearningStrategy=LearningStrategy,
                    MinimumImpact=MinimumImpact,
                    OnlyCastOnSelf=OnlyCastOnSelf,
                    ScoreModifier=ScoreModifier,
                    Skill=Skill,
                    SpellCastingAbility=SpellCastingAbility,
                    StartRound=StartRound,
                    TacticianHardcore=TacticianHardcore,
                    children=children,
                )

        children: LsxChildren = (Skill,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class StatusList(LsxNode):
        class Status(LsxNode):
            Object: str = LsxType.FIXEDSTRING

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (Status,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class Tags(LsxNode):
        class Tag(LsxNode):
            Object: str = LsxType.GUID

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (Tag,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class PickingPhysics(LsxNode):
        class PickingPhysicsTemplates(LsxNode):
            MapKey: str = LsxType.FIXEDSTRING
            MapValue: str = LsxType.FIXEDSTRING

            def __init__(self,
                         *,
                         MapKey: str = None,
                         MapValue: str = None):
                super().__init__(
                    MapKey=MapKey,
                    MapValue=MapValue,
                )

        children: LsxChildren = (PickingPhysicsTemplates,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class OnUsePeaceActions(LsxNode):
        class Action(LsxNode):
            class Attributes(LsxNode):
                AiUseInCombat: bool = LsxType.BOOL
                AllowScaling: bool = LsxType.BOOL
                Animation: str = LsxType.FIXEDSTRING
                BlockMapMarkerNavigation: bool = LsxType.BOOL
                BookId: str = LsxType.FIXEDSTRING
                BotomHorizontalOffset: float = LsxType.FLOAT
                BotomVerticalOffset: float = LsxType.FLOAT
                ClassId: str = LsxType.GUID
                ClimbDirection: int = LsxType.INT32
                CombineSlots: int = LsxType.INT8
                Conditions: str = LsxType.LSSTRING_VALUE
                Consume: bool = LsxType.BOOL
                EventID: str = LsxType.FIXEDSTRING
                FallbackPreviewRadius: float = LsxType.FLOAT
                Heal: float = LsxType.FLOAT
                InsertSlots: int = LsxType.INT8
                IsBase: bool = LsxType.BOOL
                IsHiddenStatus: bool = LsxType.BOOL
                NodeLadderOffest: float = LsxType.FLOAT
                RecipeID: str = LsxType.FIXEDSTRING
                SecretDoor: bool = LsxType.BOOL
                SkillID: str = LsxType.FIXEDSTRING
                SnapToGround: bool = LsxType.BOOL
                Source: str = LsxType.FIXEDSTRING
                SourceType: int = LsxType.INT32
                SpellId: str = LsxType.FIXEDSTRING
                StatsId: str = LsxType.FIXEDSTRING
                StatusDuration: int = LsxType.INT32
                Target: str = LsxType.FIXEDSTRING
                TopAttachNearOffset: float = LsxType.FLOAT
                TopDetachOffset: float = LsxType.FLOAT
                TopLineTolerance: float = LsxType.FLOAT
                TopMidOffset: float = LsxType.FLOAT
                TopMidToPlatformFixedLength: float = LsxType.FLOAT
                Type: int = LsxType.INT32
                Visibility: int = LsxType.INT32

                def __init__(self,
                             *,
                             AiUseInCombat: bool = None,
                             AllowScaling: bool = None,
                             Animation: str = None,
                             BlockMapMarkerNavigation: bool = None,
                             BookId: str = None,
                             BotomHorizontalOffset: float = None,
                             BotomVerticalOffset: float = None,
                             ClassId: str = None,
                             ClimbDirection: int = None,
                             CombineSlots: int = None,
                             Conditions: str = None,
                             Consume: bool = None,
                             EventID: str = None,
                             FallbackPreviewRadius: float = None,
                             Heal: float = None,
                             InsertSlots: int = None,
                             IsBase: bool = None,
                             IsHiddenStatus: bool = None,
                             NodeLadderOffest: float = None,
                             RecipeID: str = None,
                             SecretDoor: bool = None,
                             SkillID: str = None,
                             SnapToGround: bool = None,
                             Source: str = None,
                             SourceType: int = None,
                             SpellId: str = None,
                             StatsId: str = None,
                             StatusDuration: int = None,
                             Target: str = None,
                             TopAttachNearOffset: float = None,
                             TopDetachOffset: float = None,
                             TopLineTolerance: float = None,
                             TopMidOffset: float = None,
                             TopMidToPlatformFixedLength: float = None,
                             Type: int = None,
                             Visibility: int = None):
                    super().__init__(
                        AiUseInCombat=AiUseInCombat,
                        AllowScaling=AllowScaling,
                        Animation=Animation,
                        BlockMapMarkerNavigation=BlockMapMarkerNavigation,
                        BookId=BookId,
                        BotomHorizontalOffset=BotomHorizontalOffset,
                        BotomVerticalOffset=BotomVerticalOffset,
                        ClassId=ClassId,
                        ClimbDirection=ClimbDirection,
                        CombineSlots=CombineSlots,
                        Conditions=Conditions,
                        Consume=Consume,
                        EventID=EventID,
                        FallbackPreviewRadius=FallbackPreviewRadius,
                        Heal=Heal,
                        InsertSlots=InsertSlots,
                        IsBase=IsBase,
                        IsHiddenStatus=IsHiddenStatus,
                        NodeLadderOffest=NodeLadderOffest,
                        RecipeID=RecipeID,
                        SecretDoor=SecretDoor,
                        SkillID=SkillID,
                        SnapToGround=SnapToGround,
                        Source=Source,
                        SourceType=SourceType,
                        SpellId=SpellId,
                        StatsId=StatsId,
                        StatusDuration=StatusDuration,
                        Target=Target,
                        TopAttachNearOffset=TopAttachNearOffset,
                        TopDetachOffset=TopDetachOffset,
                        TopLineTolerance=TopLineTolerance,
                        TopMidOffset=TopMidOffset,
                        TopMidToPlatformFixedLength=TopMidToPlatformFixedLength,
                        Type=Type,
                        Visibility=Visibility,
                    )

            ActionType: int = LsxType.INT32
            children: LsxChildren = (Attributes,)

            def __init__(self,
                         *,
                         ActionType: int = None,
                         children: LsxChildren = None):
                super().__init__(
                    ActionType=ActionType,
                    children=children,
                )

        children: LsxChildren = (Action,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class ConstellationConfigGlobalParameters(LsxNode):
        class ConstellationConfigParameter(LsxNode):
            class Value(LsxNode):
                class Scalar(LsxNode):
                    class Scalar(LsxNode):
                        class String(LsxNode):
                            String: str = LsxType.LSSTRING_VALUE

                            def __init__(self,
                                         *,
                                         String: str = None):
                                super().__init__(
                                    String=String,
                                )

                        class double(LsxNode):
                            double: float = LsxType.DOUBLE

                            def __init__(self,
                                         *,
                                         double: float = None):
                                super().__init__(
                                    double=double,
                                )

                        children: LsxChildren = (String, double)

                        def __init__(self,
                                     *,
                                     children: LsxChildren = None):
                            super().__init__(
                                children=children,
                            )

                    children: LsxChildren = (Scalar,)

                    def __init__(self,
                                 *,
                                 children: LsxChildren = None):
                        super().__init__(
                            children=children,
                        )

                children: LsxChildren = (Scalar,)

                def __init__(self,
                             *,
                             children: LsxChildren = None):
                    super().__init__(
                        children=children,
                    )

            Name: str = LsxType.LSSTRING_VALUE
            children: LsxChildren = (Value,)

            def __init__(self,
                         *,
                         Name: str = None,
                         children: LsxChildren = None):
                super().__init__(
                    Name=Name,
                    children=children,
                )

        children: LsxChildren = (ConstellationConfigParameter,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class ExcludeInDifficulty(LsxNode):
        pass

    class InventoryList(LsxNode):
        class InventoryItem(LsxNode):
            Object: str = LsxType.FIXEDSTRING

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (InventoryItem,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class ItemList(LsxNode):
        class Item(LsxNode):
            class SourceConditions(LsxNode):
                class Tags(LsxNode):
                    pass

                MaximumHealthPercentage: int = LsxType.INT32
                MinimumHealthPercentage: int = LsxType.INT32
                children: LsxChildren = (Tags,)

                def __init__(self,
                             *,
                             MaximumHealthPercentage: int = None,
                             MinimumHealthPercentage: int = None,
                             children: LsxChildren = None):
                    super().__init__(
                        MaximumHealthPercentage=MaximumHealthPercentage,
                        MinimumHealthPercentage=MinimumHealthPercentage,
                        children=children,
                    )

            class TargetConditions(LsxNode):
                class Tags(LsxNode):
                    pass

                MaximumHealthPercentage: int = LsxType.INT32
                MinimumHealthPercentage: int = LsxType.INT32
                children: LsxChildren = (Tags,)

                def __init__(self,
                             *,
                             MaximumHealthPercentage: int = None,
                             MinimumHealthPercentage: int = None,
                             children: LsxChildren = None):
                    super().__init__(
                        MaximumHealthPercentage=MaximumHealthPercentage,
                        MinimumHealthPercentage=MinimumHealthPercentage,
                        children=children,
                    )

            class OnlyInNPCLoadout(LsxNode):
                Object: str = LsxType.GUID

                def __init__(self,
                             *,
                             Object: str = None):
                    super().__init__(
                        Object=Object,
                    )

            AIFlags: int = LsxType.UINT16
            Amount: int = LsxType.INT32
            CanBePickpocketed: bool = LsxType.BOOL
            CasualExplorer: bool = LsxType.BOOL
            Classic: bool = LsxType.BOOL
            FallbackStartRound: int = LsxType.INT32
            HonorHardcore: bool = LsxType.BOOL
            IsDroppedOnDeath: bool = LsxType.BOOL
            IsTradable: int = LsxType.UINT8
            IsTradeable: bool = LsxType.BOOL
            ItemName: str = LsxType.LSSTRING_VALUE
            LevelName: str = LsxType.LSSTRING_VALUE
            MinimumImpact: int = LsxType.INT32
            OnlyCastOnSelf: bool = LsxType.BOOL
            ScoreModifier: float = LsxType.FLOAT
            StartRound: int = LsxType.INT32
            TacticianHardcore: bool = LsxType.BOOL
            TemplateID: str = LsxType.FIXEDSTRING
            Type: int = LsxType.UINT8
            UUID: str = LsxType.FIXEDSTRING
            children: LsxChildren = (SourceConditions, TargetConditions, OnlyInNPCLoadout)

            def __init__(self,
                         *,
                         AIFlags: int = None,
                         Amount: int = None,
                         CanBePickpocketed: bool = None,
                         CasualExplorer: bool = None,
                         Classic: bool = None,
                         FallbackStartRound: int = None,
                         HonorHardcore: bool = None,
                         IsDroppedOnDeath: bool = None,
                         IsTradable: int = None,
                         IsTradeable: bool = None,
                         ItemName: str = None,
                         LevelName: str = None,
                         MinimumImpact: int = None,
                         OnlyCastOnSelf: bool = None,
                         ScoreModifier: float = None,
                         StartRound: int = None,
                         TacticianHardcore: bool = None,
                         TemplateID: str = None,
                         Type: int = None,
                         UUID: str = None,
                         children: LsxChildren = None):
                super().__init__(
                    AIFlags=AIFlags,
                    Amount=Amount,
                    CanBePickpocketed=CanBePickpocketed,
                    CasualExplorer=CasualExplorer,
                    Classic=Classic,
                    FallbackStartRound=FallbackStartRound,
                    HonorHardcore=HonorHardcore,
                    IsDroppedOnDeath=IsDroppedOnDeath,
                    IsTradable=IsTradable,
                    IsTradeable=IsTradeable,
                    ItemName=ItemName,
                    LevelName=LevelName,
                    MinimumImpact=MinimumImpact,
                    OnlyCastOnSelf=OnlyCastOnSelf,
                    ScoreModifier=ScoreModifier,
                    StartRound=StartRound,
                    TacticianHardcore=TacticianHardcore,
                    TemplateID=TemplateID,
                    Type=Type,
                    UUID=UUID,
                    children=children,
                )

        children: LsxChildren = (Item,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class OnlyInDifficulty(LsxNode):
        pass

    class ScriptConfigGlobalParameters(LsxNode):
        pass

    class ScriptOverrides(LsxNode):
        class ScriptOverrides(LsxNode):
            class Object(LsxNode):
                class ScriptOverrides(LsxNode):
                    class ScriptVariables(LsxNode):
                        class Object(LsxNode):
                            class ScriptVariables(LsxNode):
                                Value: str = LsxType.LSSTRING_VALUE

                                def __init__(self,
                                             *,
                                             Value: str = None):
                                    super().__init__(
                                        Value=Value,
                                    )

                            MapKey: str = LsxType.FIXEDSTRING
                            children: LsxChildren = (ScriptVariables,)

                            def __init__(self,
                                         *,
                                         MapKey: str = None,
                                         children: LsxChildren = None):
                                super().__init__(
                                    MapKey=MapKey,
                                    children=children,
                                )

                        children: LsxChildren = (Object,)

                        def __init__(self,
                                     *,
                                     children: LsxChildren = None):
                            super().__init__(
                                children=children,
                            )

                    children: LsxChildren = (ScriptVariables,)

                    def __init__(self,
                                 *,
                                 children: LsxChildren = None):
                        super().__init__(
                            children=children,
                        )

                MapKey: str = LsxType.FIXEDSTRING
                children: LsxChildren = (ScriptOverrides,)

                def __init__(self,
                             *,
                             MapKey: str = None,
                             children: LsxChildren = None):
                    super().__init__(
                        MapKey=MapKey,
                        children=children,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        children: LsxChildren = (ScriptOverrides,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class Scripts(LsxNode):
        class Script(LsxNode):
            class Parameters(LsxNode):
                class Parameter(LsxNode):
                    MapKey: str = LsxType.FIXEDSTRING
                    Type: int = LsxType.INT32
                    Value: list[str] = LsxType.LSSTRING

                    def __init__(self,
                                 *,
                                 MapKey: str = None,
                                 Type: int = None,
                                 Value: list[str] = None):
                        super().__init__(
                            MapKey=MapKey,
                            Type=Type,
                            Value=Value,
                        )

                children: LsxChildren = (Parameter,)

                def __init__(self,
                             *,
                             children: LsxChildren = None):
                    super().__init__(
                        children=children,
                    )

            UUID: str = LsxType.FIXEDSTRING
            children: LsxChildren = (Parameters,)

            def __init__(self,
                         *,
                         UUID: str = None,
                         children: LsxChildren = None):
                super().__init__(
                    UUID=UUID,
                    children=children,
                )

        children: LsxChildren = (Script,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class Equipment_(LsxNode):
        _id_ = "Equipment"

        class AfroLongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class AfroShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class CurlyLongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class CurlyShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class DreadLongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class DreadShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class LongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class ParentRace(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.GUID

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class ShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class Visuals(LsxNode):
            class Object(LsxNode):
                class MapValue(LsxNode):
                    Object: str = LsxType.FIXEDSTRING

                    def __init__(self,
                                 *,
                                 Object: str = None):
                        super().__init__(
                            Object=Object,
                        )

                MapKey: str = LsxType.GUID
                children: LsxChildren = (MapValue,)

                def __init__(self,
                             *,
                             MapKey: str = None,
                             children: LsxChildren = None):
                    super().__init__(
                        MapKey=MapKey,
                        children=children,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class WavyLongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class WavyShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

                def __init__(self,
                             *,
                             MapKey: str = None,
                             MapValue: str = None):
                    super().__init__(
                        MapKey=MapKey,
                        MapValue=MapValue,
                    )

            children: LsxChildren = (Object,)

            def __init__(self,
                         *,
                         children: LsxChildren = None):
                super().__init__(
                    children=children,
                )

        class Slot(LsxNode):
            Object: str = LsxType.FIXEDSTRING

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        class VisualSet(LsxNode):
            class MaterialOverrides(LsxNode):
                class MaterialPresets(LsxNode):
                    class Object(LsxNode):
                        ForcePresetValues: bool = LsxType.BOOL
                        GroupName: str = LsxType.FIXEDSTRING
                        MapKey: str = LsxType.FIXEDSTRING
                        MaterialPresetResource: str = LsxType.FIXEDSTRING

                        def __init__(self,
                                     *,
                                     ForcePresetValues: bool = None,
                                     GroupName: str = None,
                                     MapKey: str = None,
                                     MaterialPresetResource: str = None):
                            super().__init__(
                                ForcePresetValues=ForcePresetValues,
                                GroupName=GroupName,
                                MapKey=MapKey,
                                MaterialPresetResource=MaterialPresetResource,
                            )

                    children: LsxChildren = (Object,)

                    def __init__(self,
                                 *,
                                 children: LsxChildren = None):
                        super().__init__(
                            children=children,
                        )

                class Vector3Parameters(LsxNode):
                    Color: bool = LsxType.BOOL
                    Custom: bool = LsxType.BOOL
                    Enabled: bool = LsxType.BOOL
                    Parameter: str = LsxType.FIXEDSTRING
                    Value: str = LsxType.FVEC3

                    def __init__(self,
                                 *,
                                 Color: bool = None,
                                 Custom: bool = None,
                                 Enabled: bool = None,
                                 Parameter: str = None,
                                 Value: str = None):
                        super().__init__(
                            Color=Color,
                            Custom=Custom,
                            Enabled=Enabled,
                            Parameter=Parameter,
                            Value=Value,
                        )

                class ColorPreset(LsxNode):
                    ForcePresetValues: bool = LsxType.BOOL
                    GroupName: str = LsxType.FIXEDSTRING
                    MaterialPresetResource: str = LsxType.FIXEDSTRING

                    def __init__(self,
                                 *,
                                 ForcePresetValues: bool = None,
                                 GroupName: str = None,
                                 MaterialPresetResource: str = None):
                        super().__init__(
                            ForcePresetValues=ForcePresetValues,
                            GroupName=GroupName,
                            MaterialPresetResource=MaterialPresetResource,
                        )

                MaterialResource: str = LsxType.FIXEDSTRING
                children: LsxChildren = (MaterialPresets, Vector3Parameters, ColorPreset)

                def __init__(self,
                             *,
                             MaterialResource: str = None,
                             children: LsxChildren = None):
                    super().__init__(
                        MaterialResource=MaterialResource,
                        children=children,
                    )

            class RealMaterialOverrides(LsxNode):
                pass

            BodySetVisual: str = LsxType.FIXEDSTRING
            ShowEquipmentVisuals: bool = LsxType.BOOL
            children: LsxChildren = (MaterialOverrides, RealMaterialOverrides)

            def __init__(self,
                         *,
                         BodySetVisual: str = None,
                         ShowEquipmentVisuals: bool = None,
                         children: LsxChildren = None):
                super().__init__(
                    BodySetVisual=BodySetVisual,
                    ShowEquipmentVisuals=ShowEquipmentVisuals,
                    children=children,
                )

        EquipmentSlots: int = LsxType.UINT32
        children: LsxChildren = (
            AfroLongHair,
            AfroShortHair,
            CurlyLongHair,
            CurlyShortHair,
            DreadLongHair,
            DreadShortHair,
            LongHair,
            ParentRace,
            ShortHair,
            Visuals,
            WavyLongHair,
            WavyShortHair,
            Slot,
            VisualSet,
        )

        def __init__(self,
                     *,
                     EquipmentSlots: int = None,
                     children: LsxChildren = None):
            super().__init__(
                EquipmentSlots=EquipmentSlots,
                children=children,
            )

    class EquipmentTypes(LsxNode):
        class EquipmentType(LsxNode):
            _id_ = ""
            Object: str = LsxType.GUID

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (EquipmentType,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class FootStepInfos(LsxNode):
        class FootStepInfo(LsxNode):
            FootBoneName: str = LsxType.FIXEDSTRING
            FootHearingEffectName: str = LsxType.LSSTRING_VALUE
            FootPrintEffectName: str = LsxType.LSSTRING_VALUE
            FootScuffEventName: str = LsxType.FIXEDSTRING
            FootSlideEffectName: str = LsxType.LSSTRING_VALUE
            FootSmearEffectName: str = LsxType.LSSTRING_VALUE
            FootSoundEventName: str = LsxType.FIXEDSTRING
            Name: str = LsxType.LSSTRING_VALUE

            def __init__(self,
                         *,
                         FootBoneName: str = None,
                         FootHearingEffectName: str = None,
                         FootPrintEffectName: str = None,
                         FootScuffEventName: str = None,
                         FootSlideEffectName: str = None,
                         FootSmearEffectName: str = None,
                         FootSoundEventName: str = None,
                         Name: str = None):
                super().__init__(
                    FootBoneName=FootBoneName,
                    FootHearingEffectName=FootHearingEffectName,
                    FootPrintEffectName=FootPrintEffectName,
                    FootScuffEventName=FootScuffEventName,
                    FootSlideEffectName=FootSlideEffectName,
                    FootSmearEffectName=FootSmearEffectName,
                    FootSoundEventName=FootSoundEventName,
                    Name=Name,
                )

        children: LsxChildren = (FootStepInfo,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class OnDeathActions(LsxNode):
        class Action(LsxNode):
            class Attributes(LsxNode):
                ActivateSoundEvent: str = LsxType.FIXEDSTRING
                Animation: str = LsxType.FIXEDSTRING
                ApplyDeathTypeBloodCheck: bool = LsxType.BOOL
                CellAtGrow: int = LsxType.INT32
                Conditions: str = LsxType.LSSTRING_VALUE
                ExternalCauseAsSurfaceOwner: bool = LsxType.BOOL
                GrowTimer: float = LsxType.FLOAT
                LifeTime: float = LsxType.FLOAT
                PlayOnHUD: bool = LsxType.BOOL
                SurfaceType: str = LsxType.FIXEDSTRING
                Timeout: float = LsxType.FLOAT
                TotalCells: int = LsxType.INT32

                def __init__(self,
                             *,
                             ActivateSoundEvent: str = None,
                             Animation: str = None,
                             ApplyDeathTypeBloodCheck: bool = None,
                             CellAtGrow: int = None,
                             Conditions: str = None,
                             ExternalCauseAsSurfaceOwner: bool = None,
                             GrowTimer: float = None,
                             LifeTime: float = None,
                             PlayOnHUD: bool = None,
                             SurfaceType: str = None,
                             Timeout: float = None,
                             TotalCells: int = None):
                    super().__init__(
                        ActivateSoundEvent=ActivateSoundEvent,
                        Animation=Animation,
                        ApplyDeathTypeBloodCheck=ApplyDeathTypeBloodCheck,
                        CellAtGrow=CellAtGrow,
                        Conditions=Conditions,
                        ExternalCauseAsSurfaceOwner=ExternalCauseAsSurfaceOwner,
                        GrowTimer=GrowTimer,
                        LifeTime=LifeTime,
                        PlayOnHUD=PlayOnHUD,
                        SurfaceType=SurfaceType,
                        Timeout=Timeout,
                        TotalCells=TotalCells,
                    )

            ActionType: int = LsxType.INT32
            children: LsxChildren = (Attributes,)

            def __init__(self,
                         *,
                         ActionType: int = None,
                         children: LsxChildren = None):
                super().__init__(
                    ActionType=ActionType,
                    children=children,
                )

        children: LsxChildren = (Action,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class TradeTreasures(LsxNode):
        class TreasureItem(LsxNode):
            Object: str = LsxType.FIXEDSTRING

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (TreasureItem,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class Treasures(LsxNode):
        class TreasureItem(LsxNode):
            Object: str = LsxType.FIXEDSTRING

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (TreasureItem,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class ConstructionLines(LsxNode):
        class ConstructionLine(LsxNode):
            class ConstructionPoints(LsxNode):
                class ConstructionPoint(LsxNode):
                    ConstructionPointId: str = LsxType.GUID

                    def __init__(self,
                                 *,
                                 ConstructionPointId: str = None):
                        super().__init__(
                            ConstructionPointId=ConstructionPointId,
                        )

                children: LsxChildren = (ConstructionPoint,)

                def __init__(self,
                             *,
                             children: LsxChildren = None):
                    super().__init__(
                        children=children,
                    )

            class HelperEnd(LsxNode):
                ConstructionPointId: str = LsxType.GUID

                def __init__(self,
                             *,
                             ConstructionPointId: str = None):
                    super().__init__(
                        ConstructionPointId=ConstructionPointId,
                    )

            class HelperStart(LsxNode):
                ConstructionPointId: str = LsxType.GUID

                def __init__(self,
                             *,
                             ConstructionPointId: str = None):
                    super().__init__(
                        ConstructionPointId=ConstructionPointId,
                    )

            ConstructionLineGuid: str = LsxType.GUID
            children: LsxChildren = (ConstructionPoints, HelperEnd, HelperStart)

            def __init__(self,
                         *,
                         ConstructionLineGuid: str = None,
                         children: LsxChildren = None):
                super().__init__(
                    ConstructionLineGuid=ConstructionLineGuid,
                    children=children,
                )

        children: LsxChildren = (ConstructionLine,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class ConstructionPoints(LsxNode):
        class ConstructionPoint(LsxNode):
            class ConstructionPointNeighbours(LsxNode):
                class ConstructionPointNeighbour(LsxNode):
                    class ConstructionPointNeighbours(LsxNode):
                        class ConstructionPointNeighbour(LsxNode):
                            ConstructionPointId: str = LsxType.GUID

                            def __init__(self,
                                         *,
                                         ConstructionPointId: str = None):
                                super().__init__(
                                    ConstructionPointId=ConstructionPointId,
                                )

                        children: LsxChildren = (ConstructionPointNeighbour,)

                        def __init__(self,
                                     *,
                                     children: LsxChildren = None):
                            super().__init__(
                                children=children,
                            )

                    class ConstructionTileLists(LsxNode):
                        class ConstructionTileList(LsxNode):
                            class ConstructionPointLeftCornerTiles(LsxNode):
                                class ConstructionPointLeftCornerTile(LsxNode):
                                    TileId: str = LsxType.GUID

                                    def __init__(self,
                                                 *,
                                                 TileId: str = None):
                                        super().__init__(
                                            TileId=TileId,
                                        )

                                children: LsxChildren = (ConstructionPointLeftCornerTile,)

                                def __init__(self,
                                             *,
                                             children: LsxChildren = None):
                                    super().__init__(
                                        children=children,
                                    )

                            class ConstructionPointNeighbourTiles(LsxNode):
                                class ConstructionPointNeighbourTile(LsxNode):
                                    ConstructionPointTile1Id: str = LsxType.GUID

                                    def __init__(self,
                                                 *,
                                                 ConstructionPointTile1Id: str = None):
                                        super().__init__(
                                            ConstructionPointTile1Id=ConstructionPointTile1Id,
                                        )

                                children: LsxChildren = (ConstructionPointNeighbourTile,)

                                def __init__(self,
                                             *,
                                             children: LsxChildren = None):
                                    super().__init__(
                                        children=children,
                                    )

                            class ConstructionPointRightCornerTiles(LsxNode):
                                class ConstructionPointRightCornerTile(LsxNode):
                                    TileId: str = LsxType.GUID

                                    def __init__(self,
                                                 *,
                                                 TileId: str = None):
                                        super().__init__(
                                            TileId=TileId,
                                        )

                                children: LsxChildren = (ConstructionPointRightCornerTile,)

                                def __init__(self,
                                             *,
                                             children: LsxChildren = None):
                                    super().__init__(
                                        children=children,
                                    )

                            ConstructionNonOptimalTilesEnd: int = LsxType.INT32
                            ConstructionNonOptimalTilesStart: int = LsxType.INT32
                            Side: int = LsxType.INT32
                            children: LsxChildren = (
                                ConstructionPointLeftCornerTiles,
                                ConstructionPointNeighbourTiles,
                                ConstructionPointRightCornerTiles,
                            )

                            def __init__(self,
                                         *,
                                         ConstructionNonOptimalTilesEnd: int = None,
                                         ConstructionNonOptimalTilesStart: int = None,
                                         Side: int = None,
                                         children: LsxChildren = None):
                                super().__init__(
                                    ConstructionNonOptimalTilesEnd=ConstructionNonOptimalTilesEnd,
                                    ConstructionNonOptimalTilesStart=ConstructionNonOptimalTilesStart,
                                    Side=Side,
                                    children=children,
                                )

                        children: LsxChildren = (ConstructionTileList,)

                        def __init__(self,
                                     *,
                                     children: LsxChildren = None):
                            super().__init__(
                                children=children,
                            )

                    children: LsxChildren = (ConstructionPointNeighbours, ConstructionTileLists)

                    def __init__(self,
                                 *,
                                 children: LsxChildren = None):
                        super().__init__(
                            children=children,
                        )

                children: LsxChildren = (ConstructionPointNeighbour,)

                def __init__(self,
                             *,
                             children: LsxChildren = None):
                    super().__init__(
                        children=children,
                    )

            ConstructionPointId: str = LsxType.GUID
            ConstructionPointStop: bool = LsxType.BOOL
            children: LsxChildren = (ConstructionPointNeighbours,)

            def __init__(self,
                         *,
                         ConstructionPointId: str = None,
                         ConstructionPointStop: bool = None,
                         children: LsxChildren = None):
                super().__init__(
                    ConstructionPointId=ConstructionPointId,
                    ConstructionPointStop=ConstructionPointStop,
                    children=children,
                )

        children: LsxChildren = (ConstructionPoint,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class ConstructionSpline(LsxNode):
        class ConstructionPoint(LsxNode):
            class ConstructionBranches(LsxNode):
                class ConstructionBranch(LsxNode):
                    ConstructionPointId: str = LsxType.GUID

                    def __init__(self,
                                 *,
                                 ConstructionPointId: str = None):
                        super().__init__(
                            ConstructionPointId=ConstructionPointId,
                        )

                ConstructionBranchCount: int = LsxType.INT32
                children: LsxChildren = (ConstructionBranch,)

                def __init__(self,
                             *,
                             ConstructionBranchCount: int = None,
                             children: LsxChildren = None):
                    super().__init__(
                        ConstructionBranchCount=ConstructionBranchCount,
                        children=children,
                    )

            ConstructionHelperPoint: bool = LsxType.BOOL
            ConstructionPointId: str = LsxType.GUID
            ConstructionPointStretch: bool = LsxType.BOOL
            ConstructionPointTransform: str = LsxType.MAT4X4
            children: LsxChildren = (ConstructionBranches,)

            def __init__(self,
                         *,
                         ConstructionHelperPoint: bool = None,
                         ConstructionPointId: str = None,
                         ConstructionPointStretch: bool = None,
                         ConstructionPointTransform: str = None,
                         children: LsxChildren = None):
                super().__init__(
                    ConstructionHelperPoint=ConstructionHelperPoint,
                    ConstructionPointId=ConstructionPointId,
                    ConstructionPointStretch=ConstructionPointStretch,
                    ConstructionPointTransform=ConstructionPointTransform,
                    children=children,
                )

        ConstructionPointCount: int = LsxType.INT32
        id: str = LsxType.GUID
        children: LsxChildren = (ConstructionPoint,)

        def __init__(self,
                     *,
                     ConstructionPointCount: int = None,
                     id: str = None,
                     children: LsxChildren = None):
            super().__init__(
                ConstructionPointCount=ConstructionPointCount,
                id=id,
                children=children,
            )

    class Fillings(LsxNode):
        class Filling(LsxNode):
            class ConstructionSpline(LsxNode):
                class ConstructionPoint(LsxNode):
                    class ConstructionBranches(LsxNode):
                        class ConstructionBranch(LsxNode):
                            ConstructionPointId: str = LsxType.GUID

                            def __init__(self,
                                         *,
                                         ConstructionPointId: str = None):
                                super().__init__(
                                    ConstructionPointId=ConstructionPointId,
                                )

                        ConstructionBranchCount: int = LsxType.INT32
                        children: LsxChildren = (ConstructionBranch,)

                        def __init__(self,
                                     *,
                                     ConstructionBranchCount: int = None,
                                     children: LsxChildren = None):
                            super().__init__(
                                ConstructionBranchCount=ConstructionBranchCount,
                                children=children,
                            )

                    ConstructionHelperPoint: bool = LsxType.BOOL
                    ConstructionPointId: str = LsxType.GUID
                    ConstructionPointStretch: bool = LsxType.BOOL
                    ConstructionPointTransform: str = LsxType.MAT4X4
                    children: LsxChildren = (ConstructionBranches,)

                    def __init__(self,
                                 *,
                                 ConstructionHelperPoint: bool = None,
                                 ConstructionPointId: str = None,
                                 ConstructionPointStretch: bool = None,
                                 ConstructionPointTransform: str = None,
                                 children: LsxChildren = None):
                        super().__init__(
                            ConstructionHelperPoint=ConstructionHelperPoint,
                            ConstructionPointId=ConstructionPointId,
                            ConstructionPointStretch=ConstructionPointStretch,
                            ConstructionPointTransform=ConstructionPointTransform,
                            children=children,
                        )

                ConstructionPointCount: int = LsxType.INT32
                id: str = LsxType.GUID
                children: LsxChildren = (ConstructionPoint,)

                def __init__(self,
                             *,
                             ConstructionPointCount: int = None,
                             id: str = None,
                             children: LsxChildren = None):
                    super().__init__(
                        ConstructionPointCount=ConstructionPointCount,
                        id=id,
                        children=children,
                    )

            class Exclusions(LsxNode):
                pass

            class Indices(LsxNode):
                class Index(LsxNode):
                    Object: int = LsxType.UINT16

                    def __init__(self,
                                 *,
                                 Object: int = None):
                        super().__init__(
                            Object=Object,
                        )

                children: LsxChildren = (Index,)

                def __init__(self,
                             *,
                             children: LsxChildren = None):
                    super().__init__(
                        children=children,
                    )

            class Vertices(LsxNode):
                class Vertex(LsxNode):
                    Position: str = LsxType.FVEC3
                    UV: str = LsxType.FVEC2

                    def __init__(self,
                                 *,
                                 Position: str = None,
                                 UV: str = None):
                        super().__init__(
                            Position=Position,
                            UV=UV,
                        )

                children: LsxChildren = (Vertex,)

                def __init__(self,
                             *,
                             children: LsxChildren = None):
                    super().__init__(
                        children=children,
                    )

            BoundMax: str = LsxType.FVEC3
            BoundMin: str = LsxType.FVEC3
            FadeGroup: str = LsxType.FIXEDSTRING
            FadeIn: bool = LsxType.BOOL
            Fadeable: bool = LsxType.BOOL
            HierarchyOnlyFade: bool = LsxType.BOOL
            Id: str = LsxType.FIXEDSTRING
            Material: str = LsxType.FIXEDSTRING
            Name: str = LsxType.LSSTRING_VALUE
            Opacity: float = LsxType.FLOAT
            Physics: str = LsxType.FIXEDSTRING
            Rotate: str = LsxType.MAT3X3
            Scale: float = LsxType.FLOAT
            SeeThrough: bool = LsxType.BOOL
            Tiling: float = LsxType.FLOAT
            Translate: str = LsxType.FVEC3
            UVOffset: str = LsxType.FVEC2
            UVRotation: float = LsxType.FLOAT
            WalkOn: bool = LsxType.BOOL
            children: LsxChildren = (ConstructionSpline, Exclusions, Indices, Vertices)

            def __init__(self,
                         *,
                         BoundMax: str = None,
                         BoundMin: str = None,
                         FadeGroup: str = None,
                         FadeIn: bool = None,
                         Fadeable: bool = None,
                         HierarchyOnlyFade: bool = None,
                         Id: str = None,
                         Material: str = None,
                         Name: str = None,
                         Opacity: float = None,
                         Physics: str = None,
                         Rotate: str = None,
                         Scale: float = None,
                         SeeThrough: bool = None,
                         Tiling: float = None,
                         Translate: str = None,
                         UVOffset: str = None,
                         UVRotation: float = None,
                         WalkOn: bool = None,
                         children: LsxChildren = None):
                super().__init__(
                    BoundMax=BoundMax,
                    BoundMin=BoundMin,
                    FadeGroup=FadeGroup,
                    FadeIn=FadeIn,
                    Fadeable=Fadeable,
                    HierarchyOnlyFade=HierarchyOnlyFade,
                    Id=Id,
                    Material=Material,
                    Name=Name,
                    Opacity=Opacity,
                    Physics=Physics,
                    Rotate=Rotate,
                    Scale=Scale,
                    SeeThrough=SeeThrough,
                    Tiling=Tiling,
                    Translate=Translate,
                    UVOffset=UVOffset,
                    UVRotation=UVRotation,
                    WalkOn=WalkOn,
                    children=children,
                )

        children: LsxChildren = (Filling,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class tiles(LsxNode):
        class tile(LsxNode):
            CanSeeThrough: bool = LsxType.BOOL
            ClickThrough: bool = LsxType.BOOL
            Climbable: bool = LsxType.BOOL
            Flip: bool = LsxType.BOOL
            Point1: str = LsxType.GUID
            Point2: str = LsxType.GUID
            Rotate: str = LsxType.MAT3X3
            Scale: float = LsxType.FLOAT
            ScaleZ: float = LsxType.FLOAT
            ShootThrough: bool = LsxType.BOOL
            ShootThroughType: int = LsxType.INT8
            Stretchable: bool = LsxType.BOOL
            Translate: str = LsxType.FVEC3
            TwoSidedTileCount: int = LsxType.INT32
            UUID: str = LsxType.FIXEDSTRING
            WalkOn: bool = LsxType.BOOL
            WalkThrough: bool = LsxType.BOOL
            tile: str = LsxType.GUID

            def __init__(self,
                         *,
                         CanSeeThrough: bool = None,
                         ClickThrough: bool = None,
                         Climbable: bool = None,
                         Flip: bool = None,
                         Point1: str = None,
                         Point2: str = None,
                         Rotate: str = None,
                         Scale: float = None,
                         ScaleZ: float = None,
                         ShootThrough: bool = None,
                         ShootThroughType: int = None,
                         Stretchable: bool = None,
                         Translate: str = None,
                         TwoSidedTileCount: int = None,
                         UUID: str = None,
                         WalkOn: bool = None,
                         WalkThrough: bool = None,
                         tile: str = None):
                super().__init__(
                    CanSeeThrough=CanSeeThrough,
                    ClickThrough=ClickThrough,
                    Climbable=Climbable,
                    Flip=Flip,
                    Point1=Point1,
                    Point2=Point2,
                    Rotate=Rotate,
                    Scale=Scale,
                    ScaleZ=ScaleZ,
                    ShootThrough=ShootThrough,
                    ShootThroughType=ShootThroughType,
                    Stretchable=Stretchable,
                    Translate=Translate,
                    TwoSidedTileCount=TwoSidedTileCount,
                    UUID=UUID,
                    WalkOn=WalkOn,
                    WalkThrough=WalkThrough,
                    tile=tile,
                )

        CanSeeThrough: bool = LsxType.BOOL
        ClickThrough: bool = LsxType.BOOL
        Climbable: bool = LsxType.BOOL
        CollideWithCamera: bool = LsxType.BOOL
        ConstructionBend: bool = LsxType.BOOL
        ConstructionPlaceTwoTiles: bool = LsxType.BOOL
        FadeGroup: str = LsxType.FIXEDSTRING
        FadeIn: bool = LsxType.BOOL
        Fadeable: bool = LsxType.BOOL
        HierarchyOnlyFade: bool = LsxType.BOOL
        Opacity: float = LsxType.FLOAT
        SeeThrough: bool = LsxType.BOOL
        ShootThrough: bool = LsxType.BOOL
        ShootThroughType: int = LsxType.INT8
        TileSet: str = LsxType.FIXEDSTRING
        WalkOn: bool = LsxType.BOOL
        WalkThrough: bool = LsxType.BOOL
        children: LsxChildren = (tile,)

        def __init__(self,
                     *,
                     CanSeeThrough: bool = None,
                     ClickThrough: bool = None,
                     Climbable: bool = None,
                     CollideWithCamera: bool = None,
                     ConstructionBend: bool = None,
                     ConstructionPlaceTwoTiles: bool = None,
                     FadeGroup: str = None,
                     FadeIn: bool = None,
                     Fadeable: bool = None,
                     HierarchyOnlyFade: bool = None,
                     Opacity: float = None,
                     SeeThrough: bool = None,
                     ShootThrough: bool = None,
                     ShootThroughType: int = None,
                     TileSet: str = None,
                     WalkOn: bool = None,
                     WalkThrough: bool = None,
                     children: LsxChildren = None):
            super().__init__(
                CanSeeThrough=CanSeeThrough,
                ClickThrough=ClickThrough,
                Climbable=Climbable,
                CollideWithCamera=CollideWithCamera,
                ConstructionBend=ConstructionBend,
                ConstructionPlaceTwoTiles=ConstructionPlaceTwoTiles,
                FadeGroup=FadeGroup,
                FadeIn=FadeIn,
                Fadeable=Fadeable,
                HierarchyOnlyFade=HierarchyOnlyFade,
                Opacity=Opacity,
                SeeThrough=SeeThrough,
                ShootThrough=ShootThrough,
                ShootThroughType=ShootThroughType,
                TileSet=TileSet,
                WalkOn=WalkOn,
                WalkThrough=WalkThrough,
                children=children,
            )

    class SpeakerGroupList(LsxNode):
        class SpeakerGroup(LsxNode):
            Object: str = LsxType.GUID

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (SpeakerGroup,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class InteractionFilterList(LsxNode):
        class InteractionFilter(LsxNode):
            Object: str = LsxType.GUID

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (InteractionFilter,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    class FadeChildren(LsxNode):
        pass

    class GameMaster(LsxNode):
        pass

    class FX(LsxNode):
        pass

    class InstanceVisual(LsxNode):
        pass

    class IntroFX(LsxNode):
        pass

    class StatusData(LsxNode):
        class StatusData(LsxNode):
            AffectedByRoll: bool = LsxType.BOOL
            ApplyToCharacters: bool = LsxType.BOOL
            ApplyToItems: bool = LsxType.BOOL
            ApplyTypes: int = LsxType.UINT8
            Chance: float = LsxType.FLOAT
            Duration: float = LsxType.FLOAT
            Force: bool = LsxType.BOOL
            KeepAlive: bool = LsxType.BOOL
            OnlyOncePerTurn: bool = LsxType.BOOL
            Remove: bool = LsxType.BOOL
            StatusId: str = LsxType.FIXEDSTRING
            VanishOnApply: bool = LsxType.BOOL

            def __init__(self,
                         *,
                         AffectedByRoll: bool = None,
                         ApplyToCharacters: bool = None,
                         ApplyToItems: bool = None,
                         ApplyTypes: int = None,
                         Chance: float = None,
                         Duration: float = None,
                         Force: bool = None,
                         KeepAlive: bool = None,
                         OnlyOncePerTurn: bool = None,
                         Remove: bool = None,
                         StatusId: str = None,
                         VanishOnApply: bool = None):
                super().__init__(
                    AffectedByRoll=AffectedByRoll,
                    ApplyToCharacters=ApplyToCharacters,
                    ApplyToItems=ApplyToItems,
                    ApplyTypes=ApplyTypes,
                    Chance=Chance,
                    Duration=Duration,
                    Force=Force,
                    KeepAlive=KeepAlive,
                    OnlyOncePerTurn=OnlyOncePerTurn,
                    Remove=Remove,
                    StatusId=StatusId,
                    VanishOnApply=VanishOnApply,
                )

        children: LsxChildren = (StatusData,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

    Acceleration: float = LsxType.FLOAT
    ActiveCharacterLightID: str = LsxType.FIXEDSTRING
    AiHint: str = LsxType.GUID
    AiPathColor: str = LsxType.FVEC3
    AliveInventoryType: int = LsxType.UINT8
    AllowSummonGenericUse: bool = LsxType.BOOL
    Amount: float = LsxType.FLOAT
    Angle: str = LsxType.FVEC2
    AngleCutoff: float = LsxType.FLOAT
    AnimationSetResourceID: str = LsxType.FIXEDSTRING
    AnubisConfigName: str = LsxType.FIXEDSTRING
    Archetype: str = LsxType.FIXEDSTRING
    AttackableWhenClickThrough: bool = LsxType.BOOL
    AvoidTraps: bool = LsxType.BOOL
    BeamFX: str = LsxType.FIXEDSTRING
    BlockAoEDamage: bool = LsxType.BOOL
    BloodSurfaceType: str = LsxType.FIXEDSTRING
    BloodType: str = LsxType.FIXEDSTRING
    BookType: int = LsxType.UINT8
    CameraOffset: str = LsxType.FVEC3
    CanBeImprovisedWeapon: bool = LsxType.BOOL
    CanBeMoved: bool = LsxType.BOOL
    CanBePickedUp: bool = LsxType.BOOL
    CanBePickpocketed: bool = LsxType.BOOL
    CanBeTeleported: bool = LsxType.BOOL
    CanClickThrough: bool = LsxType.BOOL
    CanClimbLadders: bool = LsxType.BOOL
    CanClimbOn: bool = LsxType.BOOL
    CanConsumeItems: bool = LsxType.BOOL
    CanFight: bool = LsxType.BOOL
    CanJoinCombat: bool = LsxType.BOOL
    CanOpenDoors: bool = LsxType.BOOL
    CanShineThrough: bool = LsxType.BOOL
    CanShootThrough: bool = LsxType.BOOL
    CastBone: str = LsxType.FIXEDSTRING
    CastShadow: bool = LsxType.BOOL
    CharacterVisualResourceID: str = LsxType.FIXEDSTRING
    CinematicArenaFlags: int = LsxType.UINT32
    Color: str = LsxType.FVEC3
    Color4: str = LsxType.FVEC4
    ColorPreset: str = LsxType.GUID
    CombatGroupID: str = LsxType.FIXEDSTRING
    CombatName: str = LsxType.LSSTRING_VALUE
    ConstellationConfigName: str = LsxType.FIXEDSTRING
    ContainerAutoAddOnPickup: bool = LsxType.BOOL
    CoverAmount: int = LsxType.UINT8
    CriticalHitType: str = LsxType.FIXEDSTRING
    CurveResourceId: str = LsxType.FIXEDSTRING
    CustomPointTransform: str = LsxType.MAT4X4
    DeathEffect: str = LsxType.GUID
    DeathRaycastMaxLength: float = LsxType.FLOAT
    DeathRaycastMinLength: float = LsxType.FLOAT
    DeathRaycastVerticalLength: float = LsxType.FLOAT
    DecalMaterial: str = LsxType.FIXEDSTRING
    DefaultState_uint8: int = LsxType.UINT8  # DefaultState
    DefaultState_FixedString: str = LsxType.FIXEDSTRING  # DefaultState
    Description: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    DestroyTrailFXOnImpact: bool = LsxType.BOOL
    DestroyWithStack: bool = LsxType.BOOL
    Destroyed: bool = LsxType.BOOL
    DetachBeam: bool = LsxType.BOOL
    DevComment: str = LsxType.LSSTRING_VALUE
    Dimensions: str = LsxType.FVEC3
    DirectionLightAttenuationEnd: float = LsxType.FLOAT
    DirectionLightAttenuationFunction: int = LsxType.UINT8
    DirectionLightAttenuationSide: float = LsxType.FLOAT
    DirectionLightAttenuationStart: float = LsxType.FLOAT
    DirectionLightDimensions: str = LsxType.FVEC3
    DisableEquipping: bool = LsxType.BOOL
    DisarmDifficultyClassID: str = LsxType.GUID
    DisintegratedResourceID: str = LsxType.FIXEDSTRING
    DisplayName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    DisplayNameAlchemy: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    DistanceMax_Bezier3: float = LsxType.FLOAT
    DistanceMax_Bezier4: float = LsxType.FLOAT
    DistanceMin_Bezier3: float = LsxType.FLOAT
    DistanceMin_Bezier4: float = LsxType.FLOAT
    DropSound: str = LsxType.FIXEDSTRING
    Enabled: bool = LsxType.BOOL
    EquipSound: str = LsxType.FIXEDSTRING
    Equipment: str = LsxType.FIXEDSTRING
    EquipmentRace: str = LsxType.GUID
    EquipmentTypeID: str = LsxType.GUID
    ExamineRotation: str = LsxType.FVEC3
    ExplodedResourceID: str = LsxType.FIXEDSTRING
    ExplosionFX: str = LsxType.FIXEDSTRING
    Faction: str = LsxType.GUID
    FadeGroup: str = LsxType.FIXEDSTRING
    FadeGroupOnly: bool = LsxType.BOOL
    FadeIn: bool = LsxType.BOOL
    Fadeable: bool = LsxType.BOOL
    Flag_int32: int = LsxType.INT32  # Flag
    Flag_uint8: int = LsxType.UINT8  # Flag
    FlatFalloff: bool = LsxType.BOOL
    FoleyLongResourceID: str = LsxType.FIXEDSTRING
    FoleyMediumResourceID: str = LsxType.FIXEDSTRING
    FoleyShortResourceID: str = LsxType.FIXEDSTRING
    ForceAffectedByAura: bool = LsxType.BOOL
    ForceLifetimeDeath: bool = LsxType.BOOL
    FreezeGravity: bool = LsxType.BOOL
    Gain: float = LsxType.FLOAT
    GameplayCheckLOS: bool = LsxType.BOOL
    GameplayDirectionalDimensions: str = LsxType.FVEC3
    GameplayEdgeSharpening: float = LsxType.FLOAT
    GameplayIsActive: bool = LsxType.BOOL
    GameplayRadius: float = LsxType.FLOAT
    GameplaySpotlightAngle: float = LsxType.FLOAT
    GeneratePortrait: str = LsxType.LSSTRING_VALUE
    GizmoColorOverride: str = LsxType.FVEC4
    GravityType: int = LsxType.UINT8
    GroundImpactFX: str = LsxType.LSSTRING_VALUE
    GroupID: int = LsxType.UINT32
    GroupSizeMax: int = LsxType.UINT16
    GroupSizeMin: int = LsxType.UINT16
    GroupSpawnTimeMax: float = LsxType.FLOAT
    GroupSpawnTimeMin: float = LsxType.FLOAT
    HardcoreOnly: bool = LsxType.BOOL
    HasCustomPoint: bool = LsxType.BOOL
    HasGameplayValue: bool = LsxType.BOOL
    HiddenFromMinimapRendering: bool = LsxType.BOOL
    HierarchyOnlyFade: bool = LsxType.BOOL
    Hostile: bool = LsxType.BOOL
    Icon: str = LsxType.FIXEDSTRING
    IgnoreRoof: bool = LsxType.BOOL
    ImpactFX: str = LsxType.FIXEDSTRING
    ImpactSound: str = LsxType.FIXEDSTRING
    ImpactSoundResourceID: str = LsxType.FIXEDSTRING
    InitialSpeed: float = LsxType.FLOAT
    Intensity: float = LsxType.FLOAT
    InteractionFilterRequirement: int = LsxType.UINT8
    InteractionFilterType: int = LsxType.UINT8
    InventoryMoveSound: str = LsxType.FIXEDSTRING
    InventoryType: int = LsxType.UINT8
    IsBlocker: bool = LsxType.BOOL
    IsBlueprintDisabledByDefault: bool = LsxType.BOOL
    IsBoss: bool = LsxType.BOOL
    IsCinematic: bool = LsxType.BOOL
    IsDecorative: bool = LsxType.BOOL
    IsDroppedOnDeath: bool = LsxType.BOOL
    IsDynamicLayer: bool = LsxType.BOOL
    IsEquipmentLootable: bool = LsxType.BOOL
    IsFlickering: bool = LsxType.BOOL
    IsHalfLit: bool = LsxType.BOOL
    IsInspector: bool = LsxType.BOOL
    IsInteractionDisabled: bool = LsxType.BOOL
    IsKey: bool = LsxType.BOOL
    IsLootable: bool = LsxType.BOOL
    IsMoving: bool = LsxType.BOOL
    IsPlayer: bool = LsxType.BOOL
    IsPointerBlocker: bool = LsxType.BOOL
    IsPortal: bool = LsxType.BOOL
    IsPublicDomain: bool = LsxType.BOOL
    IsScrollingObject: bool = LsxType.BOOL
    IsShadowProxy: bool = LsxType.BOOL
    IsSimpleCharacter: bool = LsxType.BOOL
    IsSourceContainer: bool = LsxType.BOOL
    IsSunlight: bool = LsxType.BOOL
    IsSurfaceBlocker: bool = LsxType.BOOL
    IsTrap: bool = LsxType.BOOL
    JumpUpLadders: bool = LsxType.BOOL
    Kelvin: float = LsxType.FLOAT
    LadderAttachOffset: float = LsxType.FLOAT
    LadderLoopSpeed: float = LsxType.FLOAT
    Layer: int = LsxType.UINT32
    LevelName: str = LsxType.FIXEDSTRING
    LevelOverride: int = LsxType.INT32
    LevelTemplateType: int = LsxType.UINT8
    LifeTime: float = LsxType.FLOAT
    LightChannel: int = LsxType.UINT8
    LightChannelFlag: int = LsxType.UINT8
    LightCookieResource: str = LsxType.FIXEDSTRING
    LightID: str = LsxType.FIXEDSTRING
    LightType: int = LsxType.UINT8
    LightVolume: bool = LsxType.BOOL
    LightVolumeSamplesCount: int = LsxType.INT32
    LoopSound: str = LsxType.FIXEDSTRING
    MapKey: str = LsxType.FIXEDSTRING
    Material: str = LsxType.FIXEDSTRING
    MaterialType: int = LsxType.UINT8
    MaxCharacters: int = LsxType.UINT16
    MeshProxy: str = LsxType.FIXEDSTRING
    MovablePlatformStartSound: str = LsxType.FIXEDSTRING
    MovablePlatformStopSound: str = LsxType.FIXEDSTRING
    MovementAmount: float = LsxType.FLOAT
    MovementSpeed: float = LsxType.FLOAT
    Name: str = LsxType.LSSTRING_VALUE
    NeedsImpactSFX: bool = LsxType.BOOL
    NormalBlendingFactor: float = LsxType.FLOAT
    OffsetAMax_Bezier4: str = LsxType.FVEC2
    OffsetAMin_Bezier4: str = LsxType.FVEC2
    OffsetBMax_Bezier4: str = LsxType.FVEC2
    OffsetBMin_Bezier4: str = LsxType.FVEC2
    OffsetMax_Bezier3: str = LsxType.FVEC2
    OffsetMin_Bezier3: str = LsxType.FVEC2
    OnUseDescription: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    Opacity: float = LsxType.FLOAT
    ParentTemplateId: str = LsxType.FIXEDSTRING
    PhysicsFollowAnimation: bool = LsxType.BOOL
    PhysicsOpenTemplate: str = LsxType.FIXEDSTRING
    PhysicsTemplate: str = LsxType.FIXEDSTRING
    PhysicsType: int = LsxType.INT32
    PickupSound: str = LsxType.FIXEDSTRING
    PortraitVisualResourceID: str = LsxType.FIXEDSTRING
    PreExpose: bool = LsxType.BOOL
    PreviewPathImpactFX: str = LsxType.FIXEDSTRING
    PreviewPathMaterial: str = LsxType.FIXEDSTRING
    PreviewPathRadius: float = LsxType.FLOAT
    Race_int8: int = LsxType.INT8  # Race
    Race_guid: str = LsxType.GUID  # Race
    Radius: float = LsxType.FLOAT
    ReadinessFlags: int = LsxType.UINT32
    RecieveDecal: bool = LsxType.BOOL
    RenderChannel: int = LsxType.UINT8
    RollConditions: str = LsxType.LSSTRING_VALUE
    RotateImpact: bool = LsxType.BOOL
    RotateMode: int = LsxType.UINT8
    Scale: float = LsxType.FLOAT
    ScatteringScale: float = LsxType.FLOAT
    ScrollingDirection: str = LsxType.FVEC3
    ScrollingDistance: float = LsxType.FLOAT
    ScrollingOffset: float = LsxType.FLOAT
    ScrollingOrigin: str = LsxType.FVEC3
    ScrollingSpeed: float = LsxType.FLOAT
    SeeThrough: bool = LsxType.BOOL
    Shadow: bool = LsxType.BOOL
    ShadowPhysicsProxy: str = LsxType.FIXEDSTRING
    ShiftAMax_Bezier4: float = LsxType.FLOAT
    ShiftAMin_Bezier4: float = LsxType.FLOAT
    ShiftBMax_Bezier4: float = LsxType.FLOAT
    ShiftBMin_Bezier4: float = LsxType.FLOAT
    ShiftMax_Bezier3: float = LsxType.FLOAT
    ShiftMin_Bezier3: float = LsxType.FLOAT
    ShootThroughType: int = LsxType.INT8
    ShortDescription: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    ShortDescriptionParams: str = LsxType.LSSTRING_VALUE
    ShowAttachedSpellDescriptions: bool = LsxType.BOOL
    SoftBodyCollisionTemplate: str = LsxType.FIXEDSTRING
    SoundActivationRange: float = LsxType.FLOAT
    SoundAttenuation: int = LsxType.INT16
    SoundInitEvent: str = LsxType.FIXEDSTRING
    SoundMovementStartEvent: str = LsxType.FIXEDSTRING
    SoundMovementStopEvent: str = LsxType.FIXEDSTRING
    SoundObjectIndex: int = LsxType.UINT8
    Speed: float = LsxType.FLOAT
    SpellSet: str = LsxType.FIXEDSTRING
    SpotSneakers: bool = LsxType.BOOL
    StartCombatRange: float = LsxType.FLOAT
    StartingActive: bool = LsxType.BOOL
    StartingLoaded: bool = LsxType.BOOL
    Stats: str = LsxType.FIXEDSTRING
    StayInAiHints: bool = LsxType.BOOL
    StoryItem: bool = LsxType.BOOL
    SubLevelName: str = LsxType.FIXEDSTRING
    Summon: str = LsxType.FIXEDSTRING
    SurfaceCategory: int = LsxType.UINT8
    SwarmGroup: str = LsxType.FIXEDSTRING
    TechnicalDescription: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    TechnicalDescriptionParams: list[str] = LsxType.LSSTRING
    TemplateAfterDestruction: str = LsxType.FIXEDSTRING
    TextureMapping: int = LsxType.UINT8
    Tiling: str = LsxType.FVEC2
    Title: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    Tooltip: int = LsxType.UINT8
    TrailFX: str = LsxType.FIXEDSTRING
    TrajectoryType: int = LsxType.UINT8
    TreasureOnDestroy: bool = LsxType.BOOL
    TriggerGizmoOverride: str = LsxType.FIXEDSTRING
    TriggerType: str = LsxType.FIXEDSTRING
    Type: str = LsxType.FIXEDSTRING
    UnequipSound: str = LsxType.FIXEDSTRING
    Unimportant: bool = LsxType.BOOL
    UnknownDescription: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    UnknownDisplayName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    UseOcclusion: bool = LsxType.BOOL
    UsePartyLevelForTreasureLevel: bool = LsxType.BOOL
    UseRemotely: bool = LsxType.BOOL
    UseSound: str = LsxType.FIXEDSTRING
    UseSoundClustering: bool = LsxType.BOOL
    UseSoundOcclusion: bool = LsxType.BOOL
    UseTemperature: bool = LsxType.BOOL
    UsingGizmoColorOverride: bool = LsxType.BOOL
    VFXScale: float = LsxType.FLOAT
    VelocityMode: int = LsxType.UINT8
    VisualTemplate: str = LsxType.FIXEDSTRING
    VocalAlertResourceID: str = LsxType.FIXEDSTRING
    VocalAngryResourceID: str = LsxType.FIXEDSTRING
    VocalAnticipationResourceID: str = LsxType.FIXEDSTRING
    VocalAttackResourceID: str = LsxType.FIXEDSTRING
    VocalAwakeResourceID: str = LsxType.FIXEDSTRING
    VocalBoredResourceID: str = LsxType.FIXEDSTRING
    VocalBuffResourceID: str = LsxType.FIXEDSTRING
    VocalDeathResourceID: str = LsxType.FIXEDSTRING
    VocalDodgeResourceID: str = LsxType.FIXEDSTRING
    VocalEffortsResourceID: str = LsxType.FIXEDSTRING
    VocalExhaustedResourceID: str = LsxType.FIXEDSTRING
    VocalFallResourceID: str = LsxType.FIXEDSTRING
    VocalGaspResourceID: str = LsxType.FIXEDSTRING
    VocalIdle1ResourceID: str = LsxType.FIXEDSTRING
    VocalIdle2ResourceID: str = LsxType.FIXEDSTRING
    VocalIdle3ResourceID: str = LsxType.FIXEDSTRING
    VocalIdleCombat1ResourceID: str = LsxType.FIXEDSTRING
    VocalIdleCombat2ResourceID: str = LsxType.FIXEDSTRING
    VocalIdleCombat3ResourceID: str = LsxType.FIXEDSTRING
    VocalInitiativeResourceID: str = LsxType.FIXEDSTRING
    VocalLaughterManiacalResourceID: str = LsxType.FIXEDSTRING
    VocalLaughterResourceID: str = LsxType.FIXEDSTRING
    VocalNoneResourceID: str = LsxType.FIXEDSTRING
    VocalPainResourceID: str = LsxType.FIXEDSTRING
    VocalRebornResourceID: str = LsxType.FIXEDSTRING
    VocalRecoverResourceID: str = LsxType.FIXEDSTRING
    VocalRelaxedResourceID: str = LsxType.FIXEDSTRING
    VocalShoutResourceID: str = LsxType.FIXEDSTRING
    VocalSnoreResourceID: str = LsxType.FIXEDSTRING
    VocalSpawnResourceID: str = LsxType.FIXEDSTRING
    VocalVictoryResourceID: str = LsxType.FIXEDSTRING
    VocalWeakResourceID: str = LsxType.FIXEDSTRING
    VolumetricLightCollisionProbability: float = LsxType.FLOAT
    VolumetricLightIntensity: float = LsxType.FLOAT
    VolumetricShadow: bool = LsxType.BOOL
    Wadable: bool = LsxType.BOOL
    WadableSurfaceType: str = LsxType.FIXEDSTRING
    WalkOn: bool = LsxType.BOOL
    WalkThrough: bool = LsxType.BOOL
    _OriginalFileVersion_: int = LsxType.INT64
    maxStackAmount: int = LsxType.INT32
    offset: str = LsxType.FVEC2
    children: LsxChildren = (
        Bounds,
        OnDestroyActions,
        PrefabChildrenGroup,
        PrefabChildrenTransformGroup,
        LocomotionParams,
        SkillList,
        StatusList,
        Tags,
        PickingPhysics,
        OnUsePeaceActions,
        ConstellationConfigGlobalParameters,
        ExcludeInDifficulty,
        InventoryList,
        ItemList,
        OnlyInDifficulty,
        ScriptConfigGlobalParameters,
        ScriptOverrides,
        Scripts,
        Equipment_,
        EquipmentTypes,
        FootStepInfos,
        OnDeathActions,
        TradeTreasures,
        Treasures,
        ConstructionLines,
        ConstructionPoints,
        ConstructionSpline,
        Fillings,
        tiles,
        SpeakerGroupList,
        InteractionFilterList,
        FadeChildren,
        GameMaster,
        FX,
        InstanceVisual,
        IntroFX,
        StatusData,
    )

    def __init__(self,
                 *,
                 Acceleration: float = None,
                 ActiveCharacterLightID: str = None,
                 AiHint: str = None,
                 AiPathColor: str = None,
                 AliveInventoryType: int = None,
                 AllowSummonGenericUse: bool = None,
                 Amount: float = None,
                 Angle: str = None,
                 AngleCutoff: float = None,
                 AnimationSetResourceID: str = None,
                 AnubisConfigName: str = None,
                 Archetype: str = None,
                 AttackableWhenClickThrough: bool = None,
                 AvoidTraps: bool = None,
                 BeamFX: str = None,
                 BlockAoEDamage: bool = None,
                 BloodSurfaceType: str = None,
                 BloodType: str = None,
                 BookType: int = None,
                 CameraOffset: str = None,
                 CanBeImprovisedWeapon: bool = None,
                 CanBeMoved: bool = None,
                 CanBePickedUp: bool = None,
                 CanBePickpocketed: bool = None,
                 CanBeTeleported: bool = None,
                 CanClickThrough: bool = None,
                 CanClimbLadders: bool = None,
                 CanClimbOn: bool = None,
                 CanConsumeItems: bool = None,
                 CanFight: bool = None,
                 CanJoinCombat: bool = None,
                 CanOpenDoors: bool = None,
                 CanShineThrough: bool = None,
                 CanShootThrough: bool = None,
                 CastBone: str = None,
                 CastShadow: bool = None,
                 CharacterVisualResourceID: str = None,
                 CinematicArenaFlags: int = None,
                 Color: str = None,
                 Color4: str = None,
                 ColorPreset: str = None,
                 CombatGroupID: str = None,
                 CombatName: str = None,
                 ConstellationConfigName: str = None,
                 ContainerAutoAddOnPickup: bool = None,
                 CoverAmount: int = None,
                 CriticalHitType: str = None,
                 CurveResourceId: str = None,
                 CustomPointTransform: str = None,
                 DeathEffect: str = None,
                 DeathRaycastMaxLength: float = None,
                 DeathRaycastMinLength: float = None,
                 DeathRaycastVerticalLength: float = None,
                 DecalMaterial: str = None,
                 DefaultState_uint8: int = None,
                 DefaultState_FixedString: str = None,
                 Description: tuple[str, int] | str = None,
                 DestroyTrailFXOnImpact: bool = None,
                 DestroyWithStack: bool = None,
                 Destroyed: bool = None,
                 DetachBeam: bool = None,
                 DevComment: str = None,
                 Dimensions: str = None,
                 DirectionLightAttenuationEnd: float = None,
                 DirectionLightAttenuationFunction: int = None,
                 DirectionLightAttenuationSide: float = None,
                 DirectionLightAttenuationStart: float = None,
                 DirectionLightDimensions: str = None,
                 DisableEquipping: bool = None,
                 DisarmDifficultyClassID: str = None,
                 DisintegratedResourceID: str = None,
                 DisplayName: tuple[str, int] | str = None,
                 DisplayNameAlchemy: tuple[str, int] | str = None,
                 DistanceMax_Bezier3: float = None,
                 DistanceMax_Bezier4: float = None,
                 DistanceMin_Bezier3: float = None,
                 DistanceMin_Bezier4: float = None,
                 DropSound: str = None,
                 Enabled: bool = None,
                 EquipSound: str = None,
                 Equipment_: str = None,
                 EquipmentRace: str = None,
                 EquipmentTypeID: str = None,
                 ExamineRotation: str = None,
                 ExplodedResourceID: str = None,
                 ExplosionFX: str = None,
                 Faction: str = None,
                 FadeGroup: str = None,
                 FadeGroupOnly: bool = None,
                 FadeIn: bool = None,
                 Fadeable: bool = None,
                 Flag_int32: int = None,
                 Flag_uint8: int = None,
                 FlatFalloff: bool = None,
                 FoleyLongResourceID: str = None,
                 FoleyMediumResourceID: str = None,
                 FoleyShortResourceID: str = None,
                 ForceAffectedByAura: bool = None,
                 ForceLifetimeDeath: bool = None,
                 FreezeGravity: bool = None,
                 Gain: float = None,
                 GameplayCheckLOS: bool = None,
                 GameplayDirectionalDimensions: str = None,
                 GameplayEdgeSharpening: float = None,
                 GameplayIsActive: bool = None,
                 GameplayRadius: float = None,
                 GameplaySpotlightAngle: float = None,
                 GeneratePortrait: str = None,
                 GizmoColorOverride: str = None,
                 GravityType: int = None,
                 GroundImpactFX: str = None,
                 GroupID: int = None,
                 GroupSizeMax: int = None,
                 GroupSizeMin: int = None,
                 GroupSpawnTimeMax: float = None,
                 GroupSpawnTimeMin: float = None,
                 HardcoreOnly: bool = None,
                 HasCustomPoint: bool = None,
                 HasGameplayValue: bool = None,
                 HiddenFromMinimapRendering: bool = None,
                 HierarchyOnlyFade: bool = None,
                 Hostile: bool = None,
                 Icon: str = None,
                 IgnoreRoof: bool = None,
                 ImpactFX: str = None,
                 ImpactSound: str = None,
                 ImpactSoundResourceID: str = None,
                 InitialSpeed: float = None,
                 Intensity: float = None,
                 InteractionFilterRequirement: int = None,
                 InteractionFilterType: int = None,
                 InventoryMoveSound: str = None,
                 InventoryType: int = None,
                 IsBlocker: bool = None,
                 IsBlueprintDisabledByDefault: bool = None,
                 IsBoss: bool = None,
                 IsCinematic: bool = None,
                 IsDecorative: bool = None,
                 IsDroppedOnDeath: bool = None,
                 IsDynamicLayer: bool = None,
                 IsEquipmentLootable: bool = None,
                 IsFlickering: bool = None,
                 IsHalfLit: bool = None,
                 IsInspector: bool = None,
                 IsInteractionDisabled: bool = None,
                 IsKey: bool = None,
                 IsLootable: bool = None,
                 IsMoving: bool = None,
                 IsPlayer: bool = None,
                 IsPointerBlocker: bool = None,
                 IsPortal: bool = None,
                 IsPublicDomain: bool = None,
                 IsScrollingObject: bool = None,
                 IsShadowProxy: bool = None,
                 IsSimpleCharacter: bool = None,
                 IsSourceContainer: bool = None,
                 IsSunlight: bool = None,
                 IsSurfaceBlocker: bool = None,
                 IsTrap: bool = None,
                 JumpUpLadders: bool = None,
                 Kelvin: float = None,
                 LadderAttachOffset: float = None,
                 LadderLoopSpeed: float = None,
                 Layer: int = None,
                 LevelName: str = None,
                 LevelOverride: int = None,
                 LevelTemplateType: int = None,
                 LifeTime: float = None,
                 LightChannel: int = None,
                 LightChannelFlag: int = None,
                 LightCookieResource: str = None,
                 LightID: str = None,
                 LightType: int = None,
                 LightVolume: bool = None,
                 LightVolumeSamplesCount: int = None,
                 LoopSound: str = None,
                 MapKey: str = None,
                 Material: str = None,
                 MaterialType: int = None,
                 MaxCharacters: int = None,
                 MeshProxy: str = None,
                 MovablePlatformStartSound: str = None,
                 MovablePlatformStopSound: str = None,
                 MovementAmount: float = None,
                 MovementSpeed: float = None,
                 Name: str = None,
                 NeedsImpactSFX: bool = None,
                 NormalBlendingFactor: float = None,
                 OffsetAMax_Bezier4: str = None,
                 OffsetAMin_Bezier4: str = None,
                 OffsetBMax_Bezier4: str = None,
                 OffsetBMin_Bezier4: str = None,
                 OffsetMax_Bezier3: str = None,
                 OffsetMin_Bezier3: str = None,
                 OnUseDescription: tuple[str, int] | str = None,
                 Opacity: float = None,
                 ParentTemplateId: str = None,
                 PhysicsFollowAnimation: bool = None,
                 PhysicsOpenTemplate: str = None,
                 PhysicsTemplate: str = None,
                 PhysicsType: int = None,
                 PickupSound: str = None,
                 PortraitVisualResourceID: str = None,
                 PreExpose: bool = None,
                 PreviewPathImpactFX: str = None,
                 PreviewPathMaterial: str = None,
                 PreviewPathRadius: float = None,
                 Race_int8: int = None,
                 Race_guid: str = None,
                 Radius: float = None,
                 ReadinessFlags: int = None,
                 RecieveDecal: bool = None,
                 RenderChannel: int = None,
                 RollConditions: str = None,
                 RotateImpact: bool = None,
                 RotateMode: int = None,
                 Scale: float = None,
                 ScatteringScale: float = None,
                 ScrollingDirection: str = None,
                 ScrollingDistance: float = None,
                 ScrollingOffset: float = None,
                 ScrollingOrigin: str = None,
                 ScrollingSpeed: float = None,
                 SeeThrough: bool = None,
                 Shadow: bool = None,
                 ShadowPhysicsProxy: str = None,
                 ShiftAMax_Bezier4: float = None,
                 ShiftAMin_Bezier4: float = None,
                 ShiftBMax_Bezier4: float = None,
                 ShiftBMin_Bezier4: float = None,
                 ShiftMax_Bezier3: float = None,
                 ShiftMin_Bezier3: float = None,
                 ShootThroughType: int = None,
                 ShortDescription: tuple[str, int] | str = None,
                 ShortDescriptionParams: str = None,
                 ShowAttachedSpellDescriptions: bool = None,
                 SoftBodyCollisionTemplate: str = None,
                 SoundActivationRange: float = None,
                 SoundAttenuation: int = None,
                 SoundInitEvent: str = None,
                 SoundMovementStartEvent: str = None,
                 SoundMovementStopEvent: str = None,
                 SoundObjectIndex: int = None,
                 Speed: float = None,
                 SpellSet: str = None,
                 SpotSneakers: bool = None,
                 StartCombatRange: float = None,
                 StartingActive: bool = None,
                 StartingLoaded: bool = None,
                 Stats: str = None,
                 StayInAiHints: bool = None,
                 StoryItem: bool = None,
                 SubLevelName: str = None,
                 Summon: str = None,
                 SurfaceCategory: int = None,
                 SwarmGroup: str = None,
                 TechnicalDescription: tuple[str, int] | str = None,
                 TechnicalDescriptionParams: list[str] = None,
                 TemplateAfterDestruction: str = None,
                 TextureMapping: int = None,
                 Tiling: str = None,
                 Title: tuple[str, int] | str = None,
                 Tooltip: int = None,
                 TrailFX: str = None,
                 TrajectoryType: int = None,
                 TreasureOnDestroy: bool = None,
                 TriggerGizmoOverride: str = None,
                 TriggerType: str = None,
                 Type: str = None,
                 UnequipSound: str = None,
                 Unimportant: bool = None,
                 UnknownDescription: tuple[str, int] | str = None,
                 UnknownDisplayName: tuple[str, int] | str = None,
                 UseOcclusion: bool = None,
                 UsePartyLevelForTreasureLevel: bool = None,
                 UseRemotely: bool = None,
                 UseSound: str = None,
                 UseSoundClustering: bool = None,
                 UseSoundOcclusion: bool = None,
                 UseTemperature: bool = None,
                 UsingGizmoColorOverride: bool = None,
                 VFXScale: float = None,
                 VelocityMode: int = None,
                 VisualTemplate: str = None,
                 VocalAlertResourceID: str = None,
                 VocalAngryResourceID: str = None,
                 VocalAnticipationResourceID: str = None,
                 VocalAttackResourceID: str = None,
                 VocalAwakeResourceID: str = None,
                 VocalBoredResourceID: str = None,
                 VocalBuffResourceID: str = None,
                 VocalDeathResourceID: str = None,
                 VocalDodgeResourceID: str = None,
                 VocalEffortsResourceID: str = None,
                 VocalExhaustedResourceID: str = None,
                 VocalFallResourceID: str = None,
                 VocalGaspResourceID: str = None,
                 VocalIdle1ResourceID: str = None,
                 VocalIdle2ResourceID: str = None,
                 VocalIdle3ResourceID: str = None,
                 VocalIdleCombat1ResourceID: str = None,
                 VocalIdleCombat2ResourceID: str = None,
                 VocalIdleCombat3ResourceID: str = None,
                 VocalInitiativeResourceID: str = None,
                 VocalLaughterManiacalResourceID: str = None,
                 VocalLaughterResourceID: str = None,
                 VocalNoneResourceID: str = None,
                 VocalPainResourceID: str = None,
                 VocalRebornResourceID: str = None,
                 VocalRecoverResourceID: str = None,
                 VocalRelaxedResourceID: str = None,
                 VocalShoutResourceID: str = None,
                 VocalSnoreResourceID: str = None,
                 VocalSpawnResourceID: str = None,
                 VocalVictoryResourceID: str = None,
                 VocalWeakResourceID: str = None,
                 VolumetricLightCollisionProbability: float = None,
                 VolumetricLightIntensity: float = None,
                 VolumetricShadow: bool = None,
                 Wadable: bool = None,
                 WadableSurfaceType: str = None,
                 WalkOn: bool = None,
                 WalkThrough: bool = None,
                 _OriginalFileVersion_: int = None,
                 maxStackAmount: int = None,
                 offset: str = None,
                 children: LsxChildren = None):
        super().__init__(
            Acceleration=Acceleration,
            ActiveCharacterLightID=ActiveCharacterLightID,
            AiHint=AiHint,
            AiPathColor=AiPathColor,
            AliveInventoryType=AliveInventoryType,
            AllowSummonGenericUse=AllowSummonGenericUse,
            Amount=Amount,
            Angle=Angle,
            AngleCutoff=AngleCutoff,
            AnimationSetResourceID=AnimationSetResourceID,
            AnubisConfigName=AnubisConfigName,
            Archetype=Archetype,
            AttackableWhenClickThrough=AttackableWhenClickThrough,
            AvoidTraps=AvoidTraps,
            BeamFX=BeamFX,
            BlockAoEDamage=BlockAoEDamage,
            BloodSurfaceType=BloodSurfaceType,
            BloodType=BloodType,
            BookType=BookType,
            CameraOffset=CameraOffset,
            CanBeImprovisedWeapon=CanBeImprovisedWeapon,
            CanBeMoved=CanBeMoved,
            CanBePickedUp=CanBePickedUp,
            CanBePickpocketed=CanBePickpocketed,
            CanBeTeleported=CanBeTeleported,
            CanClickThrough=CanClickThrough,
            CanClimbLadders=CanClimbLadders,
            CanClimbOn=CanClimbOn,
            CanConsumeItems=CanConsumeItems,
            CanFight=CanFight,
            CanJoinCombat=CanJoinCombat,
            CanOpenDoors=CanOpenDoors,
            CanShineThrough=CanShineThrough,
            CanShootThrough=CanShootThrough,
            CastBone=CastBone,
            CastShadow=CastShadow,
            CharacterVisualResourceID=CharacterVisualResourceID,
            CinematicArenaFlags=CinematicArenaFlags,
            Color=Color,
            Color4=Color4,
            ColorPreset=ColorPreset,
            CombatGroupID=CombatGroupID,
            CombatName=CombatName,
            ConstellationConfigName=ConstellationConfigName,
            ContainerAutoAddOnPickup=ContainerAutoAddOnPickup,
            CoverAmount=CoverAmount,
            CriticalHitType=CriticalHitType,
            CurveResourceId=CurveResourceId,
            CustomPointTransform=CustomPointTransform,
            DeathEffect=DeathEffect,
            DeathRaycastMaxLength=DeathRaycastMaxLength,
            DeathRaycastMinLength=DeathRaycastMinLength,
            DeathRaycastVerticalLength=DeathRaycastVerticalLength,
            DecalMaterial=DecalMaterial,
            DefaultState_uint8=DefaultState_uint8,
            DefaultState_FixedString=DefaultState_FixedString,
            Description=Description,
            DestroyTrailFXOnImpact=DestroyTrailFXOnImpact,
            DestroyWithStack=DestroyWithStack,
            Destroyed=Destroyed,
            DetachBeam=DetachBeam,
            DevComment=DevComment,
            Dimensions=Dimensions,
            DirectionLightAttenuationEnd=DirectionLightAttenuationEnd,
            DirectionLightAttenuationFunction=DirectionLightAttenuationFunction,
            DirectionLightAttenuationSide=DirectionLightAttenuationSide,
            DirectionLightAttenuationStart=DirectionLightAttenuationStart,
            DirectionLightDimensions=DirectionLightDimensions,
            DisableEquipping=DisableEquipping,
            DisarmDifficultyClassID=DisarmDifficultyClassID,
            DisintegratedResourceID=DisintegratedResourceID,
            DisplayName=DisplayName,
            DisplayNameAlchemy=DisplayNameAlchemy,
            DistanceMax_Bezier3=DistanceMax_Bezier3,
            DistanceMax_Bezier4=DistanceMax_Bezier4,
            DistanceMin_Bezier3=DistanceMin_Bezier3,
            DistanceMin_Bezier4=DistanceMin_Bezier4,
            DropSound=DropSound,
            Enabled=Enabled,
            EquipSound=EquipSound,
            Equipment_=Equipment_,
            EquipmentRace=EquipmentRace,
            EquipmentTypeID=EquipmentTypeID,
            ExamineRotation=ExamineRotation,
            ExplodedResourceID=ExplodedResourceID,
            ExplosionFX=ExplosionFX,
            Faction=Faction,
            FadeGroup=FadeGroup,
            FadeGroupOnly=FadeGroupOnly,
            FadeIn=FadeIn,
            Fadeable=Fadeable,
            Flag_int32=Flag_int32,
            Flag_uint8=Flag_uint8,
            FlatFalloff=FlatFalloff,
            FoleyLongResourceID=FoleyLongResourceID,
            FoleyMediumResourceID=FoleyMediumResourceID,
            FoleyShortResourceID=FoleyShortResourceID,
            ForceAffectedByAura=ForceAffectedByAura,
            ForceLifetimeDeath=ForceLifetimeDeath,
            FreezeGravity=FreezeGravity,
            Gain=Gain,
            GameplayCheckLOS=GameplayCheckLOS,
            GameplayDirectionalDimensions=GameplayDirectionalDimensions,
            GameplayEdgeSharpening=GameplayEdgeSharpening,
            GameplayIsActive=GameplayIsActive,
            GameplayRadius=GameplayRadius,
            GameplaySpotlightAngle=GameplaySpotlightAngle,
            GeneratePortrait=GeneratePortrait,
            GizmoColorOverride=GizmoColorOverride,
            GravityType=GravityType,
            GroundImpactFX=GroundImpactFX,
            GroupID=GroupID,
            GroupSizeMax=GroupSizeMax,
            GroupSizeMin=GroupSizeMin,
            GroupSpawnTimeMax=GroupSpawnTimeMax,
            GroupSpawnTimeMin=GroupSpawnTimeMin,
            HardcoreOnly=HardcoreOnly,
            HasCustomPoint=HasCustomPoint,
            HasGameplayValue=HasGameplayValue,
            HiddenFromMinimapRendering=HiddenFromMinimapRendering,
            HierarchyOnlyFade=HierarchyOnlyFade,
            Hostile=Hostile,
            Icon=Icon,
            IgnoreRoof=IgnoreRoof,
            ImpactFX=ImpactFX,
            ImpactSound=ImpactSound,
            ImpactSoundResourceID=ImpactSoundResourceID,
            InitialSpeed=InitialSpeed,
            Intensity=Intensity,
            InteractionFilterRequirement=InteractionFilterRequirement,
            InteractionFilterType=InteractionFilterType,
            InventoryMoveSound=InventoryMoveSound,
            InventoryType=InventoryType,
            IsBlocker=IsBlocker,
            IsBlueprintDisabledByDefault=IsBlueprintDisabledByDefault,
            IsBoss=IsBoss,
            IsCinematic=IsCinematic,
            IsDecorative=IsDecorative,
            IsDroppedOnDeath=IsDroppedOnDeath,
            IsDynamicLayer=IsDynamicLayer,
            IsEquipmentLootable=IsEquipmentLootable,
            IsFlickering=IsFlickering,
            IsHalfLit=IsHalfLit,
            IsInspector=IsInspector,
            IsInteractionDisabled=IsInteractionDisabled,
            IsKey=IsKey,
            IsLootable=IsLootable,
            IsMoving=IsMoving,
            IsPlayer=IsPlayer,
            IsPointerBlocker=IsPointerBlocker,
            IsPortal=IsPortal,
            IsPublicDomain=IsPublicDomain,
            IsScrollingObject=IsScrollingObject,
            IsShadowProxy=IsShadowProxy,
            IsSimpleCharacter=IsSimpleCharacter,
            IsSourceContainer=IsSourceContainer,
            IsSunlight=IsSunlight,
            IsSurfaceBlocker=IsSurfaceBlocker,
            IsTrap=IsTrap,
            JumpUpLadders=JumpUpLadders,
            Kelvin=Kelvin,
            LadderAttachOffset=LadderAttachOffset,
            LadderLoopSpeed=LadderLoopSpeed,
            Layer=Layer,
            LevelName=LevelName,
            LevelOverride=LevelOverride,
            LevelTemplateType=LevelTemplateType,
            LifeTime=LifeTime,
            LightChannel=LightChannel,
            LightChannelFlag=LightChannelFlag,
            LightCookieResource=LightCookieResource,
            LightID=LightID,
            LightType=LightType,
            LightVolume=LightVolume,
            LightVolumeSamplesCount=LightVolumeSamplesCount,
            LoopSound=LoopSound,
            MapKey=MapKey,
            Material=Material,
            MaterialType=MaterialType,
            MaxCharacters=MaxCharacters,
            MeshProxy=MeshProxy,
            MovablePlatformStartSound=MovablePlatformStartSound,
            MovablePlatformStopSound=MovablePlatformStopSound,
            MovementAmount=MovementAmount,
            MovementSpeed=MovementSpeed,
            Name=Name,
            NeedsImpactSFX=NeedsImpactSFX,
            NormalBlendingFactor=NormalBlendingFactor,
            OffsetAMax_Bezier4=OffsetAMax_Bezier4,
            OffsetAMin_Bezier4=OffsetAMin_Bezier4,
            OffsetBMax_Bezier4=OffsetBMax_Bezier4,
            OffsetBMin_Bezier4=OffsetBMin_Bezier4,
            OffsetMax_Bezier3=OffsetMax_Bezier3,
            OffsetMin_Bezier3=OffsetMin_Bezier3,
            OnUseDescription=OnUseDescription,
            Opacity=Opacity,
            ParentTemplateId=ParentTemplateId,
            PhysicsFollowAnimation=PhysicsFollowAnimation,
            PhysicsOpenTemplate=PhysicsOpenTemplate,
            PhysicsTemplate=PhysicsTemplate,
            PhysicsType=PhysicsType,
            PickupSound=PickupSound,
            PortraitVisualResourceID=PortraitVisualResourceID,
            PreExpose=PreExpose,
            PreviewPathImpactFX=PreviewPathImpactFX,
            PreviewPathMaterial=PreviewPathMaterial,
            PreviewPathRadius=PreviewPathRadius,
            Race_int8=Race_int8,
            Race_guid=Race_guid,
            Radius=Radius,
            ReadinessFlags=ReadinessFlags,
            RecieveDecal=RecieveDecal,
            RenderChannel=RenderChannel,
            RollConditions=RollConditions,
            RotateImpact=RotateImpact,
            RotateMode=RotateMode,
            Scale=Scale,
            ScatteringScale=ScatteringScale,
            ScrollingDirection=ScrollingDirection,
            ScrollingDistance=ScrollingDistance,
            ScrollingOffset=ScrollingOffset,
            ScrollingOrigin=ScrollingOrigin,
            ScrollingSpeed=ScrollingSpeed,
            SeeThrough=SeeThrough,
            Shadow=Shadow,
            ShadowPhysicsProxy=ShadowPhysicsProxy,
            ShiftAMax_Bezier4=ShiftAMax_Bezier4,
            ShiftAMin_Bezier4=ShiftAMin_Bezier4,
            ShiftBMax_Bezier4=ShiftBMax_Bezier4,
            ShiftBMin_Bezier4=ShiftBMin_Bezier4,
            ShiftMax_Bezier3=ShiftMax_Bezier3,
            ShiftMin_Bezier3=ShiftMin_Bezier3,
            ShootThroughType=ShootThroughType,
            ShortDescription=ShortDescription,
            ShortDescriptionParams=ShortDescriptionParams,
            ShowAttachedSpellDescriptions=ShowAttachedSpellDescriptions,
            SoftBodyCollisionTemplate=SoftBodyCollisionTemplate,
            SoundActivationRange=SoundActivationRange,
            SoundAttenuation=SoundAttenuation,
            SoundInitEvent=SoundInitEvent,
            SoundMovementStartEvent=SoundMovementStartEvent,
            SoundMovementStopEvent=SoundMovementStopEvent,
            SoundObjectIndex=SoundObjectIndex,
            Speed=Speed,
            SpellSet=SpellSet,
            SpotSneakers=SpotSneakers,
            StartCombatRange=StartCombatRange,
            StartingActive=StartingActive,
            StartingLoaded=StartingLoaded,
            Stats=Stats,
            StayInAiHints=StayInAiHints,
            StoryItem=StoryItem,
            SubLevelName=SubLevelName,
            Summon=Summon,
            SurfaceCategory=SurfaceCategory,
            SwarmGroup=SwarmGroup,
            TechnicalDescription=TechnicalDescription,
            TechnicalDescriptionParams=TechnicalDescriptionParams,
            TemplateAfterDestruction=TemplateAfterDestruction,
            TextureMapping=TextureMapping,
            Tiling=Tiling,
            Title=Title,
            Tooltip=Tooltip,
            TrailFX=TrailFX,
            TrajectoryType=TrajectoryType,
            TreasureOnDestroy=TreasureOnDestroy,
            TriggerGizmoOverride=TriggerGizmoOverride,
            TriggerType=TriggerType,
            Type=Type,
            UnequipSound=UnequipSound,
            Unimportant=Unimportant,
            UnknownDescription=UnknownDescription,
            UnknownDisplayName=UnknownDisplayName,
            UseOcclusion=UseOcclusion,
            UsePartyLevelForTreasureLevel=UsePartyLevelForTreasureLevel,
            UseRemotely=UseRemotely,
            UseSound=UseSound,
            UseSoundClustering=UseSoundClustering,
            UseSoundOcclusion=UseSoundOcclusion,
            UseTemperature=UseTemperature,
            UsingGizmoColorOverride=UsingGizmoColorOverride,
            VFXScale=VFXScale,
            VelocityMode=VelocityMode,
            VisualTemplate=VisualTemplate,
            VocalAlertResourceID=VocalAlertResourceID,
            VocalAngryResourceID=VocalAngryResourceID,
            VocalAnticipationResourceID=VocalAnticipationResourceID,
            VocalAttackResourceID=VocalAttackResourceID,
            VocalAwakeResourceID=VocalAwakeResourceID,
            VocalBoredResourceID=VocalBoredResourceID,
            VocalBuffResourceID=VocalBuffResourceID,
            VocalDeathResourceID=VocalDeathResourceID,
            VocalDodgeResourceID=VocalDodgeResourceID,
            VocalEffortsResourceID=VocalEffortsResourceID,
            VocalExhaustedResourceID=VocalExhaustedResourceID,
            VocalFallResourceID=VocalFallResourceID,
            VocalGaspResourceID=VocalGaspResourceID,
            VocalIdle1ResourceID=VocalIdle1ResourceID,
            VocalIdle2ResourceID=VocalIdle2ResourceID,
            VocalIdle3ResourceID=VocalIdle3ResourceID,
            VocalIdleCombat1ResourceID=VocalIdleCombat1ResourceID,
            VocalIdleCombat2ResourceID=VocalIdleCombat2ResourceID,
            VocalIdleCombat3ResourceID=VocalIdleCombat3ResourceID,
            VocalInitiativeResourceID=VocalInitiativeResourceID,
            VocalLaughterManiacalResourceID=VocalLaughterManiacalResourceID,
            VocalLaughterResourceID=VocalLaughterResourceID,
            VocalNoneResourceID=VocalNoneResourceID,
            VocalPainResourceID=VocalPainResourceID,
            VocalRebornResourceID=VocalRebornResourceID,
            VocalRecoverResourceID=VocalRecoverResourceID,
            VocalRelaxedResourceID=VocalRelaxedResourceID,
            VocalShoutResourceID=VocalShoutResourceID,
            VocalSnoreResourceID=VocalSnoreResourceID,
            VocalSpawnResourceID=VocalSpawnResourceID,
            VocalVictoryResourceID=VocalVictoryResourceID,
            VocalWeakResourceID=VocalWeakResourceID,
            VolumetricLightCollisionProbability=VolumetricLightCollisionProbability,
            VolumetricLightIntensity=VolumetricLightIntensity,
            VolumetricShadow=VolumetricShadow,
            Wadable=Wadable,
            WadableSurfaceType=WadableSurfaceType,
            WalkOn=WalkOn,
            WalkThrough=WalkThrough,
            _OriginalFileVersion_=_OriginalFileVersion_,
            maxStackAmount=maxStackAmount,
            offset=offset,
            children=children,
        )


class Templates(LsxDocument):
    root = "Templates"
    path = "Public/{folder}/RootTemplates/_merged.lsf.lsx"
    children: LsxChildren = (GameObjects,)


Lsx.register(Templates)
