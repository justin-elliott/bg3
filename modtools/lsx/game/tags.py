#!/usr/bin/env python3
"""
Tags definitions.
"""

import os

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType
from xml.etree.ElementTree import Element, SubElement


class Tags(LsxDocument, LsxNode):
    class Tags(LsxNode):
        class Categories(LsxNode):
            class Category(LsxNode):
                Name: str = LsxType.LSSTRING_VALUE

                def __init__(self, *, Name: str = None):
                    super().__init__(Name=Name)

            children: LsxChildren = (Category,)

            def __init__(self, *, children: LsxChildren = None):
                super().__init__(children=children)

        Description: str = LsxType.LSSTRING_VALUE
        DisplayDescription: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
        DisplayName: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
        Icon: str = LsxType.FIXEDSTRING
        Name: str = LsxType.FIXEDSTRING
        UUID: str = LsxType.GUID
        children: LsxChildren = (Categories,)

        def __init__(self,
                     *,
                     Description: str = None,
                     DisplayDescription: tuple[str, int] | str = None,
                     DisplayName: tuple[str, int] | str = None,
                     Icon: str = None,
                     Name: str = None,
                     UUID: str = None,
                     children: LsxChildren = None):
            super().__init__(
                Description=Description,
                DisplayDescription=DisplayDescription,
                DisplayName=DisplayName,
                Icon=Icon,
                Name=Name,
                UUID=UUID,
                children=children,
            )

    root = "Tags"
    path = "Public/{folder}/Tags/{tag_name}.lsf.lsx"
    children: LsxChildren = (Tags,)

    def load(self, node: Element) -> None:
        """Load the single child."""
        child = Tags.Tags()
        child.load(node)
        self.children.append(child)

    def save(self, mod_path: os.PathLike, *,
             version: tuple[int, int, int, int] | None = None,
             **kwds: str) -> None:
        """Retrieve the tag name for path formatting."""
        assert len(self.children) == 1

        tag: Tags.Tags = self.children[0]
        tag_name = tag.Name
        super().save(mod_path, version=version, tag_name=tag_name, **kwds)

    def xml(self, *, version: tuple[int, int, int, int] | None = None) -> Element:
        """Returns an XML encoding of the document. This replaces the <node><children> root with the tag <node>."""
        assert len(self.children) == 1

        element = Element("save")
        if version:
            SubElement(element, "version", {
                attr: str(ver) for attr, ver in zip(("major", "minor", "revision", "build"), version)
            })
        region = SubElement(element, "region", id=self.region)
        tag: Tags.Tags = self.children[0]
        region.append(tag.xml())
        return element


Lsx.register(Tags)
