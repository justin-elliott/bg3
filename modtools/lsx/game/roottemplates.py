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

        children: LsxChildren = (Bound,)

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

            ActionType: int = LsxType.INT32
            children: LsxChildren = (Attributes,)

        children: LsxChildren = (Action,)

    class PrefabChildrenGroup(LsxNode):
        class PrefabChildren(LsxNode):
            Object: str = LsxType.FIXEDSTRING

        children: LsxChildren = (PrefabChildren,)

    class PrefabChildrenTransformGroup(LsxNode):
        class PrefabChildrenTransforms(LsxNode):
            Position: str = LsxType.FVEC3
            RotationQuat: str = LsxType.FVEC4
            Scale: float = LsxType.FLOAT

        children: LsxChildren = (PrefabChildrenTransforms,)

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

    class SkillList(LsxNode):
        class Skill(LsxNode):
            class SourceConditions(LsxNode):
                class Tags(LsxNode):
                    class Tag(LsxNode):
                        Object: str = LsxType.GUID

                    children: LsxChildren = (Tag,)

                MaximumHealthPercentage: int = LsxType.INT32
                MinimumHealthPercentage: int = LsxType.INT32
                children: LsxChildren = (Tags,)

            class TargetConditions(LsxNode):
                class Tags(LsxNode):
                    class Tag(LsxNode):
                        Object: str = LsxType.GUID

                    children: LsxChildren = (Tag,)

                MaximumHealthPercentage: int = LsxType.INT32
                MinimumHealthPercentage: int = LsxType.INT32
                children: LsxChildren = (Tags,)

            class OnlyInNPCLoadout(LsxNode):
                Object: str = LsxType.GUID

            class ExcludeInNPCLoadout(LsxNode):
                Object: str = LsxType.GUID

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
            children: LsxChildren = (SourceConditions, TargetConditions, OnlyInNPCLoadout, ExcludeInNPCLoadout)

        children: LsxChildren = (Skill,)

    class StatusList(LsxNode):
        class Status(LsxNode):
            Object: str = LsxType.FIXEDSTRING

        children: LsxChildren = (Status,)

    class Tags(LsxNode):
        class Tag(LsxNode):
            Object: str = LsxType.GUID

        children: LsxChildren = (Tag,)

    class PickingPhysics(LsxNode):
        class PickingPhysicsTemplates(LsxNode):
            MapKey: str = LsxType.FIXEDSTRING
            MapValue: str = LsxType.FIXEDSTRING

        children: LsxChildren = (PickingPhysicsTemplates,)

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

            ActionType: int = LsxType.INT32
            children: LsxChildren = (Attributes,)

        children: LsxChildren = (Action,)

    class ConstellationConfigGlobalParameters(LsxNode):
        class ConstellationConfigParameter(LsxNode):
            class Value(LsxNode):
                class Scalar(LsxNode):
                    class Scalar(LsxNode):
                        class String(LsxNode):
                            String: str = LsxType.LSSTRING_VALUE

                        class double(LsxNode):
                            double: float = LsxType.DOUBLE

                        children: LsxChildren = (String, double)

                    children: LsxChildren = (Scalar,)

                children: LsxChildren = (Scalar,)

            Name: str = LsxType.LSSTRING_VALUE
            children: LsxChildren = (Value,)

        children: LsxChildren = (ConstellationConfigParameter,)

    class ExcludeInDifficulty(LsxNode):
        pass

    class InventoryList(LsxNode):
        class InventoryItem(LsxNode):
            Object: str = LsxType.FIXEDSTRING

        children: LsxChildren = (InventoryItem,)

    class ItemList(LsxNode):
        class Item(LsxNode):
            class SourceConditions(LsxNode):
                class Tags(LsxNode):
                    pass

                MaximumHealthPercentage: int = LsxType.INT32
                MinimumHealthPercentage: int = LsxType.INT32
                children: LsxChildren = (Tags,)

            class TargetConditions(LsxNode):
                class Tags(LsxNode):
                    pass

                MaximumHealthPercentage: int = LsxType.INT32
                MinimumHealthPercentage: int = LsxType.INT32
                children: LsxChildren = (Tags,)

            class OnlyInNPCLoadout(LsxNode):
                Object: str = LsxType.GUID

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

        children: LsxChildren = (Item,)

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

                            MapKey: str = LsxType.FIXEDSTRING
                            children: LsxChildren = (ScriptVariables,)

                        children: LsxChildren = (Object,)

                    children: LsxChildren = (ScriptVariables,)

                MapKey: str = LsxType.FIXEDSTRING
                children: LsxChildren = (ScriptOverrides,)

            children: LsxChildren = (Object,)

        children: LsxChildren = (ScriptOverrides,)

    class Scripts(LsxNode):
        class Script(LsxNode):
            class Parameters(LsxNode):
                class Parameter(LsxNode):
                    MapKey: str = LsxType.FIXEDSTRING
                    Type: int = LsxType.INT32
                    Value: list[str] = LsxType.LSSTRING

                children: LsxChildren = (Parameter,)

            UUID: str = LsxType.FIXEDSTRING
            children: LsxChildren = (Parameters,)

        children: LsxChildren = (Script,)

    class Equipment_(LsxNode):
        _id_ = "Equipment"

        class AfroLongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class AfroShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class CurlyLongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class CurlyShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class DreadLongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class DreadShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class LongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class ParentRace(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.GUID

            children: LsxChildren = (Object,)

        class ShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class Visuals(LsxNode):
            class Object(LsxNode):
                class MapValue(LsxNode):
                    Object: str = LsxType.FIXEDSTRING

                MapKey: str = LsxType.GUID
                children: LsxChildren = (MapValue,)

            children: LsxChildren = (Object,)

        class WavyLongHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class WavyShortHair(LsxNode):
            class Object(LsxNode):
                MapKey: str = LsxType.GUID
                MapValue: str = LsxType.FIXEDSTRING

            children: LsxChildren = (Object,)

        class Slot(LsxNode):
            Object: str = LsxType.FIXEDSTRING

        class VisualSet(LsxNode):
            class MaterialOverrides(LsxNode):
                class MaterialPresets(LsxNode):
                    class Object(LsxNode):
                        ForcePresetValues: bool = LsxType.BOOL
                        GroupName: str = LsxType.FIXEDSTRING
                        MapKey: str = LsxType.FIXEDSTRING
                        MaterialPresetResource: str = LsxType.FIXEDSTRING

                    children: LsxChildren = (Object,)

                class Vector3Parameters(LsxNode):
                    Color: bool = LsxType.BOOL
                    Custom: bool = LsxType.BOOL
                    Enabled: bool = LsxType.BOOL
                    Parameter: str = LsxType.FIXEDSTRING
                    Value: str = LsxType.FVEC3

                class ColorPreset(LsxNode):
                    ForcePresetValues: bool = LsxType.BOOL
                    GroupName: str = LsxType.FIXEDSTRING
                    MaterialPresetResource: str = LsxType.FIXEDSTRING

                MaterialResource: str = LsxType.FIXEDSTRING
                children: LsxChildren = (MaterialPresets, Vector3Parameters, ColorPreset)

            class RealMaterialOverrides(LsxNode):
                pass

            BodySetVisual: str = LsxType.FIXEDSTRING
            ShowEquipmentVisuals: bool = LsxType.BOOL
            children: LsxChildren = (MaterialOverrides, RealMaterialOverrides)

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

    class EquipmentTypes(LsxNode):
        class EquipmentType(LsxNode):
            _id_ = ""
            Object: str = LsxType.GUID

        children: LsxChildren = (EquipmentType,)

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

        children: LsxChildren = (FootStepInfo,)

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

            ActionType: int = LsxType.INT32
            children: LsxChildren = (Attributes,)

        children: LsxChildren = (Action,)

    class TradeTreasures(LsxNode):
        class TreasureItem(LsxNode):
            Object: str = LsxType.FIXEDSTRING

        children: LsxChildren = (TreasureItem,)

    class Treasures(LsxNode):
        class TreasureItem(LsxNode):
            Object: str = LsxType.FIXEDSTRING

        children: LsxChildren = (TreasureItem,)

    class ConstructionLines(LsxNode):
        class ConstructionLine(LsxNode):
            class ConstructionPoints(LsxNode):
                class ConstructionPoint(LsxNode):
                    ConstructionPointId: str = LsxType.GUID

                children: LsxChildren = (ConstructionPoint,)

            class HelperEnd(LsxNode):
                ConstructionPointId: str = LsxType.GUID

            class HelperStart(LsxNode):
                ConstructionPointId: str = LsxType.GUID

            ConstructionLineGuid: str = LsxType.GUID
            children: LsxChildren = (ConstructionPoints, HelperEnd, HelperStart)

        children: LsxChildren = (ConstructionLine,)

    class ConstructionPoints(LsxNode):
        class ConstructionPoint(LsxNode):
            class ConstructionPointNeighbours(LsxNode):
                class ConstructionPointNeighbour(LsxNode):
                    class ConstructionPointNeighbours(LsxNode):
                        class ConstructionPointNeighbour(LsxNode):
                            ConstructionPointId: str = LsxType.GUID

                        children: LsxChildren = (ConstructionPointNeighbour,)

                    class ConstructionTileLists(LsxNode):
                        class ConstructionTileList(LsxNode):
                            class ConstructionPointLeftCornerTiles(LsxNode):
                                class ConstructionPointLeftCornerTile(LsxNode):
                                    TileId: str = LsxType.GUID

                                children: LsxChildren = (ConstructionPointLeftCornerTile,)

                            class ConstructionPointNeighbourTiles(LsxNode):
                                class ConstructionPointNeighbourTile(LsxNode):
                                    ConstructionPointTile1Id: str = LsxType.GUID

                                children: LsxChildren = (ConstructionPointNeighbourTile,)

                            class ConstructionPointRightCornerTiles(LsxNode):
                                class ConstructionPointRightCornerTile(LsxNode):
                                    TileId: str = LsxType.GUID

                                children: LsxChildren = (ConstructionPointRightCornerTile,)

                            ConstructionNonOptimalTilesEnd: int = LsxType.INT32
                            ConstructionNonOptimalTilesStart: int = LsxType.INT32
                            Side: int = LsxType.INT32
                            children: LsxChildren = (
                                ConstructionPointLeftCornerTiles,
                                ConstructionPointNeighbourTiles,
                                ConstructionPointRightCornerTiles,
                            )

                        children: LsxChildren = (ConstructionTileList,)

                    children: LsxChildren = (ConstructionPointNeighbours, ConstructionTileLists)

                children: LsxChildren = (ConstructionPointNeighbour,)

            ConstructionPointId: str = LsxType.GUID
            ConstructionPointStop: bool = LsxType.BOOL
            children: LsxChildren = (ConstructionPointNeighbours,)

        children: LsxChildren = (ConstructionPoint,)

    class ConstructionSpline(LsxNode):
        class ConstructionPoint(LsxNode):
            class ConstructionBranches(LsxNode):
                class ConstructionBranch(LsxNode):
                    ConstructionPointId: str = LsxType.GUID

                ConstructionBranchCount: int = LsxType.INT32
                children: LsxChildren = (ConstructionBranch,)

            ConstructionHelperPoint: bool = LsxType.BOOL
            ConstructionPointId: str = LsxType.GUID
            ConstructionPointStretch: bool = LsxType.BOOL
            ConstructionPointTransform: str = LsxType.MAT4X4
            children: LsxChildren = (ConstructionBranches,)

        ConstructionPointCount: int = LsxType.INT32
        id: str = LsxType.GUID
        children: LsxChildren = (ConstructionPoint,)

    class Fillings(LsxNode):
        class Filling(LsxNode):
            class ConstructionSpline(LsxNode):
                class ConstructionPoint(LsxNode):
                    class ConstructionBranches(LsxNode):
                        class ConstructionBranch(LsxNode):
                            ConstructionPointId: str = LsxType.GUID

                        ConstructionBranchCount: int = LsxType.INT32
                        children: LsxChildren = (ConstructionBranch,)

                    ConstructionHelperPoint: bool = LsxType.BOOL
                    ConstructionPointId: str = LsxType.GUID
                    ConstructionPointStretch: bool = LsxType.BOOL
                    ConstructionPointTransform: str = LsxType.MAT4X4
                    children: LsxChildren = (ConstructionBranches,)

                ConstructionPointCount: int = LsxType.INT32
                id: str = LsxType.GUID
                children: LsxChildren = (ConstructionPoint,)

            class Exclusions(LsxNode):
                pass

            class Indices(LsxNode):
                class Index(LsxNode):
                    Object: int = LsxType.UINT16

                children: LsxChildren = (Index,)

            class Vertices(LsxNode):
                class Vertex(LsxNode):
                    Position: str = LsxType.FVEC3
                    UV: str = LsxType.FVEC2

                children: LsxChildren = (Vertex,)

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

        children: LsxChildren = (Filling,)

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

    class SpeakerGroupList(LsxNode):
        class SpeakerGroup(LsxNode):
            Object: str = LsxType.GUID

        children: LsxChildren = (SpeakerGroup,)

    class InteractionFilterList(LsxNode):
        class InteractionFilter(LsxNode):
            Object: str = LsxType.GUID

        children: LsxChildren = (InteractionFilter,)

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

        children: LsxChildren = (StatusData,)

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
    DefaultState_FixedString: str = LsxType.FIXEDSTRING  # DefaultState
    DefaultState_uint8: int = LsxType.UINT8  # DefaultState
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
    Flag: int = LsxType.INT32
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
    Race_guid: str = LsxType.GUID  # Race
    Race_int8: int = LsxType.INT8  # Race
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


class Templates(LsxDocument):
    root = "Templates"
    path = "Public/{folder}/RootTemplates/_merged.lsf.lsx"
    children: LsxChildren = (GameObjects,)


Lsx.register(Templates)
