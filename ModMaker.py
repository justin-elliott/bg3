#!/usr/bin/env python3
"""
Generates files for the "ModMaker" mod.
"""

import os
import re
import textwrap

from moddb import multiply_resources
from modtools.lsx.game import (
    ActionResource,
    BASE_CHARACTER_CLASSES,
    CharacterClass,
)
from modtools.lsx.game import Progression
from modtools.mod import Mod
from modtools.replacers import (
    load_progressions,
    progression,
    Replacer,
)
from tempfile import TemporaryDirectory
from typing import Final, TextIO

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

def filter_classes(progressions: list[Progression], args: Replacer.Args) -> list[Progression]:
    return [progression for progression in progressions
            if progression.Name in CharacterClass
            and CharacterClass(progression.Name) in args.included_classes
            and not progression.IsMulticlass]

def allow_improvement(progress: Progression, args: Replacer.Args) -> None:
    character_class = CharacterClass(progress.Name)
    if character_class not in BASE_CHARACTER_CLASSES:
        return
    feats = (args.rogue_feats if character_class == CharacterClass.ROGUE
             else args.fighter_feats if character_class == CharacterClass.FIGHTER
             else args.other_feats)
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
                    progression_text += f"{indent}{indent}{repr(entry)},\n"
                progression_text += f"{indent}]\n"
            else:
                progression_text += f"{indent}progression.{field} = {value}\n"
    if not has_fields:
        progression_text += f"{indent}raise DontIncludeProgression()\n"

    f.write("\n")
    f.write(textwrap.indent(progression_text, indent))

def main() -> None:
    replacer = Replacer(os.path.dirname(__file__),
                        author="justin-elliott",
                        description="A mod maker.")

    title = re.sub(r"\s", "", replacer.args.name)
    title_snake = re.sub(r"(?<!^)(?=[A-Z])", "_", title).lower()

    with TemporaryDirectory() as temp_dir:
        mod = Mod(temp_dir, author="justin-elliott", name="ModMaker", description="A mod maker.")
        progression.include(
            "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
            + "Progressions/Progressions.lsx"
        )
        progressions: list[Progression] = load_progressions(mod)
        progressions = filter_classes(progressions, replacer.args)
    
    mod_file = os.path.join(os.path.dirname(__file__), f"{replacer.args.name}.py")
    with open(mod_file, "w") as f:
        f.write(PROLOGUE.format(title=title, classes=", ".join([cls.value for cls in replacer.args.classes])))
        for progress in progressions:
            allow_improvement(progress, replacer.args)
            multiply_resources(progress, [ActionResource.SPELL_SLOTS], replacer.args.spells)
            multiply_resources(progress, [ActionResource.WARLOCK_SPELL_SLOTS], replacer.args.warlock_spells)
            multiply_resources(progress, Replacer.ACTION_RESOURCES, replacer.args.actions)
            update_skills(progress, replacer.args.skills)
            update_expertise(progress, replacer.args.expertise)
            write_progression(f, progress)
        f.write(EPILOGUE.format(title=title, title_snake=title_snake))


if __name__ == "__main__":
    main()
