#!/usr/bin/env python3
"""
Parser for the ValueLists.txt file.
"""

import argparse
import os
import re
import sys

from collections import OrderedDict
from collections.abc import Set
from modtools.unpak import Unpak
from pathlib import PurePath


PROLOGUE = '''\
#!/usr/bin/env python3
"""
A class representing ValueLists, together with definitions parsed from ValueLists.txt.
"""

'''

VALUE_LISTS_PATH = "Shared.pak/Public/Shared/Stats/Generated/Structure/Base/ValueLists.txt"


class ValueListsParser:
    """Parse the ValueLists.txt file."""
    _VALUELIST_REGEX = re.compile("""\\s*valuelist\\s*"([^"]+)"\\s*""")
    _VALUE_REGEX = re.compile("""\\s*value\\s*"([^"]+)"\\s*""")

    _value_lists_path: os.PathLike

    def __init__(self, unpak: Unpak):
        pak_name, _, relative_path = str(PurePath(VALUE_LISTS_PATH).as_posix()).partition("/")
        cached_pak = unpak.get(pak_name)
        self._value_lists_path = os.path.join(cached_pak.path, relative_path)

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
                    self._complete_valuelist(valuelists, name, valid_values)
                    name = match[1]
                    valid_values = set()
                elif match := self._VALUE_REGEX.match(line):
                    valid_values.add(match[1])
                elif line.strip():
                    raise RuntimeError(f"Unknown line in ValueLists.txt: {line}")

            self._complete_valuelist(valuelists, name, valid_values)

        with (open(output_path, "w") if output_path is not None else sys.stdout) as f:
            f.write(PROLOGUE)
            for name, valid_values in sorted(valuelists.items()):
                quoted_valid_values = ", ".join(f'"{value}"' for value in sorted(valid_values))
                if len(quoted_valid_values) > 80:
                    quoted_valid_values = "\n    " + quoted_valid_values.replace(", ", ",\n    ") + "\n"
                f.write(f"{name.replace(" ", "")} = {{{quoted_valid_values}}}\n")

    def _complete_valuelist(self,
                            valuelists: dict[str, Set[str]],
                            name: str | None,
                            valid_values: Set[str]) -> None:
        """Create a new valuelist with the given allowed contents."""
        if name:
            if "None" in valid_values:
                valid_values.add("")  # An empty string is synonymous with "None"
            valuelists[name] = valid_values


def main():
    parser = argparse.ArgumentParser(description="Generate ValueLists definitions from the ValueLists.txt file.")
    parser.add_argument("-o", "--output", type=str, default=None, help="Name of the output file.")
    args = parser.parse_args()

    unpak = Unpak(cache_dir=None)
    parser = ValueListsParser(unpak)
    parser.parse(args.output)


if __name__ == "__main__":
    main()
