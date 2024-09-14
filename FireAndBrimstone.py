#!/usr/bin/env python3
"""
Generates files for the "FireAndBrimstone" mod.
"""

import os

from functools import cached_property
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


class FireAndBrimstone(Replacer):
    @cached_property
    def _hellcrawler(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_Hellcrawler"

        loca[f"{name}_Description"] = {"en": """
            Dragging yourself through the hells, you teleport to an unoccupied space you can see.
            """}

        self.mod.add(SpellData(
            name,
            using="Target_MAG_Legendary_HellCrawler",
            SpellType="Target",
            AIFlags="CanNotUse",
            Cooldown="",
            SpellProperties=["GROUND:TeleportSource()"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=[],
            UseCosts=["Movement:Distance*0.5"],
        ))

    @cached_property
    def _hellish_immunity(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_HellishImmunity"

        loca[f"{name}_DisplayName"] = {"en": "Hellish Immunity"}
        loca[f"{name}_Description"] = {"en": """
            You have immunity to Fire damage.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_Tiefling_HellishResistance",
            Properties=["Highlighted"],
            Boosts=["Resistance(Fire,Immune)", "StatusImmunity(BURNING)", "StatusImmunity(WILD_MAGIC_BURNING)"]
        ))

        return name

    @cached_property
    def _hellfire(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_Hellfire"

        loca[f"{name}_DisplayName"] = {"en": "Hellfire"}
        loca[f"{name}_Description"] = {"en": """
            Your <LSTag Tooltip="ProficiencyBonus">Proficiency Bonus</LSTag> is added to the damage of your Fire spells.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="Spell_Evocation_ChromaticOrb_Fire",
            Properties=["Highlighted"],
            Boosts=["IF(SpellDamageTypeIs(DamageType.Fire)):DamageBonus(ProficiencyBonus,Fire,false)"]
        ))

        return name

    @cached_property
    def _racial_spells_level_5(self) -> SpellList:
        spells = SpellList(
            Comment="Tiefling racial spells level 5",
            Spells=[self._hellcrawler],
            UUID=self.make_uuid("Tiefling racial spells level 5"),
        )
        self.mod.add(spells)
        return spells

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="FireAndBrimstone",
                         description="Enhancements for the Tiefling race.")

    @progression(CharacterRace.TIEFLING, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = ["ActionResource(Movement,9,0)", "ActionResource(Movement,1.5,0)"]
        progression.PassivesAdded = ["DevilsSight", "Tiefling_HellishResistance", self._hellfire]

    @progression(CharacterRace.TIEFLING, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Selectors = [f"AddSpells({self._racial_spells_level_5.UUID},,Charisma,,AlwaysPrepared)"]

    @progression(CharacterRace.TIEFLING, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._hellish_immunity]
        progression.PassivesRemoved = ["Tiefling_HellishResistance"]


def main():
    fire_and_brimstone = FireAndBrimstone()
    fire_and_brimstone.build()


if __name__ == "__main__":
    main()
