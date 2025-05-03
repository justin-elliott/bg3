#!/usr/bin/env python3
"""
Generates files for the "HexbladeExtended" mod.
"""

import argparse
import os
import re

from dataclasses import dataclass
from functools import cache, cached_property
from moddb import (
    BattleMagic,
    Bolster,
    EmpoweredSpells,
    multiply_resources,
    PackMule,
    spells_always_prepared,
)
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    ClassDescription,
    SpellList,
)
from modtools.lsx.game import Dependencies, Progression
from modtools.replacers import (
    Replacer,
    class_description,
    only_existing_progressions,
    progression,
)
from uuid import UUID


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class HexbladeExtended(Replacer):
    @dataclass
    class Args:
        feats: int   # Feats every n levels
        spells: int  # Multiplier for spell slots

    _REQ_ARG = r"(?:,([^,)]+))"
    _OPT_ARG = r"(?:,([^,)]*))?"
    _SELECT_SPELLS = re.compile(r"SelectSpells\(([^,)]+)" + _OPT_ARG * 4 + _REQ_ARG + r"\)")

    _args: Args
    _feat_levels: set[int]

    # Passives
    _battle_magic: str
    _empowered_spells: str
    _pack_mule: str

    # Spells
    _bolster: str

    def _select_to_add_spells(self, progression: Progression) -> bool:
        """Change spell selection to adding the entire spell list."""
        was_updated = False

        if progression.Selectors:
            selectors = []
            for selector in progression.Selectors:
                if match := self._SELECT_SPELLS.match(selector):
                    args = match.groups("")
                    selector = f"AddSpells({args[0]})"
                    was_updated = True
                if progression.Level % 2 == 1 and progression.Level < 10:
                    selectors.append(selector)
            progression.Selectors = selectors or None

        return was_updated

    @cached_property
    def _level_1_spells_always_prepared(self) -> str:
        spell_list = str(self.make_uuid("level_1_spells_always_prepared"))
        self.mod.add(SpellList(
            Comment="Hexblade Extended level 1 spells that are always prepared",
            Spells=[self._bolster],
            UUID=spell_list,
        ))
        return spell_list

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="HexbladeExtended",
                         description="Enhancements for the Warlock Hexblade subclass.")

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

        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.CHARISMA)
        self._bolster = Bolster(self.mod).add_bolster()
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)

    @class_description(CharacterClass.WARLOCK)
    @class_description(CharacterClass.WARLOCK_HEXBLADE)
    @class_description(CharacterClass.WARLOCK_ARCHFEY)
    @class_description(CharacterClass.WARLOCK_FIEND)
    @class_description(CharacterClass.WARLOCK_GREATOLDONE)
    def warlock_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6
        class_description.CanLearnSpells = True
        class_description.MustPrepareSpells = True

    @progression(CharacterClass.WARLOCK, range(1, 21))
    @progression(CharacterClass.WARLOCK, 1, is_multiclass=True)
    def level_1_to_20_warlock(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.WARLOCK_SPELL_SLOTS], self._args.spells)

    @progression(CharacterClass.WARLOCK, range(1, 21))
    @progression(CharacterClass.WARLOCK_HEXBLADE, range(1, 21))
    @progression(CharacterClass.WARLOCK_ARCHFEY, range(1, 21))
    @progression(CharacterClass.WARLOCK_FIEND, range(1, 21))
    @progression(CharacterClass.WARLOCK_GREATOLDONE, range(1, 21))
    @progression(CharacterClass.WARLOCK, 1, is_multiclass=True)
    @only_existing_progressions
    def level_1_to_20_prepared(self, progression: Progression) -> None:
        spells_always_prepared(progression)

    @progression(CharacterClass.WARLOCK, range(1, 21))
    @progression(CharacterClass.WARLOCK_HEXBLADE, range(1, 21))
    @progression(CharacterClass.WARLOCK_ARCHFEY, range(1, 21))
    @progression(CharacterClass.WARLOCK_FIEND, range(1, 21))
    @progression(CharacterClass.WARLOCK_GREATOLDONE, range(1, 21))
    @progression(CharacterClass.WARLOCK, 1, is_multiclass=True)
    @only_existing_progressions
    def level_1_to_20_select_to_add(self, progression: Progression) -> None:
        self._select_to_add_spells(progression)

    @progression(CharacterClass.WARLOCK_HEXBLADE, 1)
    def level_1(self, progression: Progression) -> None:
        progression.PassivesAdded = progression.PassivesAdded + [
            self._battle_magic,
            self._pack_mule,
        ]
        progression.Selectors = progression.Selectors + [
            f"AddSpells({self._level_1_spells_always_prepared},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = ["SculptSpells"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 3)
    def level_3(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 4)
    def level_4(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 5)
    def level_5(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 6)
    def level_6(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 7)
    def level_7(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 8)
    def level_8(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._empowered_spells]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 10)
    def level_10(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 11)
    def level_11(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 12)
    def level_12(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 13)
    def level_13(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 14)
    def level_14(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 15)
    def level_15(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 16)
    def level_16(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 17)
    def level_17(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 18)
    def level_18(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 19)
    def level_19(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 20)
    def level_20(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK, [11, 13, 15, 17])
    def remove_mystic_arcanum(self, progression: Progression) -> None:
        spell_level = (progression.Level - 11) // 2 + 6
        progression.Boosts = [
            f"ActionResource(WarlockSpellSlot,{3 * self._args.spells},{spell_level})",
            f"ActionResourceOverride(WarlockSpellSlot,0,{spell_level - 1})"
        ]
        progression.Selectors = [
            selector for selector in (progression.Selectors or []) if not selector.startswith("SelectSpells(")
        ] or None


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="Enhancements for the Warlock Hexblade subclass.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 17), default=8,
                        help="Spell slot multiplier (defaulting to 8)")
    args = HexbladeExtended.Args(**vars(parser.parse_args()))

    hexblade_extended = HexbladeExtended(args)
    hexblade_extended.build()


if __name__ == "__main__":
    main()
