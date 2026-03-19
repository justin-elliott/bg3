#!/usr/bin/env python3

import os

from functools import cached_property
from moddb import Maneuvers
from modtools.gamedata import InterruptData, PassiveData, SpellData
from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
    progression,
    Replacer,
)


class BattleMaster(Replacer):
    _maneuvers: Maneuvers

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="BattleMaster",
                         description="A class replacer for BattleMaster.",
                         **kwds)

        self._maneuvers = Maneuvers(self.mod)
        
    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 3)
    def battlemaster_level_3(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,3,0)"]
        progress.PassivesAdded = ["ImprovedCritical"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 4)
    def battlemaster_level_4(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 5)
    def battlemaster_level_5(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 6)
    def battlemaster_level_6(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 7)
    def battlemaster_level_7(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]
        progress.PassivesAdded = ["RemarkableAthlete_Proficiency", "RemarkableAthlete_Jump"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 8)
    def battlemaster_level_8(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 9)
    def battlemaster_level_9(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 10)
    def battlemaster_level_10(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]
        progress.Selectors += ["SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 11)
    def battlemaster_level_11(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 12)
    def battlemaster_level_12(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]
        progress.PassivesAdded = [self._maneuvers.relentless]


def main() -> None:
    battle_master = BattleMaster(
        classes=[CharacterClass.FIGHTER_BATTLEMASTER],
        actions=2,
    )
    battle_master.build()


if __name__ == "__main__":
    main()
