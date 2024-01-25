#!/usr/bin/env python3
"""
Representation of .lsx nodes.
"""

from modtools.lsx_v3.attributes import LsxAttribute
from typing import Self
from xml.etree.ElementTree import Element

import modtools.lsx_v3.detail as detail


class LsxNode:
    """A class representing an .lsx node."""

    _attributes_: dict[str, LsxAttribute]
    _allowed_child_types_: tuple

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._attributes_ = {}
        cls._allowed_child_types_ = ()
        for member_name, data_type in list(cls.__dict__.items()):
            if member_name == "children":
                cls._allowed_child_types_ = tuple(data_type)
            elif isinstance(data_type, LsxAttribute):
                cls._attributes_[member_name] = data_type

        for member_name, data_type in cls._attributes_.items():
            getter, setter = data_type._wrap_accessors("_" + member_name)
            prop = property(fget=getter, fset=setter)
            setattr(cls, member_name, prop)

        if len(cls._allowed_child_types_) > 0:
            getter, setter = detail.LsxChildren[Self]._wrap_accessors("_children", cls._allowed_child_types_)
            setattr(cls, "children", property(fget=getter, fset=setter))

    def __init__(self, **kwds):
        for name, value in kwds.items():
            if name not in self._attributes_ and getattr(self, name, None) is None:
                raise AttributeError(f"{self.__class__.__name__}.{name} is not defined", obj=self, name=name)
            setattr(self, name, value)

    def xml(self) -> Element:
        """Returns an XML encoding of the node."""
        element = Element("node", id=self.__class__.__name__)
        for id, attribute in sorted(self._attributes_.items()):
            if (value := getattr(self, id, None)) is not None:
                element.append(attribute.xml(id, value))
        if len(self._allowed_child_types_) > 0:
            element.append(self.children.xml())
        return element

    def __str__(self) -> str:
        attributes = []
        for name in sorted(self._attributes_.keys(), key=lambda name: (name == "children", name)):
            if (value := getattr(self, name)) is not None:
                attributes.append(f"{name}='{value}'" if isinstance(value, str) else f"{name}={str(value)}")
        return f"{self.__class__.__name__}({", ".join(attributes)})"
