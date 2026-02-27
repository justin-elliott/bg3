#!/usr/bin/env python3

import os

from functools import cached_property
from modtools.gamedata import SpellData, StatusData
from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)
from typing import ClassVar


class CreateSorceryPoints(Replacer):
    _multiplier: ClassVar[int] = 2

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         description="A class replacer for Sorcerer.",
                         **kwds)
        
        for level in range(1, 10):
            self._create_sorcery_points(level)
            self._create_spell_slot(level)

    def generate_name(self) -> str:
        """Generate a name for the Mod."""
        return f"CreateSorceryPoints_x{self._multiplier}"

    @cached_property
    def _create_sorcery_points_description(self) -> str:
        name = self.make_name("Description")
        self.loca[name] = """
            Spend a Level [1] <LSTag Tooltip="SpellSlot">spell slot</LSTag> to gain [2] Sorcery Points.
        """
        return self.loca[name]

    def _create_sorcery_points(self, level: int) -> None:
        spell_name = f"Shout_CreateSorceryPoints_{level}"
        status_name = f"SORCERYPOINT_{level}"
        boost = level * self._multiplier

        self.add(SpellData(
            spell_name,
            SpellType="Shout",
            using=spell_name,
            Description=self._create_sorcery_points_description,
            DescriptionParams=[level, boost],
        ))

        self.add(StatusData(
            status_name,
            StatusType="BOOST",
            using=status_name,
            DescriptionParams=[boost],
            Boosts=[f"ActionResource(SorceryPoint,{boost},0)"],
        ))
    
    def _create_spell_slot(self, level: int) -> None:
        spell_name = f"Shout_CreateSpellSlot_{level}"
        status_name = f"SPELLSLOT_{level}"

        if level < 6:
            self.add(SpellData(
                spell_name,
                SpellType="Shout",
                using=spell_name,
                DescriptionParams=[level, level],
                UseCosts=["BonusActionPoint:1", f"SorceryPoint:{level}"],
            ))
        else:
            self.loca[f"{spell_name}_DisplayName"] = f"Create Spell Slot: Level {level}"
            self.add(SpellData(
                spell_name,
                SpellType="Shout",
                using="Shout_CreateSpellSlot_5",
                DisplayName=self.loca[f"{spell_name}_DisplayName"],
                DescriptionParams=[level, level],
                PowerLevel=level,
                SpellProperties=[f"ApplyStatus({status_name},100,-1)"],
                UseCosts=["BonusActionPoint:1", f"SorceryPoint:{level}"],
            ))
            self.add(StatusData(
                status_name,
                StatusType="BOOST",
                using="SPELLSLOT_1",
                DescriptionParams=[level],
                Boosts=[f"ActionResource(SpellSlot,1,{level})"],
            ))


def main() -> None:
    create_sorcery_points = CreateSorceryPoints(
        classes=[CharacterClass.SORCERER],
        spells=2,
        actions=2,
    )
    create_sorcery_points.build()


if __name__ == "__main__":
    main()
