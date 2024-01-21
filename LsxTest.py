#!/usr/bin/env python3
"""
Test code for modtools.lsx_v2.
"""

import xml.etree.ElementTree as ElementTree

from modtools.lsx.progressions import Progression, Progressions, ProgressionSubclass, ProgressionSubclasses


progressions = Progressions(
    Progression(
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
            ProgressionSubclasses(
                children=[
                    ProgressionSubclass(Object="14374d37-a70e-41a8-9dc5-85a23f8b5dd2"),
                    ProgressionSubclass(Object="36286b0a-26f9-4b4e-9311-fd1404301d20"),
                    ProgressionSubclass(Object="d379fdae-b401-4731-8d50-277c73919ae3"),
                ]
            )
        ]
    )
)

progressions.add(
    Progression(
        Boosts=[
            "Proficiency(LightArmor)",
            "Proficiency(MediumArmor)",
            "Proficiency(HeavyArmor)",
            "Proficiency(Shields)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
        ],
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
        UUID="410ef291-f4ea-43c0-9b91-8f033b81a5f3",
        children=[
            ProgressionSubclasses(
                children=[
                    ProgressionSubclass(Object="14374d37-a70e-41a8-9dc5-85a23f8b5dd2"),
                    ProgressionSubclass(Object="36286b0a-26f9-4b4e-9311-fd1404301d20"),
                    ProgressionSubclass(Object="d379fdae-b401-4731-8d50-277c73919ae3"),
                ]
            )
        ]
    )
)

key = "410ef291-f4ea-43c0-9b91-8f033b81a5f3"
assert key in progressions
node = progressions.get(key)
del progressions[key]
assert key not in progressions
progressions[key] = node
assert progressions[key] is not None
progressions[key] = node
assert progressions[key] is not None

xml = progressions.xml(version=(4, 1, 1, 1))
ElementTree.indent(xml, space=" "*4)
ElementTree.dump(xml)
