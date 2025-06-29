
import os

from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
    progression,
    Replacer,
)


class BattleMaster(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="BattleMaster",
                         description="A class replacer for BattleMaster.",
                         **kwds)

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 3)
    def battlemaster_level_3(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,4,0)"]
        progress.PassivesAdded = ["ImprovedCritical"]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, range(4, 21))
    def battlemaster_superiority_die(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 5)
    def battlemaster_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["UncannyDodge"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 6)
    def battlemaster_level_6(self, progress: Progression) -> None:
        progress.Selectors = [
            "AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a)",  # Volley, Whirlwind
        ]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 7)
    def battlemaster_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = ["Evasion", "RemarkableAthlete_Proficiency", "RemarkableAthlete_Jump"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 10)
    def battlemaster_level_10(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 15)
    def battlemaster_level_15(self, progress: Progression) -> None:
        progress.PassivesAdded += ["SuperiorCritical"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 18)
    def battlemaster_level_18(self, progress: Progression) -> None:
        progress.PassivesAdded = ["Survivor"]


def main() -> None:
    battle_master = BattleMaster(
        classes=[CharacterClass.FIGHTER_BATTLEMASTER],
        feats=2,
    )
    battle_master.build()


if __name__ == "__main__":
    main()
