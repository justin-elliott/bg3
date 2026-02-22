#!/usr/bin/env python3

import os

from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
    progression,
    Replacer,
)


class DevilishSorceryPoints(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="DevilishSorceryPoints",
                         description="A class replacer for Sorcerer.",
                         **kwds)

    @progression(CharacterClass.SORCERER, 2)
    def sorcerer_level_2(self, progress: Progression) -> None:
        progress.Boosts = [
            *[boost for boost in progress.Boosts if not boost.startswith("ActionResource(SorceryPoint,")],
            "ActionResource(SorceryPoint,666)",
        ]

    @progression(CharacterClass.SORCERER, range(3, 21))
    def sorcerer_level_1(self, progress: Progression) -> None:
        progress.Boosts = [boost for boost in progress.Boosts if not boost.startswith("ActionResource(SorceryPoint,")]


def main() -> None:
    devilish_sorcery_points = DevilishSorceryPoints(
        classes=[CharacterClass.SORCERER],
        spells=2,
    )
    devilish_sorcery_points.build()


if __name__ == "__main__":
    main()
