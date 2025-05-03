#!/usr/bin/env python3
"""
Character ability enumeration.
"""

from enum import IntEnum


class CharacterAbility(IntEnum):
    """Character ability numbering."""
    STRENGTH = 1
    DEXTERITY = 2
    CONSTITUTION = 3
    INTELLIGENCE = 4
    WISDOM = 5
    CHARISMA = 6
