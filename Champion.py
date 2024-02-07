#!/usr/bin/env python3
"""
Generates files for the "Champion" mod.
"""

import os

from modtools.lsx.game import CharacterClass, CharacterSubclasses
from modtools.lsx.game import Progression
from modtools.progressionreplacer import class_level, ProgressionReplacer


class Champion(ProgressionReplacer):
    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Champion",
                         classes=CharacterSubclasses.FIGHTER)

    @class_level(CharacterClass.FIGHTER, levels=range(1, 13))
    @class_level(CharacterClass.FIGHTER, 1, is_multiclass=True)
    def fighter_levels(self, progression: Progression):
        progression.AllowImprovement = (progression.Level > 1)
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 3)
    def level_3(self, progression: Progression):
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 4)
    def level_4(self, progression: Progression):
        progression = progression or self._make_progression(4)
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 5)
    def level_5(self, progression: Progression):
        progression = progression or self._make_progression(5)
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 6)
    def level_6(self, progression: Progression):
        progression = progression or self._make_progression(6)
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 7)
    def level_7(self, progression: Progression):
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 8)
    def level_8(self, progression: Progression):
        progression = progression or self._make_progression(8)
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 9)
    def level_9(self, progression: Progression):
        progression = progression or self._make_progression(9)
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 10)
    def level_10(self, progression: Progression):
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 11)
    def level_11(self, progression: Progression):
        progression = progression or self._make_progression(11)
        return progression

    @class_level(CharacterClass.FIGHTER_CHAMPION, 12)
    def level_12(self, progression: Progression):
        progression = progression or self._make_progression(12)
        return progression

    def _make_progression(self, level: int) -> Progression:
        return Progression(
            Name=CharacterClass.FIGHTER_CHAMPION,
            Level=level,
            ProgressionType=1,
            TableUUID="9b2ff703-7924-4a66-b119-ae4d716a4522",
            UUID=self.make_uuid(f"Champion:{level}"),
        )


champion = Champion()
champion.build()
