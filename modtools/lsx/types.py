#!/usr/bin/env python3
"""
Representation of .lsx types.
"""

from dataclasses import dataclass
from enum import StrEnum
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
    """Class representing an .lsx attribute value."""
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


class Lsx:
    """Class representing an .lsx file."""
    region: str
    root: str
    nodes: list[Node]

    def __init__(self, region: str, root: str, nodes: list[Node]):
        self.region = region
        self.root = root
        self.nodes = nodes

    def __str__(self) -> str:
        return f"{self.region}({", ".join(str(node) for node in self.nodes)})"
