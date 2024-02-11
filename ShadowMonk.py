#!/usr/bin/env python3
"""
Generates files for the "ShadowMonk" mod.
"""

import os

from functools import cached_property
from moddb.bolster import Bolster
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
from modtools.progressionreplacer import (
    class_description,
    class_level,
    ProgressionReplacer,
)
from typing import Iterable


def cloak_of_shadows(mod: Mod) -> None:
    """Modify the existing Cloak of Shadows spell, removing the obscured requirement."""
    mod.add(PassiveData(
        "Shout_CloakOfShadows_Monk",
        using="Shout_CloakOfShadows_Monk",
        SpellType="Shout",
        SpellProperties=["ApplyStatus(GREATER_INVISIBILITY,100,-1)"],
        TooltipStatusApply=["ApplyStatus(GREATER_INVISIBILITY,100,-1)"],
        RequirementConditions="",
        RequirementEvents="",
    ))


def shadow_step(mod: Mod) -> None:
    """Modify the existing Shadow Step spell, removing the obscured requirement."""
    mod.add(PassiveData(
        "Target_ShadowStep",
        using="Target_ShadowStep",
        SpellType="Target",
        RequirementConditions="",
        RequirementEvents="",
        TargetConditions="",
    ))


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


class ShadowMonk(ProgressionReplacer):
    _bolster: str
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

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="ShadowMonk",
                         description="Upgrades the Way of Shadow Monk.",
                         classes=CharacterSubclasses.MONK)

        # Passives
        self._pack_mule = PackMule(self.mod).add_pack_mule(2.0)
        self._tempered_body = tempered_body(self.mod)

        # Spells
        self._bolster = Bolster(self.mod).add_bolster()
        cloak_of_shadows(self.mod)
        shadow_step(self.mod)

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
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_1_spelllist})",
        ]

    @class_level(CharacterClass.MONK, range(2, 13))
    def level_2_to_12_monk(self, progression: Progression) -> None:
        progression.AllowImprovement = True

    @class_level(CharacterClass.MONK_SHADOW, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Blindsight", "SuperiorDarkvision", self._pack_mule, self._tempered_body]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["FlurryOfBlowsUnlock"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(6566d841-ef96-4e13-ac40-c40f44c5e08b)"  # Open Hand: Topple, Stagger, Push
        ]

    @class_level(CharacterClass.MONK_SHADOW, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Assassinate_Resource", "JackOfAllTrades"]

    @class_level(CharacterClass.MONK_SHADOW, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(fab9f457-4570-472e-95be-ffe5b5aa863d)",  # Infiltration Expertise
        ]

    @class_level(CharacterClass.MONK_SHADOW, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Manifestation_of_Body", "Manifestation_of_Mind", "Manifestation_of_Soul"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(9487f3bd-1763-4c7f-913d-8cb7eb9052c5)",  # Wholeness of Body
        ]

    @class_level(CharacterClass.MONK_SHADOW, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]

    @class_level(CharacterClass.MONK_SHADOW, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["FastHands"]

    @class_level(CharacterClass.MONK_SHADOW, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["BrutalCritical"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(0ffe7be9-d826-42d7-b59e-d1924ad28ffc)",  # Ki Resonation
        ]

    @class_level(CharacterClass.MONK_SHADOW, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["Indomitable"]

    @class_level(CharacterClass.MONK_SHADOW, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]

    @class_level(CharacterClass.MONK_SHADOW, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(964e765d-5881-463e-b1b0-4fc6b8035aa8)",  # Action Surge
        ]

    def postprocess(self, progressions: Iterable[Progression]) -> None:
        multiply_resources(progressions, [ActionResource.KI_POINTS], 4)

    def make_progression(self, character_class: CharacterClass, level: int) -> Progression:
        assert character_class == CharacterClass.MONK_SHADOW
        return Progression(
            Name=str(character_class),
            Level=level,
            ProgressionType=1,
            TableUUID="6e1a1046-1202-410b-9d80-91c819a8bcca",
            UUID=self.make_uuid(f"Shadow Monk Level {level}")
        )


def main():
    shadow_monk = ShadowMonk()
    shadow_monk.build()


if __name__ == "__main__":
    main()
