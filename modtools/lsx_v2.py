#!/usr/bin/env python3
"""
Representation of an .lsx file.
"""

import os

import xml.etree.ElementTree as ElementTree

from dataclasses import dataclass
from enum import StrEnum
from modtools.prologue import XML_PROLOGUE
from typing import Self


class DataType(StrEnum):
    """Data types as found in the .lsx 'type' XML attribute."""
    NONE = "None"
    UINT8 = "uint8"
    INT16 = "int16"
    UINT16 = "uint16"
    INT32 = "int32"
    UINT32 = "uint32"
    FLOAT = "float"
    DOUBLE = "double"
    IVEC2 = "ivec2"
    IVEC3 = "ivec3"
    IVEC4 = "ivec4"
    FVEC2 = "fvec2"
    FVEC3 = "fvec3"
    FVEC4 = "fvec4"
    MAT2X2 = "mat2x2"
    MAT3X3 = "mat3x3"
    MAT3X4 = "mat3x4"
    MAT4X3 = "mat4x3"
    MAT4X4 = "mat4x4"
    BOOL = "bool"
    STRING = "string"
    PATH = "path"
    FIXEDSTRING = "FixedString"
    LSSTRING = "LSString"
    UINT64 = "uint64"
    SCRATCHBUFFER = "ScratchBuffer"
    OLD_INT64 = "old_int64"
    INT8 = "int8"
    TRANSLATEDSTRING = "TranslatedString"
    WSTRING = "WString"
    LSWSTRING = "LSWString"
    GUID = "guid"
    INT64 = "int64"
    TRANSLATEDFSSTRING = "TranslatedFSString"


@dataclass
class Attribute:
    """Class representing an attribute value."""
    value: str | list[str] | None = None
    handle: str | None = None
    version: int | None = None

    def __str__(self) -> str:
        if self.value is not None:
            if isinstance(self.value, str):
                return f'"{self.value}"'
            else:
                return f"[{", ".join(f'"{x}"' for x in self.value)}]"
        elif self.version == 1:
            return f'"{self.handle}"'
        else:
            return f"""Attribute(handle="{self.handle}", version={self.version})"""


class Node:
    """Class representing a node in an .lsx file."""
    id: str
    attributes: dict[str, Attribute]
    children: list[Self]

    def __init__(self, id: str, attributes: dict[str, Attribute], children: [Self]):
        self.id = id
        self.attributes = attributes
        self.children = children

    def __str__(self) -> str:
        args = [f"{key}={value}" for key, value in self.attributes.items()]
        if len(self.children) > 0:
            args.append(f"children=[{", ".join(str(node) for node in self.children)}]")
        return f"{self.id}({", ".join(args)})"


class NodeBuilder:
    """Class that builds a Node."""
    id: str
    key: str
    attributes: dict[str, DataType]
    child_builders: list[Self]

    def __init__(self,
                 id: str,
                 attributes: dict[str, DataType] = {},
                 child_builders: list[Self] = [],
                 key: str = "UUID"):
        self.id = id
        self.key = key
        self.attributes = attributes
        self.child_builders = child_builders

    def __call__(self, **kwargs: dict[str, str | Attribute | list[Node]]) -> Node:
        attributes = {}
        children = []

        for name, value in kwargs.items():
            if name == "children":
                assert len(self.child_builders) > 0
                for node in value:
                    assert isinstance(node, Node)
                    assert any(node.id == child_builder.id for child_builder in self.child_builders)
                children = value
            elif (data_type := self.attributes.get(name, None)) is not None:
                attribute = Attribute()
                if data_type in [DataType.TRANSLATEDSTRING, DataType.TRANSLATEDFSSTRING]:
                    if isinstance(value, Attribute):
                        assert value.value is None
                        assert isinstance(value.handle, str)
                        assert isinstance(value.version, int)
                        attribute.handle = value.handle
                        attribute.version = value.version
                    else:
                        attribute.handle = str(value)
                        attribute.version = 1
                else:
                    if isinstance(value, Attribute):
                        assert value.value is not None
                        assert value.handle is None
                        assert value.version is None
                        attribute.value = value.value
                    elif isinstance(value, str):
                        attribute.value = value
                    else:
                        try:
                            attribute.value = list(iter(value))
                            assert data_type in [DataType.LSSTRING, DataType.LSWSTRING]
                        except TypeError:
                            attribute.value = str(value)
                attributes[name] = attribute
            else:
                raise KeyError(f"{self.id} does not have an attribute '{name}'")

        if self.key is not None and self.key not in attributes:
            raise KeyError(f"{self.id} missing attribute '{self.key}'")
        return Node(self.id, attributes, children)


class Lsx:
    """Class representing an .lsx file."""
    region: str
    root: str
    node_builder: NodeBuilder

    def __init__(self, region: str, root: str, node_builder: NodeBuilder):
        self.region = region
        self.root = root
        self.node = Node
