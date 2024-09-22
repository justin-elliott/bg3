#!/usr/bin/env python3
"""
Generates files for the "ChildOfTheDark" mod.
"""

import os

from functools import cached_property
from moddb import EmpoweredSpells
from modtools.gamedata import (
    PassiveData,
    SpellData,
)
from modtools.lsx.game import (
    CharacterRace,
    Progression,
    SpellList,
)
from modtools.replacers import (
    progression,
    Replacer,
)


class ChildOfTheDark(Replacer):
    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="ChildOfTheDark",
                         description="Enhancements for the Drow Half-Elf subrace.")

    EXTRA_SKILLS = 5

    @cached_property
    def _child_of_the_dark(self) -> dict[int, str]:
        passives = {}

        name = f"{self.mod.get_prefix()}_ChildOfTheDark"
        loca = self.mod.get_localization()

        loca[f"{name}_DisplayName"] = {"en": "Child of the Dark"}

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

    @cached_property
    def _harrowing_words(self) -> str:
        # Upgrade Vicious Mockery to a d6 damage cantrip.
        self.mod.add(SpellData(
            "Target_ViciousMockery",
            SpellType="Target",
            using="Target_ViciousMockery",
            SpellSuccess=[
                "ApplyStatus(VICIOUSMOCKERY,100,1)",
                "DealDamage(LevelMapValue(D6Cantrip),Psychic,Magical)",
            ],
            SpellFail=[
                "IF(HasPassive('PotentCantrip',context.Source)):"
                + "DealDamage((LevelMapValue(D6Cantrip))/2,Psychic,Magical)",
            ],
            TooltipDamageList=["DealDamage(LevelMapValue(D6Cantrip),Psychic)"],
        ))

        name = f"{self.mod.get_prefix()}_HarrowingWords"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Harrowing Words"}
        loca[f"{name}_Description"] = {"en": """
            You can cast <LSTag Type="Spell" Tooltip="Target_ViciousMockery">Vicious Mockery</LSTag> as a
            <LSTag Type="ActionResource" Tooltip="BonusActionPoint">Bonus Action</LSTag>,
            and it deals additional damage equal to your
            <LSTag Tooltip="SpellcastingAbilityModifier">Spellcasting Modifier</LSTag>.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="Spell_Enchantment_ViciousMockery",
            Properties=["ForceShowInCC", "Highlighted"],
            Boosts=[
                "IF(SpellId('Target_ViciousMockery')):DamageBonus(max(0,SpellCastingAbilityModifier))"
                "UnlockSpellVariant(SpellId('Target_ViciousMockery'),"
                + "ModifyUseCosts(Replace,BonusActionPoint,1,0,ActionPoint),ModifyTooltipDescription())",
            ],
        ))

        return name

    @cached_property
    def _vicious_mockery_spell_list(self) -> SpellList:
        vicious_mockery_spell_list = SpellList(
            Comment="Child of the Dark Vicious Mockery",
            Spells=["Target_ViciousMockery"],
            UUID=self.make_uuid("Vicious Mockery"),
        )
        self.mod.add(vicious_mockery_spell_list)
        return vicious_mockery_spell_list

    @progression(CharacterRace.HALF_ELF_DROW, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = [
            "ActionResource(Movement,1.5,0)",
            "Proficiency(MediumArmor)",
            "Proficiency(HeavyArmor)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
            "ProficiencyBonus(SavingThrow,Constitution)",
        ]
        progression.PassivesAdded = [self._child_of_the_dark[1], self._harrowing_words]
        progression.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5,ChildOfTheDark)",
            f"AddSpells({self._vicious_mockery_spell_list.UUID},,,,AlwaysPrepared,OncePerTurn)",
        ]

    @progression(CharacterRace.HALF_ELF_DROW, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = ["JackOfAllTrades"]

    @progression(CharacterRace.HALF_ELF_DROW, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = ["SculptSpells"]

    @progression(CharacterRace.HALF_ELF_DROW, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._child_of_the_dark[6], "PotentCantrip"]
        progression.PassivesRemoved = [self._child_of_the_dark[1]]

    @progression(CharacterRace.HALF_ELF_DROW, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack", "UncannyDodge"]

    @progression(CharacterRace.HALF_ELF_DROW, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            "Evasion",
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
            "FOR_NightWalkers_WebImmunity",
        ]

    @progression(CharacterRace.HALF_ELF_DROW, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = [EmpoweredSpells(self.mod).add_empowered_spells()]

    @progression(CharacterRace.HALF_ELF_DROW, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack_2", "ReliableTalent"]
        progression.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterRace.HALF_ELF_DROW, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._child_of_the_dark[12]]
        progression.PassivesRemoved = [self._child_of_the_dark[6]]

    @progression(CharacterRace.HALF_ELF_DROW, 18)
    def level_18(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._child_of_the_dark[18]]
        progression.PassivesRemoved = [self._child_of_the_dark[12]]


def main():
    child_of_the_dark = ChildOfTheDark()
    child_of_the_dark.build()


if __name__ == "__main__":
    main()
