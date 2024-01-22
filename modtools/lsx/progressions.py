#!/usr/bin/env python3
"""
Progression definitions.
"""

from modtools.lsx.builders import LsxBuilder, NodeBuilder
from modtools.lsx.types import DataType, LsxCollection
from typing import Final


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

PROGRESSIONS_LSX_PATH: Final = "Public/Shared/Progressions/Progressions.lsx"
PROGRESSIONS_DEV_LSX_PATH: Final = "Public/SharedDev/Progressions/Progressions.lsx"

Progressions: Final = LsxBuilder("Progressions", "root", Progression, PROGRESSIONS_LSX_PATH)

LsxCollection.register(Progression, Progressions)
