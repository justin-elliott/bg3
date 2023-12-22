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

        def version(self, version_: (int, int, int, int)) -> None:
            assert self.__version is None
            self.__version = version_

        def region(self, region_: Lsx.Region) -> None:
            assert self.__region is None
            self.__region = region_

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

        def node(self, node: Lsx.Node) -> None:
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

        def attributes(self, attributes_: [Lsx.Attribute]) -> None:
            self.__attributes += attributes_

        def children(self, children_: Lsx.Children | [Lsx.Node]) -> None:
            assert self.__children is None
            self.__children = children_ if isinstance(children_, Lsx.Children) else Lsx.Children(children_)

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

        def node(self, node_: Lsx.Node) -> None:
            self.__nodes.append(node_)

        def xml(self, parent: ElementTree.Element) -> None:
            children = ElementTree.SubElement(parent, "children")
            for node in self.__nodes:
                node.xml(children)

    class Attribute:
        """Class representing an .lsx <attribute>."""

        __id: str
        __type: str
        __value: str
        __handle: str
        __version: int

        def __init__(self, id: str, type: str, value: str = None, handle: str = None, version: int = 0):
            if value is not None:
                assert handle is None
                assert version == 0
            else:
                assert handle is not None
                assert version > 0

            self.__id = id
            self.__type = type
            self.__value = value
            self.__handle = handle
            self.__version = version

        def xml(self, parent: ElementTree.Element) -> None:
            attrib = {
                "id": self.__id,
                "type": self.__type
            }
            if self.__value is not None:
                attrib["value"] = self.__value
            else:
                attrib["handle"] = self.__handle
                attrib["version"] = str(self.__version)

            ElementTree.SubElement(parent, "attribute", attrib=attrib)

    __document: Lsx.Document

    def __init__(self, relative_path: str, version: (int, int, int, int) = None, region: Lsx.Region = None):
        self.__document = Lsx.Document(version, region)

    def version(self, version_: (int, int, int, int)) -> None:
        self.__document.version(version_)

    def region(self, region_: Lsx.Region) -> None:
        self.__document.region(region_)

    def build(self, mod_dir: str) -> None:
        document = self.__document.xml()
        ElementTree.indent(document, space=" "*4)
        ElementTree.dump(document)
