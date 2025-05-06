#!/usr/bin/env python3
"""
Generates files for the "EldritchKnightFullCaster" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import EmpoweredSpells, Movement
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import (
    CharacterAbility,
    CharacterClass,
    ClassDescription,
    Progression,
)
from modtools.replacers import (
    class_description,
    DontIncludeProgression,
    only_existing_progressions,
    progression,
    Replacer,
    eldritch_knight_cantrips,
    eldritch_knight_level_1_spells,
    eldritch_knight_level_2_spells,
    wizard_cantrips,
    wizard_level_1_spells,
    wizard_level_2_spells,
    wizard_level_3_spells,
    wizard_level_4_spells,
    wizard_level_5_spells,
    wizard_level_6_spells,
)


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class EldritchKnightFullCaster(Replacer):
    @dataclass
    class Args:
        spells: int  # Multiplier for spell slots

    _args: Args
    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="EldritchKnightFullCaster",
                         description="Full casting for the Eldritch Knight subclass.")
        self._args = args

    @class_description(CharacterClass.FIGHTER_ELDRITCHKNIGHT)
    def eldritch_knight_description(self, class_description: ClassDescription) -> None:
        class_description.MulticlassSpellcasterModifier = 1.0

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, range(3, 21))
    @only_existing_progressions
    def level_3_to_20(self, progression: Progression) -> None:
        progression.Boosts = [
            boost for boost in (progression.Boosts or []) if not boost.startswith("ActionResource(SpellSlot,")
        ] or None
        progression.PassivesAdded = [
            passive for passive in (progression.PassivesAdded or []) if not passive.startswith("UnlockedSpellSlotLevel")
        ] or None
        progression.Selectors = [
            selector for selector in (progression.Selectors or [])
            if not selector.startswith(f"SelectSpells({eldritch_knight_cantrips(self).UUID}")
            and not selector.startswith(f"SelectSpells({eldritch_knight_level_1_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({eldritch_knight_level_2_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_cantrips(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_1_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_2_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_3_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_4_spells(self).UUID}")
        ] or None

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{4 * self._args.spells},1)",
            f"ActionResource(SpellSlot,{2 * self._args.spells},2)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "DevilsSight",
            "SculptSpells",
            "UnlockedSpellSlotLevel1",
            "UnlockedSpellSlotLevel2",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},4,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},4,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},2)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_2_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{2 * self._args.spells},3)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "UnlockedSpellSlotLevel3",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_3_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},3)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_3_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_5_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_5_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 13)
    def level_13(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},7)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 14)
    def level_14(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 15)
    def level_15(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},8)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 16)
    def level_16(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 17)
    def level_17(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},9)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 18)
    def level_18(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 19)
    def level_19(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 20)
    def level_20(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},7)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="Full casting for the Fighter Eldritch Knight subclass.")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (default 2; double spell slots)")
    args = EldritchKnightFullCaster.Args(**vars(parser.parse_args()))

    eldritch_knight_full_caster = EldritchKnightFullCaster(args)
    eldritch_knight_full_caster.build()


if __name__ == "__main__":
    main()
