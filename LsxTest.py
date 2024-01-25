#!/usr/bin/env python3
"""
Test code for modtools.lsx_v2.
"""

import os
import xml.etree.ElementTree as ElementTree

from modtools.lsx_v3.children import LsxChildren
from modtools.lsx_v3.node import LsxNode
from modtools.lsx_v3.type import LsxType
from modtools.lsx.characterclasses import CharacterClass, CharacterSubclasses
from modtools.lsx.progressions import (
    Progression,
    Progressions,
    ProgressionSubclass,
    ProgressionSubclasses
)
from modtools.unpak import Unpak


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

assert node["UUID"].value == key
assert node["ProgressionType"].value == "0"

xml = progressions.xml(version=(4, 1, 1, 1))
ElementTree.indent(xml, space=" "*4)
# ElementTree.dump(xml)

unpak = Unpak(cache_dir=None)
shared = unpak.get("Shared")

class_progressions = Progressions.load(os.path.join(shared.path, "Public/Shared/Progressions/Progressions.lsx"),
                                       os.path.join(shared.path, "Public/SharedDev/Progressions/Progressions.lsx"))
sorcerer_progressions = Progressions()
sorcerer_nodes = []
for node in class_progressions.nodes.values():
    if (name := node.get("Name")) is not None and name.value in CharacterSubclasses.SORCERER:
        sorcerer_nodes.append(node)

sorcerer_nodes.sort(key=lambda node: (CharacterClass(node.get("Name").value).name, int(node.get("Level").value)))
for node in sorcerer_nodes:
    sorcerer_progressions.add(node)

xml = sorcerer_progressions.xml(version=(4, 1, 1, 1))
ElementTree.indent(xml, space=" "*4)
# ElementTree.dump(xml)


class Bob(LsxNode):
    Name = LsxType.LSSTRING_VALUE


class Alice(LsxNode):
    Name = LsxType.LSSTRING_VALUE
    Hobbies = LsxType.LSSTRING


class Mallory(LsxNode):
    Name = LsxType.LSSTRING_VALUE
    Hobbies = LsxType.LSSTRING


class MyClass(LsxNode):
    Name = LsxType.LSSTRING_VALUE
    UUID = LsxType.GUID
    Level = LsxType.UINT8
    Passives = LsxType.LSSTRING
    DisplayName = LsxType.TRANSLATEDSTRING
    PassiveList = LsxType.LSSTRING_COMMA
    Dummy = LsxType.UINT8
    children = (Bob, Alice)


my_obj_1 = MyClass(Level=42, Passives=["42", "84"], PassiveList="foo,bar,baz")
print(my_obj_1.__dict__)
my_obj_1.Name = "hello world"
my_obj_1.UUID = "hello!"
my_obj_1.Passives = "abc;def;ghi;"
print(my_obj_1.Passives)
my_obj_1.Passives = ["abc", "def", "ghi"]
print(my_obj_1.Passives)
my_obj_1.DisplayName = ("xxx", 42)
print("DisplayName =", my_obj_1.DisplayName)
my_obj_1.DisplayName = "yyy"
print("DisplayName =", my_obj_1.DisplayName)

my_obj_2 = MyClass()
print(my_obj_2.__dict__)
my_obj_2.UUID = "world"

a = my_obj_1.UUID
print(a)

print(my_obj_1.UUID)
print(my_obj_2.UUID)
# print(my_obj_2.Name)

print(my_obj_1.__dict__)
print(my_obj_2.__dict__)

b = my_obj_1.Level
print(b)

print(my_obj_1._allowed_child_types_)

bob = Bob(Name="Bob")
alice = Alice(Name="Alice", Hobbies="Reading;Gaming")
mallory = Mallory(Name="Mallory", Hobbies="Hacking;Phishing")

# my_obj_1.children = (bob, alice)

print(my_obj_1._attributes_)
print(my_obj_1)

# for child in my_obj_1.children:
#     print(child)

lsx_children = LsxChildren[LsxNode]([alice, bob], (Alice, Bob))
lsx_children[0] = alice
print(lsx_children)
print(lsx_children[0])
assert len(lsx_children) == 2
for child in lsx_children:
    print("Child =", child)
assert bob in lsx_children

try:
    lsx_children.append(mallory)
    assert False
except TypeError as e:
    print("Correctly received:", e)

children_copy = lsx_children.copy()
assert len(set(children_copy).difference(lsx_children)) == 0

children_copy.extend(lsx_children)
assert len(children_copy) == 2 * len(lsx_children)
print(children_copy)

print(children_copy + lsx_children)
children_copy += lsx_children
print(children_copy)

children_copy = children_copy.copy(predicate=lambda n: n.Name == "Bob")
assert len(children_copy) == 3
print(children_copy)

print(children_copy.find(lambda n: n.Name == "Mallory"))
print("Alice:", lsx_children.findall(lambda n: n.Name == "Alice"))
print("Mallory:", lsx_children.finditer(lambda n: n.Name == "Mallory"))

children_copy = lsx_children.copy() + lsx_children.copy()
children_copy.removeall(lambda n: n.Name == "Bob")
print(children_copy)

children_copy.update(lsx_children, key=lambda n: n.Name)
print("Update:", children_copy)

my_obj_1 = MyClass(Name="Bob Smith", Level=13, children=[alice, bob, bob, alice])
print("my_obj_1.children =", my_obj_1.children)
