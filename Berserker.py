#!/usr/bin/env python3
"""
Generates files for the "Berserker" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import Attack, Movement
from modtools.gamedata import PassiveData
from modtools.lsx.game import CharacterClass, Progression, SpellList
from modtools.replacers import progression, DontIncludeProgression, Replacer


class Berserker(Replacer):
    @dataclass
    class Args:
        feats: set[int]  # Feat improvement levels
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
    def _wolverine(self) -> str:
        """Return the Wolverine passive's name."""
        name = f"{self.mod.get_prefix()}_Wolverine"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Wolverine"}
        loca[f"{name}_Description"] = {"en": """
            While raging, you regenerate [1] every turn.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["RegainHitPoints(1d4)"],
            Icon="PassiveFeature_AspectOfTheBeast_Wolverine",
            Properties=["Highlighted", "OncePerTurn"],
            Boosts=[
                "IF(HasStatus('RAGE_FRENZY') and not HasStatus('DOWNED') and not Dead()):RegainHitPoints(1d4)",
            ],
        ))

        return name

    @cached_property
    def _level_3_spell_list(self) -> SpellList:
        spells = SpellList(
            Comment="Berserker level 3 abilities",
            Spells=[
                Attack(self.mod).add_brutal_cleave(),
            ],
            UUID=self.make_uuid("Berserker level 3 abilities"),
        )
        self.mod.add(spells)
        return spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Berserker",
                         description="Enhancements for the Berserker subclass.")

        self._args = args

        if len(args.feats) == 0:
            self._feat_levels = frozenset(range(2, 13, 2))
        elif len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            self._feat_levels = frozenset(range(max(feat_level, 2), 13, feat_level))
        else:
            self._feat_levels = args.feats - frozenset([1])

    @progression(CharacterClass.BARBARIAN, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Selectors = [
            *[selector for selector in progression.Selectors if not selector.startswith("SelectSkills")],
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.BARBARIAN, range(2, 13))
    def level_2_to_12_fighter(self, progression: Progression) -> None:
        previous_improvement = progression.AllowImprovement or None
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        if progression.AllowImprovement == previous_improvement:
            raise DontIncludeProgression

    @progression(CharacterClass.BARBARIAN_BERSERKER, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "FastHands",
            self._remarkable_athlete_run,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_3_spell_list.UUID})",
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ImprovedCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "UncannyDodge",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "RemarkableAthlete_Jump",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Evasion",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_Advantage",
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._wolverine,
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 12)
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
    parser = argparse.ArgumentParser(description="Enhancements for the Berserker subclass.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource multiplier (defaulting to 2; double resources)")
    args = Berserker.Args(**vars(parser.parse_args()))

    berserker = Berserker(args)
    berserker.build()


if __name__ == "__main__":
    main()
