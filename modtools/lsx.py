#!/usr/bin/env python3
"""
Representation of an .lsx file.
"""

from __future__ import annotations

import io
import os

import xml.etree.ElementTree as ElementTree

from .prologue import XML_PROLOGUE


class Lsx:
    """Class representing an .lsx file."""

    class Document:
        """Class representing an .lsx document."""

        __version: (int, int, int, int)
        __region: Lsx.Region

        def __init__(self, version: (int, int, int, int) = None, region: Lsx.Region = None):
            self.__version = version
            self.__region = region

        def get_version(self) -> (int, int, int, int):
            return self.__version

        def get_region(self) -> Lsx.Region:
            return self.__region

        def set_version(self, version: (int, int, int, int)) -> None:
            assert self.__version is None
            self.__version = version

        def set_region(self, region: Lsx.Region) -> None:
            assert self.__region is None
            self.__region = region

        def xml(self) -> ElementTree.ElementTree:
            document = ElementTree.Element("save")
            if self.__version:
                ElementTree.SubElement(document, "version", {
                    "major": str(self.__version[0]),
                    "minor": str(self.__version[1]),
                    "revision": str(self.__version[2]),
                    "build": str(self.__version[3]),
                })
            if self.__region:
                self.__region.xml(document)

            return ElementTree.ElementTree(document)

    class Region:
        """Class representing an .lsx <region>."""

        __id: str
        __node: Lsx.Node

        def __init__(self, id: str, node: Lsx.Node = None):
            self.__id = id
            self.__node = node

        def get_id(self) -> str:
            return self.__id

        def get_node(self) -> Lsx.Node:
            return self.__node

        def set_node(self, node: Lsx.Node) -> None:
            assert self.__node is None
            self.__node = node

        def xml(self, document: ElementTree.Element) -> None:
            region = ElementTree.SubElement(document, "region", id=self.__id)
            if self.__node:
                self.__node.xml(region)

    class Node:
        """Class representing an .lsx <node>."""

        __id: str
        __attributes: [Lsx.Attribute]
        __children: Lsx.Children

        def __init__(self, id: str, attributes: [Lsx.Attribute] = [], children: Lsx.Children | [Lsx.Node] = None):
            self.__id = id
            self.__attributes = attributes
            if children is None or isinstance(children, Lsx.Children):
                self.__children = children
            else:
                self.__children = Lsx.Children(children)

        def get_id(self) -> str:
            return self.__id

        def get_attributes(self) -> [Lsx.Attribute]:
            return self.__attributes

        def get_children(self) -> Lsx.Children:
            return self.__children

        def add_attributes(self, attributes: [Lsx.Attribute]) -> None:
            self.__attributes += attributes

        def add_children(self, nodes: [Lsx.Node]) -> None:
            if self.__children is None:
                self.__children = Lsx.Children(nodes)
            else:
                self.__children.add_nodes(nodes)

        def xml(self, parent: ElementTree.Element) -> None:
            node = ElementTree.SubElement(parent, "node", id=self.__id)
            for attribute in self.__attributes:
                attribute.xml(node)
            if self.__children:
                self.__children.xml(node)

    class Children:
        """Class representing .lsx <children>."""

        __nodes: [Lsx.Node]

        def __init__(self, nodes: [Lsx.Node] = []):
            self.__nodes = nodes

        def get_nodes(self) -> [Lsx.Node]:
            return self.__nodes

        def add_nodes(self, nodes: [Lsx.Node]) -> None:
            self.__nodes += nodes

        def xml(self, parent: ElementTree.Element) -> None:
            children = ElementTree.SubElement(parent, "children")
            for node in self.__nodes:
                node.xml(children)

    class Attribute:
        """Class representing an .lsx <attribute>."""

        __valid_types = set([
            "bool",
            "FixedString",
            "float",
            "fvec3",
            "guid",
            "int8",
            "int16",
            "int32",
            "int64",
            "LSString",
            "LSWString",
            "TranslatedString",
            "uint8",
            "uint16",
            "uint32",
            "uint64",
        ])

        __id: str
        __type: str
        __value: str
        __handle: str
        __version: str

        def __init__(self, id: str, type: str, value: str = None, handle: str = None, version: int | str = 0):
            assert type in Lsx.Attribute.__valid_types

            if value is not None:
                assert type != "TranslatedString"
                assert handle is None
                assert int(version) == 0
            else:
                assert type == "TranslatedString"
                assert handle is not None
                assert int(version) > 0

            self.__id = id
            self.__type = type
            self.__value = value
            self.__handle = handle
            self.__version = str(version)

        def get_id(self) -> str:
            return self.__id

        def get_type(self) -> str:
            return self.__type

        def get_value(self) -> str:
            return self.__value

        def get_handle(self) -> str:
            return self.__handle

        def get_version(self) -> str:
            return self.__version

        def xml(self, parent: ElementTree.Element) -> None:
            attrib = {
                "id": self.__id,
                "type": self.__type
            }
            if self.__value is not None:
                attrib["value"] = self.__value
            else:
                attrib["handle"] = self.__handle
                attrib["version"] = self.__version

            ElementTree.SubElement(parent, "attribute", attrib=attrib)

    __document: Lsx.Document
    __region: Lsx.Region
    __root: Lsx.Node

    def __init__(self, version: (int, int, int, int) = None, region_id: str = None,
                 root_id: str = None):
        self.__region = None
        self.__root = None

        if root_id:
            assert region_id
            self.__root = Lsx.Node(root_id)
        if region_id:
            self.__region = Lsx.Region(region_id, self.__root)

        self.__document = Lsx.Document(version, self.__region)

    def set_version(self, version: (int, int, int, int)) -> None:
        self.__document.set_version(version)

    def set_region(self, region: Lsx.Region) -> None:
        self.__document.set_region(region)
        self.__region = region
        self.__root = region.get_node()

    def set_root(self, root: Lsx.Node) -> None:
        assert self.__region
        assert not self.__root
        self.__root = root

    def add_children(self, nodes: [Lsx.Node]) -> None:
        assert self.__root
        self.__root.add_children(nodes)

    def build(self, path: str) -> None:
        document = self.__document.xml()
        ElementTree.indent(document, space=" "*4)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(XML_PROLOGUE)
            document.write(f, encoding="UTF-8", xml_declaration=False)
