#!/usr/bin/env python3
"""
Generates files for the "ModMaker" mod.
"""

import os
import re
import textwrap

from modtools.lsx.game import (
    BASE_CHARACTER_CLASSES,
    CharacterClass,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    load_progressions,
    progression,
    Replacer,
)
from typing import Final, TextIO

PROLOGUE = """
import os

from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class {title}(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="{title}",
                         description="A class replacer for {classes}.",
                         **kwds)
"""

EPILOGUE = """

def main() -> None:
    {title_snake} = {title}(
        classes=[
            {classes}
        ],
        feats={feats},
        spells={spells},
        warlock_spells={warlock_spells},
        actions={actions},
        skills={skills},
        expertise={expertise},
    )
    {title_snake}.build()


if __name__ == "__main__":
    main()
"""

def filter_classes(progressions: list[Progression], args: Replacer.Args) -> list[Progression]:
    return [progression for progression in progressions
            if progression.Name in CharacterClass
            and CharacterClass(progression.Name) in args.classes
            and not progression.IsMulticlass]

INDENT: Final[int] = 4
MAX_LIST_LENGTH: Final[int] = 80

def write_progression(f: TextIO, progress: Progression) -> None:
    indent = " " * INDENT
    class_name = CharacterClass(progress.Name).name
    progression_text = textwrap.dedent(f"""\

        @progression(CharacterClass.{class_name}, {progress.Level})
        def {class_name.lower()}_level_{progress.Level}(self, _: Progression) -> None:
            raise DontIncludeProgression()
        """)
    f.write(textwrap.indent(progression_text, indent))

def main() -> None:
    replacer = Replacer(os.path.dirname(__file__),
                        author="justin-elliott",
                        description="A mod maker.")
    progressions: list[Progression] = load_progressions(replacer.mod)
    progressions = filter_classes(progressions, replacer.args)
    
    title = re.sub(r"\s", "", replacer.args.name)
    title_snake = re.sub(r"(?<!^)(?=[A-Z])", "_", title).lower()

    mod_file = os.path.join(os.path.dirname(__file__), f"{replacer.args.name}.py")
    with open(mod_file, "w") as f:
        f.write(PROLOGUE.format(title=title, classes=", ".join([cls.value for cls in replacer.args.classes])))

        for progress in progressions:
            write_progression(f, progress)
        
        classes = f",\n{' ' * INDENT * 3}".join([f"CharacterClass.{cls.name}" for cls in replacer.args.classes])
        feats = ", ".join(map(str, sorted(replacer.args.feats)))
        f.write(EPILOGUE.format(title=title,
                                title_snake=title_snake,
                                classes=classes,
                                feats=feats,
                                spells=replacer.args.spells,
                                warlock_spells=replacer.args.warlock_spells,
                                actions=replacer.args.actions,
                                skills=replacer.args.skills,
                                expertise=replacer.args.expertise))


if __name__ == "__main__":
    main()
