#!/usr/bin/env python3
"""
Representation of a collection of .lsx child nodes.
"""

from collections.abc import Iterable
from modtools.lsx_v3.node import LsxNode
from typing import Self


class LsxChildren:
    """A class representing a collection of .lsx child nodes."""

    _allowed_child_types: tuple[type[LsxNode]]
    _children: list[LsxNode]

    def __init__(self, children: Iterable[LsxNode], allowed_child_types: tuple[type[LsxNode]] = (LsxNode,)):
        self._check_child_types("allowed_child_types", allowed_child_types, (LsxNode,))
        self._check_child_types("children", [type(child) for child in children], allowed_child_types)
        self._allowed_child_types = tuple(allowed_child_types)
        self._children = list(children)

    def __len__(self) -> int:
        return len(self._children)

    def __getitem__(self, index: int) -> LsxNode:
        return self._children[index]

    def __setitem__(self, index: int, child: LsxNode) -> None:
        self._check_child_types("assignment", (type(child),), self._allowed_child_types)
        self._children[index] = child

    def __iter__(self) -> Iterable[LsxNode]:
        return iter(self._children)

    def __add__(self, children: Iterable[LsxNode]) -> Self:
        return self.copy().extend(children)

    def append(self, child: LsxNode) -> Self:
        self._check_child_types("append", (type(child),), self._allowed_child_types)
        self._children.append(child)
        return self

    def clear(self) -> Self:
        self._children.clear()
        return self

    def copy(self) -> Self:
        return LsxChildren(self._children.copy(), self._allowed_child_types)

    def extend(self, children: Iterable[LsxNode]) -> Self:
        self._check_child_types("extend", [type(child) for child in children], self._allowed_child_types)
        self._children.extend(children)
        return self

    def _check_child_types(self,
                           name: str,
                           children: Iterable[type[LsxNode]],
                           allowed_child_types: tuple[type[LsxNode]]) -> None:
        invalid_types = [t.__name__ for t in filter(lambda t: not issubclass(t, allowed_child_types), children)]
        if len(invalid_types) > 0:
            raise TypeError(f"Invalid type(s) for {name}: {", ".join(invalid_types)}")
