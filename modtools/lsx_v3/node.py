#!/usr/bin/env python3
"""
Representation of .lsx nodes.
"""

from modtools.lsx_v3.attributes import LsxAttribute
from typing import Self


class LsxNode:
    """A class representing an .lsx node."""

    _attributes_: dict[str, LsxAttribute]
    _children_: tuple[type[Self]]

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._attributes_ = {}
        cls._children_ = ()
        for member_name, data_type in list(cls.__dict__.items()):
            if member_name == "children":
                invalid_types = [t.__name__ for t in filter(lambda t: not issubclass(t, LsxNode), data_type)]
                if len(invalid_types) > 0:
                    raise TypeError(f"Invalid type(s) for children: {", ".join(invalid_types)}")
                cls._children_ = tuple(data_type)
            elif isinstance(data_type, LsxAttribute):
                cls._attributes_[member_name] = data_type

        for member_name, data_type in cls._attributes_.items():
            getter, setter = data_type.wrap_accessors("_" + member_name)
            prop = property(fget=getter, fset=setter)
            setattr(cls, member_name, prop)

        if len(cls._children_) > 0:
            setattr(cls, "children", property())

    def __init__(self, **kwds):
        for name, value in kwds.items():
            if name not in self._attributes_:
                raise AttributeError(f"{self.__class__.__name__}.{name} is not defined", obj=self, name=name)
            setattr(self, name, value)

    def __str__(self) -> str:
        attributes = []
        for name in sorted(self._attributes_.keys(), key=lambda name: (name == "children", name)):
            if (value := getattr(self, name)) is not None:
                attributes.append(f"{name}='{value}'" if isinstance(value, str) else f"{name}={str(value)}")
        return f"{self.__class__.__name__}({", ".join(attributes)})"
