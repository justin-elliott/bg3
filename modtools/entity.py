#!/usr/bin/env python3
"""
Representation of spell and item data.
"""

# from .modifiers import Modifiers


class Entity:
    """Spell and Item data representation."""

    # __modifiers = Modifiers()

    __type: str
    __using: str
    __data: {str: str | [str]}

    def __init__(self, type: str, using: str, **kwargs: {str: str | [str]}):
        pass
