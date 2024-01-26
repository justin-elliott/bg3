#!/usr/bin/env python3
"""
Parser for .lsx files.
"""

import argparse
import os

from modtools.lsx.type import LsxType
from modtools.unpak import Unpak
from operator import itemgetter
from pathlib import PurePath
from typing import Self
from xml.etree.ElementTree import XMLParser


PROLOGUE = '''\
#!/usr/bin/env python3
"""
LSX definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType

'''


class Attribute:
    id: str
    fields: dict[str, set[str]]  # name -> values

    def __init__(self, xml_attrs: dict[str, str]):
        self.id = xml_attrs.get("id")
        self.fields = {
            field: set([value]) for field, value in xml_attrs.items() if field != "id"
        }

    def merge(self, other: Self) -> Self:
        for field, values in other.fields.items():
            if (our_values := self.fields.setdefault(field, values)) != values:
                our_values |= values
        return self

    def __str__(self, indent: int = 0) -> str:
        pad = " " * (indent * 4)
        s = f"{pad}{self.id}("
        fields = []
        for field, values in self.fields.items():
            f = field
            if len(values) > 0:
                f += f"=\"{"|".join(list(values))}\""
            fields.append(f)
        s += ", ".join(fields)
        s += ")"
        return s


class Node:
    id: str
    attributes: dict[str, Attribute]
    children: dict[str, Self]

    def __init__(self, xml_attrs: dict[str, str]):
        self.id = xml_attrs.get("id")
        self.attributes = {}
        self.children = {}

    def __str__(self, indent: int = 0) -> str:
        pad = " " * (indent * 4)
        s = f"{pad}{self.id}(\n"
        for _, attribute in sorted(self.attributes.items()):
            s += f"{attribute.__str__(indent + 1)}\n"
        if len(self.children) > 0:
            s += f"{pad}    children=[\n"
            for _, child in sorted(self.children.items()):
                s += f"{child.__str__(indent + 2)}\n"
            s += f"{pad}    ]\n"
        s += f"{pad})"
        return s


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
            self.__node_stack = [Node({"id": ""})]  # Sentinel to ensure that there is always a parent node

        def start(self, xml_tag: str, xml_attrs: dict) -> None:
            match xml_tag:
                case "save":
                    pass
                case "version":
                    self.version = itemgetter("major", "minor", "revision", "build")(xml_attrs)
                case "region":
                    self.region_id = xml_attrs.get("id", "")
                case "node":
                    node = Node(xml_attrs)
                    parent_node = self.__node_stack[-1]
                    node = parent_node.children.setdefault(node.id, node)
                    self.__node_stack.append(node)
                case "attribute":
                    attribute = Attribute(xml_attrs)
                    node = self.__node_stack[-1]
                    if (node_attrs := node.attributes.setdefault(attribute.id, attribute)) != attribute:
                        node_attrs.merge(attribute)
                case "children":
                    pass
                case _:
                    raise LsxParser.UnexpectedTagError(f"Tag <{xml_tag}> was not expected")

        def end(self, xml_tag: str) -> None:
            if xml_tag == "node":
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

        print(PROLOGUE)
        for child in lsx.root.children.values():
            self.output_node(child)

        print(f"class {lsx.region_id}(LsxDocument):")
        if lsx.root.id != "root":
            print(f'    root = "{lsx.root.id}"')
        print(f'    path = "{lsx_path}"')
        self.output_child_list(lsx.root)

        print()
        print()
        print(f"Lsx.register({lsx.region_id})")

    def output_node(self, node: Node) -> None:
        for child in node.children.values():
            self.output_node(child)

        print(f"class {node.id}(LsxNode):")

        for name, attribute in sorted(node.attributes.items()):
            attribute_type = attribute.fields["type"]
            for sub_type in attribute_type:
                type_name = LsxType.BY_NAME[sub_type]

                if type_name == "LSSTRING" and (values := attribute.fields.get("value")) is not None:
                    has_commas = any("," in text and "(" not in text for text in values)
                    if has_commas:
                        type_name = "LSSTRING_COMMA"
                    else:
                        has_semicolons = any(";" in text for text in values)
                        if not has_semicolons:
                            type_name = "LSSTRING_VALUE"

                if len(attribute_type) == 1:
                    sub_name = ""
                    comment = ""
                else:
                    sub_name = "_" + sub_type
                    comment = f"  # {name}"

                python_type = getattr(LsxType, type_name)._python_type
                print(f"    {name}{sub_name}: {python_type} = LsxType.{type_name}{comment}")

        self.output_child_list(node)

        if len(node.attributes) == 0 and len(node.children) == 0:
            print("    pass")

        print()
        print()

    def output_child_list(self, node: Node) -> None:
        child_list = ", ".join(node.children.keys())
        if len(node.children) == 1:
            child_list += ","
        if len(child_list) > 100 and len(node.children) > 1:
            print("    children = (")
            for child in node.children.keys():
                print(f"        {child},")
            print("    )")
        elif len(node.children) > 0:
            print(f"    children = ({child_list})")


def main():
    parser = argparse.ArgumentParser(description="Generate LSX definitions from an .lsx file.")
    parser.add_argument("pak_path", type=str, default=None, help="Path to .lsx file within a .pak.")
    args = parser.parse_args()

    unpak = Unpak(cache_dir=None)
    lsx_parser = LsxParser(unpak)
    lsx_parser.parse(args.pak_path)


if __name__ == "__main__":
    main()
