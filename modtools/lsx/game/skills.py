#!/usr/bin/env python3
"""
Skills enumeration.
"""

from modtools.lsx.game.characterability import CharacterAbility

from enum import StrEnum
from typing import Final


class Skills(StrEnum):
    """Character skill names."""
    ATHLETICS = "Athletics"
    ACROBATICS = "Acrobatics"
    SLEIGHT_OF_HAND = "SleightOfHand"
    STEALTH = "Stealth"
    ARCANA = "Arcana"
    HISTORY = "History"
    INVESTIGATION = "Investigation"
    NATURE = "Nature"
    RELIGION = "Religion"
    ANIMAL_HANDLING = "AnimalHandling"
    INSIGHT = "Insight"
    MEDICINE = "Medicine"
    PERCEPTION = "Perception"
    SURVIVAL = "Survival"
    DECEPTION = "Deception"
    INTIMIDATION = "Intimidation"
    PERFORMANCE = "Performance"
    PERSUASION = "Persuasion"


class SkillGroups:
    """Sets of skills by ability."""
    STRENGTH: Final = frozenset([
        Skills.ATHLETICS,
    ])
    DEXTERITY: Final = frozenset([
        Skills.ACROBATICS,
        Skills.SLEIGHT_OF_HAND,
        Skills.STEALTH,
    ])
    CONSTITUTION: Final = frozenset([
    ])
    INTELLIGENCE: Final = frozenset([
        Skills.ARCANA,
        Skills.HISTORY,
        Skills.INVESTIGATION,
        Skills.NATURE,
        Skills.RELIGION,
    ])
    WISDOM: Final = frozenset([
        Skills.ANIMAL_HANDLING,
        Skills.INSIGHT,
        Skills.MEDICINE,
        Skills.PERCEPTION,
        Skills.SURVIVAL,
    ])
    CHARISMA: Final = frozenset([
        Skills.DECEPTION,
        Skills.INTIMIDATION,
        Skills.PERFORMANCE,
        Skills.PERSUASION,
    ])

    def __class_getitem__(cls, ability: CharacterAbility) -> frozenset[Skills]:
        return vars(cls)[ability.name]
