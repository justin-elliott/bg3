
import os

from functools import cached_property
from moddb import Awareness
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class OpenHand(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="OpenHand",
                         description="A class replacer for OpenHand.",
                         **kwds)

    @cached_property
    def _awareness(self) -> str:
        return Awareness(self.mod).add_awareness()

    @cached_property
    def _flurry_of_blows(self) -> str:
        """Flurry of Blows zone attack."""
        name = self.make_name("Zone_FlurryOfBlows")
        self.add(SpellData(
            name,
            using="Zone_SweepingAttack",
            SpellType="Zone",
            DisplayName=self.loca(f"{name}_DisplayName", "Flurry of Blows"),
            Description=self.loca(f"{name}_Description", """
                Strike a flurry of blows against all enemies in front of you.
            """),
            Icon="Action_Monk_FlurryOfBlows",
            MaximumTargets="",
            SpellFlags=["IsMelee", "IsHarmful", "DisableBlood"],
            SpellProperties="",
            SpellRoll="Attack(AttackType.MeleeUnarmedAttack)",
            SpellSuccess=["DealDamage(UnarmedDamage,Bludgeoning)"],
            TooltipDamageList=["DealDamage(UnarmedDamage,Bludgeoning)"],
            DamageType="Bludgeoning",
            Sheathing="Sheathed",
            UseCosts=["BonusActionPoint:1", "KiPoint:1"],
            WeaponTypes="",
            PrepareSound="Vocal_Component_Monk_Damage",
            CastSound="Spell_Cast_Monk_FlurryofBlows_L1to3",
            TargetSound="Spell_Impact_Monk_OpenHandTech_L1to3",
            PrepareEffect="d8ea7a73-027c-4472-b638-2b939d384900",
            CastEffect="57a6a6b3-a088-4b90-9777-683963616236",
            TargetEffect="dc8efa81-182b-4446-82ac-5e0e4c5f87d0",
        ))
        return name

    @cached_property
    def _flurry_of_blows_topple(self) -> str:
        name = self.make_name("Zone_FlurryOfBlows_Topple")
        self.add(SpellData(
            name,
            using=self._flurry_of_blows,
            SpellType="Zone",
            DisplayName=self.loca(f"{name}_DisplayName", "Flurry of Blows: Topple"),
            Description=self.loca(f"{name}_Description", """
                Strike a flurry of blows against all enemies in front of you, possibly knocking them
                <LSTag Type="Status" Tooltip="PRONE">Prone</LSTag>.
            """),
            Icon="Action_Monk_OpenHandTechnique_Knock",
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                "IF(not SavingThrow(Ability.Dexterity,ManeuverSaveDC())):ApplyStatus(PRONE,100,1)",
            ],
            TooltipStatusApply=["ApplyStatus(PRONE,100,1)"],
            PrepareEffect="85386181-e9ec-4996-a1dd-7f09f3013189",
            CastEffect="208b02ef-5847-493d-94b8-a901691979ef",
            TargetEffect="82b8aad9-5031-41f8-a871-dc55eb52af88",
        ))
        return name

    @cached_property
    def _flurry_of_blows_stagger(self) -> str:
        name = self.make_name("Zone_FlurryOfBlows_Stagger")
        self.add(SpellData(
            name,
            using=self._flurry_of_blows,
            SpellType="Zone",
            DisplayName=self.loca(f"{name}_DisplayName", "Flurry of Blows: Stagger"),
            Description=self.loca(f"{name}_Description", """
                Strike a flurry of blows against all enemies in front of you,
                <LSTag Type="Status" Tooltip="OPEN_HAND_NO_REACTIONS">Staggering</LSTag> them, making them unable to
                take reactions.
            """),
            Icon="Action_Monk_OpenHandTechnique_NoReactions",
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                "ApplyStatus(OPEN_HAND_NO_REACTIONS,100,1)",
            ],
            TooltipStatusApply=["ApplyStatus(OPEN_HAND_NO_REACTIONS,100,1)"],
            PrepareEffect="85386181-e9ec-4996-a1dd-7f09f3013189",
            TargetEffect="cff54a9a-6f6d-4b1b-9d0e-4177302cd63d",
        ))
        return name

    @cached_property
    def _flurry_of_blows_push(self) -> str:
        name = self.make_name("Zone_FlurryOfBlows_Push")
        self.add(SpellData(
            name,
            using=self._flurry_of_blows,
            SpellType="Zone",
            DisplayName=self.loca(f"{name}_DisplayName", "Flurry of Blows: Push"),
            Description=self.loca(f"{name}_Description", """
                Strike a flurry of blows against all enemies in front of you, possibly pushing them [1] away.
            """),
            DescriptionParams=["Distance(5)"],
            Icon="Action_Monk_OpenHandTechnique_Push",
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                "IF(not SavingThrow(Ability.Strength,ManeuverSaveDC())):Force(5)",
            ],
            PrepareEffect="85386181-e9ec-4996-a1dd-7f09f3013189",
            CastEffect="4aac52d4-55eb-4867-95b9-c8309bb48129",
            TargetEffect="f02c259a-32ff-4667-80db-3a52f290081d",
        ))
        return name

    @cached_property
    def _stillness_of_mind(self) -> str:
        """The Stillness of Mind class feature as a passive."""
        name = self.make_name("StillnessOfMind")

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Stillness of Mind"}
        loca[f"{name}_Description"] = {"en": """
            You are immune to being <LSTag Tooltip="CharmedGroup">Charmed</LSTag> or
            <LSTag Type="Status" Tooltip="FRIGHTENED">Frightened</LSTag>.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_StillnessOfMind",
            Properties=["Highlighted"],
            Boosts=[
                "StatusImmunity(SG_Charmed)",
                "StatusImmunity(SG_Frightened)",
            ],
        ))

        return name

    @cached_property
    def _wholeness_of_body(self) -> str:
        """The Wholeness of Body subclass feature as a passive."""
        name = self.make_name("WholenessOfBody")

        HEALTH_PER_TURN = "1d4"
        KI_PER_TURN = "1"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Wholeness of Body"}
        loca[f"{name}_Description"] = {"en": """
            Gain an additional bonus action.

            While in combat, you heal [1] every turn, and restore [2]
            <LSTag Type="ActionResource" Tooltip="KiPoint">Ki Point(s)</LSTag>.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=[
                f"RegainHitPoints({HEALTH_PER_TURN})",
                str(KI_PER_TURN),
            ],
            Icon="Action_Monk_WholenessOfBody",
            Properties=["Highlighted", "OncePerTurn"],
            Boosts=["ActionResource(BonusActionPoint,1,0)"],
            StatsFunctorContext=["OnTurn"],
            Conditions=["not HasStatus('DOWNED') and not Dead() and Combat()"],
            StatsFunctors=[
                f"RegainHitPoints({HEALTH_PER_TURN})",
                f"RestoreResource(KiPoint,{KI_PER_TURN},0)",
            ],
        ))

        return name

    @cached_property
    def _level_3_spell_list(self) -> str:
        spell_list = str(self.make_uuid("level_3_spell_list"))
        self.mod.add(SpellList(
            Name="Way of the Open Hand Monk Level 3 Spells",
            Spells=[
                self._flurry_of_blows_topple,
                self._flurry_of_blows_stagger,
                self._flurry_of_blows_push,
            ],
            UUID=spell_list,
        ))
        return spell_list

    @progression(CharacterClass.MONK, 7)
    def monk_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            *[passive for passive in progress.PassivesAdded if not passive == "StillnessOfMind"],
            self._stillness_of_mind,
        ]

    @progression(CharacterClass.MONK_OPENHAND, 3)
    def openhand_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            self._awareness,
            "FastHands",
        ]
        progress.Selectors = [
            f"AddSpells({self._level_3_spell_list})",
        ]

    @progression(CharacterClass.MONK_OPENHAND, 4)
    def openhand_level_4(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ImprovedCritical"]

    @progression(CharacterClass.MONK_OPENHAND, 5)
    def openhand_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["UncannyDodge"]

    @progression(CharacterClass.MONK_OPENHAND, 6)
    def openhand_level_6(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [self._wholeness_of_body]
        progress.Selectors = None

    @progression(CharacterClass.MONK_OPENHAND, 7)
    def openhand_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 8)
    def openhand_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 9)
    def openhand_level_9(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ReliableTalent"]
        progress.Selectors = None

    @progression(CharacterClass.MONK_OPENHAND, 10)
    def openhand_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 11)
    def openhand_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_2"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack"]

    @progression(CharacterClass.MONK_OPENHAND, 12)
    def openhand_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 13)
    def openhand_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 14)
    def openhand_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 15)
    def openhand_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 16)
    def openhand_level_16(self, progress: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 17)
    def openhand_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 18)
    def openhand_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 19)
    def openhand_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 20)
    def openhand_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_3"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack_2"]


def main() -> None:
    open_hand = OpenHand(
        classes=[CharacterClass.MONK_OPENHAND],
        actions=2,
        level_20=True,
    )
    open_hand.build()


if __name__ == "__main__":
    main()
