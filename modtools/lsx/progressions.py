#!/usr/bin/env python3
"""
Progression definitions.
"""

from modtools.lsx.builders import LsxBuilder, NodeBuilder
from modtools.lsx.characterclasses import CharacterClass
from modtools.lsx.types import DataType, LsxCollection, Node
from typing import Final, NamedTuple


class ProgressionKey(NamedTuple):
    name: str
    level: int
    is_multiclass: bool

    @classmethod
    def for_node(cls, node: Node) -> "ProgressionKey":
        """Return a key for a given node."""
        return cls(
            CharacterClass(node["Name"].value).name,
            int(node["Level"].value),
            node["IsMulticlass"].value.lower() == "true" if "IsMulticlass" in node else False
        )


ProgressionSubclass: Final = NodeBuilder("SubClass", key_attribute=None, attributes={
    "Object": DataType.GUID,
})

ProgressionSubclasses: Final = NodeBuilder("SubClasses", key_attribute=None, child_builders=[
    ProgressionSubclass,
])

Progression: Final = NodeBuilder("Progression", {
        "AllowImprovement": DataType.BOOL,
        "Boosts": DataType.LSSTRING,
        "IsMulticlass": DataType.BOOL,
        "Level": DataType.UINT8,
        "Name": DataType.LSSTRING_VALUE,
        "PassivesAdded": DataType.LSSTRING,
        "PassivesRemoved": DataType.LSSTRING,
        "ProgressionType": DataType.UINT8,
        "Selectors": DataType.LSSTRING,
        "TableUUID": DataType.GUID,
        "UUID": DataType.GUID,
    },
    child_builders=[
        ProgressionSubclasses,
    ],
)

PROGRESSIONS_LSX_PATH: Final = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
PROGRESSIONS_DEV_LSX_PATH: Final = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"

Progressions: Final = LsxBuilder("Progressions", "root", Progression, "Public/{0}/Progressions/Progressions.lsx")

LsxCollection.register(Progression, Progressions)
