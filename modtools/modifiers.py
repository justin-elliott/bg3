#!/usr/bin/env python3
"""
Parser and code generator for gamedata/Modifiers.txt.
"""

import io
import os
import re

from .prologue import TXT_PROLOGUE
from .valuelists import ValueLists
from collections.abc import Callable, Iterable


class Modifiers:
    """Parser and code generator for gamedata/Modifiers.txt."""

    __modifier_regex = re.compile("""\\s*modifier\\s+type\\s*"([^"]+)"\\s*""")
    __member_regex = re.compile("""\\s*modifier\\s*"([^"]+)"\\s*,\\s*"([^"]+)"\\s*""")

    __modifier_filename = {
        "Character": "Character.txt",
        "Armor": "Armor.txt",
        "Object": "Object.txt",
        "Weapon": "Weapon.txt",
        "SpellData": ("SpellType", lambda key: f"Spell_{key}.txt"),
        "StatusData": ("StatusType", lambda key: f"Status_{key}.txt"),
        "PassiveData": "Passive.txt",
        "InterruptData": "Interrupt.txt",
        "CriticalHitTypeData": "CriticalHitTypes.txt",
    }

    __method_target: type[any]
    __modifiers: {str: {str: str | Iterable}}
    __valuelists: ValueLists

    def __init__(self, method_target: type[any]):
        """Create a Modifier instance.

        method_target -- the object in which to create functions implementing the modifiers
        """
        self.__method_target = method_target
        self.__modifiers = {}
        self.__valuelists = ValueLists()

        with open(os.path.join(os.path.dirname(__file__), "gamedata", "Modifiers.txt"), "r") as f:
            self._parse(f)

    def build(self, mod_dir: str, folder: str) -> None:
        """Build all modifier files in the given mod_dir, folder."""
        files = {}
        for name in self.__modifiers.keys():
            files.setdefault(self._modifier_filename(name), []).append(name)

        data_dir = os.path.join(mod_dir, "Public", folder, "Stats", "Generated", "Data")
        os.makedirs(data_dir, exist_ok=True)

        for filename, modifier_names in files.items():
            with open(os.path.join(data_dir, filename), "w") as f:
                self._write_modifiers(f, modifier_names)

    def _write_modifiers(self, f: io.TextIOWrapper, modifier_names: [str]) -> None:
        """Build the modifiers specific to a file."""
        f.write(TXT_PROLOGUE)
        self._write_modifier(f, modifier_names[0])
        for name in modifier_names[1:]:
            f.write("\n")
            self._write_modifier(f, name)

    def _write_modifier(self, f: io.TextIOWrapper, name: str) -> None:
        """Write a single modifier to a file."""
        modifier = self.__modifiers[name].copy()

        # Output the prologue in a fixed order
        f.write(f"""new entry "{name}"\n""")
        type = modifier.pop("type")
        f.write(f"""type "{type}"\n""")
        if spell_type := modifier.pop("SpellType", None):
            f.write(f"""data "SpellType" "{spell_type}"\n""")
        if status_type := modifier.pop("StatusType", None):
            f.write(f"""data "StatusType" "{status_type}"\n""")
        if using := modifier.pop("using", None):
            f.write(f"""using "{using}"\n""")

        # Output the remaining members in sorted order
        for member in sorted(modifier.keys()):
            value = modifier[member]
            if not isinstance(value, str):
                value = ";".join(value)
            f.write(f"""data "{member}" "{value}"\n""")

    def _parse(self, f: io.TextIOWrapper) -> None:
        """Parse the gamedata/ValueLists.txt file, building our __validators."""
        modifier: str = None
        members: {str: Callable[[str | Iterable], bool]} = {}

        for line in f:
            if match := Modifiers.__modifier_regex.match(line):
                self._complete_modifier(modifier, members)
                modifier = match[1]
                members = {}
            elif match := Modifiers.__member_regex.match(line):
                members[match[1]] = self.__valuelists.get_validator(match[2])
            elif line.strip():
                raise RuntimeError(f"Unknown line in Modifiers.txt: {line}")

        self._complete_modifier(modifier, members)

    def _complete_modifier(self, modifier: str, members: {str: Callable[[str | Iterable], None]}) -> None:
        """Add a function implementing the given modifier and members."""
        def impl(name: str, using: str = None, **kwargs):
            assert all([key in members and members[key](value) for key, value in kwargs.items()])
            self.__modifiers[name] = {"type": modifier, "using": using, **kwargs}

        if modifier:
            setattr(self.__method_target, modifier, impl)

    def _modifier_filename(self, name: str) -> str:
        """Get the filename corresponding to the given name."""
        modifier = self.__modifiers[name]
        filename = self.__modifier_filename[modifier["type"]]
        if isinstance(filename, str):
            return filename
        key, make = filename
        sub_type = modifier[key]
        return make(sub_type)
