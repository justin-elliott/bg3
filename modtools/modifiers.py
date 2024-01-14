#!/usr/bin/env python3
"""
Parser and code generator for Shared.pak Modifiers.txt.
"""

import io
import os
import re

from modtools.unpak import Unpak
from collections.abc import Mapping


class Modifiers:
    """Parser and code generator for Shared.pak Modifiers.txt."""

    type Modifier = Mapping[str, str]  # {member_name: valuelist}

    __modifier_regex = re.compile("""\\s*modifier\\s+type\\s*"([^"]+)"\\s*""")
    __member_regex = re.compile("""\\s*modifier\\s*"([^"]+)"\\s*,\\s*"([^"]+)"\\s*""")

    __modifiers: Mapping[str, Modifier]  # {modifier_name: Modifier}

    def __init__(self, unpak: Unpak):
        """Create a Modifier instance.

        method_target -- the object in which to create functions implementing the modifiers
        """
        self.__modifiers = {}

        modifiers_path = unpak.get_file_path("Shared:Public/Shared/Stats/Generated/Structure/Modifiers.txt")
        with open(modifiers_path, "r") as f:
            self._parse(f)

    def get_modifier(self, modifier_name: str) -> Modifier:
        """Get a modifier."""
        return self.__modifiers[modifier_name]

    def _parse(self, f: io.TextIOWrapper) -> None:
        """Parse the Modifiers.txt file, building our __modifiers."""
        modifier: str = None
        members: {str: str} = {}

        for line in f:
            if match := Modifiers.__modifier_regex.match(line):
                if modifier is not None:
                    self.__modifiers[modifier] = members
                modifier = match[1]
                members = {}
            elif match := Modifiers.__member_regex.match(line):
                members[match[1].replace(" ", "_")] = match[2]
            elif line.strip():
                raise RuntimeError(f"Unknown line in Modifiers.txt: {line}")

        if modifier is not None:
            self.__modifiers[modifier] = members
