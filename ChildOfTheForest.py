#!/usr/bin/env python3
"""
Generates files for the "ChildOfTheForest" mod.
"""

import os

from functools import cached_property
from modtools.gamedata import (
    PassiveData,
)
from modtools.lsx.game import (
    CharacterRace,
    Progression,
)
from modtools.replacers import (
    progression,
    Replacer,
)


class ChildOfTheForest(Replacer):
    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="ChildOfTheForest",
                         description="Enhancements for the Wood Half-Elf subrace.")

    EXTRA_SKILLS = 5

    @cached_property
    def _child_of_the_forest(self) -> dict[int, str]:
        passives = {}

        name = f"{self.mod.get_prefix()}_ChildOfTheForest"
        loca = self.mod.get_localization()

        loca[f"{name}_DisplayName"] = {"en": "Child of the Forest"}

        for bonus, level in [(2 * i, level) for i, level in enumerate([1, 6, 12, 18], start=1)]:
            passives[level] = f"{name}_{level}"

            loca[f"{name}_{level}_Description"] = {"en": """
                Select [1] additional <LSTag Tooltip="Skill">Skills</LSTag> to be
                <LSTag Tooltip="Proficiency">Proficient</LSTag> in.
                All of your abilities are increased by [2].
                """}

            self.mod.add(PassiveData(
                passives[level],
                DisplayName=loca[f"{name}_DisplayName"],
                Description=loca[f"{name}_{level}_Description"],
                DescriptionParams=[self.EXTRA_SKILLS, bonus],
                Icon="PassiveFeature_Generic_Tactical",
                Properties=["ForceShowInCC", "Highlighted"],
                Boosts=[
                    f"Ability(Strength,{bonus})",
                    f"Ability(Dexterity,{bonus})",
                    f"Ability(Constitution,{bonus})",
                    f"Ability(Intelligence,{bonus})",
                    f"Ability(Wisdom,{bonus})",
                    f"Ability(Charisma,{bonus})",
                ],
            ))

        return passives

    @progression(CharacterRace.HALF_ELF_WOOD, 1)
    def level_1(self, progression: Progression) -> None:
        SKILLS = ["Acrobatics", "SleightOfHand", "Stealth", "Perception", "Survival"]
        progression.Boosts = [
            "ActionResource(Movement,1.5,0)",
            *[f"Advantage(Skill,{skill})" for skill in SKILLS],
            *[f"ProficiencyBonus(Skill,{skill})" for skill in SKILLS],
            *[f"ExpertiseBonus({skill})" for skill in SKILLS],
        ]
        progression.PassivesAdded = [self._child_of_the_forest[1]]
        progression.Selectors = [
            f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self.EXTRA_SKILLS},ChildOfTheForest)",
        ]

    @progression(CharacterRace.HALF_ELF_WOOD, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = ["JackOfAllTrades"]

    @progression(CharacterRace.HALF_ELF_WOOD, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = ["FastHands"]

    @progression(CharacterRace.HALF_ELF_WOOD, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = ["FeralInstinct"]

    @progression(CharacterRace.HALF_ELF_WOOD, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack", "UncannyDodge"]

    @progression(CharacterRace.HALF_ELF_WOOD, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._child_of_the_forest[6]]
        progression.PassivesRemoved = [self._child_of_the_forest[1]]

    @progression(CharacterRace.HALF_ELF_WOOD, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            "Evasion",
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
            "FOR_NightWalkers_WebImmunity",
        ]

    @progression(CharacterRace.HALF_ELF_WOOD, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack_2", "ReliableTalent"]
        progression.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterRace.HALF_ELF_WOOD, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._child_of_the_forest[12]]
        progression.PassivesRemoved = [self._child_of_the_forest[6]]

    @progression(CharacterRace.HALF_ELF_WOOD, 18)
    def level_18(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._child_of_the_forest[18]]
        progression.PassivesRemoved = [self._child_of_the_forest[12]]


def main():
    child_of_the_forest = ChildOfTheForest()
    child_of_the_forest.build()


if __name__ == "__main__":
    main()
