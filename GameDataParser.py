#!/usr/bin/env python3
"""
Parser for the ValueLists.txt file.
"""

import argparse
import inspect
import os
import re
import sys

import modtools.valuelists_v2 as VL

from collections.abc import Callable, Mapping, Set
from modtools.prologue import PYTHON_PROLOGUE
from modtools.unpak import Unpak
from pathlib import PurePath
from typing import ClassVar


PROLOGUE = f'''\
{PYTHON_PROLOGUE}
"""
A class representing game data, together with definitions parsed from Modifiers.txt.
"""

import modtools.valuelists_v2 as VL

from collections.abc import Callable, Set
from typing import ClassVar


'''

MODIFIERS_PATH = "Shared.pak/Public/Shared/Stats/Generated/Structure/Modifiers.txt"


class GameData:
    """Representation of game data ("Modifiers")."""

    _LIST_TYPES = (list, tuple, set)

    _id_: ClassVar[str]                      # The data's id attribute (defaulting to the subclass name).
    _fields_: ClassVar[dict[str, Set[str]]]  # The data's field definitions.

    name: str
    using: str

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._id_ = str(cls.__dict__.get("_id_", cls.__name__))
        cls._fields_ = dict()

        for member_name, value in list(cls.__dict__.items()):
            if value in VL.VALUELISTS:
                cls._fields_[member_name.replace(" ", "_")] = value

        for member_name in cls._fields_:
            getter, setter = cls._wrap_accessors(member_name)
            prop = property(fget=getter, fset=setter)
            setattr(cls, member_name, prop)

    def __init__(self, name: str, **kwds):
        self.name = name
        self.using = None

        for key, value in kwds.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        """Returns a game data string."""
        s = f"new entry \"{self.name}\"\n"
        s += f"type \"{self._id_}\"\n"
        if self.using:
            s += f"using \"{self.using}\"\n"
        for key in self._fields_.keys():
            if (values := getattr(self, key, None)) is not None:
                if len(values) == 1:
                    values = values[0]
                else:
                    values = ";".join(values)
                s += f"data \"{key.replace("_", " ")}\" \"{values}\"\n"
        return s

    @classmethod
    def _wrap_accessors(cls, member_name: str) -> tuple[Callable[[object], any],
                                                        Callable[[object, any], None]]:
        private_member = "_" + member_name
        member_type = cls._fields_[member_name]

        def getter(obj: object) -> list[str] | None:
            return obj.__dict__.get(private_member)

        def setter(obj: object, values: list[str] | None) -> None:
            if values is not None:
                if not isinstance(values, cls._LIST_TYPES):
                    values = [value for value in str(values).split(";") if value]
                values = [str(member_type(value)) for value in values]
            obj.__dict__[private_member] = values

        return (getter, setter)


class GameDataParser:
    """Parse the Modifiers.txt file."""
    _MODIFIER_REGEX = re.compile("""\\s*modifier\\s+type\\s*"([^"]+)"\\s*""")
    _MEMBER_REGEX = re.compile("""\\s*modifier\\s*"([^"]+)"\\s*,\\s*"([^"]+)"\\s*""")

    _modifiers_path: os.PathLike

    def __init__(self, unpak: Unpak):
        pak_name, _, relative_path = str(PurePath(MODIFIERS_PATH).as_posix()).partition("/")
        cached_pak = unpak.get(pak_name)
        self._modifiers_path = os.path.join(cached_pak.path, relative_path)

    def parse(self, output: str | None):
        if output:
            output_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "modtools", output))
        else:
            output_path = None

        modifiers: Mapping[str, Mapping[str, str]] = {}
        modifier: str = None
        members: Mapping[str, str] = {}

        with open(self._modifiers_path, "r") as modifiers_file:
            for line in modifiers_file:
                if match := self._MODIFIER_REGEX.match(line):
                    if modifier:
                        modifiers[modifier] = members
                    modifier = match[1]
                    members = {}
                    if modifier == "Object":
                        modifier = "ObjectData"
                        members = {"_id_": "Object"}
                elif match := self._MEMBER_REGEX.match(line):
                    members[match[1].replace(" ", "_")] = match[2].replace(" ", "")
                elif line.strip():
                    raise RuntimeError(f"Unknown line in Modifiers.txt: {line}")

        if modifier is not None:
            modifiers[modifier] = members

        with (open(output_path, "w") if output_path is not None else sys.stdout) as f:
            f.write(PROLOGUE)
            f.write(inspect.getsource(GameData))

            for modifier, members in sorted(modifiers.items()):
                f.write("\n\n")
                f.write(f"class {modifier}(GameData):\n")
                if "_id_" in members:
                    f.write(f"    _id_ = \"{members["_id_"]}\"\n")
                for member, member_type in sorted(members.items()):
                    if member != "_id_":
                        f.write(f"    {member}: VL.{member_type} = VL.{member_type}\n")


def main():
    parser = argparse.ArgumentParser(description="Generate GameData definitions from the Modifiers.txt file.")
    parser.add_argument("-o", "--output", type=str, default=None, help="Name of the output file.")
    args = parser.parse_args()

    unpak = Unpak(cache_dir=None)
    parser = GameDataParser(unpak)
    parser.parse(args.output)


if __name__ == "__main__":
    main()
