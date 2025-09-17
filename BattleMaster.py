
import os

from functools import cached_property
from moddb import Awareness, CunningActions, Movement
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    progression,
    Replacer,
)


class BattleMaster(Replacer):
    # Passives
    _awareness: str
    _bonus_action_dash: str
    _remarkable_athlete_run: str
    _running_jump: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="BattleMaster",
                         description="A class replacer for BattleMaster.",
                         **kwds)

        loca = self._mod.get_localization()
        run_display_name = f"{self.mod.get_prefix()}_RemarkableAthleteRun_DisplayName"
        loca[run_display_name] = {"en": "Remarkable Athlete: Run"}
        self._remarkable_athlete_run = Movement(self.mod).add_fast_movement(3.0, display_name=loca[run_display_name])

        self._awareness = Awareness(self.mod).add_awareness(5)
        self._bonus_action_dash = CunningActions(self.mod).add_dash_bonus_action()
        self._running_jump = CunningActions(self.mod).add_running_jump()

    @cached_property
    def _bonus_action_dash_spell_list(self) -> str:
        name = "Bonus Action Dash"
        spells = SpellList(
            Name=name,
            Spells=[self._bonus_action_dash],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return spells.UUID

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 3)
    def battlemaster_level_3(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,5,0)"]
        progress.PassivesAdded = ["ImprovedCritical", "JackOfAllTrades", self._remarkable_athlete_run]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, range(4, 21))
    def battlemaster_superiority_die(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 4)
    def battlemaster_level_4(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._awareness, self._running_jump]
        progress.Selectors = [
            f"AddSpells({self._bonus_action_dash_spell_list})",
        ]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 5)
    def battlemaster_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["UncannyDodge"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 7)
    def battlemaster_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            "Evasion",
            "RemarkableAthlete_Proficiency",
            "RemarkableAthlete_Jump",
        ]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 9)
    def battlemaster_level_9(self, progress: Progression) -> None:
        progress.PassivesAdded = ["BrutalCritical"]

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
