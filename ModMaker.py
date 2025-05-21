#!/usr/bin/env python3
"""
Generates files for the "ModMaker" mod.
"""

import argparse
import os
import re
import sys

from collections import OrderedDict
from dataclasses import dataclass
from moddb import multiply_resources
from modtools.lsx.game import (
    ActionResource,
    BASE_CHARACTER_CLASSES,
    CharacterClass,
    CharacterSubclasses,
)
from modtools.lsx.game import Dependencies, Progression
from modtools.mod import Mod
from modtools.replacers import (
    DontIncludeProgression,
    load_progressions,
    only_existing_progressions,
    progression,
    Replacer,
)
from tempfile import TemporaryDirectory
from typing import Final

@dataclass
class Args:
    name: str                                      # Mod name
    classes: list[CharacterClass]                  # Class progressions to replace
    feats: set[int]                                # Feat improvement levels
    spells: int                                    # Multiplier for spell slots
    warlock_spells: int                            # Multiplier for Warlock spell slots
    actions: int                                   # Multiplier for other action resources
    skills: int                                    # Number of skills to select at character creation
    expertise: int                                 # Number of skill expertises to select at character creation
    fighter_feats: set[int] = None                 # Fighter feat improvement levels
    rogue_feats: set[int] = None                   # Rogue feat improvement levels
    included_classes: list[CharacterClass] = None  # The classes belonging together with the named classes

def class_list(s: str) -> list[str]:
    classes = [CharacterClass(cc) for cc in s.split(",")]
    if not set(classes).issubset(CharacterSubclasses.ALL):
        raise "Invalid class names"
    return classes

def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels

FIGHTER_EXTRA_FEATS: Final[dict[int, set[int]]] = {
    1: set(),
    2: {3, 5, 13},
    3: {5, 14},
    4: {6, 14},
}

ROGUE_EXTRA_FEATS: Final[dict[int, set[int]]] = {
    1: set(),
    2: {3, 9},
    3: {10},
    4: {10},
}

def update_feat_levels(args: Args) -> None:
    if len(args.feats) == 1:
        feat_level = next(level for level in args.feats)
        feat_level = min(4, max(1, feat_level))
        args.feats = frozenset(
            {*range(max(feat_level, 2), 20, feat_level)} | ({19} if 20 % feat_level == 0 else set()))
        args.fighter_feats = args.feats | FIGHTER_EXTRA_FEATS[feat_level]
        args.rogue_feats = args.feats | ROGUE_EXTRA_FEATS[feat_level]
    else:
        args.feats = args.feats - frozenset([1, 20])
        args.fighter_feats = args.feats
        args.rogue_feats = args.feats

def update_classes(args: Args) -> None:
    classes: OrderedDict[str, None] = OrderedDict()
    included_classes: OrderedDict[str, None] = OrderedDict()

    for name in args.classes:
        character_class = CharacterClass(name)
        classes[character_class] = None

        if character_class in BASE_CHARACTER_CLASSES:
            included_classes[character_class] = None
            for subclass in sorted(vars(CharacterSubclasses)[character_class.name] - {character_class}):
                included_classes[subclass] = None
        else:
            included_classes[[base_class for base_class in BASE_CHARACTER_CLASSES
                              if character_class in vars(CharacterSubclasses)[base_class.name]][0]] = None
            included_classes[character_class] = None
    
    args.classes = [*classes.keys()]
    args.included_classes = [*included_classes.keys()]


def parse_arguments() -> Args:
    parser = argparse.ArgumentParser(description="A mod maker.")
    parser.add_argument("-n", "--name", type=str, required=True,
                        help="Mod name")
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
                        help="Number of skills to select at levels 1, 4, 10, and 16")
    parser.add_argument("-e", "--expertise", type=int,
                        help="Number of skills with expertise to select at levels 1, 6, 12, and 18")
    args = Args(**vars(parser.parse_args()))
    update_feat_levels(args)
    update_classes(args)
    return args

PROLOGUE = """
import os

from modtools.replacers import Replacer


class {title}(Replacer):
    def __init__(self):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="{title}",
                         description="A class replacer for {classes}.")
"""

EPILOGUE = """
def main() -> None:
    {title_snake} = {title}()
    {title_snake}.build()


if __name__ == "__main__":
    main()
"""

def main() -> None:
    args = parse_arguments()

    title = re.sub(r"\s", "", args.name)
    title_snake = re.sub(r"(?<!^)(?=[A-Z])", "_", title).lower()

    with TemporaryDirectory() as temp_dir:
        mod = Mod(temp_dir,
                author="justin-elliott",
                name="ModMaker",
                description="A mod maker.")

        progression.include(
            "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
            + "Progressions/Progressions.lsx"
        )
        progressions: list[Progression] = load_progressions(mod)
    
    # mod_file = os.path.join(os.path.dirname(__file__), f"{args.name}.py")
    # with open(mod_file, "w") as f:
    with sys.stdout as f:
        f.write(PROLOGUE.format(title=title, classes=", ".join([cls.value for cls in args.classes])))
        f.write(EPILOGUE.format(title=title, title_snake=title_snake))


if __name__ == "__main__":
    main()
