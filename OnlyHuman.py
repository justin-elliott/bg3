#!/usr/bin/env python3
"""
Generates files for the "OnlyHuman" mod.
"""

import os

from functools import cached_property
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    CharacterRace,
    Progression,
)
from modtools.replacers import (
    progression,
    Replacer,
)


class OnlyHuman(Replacer):
    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="OnlyHuman",
                         description="Enhancements for the Human race.")

    @cached_property
    def _human_versatility(self) -> dict[int, str]:
        passives = {}

        name = f"{self.mod.get_prefix()}_HumanVersatility"
        loca = self.mod.get_localization()

        loca[f"{name}_DisplayName"] = {"en": "Human Versatility"}
        for i in range(1, 5):
            level = (i - 1) * 6 if i > 1 else 1
            passives[level] = f"{name}_{level}"

            loca[f"{name}_{level}_Description"] = {"en": """
                Select [1] additional <LSTag Tooltip="Skill">Skills</LSTag> to be
                <LSTag Tooltip="Proficiency">Proficient</LSTag> in.
                All of your abilities are increased by [2].
                Your carrying capacity is increased by a quarter.
                """}

            self.mod.add(PassiveData(
                passives[level],
                DisplayName=loca[f"{name}_DisplayName"],
                Description=loca[f"{name}_{level}_Description"],
                DescriptionParams=["5", f"{i * 2}"],
                Icon="PassiveFeature_Generic_Tactical",
                Properties=["ForceShowInCC", "Highlighted"],
                Boosts=[
                    f"Ability(Strength,{i * 2})",
                    f"Ability(Dexterity,{i * 2})",
                    f"Ability(Constitution,{i * 2})",
                    f"Ability(Intelligence,{i * 2})",
                    f"Ability(Wisdom,{i * 2})",
                    f"Ability(Charisma,{i * 2})",
                    "CarryCapacityMultiplier(1.25)",
                ],
            ))

        return passives

    @progression(CharacterRace.HUMAN, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = [
            "ActionResource(Movement,9,0)",
            "ActionResource(Movement,1.5,0)",
            "Proficiency(LightArmor)",
            "Proficiency(MediumArmor)",
            "Proficiency(Shields)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
            "ProficiencyBonus(SavingThrow,Constitution)",
        ]
        progression.PassivesAdded = [self._human_versatility[1]]
        progression.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5,HumanVersatility)",
        ]

    @progression(CharacterRace.HUMAN, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = ["JackOfAllTrades"]

    @progression(CharacterRace.HUMAN, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = ["FastHands"]

    @progression(CharacterRace.HUMAN, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._human_versatility[6]]
        progression.PassivesRemoved = [self._human_versatility[1]]

    @progression(CharacterRace.HUMAN, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack", "UncannyDodge"]

    @progression(CharacterRace.HUMAN, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = ["Evasion"]

    @progression(CharacterRace.HUMAN, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack_2", "ReliableTalent"]
        progression.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterRace.HUMAN, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._human_versatility[12]]
        progression.PassivesRemoved = [self._human_versatility[6]]

    @progression(CharacterRace.HUMAN, 18)
    def level_18(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._human_versatility[18]]
        progression.PassivesRemoved = [self._human_versatility[12]]


def main():
    only_human = OnlyHuman()
    only_human.build()


if __name__ == "__main__":
    main()
