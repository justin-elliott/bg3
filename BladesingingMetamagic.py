#!/usr/bin/env python3

import os

from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class BladesingingMetamagic(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="BladesingingMetamagic",
                         description="A class replacer for Bladesinging.",
                         **kwds)

    @progression(CharacterClass.WIZARD_BLADESINGING, 2)
    def bladesingingschool_level_2(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            f"ActionResource(SorceryPoint,{2 * self.args.actions},0)",
            "Tag(SORCERER_METAMAGIC)",
        ]
        progress.Selectors = (progress.Selectors or []) + [
            "AddSpells(979e37ad-05fa-466c-af99-9eb104a6e876,,,,AlwaysPrepared)",
            "SelectPassives(49704931-e47b-4ce6-abc6-dfa7ba640752,2,Metamagic)",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 3)
    def bladesingingschool_level_3(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives(c3506532-36eb-4d18-823e-497a537a9619,1,Metamagic)",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 10)
    def bladesingingschool_level_10(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives(c3506532-36eb-4d18-823e-497a537a9619,1,Metamagic)",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 17)
    def bladesingingschool_level_17(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives(c3506532-36eb-4d18-823e-497a537a9619,1,Metamagic)",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, range(3, 21))
    def bladesingingschool_sorcery_points(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            f"ActionResource(SorceryPoint,{self.args.actions},0)",
        ]


def main() -> None:
    bladesinging_metamagic = BladesingingMetamagic(
        classes=[CharacterClass.WIZARD_BLADESINGING],
        spells=2,
        actions=2,
    )
    bladesinging_metamagic.build()


if __name__ == "__main__":
    main()
