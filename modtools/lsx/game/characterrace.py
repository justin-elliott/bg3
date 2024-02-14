#!/usr/bin/env python3
"""
Character races enumeration.
"""

from enum import StrEnum
from typing import Final


class CharacterRace(StrEnum):
    """Baldur's Gate 3 character races as found in Progressions.lsx."""
    DRAGONBORN = "Dragonborn"
    DRAGONBORN_BLACK = "BlackDragonborn"
    DRAGONBORN_BLUE = "BlueDragonborn"
    DRAGONBORN_BRASS = "BrassDragonborn"
    DRAGONBORN_BRONZE = "BronzeDragonborn"
    DRAGONBORN_COPPER = "CopperDragonborn"
    DRAGONBORN_GOLD = "GoldDragonborn"
    DRAGONBORN_GREEN = "GreenDragonborn"
    DRAGONBORN_RED = "RedDragonborn"
    DRAGONBORN_SILVER = "SilverDragonborn"
    DRAGONBORN_WHITE = "WhiteDragonborn"

    DROW = "Drow"
    DROW_LOLTH = "LolthDrow"
    DROW_SELDARINE = "SeldarineDrow"

    DWARF = "Dwarf"
    DWARF_HILL = "HillDwarf"
    DWARF_MOUNTAIN = "MountainDwarf"
    DWARF_DUERGAR = "DWARF_DUERGAR"

    ELF = "Elf"
    ELF_HIGH = "HighElf"
    ELF_WOOD = "WoodElf"

    GITHYANKI = "Githyanki"

    GNOME = "Gnome"
    GNOME_DEEP = "DeepGnome"
    GNOME_FOREST = "ForestGnome"
    GNOME_ROCK = "RockGnome"

    HALF_ELF = "HalfElf"
    HALF_ELF_DROW = "HalfDrow"
    HALF_ELF_HIGH = "HighHalfElf"
    HALF_ELF_WOOD = "WoodHalfElf"

    HALF_ORC = "HalfOrc"

    HALFLING = "Halfling"
    HALFLING_LIGHTFOOT = "LightfootHalfing"
    HALFLING_STOUT = "StoutHalfling"

    HUMAN = "Human"

    TIEFLING = "Tiefling"
    TIEFLING_ASMODEUS = "AsmodeusTiefling"
    TIEFLING_MEPHISTOPHELES = "MephistophelesTiefling"
    TIEFLING_ZARIEL = "ZarielTiefling"


BASE_CHARACTER_RACES: Final = frozenset([
    CharacterRace.DRAGONBORN,
    CharacterRace.DROW,
    CharacterRace.DWARF,
    CharacterRace.ELF,
    CharacterRace.GITHYANKI,
    CharacterRace.GNOME,
    CharacterRace.HALFLING,
    CharacterRace.HALF_ELF,
    CharacterRace.HALF_ORC,
    CharacterRace.HUMAN,
    CharacterRace.TIEFLING,
])


class CharacterSubraces:
    """Sets of character race and subraces by primary race."""
    DRAGONBORN: Final = frozenset([
        CharacterRace.DRAGONBORN,
        CharacterRace.DRAGONBORN_BLACK,
        CharacterRace.DRAGONBORN_BLUE,
        CharacterRace.DRAGONBORN_BRASS,
        CharacterRace.DRAGONBORN_BRONZE,
        CharacterRace.DRAGONBORN_COPPER,
        CharacterRace.DRAGONBORN_GOLD,
        CharacterRace.DRAGONBORN_GREEN,
        CharacterRace.DRAGONBORN_RED,
        CharacterRace.DRAGONBORN_SILVER,
        CharacterRace.DRAGONBORN_WHITE,
    ])
    DROW: Final = frozenset([
        CharacterRace.DROW,
        CharacterRace.DROW_LOLTH,
        CharacterRace.DROW_SELDARINE,
    ])
    DWARF: Final = frozenset([
        CharacterRace.DWARF,
        CharacterRace.DWARF_HILL,
        CharacterRace.DWARF_MOUNTAIN,
        CharacterRace.DWARF_DUERGAR,
    ])
    ELF: Final = frozenset([
        CharacterRace.ELF,
        CharacterRace.ELF_HIGH,
        CharacterRace.ELF_WOOD,
    ])
    GITHYANKI: Final = frozenset([
        CharacterRace.GITHYANKI,
    ])
    GNOME: Final = frozenset([
        CharacterRace.GNOME,
        CharacterRace.GNOME_DEEP,
        CharacterRace.GNOME_FOREST,
        CharacterRace.GNOME_ROCK,
    ])
    HALF_ELF: Final = frozenset([
        CharacterRace.HALF_ELF,
        CharacterRace.HALF_ELF_DROW,
        CharacterRace.HALF_ELF_HIGH,
        CharacterRace.HALF_ELF_WOOD,
    ])
    HALF_ORC: Final = frozenset([
        CharacterRace.HALF_ORC,
    ])
    HALFLING: Final = frozenset([
        CharacterRace.HALFLING,
        CharacterRace.HALFLING_LIGHTFOOT,
        CharacterRace.HALFLING_STOUT,
    ])
    HUMAN: Final = frozenset([
        CharacterRace.HUMAN,
    ])
    TIEFLING: Final = frozenset([
        CharacterRace.TIEFLING,
        CharacterRace.TIEFLING_ASMODEUS,
        CharacterRace.TIEFLING_MEPHISTOPHELES,
        CharacterRace.TIEFLING_ZARIEL,
    ])
    ALL: Final = (DRAGONBORN | DROW | DWARF | ELF | GITHYANKI | GNOME | HALF_ELF | HALF_ORC | HALFLING | HUMAN |
                  TIEFLING)
