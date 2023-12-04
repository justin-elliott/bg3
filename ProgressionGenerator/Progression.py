#!/usr/bin/env python3

import argparse
import os
import re
import sys
import uuid

import xml.etree.ElementTree as ElementTree

from typing import AnyStr, Final, NamedTuple, Pattern

CLASS_NAMES: Final[set[str]] = {
    "Barbarian",
    "Bard",
    "Cleric",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard",
}

def class_list(s: str) -> set[str]:
    classes = set([t.title() for t in s.split(",")])
    if classes & CLASS_NAMES != classes or len(classes) == 0:
        raise "Invalid class names"
    return classes

parser = argparse.ArgumentParser(description='Combine the Progression.lsx tables, updating feat and resource definitions')
parser.add_argument("-c", "--classes", type=class_list, default=CLASS_NAMES,
                    help="Classes to include in the progression (defaulting to all)")
parser.add_argument("-f", "--feats", type=int, choices=range(1,5), default=4,
                    help="Feat progression every n levels (defaulting to 4; normal progression)")
parser.add_argument("-s", "--spells", type=int, choices=range(1,9), default=1,
                    help="Spell slot multiplier (defaulting to 1; normal spell slots)")
parser.add_argument("-a", "--actions", type=int, choices=range(1,9), default=1,
                    help="Action resource multiplier (defaulting to 1; normal resources)")
args = parser.parse_args()

SCRIPTS_DIR: Final[str] = os.path.dirname(os.path.abspath(sys.argv[0]))
PARENT_DIR: Final[str] = os.path.normpath(os.path.join(SCRIPTS_DIR, ".."))
UNPACKED_MODS_DIR: Final[str] = os.path.normpath(os.path.join(PARENT_DIR, "..", "UnpackedMods"))

SPELL_SLOTS: Final[list[str]] = [
    "SpellSlot",
    "WarlockSpellSlot",
]
ACTION_RESOURCES: Final[list[str]] = [
    "ArcaneRecoveryPoint",
    "BardicInspiration",
    "ChannelDivinity",
    "ChannelOath",
    "FungalInfestationCharge",
    "KiPoint",
    "LayOnHandsCharge",
    "NaturalRecoveryPoint",
    "Rage",
    "SorceryPoint",
    "SuperiorityDie",
    "WarPriestActionPoint",
    "WildShape",
]
SPELL_SLOT_REGEX: Final[Pattern[AnyStr]] = re.compile(f"ActionResource\\(({"|".join(SPELL_SLOTS)}),\\s*(\\d+),\\s*(\\d+)\\)")
ACTION_RESOURCE_REGEX: Final[Pattern[AnyStr]] = re.compile(f"ActionResource\\(({"|".join(ACTION_RESOURCES)}),\\s*(\\d+),\\s*(\\d+)\\)")

UuidToClassDict = dict[str, str]
SubclassToClassDict = dict[str, str]

class ProgressionsKey(NamedTuple):
    class_name: str
    subclass_name: str
    level: int
    uuid: str

ProgressionsDict = dict[ProgressionsKey, ElementTree.Element]

def collect_uuid_to_class(class_descriptions: ElementTree) -> UuidToClassDict:
    uuid_to_class: UuidToClassDict = {}
    for node in class_descriptions.findall("./region[@id='ClassDescriptions']/node[@id='root']/children/node[@id='ClassDescription']"):
        uuid_node = node.find("attribute[@id='UUID']")
        name_node = node.find("attribute[@id='Name']")
        if uuid_node != None and name_node != None:
            uuid = uuid_node.get("value")
            name = name_node.get("value")
            if uuid != None and name != None:
                uuid_to_class[uuid] = name
    return uuid_to_class

def collect_subclass_to_class(progressions: ElementTree, uuid_to_class: UuidToClassDict) -> SubclassToClassDict:
    subclass_to_class: SubclassToClassDict = dict()
    for node in progressions.findall("./region[@id='Progressions']/node[@id='root']/children/node[@id='Progression']"):
        name_node = node.find("attribute[@id='Name']")
        children_node = node.find("children")
        if name_node != None and children_node != None:
            name = name_node.get("value")
            if name in args.classes:
                subclass_nodes = children_node.findall("node[@id='SubClasses']/children/node[@id='SubClass']")
                for subclass_node in subclass_nodes:
                    class_description_node = subclass_node.find("attribute[@id='Object']")
                    if class_description_node != None:
                        uuid = class_description_node.get("value")
                        if uuid in uuid_to_class:
                            subclass_to_class[uuid_to_class[uuid]] = name
    return subclass_to_class

def collect_progressions(progressions: ElementTree, subclass_to_class: SubclassToClassDict) -> ProgressionsDict:
    nodes: ProgressionsDict = {}
    for node in progressions.findall("./region[@id='Progressions']/node[@id='root']/children/node[@id='Progression']"):
        name_node = node.find("attribute[@id='Name']")
        level_node = node.find("attribute[@id='Level']")
        uuid_node = node.find("attribute[@id='UUID']")
        if name_node != None and level_node != None and uuid_node != None:
            name = name_node.get("value")
            level = level_node.get("value")
            uuid = uuid_node.get("value")
            if level != None and uuid != None:
                if name in args.classes:
                    nodes[(name, "", int(level), uuid)] = node
                elif name in subclass_to_class:
                    nodes[(subclass_to_class[name], name, int(level), uuid)] = node
    return nodes

def feat_every_n_levels(progressions: ProgressionsDict, n_levels: int):
    for (_, _, level, _), node in progressions.items():
        if (allow_improvement_node := node.find("attribute[@id='AllowImprovement']")) != None:
            node.remove(allow_improvement_node)
        if level > 1 and level % n_levels == 0:
            ElementTree.SubElement(node, "attribute", attrib={"id": "AllowImprovement", "type": "bool", "value": "true"})

def resources_multiplier(progressions: ProgressionsDict, resources_regex: Pattern[AnyStr], multiplier: int):
    for node in progressions.values():
        boosts_node = node.find("attribute[@id='Boosts']")
        if boosts_node != None:
            boosts = boosts_node.get("value")
            if boosts != None:
                boosts = resources_regex.sub(lambda match: f"ActionResource({match[1]},{int(match[2])*multiplier},{match[3]})", boosts)
                boosts_node.set("value", boosts)

def sort_node_attributes(progressions: ProgressionsDict):
    for node in progressions.values():
        attributes = node.findall("attribute[@id]")
        sorted_attributes = sorted([(attribute.get("id"), attribute) for attribute in attributes])
        for attribute in attributes:
            node.remove(attribute)
        for attribute in sorted_attributes:
            node.append(attribute[1])
        children = node.find("children")
        if children != None:
            node.remove(children)
            node.append(children) # Move to back

shared_class_descriptions_file: Final[str] = os.path.join(UNPACKED_MODS_DIR, "Shared", "Public", "Shared", "ClassDescriptions", "ClassDescriptions.lsx")
shareddev_class_descriptions_file: Final[str] = os.path.join(UNPACKED_MODS_DIR, "Shared", "Public", "SharedDev", "ClassDescriptions", "ClassDescriptions.lsx")

shared_class_descriptions = ElementTree.parse(shared_class_descriptions_file)
shareddev_class_descriptions = ElementTree.parse(shareddev_class_descriptions_file)

uuid_to_class = collect_uuid_to_class(shared_class_descriptions) | collect_uuid_to_class(shareddev_class_descriptions)

shared_progressions_file: Final[str] = os.path.join(UNPACKED_MODS_DIR, "Shared", "Public", "Shared", "Progressions", "Progressions.lsx")
shareddev_progressions_file: Final[str] = os.path.join(UNPACKED_MODS_DIR, "Shared", "Public", "SharedDev", "Progressions", "Progressions.lsx")

shared_progressions = ElementTree.parse(shared_progressions_file)
shareddev_progressions = ElementTree.parse(shareddev_progressions_file)

subclass_to_class = collect_subclass_to_class(shared_progressions, uuid_to_class) | collect_subclass_to_class(shareddev_progressions, uuid_to_class)

combined_progressions = collect_progressions(shared_progressions, subclass_to_class) | collect_progressions(shareddev_progressions, subclass_to_class)

# Remove the unused (and unusual) Cleric progression entry
UNUSED_CLERIC_KEY: Final[ProgressionsKey] = ("Cleric", "", 1, "2b249feb-bba5-4922-8385-c2dd9baaa049")
combined_progressions.pop(UNUSED_CLERIC_KEY, None)

# Remove the erroneous Ranger level 12 spell slot
if "Ranger" in args.classes:
    RANGER_LEVEL_12_KEY: Final[ProgressionsKey] = ("Ranger", "", 12, "0bf247c5-2217-409e-8f88-eee095448f32")
    ranger_level_12_node = combined_progressions[RANGER_LEVEL_12_KEY]
    ranger_level_12_boosts_node = ranger_level_12_node.find("attribute[@id='Boosts'][@value='ActionResource(SpellSlot,1,3)']")
    if ranger_level_12_boosts_node != None:
        ranger_level_12_node.remove(ranger_level_12_boosts_node)

feat_every_n_levels(combined_progressions, args.feats)
resources_multiplier(combined_progressions, SPELL_SLOT_REGEX, args.spells)
resources_multiplier(combined_progressions, ACTION_RESOURCE_REGEX, args.actions)

sort_node_attributes(combined_progressions)

if (args.classes == CLASS_NAMES):
    progressions_name = f"Progressions-All-F{args.feats}-S{args.spells}-A{args.actions}"
else:
    progressions_name = f"Progressions-{"-".join(sorted([c for c in args.classes]))}-F{args.feats}-S{args.spells}-A{args.actions}"

mod_base_dir = os.path.join(PARENT_DIR, progressions_name)
mod_meta_dir = os.path.join(mod_base_dir, "Mods", progressions_name)
mod_progressions_dir = os.path.join(mod_base_dir, "Public", progressions_name, "Progressions")

os.makedirs(mod_meta_dir, exist_ok=True)
os.makedirs(mod_progressions_dir, exist_ok=True)

meta_xml = ElementTree.fromstring(f"""\
<?xml version="1.0" encoding="UTF-8"?>
<save>
    <version major="4" minor="1" revision="1" build="0"/>
    <region id="Config">
        <node id="root">
            <children>
                <node id="Dependencies"/>
                <node id="ModuleInfo">
                    <attribute id="Author" type="LSWString" value="BinaryPrimitive"/>
                    <attribute id="CharacterCreationLevelName" type="FixedString" value=""/>
                    <attribute id="Description" type="LSWString" value="Updated character progressions"/>
                    <attribute id="Folder" type="LSWString" value="{progressions_name}"/>
                    <attribute id="LobbyLevelName" type="FixedString" value=""/>
                    <attribute id="MD5" type="LSString" value=""/>
                    <attribute id="MainMenuBackgroundVideo" type="FixedString" value=""/>
                    <attribute id="MenuLevelName" type="FixedString" value=""/>
                    <attribute id="Name" type="FixedString" value="{progressions_name}"/>
                    <attribute id="NumPlayers" type="uint8" value="4"/>
                    <attribute id="PhotoBooth" type="FixedString" value=""/>
                    <attribute id="StartupLevelName" type="FixedString" value=""/>
                    <attribute id="Tags" type="LSString" value=""/>
                    <attribute id="Type" type="FixedString" value="Add-on"/>
                    <attribute id="UUID" type="FixedString" value="{str(uuid.uuid4())}"/>
                    <attribute id="Version" type="int32" value="1"/>
                    <children>
                        <node id="PublishVersion">
                            <attribute id="Version" type="int32" value="1"/>
                        </node>
                        <node id="Scripts"/>
                        <node id="TargetModes">
                            <children>
                                <node id="Target">
                                    <attribute id="Object" type="FixedString" value="Story"/>
                                </node>
                            </children>
                        </node>
                    </children>
                </node>
            </children>
        </node>
    </region>
</save>
""")
meta_file = os.path.join(mod_meta_dir, "meta.lsx")
ElementTree.ElementTree(meta_xml).write(meta_file, encoding="UTF-8", xml_declaration=True)

progressions = ElementTree.fromstring("""\
<?xml version="1.0" encoding="UTF-8"?>
<save>
    <version major="4" minor="1" revision="1" build="0"/>
    <region id="Progressions">
        <node id="root">
            <children>
            </children>
        </node>
    </region>
</save>
""")
progressions.find("./region[@id='Progressions']/node[@id='root']/children").extend(
    [combined_progressions[key] for key in sorted(combined_progressions.keys())])
ElementTree.indent(progressions, space=" "*4)

progressions_file = os.path.join(mod_progressions_dir, "Progressions.lsx")
ElementTree.ElementTree(progressions).write(progressions_file, encoding="UTF-8", xml_declaration=True)