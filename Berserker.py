#!/usr/bin/env python3

import os

from functools import cached_property
from moddb import CunningActions
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class Berserker(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Berserker",
                         description="A class replacer for Berserker.",
                         **kwds)

        self._rage_frenzy()

    @cached_property
    def _frenzy_extra_resistances(self) -> str:
        name = f"{self.mod.get_prefix()}_FrenzyExtraResistances"
        self.mod.add(PassiveData(
            name,
            Properties=["IsHidden"],
            BoostContext=["OnEquip", "OnCreate"],
            BoostConditions=["not HasHeavyArmor(context.Source)"],
            Boosts=[
                "Resistance(Acid,Resistant)",
                "Resistance(Cold,Resistant)",
                "Resistance(Fire,Resistant)",
                "Resistance(Force,Resistant)",
                "Resistance(Lightning,Resistant)",
                "Resistance(Necrotic,Resistant)",
                "Resistance(Poison,Resistant)",
                "Resistance(Psychic,Resistant)",
                "Resistance(Radiant,Resistant)",
                "Resistance(Thunder,Resistant)",
            ],
        ))
        return name

    def _rage_frenzy(self) -> None:
        self.mod.add(StatusData(
            "RAGE_FRENZY",
            StatusType="BOOST",
            using="RAGE_FRENZY",
            Passives=[
                "Rage_Rage_Boosts",
                "Rage_Attack",
                "Rage_Damaged",
                "Rage_Frenzy_NoHeavyArmour_VFX",
                self._frenzy_extra_resistances,
            ],
        ))

    @cached_property
    def _dash_bonus_action(self) -> None:
        return CunningActions(self.mod).add_dash_bonus_action()

    @cached_property
    def _level_3_spells(self) -> SpellList:
        spells = SpellList(
            Name="Berserker level 3 spells",
            Spells=[
                "Shout_ActionSurge",
                self._dash_bonus_action,
            ],
            UUID=self.make_uuid("level_3_spells"),
        )
        self.mod.add(spells)
        return spells

    @progression(CharacterClass.BARBARIAN_BERSERKER, 3)
    def berserkerpath_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            "FastHands",
            "ImprovedCritical",
        ]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._level_3_spells.UUID})",
            "AddSpells(afe6b18c-47a7-4c5f-aed5-49dfe07e5234)", # Thaumaturgy
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 4)
    def berserkerpath_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 5)
    def berserkerpath_level_5(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 6)
    def berserkerpath_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 7)
    def berserkerpath_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 8)
    def berserkerpath_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 9)
    def berserkerpath_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 10)
    def berserkerpath_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 11)
    def berserkerpath_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_2"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack"]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 12)
    def berserkerpath_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 13)
    def berserkerpath_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 14)
    def berserkerpath_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 15)
    def berserkerpath_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 16)
    def berserkerpath_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 17)
    def berserkerpath_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 18)
    def berserkerpath_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 19)
    def berserkerpath_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_BERSERKER, 20)
    def berserkerpath_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_3"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack_2"]


def main() -> None:
    berserker = Berserker(
        classes=[CharacterClass.BARBARIAN_BERSERKER],
    )
    berserker.build()


if __name__ == "__main__":
    main()
