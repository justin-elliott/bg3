#!/usr/bin/env python3

import os

from moddb import Sorcery
from modtools.replacers import (
    CharacterClass,
    Replacer,
)


class CreateSorceryPoints(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         description="A class replacer for Sorcerer.",
                         **kwds)
        
        Sorcery(self.mod).increase_create_sorcery_points(self.args.actions)

    def generate_name(self) -> str:
        """Generate a name for the Mod."""
        return f"CreateSorceryPoints_x{self.args.actions}"


def main() -> None:
    create_sorcery_points = CreateSorceryPoints(
        classes=[CharacterClass.SORCERER],
        spells=2,
        actions=2,
    )
    create_sorcery_points.build()


if __name__ == "__main__":
    main()
