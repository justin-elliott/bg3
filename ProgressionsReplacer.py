#!/usr/bin/env python3
"""
Generates files for the "ProgressionsReplacer" mod.
"""

import argparse
import os

from dataclasses import dataclass
from moddb import multiply_resources
from modtools.lsx.game import (
    ActionResource,
    BASE_CHARACTER_CLASSES,
    CharacterClass,
    CharacterSubclasses,
)
from modtools.lsx.game import Dependencies, Progression
from modtools.replacers import (
    DontIncludeProgression,
    only_existing_progressions,
    progression,
    Replacer,
)


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class ProgressionsReplacer(Replacer):
    @dataclass
    class Args:
        name: str                       # Mod name
        classes: set[CharacterClass]    # Class progressions to replace
        feats: set[int]                 # Feat improvement levels
        spells: int                     # Multiplier for spell slots
        warlock_spells: int             # Multiplier for Warlock spell slots
        actions: int                    # Multiplier for other action resources
        skills: int                     # Number of skills to select at character creation
        expertise: int                  # Number of skill expertises to select at character creation
        fighter_feats: set[int] = None  # Fighter feat improvement levels
        rogue_feats: set[int] = None    # Rogue feat improvement levels

    ACTION_RESOURCES = frozenset([
        ActionResource.ARCANE_RECOVERY_CHARGES,
        ActionResource.ARCANE_SHOT_CHARGES,
        ActionResource.BARDIC_INSPIRATION_CHARGES,
        ActionResource.BLADESONG_CHARGES,
        ActionResource.CHANNEL_DIVINITY_CHARGES,
        ActionResource.CHANNEL_OATH_CHARGES,
        ActionResource.COSMIC_OMEN_POINTS,
        ActionResource.FUNGAL_INFESTATION_CHARGES,
        ActionResource.KI_POINTS,
        ActionResource.LAY_ON_HANDS_CHARGES,
        ActionResource.NATURAL_RECOVERY_CHARGES,
        ActionResource.RAGE_CHARGES,
        ActionResource.SORCERY_POINTS,
        ActionResource.STAR_MAP_POINTS,
        ActionResource.SUPERIORITY_DICE,
        ActionResource.SWARM_CHARGES,
        ActionResource.WAR_PRIEST_CHARGES,
        ActionResource.WILD_SHAPE_CHARGES,
        ActionResource.WRITHING_TIDE_POINTS,
    ])

    _args: Args

    def __init__(self, args: Args):
        if len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            feat_levels = str(feat_level)
            args.feats = frozenset(
                {*range(max(feat_level, 2), 20, feat_level)} | ({19} if 20 % feat_level == 0 else {}))
            args.fighter_feats = args.feats | {3, 5, 13}
            args.rogue_feats = args.feats | {3, 9}
        else:
            args.feats = args.feats - frozenset([1, 20])
            args.fighter_feats = args.feats
            args.rogue_feats = args.feats
            feat_levels = "_".join(str(level) for level in sorted(args.feats))

        if len(feat_levels) > 0:
            feat_levels = f"F{feat_levels}-"

        if len(args.classes) == 0:
            class_names = "All"
            args.classes = CharacterSubclasses.ALL
        else:
            class_names = "-".join(class_name for class_name in args.classes)
            subclasses = set()
            for character_class in args.classes:
                name = CharacterClass(character_class).name
                subclasses |= vars(CharacterSubclasses)[name]
            args.classes = subclasses

        if not args.name:
            args.name = f"Progressions-{class_names}-{feat_levels}S{args.spells}-W{args.warlock_spells}-A{args.actions}"
            if args.skills is not None:
                args.name += f"-K{args.skills}"
            if args.expertise is not None:
                args.name += f"-E{args.expertise}"

        super().__init__(os.path.join(os.path.dirname(__file__), "Progressions"),
                         author="justin-elliott",
                         name=args.name,
                         description="A class progressions replacer.")

        self.mod.add(Dependencies.ShortModuleDesc(
            Folder="UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            MD5="f94d034502139cf8b65a1597554e7236",
            Name="UnlockLevelCurve",
            PublishHandle=4166963,
            UUID="a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            Version64=72057594037927960,
        ))
    
        self._args = args

    def _allow_improvement(self, progression: Progression, feats: set[int]) -> None:
        if (len(feats) == 0):
            raise DontIncludeProgression()
        if CharacterClass(progression.Name) not in self._args.classes:
            raise DontIncludeProgression()
        allow_improvement = progression.AllowImprovement
        progression.AllowImprovement = True if progression.Level in feats else None
        if allow_improvement == progression.AllowImprovement:
            raise DontIncludeProgression()

    @progression(BASE_CHARACTER_CLASSES - {CharacterClass.FIGHTER, CharacterClass.ROGUE}, range(2, 21))
    @only_existing_progressions
    def allow_improvement_base(self, progression: Progression) -> None:
        self._allow_improvement(progression, self._args.feats)

    @progression(CharacterClass.FIGHTER, range(2, 21))
    @only_existing_progressions
    def allow_improvement_fighter(self, progression: Progression) -> None:
        self._allow_improvement(progression, self._args.fighter_feats)

    @progression(CharacterClass.ROGUE, range(2, 21))
    @only_existing_progressions
    def allow_improvement_rogue(self, progression: Progression) -> None:
        self._allow_improvement(progression, self._args.rogue_feats)

    @progression(CharacterSubclasses.ALL, range(1, 21))
    @only_existing_progressions
    def increase_resources(self, progression: Progression) -> None:
        if CharacterClass(progression.Name) not in self._args.classes:
            raise DontIncludeProgression()
        boosts = progression.Boosts
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression, [ActionResource.WARLOCK_SPELL_SLOTS], self._args.warlock_spells)
        multiply_resources(progression, self.ACTION_RESOURCES, self._args.actions)
        if boosts == progression.Boosts:
            raise DontIncludeProgression()

    @progression(BASE_CHARACTER_CLASSES, 1, is_multiclass=False)
    def increase_skills(self, progression: Progression) -> None:
        if CharacterClass(progression.Name) not in self._args.classes:
            raise DontIncludeProgression()
        selectors = progression.Selectors
        if self._args.skills is not None:
            selectors = [selector for selector in (selectors or []) if not selector.startswith("SelectSkills(")]
            selectors.append(f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self._args.skills})")
        if self._args.expertise is not None:
            selectors = [selector for selector in selectors if not selector.startswith("SelectSkillsExpertise(")]
            selectors.append(f"SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self._args.expertise})")
        if progression.Selectors == selectors:
            raise DontIncludeProgression
        progression.Selectors = selectors


def class_list(s: str) -> set[str]:
    classes = frozenset([CharacterClass(cc) for cc in s.split(",")])
    if not classes.issubset(BASE_CHARACTER_CLASSES):
        raise "Invalid class names"
    return classes


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="A replacer for class progressions.")
    parser.add_argument("-n", "--name", type=str, default=None,
                        help="Progression name (optional)")
    parser.add_argument("-c", "--classes", type=class_list, default=set(),
                        help="Classes to include in the progression (defaulting to all)")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to normal progression)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=1,
                        help="Spell slot multiplier (defaulting to 1; normal spell slots)")
    parser.add_argument("-w", "--warlock_spells", type=int, choices=range(1, 9), default=1,
                        help="Warlock spell slot multiplier (defaulting to 1; normal spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=1,
                        help="Action resource multiplier (defaulting to 1; normal resources)")
    parser.add_argument("-k", "--skills", type=int,
                        help="Number of skills to select at character creation")
    parser.add_argument("-e", "--expertise", type=int,
                        help="Number of skill expertises to select at character creation")
    args = ProgressionsReplacer.Args(**vars(parser.parse_args()))

    progressions_replacer = ProgressionsReplacer(args)
    progressions_replacer.build()


if __name__ == "__main__":
    main()
