#!/usr/bin/env python3
"""
Generates files for the "ModMaker" mod.
"""

import os
import re
import textwrap

from modtools.lsx.game import CharacterClass
from modtools.replacers import (
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
        classes=[{classes}],
        feats={feats},
        spells={spells},
        warlock_spells={warlock_spells},
        actions={actions},
        skills={skills},
        expertise={expertise},
        full_caster={full_caster},
    )
    {title_snake}.build()


if __name__ == "__main__":
    main()
"""

INDENT: Final[int] = 4
MAX_LIST_LENGTH: Final[int] = 80

def write_progression(f: TextIO, character_class: str, level: int) -> None:
    indent = " " * INDENT
    progression_text = textwrap.dedent(f"""\

        @progression(CharacterClass.{character_class.name}, {level})
        def {character_class.lower()}_level_{level}(self, _: Progression) -> None:
            raise DontIncludeProgression()
        """)
    f.write(textwrap.indent(progression_text, indent))

def main() -> None:
    replacer = Replacer(os.path.dirname(__file__),
                        author="justin-elliott",
                        description="A mod maker.")

    title = re.sub(r"\s", "", replacer.args.name)
    title_snake = re.sub(r"(?<!^)(?=[A-Z])", "_", title).lower()

    mod_file = os.path.join(os.path.dirname(__file__), f"{replacer.args.name}.py")
    with open(mod_file, "w") as f:
        f.write(PROLOGUE.format(title=title, classes=", ".join([cls.value for cls in replacer.args.classes])))

        for character_class in replacer.args.classes:
            for level in range(1, 21):
                write_progression(f, character_class, level)
        
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
                                expertise=replacer.args.expertise,
                                full_caster=replacer.args.full_caster))


if __name__ == "__main__":
    main()
