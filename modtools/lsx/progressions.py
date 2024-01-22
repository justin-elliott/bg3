#!/usr/bin/env python3
"""
Test code for modtools.lsx_v2.
"""

from modtools.lsx.builders import LsxBuilder, NodeBuilder
from modtools.lsx.types import DataType


ProgressionSubclass = NodeBuilder("SubClass", key_attribute="Object", attributes={
    "Object": DataType.GUID,
})

ProgressionSubclasses = NodeBuilder("SubClasses", key_attribute=None, child_builders=[
    ProgressionSubclass
])

Progression = NodeBuilder("Progression", {
        "AllowImprovement": DataType.BOOL,
        "Boosts": DataType.LSSTRING,
        "IsMulticlass": DataType.BOOL,
        "Level": DataType.UINT8,
        "Name": DataType.LSSTRING,
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

Progressions = LsxBuilder("Progressions", "root", Progression)
