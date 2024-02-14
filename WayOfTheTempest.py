#!/usr/bin/env python3
"""
Generates files for the "WayOfTheTempest" mod.
"""

import os

from functools import cached_property
from moddb.bolster import Bolster
from moddb.pack_mule import PackMule
from moddb.progression import multiply_resources
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
    update_action_resources,
)
from modtools.lsx.game import Progression, SpellList
from modtools.mod import Mod
from modtools.replacers import (
    class_description,
    progression,
    Replacer,
)
from typing import Iterable


def tempered_body(mod: Mod) -> str:
    """Add the Tempered Body passive, returning its name."""
    name = f"{mod.get_prefix()}_TemperedBody"

    loca = mod.get_localization()
    loca[f"{name}_DisplayName"] = {"en": "Tempered Body"}
    loca[f"{name}_Description"] = {"en": """
        Through training, you have gained resistance to all forms of damage. Incoming damage is reduced by [1].
        """}

    mod.add(PassiveData(
        name,
        DisplayName=loca[f"{name}_DisplayName"],
        Description=loca[f"{name}_Description"],
        DescriptionParams=["RegainHitPoints(max(1,ClassLevel(Monk)))"],
        Icon="PassiveFeature_Durable",
        Properties=["Highlighted"],
        Boosts=["DamageReduction(All,Flat,ClassLevel(Monk))"],
    ))

    return name


def tempestuous_flight(mod: Mod) -> str:
    """Add the Tempestuous Flight spell, returning its name."""
    name = f"{mod.get_prefix()}_TempestuousFlight"

    loca = mod.get_localization()
    loca[f"{name}_DisplayName"] = {"en": "Tempestuous Flight"}
    loca[f"{name}_Description"] = {"en": "Call on the winds to fly you to your destination."}

    mod.add(SpellData(
        name,
        using="Projectile_Fly_TempestuousMagic",
        SpellType="Projectile",
        DisplayName=loca[f"{name}_DisplayName"],
        Description=loca[f"{name}_Description"],
        SpellFlags=[
            "IsJump",
            "HasHighGroundRangeExtension",
            "IgnoreVisionBlock",
            "RangeIgnoreVerticalThreshold",
            "Stealth",
            "Invisible",
            "CannotTargetCharacter",
            "CannotTargetItems",
            "NoAOEDamageOnLand",
        ],
        TargetRadius=18,
        UseCosts=["Movement:Distance*0.5"],
    ))

    return name


class WayOfTheTempest(Replacer):
    _bolster: str
    _pack_mule: str
    _tempered_body: str
    _tempestuous_flight: str

    @cached_property
    def _level_1_spelllist(self) -> str:
        spelllist = str(self.make_uuid("level_1_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Monk level 1",
            Spells=[self._bolster],
            UUID=spelllist,
        ))
        return spelllist

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="WayOfTheTempest",
                         description="Changes the Way of Shadow Monk to the Way of the Tempest.")

        # Passives
        self._pack_mule = PackMule(self.mod).add_pack_mule(2.0)
        self._tempered_body = tempered_body(self.mod)

        # Spells
        self._bolster = Bolster(self.mod).add_bolster()
        self._tempestuous_flight = tempestuous_flight(self.mod)

    @class_description(CharacterClass.MONK)
    def monk_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6

    @class_description(CharacterClass.MONK_SHADOW)
    def way_of_the_tempest_description(self, class_description: ClassDescription) -> None:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_DisplayName"] = {"en": "Way of the Tempest"}
        loca[f"{self.mod.get_prefix()}_Description"] = {"en": """
            You channel your ki into electrifying strikes and thunderous blows, leaving foes trembling in the wake of
            your martial maelstrom.
            """}

        class_description.DisplayName = loca[f"{self.mod.get_prefix()}_DisplayName"]
        class_description.Description = loca[f"{self.mod.get_prefix()}_Description"]

        class_description.CanLearnSpells = True
        class_description.MustPrepareSpells = True

    @progression(CharacterClass.MONK, 1)
    def level_1(self, progression: Progression) -> None:
        # Add common features
        self.level_1_multiclass(progression)

        selectors = progression.Selectors or []
        selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
        selectors.extend([
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @progression(CharacterClass.MONK, 1, is_multiclass=True)
    def level_1_multiclass(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_1_spelllist},,,,AlwaysPrepared)",
        ]
        self._increase_ki_points(progression)

    @progression(CharacterClass.MONK, range(2, 13))
    def level_2_to_12_monk(self, progression: Progression) -> None:
        progression.AllowImprovement = True
        self._increase_ki_points(progression)

    @progression(CharacterClass.MONK_SHADOW, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Blindsight", "SuperiorDarkvision", self._pack_mule, self._tempered_body]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["FlurryOfBlowsUnlock"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(6566d841-ef96-4e13-ac40-c40f44c5e08b,,,,AlwaysPrepared)"  # Open Hand: Topple, Stagger, Push
        ]

    @progression(CharacterClass.MONK_SHADOW, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Assassinate_Resource", "JackOfAllTrades"]

    @progression(CharacterClass.MONK_SHADOW, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(fab9f457-4570-472e-95be-ffe5b5aa863d,,,,AlwaysPrepared)",  # Infiltration Expertise
        ]

    @progression(CharacterClass.MONK_SHADOW, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Manifestation_of_Body", "Manifestation_of_Mind", "Manifestation_of_Soul"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(9487f3bd-1763-4c7f-913d-8cb7eb9052c5,,,,AlwaysPrepared)",  # Wholeness of Body
        ]

    @progression(CharacterClass.MONK_SHADOW, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]

    @progression(CharacterClass.MONK_SHADOW, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]

    @progression(CharacterClass.MONK_SHADOW, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(0ffe7be9-d826-42d7-b59e-d1924ad28ffc,,,,AlwaysPrepared)",  # Ki Resonation
        ]

    @progression(CharacterClass.MONK_SHADOW, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["Indomitable"]

    @progression(CharacterClass.MONK_SHADOW, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    @progression(CharacterClass.MONK_SHADOW, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(964e765d-5881-463e-b1b0-4fc6b8035aa8,,,,AlwaysPrepared)",  # Action Surge
        ]

    def _increase_ki_points(self, progression: Progression):
        if progression.Boosts:
            progression.Boosts = update_action_resources(progression.Boosts or [],
                                                         [ActionResource.KI_POINTS],
                                                         lambda _1, count, _2: count * 4)


def main():
    way_of_the_tempest = WayOfTheTempest()
    way_of_the_tempest.build()


if __name__ == "__main__":
    main()
