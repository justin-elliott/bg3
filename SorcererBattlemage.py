#!/usr/bin/env python3
"""
Generates files for the "SorcererBattlemage" mod.
"""

import os

from functools import cached_property
from moddb import (
    BattleMagic,
    Bolster,
    Defense,
    EmpoweredSpells,
    Movement,
    multiply_resources,
    PackMule,
    spells_always_prepared,
    storm_bolt,
)
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
)
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    class_description,
    only_existing_progressions,
    progression,
    Replacer,
    spell_list
)


class SorcererBattlemage(Replacer):
    _ACTION_RESOURCES = frozenset([ActionResource.SPELL_SLOTS, ActionResource.SORCERY_POINTS])

    # Passives
    _battle_magic: str
    _empowered_spells: str
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str
    _pack_mule: str
    _warding: str

    # Spells
    _bolster: str
    _storm_bolt: str

    @cached_property
    def _level_1_spell_list(self) -> str:
        spell_list = str(self.make_uuid("level_1_spell_list"))
        self.mod.add(SpellList(
            Comment="SorcererBattlemage level 1 spells",
            Spells=[self._bolster],
            UUID=spell_list,
        ))
        return spell_list

    @cached_property
    def _level_1_storm_sorcery_spell_list(self) -> str:
        spell_list = str(self.make_uuid("level_1_storm_sorcery_spell_list"))
        self.mod.add(SpellList(
            Comment="SorcererBattlemage level 1 Storm Sorcery spells",
            Spells=["Target_ShockingGrasp", self._storm_bolt, "Projectile_WitchBolt"],
            UUID=spell_list,
        ))
        return spell_list

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="SorcererBattlemage",
                         description="Upgrades the Sorcerer class to a Battlemage.")

        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.CHARISMA)
        self._pack_mule = PackMule(self.mod).add_pack_mule(2.0)

        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(4.5)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(6.0)

        defense = Defense(self.mod)
        self._warding = defense.add_warding()

        self._bolster = Bolster(self.mod).add_bolster()
        self._storm_bolt = storm_bolt(self.mod)

    @class_description(CharacterClass.SORCERER)
    def sorcerer_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6
        class_description.MustPrepareSpells = True
        class_description.children.append(ClassDescription.Tags(
            Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
        ))

    @spell_list("Sorcerer cantrips")
    def cantrips(self, spell_list: SpellList) -> None:
        spell_list.Spells += ["Target_Guidance", "Target_Resistance", self._storm_bolt]

    @spell_list("Sorcerer SLevel 2 expanded")
    @spell_list("Sorcerer SLevel 3")
    @spell_list("Sorcerer SLevel 4")
    @spell_list("Sorcerer SLevel 5")
    @spell_list("Sorcerer SLevel 6")
    def spell_lists_with_enhance_ability(self, spell_list: SpellList) -> None:
        spell_list.Spells.append("Target_EnhanceAbility")

    @progression(CharacterSubclasses.SORCERER, range(1, 13))
    @only_existing_progressions
    def level_1_to_12_resources(self, progression: Progression) -> None:
        multiply_resources(progression, self._ACTION_RESOURCES, 2)
        spells_always_prepared(progression)

    @progression(CharacterClass.SORCERER, range(2, 13))
    def level_2_to_12_improvement(self, progression: Progression) -> None:
        progression.AllowImprovement = True

    @progression(CharacterClass.SORCERER, 1)
    def level_1(self, progression: Progression) -> None:
        for proficiency in ["LightArmor", "MediumArmor", "HeavyArmor", "Shields", "SimpleWeapons", "MartialWeapons"]:
            progression.Boosts.append(f"Proficiency({proficiency})")

        for proficiency in ["Daggers", "Quarterstaffs", "LightCrossbows"]:
            progression.Boosts.remove(f"Proficiency({proficiency})")

        selectors = [selector for selector in progression.Selectors if not selector.startswith("SelectSkills")]
        selectors.extend([
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @progression(CharacterClass.SORCERER, 1)
    @progression(CharacterClass.SORCERER, 1, is_multiclass=True)
    def level_1_multiclass(self, progression: Progression) -> None:
        progression.PassivesAdded += [
            self._battle_magic,
            self._fast_movement_30,
            self._pack_mule,
            "SculptSpells",
            self._warding,
        ]
        progression.Selectors += [
            f"AddSpells({self._level_1_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_STORM, 1)
    def level_1_storm_sorcery(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_1_storm_sorcery_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["Blindsight", "SuperiorDarkvision"]

    @progression(CharacterClass.SORCERER, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["JackOfAllTrades"]

    @progression(CharacterClass.SORCERER, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]

    @progression(CharacterClass.SORCERER, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack", self._fast_movement_45]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [self._fast_movement_30]

    @progression(CharacterClass.SORCERER, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["PotentCantrip"]

    @progression(CharacterClass.SORCERER, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]

    @progression(CharacterClass.SORCERER, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]

    @progression(CharacterClass.SORCERER, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical", self._fast_movement_60]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [self._fast_movement_45]

    @progression(CharacterClass.SORCERER, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._empowered_spells]

    @progression(CharacterClass.SORCERER, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
        ]

    @progression(CharacterClass.SORCERER, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(964e765d-5881-463e-b1b0-4fc6b8035aa8,,,,AlwaysPrepared)",  # Action Surge
        ]


if __name__ == "__main__":
    sorcerer_battlemage = SorcererBattlemage()
    sorcerer_battlemage.build()
