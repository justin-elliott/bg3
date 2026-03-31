#!/usr/bin/env python3

import os

from functools import cached_property
from moddb import Awareness, Movement
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    progression,
    Replacer,
)


class Chronomage(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Chronomage",
                         description="A class replacer for DivinationSchool.",
                         **kwds)

    @cached_property
    def _alter_time_1(self) -> str:
        name = self.make_name("AlterTime_1")
        self.add(PassiveData(
            name,
            DisplayName=self.loca(f"{name}_DisplayName", "Alter Time"),
            Description=self.loca(f"{name}_Description", """
                Time bends to your will. You gain an additional <LSTag Tooltip="Action">action</LSTag> each turn.
            """),
            Icon="Spell_Transmutation_Slow",
            Boosts=["ActionResource(ActionPoint,1,0)"],
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _alter_time_2(self) -> str:
        name = self.make_name("AlterTime_2")
        self.add(PassiveData(
            name,
            using=self._alter_time_1,
            Description=self.loca(f"{name}_Description", """
                Time bends to your will. You gain two additional <LSTag Tooltip="Action">actions</LSTag> each turn.
            """),
            Boosts=["ActionResource(ActionPoint,2,0)"],
        ))
        return name

    @cached_property
    def _awareness(self) -> str:
        return Awareness(self.mod).add_awareness()

    @cached_property
    def _displacement_display_name(self) -> str:
        return self.loca("Displacement_DisplayName", "Displacement")

    @cached_property
    def _displacement_description(self) -> str:
        return self.loca("Displacement_Description", """
            Attackers have <LSTag Tooltip="Disadvantage">Disadvantage</LSTag> on
            <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag> against you.
        """)

    @cached_property
    def _displacement(self) -> str:
        name = self.make_name("Displacement")
        self.add(PassiveData(
            name,
            DisplayName=self._displacement_display_name,
            Description=self._displacement_description,
            Icon="Spell_Illusion_Blur",
            Boosts=["Disadvantage(AttackTarget)"],
            Properties=["Highlighted"],
            StatsFunctorContext=["OnCombatStarted"],
            StatsFunctors=[f"ApplyStatus(SELF,{self._displacement_status},100,-1)"],
        ))
        return name

    @cached_property
    def _displacement_status(self) -> str:
        name = self.make_name("Displacement").upper()
        self.add(StatusData(
            name,
            StatusType="BOOST",
            DisplayName=self._displacement_display_name,
            Description=self._displacement_description,
            Icon="Spell_Illusion_Blur",
            RemoveEvents=["OnCombatEnded"],
            StatusEffect="d37fab67-6932-44c4-995e-f051d7027fc5",
            StatusPropertyFlags=["DisableOverhead", "DisableCombatlog", "DisablePortraitIndicator"],
        ))
        return name

    @cached_property
    def _fast_movement_30(self) -> str:
        return self._movement.add_fast_movement(3.0)

    @cached_property
    def _fast_movement_45(self) -> str:
        return self._movement.add_fast_movement(4.5)

    @cached_property
    def _fast_movement_60(self) -> str:
        return self._movement.add_fast_movement(6.0)

    @cached_property
    def _movement(self) -> Movement:
        return Movement(self.mod)

    @cached_property
    def _warp(self) -> str:
        return self._movement.add_misty_step(
            display_name="Warp",
            description="""
                You warp space around you to to reappear in an unoccupied space you can see.
            """,
            icon="Action_WildMagic_Teleport",
            use_costs="Movement:Distance*0.5")

    @cached_property
    def _level_3_spelllist(self) -> str:
        name = "Chronomage Level 3 Spells"
        uuid = self.make_uuid(name)
        self.add(SpellList(
            Name=name,
            Spells=[self._warp],
            UUID=uuid,
        ))
        return uuid

    @progression(CharacterClass.WIZARD_DIVINATION, 2)
    def divinationschool_level_2(self, progress: Progression) -> None:
        progress.Boosts += ["ProficiencyBonus(SavingThrow,Constitution)"]
        progress.PassivesAdded += [
            self._awareness,
            self._displacement,
            self._fast_movement_30,
            "JackOfAllTrades",
        ]
        progress.Selectors += ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)"]

    @progression(CharacterClass.WIZARD_DIVINATION, 3)
    def divinationschool_level_3(self, progress: Progression) -> None:
        progress.Selectors += [f"AddSpells({self._level_3_spelllist},,,,AlwaysPrepared)"]

    @progression(CharacterClass.WIZARD_DIVINATION, 5)
    def divinationschool_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._alter_time_1]

    @progression(CharacterClass.WIZARD_DIVINATION, 7)
    def divinationschool_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_45]
        progress.PassivesRemoved = [self._fast_movement_30]

    @progression(CharacterClass.WIZARD_DIVINATION, 9)
    def divinationschool_level_9(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ReliableTalent"]

    @progression(CharacterClass.WIZARD_DIVINATION, 11)
    def divinationschool_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._alter_time_2]
        progress.PassivesRemoved = [self._alter_time_1]

    @progression(CharacterClass.WIZARD_DIVINATION, 12)
    def divinationschool_level_12(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_60]
        progress.PassivesRemoved = [self._fast_movement_45]


def main() -> None:
    chronomage = Chronomage(classes=[CharacterClass.WIZARD_DIVINATION])
    chronomage.build()


if __name__ == "__main__":
    main()
