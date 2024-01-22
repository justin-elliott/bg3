#!/usr/bin/env python3
"""
Builders for .lsx types.
"""

import os
import xml.etree.ElementTree as ElementTree

from modtools.lsx.types import Attribute, DataType, Lsx, LsxMetadata, Node, NodeMetadata
from typing import Self


class NodeBuilder(NodeMetadata):
    """Class that builds an lsx.types.Node."""
    def __init__(self,
                 id: str,
                 attributes: dict[str, DataType] = {},
                 child_builders: list[Self] = [],
                 key_attribute: str = "UUID"):
        super().__init__(id, key_attribute, attributes, child_builders)

    def __call__(self, **kwargs: str | Attribute | list[Node]) -> Node:
        attributes = {}
        children = []

        for name, value in kwargs.items():
            if name == "children":
                children = self._build_children(value)
            elif (data_type := self.attributes.get(name, None)) is not None:
                attributes[name] = self._build_attribute(data_type, value)
            else:
                raise KeyError(f"{self.id} does not have an attribute '{name}'")

        if self.key_attribute is not None and self.key_attribute not in attributes:
            raise KeyError(f"{self.id} missing attribute '{self.key}'")
        return Node(self, attributes, children)

    def _build_children(self, children: str | Attribute | list[Node]) -> list[Node]:
        for node in children:
            assert isinstance(node, Node)
            assert node.metadata == self.child_builders[node.metadata.id]
        return children

    def _build_attribute(self, data_type: DataType, value: str | Attribute | list[Node]) -> list[Node]:
        if data_type in Attribute.HANDLE_TYPES:
            if isinstance(value, Attribute):
                assert value.data_type == data_type
                return value
            return Attribute(data_type, handle=str(value), version=1)
        elif data_type in Attribute.LIST_TYPES:
            if isinstance(value, Attribute):
                assert value.data_type == data_type
                return value
            return Attribute(data_type, value=value)
        else:
            if isinstance(value, Attribute):
                assert value.data_type == data_type
                return value
            return Attribute(data_type, value=str(value))

    def load_from_xml(self, element: ElementTree.Element) -> Node:
        assert element.tag == "node" and element.get("id", "") == self.id

        attributes = {}
        for attribute in element.findall("attribute"):
            id = attribute.get("id", "")
            if (data_type := self.attributes.get(id, None)) is not None:
                assert attribute.get("type", "") == data_type if data_type not in Attribute.PSEUDO_LSSTRING_TYPES else (
                    attribute.get("type", "") == DataType.LSSTRING
                )
                if (value := attribute.get("value")) is not None:
                    if data_type in Attribute.LIST_TYPES:
                        separator = "," if data_type == DataType.LSSTRING_COMMA else ";"
                        attributes[id] = Attribute(data_type, value=[s for s in value.split(separator) if len(s) > 0])
                    else:
                        attributes[id] = Attribute(data_type, value=value)
                else:
                    attributes[id] = Attribute(data_type,
                                               handle=attribute.get("handle"),
                                               version=attribute.get("version"))
            else:
                raise KeyError(f"{self.id} does not have an attribute '{id}'")

        children = []
        if (children_node := element.find("children")) is not None:
            for node in children_node.findall("node"):
                builder = self.child_builders[node.get("id")]
                child = builder.load_from_xml(node)
                children.append(child)

        return Node(self, attributes, children)


class LsxBuilder(LsxMetadata):
    """Class that builds an lsx.types.Lsx."""

    def __init__(self,
                 region: str,
                 root: str,
                 node_builder: NodeBuilder,
                 relative_path: os.PathLike):
        super().__init__(region, root, node_builder, relative_path)

    def __call__(self, *nodes: Node) -> Lsx:
        assert all(node.metadata == self.node_builder for node in nodes)
        return Lsx(self, list(nodes))

    def load(self, *paths: os.PathLike) -> Lsx:
        lsx = Lsx(self, [])
        for path in paths:
            with open(path, "rb") as f:
                document = ElementTree.parse(f).getroot()
                self._load_from_xml(lsx, document)
        return lsx

    def _load_from_xml(self, lsx: Lsx, document: ElementTree.Element) -> None:
        # Parse the document preamble: <save><region id="..."><node id="..."><children>
        assert document.tag == "save"
        region = document.find("region")
        assert region and region.tag == "region" and region.get("id", "") == self.region
        root = region.find("node")
        assert root and root.tag == "node" and root.get("id", "") == self.root
        children = root.find("children")
        assert children and children.tag == "children"

        # Load each of the nodes
        for node in children.findall("node"):
            lsx.add(self.node_builder.load_from_xml(node))
