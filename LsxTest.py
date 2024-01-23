#!/usr/bin/env python3
"""
Test code for modtools.lsx_v2.
"""

from abc import abstractmethod
import os
from typing import Callable
import xml.etree.ElementTree as ElementTree

from modtools.lsx.characterclasses import CharacterClass, CharacterSubclasses
from modtools.lsx.progressions import (
    Progression,
    Progressions,
    ProgressionSubclass,
    ProgressionSubclasses
)
from modtools.lsx.types import DataType
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


class LsxAttribute:
    _type_name: str

    def __init__(self, type_name: str):
        self._type_name = type_name

    @abstractmethod
    def wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                   Callable[[object, any], None],
                                                   Callable[[object], None]]:
        """Returns the get, set, and del accessors for the LsxAttribute."""
        pass


class LsxString(LsxAttribute):
    def __init__(self, type_name: str):
        super().__init__(type_name)

    def wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                   Callable[[object, any], None],
                                                   Callable[[object], None]]:
        def getter(obj: object) -> str:
            store: dict = obj.__dict__.setdefault(member, {})
            return store.get("str")

        def setter(obj: object, value: str) -> None:
            store: dict = obj.__dict__.setdefault(member, {})
            store["str"] = str(value)

        def deleter(obj: object) -> None:
            store: dict = obj.__dict__.setdefault(member, {})
            if "str" in store:
                del store["str"]

        return (getter, setter, deleter)


class LsxList(LsxAttribute):
    LIST_TYPES = (list, tuple, set)

    _separator: str

    def __init__(self, type_name: str, separator: str = ";"):
        super().__init__(type_name)
        self._separator = separator

    def wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                   Callable[[object, any], None],
                                                   Callable[[object], None]]:
        def getter(obj: object) -> list[str]:
            store: dict = obj.__dict__.setdefault(member, {})
            return store.get("list")

        def setter(obj: object, values: list[str]) -> None:
            if not isinstance(values, LsxList.LIST_TYPES):
                values = [x for x in str(values).split(self._separator) if x]
            else:
                values = [str(x) for x in values]
            store: dict = obj.__dict__.setdefault(member, {})
            store["list"] = values

        def deleter(obj: object) -> None:
            store: dict = obj.__dict__.setdefault(member, {})
            if "list" in store:
                del store["list"]

        return (getter, setter, deleter)


class LsxTranslation(LsxAttribute):
    def __init__(self, type_name: str):
        super().__init__(type_name)

    def wrap_accessors(self, member: str) -> tuple[Callable[[object], any],
                                                   Callable[[object, any], None],
                                                   Callable[[object], None]]:
        def getter(obj: object) -> tuple[str, int]:
            store: dict = obj.__dict__.setdefault(member, {})
            return (store.get("handle"), store.get("version"))

        def setter(obj: object, value: str | tuple[str, int]) -> None:
            store: dict = obj.__dict__.setdefault(member, {})
            if not isinstance(value, tuple):
                value = (value, 1)
            handle, version = value
            store["handle"] = str(handle)
            store["version"] = int(version)

        def deleter(obj: object) -> None:
            store: dict = obj.__dict__.setdefault(member, {})
            if "handle" in store:
                del store["handle"]
                del store["version"]

        return (getter, setter, deleter)


class LsxType:
    LSString = LsxList("LSString")
    LSStringComma = LsxList("LSString", ",")
    LSStringValue = LsxString("LSString")
    GUID = LsxString("guid")
    TranslatedString = LsxTranslation("TranslatedString")
    uint8 = LsxString("uint8")


class LsxNode:
    _attributes_: dict[str, LsxAttribute]

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._attributes_ = {}
        for member_name, data_type in list(cls.__dict__.items()):
            if isinstance(data_type, LsxAttribute):
                cls._attributes_[member_name] = data_type

        for member_name, data_type in cls._attributes_.items():
            getter, setter, deleter = data_type.wrap_accessors("_" + member_name)
            prop = property(fget=getter, fset=setter, fdel=deleter)
            setattr(cls, member_name, prop)

    def __init__(self, **kwds):
        for name, value in kwds.items():
            if name not in self._attributes_:
                raise AttributeError(f"{self.__class__.__name__}.{name} is not defined", obj=self, name=name)
            setattr(self, name, value)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({", ".join(
            f"{name}={repr(getattr(self, name))}" for name in sorted(self._attributes_.keys())
            if getattr(self, name) is not None
            )})"


class MyClass(LsxNode):
    Name = LsxType.LSStringValue
    UUID = LsxType.GUID
    Level = LsxType.uint8
    Passives = LsxType.LSString
    DisplayName = LsxType.TranslatedString
    PassiveList = LsxType.LSStringComma
    Dummy = LsxType.uint8


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
print(my_obj_1._attributes_)
print(my_obj_1)
