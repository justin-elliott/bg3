#!/usr/bin/env python3
"""
Registration, loading, and saving of .lsx documents
"""

import os

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from typing import ClassVar
from xml.etree.ElementTree import parse as xml_parse


class Lsx:
    """A class implementing registering, loading, and saving .lsx documents."""

    _document_types: ClassVar[dict[str, type[LsxDocument]]] = {}
    _child_mapping: ClassVar[dict[type[LsxNode], type[LsxDocument]]] = {}

    _children: LsxChildren

    def __init__(self):
        self._children = LsxChildren()

    @property
    def children(self) -> LsxChildren:
        return self._children

    @classmethod
    def register(cls, document_type: type[LsxDocument]) -> None:
        """Register all of the child types that the document manages against the document."""
        region = getattr(document_type, "_region")
        cls._document_types[region] = document_type

        for child_type in document_type._child_types_:
            if (existing_owner := cls._child_mapping.get(child_type)) is not None and document_type != existing_owner:
                raise ValueError(f"{Lsx.register.__qualname__}({region}): "
                                 f"{child_type.__name__} is already registered to "
                                 f"{cls._child_mapping[child_type].__name__}")
            cls._child_mapping[child_type] = document_type

    @classmethod
    def load(cls, path: os.PathLike) -> LsxDocument:
        with open(path, "rb") as f:
            element = xml_parse(f).getroot()

            # Parse the document preamble: <save><region id="..."><node id="..."><children>
            if element.tag != "save":
                raise KeyError(f"{Lsx.load.__qualname__} missing <save> node in LSX document '{path}'")

            region = element.find("region")
            if region is None:
                raise KeyError(f"{Lsx.load.__qualname__} missing <region> node in LSX document '{path}'")

            region_id = region.get("id")
            if (document_type := Lsx._document_types.get(region_id)) is None:
                raise TypeError(f"{Lsx.load.__qualname__} unsupported LSX document type: {region_id}")

            root = region.find("node")
            document_root = getattr(document_type, "_root")
            if root is None or root.get("id") != document_root:
                raise KeyError(f"{Lsx.load.__qualname__} expected root id='{document_type.root}' in LSX document")

            document = document_type()

            if document_root == "Tags":
                document.load(root)
            elif (children_node := root.find("children")) is not None:
                document.load(children_node)

            return document

    def save(self, mod_path: os.PathLike, *,
             version: tuple[int, int, int, int] | None = None,
             **kwds: str) -> None:
        """Save each child to the appropriate .lsx file."""
        documents: dict[type[LsxDocument], LsxDocument] = {}

        for child in self.children:
            if (document_type := Lsx._child_mapping.get(type(child))) is None:
                raise TypeError(f"{Lsx.save.__qualname__}: {type(child).__name__} is not registered")
            document = documents.setdefault(document_type, document_type())
            children: LsxChildren = document.children
            children.append(child)

        for document in documents.values():
            document.save(mod_path, version=version, **kwds)
