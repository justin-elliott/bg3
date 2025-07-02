
import os

from functools import cached_property
from moddb import (
    Awareness,
    Bolster,
    Defense,
)
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class OpenHand(Replacer):
    # Passives
    _awareness: str
    _warding: str

    # Spells
    _bolster: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="OpenHand",
                         description="A class replacer for OpenHand.",
                         **kwds)

        self._awareness = Awareness(self.mod).add_awareness(5)
        self._warding = Defense(self.mod).add_warding()

        self._bolster = Bolster(self.mod).add_bolster_spell_list()

    @cached_property
    def _whirlwind_attack(self) -> str:
        """Whirlwind attack as a bonus action."""
        name = f"{self.mod.get_prefix()}_WhirlwindAttack"

        self.mod.add(SpellData(
            name,
            using="Shout_Whirlwind",
            SpellType="Shout",
            PrepareSound="Vocal_Component_Monk_Damage",
            CastSound="Spell_Cast_Monk_FlurryofBlows_L1to3",
            HitAnimationType="PhysicalDamage",
            SpellFlags=["IsMelee", "IsHarmful", "DisableBlood"],
            SpellRoll="Attack(AttackType.MeleeUnarmedAttack)",
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                "IF(not SavingThrow(Ability.Dexterity,ManeuverSaveDC())):ApplyStatus(PRONE,100,1)",
            ],
            TooltipAttackSave="MeleeUnarmedAttack",
            TooltipDamageList=["DealDamage(UnarmedDamage,Bludgeoning)"],
            TooltipStatusApply=["ApplyStatus(PRONE,100,1)"],
            DamageType="Bludgeoning",
            Sheathing="Sheathed",
            VerbalIntent="Damage",
            WeaponTypes=[],
            PrepareEffect="85386181-e9ec-4996-a1dd-7f09f3013189",
            CastEffect="208b02ef-5847-493d-94b8-a901691979ef",
            TargetEffect="82b8aad9-5031-41f8-a871-dc55eb52af88",
            UseCosts=["BonusActionPoint:1", "KiPoint:1"],
        ))

        return name

    @cached_property
    def _stillness_of_mind(self) -> str:
        """The Stillness of Mind class feature as a passive."""
        name = f"{self.mod.get_prefix()}_StillnessOfMind"

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
        name = f"{self.mod.get_prefix()}_WholenessOfBody"

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
    def _level_9_spell_list(self) -> str:
        spell_list = str(self.make_uuid("level_9_spell_list"))
        self.mod.add(SpellList(
            Name="Way of the Open Hand Monk Whirlwind and Volley",
            Spells=[self._whirlwind_attack, "Target_Volley"],
            UUID=spell_list,
        ))
        return spell_list

    @progression(CharacterClass.MONK, 1)
    def monk_level_1(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._bolster},,,,AlwaysPrepared)",
        ]

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
            "DevilsSight",
            "FastHands",
            self._warding,
        ]

    @progression(CharacterClass.MONK_OPENHAND, 4)
    def openhand_level_4(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ImprovedCritical"]
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

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
    def openhand_level_8(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.MONK_OPENHAND, 9)
    def openhand_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 10)
    def openhand_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_OPENHAND, 11)
    def openhand_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_2"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack"]

    @progression(CharacterClass.MONK_OPENHAND, 12)
    def openhand_level_12(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ReliableTalent"]
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

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
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

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
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]


def main() -> None:
    open_hand = OpenHand(
        classes=[CharacterClass.MONK_OPENHAND],
        feats=2,
        actions=2,
        skills=4,
        expertise=2,
    )
    open_hand.build()


if __name__ == "__main__":
    main()
