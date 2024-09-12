#!/usr/bin/env python3
"""
Generates files for the "UndisputedChampion" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import Attack, Movement
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import CharacterClass, Progression, SpellList
from modtools.replacers import progression, DontIncludeProgression, Replacer


class UndisputedChampion(Replacer):
    @dataclass
    class Args:
        feats: set[int]  # Feat improvement levels
        spells: int      # Multiplier for spell slots
        actions: int     # Multiplier for other action resources

    _args: Args
    _feat_levels: set[int]

    @cached_property
    def _remarkable_athlete_run(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_RemarkableAthlete_Run"
        loca[name] = {"en": "Remarkable Athlete: Run"}
        return Movement(self.mod).add_fast_movement(3.0, loca[name])

    @cached_property
    def _precise_attacks(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_PreciseAttacks"

        loca[f"{name}_DisplayName"] = {"en": "Precise Attacks"}
        loca[f"{name}_Description"] = {"en": """
            When you make a melee attack, your Strength <LSTag Tooltip="AbilityModifier">Modifier</LSTag> is added
            twice to the <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="Action_PrecisionAttack",
            Properties=["Highlighted"],
            Boosts=[
                "IF(IsMeleeAttack()):RollBonus(Attack,StrengthModifier)",
            ],
        ))

        return name

    @cached_property
    def _mighty_throw_spell(self) -> str:
        loca = self.mod.get_localization()

        name = f"{self._mod.get_prefix()}_MightyThrow"
        loca[name] = {"en": "Mighty Throw"}

        self.mod.add(SpellData(
            name,
            using="Throw_FrenziedThrow",
            SpellType="Throw",
            DisplayName=loca[name],
            RequirementConditions=[],
        ))

        return name

    @cached_property
    def _level_3_spell_list(self) -> SpellList:
        spells = SpellList(
            Comment="Champion level 3 abilities",
            Spells=[
                Attack(self.mod).add_brutal_cleave(),
                self._mighty_throw_spell,
            ],
            UUID=self.make_uuid("Champion level 3 abilities"),
        )
        self.mod.add(spells)
        return spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="UndisputedChampion",
                         description="Enhancements for the Champion subclass.")

        self._args = args

        if len(args.feats) == 0:
            self._feat_levels = frozenset([2, 3, 4, 5, 6, 8, 10, 12])
        elif len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            self._feat_levels = frozenset(range(max(feat_level, 2), 13, feat_level))
        else:
            self._feat_levels = args.feats - frozenset([1])

    @progression(CharacterClass.FIGHTER, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Selectors = [
            *[selector for selector in progression.Selectors if not selector.startswith("SelectSkills")],
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.FIGHTER, range(2, 13))
    def level_2_to_12_fighter(self, progression: Progression) -> None:
        previous_improvement = progression.AllowImprovement or None
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        if progression.AllowImprovement == previous_improvement:
            raise DontIncludeProgression

    @progression(CharacterClass.FIGHTER_CHAMPION, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._remarkable_athlete_run,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_3_spell_list.UUID})",
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "FeralInstinct",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "UncannyDodge",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._precise_attacks,
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Evasion",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "BrutalCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ReliableTalent",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 12))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="Enhancements for the Ranger class.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource multiplier (defaulting to 2; double resources)")
    args = UndisputedChampion.Args(**vars(parser.parse_args()))

    undisputed_champion = UndisputedChampion(args)
    undisputed_champion.build()


if __name__ == "__main__":
    main()
