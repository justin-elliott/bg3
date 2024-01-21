#!/usr/bin/env python3
"""
Builders for .lsx types.
"""

from modtools.lsx.types import Attribute, DataType, Lsx, Node
from typing import Self


class NodeBuilder:
    """Class that builds an lsx.types.Node."""
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

    def __call__(self, **kwargs: str | Attribute | list[Node]) -> Node:
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


class LsxBuilder:
    """Class that builds an lsx.types.Lsx."""
    region: str
    root: str
    node_builder: NodeBuilder

    def __init__(self, region: str, root: str, node_builder: NodeBuilder):
        self.region = region
        self.root = root
        self.node_builder = node_builder

    def __call__(self, *nodes: Node) -> Lsx:
        assert all(node.id == self.node_builder.id for node in nodes)
        return Lsx(self.region, self.root, nodes)
