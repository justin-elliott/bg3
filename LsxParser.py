#!/usr/bin/env python3
"""
Parser for .lsx files.
"""

import os

from dataclasses import dataclass, field
from modtools.unpak import Unpak
from operator import itemgetter
from pathlib import PurePath
from typing import Self
from xml.etree.ElementTree import XMLParser


@dataclass
class Node:
    id: str
    attributes: dict[str, set[str]] = field(default_factory=dict)
    children: dict[str, Self] = field(default_factory=dict)


class LsxParser:
    """Parser for .lsx files."""
    class UnexpectedTagError(Exception):
        def __init__(self, *args: any):
            super().__init__(*args)

    class Lsx:
        version: tuple[int, int, int, int] | None
        region_id: str | None
        root: Node | None

        __node_stack: list[Node]

        def __init__(self):
            self.version = None
            self.region_id = None
            self.root = None
            self.__node_stack = [Node("")]  # Sentinel to ensure that there is always a parent node

        def start(self, tag: str, attributes: dict) -> None:
            match tag:
                case "save":
                    pass
                case "version":
                    self.version = itemgetter("major", "minor", "revision", "build")(attributes)
                case "region":
                    self.region_id = attributes.get("id", "")
                case "node":
                    node_id = attributes.get("id", "")
                    parent_node = self.__node_stack[-1]
                    node = parent_node.children.get(node_id, None)
                    if node is None:
                        node = Node(node_id)
                        parent_node.children[node_id] = node
                    self.__node_stack.append(node)
                case "attribute":
                    node = self.__node_stack[-1]
                    attribute_id = attributes.get("id")
                    node_attrs = node.attributes.setdefault(attribute_id, set())
                    node_attrs.add(attributes.get("type"))
                case "children":
                    pass
                case _:
                    raise LsxParser.UnexpectedTagError(f"Tag <{tag}> was not expected")

        def end(self, tag: str) -> None:
            if tag == "node":
                node = self.__node_stack.pop()
                if len(self.__node_stack) == 1:  # The root node is just above the sentinel
                    self.root = node

    __unpak: Unpak

    def __init__(self, unpak: Unpak):
        self.__unpak = unpak

    def parse(self, lsx_path: os.PathLike) -> None:
        pak_name, _, relative_path = str(PurePath(lsx_path).as_posix()).partition("/")
        cached_pak = self.__unpak.get(pak_name)
        cached_path = os.path.join(cached_pak.path, relative_path)
        lsx = LsxParser.Lsx()
        xml_parser = XMLParser(target=lsx)
        with open(cached_path, "rb") as lsx_file:
            for line in lsx_file:
                xml_parser.feed(line)
        print(lsx.version)
        print(lsx.region_id)
        print(lsx.root)


def main():
    unpak = Unpak(cache_dir=None)
    lsx_parser = LsxParser(unpak)
    lsx_parser.parse("Shared/Public/Shared/Progressions/Progressions.lsx")
    lsx_parser.parse("Shared/Public/SharedDev/Progressions/Progressions.lsx")


if __name__ == "__main__":
    main()
