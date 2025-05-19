#!/usr/bin/env python3
"""
Generates files for the "OpenHand" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import multiply_resources
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import ActionResource, CharacterClass, Progression, SpellList
from modtools.replacers import progression, Replacer


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class OpenHand(Replacer):
    @dataclass
    class Args:
        feats: set[int]  # Feat improvement levels
        actions: int     # Multiplier for other action resources

    _args: Args
    _feat_levels: set[int]

    @cached_property
    def _spinning_kick(self) -> str:
        """The Spinning Kick attack."""
        name = f"{self.mod.get_prefix()}_SpinningKick"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Spinning Kick"}
        loca[f"{name}_Description"] = {"en": """
            Strike out with a spinning kick at all nearby foes, making separate
            <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag> against each target.
            """}

        self.mod.add(SpellData(
            name,
            using="Shout_Whirlwind",
            SpellType="Shout",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="Action_IronboundPursuit",
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
            Name="Way of the Open Hand Monk Spinning Kick",
            Spells=[self._spinning_kick],
            UUID=spell_list,
        ))
        return spell_list

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="OpenHand",
                         description="Enhancements for the Way of the Open Hand subclass.")

        self._args = args

        if len(args.feats) == 0:
            self._feat_levels = frozenset({*range(2, 20, 2)} | {19})
        elif len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            self._feat_levels = frozenset(
                {*range(max(feat_level, 2), 20, feat_level)} | ({19} if 20 % feat_level == 0 else {}))
        else:
            self._feat_levels = args.feats - frozenset([1])

    @progression(CharacterClass.MONK, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Selectors = [
            *[selector for selector in progression.Selectors if not selector.startswith("SelectSkills")],
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.MONK, range(1, 21))
    def level_1_to_20_monk(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.KI_POINTS], self._args.actions)

    @progression(CharacterClass.MONK_OPENHAND, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "FastHands",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ImprovedCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
        ]

    @progression(CharacterClass.MONK_OPENHAND, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._wholeness_of_body,
        ]
        progression.Selectors = [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"
        ]

    @progression(CharacterClass.MONK, 7)
    def level_7_monk(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            *[passive for passive in progression.PassivesAdded if not passive == "StillnessOfMind"],
            self._stillness_of_mind,
        ]

    @progression(CharacterClass.MONK_OPENHAND, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = [
            f"AddSpells({self._level_9_spell_list})",
        ]

    @progression(CharacterClass.MONK_OPENHAND, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "BrutalCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
        ]

    @progression(CharacterClass.MONK_OPENHAND, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ReliableTalent",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"
        ]

    @progression(CharacterClass.MONK_OPENHAND, 13)
    def level_13(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 14)
    def level_14(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 15)
    def level_15(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 16)
    def level_16(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
        ]

    @progression(CharacterClass.MONK_OPENHAND, 17)
    def level_17(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 18)
    def level_18(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"
        ]

    @progression(CharacterClass.MONK_OPENHAND, 19)
    def level_19(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.MONK_OPENHAND, 20)
    def level_20(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_3"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack_2"]
        progression.Selectors = (progression.Selectors or []) + [
        ]


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 12))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="Enhancements for the Way of the Open Hand subclass.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource multiplier (defaulting to 2; double resources)")
    args = OpenHand.Args(**vars(parser.parse_args()))

    open_hand = OpenHand(args)
    open_hand.build()


if __name__ == "__main__":
    main()
