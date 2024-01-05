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

    __prologue_entries = set([".name", ".type", ".using", "SpellType", "StatusType"])

    __members: Members

    def __init__(self, members: Members):
        self.__members = members

    def __getitem__(self, member_name: str) -> str | Iterable[str]:
        return self.__members[member_name]

    def validate(self, modifiers: Modifiers, valuelists: ValueLists) -> None:
        """Validate the entity against the modifiers and valuelists, raising an exception on a mismatch."""
        entity_name = self.__members[".name"]
        entity_type = self.__members[".type"]

        modifier = modifiers.get_modifier(entity_type)

        for member_name, values in self.__members.items():
            if not member_name.startswith("."):
                valuelist = modifier.get(member_name, None)
                if valuelist is None:
                    raise KeyError(f"{entity_name}: {member_name} is not a member of {entity_type}")

                valid_values = valuelists.get_valid_values(valuelist)
                if len(valid_values) > 0:
                    values = [values] if isinstance(values, str) else values
                    for value in values:
                        if value not in valid_values:
                            raise KeyError(f"""{entity_name}: "{value}" is not a valid value for {entity_type}."""
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
                f.write(f"""data "{member_name}" "{value}"\n""")


class EntityFactory:
    """Spell and Item data representation."""

    __modifier_name: str

    def __init__(self, modifier_name: str):
        self.__modifier_name = modifier_name

    def __call__(self, name: str, using: str | None = None, **members: Entity.Members) -> Entity:
        return Entity({
            ".name": name,
            ".type": self.__modifier_name,
            ".using": using,
            **members
        })


class Entities:
    """A collection of entities."""

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

    __entities: [Entity]

    def __init__(self, modifiers: Modifiers, valuelists: ValueLists):
        """Create an entity."""
        self.__modifiers = modifiers
        self.__valuelists = valuelists
        self.__entities = []

    def add(self, entity: Entity) -> None:
        """Add an entity to the collection."""
        entity.validate(self.__modifiers, self.__valuelists)
        self.__entities.append(entity)

    def build(self, mod_dir: str, folder: str) -> None:
        """Build all entity files in the given mod_dir, folder."""
        files = {}
        for entity in self.__entities:
            files.setdefault(self._entity_filename(entity), []).append(entity)

        data_dir = os.path.join(mod_dir, "Public", folder, "Stats", "Generated", "Data")
        os.makedirs(data_dir, exist_ok=True)

        for filename, entities in files.items():
            with open(os.path.join(data_dir, filename), "w") as f:
                self._write_entities(f, entities)

    def _write_entities(self, f: io.TextIOWrapper, entities: [Entity]) -> None:
        """Write the entities specific to a file."""
        f.write(TXT_PROLOGUE)
        entities[0].write(f)
        for entity in entities[1:]:
            f.write("\n")
            entity.write(f)

    def _entity_filename(self, entity: Entity) -> str:
        """Get the filename corresponding to the given modifier_name."""
        filename = self.__modifier_to_filename[entity[".type"]]
        if isinstance(filename, str):
            return filename
        key, make = filename
        sub_type = entity[key]
        return make(sub_type)


armor_data = EntityFactory("Armor")
character_data = EntityFactory("Character")
critical_hit_type_data = EntityFactory("CriticalHitTypeData")
interrupt_data = EntityFactory("InterruptData")
object_data = EntityFactory("Object")
passive_data = EntityFactory("PassiveData")
spell_data = EntityFactory("SpellData")
status_data = EntityFactory("StatusData")
weapon_data = EntityFactory("Weapon")
