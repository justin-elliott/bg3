#!/usr/bin/env python3
"""
Representation of a collection of .lsx child nodes.
"""

from collections.abc import Callable, Iterable
from typing import Self


class LsxChildren[Node]:
    """A class representing a collection of .lsx child nodes."""

    type KeyFunction = Callable[[Node], any]  # A function returning a key identifying a child node.
    type Predicate = Callable[[Node], bool]   # A predicate testing a child node.

    _allowed_child_types: tuple[Node, ...]
    _children: list[Node]

    def __init__(self, children: Iterable[Node] = [], *, allowed_child_types: Iterable[Node]):
        """Initialize the collection, setting the allowed child types and, optionally, the children."""
        self._allowed_child_types = tuple(allowed_child_types)
        self._check_child_types([type(child) for child in children], self._allowed_child_types)
        self._children = list(children)

    def __len__(self) -> int:
        return len(self._children)

    def __getitem__(self, index: int) -> Node:
        return self._children[index]

    def __setitem__(self, index: int, child: Node) -> None:
        self._check_child_types((type(child),), self._allowed_child_types)
        self._children[index] = child

    def __iter__(self) -> Iterable[Node]:
        return iter(self._children)

    def __add__(self, children: Iterable[Node]) -> Self:
        return self.copy().extend(children)

    def __str__(self) -> str:
        return f"[{", ".join(str(child) for child in self._children)}]"

    def append(self, child: Node) -> Self:
        self._check_child_types((type(child),), self._allowed_child_types)
        self._children.append(child)
        return self

    def clear(self) -> Self:
        self._children.clear()
        return self

    def extend(self, children: Iterable[Node]) -> Self:
        self._check_child_types([type(child) for child in children], self._allowed_child_types)
        self._children.extend(children)
        return self

    def update(self, children: Iterable[Node], key: KeyFunction) -> Self:
        """
        Update this collection with the contents of 'children', overwriting existing entries with the same key as the
        incoming children.
        """
        self._check_child_types([type(child) for child in children], self._allowed_child_types)
        lhs = {key(child): child for child in self._children}
        rhs = {key(child): child for child in children}
        lhs.update(rhs)
        self._children = list(lhs.values())
        return self

    def copy(self, *, predicate: Predicate | None = None) -> Self:
        """Create a copy of this collection, optionally including only children that match the 'predicate'."""
        return LsxChildren(list(filter(predicate, self._children) if predicate else self._children),
                           allowed_child_types=self._allowed_child_types)

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

    def _check_child_types(self, children: Iterable[Node], allowed_child_types: tuple[Node, ...]) -> None:
        invalid_types = [t.__name__ for t in filter(lambda t: not issubclass(t, allowed_child_types), children)]
        if len(invalid_types) > 0:
            raise TypeError(f"Invalid type(s) for children: {", ".join(invalid_types)}")

    @staticmethod
    def _wrap_accessors(member: str, allowed_child_types: Iterable[Node]) -> tuple[Callable[[object], any],
                                                                                   Callable[[object, any], None]]:
        def getter(obj: object) -> LsxChildren:
            return obj.__dict__.setdefault(member, LsxChildren(allowed_child_types=allowed_child_types))

        def setter(obj: object, children: Iterable[Node]) -> None:
            setattr(obj, member, LsxChildren(children, allowed_child_types=allowed_child_types))

        return (getter, setter)
