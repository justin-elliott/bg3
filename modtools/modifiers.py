#!/usr/bin/env python3
"""
Parser and code generator for gamedata/Modifiers.txt.
"""

import io
import os
import re

from .valuelists import ValueLists
from collections.abc import Callable, Iterable


class Modifiers:
    """Parser and code generator for gamedata/Modifiers.txt."""

    __modifier_regex = re.compile("""\\s*modifier\\s+type\\s*"([^"]+)"\\s*""")
    __member_regex = re.compile("""\\s*modifier\\s*"([^"]+)"\\s*,\\s*"([^"]+)"\\s*""")

    __valuelists: ValueLists

    def __init__(self):
        self.__valuelists = ValueLists()
        with open(os.path.join(os.path.dirname(__file__), "gamedata", "Modifiers.txt"), "r") as f:
            self._parse(f)

    def _parse(self, f: io.TextIOWrapper) -> None:
        """Parse the gamedata/ValueLists.txt file, building our __validators."""
        modifier: str = None
        members: {str: Callable[[str | Iterable], None]} = {}

        for line in f:
            if (match := Modifiers.__modifier_regex.match(line)):
                self._complete_modifier(modifier, members)
                modifier = match[1]
                members = {}
            elif (match := Modifiers.__member_regex.match(line)):
                members[match[1]] = self.__valuelists.get_validator(match[2])
            elif line.strip():
                raise RuntimeError(f"Unknown line in Modifiers.txt: {line}")

        self._complete_modifier(modifier, members)

    def _complete_modifier(self, modifier: str, members: {str: Callable[[str | Iterable], None]}) -> None:
        if modifier:
            pass
