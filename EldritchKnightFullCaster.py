#!/usr/bin/env python3
"""
Generates files for the "EldritchKnightFullCaster" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import EmpoweredSpells, Movement
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import (
    CharacterAbility,
    CharacterClass,
    ClassDescription,
    Progression,
)
from modtools.replacers import (
    class_description,
    DontIncludeProgression,
    only_existing_progressions,
    progression,
    Replacer,
    eldritch_knight_cantrips,
    eldritch_knight_level_1_spells,
    eldritch_knight_level_2_spells,
    wizard_cantrips,
    wizard_level_1_spells,
    wizard_level_2_spells,
    wizard_level_3_spells,
    wizard_level_4_spells,
    wizard_level_5_spells,
    wizard_level_6_spells,
)


class EldritchKnightFullCaster(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="EldritchKnightFullCaster",
                         description="Full casting for the Eldritch Knight subclass.",
                         **kwds)

    @class_description(CharacterClass.FIGHTER_ELDRITCHKNIGHT)
    def eldritch_knight_description(self, class_description: ClassDescription) -> None:
        class_description.MulticlassSpellcasterModifier = 1.0

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, range(3, 21))
    @only_existing_progressions
    def level_3_to_20(self, progress: Progression) -> None:
        progress.Selectors = [
            selector for selector in (progress.Selectors or [])
            if not selector.startswith(f"SelectSpells({eldritch_knight_cantrips(self).UUID}")
            and not selector.startswith(f"SelectSpells({eldritch_knight_level_1_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({eldritch_knight_level_2_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_cantrips(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_1_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_2_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_3_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_4_spells(self).UUID}")
        ] or None

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 3)
    def level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            "DevilsSight",
            "SculptSpells",
        ]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},4,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},4,0)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 4)
    def level_4(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_2_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 5)
    def level_5(self, progress: Progression) -> None:
        progress.PassivesAdded += ["UncannyDodge"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_3_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 6)
    def level_6(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_3_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["PotentCantrip"]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 7)
    def level_7(self, progress: Progression) -> None:
        progress.PassivesAdded += ["Evasion"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 8)
    def level_8(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 9)
    def level_9(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_5_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 10)
    def level_10(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_5_spells(self).UUID},1,1)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["EmpoweredEvocation"]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 11)
    def level_11(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ReliableTalent"]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 12)
    def level_12(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 13)
    def level_13(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 14)
    def level_14(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 15)
    def level_15(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 16)
    def level_16(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 17)
    def level_17(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 18)
    def level_18(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 19)
    def level_19(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 20)
    def level_20(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]


def main():
    eldritch_knight_full_caster = EldritchKnightFullCaster(
        classes=[CharacterClass.FIGHTER_ELDRITCHKNIGHT],
        spells=2,
        full_caster=True,
    )
    eldritch_knight_full_caster.build()


if __name__ == "__main__":
    main()
