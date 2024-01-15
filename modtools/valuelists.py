#!/usr/bin/env python3
"""
Parser and code generator for Shared.pak ValueLists.txt.
"""

import io
import os
import re

from modtools.unpak import Unpak
from collections.abc import Mapping, Set


class ValueLists:
    """Parser and code generator for Shared.pak ValueLists.txt."""

    __valuelist_regex = re.compile("""\\s*valuelist\\s*"([^"]+)"\\s*""")
    __value_regex = re.compile("""\\s*value\\s*"([^"]+)"\\s*""")

    __valuelists: Mapping[str, Set[str]]

    def __init__(self, unpak: Unpak):
        self.__valuelists = {}
        shared_pak = unpak.get("Shared")
        value_lists_path = os.path.join(shared_pak.path, "Public/Shared/Stats/Generated/Structure/Base/ValueLists.txt")
        with open(value_lists_path, "r") as value_lists_file:
            self._parse(value_lists_file)

    def get_valid_values(self, valuelist: str) -> Set[str]:
        """Return the set of valid values in a valuelist. An empty set indicates that any value is acceptable."""
        return self.__valuelists[valuelist]

    def _parse(self, value_lists_file: io.TextIOWrapper) -> None:
        """Parse the ValueLists.txt file, building our __valuelists."""
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

    def _complete_valuelist(self, valuelist: str | None, allowed_contents: Set[str]) -> None:
        """Create a new valuelist with the given allowed contents."""
        if valuelist:
            if "None" in allowed_contents:
                allowed_contents.add("")  # An empty string is synonymous with "None"
            self.__valuelists[valuelist] = allowed_contents
