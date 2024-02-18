#!/usr/bin/env python3
"""
A class representing game data parsed from Modifiers.txt.
"""

import modtools.gamedata.valuelists as VL

from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Set
from typing import ClassVar


class GameData(metaclass=ABCMeta):
    """Representation of game data ("Modifiers")."""

    _LIST_TYPES = (list, tuple, set)

    _id_: ClassVar[str]                      # The data's id attribute (defaulting to the subclass name).
    _fields_: ClassVar[dict[str, Set[str]]]  # The data's field definitions.

    name: str
    using: str

    @abstractmethod
    def filename(self) -> str:
        """Return the filename for this game data object."""
        pass

    @classmethod
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        cls._id_ = str(cls.__dict__.get("_id_", cls.__name__))
        cls._fields_ = dict()

        for member_name, value in list(cls.__dict__.items()):
            if value in VL.VALUELISTS:
                cls._fields_[member_name.replace(" ", "_")] = value

        for member_name in cls._fields_:
            getter, setter = cls._wrap_accessors(member_name)
            prop = property(fget=getter, fset=setter)
            setattr(cls, member_name, prop)

    def __str__(self) -> str:
        """Returns a game data string."""
        s = f"""new entry "{self.name}"\n"""

        # Fixed order prologue
        s += f"""type "{self._id_}"\n"""
        if spell_type := getattr(self, "SpellType", None):
            s += f"""data "SpellType" "{spell_type[0]}"\n"""
        if status_type := getattr(self, "StatusType", None):
            s += f"""data "StatusType" "{status_type[0]}"\n"""
        if self.using:
            s += f"""using "{self.using}"\n"""

        # Sorted order data
        for key in self._fields_.keys():
            if key not in ("SpellType", "StatusType"):
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
