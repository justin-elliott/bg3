#!/usr/bin/env python3

import os

from functools import cached_property
from moddb import Movement
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
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
    def _displacement_display_name(self) -> str:
        return self.loca("Displacement_DisplayName", "Displacement")

    @cached_property
    def _displacement_description(self) -> str:
        return self.loca("Displacement_Description", """
                Attackers have <LSTag Tooltip="Disadvantage">Disadvantage</LSTag> on
                <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag> against you.
                Your <LSTag Tooltip="ProficiencyBonus">Proficiency Bonus</LSTag> is added to your Initiative rolls,
                and you can't be <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>.
            """)

    @cached_property
    def _displacement(self) -> str:
        name = self.make_name("Displacement")
        self.add(PassiveData(
            name,
            DisplayName=self._displacement_display_name,
            Description=self._displacement_description,
            Icon="Spell_Illusion_Blur",
            Boosts=[
                "Disadvantage(AttackTarget)",
                "Initiative(2)",
                "StatusImmunity(SURPRISED)",
                "IF(CharacterLevelGreaterThan(4)):Initiative(1)",
                "IF(CharacterLevelGreaterThan(8)):Initiative(1)",
                "IF(CharacterLevelGreaterThan(11)):Initiative(1)"
            ],
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
    def _misty_step(self) -> str:
        return Movement(self.mod).add_misty_step("Movement:Distance*0.5")

    @cached_property
    def _quickened(self) -> str:
        name = self.make_name("Quickened")
        self.add(PassiveData(
            name,
            using="Metamagic_Quickened",
            DisplayName=self.loca("Quickened_DisplayName", "Quickened Spell"),
            Description=self.loca("Quickened_Description", """
                Spells that cost an action cost a bonus action instead.
            """),
            Boosts=[
                "UnlockSpellVariant(QuickenedSpellCheck(),ModifyUseCosts(Replace,BonusActionPoint,1,0,ActionPoint))",
            ],
            EnabledConditions=[],
        ))
        return name
    
    @cached_property
    def _twinned(self) -> str:
        name = self.make_name("Twinned")
        self.add(PassiveData(
            name,
            using="Metamagic_Twinned",
            DisplayName=self.loca("Twinned_DisplayName", "Twinned Spell"),
            Description=self.loca("Twinned_Description", """
                Spells that only target 1 creature can target an additional creature.
            """),
            Boosts=[
                "UnlockSpellVariant(TwinnedProjectileSpellCheck(),ModifyNumberOfTargets(AdditiveBase,1,false))",
                "UnlockSpellVariant(TwinnedTargetSpellCheck(),ModifyNumberOfTargets(AdditiveBase,1,false))",
                "UnlockSpellVariant(TwinnedTargetTouchSpellCheck(),ModifyNumberOfTargets(AdditiveBase,1,false))",
            ],
            EnabledConditions=[],
        ))
        return name

    @cached_property
    def _alter_time(self) -> str:
        name = self.make_name("AlterTime")
        self.add(PassiveData(
            name,
            DisplayName=self.loca("AlterTime_DisplayName", "Alter Time"),
            Description=self.loca("AlterTime_Description", """
                Your <LSTag Type="Spell" Tooltip="Target_Haste">Haste</LSTag> and
                <LSTag Type="Spell" Tooltip="Target_Slow">Slow</LSTag> spells do not require
                <LSTag Tooltip="Concentration">concentration</LSTag>.
            """),
            Icon="Spell_Transmutation_Slow",
            Boosts=[
                "UnlockSpellVariant("
                +   "SpellId('Target_Haste') or SpellId('Target_Slow'),"
                +   "ModifySpellFlags(Concentration,0)"
                + ")",
            ],
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _level_3_spelllist(self) -> str:
        name = "Chronomage Level 3 Spells"
        uuid = self.make_uuid(name)
        self.add(SpellList(
            Name=name,
            Spells=[self._misty_step],
            UUID=uuid,
        ))
        return uuid

    @cached_property
    def _level_5_spelllist(self) -> str:
        name = "Chronomage Level 5 Spells"
        uuid = self.make_uuid(name)
        self.add(SpellList(
            Name=name,
            Spells=["Target_Haste", "Target_Slow"],
            UUID=uuid,
        ))
        return uuid

    @progression(CharacterClass.WIZARD_DIVINATION, 2)
    def divinationschool_level_2(self, progress: Progression) -> None:
        progress.PassivesAdded += [self._displacement, self._twinned]

    @progression(CharacterClass.WIZARD_DIVINATION, 3)
    def divinationschool_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._quickened]
        progress.Selectors += [f"AddSpells({self._level_3_spelllist},,,,AlwaysPrepared)"]

    @progression(CharacterClass.WIZARD_DIVINATION, 5)
    def divinationschool_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._alter_time]
        progress.Selectors += [f"AddSpells({self._level_5_spelllist},,,,AlwaysPrepared)"]


def main() -> None:
    chronomage = Chronomage(
        classes=[CharacterClass.WIZARD_DIVINATION],
    )
    chronomage.build()


if __name__ == "__main__":
    main()
