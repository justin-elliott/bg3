#!/usr/bin/env python3
"""
Generates files for the "TheFifthElement" mod.
"""

import os

from functools import cached_property
from moddb.bolster import Bolster
from moddb.movement import Movement
from moddb.pack_mule import PackMule
from moddb.progression import multiply_resources
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
)
from modtools.lsx.game import Progression, SpellList
from modtools.mod import Mod
from modtools.progressionreplacer import class_description, class_level, ProgressionReplacer
from typing import Iterable


def manifestation_of_will(mod: Mod) -> str:
    """Add the Manifestion of Will passive, returning its name."""
    name = f"{mod.get_prefix()}_ManifestationOfWill"

    loca = mod.get_localization()
    loca[f"{name}_DisplayName"] = {"en": "Manifestation of Will"}
    loca[f"{name}_Description"] = {"en": """
        Your strength of will infuses your strikes with ki. Your unarmed attacks deal an additional [1].
        """}

    mod.add(PassiveData(
        name,
        DisplayName=loca[f"{name}_DisplayName"],
        Description=loca[f"{name}_Description"],
        DescriptionParams="DealDamage(1d4+WisdomModifier,Force)",
        Icon="Action_Barbarian_MagicAwareness",
        Properties="Highlighted",
        Boosts=[
            "IF(IsMeleeUnarmedAttack()):CharacterUnarmedDamage(1d4+WisdomModifier,Force)",
            "UnlockSpellVariant(MeleeUnarmedAttackCheck(),ModifyTargetRadius(Multiplicative,1))",
        ],
    ))

    return name


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


class TheFifthElement(ProgressionReplacer):
    _bolster: str
    _manifestation_of_will: str
    _misty_step: str
    _pack_mule: str
    _tempered_body: str

    @cached_property
    def _level_1_spelllist(self) -> str:
        spelllist = str(self.make_uuid("level_1_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Monk level 1",
            Spells=[self._bolster],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_5_spelllist(self) -> str:
        spelllist = str(self.make_uuid("level_5_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Monk level 5",
            Spells=[self._misty_step],
            UUID=spelllist,
        ))
        return spelllist

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="TheFifthElement",
                         description="Upgrades the Way of the Four Elements Monk subclass.",
                         classes=CharacterSubclasses.MONK)

        # Passives and skills
        self._bolster = Bolster(self.mod).add_bolster()
        self._manifestation_of_will = manifestation_of_will(self.mod)
        self._misty_step = Movement(self.mod).add_misty_step()
        self._pack_mule = PackMule(self.mod).add_pack_mule(2.0)
        self._tempered_body = tempered_body(self.mod)

    @class_description(CharacterClass.MONK)
    def monk_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6

    @class_level(CharacterClass.MONK, 1)
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

    @class_level(CharacterClass.MONK, 1, is_multiclass=True)
    def level_1_multiclass(self, progression: Progression) -> None:
        selectors = progression.Selectors or []
        selectors.append(f"AddSpells({self._level_1_spelllist})")
        progression.Selectors = selectors

    @class_level(CharacterClass.MONK, range(2, 13))
    def level_2_to_12_monk(self, progression: Progression) -> None:
        progression.AllowImprovement = True

    @class_level(CharacterClass.MONK_FOURELEMENTS, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Blindsight", "SuperiorDarkvision", self._pack_mule, self._tempered_body]

        selectors = self._exclude_select_spells(progression)
        selectors.extend([
            "AddSpells(9da8ef4f-676b-46f1-81e4-f7c3cfd1c34c)",  # All level 3 spells
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @class_level(CharacterClass.MONK_FOURELEMENTS, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["JackOfAllTrades"]
        progression.Selectors = self._exclude_select_spells(progression)

    @class_level(CharacterClass.MONK_FOURELEMENTS, 5)
    def level_5(self, progression: Progression) -> None:
        selectors = self._exclude_select_spells(progression)
        selectors.append(f"AddSpells({self._level_5_spelllist})")
        progression.Selectors = selectors

    @class_level(CharacterClass.MONK_FOURELEMENTS, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._manifestation_of_will]

        selectors = self._exclude_select_spells(progression)
        selectors.append("AddSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4)")  # All level 6 spells
        selectors.append("AddSpells(9487f3bd-1763-4c7f-913d-8cb7eb9052c5)")  # Wholeness of Body
        progression.Selectors = selectors

    @class_level(CharacterClass.MONK_FOURELEMENTS, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]
        progression.Selectors = self._exclude_select_spells(progression)

    @class_level(CharacterClass.MONK_FOURELEMENTS, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]
        progression.Selectors = self._exclude_select_spells(progression)

    @class_level(CharacterClass.MONK_FOURELEMENTS, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]
        progression.Selectors = self._exclude_select_spells(progression)

    @class_level(CharacterClass.MONK_FOURELEMENTS, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["Indomitable"]
        progression.Selectors = self._exclude_select_spells(progression)

    @class_level(CharacterClass.MONK_FOURELEMENTS, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

        selectors = self._exclude_select_spells(progression)
        selectors.append("AddSpells(cf014f77-4d0a-4322-a2bf-95e38b89435b)")  # All level 11 spells
        progression.Selectors = selectors

    @class_level(CharacterClass.MONK_FOURELEMENTS, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]

        selectors = self._exclude_select_spells(progression)
        selectors.append("AddSpells(964e765d-5881-463e-b1b0-4fc6b8035aa8)")  # Action Surge
        progression.Selectors = selectors

    def postprocess(self, progressions: Iterable[Progression]) -> None:
        multiply_resources(progressions, [ActionResource.KI_POINTS], 3)

    def _exclude_select_spells(self, progression: Progression) -> list[str]:
        return [selector for selector in progression.Selectors if not selector.startswith("SelectSpells")]


def main():
    the_fifth_element = TheFifthElement()
    the_fifth_element.build()


if __name__ == "__main__":
    main()
