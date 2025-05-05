#!/usr/bin/env python3
"""
Generates files for the "WarlockExtended" mod.
"""

import argparse
import os
import re

from dataclasses import dataclass
from functools import cache, cached_property
from moddb import (
    BattleMagic,
    Bolster,
    PackMule,
    multiply_resources,
)
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    SpellList,
)
from modtools.lsx.game import Dependencies, Progression
from modtools.replacers import (
    Replacer,
    progression,
    spell_list,
    warlock_archfey_level_1_spells,
    warlock_archfey_level_2_spells,
    warlock_archfey_level_3_spells,
    warlock_archfey_level_4_spells,
    warlock_archfey_level_5_spells,
    warlock_fiend_level_1_spells,
    warlock_fiend_level_2_spells,
    warlock_fiend_level_3_spells,
    warlock_fiend_level_4_spells,
    warlock_fiend_level_5_spells,
    warlock_greatoldone_level_1_spells,
    warlock_greatoldone_level_2_spells,
    warlock_greatoldone_level_3_spells,
    warlock_greatoldone_level_4_spells,
    warlock_greatoldone_level_5_spells,
    warlock_hexblade_level_1_spells,
    warlock_hexblade_level_2_spells,
    warlock_hexblade_level_3_spells,
    warlock_hexblade_level_4_spells,
    warlock_hexblade_level_5_spells,
)


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class WarlockExtended(Replacer):
    @dataclass
    class Args:
        feats: int      # Feats every n levels
        spells: int     # Multiplier for spell slots
        skills: int     # Number of skills to select at character creation
        expertise: int  # Number of skills with expertise to select at character creation

    _REQ_ARG = r"(?:,([^,)]+))"
    _OPT_ARG = r"(?:,([^,)]*))?"
    _SELECT_SPELLS = re.compile(r"SelectSpells\(([^,)]+)" + _OPT_ARG * 4 + _REQ_ARG + r"\)")

    _args: Args
    _feat_levels: set[int]

    _battle_magic: str
    _bolster: str
    _pack_mule: str

    @cached_property
    def _archfey_spells(self) -> list[list[str]]:
        return [
            warlock_archfey_level_1_spells(self).Spells,
            warlock_archfey_level_2_spells(self).Spells,
            warlock_archfey_level_3_spells(self).Spells,
            warlock_archfey_level_4_spells(self).Spells,
            warlock_archfey_level_5_spells(self).Spells,
        ]

    @cached_property
    def _fiend_spells(self) -> list[list[str]]:
        return [
            warlock_fiend_level_1_spells(self).Spells,
            warlock_fiend_level_2_spells(self).Spells,
            warlock_fiend_level_3_spells(self).Spells,
            warlock_fiend_level_4_spells(self).Spells,
            warlock_fiend_level_5_spells(self).Spells,
        ]

    @cached_property
    def _greatoldone_spells(self) -> list[list[str]]:
        return [
            warlock_greatoldone_level_1_spells(self).Spells,
            warlock_greatoldone_level_2_spells(self).Spells,
            warlock_greatoldone_level_3_spells(self).Spells,
            warlock_greatoldone_level_4_spells(self).Spells,
            warlock_greatoldone_level_5_spells(self).Spells,
        ]

    @cached_property
    def _hexblade_spells(self) -> list[list[str]]:
        return [
            warlock_hexblade_level_1_spells(self).Spells,
            warlock_hexblade_level_2_spells(self).Spells,
            warlock_hexblade_level_3_spells(self).Spells,
            warlock_hexblade_level_4_spells(self).Spells,
            warlock_hexblade_level_5_spells(self).Spells,
        ]

    @cache
    def _merge_spells(self, level: int) -> list[str]:
        if level == 0:
            return []
        previous_spells = self._merge_spells(level - 1)
        current_set = set(self._archfey_spells[level - 1] +
                          self._fiend_spells[level - 1] +
                          self._greatoldone_spells[level - 1] +
                          self._hexblade_spells[level - 1])
        current_spells = list(current_set - set(previous_spells))
        current_sorted = sorted(current_spells, key=lambda key: key[key.index("_"):])
        return current_sorted + previous_spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="WarlockExtended",
                         description="Warlock enhancements.")

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
        self._bolster = Bolster(self.mod).add_bolster_spell_list()
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)

    @spell_list("Warlock Archfey SLevel 1")
    def archfey_level_1_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(1)

    @spell_list("Warlock Archfey SLevel 2")
    def archfey_level_2_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(2)

    @spell_list("Warlock Archfey SLevel 3")
    def archfey_level_3_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(3)

    @spell_list("Warlock Archfey SLevel 4")
    def archfey_level_4_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(4)

    @spell_list("Warlock Archfey SLevel 5")
    def archfey_level_5_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(5)

    @spell_list("Warlock Fiend SLevel 1")
    def fiend_level_1_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(1)

    @spell_list("Warlock Fiend SLevel 2")
    def fiend_level_2_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(2)

    @spell_list("Warlock Fiend SLevel 3")
    def fiend_level_3_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(3)

    @spell_list("Warlock Fiend SLevel 4")
    def fiend_level_4_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(4)

    @spell_list("Warlock Fiend SLevel 5")
    def fiend_level_5_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(5)

    @spell_list("Warlock The Great Old One SLevel 1")
    def greatoldone_level_1_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(1)

    @spell_list("Warlock The Great Old One SLevel 2")
    def greatoldone_level_2_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(2)

    @spell_list("Warlock The Great Old One SLevel 3")
    def greatoldone_level_3_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(3)

    @spell_list("Warlock The Great Old One SLevel 4")
    def greatoldone_level_4_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(4)

    @spell_list("Warlock The Great Old One SLevel 5")
    def greatoldone_level_5_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(5)

    @spell_list("Warlock Hexblade SLevel 1")
    def hexblade_level_1_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(1)

    @spell_list("Warlock Hexblade SLevel 2")
    def hexblade_level_2_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(2)

    @spell_list("Warlock Hexblade SLevel 3")
    def hexblade_level_3_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(3)

    @spell_list("Warlock Hexblade SLevel 4")
    def hexblade_level_4_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(4)

    @spell_list("Warlock Hexblade SLevel 5")
    def hexblade_level_5_spells(self, spells: SpellList) -> None:
        spells.Spells = self._merge_spells(5)

    @progression(CharacterClass.WARLOCK, range(1, 21))
    @progression(CharacterClass.WARLOCK, 1, is_multiclass=True)
    def level_1_to_20_warlock(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.WARLOCK_SPELL_SLOTS], self._args.spells)

    @progression(CharacterClass.WARLOCK, 1, is_multiclass=False)
    def increase_skills(self, progression: Progression) -> None:
        selectors = progression.Selectors
        if self._args.skills is not None:
            selectors = [selector for selector in (selectors or []) if not selector.startswith("SelectSkills(")]
            selectors.append(f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self._args.skills})")
        if self._args.expertise is not None:
            selectors = [selector for selector in selectors if not selector.startswith("SelectSkillsExpertise(")]
            selectors.append(f"SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self._args.expertise})")
        progression.Selectors = selectors

    @progression(CharacterClass.WARLOCK, 1)
    def warlock_level_1(self, progression: Progression) -> None:
        progression.Boosts += ["ProficiencyBonus(SavingThrow,Constitution)"]
        progression.PassivesAdded += [self._battle_magic, self._pack_mule]
        progression.Selectors += [f"AddSpells({self._bolster})"]


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="Warlock enhancements.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 17), default=8,
                        help="Spell slot multiplier (default 8)")
    parser.add_argument("-k", "--skills", type=int, default=9,
                        help="Number of skills to select at character creation (default 9)")
    parser.add_argument("-e", "--expertise", type=int, default=3,
                        help="Number of skills with expertise to select at character creation (default 3)")
    args = WarlockExtended.Args(**vars(parser.parse_args()))

    warlock_extended = WarlockExtended(args)
    warlock_extended.build()


if __name__ == "__main__":
    main()
