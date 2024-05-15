#!/usr/bin/env python3
"""
Generates files for the "RangerReloaded" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    Movement,
    multiply_resources,
    spells_always_prepared,
)
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    ClassDescription,
    SpellList,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    class_description,
    druid_cantrips,
    druid_level_1_spells,
    druid_level_2_spells,
    druid_level_3_spells,
    druid_level_4_spells,
    druid_level_5_spells,
    druid_level_6_spells,
    progression,
    ranger_level_1_spells,
    ranger_level_2_spells,
    ranger_level_3_spells,
    Replacer,
)


class RangerReloaded(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots

    _args: Args
    _feat_levels: set[int]

    # Passives
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str

    # Spells
    _misty_step: str

    @cached_property
    def _cantrips(self) -> SpellList:
        cantrips = SpellList(
            Comment="Ranger cantrips",
            Spells=sorted(set(druid_cantrips(self).Spells)),
            UUID=self.make_uuid("cantrips"),
        )
        self.mod.add(cantrips)
        return cantrips

    @cached_property
    def _level_1_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Ranger level 1 spells",
            Spells=sorted(set([
                *druid_level_1_spells(self).Spells,
                *ranger_level_1_spells(self).Spells,
                "Shout_Shield_Wizard",
            ])),
            UUID=self.make_uuid("level_1_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_2_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Ranger level 2 spells",
            Spells=sorted(set([
                *druid_level_2_spells(self).Spells,
                *ranger_level_2_spells(self).Spells,
            ]) - set([
                *ranger_level_1_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_2_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_3_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Ranger level 3 spells",
            Spells=sorted(set([
                *druid_level_3_spells(self).Spells,
                *ranger_level_3_spells(self).Spells,
                "Target_Counterspell",
            ]) - set([
                *ranger_level_2_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_3_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_4_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Ranger level 4 spells",
            Spells=sorted(set(druid_level_4_spells(self).Spells)),
            UUID=self.make_uuid("level_4_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_5_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Ranger level 5 spells",
            Spells=sorted(set(druid_level_5_spells(self).Spells)),
            UUID=self.make_uuid("level_5_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_6_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Ranger level 6 spells",
            Spells=sorted(set(druid_level_6_spells(self).Spells)),
            UUID=self.make_uuid("level_6_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _misty_step_spell_list(self) -> SpellList:
        spells = SpellList(
            Comment="Hunter misty step",
            Spells=[self._misty_step],
            UUID=self.make_uuid(self._misty_step),
        )
        self.mod.add(spells)
        return spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="RangerReloaded",
                         description="Enhancements for the Ranger class.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        movement = Movement(self.mod)

        # Passives
        self._fast_movement_30 = movement.add_fast_movement(3.0)
        self._fast_movement_45 = movement.add_fast_movement(4.5)
        self._fast_movement_60 = movement.add_fast_movement(6.0)

        # Spells
        self._misty_step = movement.add_misty_step()

    @class_description(CharacterClass.RANGER)
    @class_description(CharacterClass.RANGER_BEASTMASTER)
    @class_description(CharacterClass.RANGER_GLOOMSTALKER)
    @class_description(CharacterClass.RANGER_HUNTER)
    def ranger_description(self, class_description: ClassDescription) -> None:
        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.MustPrepareSpells = True

    @progression(CharacterClass.RANGER, range(1, 13))
    @progression(CharacterClass.RANGER, 1, is_multiclass=True)
    def level_1_to_12_ranger(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        spells_always_prepared(progression)
        progression.Boosts = [
            boost for boost in (progression.Boosts or []) if not boost.startswith("ActionResource(SpellSlot,")
        ]
        progression.Selectors = [
            selector for selector in (progression.Selectors or [])
            if not selector.startswith(f"SelectSpells({ranger_level_1_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({ranger_level_2_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({ranger_level_3_spells(self).UUID}")
        ] or None

    @progression(CharacterClass.RANGER, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts += (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{2 * self._args.spells},1)",
            "ProficiencyBonus(SavingThrow,Constitution)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_30,
            "UnlockedSpellSlotLevel1",
        ]
        progression.Selectors = [
            *[selector for selector in progression.Selectors if not selector.startswith("SelectSkills")],
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            f"SelectSpells({self._cantrips.UUID},2,0,,,,AlwaysPrepared)",
            f"SelectSpells({self._cantrips.UUID},2,0,,,,AlwaysPrepared)",
            f"AddSpells({self._level_1_spells.UUID})",
        ]

    @progression(CharacterClass.RANGER, 1, is_multiclass=True)
    def level_1_multiclass(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_30,
            "UnlockedSpellSlotLevel1",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self._cantrips.UUID},2,0,,,,AlwaysPrepared)",
            f"AddSpells({self._level_1_spells.UUID})",
        ]

    @progression(CharacterClass.RANGER, 2)
    def level_2(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},1)",
        ]
        progression.PassivesAdded = [
            passive for passive in progression.PassivesAdded if passive != "UnlockedSpellSlotLevel1"
        ] or None

    @progression(CharacterClass.RANGER, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},1)",
            f"ActionResource(SpellSlot,{2 * self._args.spells},2)",
        ]
        progression.PassivesAdded = [
            passive for passive in progression.PassivesAdded if passive != "UnlockedSpellSlotLevel1"
        ] + [
            "UnlockedSpellSlotLevel2",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_2_spells.UUID})",
        ]

    @progression(CharacterClass.RANGER, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},2)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self._cantrips.UUID},1,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.RANGER, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{2 * self._args.spells},3)",
        ]
        progression.PassivesAdded = [
            passive for passive in progression.PassivesAdded if passive != "UnlockedSpellSlotLevel2"
        ] + [
            self._fast_movement_45,
            "UnlockedSpellSlotLevel3",
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_30,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_3_spells.UUID})",
        ]

    @progression(CharacterClass.RANGER, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},3)",
        ]

    @progression(CharacterClass.RANGER, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]
        progression.PassivesAdded = [
            passive for passive in progression.PassivesAdded if passive != "UnlockedSpellSlotLevel2"
        ] or None
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_4_spells.UUID})",
        ]

    @progression(CharacterClass.RANGER, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]

    @progression(CharacterClass.RANGER, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.PassivesAdded = [
            passive for passive in progression.PassivesAdded if passive != "UnlockedSpellSlotLevel3"
        ] + [
            self._fast_movement_60,
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_45,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_5_spells.UUID})",
        ]

    @progression(CharacterClass.RANGER, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self._cantrips.UUID},1,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.RANGER, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_6_spells.UUID})",
        ]

    @progression(CharacterClass.RANGER, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 3)
    def level_3_hunter(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            "ColossusSlayer",
            "GiantKiller",
            "HordeBreaker",
        ]
        progression.Selectors = None

    @progression(CharacterClass.RANGER_HUNTER, 5)
    def level_5_hunter(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ImprovedCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._misty_step_spell_list.UUID},,,,AlwaysPrepared)",
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 7)
    def level_7_hunter(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            "EscapeTheHorde",
            "SteelWill",
            "MultiattackDefense",
        ]
        progression.Selectors = None

    @progression(CharacterClass.RANGER_HUNTER, 9)
    def level_9_hunter(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "BrutalCritical",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 11)
    def level_11_hunter(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ExtraAttack_2",
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            "ExtraAttack",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 12)
    def level_12_hunter(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ReliableTalent",
        ]


def main():
    parser = argparse.ArgumentParser(description="Enhancements for the Ranger class.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=2,
                        help="Feat progression every n levels (defaulting to 2; feat every other level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    args = RangerReloaded.Args(**vars(parser.parse_args()))

    ranger_reloaded = RangerReloaded(args)
    ranger_reloaded.build()


if __name__ == "__main__":
    main()
