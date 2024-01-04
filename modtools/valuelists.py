#!/usr/bin/env python3
"""
Parser and code generator for gamedata/ValueLists.txt.
"""

import io
import os
import re

from .gamedata import GameData
from collections.abc import Callable, Iterable


class ValueLists:
    """Parser and code generator for gamedata/ValueLists.txt."""

    __valuelist_regex = re.compile("""\\s*valuelist\\s*"([^"]+)"\\s*""")
    __value_regex = re.compile("""\\s*value\\s*"([^"]+)"\\s*""")

    __validators: {str, Callable[[str | Iterable], Iterable]}

    def __init__(self):
        self.__validators = {}
        value_lists_path = GameData.get_file_path("Shared", os.path.join(
            "Public", "Shared", "Stats", "Generated", "Structure", "Base", "ValueLists.txt"))
        with open(value_lists_path, "r") as value_lists_file:
            self._parse(value_lists_file)

    def get_validator(self, valuelist: str) -> Callable[[str | Iterable], Iterable]:
        """Return the validator for the given valuelist."""
        return self.__validators[valuelist]

    def _parse(self, value_lists_file: io.TextIOWrapper) -> None:
        """Parse the gamedata/ValueLists.txt file, building our __validators."""
        valuelist: str = None
        allowed_contents = set()

        for line in value_lists_file:
            if match := ValueLists.__valuelist_regex.match(line):
                self._complete_valuelist(valuelist, allowed_contents)
                valuelist = match[1]
                allowed_contents = set()
            elif match := ValueLists.__value_regex.match(line):
                allowed_contents.add(match[1])
            elif line.strip():
                raise RuntimeError(f"Unknown line in ValueLists.txt: {line}")

        self._complete_valuelist(valuelist, allowed_contents)

    def _complete_valuelist(self, valuelist: str, allowed_contents: set) -> None:
        """Add a validator for the given valuelist and allowed_contents."""
        def validator(values: str | Iterable) -> [str]:
            """Return a list of the values that fail validation."""
            return [value for value in ([values] if isinstance(values, str) else values)
                    if allowed_contents and value not in allowed_contents]

        if valuelist:
            self.__validators[valuelist] = validator
