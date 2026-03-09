#!/usr/bin/env python3
"""
Sorcery-related features for Baldur's Gate 3 mods.
"""
from functools import cached_property

from modtools.gamedata import SpellData, StatusData
from modtools.mod import Mod

class Sorcery:
    """Sorcery-related features for Baldur's Gate 3 mods."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    def increase_create_sorcery_points(self, multiplier: int) -> None:
        for level in range(1, 10):
            self._create_sorcery_points(level, multiplier)
            self._create_spell_slot(level, multiplier)

    @cached_property
    def _create_sorcery_points_description(self) -> str:
        name = self._mod.make_name("Description")
        self._mod.loca[name] = """
            Spend a Level [1] <LSTag Tooltip="SpellSlot">spell slot</LSTag> to gain [2] Sorcery Points.
        """
        return self._mod.loca[name]

    def _create_sorcery_points(self, level: int, multiplier: int) -> None:
        spell_name = f"Shout_CreateSorceryPoints_{level}"
        status_name = f"SORCERYPOINT_{level}"
        boost = level * multiplier
        self._mod.loca[spell_name] = f"Create Sorcery Points: {level}"
        self._mod.add(SpellData(
            spell_name,
            SpellType="Shout",
            using=spell_name,
            DisplayName=self._mod.loca[spell_name],
            Description=self._create_sorcery_points_description,
            DescriptionParams=[level, boost],
        ))
        self._mod.add(StatusData(
            status_name,
            StatusType="BOOST",
            using=status_name,
            DescriptionParams=[boost],
            Boosts=[f"ActionResource(SorceryPoint,{boost},0)"],
        ))
    
    def _create_spell_slot(self, level: int, multiplier: int) -> None:
        spell_name = f"Shout_CreateSpellSlot_{level}"
        status_name = f"SPELLSLOT_{level}"
        if level < 6:
            self._create_spell_slot_1_to_5(spell_name, level)
        else:
            self._create_spell_slot_6_to_9(spell_name, status_name, level)
        self._create_spell_slot_status(status_name, level, multiplier)
    
    def _create_spell_slot_1_to_5(self, spell_name: str, level: int) -> None:
        spell_name = f"Shout_CreateSpellSlot_{level}"
        self._mod.add(SpellData(
            spell_name,
            SpellType="Shout",
            using=spell_name,
            DescriptionParams=[level, level],
            UseCosts=["BonusActionPoint:1", f"SorceryPoint:{level}"],
        ))
    
    def _create_spell_slot_6_to_9(self, spell_name: str, status_name: str, level: int) -> None:
        self._mod.loca[f"{spell_name}_DisplayName"] = f"Create Spell Slot: Level {level}"
        self._mod.add(SpellData(
            spell_name,
            SpellType="Shout",
            using="Shout_CreateSpellSlot_5",
            DisplayName=self._mod.loca[f"{spell_name}_DisplayName"],
            DescriptionParams=[level, level],
            PowerLevel=level,
            SpellProperties=[f"ApplyStatus({status_name},100,-1)"],
            UseCosts=["BonusActionPoint:1", f"SorceryPoint:{level}"],
        ))
    
    def _create_spell_slot_status(self, status_name: str, level: int, multiplier: int) -> None:
        self._mod.add(StatusData(
            status_name,
            StatusType="BOOST",
            using="SPELLSLOT_1",
            DescriptionParams=[level],
            Boosts=[f"ActionResource(SpellSlot,{multiplier},{level})"],
        ))

