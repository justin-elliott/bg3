#!/usr/bin/env python3
"""
Generates files for the "HolyWarrior" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    Movement,
    multiply_resources,
)
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    SpellList,
)
from modtools.lsx.game import Progression
from modtools.replacers import Replacer, progression


class HolyWarrior(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Channel Divinity, War Priest charges)

    _args: Args
    _feat_levels: set[int]

    # Passives
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str

    @cached_property
    def _counterspell(self) -> SpellList:
        spells = SpellList(
            Comment="War Domain Cleric Counterspell",
            Spells=["Target_Counterspell"],
            UUID=self.make_uuid("Counterspell"),
        )
        self.mod.add(spells)
        return spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="HolyWarrior",
                         description="Boosts War Domain Cleric.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        # Passives
        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(4.5)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(6.0)

    @progression(CharacterClass.CLERIC, range(1, 13))
    @progression(CharacterClass.CLERIC, 1, is_multiclass=True)
    def level_1_to_12_cleric(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression,
                           [ActionResource.CHANNEL_DIVINITY_CHARGES,
                            ActionResource.WAR_PRIEST_CHARGES],
                           self._args.actions)

    @progression(CharacterClass.CLERIC_WAR, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ProficiencyBonus(SavingThrow,Constitution)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_30,
        ]

    @progression(CharacterClass.CLERIC_WAR, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Smite_Divine",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(58aef51d-a46c-44c8-8bed-df90870eb55f,,,,AlwaysPrepared)",  # Smite
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]

    @progression(CharacterClass.CLERIC_WAR, 3)
    def level_3(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.CLERIC_WAR, 4)
    def level_4(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.CLERIC_WAR, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_45,
            "ExtraAttack",
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_30,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._counterspell.UUID},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_WAR, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ImprovedCritical",
        ]

    @progression(CharacterClass.CLERIC_WAR, 7)
    def level_7(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.CLERIC_WAR, 8)
    def level_8(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.CLERIC_WAR, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_60,
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_45,
        ]

    @progression(CharacterClass.CLERIC_WAR, 10)
    def level_10(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.CLERIC_WAR, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a,,,,AlwaysPrepared)",  # Volley, Whirlwind
        ]

    @progression(CharacterClass.CLERIC_WAR, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "BrutalCritical",
        ]


def main():
    parser = argparse.ArgumentParser(description="Boosts War Domain Cleric.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=1,
                        help="Feat progression every n levels (defaulting to 1; feat every level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Channel Divinity, War Priest charges) multiplier"
                             " (defaulting to 2; double charges)")
    args = HolyWarrior.Args(**vars(parser.parse_args()))

    holy_warrior = HolyWarrior(args)
    holy_warrior.build()


if __name__ == "__main__":
    main()
