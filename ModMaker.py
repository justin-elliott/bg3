#!/usr/bin/env python3
"""
Generates files for the "ModMaker" mod.
"""

import argparse
import os
import re
import sys
import textwrap

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
from typing import Final, TextIO

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
                        help="Number of skills to select at level 1")
    parser.add_argument("-e", "--expertise", type=int,
                        help="Number of skills with expertise to select at level 1")
    args = Args(**vars(parser.parse_args()))
    update_feat_levels(args)
    update_classes(args)
    return args

PROLOGUE = """
import os

from modtools.lsx.game import Dependencies, Progression
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class {title}(Replacer):
    def __init__(self):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="{title}",
                         description="A class replacer for {classes}.")

        self.mod.add(Dependencies.ShortModuleDesc(
            Folder="UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            MD5="f94d034502139cf8b65a1597554e7236",
            Name="UnlockLevelCurve",
            PublishHandle=4166963,
            UUID="a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            Version64=72057594037927960,
        ))
"""

EPILOGUE = """

def main() -> None:
    {title_snake} = {title}()
    {title_snake}.build()


if __name__ == "__main__":
    main()
"""

def filter_classes(args: Args, progressions: list[Progression]) -> list[Progression]:
    return [progression for progression in progressions
            if progression.Name in CharacterClass
            and CharacterClass(progression.Name) in args.included_classes
            and not progression.IsMulticlass]

def allow_improvement(progress: Progression, args: Args) -> None:
    character_class = CharacterClass(progress.Name)
    if character_class not in BASE_CHARACTER_CLASSES:
        return
    feats = (args.rogue_feats if character_class == CharacterClass.ROGUE
             else args.fighter_feats if character_class == CharacterClass.FIGHTER
             else args.feats)
    progress.AllowImprovement = (progress.Level in feats) or None

def update_skills(progress: Progression, skills: int | None) -> None:
    if skills is None:
        return
    character_class = CharacterClass(progress.Name)
    if character_class in BASE_CHARACTER_CLASSES and progress.Level == 1:
        selectors = [selector for selector in progress.Selectors if not selector.startswith("SelectSkills(")]
        selectors.append(f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{skills})")
        progress.Selectors = selectors

def update_expertise(progress: Progression, expertise: int | None) -> None:
    if expertise is None:
        return
    character_class = CharacterClass(progress.Name)
    if character_class in BASE_CHARACTER_CLASSES and progress.Level == 1:
        selectors = [selector for selector in progress.Selectors if not selector.startswith("SelectSkillsExpertise(")]
        selectors.append(f"SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,{expertise})")
        progress.Selectors = selectors

INCLUDED_PROGRESSION_FIELDS: Final[list[str]] = [
    "AllowImprovement",
    "Boosts",
    "PassivesAdded",
    "PassivesRemoved",
    "Selectors",
]

INDENT: Final[int] = 4
MAX_LIST_LENGTH: Final[int] = 80

def write_progression(f: TextIO, progress: Progression) -> None:
    indent = " " * INDENT
    class_name = CharacterClass(progress.Name).name
    progression_text = textwrap.dedent(f"""\
        @progression(CharacterClass.{class_name}, {progress.Level})
        def {class_name.lower()}_level_{progress.Level}(self, progression: Progression) -> None:
        """)
    
    has_fields = False
    for field in INCLUDED_PROGRESSION_FIELDS:
        if (value := getattr(progress, field, None)) is not None:
            has_fields = True
            if isinstance(value, list) and len(str(value)) > MAX_LIST_LENGTH:
                progression_text += f"{indent}progression.{field} = [\n"
                for entry in value:
                    progression_text += f"{indent}{indent}'{entry}',\n"
                progression_text += f"{indent}]\n"
            else:
                progression_text += f"{indent}progression.{field} = {value}\n"
    if not has_fields:
        progression_text += f"{indent}raise DontIncludeProgression()\n"

    f.write("\n")
    f.write(textwrap.indent(progression_text, indent))

def main() -> None:
    args = parse_arguments()

    title = re.sub(r"\s", "", args.name)
    title_snake = re.sub(r"(?<!^)(?=[A-Z])", "_", title).lower()

    with TemporaryDirectory() as temp_dir:
        mod = Mod(temp_dir, author="justin-elliott", name="ModMaker", description="A mod maker.")
        progression.include(
            "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
            + "Progressions/Progressions.lsx"
        )
        progressions: list[Progression] = load_progressions(mod)
        progressions = filter_classes(args, progressions)
    
    mod_file = os.path.join(os.path.dirname(__file__), f"{args.name}.py")
    with open(mod_file, "w") as f:
        f.write(PROLOGUE.format(title=title, classes=", ".join([cls.value for cls in args.classes])))
        for progress in progressions:
            allow_improvement(progress, args)
            multiply_resources(progress, [ActionResource.SPELL_SLOTS], args.spells)
            multiply_resources(progress, [ActionResource.WARLOCK_SPELL_SLOTS], args.warlock_spells)
            multiply_resources(progress, ACTION_RESOURCES, args.actions)
            update_skills(progress, args.skills)
            update_expertise(progress, args.expertise)
            write_progression(f, progress)
        f.write(EPILOGUE.format(title=title, title_snake=title_snake))


if __name__ == "__main__":
    main()
