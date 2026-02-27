#!/usr/bin/env python3

import os

from moddb import Sorcery
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
    progression,
    Replacer,
)


class Metamage(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Metamage",
                         description="A class replacer for AbjurationSchool.",
                         **kwds)

        Sorcery(self.mod).increase_create_sorcery_points(self.args.actions)

        self.loca["ArcaneWard_ExtraDescription"] = """
            Each time you cast a spell, the intensity of the ward increases by the amount of the spell's Level.
            
            Each time you take damage, the ward blocks an amount of damage equal to its intensity, and its intensity
            decreases by [1].
            
            After each <LSTag Tooltip="LongRest">Long Rest</LSTag>, the ward's intensity resets, and becomes the same
            as your wizard level.
        """
        self.add(PassiveData(
            "ArcaneWard",
            using="ArcaneWard",
            ExtraDescription=self.loca["ArcaneWard_ExtraDescription"],
        ))

        self.add(PassiveData(
            "ArcaneWard_Cast",
            using="ArcaneWard_Cast",
            Conditions=["IsSpell() and not IsCantrip()"],  # Any spell qualifies for Arcane Ward
        ))

        self.loca["ARCANE_WARD_Description"] = """
            Your arcane ward blocks damage equal to its charges and then loses 1 charge. Casting spells will add charges
            equal to the level of the spell.
        """
        self.add(StatusData(
            "ARCANE_WARD",
            StatusType="BOOST",
            using="ARCANE_WARD",
            Description=self.loca["ARCANE_WARD_Description"],
        ))

    @progression(CharacterClass.WIZARD_ABJURATION, range(3, 21))
    def abjurationschool_sorcery_points(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            f"ActionResource(SorceryPoint,{self.args.actions},0)",
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 2)
    def abjurationschool_level_2(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            f"ActionResource(SorceryPoint,{2 * self.args.actions},0)",
            "Tag(SORCERER_METAMAGIC)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            "SculptSpells",
        ]
        progress.Selectors = (progress.Selectors or []) + [
            "AddSpells(979e37ad-05fa-466c-af99-9eb104a6e876,,,,AlwaysPrepared)",
            "SelectPassives(49704931-e47b-4ce6-abc6-dfa7ba640752,2,Metamagic)",
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 3)
    def abjurationschool_level_3(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives(c3506532-36eb-4d18-823e-497a537a9619,1,Metamagic)",
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 10)
    def abjurationschool_level_10(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives(c3506532-36eb-4d18-823e-497a537a9619,1,Metamagic)",
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 17)
    def abjurationschool_level_17(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives(c3506532-36eb-4d18-823e-497a537a9619,1,Metamagic)",
        ]


def main() -> None:
    metamage = Metamage(
        classes=[CharacterClass.WIZARD_ABJURATION],
        spells=2,
        actions=4,
    )
    metamage.build()


if __name__ == "__main__":
    main()
