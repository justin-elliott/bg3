#!/usr/bin/env python3

import os

from functools import cache, cached_property
from modtools.lsx.game import (
    Progression,
    SpellList,
)
from modtools.replacers import (
    CharacterClass,
    progression,
    Replacer,
    warlock_cantrips,
    warlock_combined_spells,
)

class HexbladeCombined(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="HexbladeCombined",
                         description="A class replacer for Hexblade Warlock.",
                         **kwds)

    @cache
    def __combined_spells(self, level: int) -> str:
        name = f"Hexblade Combined Level {level} spells"
        uuid = self.make_uuid(name)
        self.mod.add(SpellList(
            Name=name,
            Spells=warlock_combined_spells(self, level),
            UUID=uuid,
        ))
        return uuid

    @progression(CharacterClass.WARLOCK_HEXBLADE, 1)
    def hexblade_level_1(self, progress: Progression) -> None:
        progress.PassivesAdded = ["HexWarrior", "HexbladesCurse", "DarkOnesBlessing", "ClarifiedMortality"]
        progress.Selectors = [
            "AddSpells(c4020f68-bb82-4c45-8a4a-8c24fb400526)",  # Hexblade's Curse
            "AddSpells(489ff3dd-b93e-4a96-b553-b59c07d5cd6f)",  # Fey Presence
            f"SelectSpells({self.__combined_spells(1)},2,0,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 2)
    def hexblade_level_2(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(1)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 3)
    def hexblade_level_3(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(2)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 4)
    def hexblade_level_4(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({warlock_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.__combined_spells(2)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 5)
    def hexblade_level_5(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(3)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 6)
    def hexblade_level_6(self, progress: Progression) -> None:
        progress.PassivesAdded = ["AccursedSpecter", "MistyEscape", "DarkOnesOwnLuck", "EntropicWard"]
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(3)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 7)
    def hexblade_level_7(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(4)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 8)
    def hexblade_level_8(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(4)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 9)
    def hexblade_level_9(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(5)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 10)
    def hexblade_level_10(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            "ArmorOfHexes",
            "BeguilingDefenses",
            "FiendishResilience",
            "Thought_Shield_Psychic_Resistance",
            "Thought_Shield_Psychic_Reflection",
        ]
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(5)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 11)
    def hexblade_level_11(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(5)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 12)
    def hexblade_level_12(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__combined_spells(5)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]


def main() -> None:
    hexblade_combined = HexbladeCombined(
        classes=[CharacterClass.WARLOCK_HEXBLADE],
        warlock_spells=4,
        actions=2,
    )
    hexblade_combined.build()


if __name__ == "__main__":
    main()
