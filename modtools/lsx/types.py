#!/usr/bin/env python3
"""
Representation of .lsx types.
"""

import os
import xml.etree.ElementTree as ElementTree

from enum import StrEnum
from modtools.prologue import XML_PROLOGUE
from typing import Final, Self


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
    LSSTRING_COMMA = "LSString,"  # A pseudo-type representing comma-separated lists such as PassiveLists.
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


class Attribute:
    """Class representing an .lsx attribute value."""
    HANDLE_TYPES: Final[frozenset[DataType]] = frozenset([DataType.TRANSLATEDSTRING, DataType.TRANSLATEDFSSTRING])
    LIST_TYPES: Final[frozenset[DataType]] = frozenset([DataType.LSSTRING, DataType.LSSTRING_COMMA, DataType.LSWSTRING])

    _data_type: DataType
    _value: str | list[str] | None = None
    _handle: str | None = None
    _version: int | None = None

    @property
    def data_type(self) -> DataType:
        return self._data_type

    @property
    def value(self) -> str | list[str]:
        assert self._data_type not in Attribute.HANDLE_TYPES
        assert self._value is not None
        return self._value

    @value.setter
    def value(self, value_or_list: str | list[str]) -> None:
        if self._data_type in Attribute.LIST_TYPES:
            self._value = [value_or_list] if isinstance(value_or_list, str) else list(value_or_list)
        else:
            assert self._data_type not in Attribute.HANDLE_TYPES
            self._value = str(value_or_list)

    @property
    def handle(self) -> str:
        assert self._data_type in Attribute.HANDLE_TYPES
        assert self._handle is not None
        return self._handle

    @handle.setter
    def handle(self, handle_version: str | tuple[str, int]) -> None:
        assert self._data_type in Attribute.HANDLE_TYPES
        if isinstance(handle_version, str):
            self._handle = handle_version
            self._version = 1
        else:
            self._handle, self._version = handle_version

    @property
    def version(self) -> str:
        assert self._data_type in Attribute.HANDLE_TYPES
        assert self._version is not None
        return self._version

    def __init__(self,
                 data_type: DataType,
                 value: str | list[str] | None = None,
                 handle: str | None = None,
                 version: int | None = None):
        self._data_type = data_type
        self._value = None
        self._handle = None
        self._version = None

        if value is not None:
            assert handle is None
            assert version is None
            self.value = value
        else:
            assert value is None
            assert handle is not None
            self.handle = (str(handle), int(version) if version is not None else 1)

    def xml(self, id: str) -> ElementTree.Element:
        attributes = {
            "id": id,
            "type": self._data_type
        }
        if self._data_type == DataType.LSSTRING_COMMA:
            attributes["type"] = DataType.LSSTRING
            attributes["value"] = ",".join(self.value)
        if self._data_type in Attribute.LIST_TYPES:
            attributes["value"] = ";".join(self.value)
        elif self._data_type in Attribute.HANDLE_TYPES:
            attributes["handle"] = self.handle
            attributes["version"] = self.version
        else:
            attributes["value"] = self.value
        return ElementTree.Element("attribute", attributes)

    def __str__(self) -> str:
        if self._data_type in Attribute.LIST_TYPES:
            return f"[{", ".join(f'"{entry}"' for entry in self.value)}]"
        elif self._data_type in Attribute.HANDLE_TYPES:
            return f'"{self.handle}"' if self.version == 1 else (
                f"""Attribute(handle="{self.handle}", version={self.version})""")
        else:
            return f'"{self.value}"'


class NodeMetadata:
    """Class representing the metadata for a node in an .lsx file."""
    _id: str
    _key: str | None
    _attributes: dict[str, DataType]
    _child_builders: list[Self]

    @property
    def id(self) -> str:
        return self._id

    @property
    def key(self) -> str | None:
        return self._key

    @property
    def attributes(self) -> dict[str, DataType]:
        return self._attributes

    @property
    def child_builders(self) -> list[Self]:
        return self._child_builders

    def __init__(self,
                 id: str,
                 key: str | None,
                 attributes: dict[str, DataType],
                 child_builders: list[Self]):
        self._id = id
        self._key = key
        self._attributes = attributes
        self._child_builders = child_builders


class Node:
    """Class representing a node in an .lsx file."""
    _metadata: NodeMetadata
    _attributes: dict[str, Attribute]
    _children: list[Self]

    @property
    def metadata(self) -> NodeMetadata:
        return self._metadata

    @property
    def id(self) -> str:
        return self._metadata.id

    @property
    def key(self) -> str | None:
        return self._metadata.key

    @property
    def attributes(self) -> dict[str, Attribute]:
        return self._attributes

    @property
    def children(self) -> list[Self]:
        return self._children

    def __init__(self, metadata: NodeMetadata, attributes: dict[str, Attribute] = {}, children: [Self] = []):
        self._metadata = metadata
        self._attributes = attributes
        self._children = children

    def xml(self) -> ElementTree.Element:
        element = ElementTree.Element("node", id=self.id)
        for id, attribute in self.attributes.items():
            element.append(attribute.xml(id))
        if len(self.children) > 0:
            children = ElementTree.SubElement(element, "children")
            for child in self.children:
                children.append(child.xml())
        return element


class LsxMetadata:
    """Class representing the metadata for an .lsx file."""
    _region: str
    _root: str
    _node_builder: NodeMetadata

    @property
    def region(self) -> str:
        return self._region

    @property
    def root(self) -> str:
        return self._root

    @property
    def node_builder(self) -> NodeMetadata:
        return self._node_builder

    def __init__(self, region: str, root: str, node_builder: NodeMetadata):
        self._region = region
        self._root = root
        self._node_builder = node_builder


class Lsx:
    """Class representing an .lsx file."""
    _metadata: LsxMetadata
    _nodes: list[Node]

    @property
    def metadata(self) -> NodeMetadata:
        return self._metadata

    @property
    def region(self) -> str:
        return self._metadata.region

    @property
    def root(self) -> str:
        return self._metadata.root

    @property
    def nodes(self) -> list[Node]:
        return self._nodes

    def __init__(self, metadata: LsxMetadata, nodes: list[Node]):
        self._metadata = metadata
        self._nodes = nodes

    def save(self, path: os.PathLike, version: tuple[int, int, int, int] | None = None):
        document = ElementTree.ElementTree(self.xml(version))
        ElementTree.indent(document, space=" "*4)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(XML_PROLOGUE)
            document.write(f, encoding="UTF-8", xml_declaration=False)

    def xml(self, version: tuple[int, int, int, int] | None = None) -> ElementTree.Element:
        element = ElementTree.Element("save")
        if version:
            ElementTree.SubElement(element, "version", {
                attr: str(ver) for attr, ver in zip(["major", "minor", "revision", "build"], version)
            })
        region = ElementTree.SubElement(element, "region", id=self.region)
        root = ElementTree.SubElement(region, "node", id=self.root)
        children = ElementTree.SubElement(root, "children")
        for node in self._nodes:
            children.append(node.xml())
        return element
