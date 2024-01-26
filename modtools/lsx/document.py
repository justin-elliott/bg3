#!/usr/bin/env python3
"""
Representation of .lsx documents.
"""

import os

from collections.abc import Callable
from modtools.lsx.children import LsxChildren
from modtools.lsx.node import LsxNode
from modtools.prologue import XML_PROLOGUE
from xml.etree.ElementTree import Element, ElementTree, indent as xml_indent, SubElement


class LsxDocument:
    """A class representing an .lsx document."""

    _child_types_: tuple[type[LsxNode], ...] = ()

    region: str
    root: str
    path: str
    children: LsxChildren

    @classmethod
    def __init_subclass__(cls) -> None:
        missing_members = [member for member in ["path", "children"] if member not in cls.__dict__]
        if missing_members:
            raise AttributeError(f"{cls.__name__} missing member(s): {", ".join(missing_members)}")

        cls._child_types_ = tuple(cls.__dict__["children"])
        if len(cls._child_types_) == 0:
            raise TypeError(f"{cls.__name__} missing child types")

        setattr(cls, "_region", str(cls.__dict__.get("region", cls.__name__)))
        setattr(cls, "region", property(fget=cls._wrap_getter("_region")))

        setattr(cls, "_root", str(cls.__dict__.get("root", "root")))
        setattr(cls, "root", property(fget=cls._wrap_getter("_root")))

        setattr(cls, "_path", str(cls.__dict__["path"]))
        setattr(cls, "path", property(fget=cls._wrap_getter("_path")))

        getter, setter = LsxChildren._wrap_accessors("_children", cls._child_types_)
        setattr(cls, "children", property(fget=getter, fset=setter))

    def __init__(self, *nodes: LsxNode):
        self.children.extend(nodes)

    def load(self, children_node: Element) -> None:
        """Load the document's children from the given XML <children> node."""
        self.children.clear()

        for node in children_node.findall("node"):
            child_name = node.get("id")
            try:
                child_type: type[LsxNode] = next(
                    child_type for child_type in self._child_types_ if child_type._id_ == child_name)
            except StopIteration:
                raise TypeError(f"{LsxDocument.load.__qualname__} unsupported node id='{child_name}'")
            child = child_type()
            child.load(node)
            self.children.append(child)

    def save(self, mod_path: os.PathLike, *,
             version: tuple[int, int, int, int] | None = None,
             **kwds: str) -> None:
        """Save the document to the path identified by the document's 'path' property."""
        path = os.path.normpath(os.path.join(mod_path, self.path.format(**kwds)))
        document = ElementTree(self.xml(version=version))
        xml_indent(document, space=" "*4)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(XML_PROLOGUE)
            document.write(f, encoding="UTF-8", xml_declaration=False)

    def xml(self, *, version: tuple[int, int, int, int] | None = None) -> Element:
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
