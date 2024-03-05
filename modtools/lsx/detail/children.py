#!/usr/bin/env python3
"""
Representation of a collection of .lsx child nodes.
"""

from collections.abc import Callable, Iterable
from typing import Self
from xml.etree.ElementTree import Element


class LsxChildren[Node]:
    """A class representing a collection of .lsx child nodes."""

    type KeyFunction = Callable[[Node], any]  # A function returning a key identifying a child node.
    type Predicate = Callable[[Node], bool]   # A predicate testing a child node.

    _types: tuple[type[Node], ...]  # The child types that the collection can contain.
    _children: list[Node]           # The list of children.

    def __init__(self, children: Iterable[Node] = None, *, types: Iterable[Node]):
        """Initialize the collection, setting the expected child types and, optionally, the children."""
        if children is None:
            children = []
        self._types = tuple(types)
        self._check_child_types([type(child) for child in children])
        self._children = list(children)

    @property
    def types(self) -> tuple[type[Node], ...]:
        return self._types

    def __len__(self) -> int:
        return len(self._children)

    def __getitem__(self, index: int) -> Node:
        return self._children[index]

    def __setitem__(self, index: int, child: Node) -> None:
        self._check_child_types((type(child),))
        self._children[index] = child

    def __iter__(self) -> Iterable[Node]:
        return iter(self._children)

    def __add__(self, children: Iterable[Node]) -> Self:
        return self.copy().extend(children)

    def __str__(self) -> str:
        return f"[{", ".join(str(child) for child in self._children)}]"

    def append(self, child: Node) -> Self:
        self._check_child_types((type(child),))
        self._children.append(child)
        return self

    def clear(self) -> Self:
        self._children.clear()
        return self

    def extend(self, children: Iterable[Node]) -> Self:
        self._check_child_types([type(child) for child in children])
        self._children.extend(children)
        return self

    def sort(self, *, key: KeyFunction) -> Self:
        """Sort the collection by the key."""
        self._children.sort(key=key)

    def unique(self, *, key: KeyFunction) -> Self:
        """
        Remove duplicates from the collection by replacing earlier entries with later entries that have the same key.
        """
        self._children = list({key(child): child for child in self._children}.values())
        return self

    def update(self, children: Iterable[Node], *, key: KeyFunction) -> Self:
        """
        Update this collection with the contents of 'children', overwriting existing entries with the same key as the
        incoming children.
        """
        self._check_child_types([type(child) for child in children])
        lhs = {key(child): child for child in self._children}
        rhs = {key(child): child for child in children}
        lhs.update(rhs)
        self._children = list(lhs.values())
        return self

    def copy(self, *, predicate: Predicate | None = None) -> Self:
        """Create a copy of this collection, optionally including only children that match the 'predicate'."""
        return LsxChildren(list(filter(predicate, self._children) if predicate else self._children),
                           types=self._types)

    def find(self, predicate: Predicate) -> Node | None:
        """Return the first child that matches the 'predicate', or None if there is no match."""
        try:
            return next(self.finditer(predicate))
        except StopIteration:
            return None

    def findall(self, predicate: Predicate) -> list[Node]:
        """Return a list of all children matching the 'predicate'."""
        return list(self.finditer(predicate))

    def finditer(self, predicate: Predicate) -> list[Node]:
        """Return an iterator of all children matching the 'predicate'."""
        return filter(predicate, self._children)

    def keepall(self, predicate: Predicate) -> Self:
        """Keep only those children matching the 'predicate'."""
        self._children = [child for child in self._children if predicate(child)]
        return self

    def removeall(self, predicate: Predicate) -> Self:
        """Remove all children matching the 'predicate'."""
        self._children = [child for child in self._children if not predicate(child)]
        return self

    def load(self, children_node: Element) -> None:
        """Load the children from the given XML <children> node."""
        self._children.clear()

        for node in children_node.findall("node"):
            child_name = node.get("id")
            try:
                child_type: type[Node] = next(child_type for child_type in self._types if child_type._id_ == child_name)
            except StopIteration:
                raise TypeError(f"{LsxChildren.load.__qualname__} unsupported node id='{child_name}'")
            child = child_type()
            child.load(node)
            self._children.append(child)

    def xml(self) -> Element:
        """Returns an XML encoding of the children."""
        element = Element("children")
        for child in self._children:
            element.append(child.xml())
        return element

    def _check_child_types(self, children: Iterable[type[Node]]) -> None:
        invalid_types = [t.__name__ for t in filter(lambda t: not issubclass(t, self._types), children)]
        if len(invalid_types) > 0:
            raise TypeError(f"Invalid type(s) for children: {", ".join(invalid_types)}")

    @staticmethod
    def _wrap_accessors(member: str, types: Iterable[type[Node]]) -> tuple[Callable[[object], any],
                                                                           Callable[[object, any], None]]:
        def getter(obj: object) -> LsxChildren:
            return obj.__dict__.setdefault(member, LsxChildren(types=types))

        def setter(obj: object, children: Iterable[Node]) -> None:
            setattr(obj, member, LsxChildren(children, types=types))

        return (getter, setter)
