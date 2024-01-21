#!/usr/bin/env python3
"""
Test code for modtools.lsx_v2.
"""

from modtools.lsx_v2 import Attribute, DataType, Lsx, Node, NodeBuilder


progression_subclass = NodeBuilder("SubClass", key="Object", attributes={
    "Object": DataType.GUID,
})

progression_subclasses = NodeBuilder("SubClasses", key=None, child_builders=[
    progression_subclass
])

progression = NodeBuilder("Progression", {
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
        progression_subclasses,
    ],
)

progressions = Lsx("Progressions", "root", progression)

node = progression(
    Boosts=[
        "Proficiency(LightArmor)",
        "Proficiency(MediumArmor)",
        "Proficiency(HeavyArmor)",
        "Proficiency(Shields)",
        "Proficiency(SimpleWeapons)",
        "Proficiency(MartialWeapons)",
    ],
    IsMulticlass=True,
    Level=1,
    Name="Sorcerer",
    PassivesAdded=[
        "UnlockedSpellSlotLevel1",
        "SorcererBattlemage_BattleMagic",
        "SculptSpells",
    ],
    ProgressionType=0,
    Selectors=[
        "SelectSpells(485a68b4-c678-4888-be63-4a702efbe391,4,0,SorcererCantrip,,,AlwaysPrepared)",
        "SelectSpells(92c4751f-6255-4f67-822c-a75d53830b27,2,0,SorcererSpell)",
        "AddSpells(7f5b917c-be99-4f36-a87c-09a58bc56290,,,,AlwaysPrepared)",
    ],
    TableUUID="e2416b02-953a-4ce8-aa8f-eb98d549d86d",
    UUID="e115c732-80b1-4ae1-bf04-cee44660d64f",
    children=[
        progression_subclasses(
            children=[
                progression_subclass(Object="14374d37-a70e-41a8-9dc5-85a23f8b5dd2"),
                progression_subclass(Object="36286b0a-26f9-4b4e-9311-fd1404301d20"),
                progression_subclass(Object="d379fdae-b401-4731-8d50-277c73919ae3"),
            ]
        )
    ]
)

print(node)
