
import os

from moddb import (
    Awareness,
    CunningActions,
    Movement,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class Huntress(Replacer):
    # Passives
    _awareness: str
    _remarkable_athlete_run_30: str
    _remarkable_athlete_run_45: str
    _remarkable_athlete_run_60: str
    _running_jump: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Huntress",
                         description="A class replacer for Champion.",
                         **kwds)

        loca = self._mod.get_localization()
        run_display_name = f"{self.mod.get_prefix()}_RemarkableAthleteRun_DisplayName"
        loca[run_display_name] = {"en": "Remarkable Athlete: Run"}

        self._remarkable_athlete_run_30 = Movement(self.mod).add_fast_movement(3.0, display_name=loca[run_display_name])
        self._remarkable_athlete_run_45 = Movement(self.mod).add_fast_movement(4.5, display_name=loca[run_display_name])
        self._remarkable_athlete_run_60 = Movement(self.mod).add_fast_movement(6.0, display_name=loca[run_display_name])

        self._awareness = Awareness(self.mod).add_awareness(5)
        self._running_jump = CunningActions(self.mod).add_running_jump()

    @progression(CharacterClass.FIGHTER_CHAMPION, 3)
    def champion_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded += [
            "Assassinate_Initiative",
            "Assassinate_Ambush",
            "Assassinate_Resource",
            "DevilsSight",
            self._remarkable_athlete_run_30,
        ]
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 4)
    def champion_level_4(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            self._awareness,
            self._running_jump,
        ]
        progress.Selectors = [
            f"AddSpells({CunningActions.SPELL_LIST})",
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 5)
    def champion_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["UncannyDodge"]

    @progression(CharacterClass.FIGHTER_CHAMPION, 6)
    def champion_level_6(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 7)
    def champion_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded += ["Evasion", self._remarkable_athlete_run_45]
        progress.PassivesRemoved = [self._remarkable_athlete_run_30]

    @progression(CharacterClass.FIGHTER_CHAMPION, 8)
    def champion_level_8(self, progress: Progression) -> None:
        progress.Selectors = [
            "AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a)",  # Volley, Whirlwind
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 9)
    def champion_level_9(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 10)
    def champion_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 11)
    def champion_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ReliableTalent", self._remarkable_athlete_run_60]
        progress.PassivesRemoved = [self._remarkable_athlete_run_45]

    @progression(CharacterClass.FIGHTER_CHAMPION, 12)
    def champion_level_12(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 13)
    def champion_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 14)
    def champion_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 15)
    def champion_level_15(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 16)
    def champion_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 17)
    def champion_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 18)
    def champion_level_18(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 19)
    def champion_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 20)
    def champion_level_20(self, _: Progression) -> None:
        raise DontIncludeProgression()


def main() -> None:
    huntress = Huntress(
        classes=[CharacterClass.FIGHTER_CHAMPION],
        feats=2,
    )
    huntress.build()


if __name__ == "__main__":
    main()
