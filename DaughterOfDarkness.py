#!/usr/bin/env python3
"""
Generates files for the "DaughterOfDarkness" mod.
"""

import os

from functools import cached_property
from moddb.battlemagic import BattleMagic
from moddb.empoweredspells import EmpoweredSpells
from moddb.movement import Movement
from moddb.progression import multiply_resources
from moddb.witchbolt import witch_bolt_to_cantrip
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
)


class DaughterOfDarkness(Replacer):
    _battle_magic: str
    _empowered_spells: str
    _fast_movement: str

    @cached_property
    def _level_1_spelllist(self) -> str:
        spelllist = str(self.make_uuid("level_1_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Tempest Domain Cleric level 1",
            Spells=["Projectile_WitchBolt"],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_5_spelllist(self) -> str:
        spelllist = str(self.make_uuid("level_5_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Tempest Domain Cleric level 5",
            Spells=["Target_Counterspell"],
            UUID=spelllist,
        ))
        return spelllist

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="DaughterOfDarkness",
                         description="Changes Shadowheart to a Tempest Cleric.")

        # Passives
        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)
        self._fast_movement = Movement(self.mod).add_fast_movement(3.0)

        # Spells
        witch_bolt_to_cantrip(self.mod)

    @origin("Shadowheart")
    def shadowheart(self, origin: Origin) -> None:
        origin.SubClassUUID = "89bacf1b-8f15-4972-ada7-bf59c7c78441"  # Tempest Domain

    @class_description(CharacterClass.CLERIC)
    def druid_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True

    @progression(CharacterClass.CLERIC, range(1, 13))
    def level_1_to_12_cleric(self, progression: Progression) -> None:
        progression.AllowImprovement = True if (progression.Level % 2) == 0 else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS, ActionResource.CHANNEL_DIVINITY_CHARGES], 2)

    @progression(CharacterClass.CLERIC_TEMPEST, 1)
    def level_1(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._battle_magic, "SculptSpells"]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_1_spelllist},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_TEMPEST, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._fast_movement]

    @progression(CharacterClass.CLERIC_TEMPEST, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack"]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_5_spelllist},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_TEMPEST, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]

    @progression(CharacterClass.CLERIC_TEMPEST, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._empowered_spells]

    @progression(CharacterClass.CLERIC_TEMPEST, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]


def main():
    daughter_of_darkness = DaughterOfDarkness()
    daughter_of_darkness.build()


if __name__ == "__main__":
    main()
