#!/usr/bin/env python3
"""
Generates files for the "MonkExpanded" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    Bolster,
    multiply_resources,
    PackMule,
)
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
)
from modtools.lsx.game import Dependencies, Progression
from modtools.replacers import (
    Replacer,
    progression,
)
from uuid import UUID


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class MonkExpanded(Replacer):
    @dataclass
    class Args:
        feats: int      # Feats every n levels
        actions: int    # Multiplier for action resources (Ki Points)
        skills: int     # Number of skills to select at character creation
        expertise: int  # Number of skills with expertise to select at character creation

    _args: Args
    _feat_levels: set[int]

    # Passives
    _pack_mule: str

    # Spell lists
    _bolster_spell_list: str

    @cached_property
    def _awareness(self) -> str:
        """The Awareness passive, a variant of Alert."""
        name = f"{self.mod.get_prefix()}_Awareness"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Awareness"}
        loca[f"{name}_Description"] = {"en": """
            You have honed your senses to the utmost degree. You gain a +[1] bonus to Initiative, can't be
            <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>, and attackers can't land
            <LSTag Tooltip="CriticalHit">Critical Hits</LSTag> against you.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["3"],
            Icon="Action_Barbarian_MagicAwareness",
            Properties=["ForceShowInCC", "Highlighted"],
            Boosts=[
                "Initiative(3)",
                "StatusImmunity(SURPRISED)",
                "CriticalHit(AttackTarget,Success,Never)",
            ],
        ))

        return name

    @cached_property
    def _ki_empowered_strikes(self) -> str:
        """Ki-Empowered strikes incorporating a manifestation bonus."""
        name = f"{self.mod.get_prefix()}_KiEmpoweredStrikes"

        loca = self.mod.get_localization()
        loca[f"{name}_Description"] = {"en": """
            Your unarmed attacks deal an additional [1] and count as magical for the purpose of overcoming enemies'
            <LSTag Tooltip="Resistant">Resistance</LSTag> and <LSTag Tooltip="Immune">Immunity</LSTag> to non-magical
            damage.
            """}

        self.mod.add(PassiveData(
            name,
            using="KiEmpoweredStrikes",
            Description=loca[f"{name}_Description"],
            DescriptionParams=["DealDamage(1d4+WisdomModifier,Force)"],
            Boosts=[
                "UnarmedMagicalProperty()",
                "IF(IsMeleeUnarmedAttack()):CharacterUnarmedDamage(1d4+WisdomModifier,Force)",
                "UnlockSpellVariant(MeleeUnarmedAttackCheck(),ModifyTargetRadius(Multiplicative,1))",
            ],
            Properties=["ForceShowInCC", "Highlighted"],
        ))

        return name

    @cached_property
    def _slow_fall(self) -> str:
        """The Slow Fall class feature as a passive."""
        name = f"{self.mod.get_prefix()}_SlowFall"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Slow Fall"}
        loca[f"{name}_Description"] = {"en": """
            You only take half damage from falling.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_SlowFall",
            Properties=["Highlighted"],
            Boosts=["FallDamageMultiplier(0.5)"],
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
            Properties=["ForceShowInCC", "Highlighted"],
            Boosts=["StatusImmunity(SG_Charmed)", "StatusImmunity(SG_Frightened)"],
        ))

        return name

    @cached_property
    def _wholeness_of_body(self) -> str:
        """The Wholeness of Body subclass feature as a passive."""
        name = f"{self.mod.get_prefix()}_WholenessOfBody"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Wholeness of Body"}
        loca[f"{name}_Description"] = {"en": """
            While in combat, you heal [1] every turn, and restore [2]
            <LSTag Type="ActionResource" Tooltip="KiPoint">Ki Point(s)</LSTag>.
            """}
    
        HEALTH_PER_TURN = "1d4"
        KI_PER_TURN = 1

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=[f"{name}_Description"],
            DescriptionParams=[
                f"RegainHitPoints({HEALTH_PER_TURN})",
                str(KI_PER_TURN),
            ],
            Icon="Action_Monk_WholenessOfBody",
            Properties=["ForceShowInCC", "Highlighted", "OncePerTurn"],
            StatsFunctorContext=["OnTurn"],
            Conditions=["not HasStatus('DOWNED') and not Dead() and Combat()"],
            StatsFunctors=[
                f"RegainHitPoints({HEALTH_PER_TURN})",
                f"RestoreResource(KiPoint,{KI_PER_TURN},0)",
            ],
        ))

        return name

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="MonkExpanded",
                         description="Monk expansion.")

        self.mod.add(Dependencies.ShortModuleDesc(
            Folder="UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            MD5="f94d034502139cf8b65a1597554e7236",
            Name="UnlockLevelCurve",
            PublishHandle=4166963,
            UUID="a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            Version64=72057594037927960,
        ))

        self._args = args

        if len(args.feats) == 0:
            self._feat_levels = frozenset({*range(2, 20, 2)} | {19})
        elif len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            self._feat_levels = frozenset(
                {*range(max(feat_level, 2), 20, feat_level)} | ({19} if 20 % feat_level == 0 else {}))
        else:
            self._feat_levels = args.feats - frozenset([1])

        self._bolster_spell_list = Bolster(self.mod).add_bolster_spell_list()
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)

    @progression(CharacterClass.MONK, range(1, 21))
    @progression(CharacterClass.MONK, 1, is_multiclass=True)
    def level_1_to_12_monk(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.KI_POINTS], self._args.actions)

    @progression(CharacterClass.MONK, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Selectors = [
            "SelectAbilityBonus(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,AbilityBonus,2,1)",
            f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self._args.skills})",
            f"SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self._args.expertise})",
            f"AddSpells({self._bolster_spell_list},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK, 2)
    def level_2(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = progression.PassivesAdded + ["FastHands"]

    @progression(CharacterClass.MONK, 4)
    def level_4_monk(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            *[passive for passive in progression.PassivesAdded if not passive == "SlowFall"],
            self._slow_fall,
        ]

    @progression(CharacterClass.MONK, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = progression.PassivesAdded + ["UncannyDodge"]

    @progression(CharacterClass.MONK, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            *[passive for passive in progression.PassivesAdded if not passive == "KiEmpoweredStrikes"],
            self._awareness,
            self._ki_empowered_strikes,
        ]

    @progression(CharacterClass.MONK_OPENHAND, 6)
    def level_6_open_hand(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._wholeness_of_body]
        progression.Selectors = None

    @progression(CharacterClass.MONK, 7)
    def level_7_monk(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            *[passive for passive in progression.PassivesAdded if not passive == "StillnessOfMind"],
            self._stillness_of_mind,
        ]

    @progression(CharacterClass.MONK, 8)
    def level_8(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = progression.PassivesAdded + ["Indomitable"]

    @progression(CharacterClass.MONK, 10)
    def level_10(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack_2"]
        progression.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.MONK, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ReliableTalent"]

    @progression(CharacterClass.MONK, 13)
    def level_13(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 14)
    def level_14(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 15)
    def level_15(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 16)
    def level_16(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 17)
    def level_17(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 18)
    def level_18(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 19)
    def level_19(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.MONK, 20)
    def level_20(self, progression: Progression) -> None:
        progression.PassivesAdded = progression.PassivesAdded + ["ExtraAttack_3"]
        progression.PassivesRemoved = ["ExtraAttack_2"]


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="Monk expansion.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Ki) multiplier (defaulting to 2x)")
    parser.add_argument("-k", "--skills", type=int, default=6,
                        help="Number of skills to select at character creation (defaulting to 6)")
    parser.add_argument("-e", "--expertise", type=int, default=2,
                        help="Number of skills with expertise to select at character creation (defaulting to 2)")
    args = MonkExpanded.Args(**vars(parser.parse_args()))

    monk_expanded = MonkExpanded(args)
    monk_expanded.build()


if __name__ == "__main__":
    main()
