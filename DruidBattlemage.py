#!/usr/bin/env python3
"""
Generates files for the "DruidBattlemage" mod.
"""

import os

from functools import cached_property
from moddb import (
    BattleMagic,
    Bolster,
    Defense,
    EmpoweredSpells,
    Movement,
    PackMule,
    multiply_resources,
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
)
from uuid import UUID


class DruidBattlemage(Replacer):
    _battle_magic: str
    _bolster: str
    _empowered_spells: str
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str
    _pack_mule: str

    @cached_property
    def _natural_resistance(self) -> str:
        """Add the Natural Resistance passive, returning its name."""
        prefix = f"{self.mod.get_prefix()}_NaturalResistance"

        loca = self.mod.get_localization()
        loca[f"{prefix}_DisplayName"] = {"en": "Natural Resistance"}
        loca[f"{prefix}_Description"] = {"en": """
            You are naturally resistant to all forms of damage. Incoming damage is reduced by [1].
            """}

        return Defense(self.mod).add_warding(
            display_name_handle=loca[f"{prefix}_DisplayName"],
            description_handle=loca[f"{prefix}_Description"],
            icon="PassiveFeature_Durable",
        )

    @cached_property
    def _level_1_spelllist(self) -> str:
        spelllist = str(self.make_uuid("level_1_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Druid level 1",
            Spells=[self._bolster, "Shout_Shield_Wizard"],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_3_spelllist(self) -> str:
        spelllist = str(self.make_uuid("level_3_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Druid level 3",
            Spells=["Shout_Dash_BonusAction"],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_5_spelllist(self) -> str:
        spelllist = str(self.make_uuid("level_5_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Druid level 5",
            Spells=["Target_Counterspell"],
            UUID=spelllist,
        ))
        return spelllist

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="DruidBattlemage",
                         mod_uuid=UUID("a5ffe54f-736e-44a1-8814-76c128875bbc"),
                         description="Upgrades the Druid class to a Battlemage.")

        # Passives and skills
        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)
        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(4.5)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(6.0)
        self._pack_mule = PackMule(self.mod).add_pack_mule(2.0)

        # Spells
        self._bolster = Bolster(self.mod).add_bolster()

    @class_description(CharacterClass.DRUID)
    def druid_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6
        class_description.children.append(
            ClassDescription.Tags(Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"),  # WIZARD
        )

    @progression(CharacterClass.DRUID, 1)
    def level_1(self, progression: Progression) -> None:
        # Add common features
        self.level_1_multiclass(progression)

        boosts = progression.Boosts or []
        boosts = [boost for boost in boosts if not boost.startswith("Proficiency")]
        boosts += [
            "ProficiencyBonus(SavingThrow,Constitution)",
            "ProficiencyBonus(SavingThrow,Wisdom)",
            "Proficiency(LightArmor)",
            "Proficiency(MediumArmor)",
            "Proficiency(Shields)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
        ]
        progression.Boosts = boosts

        selectors = progression.Selectors or []
        selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
        selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]
        progression.Selectors = selectors

    @progression(CharacterClass.DRUID, 1, is_multiclass=True)
    def level_1_multiclass(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._battle_magic,
            self._fast_movement_30,
            self._natural_resistance,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_1_spelllist},,,,AlwaysPrepared)",
        ]

    @progression(CharacterSubclasses.DRUID, range(1, 13))
    @only_existing_progressions
    def level_1_to_12_druid(self, progression: Progression) -> None:
        if progression.Name == CharacterClass.DRUID:
            progression.AllowImprovement = True if progression.Level > 1 else None
        multiply_resources(progression,
                           [ActionResource.SPELL_SLOTS,
                            ActionResource.FUNGAL_INFESTATION_CHARGES,
                            ActionResource.NATURAL_RECOVERY_CHARGES,
                            ActionResource.WILD_SHAPE_CHARGES],
                           2)

    @progression(CharacterClass.DRUID, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["Blindsight", "SuperiorDarkvision"]

    @progression(CharacterClass.DRUID, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["JackOfAllTrades"]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_3_spelllist},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.DRUID, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]

    @progression(CharacterClass.DRUID, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ExtraAttack",
            self._fast_movement_45,
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_30,
        ]

        selectors = progression.Selectors or []
        selectors.append(f"AddSpells({self._level_5_spelllist},,,,AlwaysPrepared)")
        progression.Selectors = selectors

    @progression(CharacterClass.DRUID, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["PotentCantrip"]

    @progression(CharacterClass.DRUID, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]

    @progression(CharacterClass.DRUID, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "FastHands",
            self._fast_movement_60,
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_45,
        ]

    @progression(CharacterClass.DRUID, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]

    @progression(CharacterClass.DRUID, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._empowered_spells, "ExtraAttack_2", "NaturesWard"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    @progression(CharacterClass.DRUID, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]

        selectors = progression.Selectors or []
        selectors.append("AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a,,,,AlwaysPrepared)")  # Volley, Whirlwind
        progression.Selectors = selectors

    @progression(CharacterClass.DRUID, 12)
    def level_12(self, progression: Progression) -> None:
        selectors = progression.Selectors or []
        selectors.append("AddSpells(964e765d-5881-463e-b1b0-4fc6b8035aa8,,,,AlwaysPrepared)")  # Action Surge
        progression.Selectors = selectors


def main():
    druid_battlemage = DruidBattlemage()
    druid_battlemage.build()


if __name__ == "__main__":
    main()
