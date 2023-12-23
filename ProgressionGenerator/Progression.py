#!/usr/bin/env python3

import textwrap
import uuid

import xml.etree.ElementTree as ElementTree

from typing import Final, Optional

class ClassProgression:
    allow_improvement: Optional[bool]
    boosts: Optional[list[str]]
    is_multiclass: Optional[bool]
    level: int
    name: str
    passives_added: Optional[list[str]]
    passives_removed: Optional[list[str]]
    progression_type: int
    selectors: Optional[list[str]]
    table_uuid: uuid.UUID
    our_uuid: uuid.UUID
    children: Optional[list[uuid.UUID]]

    def __init__(self,
                 level: int,
                 name: str,
                 progression_type: int,
                 table_uuid: uuid.UUID,
                 our_uuid: uuid.UUID,
                 allow_improvement: Optional[bool] = None,
                 boosts: Optional[list[str]] = None,
                 is_multiclass: Optional[bool] = None,
                 passives_added: Optional[list[str]] = None,
                 passives_removed: Optional[list[str]] = None,
                 selectors: Optional[list[str]] = None,
                 children: Optional[list[uuid.UUID]] = None):
        self.allow_improvement = allow_improvement
        self.boosts = boosts
        self.is_multiclass = is_multiclass
        self.level = level
        self.name = name
        self.passives_added = passives_added
        self.passives_removed = passives_removed
        self.progression_type = progression_type
        self.selectors = selectors
        self.table_uuid = table_uuid
        self.our_uuid = our_uuid
        self.children = children

    def parse(progression: ElementTree.Element):
        self = ClassProgression(level=None, name=None, progression_type=None, table_uuid=None, our_uuid=None)
        self.__validate_nodes(progression)
        if self.level is None:
            raise AttributeError(f"Missing Progression attribute id='Level': {self}")
        if self.name is None:
            raise AttributeError(f"Missing Progression attribute id='Name': {self}")
        if self.progression_type is None:
            raise AttributeError(f"Missing Progression attribute id='ProgressionType': {self}")
        if self.table_uuid is None:
            raise AttributeError(f"Missing Progression attribute id='TableUUID': {self}")
        if self.our_uuid is None:
            raise AttributeError(f"Missing Progression attribute id='UUID': {self}")
        print(self)
        return self

    def __validate_nodes(self, progression: ElementTree.Element):
        for node in progression.findall("./"):
            if node.tag == "attribute":
                self.__parse_attribute(node)
            elif node.tag == "children":
                self.__parse_children(node)
            else:
                raise AttributeError(f"Unknown Progression tag: {node.tag}")

    def __parse_attribute(self, attribute: ElementTree.Element):
        id = attribute.get("id")
        value = attribute.get("value")

        match id:
            case "AllowImprovement":
                self.allow_improvement = value.lower() == "true"
            case "Boosts":
                self.boosts = value.split(";")
            case "IsMulticlass":
                self.level = value.lower() == "true"
            case "Level":
                self.level = int(value)
            case "Name":
                self.name = value
            case "PassivesAdded":
                self.passives_added = value.split(";")
            case "PassivesRemoved":
                self.passives_removed = value.split(";")
            case "ProgressionType":
                self.progression_type = int(value)
            case "Selectors":
                self.selectors = value.split(";")
            case "TableUUID":
                self.table_uuid = uuid.UUID(value)
            case "UUID":
                self.our_uuid = uuid.UUID(value)
            case _:
                raise AttributeError(f"Unknown Progression attribute id='{id}'")

    def __parse_children(self, children: ElementTree.Element):
        pass

    def __str__(self):
        args: Final[list[str]] = [
            "allow_improvement",
            "boosts",
            "is_multiclass",
            "level",
            "name",
            "passives_added",
            "passives_removed",
            "progression_type",
            "selectors",
            "table_uuid",
            "our_uuid",
            "children",
        ]

        return f"Progression({", ".join([f"{s}={repr(self.__dict__[s])}" for s in args if self.__dict__[s] is not None])})"
