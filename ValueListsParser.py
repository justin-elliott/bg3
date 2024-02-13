#!/usr/bin/env python3
"""
Parser for the ValueLists.txt file.
"""

import argparse
import os
import re
import sys

from collections.abc import Set
from modtools.prologue import PYTHON_PROLOGUE
from modtools.unpak import Unpak
from typing import TextIO


PROLOGUE = f'''\
{PYTHON_PROLOGUE}
"""
A class representing ValueLists, together with definitions parsed from ValueLists.txt.
"""

from enum import StrEnum

'''

VALUE_LISTS_PATH = "Shared.pak/Public/Shared/Stats/Generated/Structure/Base/ValueLists.txt"


class ValueListsParser:
    """Parse the ValueLists.txt file."""
    _VALUELIST_REGEX = re.compile("""\\s*valuelist\\s*"([^"]+)"\\s*""")
    _VALUE_REGEX = re.compile("""\\s*value\\s*"([^"]+)"\\s*""")

    _value_lists_path: os.PathLike

    def __init__(self, unpak: Unpak):
        self._value_lists_path = unpak.get_path(VALUE_LISTS_PATH)

    def parse(self, output: str | None):
        if output:
            output_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "modtools", output))
        else:
            output_path = None

        valuelists: dict[str, Set[str]] = {}
        name: str = None
        valid_values: Set[str] = set()

        with open(self._value_lists_path, "r") as value_lists_file:
            for line in value_lists_file:
                if match := self._VALUELIST_REGEX.match(line):
                    if name:
                        valuelists[name] = valid_values
                    name = match[1]
                    valid_values = set()
                elif match := self._VALUE_REGEX.match(line):
                    valid_values.add(match[1])
                elif line.strip():
                    raise RuntimeError(f"Unknown line in ValueLists.txt: {line}")

            if name:
                valuelists[name] = valid_values

        with (open(output_path, "w") if output_path is not None else sys.stdout) as f:
            f.write(PROLOGUE)
            for name, valid_values in sorted(valuelists.items()):
                self._write_valuelist(f, name, valid_values)
            f.write("\n")
            f.write("VALUELISTS = [\n")
            for name in sorted(valuelists.keys()):
                f.write(f"    {name.replace(" ", "")},\n")
            f.write("]\n")

    def _write_valuelist(self, f: TextIO, name: str, valid_values: Set[str]) -> None:
        """Create a class representing the valuelist."""
        class_name = name.replace(" ", "")
        f.write("\n")
        if len(valid_values) == 0:
            f.write(f"class {class_name}(str):\n")
            f.write("    pass\n")
        elif all(value.replace(" ", "").upper().isidentifier() for value in valid_values):
            # Create an enum
            f.write(f"class {class_name}(StrEnum):\n")
            for value in sorted(valid_values):
                f.write(f"    {value.replace(" ", "").upper()} = \"{value}\"\n")
        else:
            f.write(f"class {class_name}(str):\n")
            f.write("    _VALID_VALUES = {\n")
            for value in sorted(valid_values):
                f.write(f"        \"{value}\",\n")
            f.write("    }\n")
            f.write("\n")
            f.write("    def __new__(cls, value: str):\n")
            f.write("        value = str(value)\n")
            f.write("        if value not in cls._VALID_VALUES:\n")
            f.write(f"            raise KeyError(f\"{{value}} is not a member of {class_name}\")\n")
            f.write("        return super().__new__(cls, value)\n")
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Generate ValueLists definitions from the ValueLists.txt file.")
    parser.add_argument("-o", "--output", type=str, default=None, help="Name of the output file.")
    args = parser.parse_args()

    unpak = Unpak(cache_dir=None)
    parser = ValueListsParser(unpak)
    parser.parse(args.output)


if __name__ == "__main__":
    main()
