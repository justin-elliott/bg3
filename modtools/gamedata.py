#!/usr/bin/env python3
"""
Representation of spell and item data.
"""

import io
import os

from modtools.modifiers import Modifiers
from modtools.prologue import TXT_PROLOGUE
from modtools.valuelists import ValueLists
from collections.abc import Iterable, Mapping


class GameDatum:
    """Spell and Item data representation."""

    type Members = Mapping[str, str | Iterable[str]]  # {member_name: value | [values]}

    __prologue_entries = set([".name", ".type", ".using", "SpellType", "StatusType"])

    __members: Members

    def __init__(self, members: Members):
        self.__members = members

    def __getitem__(self, member_name: str) -> str | Iterable[str]:
        return self.__members[member_name]

    def validate(self, modifiers: Modifiers, valuelists: ValueLists) -> None:
        """Validate the GameDatum against the modifiers and valuelists, raising an exception on a mismatch."""
        my_name = self.__members[".name"]
        my_type = self.__members[".type"]

        modifier = modifiers.get_modifier(my_type)

        for member_name, values in self.__members.items():
            if not member_name.startswith("."):
                valuelist = modifier.get(member_name, None)
                if valuelist is None:
                    raise KeyError(f"{my_name}: {member_name} is not a member of {my_type}")

                valid_values = valuelists.get_valid_values(valuelist)
                if len(valid_values) > 0:
                    values = [values] if isinstance(values, str) else values
                    for value in values:
                        if value not in valid_values:
                            raise KeyError(f"""{my_name}: "{value}" is not a valid value for {my_type}."""
                                           f"""{member_name}""")

    def write(self, f: io.TextIOWrapper) -> None:
        """Write ourselves to a file."""
        # Output the prologue in a fixed order
        f.write(f"""new entry "{self.__members[".name"]}"\n""")
        f.write(f"""type "{self.__members[".type"]}"\n""")
        if spell_type := self.__members.get("SpellType", None):
            f.write(f"""data "SpellType" "{spell_type}"\n""")
        if status_type := self.__members.get("StatusType", None):
            f.write(f"""data "StatusType" "{status_type}"\n""")
        if using := self.__members.get(".using", None):
            f.write(f"""using "{using}"\n""")

        # Output the remaining members in sorted order
        for member_name in sorted(self.__members.keys()):
            if member_name not in self.__prologue_entries:
                value = self.__members[member_name]
                if not isinstance(value, str):
                    value = ";".join(value)
                f.write(f"""data "{member_name.replace("_", " ")}" "{value}"\n""")


class GameDatumFactory:
    """Spell and Item data representation."""

    __modifier_name: str

    def __init__(self, modifier_name: str):
        self.__modifier_name = modifier_name

    def __call__(self, name: str, using: str | None = None, **members: GameDatum.Members) -> GameDatum:
        return GameDatum({
            ".name": name,
            ".type": self.__modifier_name,
            ".using": using,
            **members
        })


class GameData:
    """A collection of GameDatum."""

    __modifier_to_filename = {
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

    __modifiers: Modifiers
    __valuelists: ValueLists

    __data: Iterable[GameDatum]

    def __init__(self, modifiers: Modifiers, valuelists: ValueLists):
        """Create an instance."""
        self.__modifiers = modifiers
        self.__valuelists = valuelists
        self.__data = []

    def add(self, data: GameDatum | Iterable[GameDatum]) -> None:
        """Add GameDatum to the collection."""
        data = [data] if isinstance(data, GameDatum) else data
        for datum in data:
            datum.validate(self.__modifiers, self.__valuelists)
        self.__data.extend(data)

    def build(self, mod_dir: str, folder: str) -> None:
        """Build all data files in the given mod_dir, folder."""
        files = {}
        for datum in self.__data:
            files.setdefault(self._datum_filename(datum), []).append(datum)

        data_dir = os.path.join(mod_dir, "Public", folder, "Stats", "Generated", "Data")
        os.makedirs(data_dir, exist_ok=True)

        for filename, data in files.items():
            with open(os.path.join(data_dir, filename), "w") as f:
                self._write_data(f, data)

    def _write_data(self, f: io.TextIOWrapper, data: Iterable[GameDatum]) -> None:
        """Write the entries specific to a file."""
        f.write(TXT_PROLOGUE)
        data[0].write(f)
        for datum in data[1:]:
            f.write("\n")
            datum.write(f)

    def _datum_filename(self, datum: GameDatum) -> str:
        """Get the filename corresponding to the given modifier_name."""
        filename = self.__modifier_to_filename[datum[".type"]]
        if isinstance(filename, str):
            return filename
        key, make = filename
        sub_type = datum[key]
        return make(sub_type)


armor_data = GameDatumFactory("Armor")
character_data = GameDatumFactory("Character")
critical_hit_type_data = GameDatumFactory("CriticalHitTypeData")
interrupt_data = GameDatumFactory("InterruptData")
object_data = GameDatumFactory("Object")
passive_data = GameDatumFactory("PassiveData")
spell_data = GameDatumFactory("SpellData")
status_data = GameDatumFactory("StatusData")
weapon_data = GameDatumFactory("Weapon")
