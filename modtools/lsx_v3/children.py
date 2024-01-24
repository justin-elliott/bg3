"""
Representation of .lsx children nodes.
"""

from collections.abc import Callable
from modtools.lsx_v3.attributes import LsxAttribute
from modtools.lsx_v3.node import LsxNode


class LsxChildren(LsxAttribute):
    """An attribute subclass representing a list of child nodes."""

    _allowed_children: tuple[LsxNode]

    def __init__(self, *allowed_children: LsxNode):
        super().__init__("children")
        self._allowed_children = tuple(allowed_children)

    def wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                   Callable[[object, any], None],
                                                   Callable[[object], None]]:
        def getter(obj: object) -> list[LsxNode] | None:
            store: dict = obj.__dict__.setdefault(member, {})
            return store.get("children")

        def setter(obj: object, children: list[LsxNode] | None) -> None:
            for child in children:
                if not isinstance(child, self._allowed_children):
                    raise TypeError(f"Invalid type for child node: {child.__class__.__name__}")
            store: dict = obj.__dict__.setdefault(member, {})
            store["children"] = list(children)

        return (getter, setter)
