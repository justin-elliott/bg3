#!/usr/bin/env python3
"""
Generates files for the Best of All Worlds, a mod to give Half-Elves the features of all races.
"""

from functools import cached_property
import os

from moddb import Bolster, Knowledge
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    CharacterAbility,
    CharacterClass,
    CharacterRace,
    Progression,
    SpellList,
)
from modtools.replacers import (
    progression,
    Replacer,
)


class BestOfAllWorlds(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="BestOfAllWorlds",
                         description="Enhancements for the Half-Elf subraces.",
                         **kwds)

    @cached_property
    def _exceptional(self) -> str:
        name = self.make_name("Exceptional")
        ABILITY_BONUS = 2

        self.loca[f"{name}_DisplayName"] = "Exceptional"
        self.loca[f"{name}_Description"] = f"""
            All of your ability scores are increased by [1].
        """

        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            DescriptionParams=[f"{ABILITY_BONUS}"],
            Icon="Spell_Transmutation_EnhanceAbility",
            Boosts=[f"Ability({ability.name.title()},{ABILITY_BONUS},30)" for ability in CharacterAbility],
        ))

        return name

    @cached_property
    def _spell_list(self) -> str:
        name = f"Best of All Worlds spells"
        uuid = self.make_uuid(name)
        self.add(SpellList(
            Name=name,
            Spells=[
                Bolster(self.mod).add_bolster(),
                Knowledge(self.mod).add_knowledge_of_the_ages(),
                "Shout_Thaumaturgy",
            ],
            UUID=uuid
        ))
        return uuid

    @progression(CharacterRace.HALF_ELF, 1)
    def half_elf_level_1(self, progress: Progression) -> None:
        progress.Boosts = [
            "ActionResource(Movement,12,0)",
            "Advantage(SavingThrow,Constitution)",
            "ProficiencyBonus(Skill,Perception)",
            "ProficiencyBonus(Skill,Investigation)",
            "ProficiencyBonus(Skill,Nature)",
        ]
        progress.PassivesAdded = [
            "RockGnome_ArtificersLore",
            "Duergar_DuergarResilience",
            self._exceptional,
            "FeyAncestry",
            "Gnome_Cunning",
            "Halfling_Brave",
            "Halfling_Lucky",
            "Halfling_LightfootStealth",
            "Halfling_StoutResilience",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
            "Proficiency(Shields)",
            "RelentlessEndurance",
            "SavageAttacks",
            "SuperiorDarkvision",
            "Tiefling_HellishResistance",
        ]
        progress.Selectors = [
            f"AddSpells({self._spell_list},,Intelligence,,AlwaysPrepared)",
        ]

    @progression(CharacterRace.HALF_ELF, 3)
    def half_elf_level_3(self, progress: Progression) -> None:
        progress.Selectors = [
            "AddSpells(0c23701c-a79b-483d-b283-9f234211d979)", # Enlarge
        ]

    @progression(CharacterRace.HALF_ELF, 5)
    def half_elf_level_5(self, progress: Progression) -> None:
        progress.Selectors = [
            "AddSpells(3928cc43-fd2d-46e3-90f5-9171e3aad0f2)", # Invisibility
            "AddSpells(b5218b5e-37a6-4ff7-8821-8bead1baa9ba,,Intelligence,,AlwaysPrepared,OncePerTurnNoRealtime)", # Misty Step
        ]


if __name__ == "__main__":
    best_of_all_worlds = BestOfAllWorlds(
        classes=[CharacterClass.ROGUE],  # Ignored, but prevents multiclass slots from being updated
    )
    best_of_all_worlds.build()
