#!/usr/bin/env python3
"""
Generates files for the Best of Both Worlds, a mod to give Half-Elves the features of both of their parent races.
"""

import os

from modtools.lsx.game import (
    CharacterClass,
    CharacterRace,
    Progression,
)
from modtools.replacers import (
    progression,
    Replacer,
)


class BestOfBothWorlds(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="BestOfBothWorlds",
                         description="Enhancements for the Half-Elf subraces.",
                         **kwds)

    @progression(CharacterRace.HALF_ELF, 1)
    def half_elf(self, progress: Progression) -> None:
        progress.Boosts += ["ProficiencyBonus(Skill,Perception)"]
        progress.PassivesAdded += ["Elf_WeaponTraining"]
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,1,HumanVersatility)",
        ]


if __name__ == "__main__":
    best_of_both_worlds = BestOfBothWorlds(
        classes=[CharacterClass.ROGUE],  # Ignored, but prevents multiclass slots from being updated
    )
    best_of_both_worlds.build()
