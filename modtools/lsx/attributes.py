#!/usr/bin/env python3
"""
Classes representing .lsx attributes.
"""

from abc import abstractmethod
from ast import literal_eval
from collections.abc import Callable
from numbers import Number
from xml.etree.ElementTree import Element


class LsxAttribute:
    """An abstract class representing an .lsx attribute."""

    _python_type: str  # The attribute's Python type name
    _type_name: str    # The attribute's .lsx 'type' XML attribute

    def __init__(self, python_type: str, type_name: str):
        self._python_type = python_type
        self._type_name = type_name

    @abstractmethod
    def xml(self, id: str, value: any) -> Element:
        """Returns an XML encoding of the attribute."""
        pass

    @abstractmethod
    def _wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                    Callable[[object, any], None]]:
        """Returns the get and set accessors for the LsxAttribute."""
        pass


class LsxBool(LsxAttribute):
    """An attribute subclass representing a Boolean."""

    def __init__(self, type_name: str):
        super().__init__("bool", type_name)

    def xml(self, id: str, value: bool) -> Element:
        return Element("attribute", id=id, type=self._type_name, value=str(value).lower())

    def _wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                    Callable[[object, any], None]]:
        def getter(obj: object) -> bool | None:
            store: dict = obj.__dict__.setdefault(member, {})
            return store.get("bool")

        def setter(obj: object, value: bool | None) -> None:
            store: dict = obj.__dict__.setdefault(member, {})
            if isinstance(value, str):
                value = literal_eval(value.title())
            store["bool"] = bool(value) if value is not None else None

        return (getter, setter)


class LsxList(LsxAttribute):
    """An attribute subclass representing a list of strings."""

    LIST_TYPES = (list, tuple, set)

    _separator: str

    def __init__(self, type_name: str, separator: str = ";"):
        super().__init__("LsxChildren", type_name)
        self._separator = separator

    def xml(self, id: str, value: list) -> Element:
        return Element("attribute", id=id, type=self._type_name, value=self._separator.join(value))

    def _wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                    Callable[[object, any], None]]:
        def getter(obj: object) -> list[str] | None:
            store: dict = obj.__dict__.setdefault(member, {})
            return store.get("list")

        def setter(obj: object, values: list[str] | None) -> None:
            if values is not None:
                if not isinstance(values, LsxList.LIST_TYPES):
                    values = [x for x in str(values).split(self._separator) if x]
                else:
                    values = [str(x) for x in values]
            store: dict = obj.__dict__.setdefault(member, {})
            store["list"] = values

        return (getter, setter)


class LsxNumber(LsxAttribute):
    """An attribute subclass representing a Number."""

    def __init__(self, type_name: str):
        super().__init__("float" if type_name in ("float", "double") else "int", type_name)

    def xml(self, id: str, value: Number) -> Element:
        return Element("attribute", id=id, type=self._type_name, value=str(value))

    def _wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                    Callable[[object, any], None]]:
        def getter(obj: object) -> Number | None:
            store: dict = obj.__dict__.setdefault(member, {})
            return store.get("number")

        def setter(obj: object, value: Number | None) -> None:
            store: dict = obj.__dict__.setdefault(member, {})
            if isinstance(value, str):
                value = literal_eval(value)
            store["number"] = value if value is not None else None

        return (getter, setter)


class LsxString(LsxAttribute):
    """An attribute subclass representing a (non-list) string."""

    def __init__(self, type_name: str):
        super().__init__("str", type_name)

    def xml(self, id: str, value: str) -> Element:
        return Element("attribute", id=id, type=self._type_name, value=value)

    def _wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                    Callable[[object, any], None]]:
        def getter(obj: object) -> str | None:
            store: dict = obj.__dict__.setdefault(member, {})
            return store.get("str")

        def setter(obj: object, value: str | None) -> None:
            store: dict = obj.__dict__.setdefault(member, {})
            store["str"] = str(value) if value is not None else None

        return (getter, setter)


class LsxTranslation(LsxAttribute):
    """An attribute subclass representing a translated string."""

    def __init__(self, type_name: str):
        super().__init__("tuple[str, int] | str", type_name)

    def xml(self, id: str, value: tuple[str, int]) -> Element:
        handle, version = value
        return Element("attribute", id=id, type=self._type_name, handle=handle, version=str(version))

    def _wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                    Callable[[object, any], None]]:
        def getter(obj: object) -> tuple[str, int] | None:
            store: dict = obj.__dict__.setdefault(member, {})
            handle = store.get("handle")
            return (handle, store.get("version")) if handle is not None else None

        def setter(obj: object, value: str | tuple[str, int] | None) -> None:
            store: dict = obj.__dict__.setdefault(member, {})
            if not isinstance(value, tuple):
                value = (value, 1)
            handle, version = value
            store["handle"] = str(handle) if handle is not None else None
            store["version"] = int(version)

        return (getter, setter)
