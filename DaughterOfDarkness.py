#!/usr/bin/env python3
"""
Generates files for the "DaughterOfDarkness" mod.
"""

import argparse
import os

from dataclasses import dataclass
from moddb.battlemagic import BattleMagic
from moddb.empoweredspells import EmpoweredSpells
from moddb.movement import Movement
from moddb.progression import multiply_resources
from moddb.stormbolt import storm_bolt
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    ClassDescription,
    Origin,
    SpellList,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    class_description,
    origin,
    progression,
    Replacer,
    spell_list,
)


class DaughterOfDarkness(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Channel Divinity charges)

    _args: Args
    _feat_levels: set[int]

    # Passives
    _battle_magic: str
    _empowered_spells: str
    _fast_movement: str

    # Spells
    _storm_bolt: str

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="DaughterOfDarkness",
                         description="Changes Shadowheart to a Tempest Cleric.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        # Passives
        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)
        self._fast_movement = Movement(self.mod).add_fast_movement(3.0)

        # Spells
        self._storm_bolt = storm_bolt(self.mod)

    @origin("Shadowheart")
    def shadowheart(self, origin: Origin) -> None:
        origin.SubClassUUID = "89bacf1b-8f15-4972-ada7-bf59c7c78441"  # Tempest Domain

    @class_description(CharacterClass.CLERIC)
    def cleric_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True

    @spell_list("Cleric Tempest Domain 1")
    def level_1_tempest_spell_list(self, spell_list: SpellList) -> None:
        spell_list.Spells.append(self._storm_bolt)

    @spell_list("Cleric Tempest Domain 5")
    def level_5_tempest_spell_list(self, spell_list: SpellList) -> None:
        spell_list.Spells.append("Target_Counterspell")

    @progression(CharacterClass.CLERIC, range(1, 13))
    def level_1_to_12_cleric(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression, [ActionResource.CHANNEL_DIVINITY_CHARGES], self._args.actions)

    @progression(CharacterClass.CLERIC_TEMPEST, 1)
    def level_1(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._battle_magic, "SculptSpells"]

    @progression(CharacterClass.CLERIC_TEMPEST, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._fast_movement]

    @progression(CharacterClass.CLERIC_TEMPEST, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack"]

    @progression(CharacterClass.CLERIC_TEMPEST, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]

    @progression(CharacterClass.CLERIC_TEMPEST, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._empowered_spells]

    @progression(CharacterClass.CLERIC_TEMPEST, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
        ]


def main():
    parser = argparse.ArgumentParser(description="A replacer for Shadowheart, and Tempest Domain Clerics.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=1,
                        help="Feat progression every n levels (defaulting to 1; feat every level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=4,
                        help="Spell slot multiplier (defaulting to 4; quadruple spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=4,
                        help="Action resource (Channel Divinity) multiplier (defaulting to 4; quadruple charges)")
    args = DaughterOfDarkness.Args(**vars(parser.parse_args()))

    daughter_of_darkness = DaughterOfDarkness(args)
    daughter_of_darkness.build()


if __name__ == "__main__":
    main()
