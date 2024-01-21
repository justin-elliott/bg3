#!/usr/bin/env python3
"""
Builders for .lsx types.
"""

from modtools.lsx.types import Attribute, DataType, Lsx, LsxMetadata, Node, NodeMetadata
from typing import Self


class NodeBuilder(NodeMetadata):
    """Class that builds an lsx.types.Node."""
    def __init__(self,
                 id: str,
                 attributes: dict[str, DataType] = {},
                 child_builders: list[Self] = [],
                 key: str = "UUID"):
        super().__init__(id, key, attributes, child_builders)

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

        if self.key is not None and self.key not in attributes:
            raise KeyError(f"{self.id} missing attribute '{self.key}'")
        return Node(self, attributes, children)

    def _build_children(self, children: str | Attribute | list[Node]) -> list[Node]:
        for node in children:
            assert isinstance(node, Node)
            assert node.metadata in self.child_builders
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


class LsxBuilder(LsxMetadata):
    """Class that builds an lsx.types.Lsx."""
    def __init__(self, region: str, root: str, node_builder: NodeBuilder):
        super().__init__(region, root, node_builder)

    def __call__(self, *nodes: Node) -> Lsx:
        assert all(node.metadata == self.node_builder for node in nodes)
        return Lsx(self, list(nodes))
