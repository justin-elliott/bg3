#!/usr/bin/env python3
"""
Representation of .lsx nodes.
"""

from collections import OrderedDict
from modtools.lsx.attributes import LsxAttribute
from typing import Self
from xml.etree.ElementTree import Element

import modtools.lsx.detail as detail


class LsxNode:
    """A class representing an .lsx node."""

    _id_: str                                     # The node's id attribute (defaulting to the subclass name).
    _attributes_: OrderedDict[str, LsxAttribute]  # The node's attribute definitions.
    _child_types_: tuple[type[Self], ...]         # The valid types for the node's children.

    children: detail.LsxChildren[Self]

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._id_ = cls.__name__
        cls._attributes_ = OrderedDict()
        cls._child_types_ = ()
        for member_name, value in list(cls.__dict__.items()):
            if member_name == "id":
                cls._id_ = str(value)
            elif member_name == "children":
                cls._child_types_ = tuple(value)
            elif isinstance(value, LsxAttribute):
                cls._attributes_[member_name] = value

        for member_name, data_type in cls._attributes_.items():
            getter, setter = data_type._wrap_accessors("_" + member_name)
            prop = property(fget=getter, fset=setter)
            setattr(cls, member_name, prop)

        if len(cls._child_types_) > 0:
            getter, setter = detail.LsxChildren[Self]._wrap_accessors("_children", cls._child_types_)
            setattr(cls, "children", property(fget=getter, fset=setter))

    def __init__(self, **kwds):
        for name, value in kwds.items():
            if name not in self._attributes_ and getattr(self, name, None) is None:
                raise AttributeError(f"{self.__class__.__name__}.{name} is not defined", obj=self, name=name)
            setattr(self, name, value)

    def load(self, node: Element) -> None:
        """Load the node from the given XML <node>."""
        assert node.get("id") == self._id_

        for attribute in node.findall("attribute"):
            id = attribute.get("id")
            if (value := attribute.get("value")) is not None:
                setattr(self, id, value)
            else:
                handle = attribute.get("handle")
                version = attribute.get("version")
                setattr(self, id, (handle, int(version)))

        if (children_node := node.find("children")) is not None:
            self.children.load(children_node)

    def xml(self) -> Element:
        """Returns an XML encoding of the node."""
        element = Element("node", id=self._id_)
        for id, attribute in self._attributes_.items():
            if (value := getattr(self, id, None)) is not None:
                element.append(attribute.xml(id, value))
        if len(self._child_types_) > 0:
            children: detail.LsxChildren[Self] = getattr(self, "children")
            element.append(children.xml())
        return element

    def __str__(self) -> str:
        attributes = []
        for name in self._attributes_.keys():
            if (value := getattr(self, name)) is not None:
                attributes.append(f"{name}='{value}'" if isinstance(value, str) else f"{name}={str(value)}")
        if len(self._child_types_) > 0:
            children: detail.LsxChildren[Self] = getattr(self, "children")
            attributes.append(f"children={children}")
        return f"{self._id_}({", ".join(attributes)})"
