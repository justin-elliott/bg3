#!/usr/bin/env python3
"""
Representation of .lsx documents.
"""

from collections.abc import Callable
from modtools.lsx_v3.children import LsxChildren
from modtools.lsx_v3.node import LsxNode
from xml.etree.ElementTree import Element, SubElement


class LsxDocument:
    """A class representing an .lsx document."""

    id: str
    region: str
    root: str
    children: tuple[type[LsxNode], ...]

    @classmethod
    def __init_subclass__(cls) -> None:
        missing_members = [member for member in ["region", "root", "children"] if member not in cls.__dict__]
        if missing_members:
            raise AttributeError(f"{cls.__name__} missing member(s): {", ".join(missing_members)}")

        child_types = tuple(cls.__dict__["children"])
        if len(child_types) == 0:
            raise TypeError(f"{cls.__name__} missing child types")

        setattr(cls, "_id", str(cls.__dict__["id"]) if "id" in cls.__dict__ else cls.__name__)
        setattr(cls, "id", property(fget=cls._wrap_getter("_id")))

        setattr(cls, "_region", str(cls.__dict__["region"]))
        setattr(cls, "region", property(fget=cls._wrap_getter("_region")))

        setattr(cls, "_root", str(cls.__dict__["root"]))
        setattr(cls, "root", property(fget=cls._wrap_getter("_root")))

        getter, setter = LsxChildren._wrap_accessors("_children", child_types)
        setattr(cls, "children", property(fget=getter, fset=setter))

    def __init__(self, *nodes: LsxNode):
        children: LsxChildren = self.children
        children.extend(nodes)

    def xml(self, version: tuple[int, int, int, int] | None = None) -> Element:
        """Returns an XML encoding of the document."""
        element = Element("save")
        if version:
            SubElement(element, "version", {
                attr: str(ver) for attr, ver in zip(("major", "minor", "revision", "build"), version)
            })
        region = SubElement(element, "region", id=self.region)
        root = SubElement(region, "node", id=self.root)
        root.append(self.children.xml())
        return element

    def __str__(self) -> str:
        return f"{self.id}(region='{self.region}', root='{self.root}', children={self.children})"

    @staticmethod
    def _wrap_getter(member: str) -> tuple[Callable[[object], str]]:
        def getter(obj: object) -> str:
            return getattr(obj, member)
        return getter
