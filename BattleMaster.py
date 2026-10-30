#!/usr/bin/env python3

import os

from moddb import Maneuvers
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
        progress.Boosts = [f"ActionResource(SuperiorityDie,{3*self.args.actions},0)"]
        progress.PassivesAdded = ["ImprovedCritical"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, range(4, 21))
    def battlemaster_level_4(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SuperiorityDie,{self.args.actions},0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 7)
    def battlemaster_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = ["RemarkableAthlete_Proficiency", "RemarkableAthlete_Jump"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 10)
    def battlemaster_level_10(self, progress: Progression) -> None:
        progress.Selectors += ["SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)"]


def main() -> None:
    battle_master = BattleMaster(
        classes=[CharacterClass.FIGHTER_BATTLEMASTER],
        actions=2,
        level_20=True,
    )
    battle_master.build()


if __name__ == "__main__":
    main()
