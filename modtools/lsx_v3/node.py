#!/usr/bin/env python3
"""
Representation of .lsx nodes.
"""

from modtools.lsx_v3.attributes import LsxAttribute


class LsxNode:
    """A class representing an .lsx node."""

    _attributes_: dict[str, LsxAttribute]

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._attributes_ = {}
        for member_name, data_type in list(cls.__dict__.items()):
            if isinstance(data_type, LsxAttribute):
                cls._attributes_[member_name] = data_type

        for member_name, data_type in cls._attributes_.items():
            getter, setter = data_type.wrap_accessors("_" + member_name)
            prop = property(fget=getter, fset=setter)
            setattr(cls, member_name, prop)

    def __init__(self, **kwds):
        for name, value in kwds.items():
            if name not in self._attributes_:
                raise AttributeError(f"{self.__class__.__name__}.{name} is not defined", obj=self, name=name)
            setattr(self, name, value)

    def __str__(self) -> str:
        attributes = []
        for name in sorted(self._attributes_.keys()):
            if (value := getattr(self, name)) is not None:
                attributes.append(f"{name}={repr(value)}")
        return f"{self.__class__.__name__}({", ".join(attributes)})"
