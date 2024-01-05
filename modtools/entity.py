#!/usr/bin/env python3
"""
Representation of spell and item data.
"""

import io
import os

from .modifiers import Modifiers
from .prologue import TXT_PROLOGUE
from .valuelists import ValueLists
from collections.abc import Iterable, Mapping


class Entity:
    """Spell and Item data representation."""

    type Members = Mapping[str, str | Iterable[str]]  # {member_name: value | [values]}

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

    __modifier_name: str
    __modifier: Modifiers.Modifier
    __valuelists: ValueLists

    __entities: Mapping[str, Members]  # {name: members}

    def __init__(self, modifier_name: str, modifiers: Modifiers, valuelists: ValueLists):
        """Create an entity."""
        self.__modifier_name = modifier_name
        self.__modifier = modifiers.get_modifier(modifier_name)
        self.__valuelists = valuelists
        self.__entities = {}

    def add(self, name: str, using: str | None = None, **members: Members) -> None:
        for member_name, values in members.items():
            valuelist = self.__modifier.get(member_name, None)
            if valuelist is None:
                raise KeyError(f"{name}: {member_name} is not a member of {self.__modifier_name}")
            values = [values] if isinstance(values, str) else values
            valid_values = self.__valuelists.get_valid_values(valuelist)
            if len(valid_values) > 0:
                for value in values:
                    if value not in valid_values:
                        raise KeyError(f"""{name}: "{value}" is not a valid value for {self.__modifier_name}.{
                            member_name}""")

        self.__entities[name] = {
            ".name": name,
            ".using": using,
            **members,
        }

    def build(self, mod_dir: str, folder: str) -> None:
        """Build all entity files in the given mod_dir, folder."""
        files = {}
        for entity in self.__entities.values():
            files.setdefault(self._entity_filename(entity), []).append(entity)

        data_dir = os.path.join(mod_dir, "Public", folder, "Stats", "Generated", "Data")
        os.makedirs(data_dir, exist_ok=True)

        for filename, entities in files.items():
            with open(os.path.join(data_dir, filename), "w") as f:
                self._write_entities(f, entities)

    def _write_entities(self, f: io.TextIOWrapper, entities: [Members]) -> None:
        """Build the entities specific to a file."""
        f.write(TXT_PROLOGUE)
        self._write_entity(f, entities[0])
        for entity in entities[1:]:
            f.write("\n")
            self._write_entity(f, entity)

    def _write_entity(self, f: io.TextIOWrapper, entity: Members) -> None:
        """Write a single entity to a file."""
        entity = entity.copy()

        # Output the prologue in a fixed order
        f.write(f"""new entry "{entity.pop(".name")}"\n""")
        f.write(f"""type "{self.__modifier_name}"\n""")
        if spell_type := entity.pop("SpellType", None):
            f.write(f"""data "SpellType" "{spell_type}"\n""")
        if status_type := entity.pop("StatusType", None):
            f.write(f"""data "StatusType" "{status_type}"\n""")
        if using := entity.pop(".using", None):
            f.write(f"""using "{using}"\n""")

        # Output the remaining members in sorted order
        for member in sorted(entity.keys()):
            value = entity[member]
            if not isinstance(value, str):
                value = ";".join(value)
            f.write(f"""data "{member}" "{value}"\n""")

    def _entity_filename(self, entity: Members) -> str:
        """Get the filename corresponding to the given modifier_name."""
        filename = self.__modifier_to_filename[self.__modifier_name]
        if isinstance(filename, str):
            return filename
        key, make = filename
        sub_type = entity[key]
        return make(sub_type)
