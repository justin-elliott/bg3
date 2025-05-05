#!/usr/bin/env python3
"""
Generates files for the "WarlockExtended" mod.
"""

import argparse
import os
import re

from dataclasses import dataclass
from functools import cached_property
from moddb import (
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

    _bolster: str
    _pack_mule: str

    @cached_property
    def _wizard_spells(self) -> list[list[str]]:
        return [
            [spell for spell in wizard_level_1_spells(self).Spells if spell != "Shout_Shield_Wizard"],
            [spell for spell in wizard_level_2_spells(self).Spells if spell != "Shout_Shield_Wizard"],
            [spell for spell in wizard_level_3_spells(self).Spells if spell != "Shout_Shield_Wizard"],
            [spell for spell in wizard_level_4_spells(self).Spells if spell != "Shout_Shield_Wizard"],
            [spell for spell in wizard_level_5_spells(self).Spells if spell != "Shout_Shield_Wizard"],
            [spell for spell in wizard_level_6_spells(self).Spells if spell != "Shout_Shield_Wizard"],
        ]

    @cached_property
    def _archfey_spells(self) -> list[list[str]]:
        return [
            warlock_archfey_level_1_spells(self).Spells,
            warlock_archfey_level_2_spells(self).Spells,
            warlock_archfey_level_3_spells(self).Spells,
            warlock_archfey_level_4_spells(self).Spells,
            warlock_archfey_level_5_spells(self).Spells,
            [],
        ]

    @cached_property
    def _fiend_spells(self) -> list[list[str]]:
        return [
            warlock_fiend_level_1_spells(self).Spells,
            warlock_fiend_level_2_spells(self).Spells,
            warlock_fiend_level_3_spells(self).Spells,
            warlock_fiend_level_4_spells(self).Spells,
            warlock_fiend_level_5_spells(self).Spells,
            [],
        ]

    @cached_property
    def _greatoldone_spells(self) -> list[list[str]]:
        return [
            warlock_greatoldone_level_1_spells(self).Spells,
            warlock_greatoldone_level_2_spells(self).Spells,
            warlock_greatoldone_level_3_spells(self).Spells,
            warlock_greatoldone_level_4_spells(self).Spells,
            warlock_greatoldone_level_5_spells(self).Spells,
            [],
        ]

    @cached_property
    def _hexblade_spells(self) -> list[list[str]]:
        return [
            warlock_hexblade_level_1_spells(self).Spells,
            warlock_hexblade_level_2_spells(self).Spells,
            warlock_hexblade_level_3_spells(self).Spells,
            warlock_hexblade_level_4_spells(self).Spells,
            warlock_hexblade_level_5_spells(self).Spells,
            [],
        ]

    _combined_spells: list[list[str]] = [[], None, None, None, None, None, None]
    
    def _combine_spells(self, level: int, warlock_spells: list[list[str]]) -> list[str]:
        if self._combined_spells[level] is None:
            previous_spells = self._combine_spells(level - 1, warlock_spells)
            current_spells = list(set(warlock_spells[level - 1] + self._wizard_spells[level - 1]) -
                                set(previous_spells))
            current_sorted = sorted(current_spells, key=lambda key: key[key.index("_"):])
            self._combined_spells[level] = current_sorted + previous_spells
        return self._combined_spells[level]

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
        
        self._bolster = Bolster(self.mod).add_bolster_spell_list()
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)

    @spell_list("Warlock Archfey SLevel 1")
    def archfey_level_1_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(1, self._archfey_spells)

    @spell_list("Warlock Archfey SLevel 2")
    def archfey_level_2_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(2, self._archfey_spells)

    @spell_list("Warlock Archfey SLevel 3")
    def archfey_level_3_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(3, self._archfey_spells)

    @spell_list("Warlock Archfey SLevel 4")
    def archfey_level_4_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(4, self._archfey_spells)

    @spell_list("Warlock Archfey SLevel 5")
    def archfey_level_5_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(5, self._archfey_spells)

    @cached_property
    def archfey_level_6_spells(self) -> SpellList:
        spells = SpellList(
            Name="Warlock Archfey SLevel 6",
            Spells=self._combine_spells(6, self._archfey_spells),
            UUID=self.make_uuid("Warlock Archfey SLevel 6"),
        )
        self.mod.add(spells)
        return spells

    @spell_list("Warlock Fiend SLevel 1")
    def fiend_level_1_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(1, self._fiend_spells)

    @spell_list("Warlock Fiend SLevel 2")
    def fiend_level_2_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(2, self._fiend_spells)

    @spell_list("Warlock Fiend SLevel 3")
    def fiend_level_3_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(3, self._fiend_spells)

    @spell_list("Warlock Fiend SLevel 4")
    def fiend_level_4_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(4, self._fiend_spells)

    @spell_list("Warlock Fiend SLevel 5")
    def fiend_level_5_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(5, self._fiend_spells)

    @cached_property
    def fiend_level_6_spells(self) -> SpellList:
        spells = SpellList(
            Name="Warlock Fiend SLevel 6",
            Spells=self._combine_spells(6, self._fiend_spells),
            UUID=self.make_uuid("Warlock Fiend SLevel 6"),
        )
        self.mod.add(spells)
        return spells

    @spell_list("Warlock The Great Old One SLevel 1")
    def greatoldone_level_1_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(1, self._greatoldone_spells)

    @spell_list("Warlock The Great Old One SLevel 2")
    def greatoldone_level_2_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(2, self._greatoldone_spells)

    @spell_list("Warlock The Great Old One SLevel 3")
    def greatoldone_level_3_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(3, self._greatoldone_spells)

    @spell_list("Warlock The Great Old One SLevel 4")
    def greatoldone_level_4_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(4, self._greatoldone_spells)

    @spell_list("Warlock The Great Old One SLevel 5")
    def greatoldone_level_5_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(5, self._greatoldone_spells)

    @cached_property
    def greatoldone_level_6_spells(self) -> SpellList:
        spells = SpellList(
            Name="Warlock The Great Old One SLevel 6",
            Spells=self._combine_spells(6, self._greatoldone_spells),
            UUID=self.make_uuid("Warlock The Great Old One SLevel 6"),
        )
        self.mod.add(spells)
        return spells

    @spell_list("Warlock Hexblade SLevel 1")
    def hexblade_level_1_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(1, self._hexblade_spells)

    @spell_list("Warlock Hexblade SLevel 2")
    def hexblade_level_2_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(2, self._hexblade_spells)

    @spell_list("Warlock Hexblade SLevel 3")
    def hexblade_level_3_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(3, self._hexblade_spells)

    @spell_list("Warlock Hexblade SLevel 4")
    def hexblade_level_4_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(4, self._hexblade_spells)

    @spell_list("Warlock Hexblade SLevel 5")
    def hexblade_level_5_spells(self, spells: SpellList) -> None:
        spells.Spells = self._combine_spells(5, self._hexblade_spells)

    @cached_property
    def hexblade_level_6_spells(self) -> SpellList:
        spells = SpellList(
            Name="Warlock Hexblade SLevel 6",
            Spells=self._combine_spells(6, self._hexblade_spells),
            UUID=self.make_uuid("Warlock Hexblade SLevel 6"),
        )
        self.mod.add(spells)
        return spells

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
        progression.PassivesAdded += [self._pack_mule]
        progression.Selectors += [f"AddSpells({self._bolster})"]

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

    @progression(CharacterClass.WARLOCK_ARCHFEY, range(11, 21))
    def archfey_level_11_to_20(self, progression: Progression) -> None:
        progression.Selectors = [
            f"SelectSpells({self.archfey_level_6_spells.UUID},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_FIEND, range(11, 21))
    def fiend_level_11_to_20(self, progression: Progression) -> None:
        progression.Selectors = [
            f"SelectSpells({self.fiend_level_6_spells.UUID},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_GREATOLDONE, range(11, 21))
    def greatoldone_level_11_to_20(self, progression: Progression) -> None:
        progression.Selectors = [
            f"SelectSpells({self.greatoldone_level_6_spells.UUID},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 2)
    def hexblade_level_2(self, progression: Progression) -> None:
        progression.Selectors = [
            f"SelectSpells({warlock_hexblade_level_1_spells(self).UUID},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)"
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, range(11, 21))
    def hexblade_level_11_to_20(self, progression: Progression) -> None:
        progression.Selectors = [
            f"SelectSpells({self.hexblade_level_6_spells.UUID},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]


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
    parser.add_argument("-k", "--skills", type=int, default=6,
                        help="Number of skills to select at character creation (default 6)")
    parser.add_argument("-e", "--expertise", type=int, default=2,
                        help="Number of skills with expertise to select at character creation (default 2)")
    args = WarlockExtended.Args(**vars(parser.parse_args()))

    warlock_extended = WarlockExtended(args)
    warlock_extended.build()


if __name__ == "__main__":
    main()
