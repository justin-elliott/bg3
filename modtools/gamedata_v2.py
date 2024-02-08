#!/usr/bin/env python3
"""
Representation of game data declarations from Modifiers.txt.
"""

from collections.abc import Callable, Set
from modtools.valuelists_v2 import VALUELISTS
from typing import ClassVar


class GameData:
    """Representation of game data ("Modifiers")."""

    _LIST_TYPES = (list, tuple, set)

    _id_: ClassVar[str]                      # The data's id attribute (defaulting to the subclass name).
    _fields_: ClassVar[dict[str, Set[str]]]  # The data's field definitions.

    name: str
    using: str

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._id_ = str(cls.__dict__.get("_id_", cls.__name__))
        cls._fields_ = dict()

        for member_name, value in list(cls.__dict__.items()):
            if value in VALUELISTS:
                cls._fields_[member_name.replace(" ", "_")] = value

        for member_name in cls._fields_:
            getter, setter = cls._wrap_accessors(member_name)
            prop = property(fget=getter, fset=setter)
            setattr(cls, member_name, prop)

    def __init__(self, name: str, **kwds):
        self.name = name
        self.using = None

        for key, value in kwds.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        """Returns a game data string."""
        s = f"new entry \"{self.name}\"\n"
        s += f"type \"{self._id_}\"\n"
        if self.using:
            s += f"using \"{self.using}\"\n"
        for key in self._fields_.keys():
            if (values := getattr(self, key, None)) is not None:
                if len(values) == 1:
                    values = values[0]
                else:
                    values = ";".join(values)
                s += f"data \"{key.replace("_", " ")}\" \"{values}\"\n"
        return s

    @classmethod
    def _wrap_accessors(cls, member_name: str) -> tuple[Callable[[object], any],
                                                        Callable[[object, any], None]]:
        private_member = "_" + member_name
        member_type = cls._fields_[member_name]

        def getter(obj: object) -> list[str] | None:
            return obj.__dict__.get(private_member)

        def setter(obj: object, values: list[str] | None) -> None:
            if values is not None:
                if not isinstance(values, cls._LIST_TYPES):
                    values = [value for value in str(values).split(";") if value]
                values = [str(member_type(value)) for value in values]
            obj.__dict__[private_member] = values

        return (getter, setter)
