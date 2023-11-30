#!/usr/bin/env python3

import argparse
import os
import re
import sys
import uuid

import xml.etree.ElementTree as ElementTree

from typing import AnyStr, Final, Pattern

parser = argparse.ArgumentParser(description='Combine the Progression.lsx tables, updating feat and resource definitions')
parser.add_argument("-f", "--feats", type=int, choices=range(1,5), default=4,
                    help="Feat progression every n levels")
parser.add_argument("-a", "--actions", type=int, choices=range(1,9), default=1,
                    help="Action resource multiplier")
args = parser.parse_args()

SCRIPTS_DIR: Final[str] = os.path.dirname(os.path.abspath(sys.argv[0]))
PARENT_DIR: Final[str] = os.path.normpath(os.path.join(SCRIPTS_DIR, ".."))
UNPACKED_MODS_DIR: Final[str] = os.path.normpath(os.path.join(PARENT_DIR, "..", "UnpackedMods"))

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

ACTION_RESOURCES: Final[list[str]] = [
    "ArcaneRecoveryPoint",
    "BardicInspiration",
    "ChannelDivinity",
    "ChannelOath",
    "KiPoint",
    "LayOnHandsCharge",
    "Rage",
    "SorceryPoint",
    "SpellSlot",
    "WarlockSpellSlot",
]
SPELL_SLOT_REGEX: Final[Pattern[AnyStr]] = re.compile(f"ActionResource\\(({"|".join(ACTION_RESOURCES)}),\\s*(\\d+),\\s*(\\d+)\\)")

def collect_nodes(root: ElementTree) -> dict[tuple[str, int, str], ElementTree.Element]:
    nodes: dict[tuple[str, int, bool], ElementTree.Element] = {}
    for node in root.findall("./region[@id='Progressions']/node[@id='root']/children/node[@id='Progression']"):
        name_node = node.find("attribute[@id='Name']")
        level_node = node.find("attribute[@id='Level']")
        uuid_node = node.find("attribute[@id='UUID']")
        if name_node != None and level_node != None and uuid_node != None:
            name = name_node.get("value")
            level = level_node.get("value")
            uuid = uuid_node.get("value")
            if name in CLASS_NAMES and level != None and uuid != None:
                nodes[(name, int(level), uuid)] = node
    return nodes

def feat_every_n_levels(nodes: dict[tuple[str, int, str], ElementTree.Element], n_levels: int):
    for (_, level, _), node in nodes.items():
        allow_improvement_node = node.find("attribute[@id='AllowImprovement']")
        allow_improvement = (level > 1 and level % n_levels == 0) if allow_improvement_node == None else (
            allow_improvement_node.get("value").lower() == "true")
        if allow_improvement_node != None:
            node.remove(allow_improvement_node)
        if allow_improvement:
            ElementTree.SubElement(node, "attribute", attrib={"id": "AllowImprovement", "type": "bool", "value": "true"})

def action_resources_multiplier(nodes: dict[tuple[str, int, str], ElementTree.Element], multiplier: int):
    for node in nodes.values():
        boosts_node = node.find("attribute[@id='Boosts']")
        if boosts_node != None:
            boosts = boosts_node.get("value")
            if boosts != None:
                boosts = SPELL_SLOT_REGEX.sub(lambda match: f"ActionResource({match[1]},{int(match[2])*multiplier},{match[3]})", boosts)
                boosts_node.set("value", boosts)

def sort_node_attributes(nodes: dict[tuple[str, int, str], ElementTree.Element]):
    for node in nodes.values():
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

shared_progressions_file: Final[str] = os.path.join(UNPACKED_MODS_DIR, "Shared", "Public", "Shared", "Progressions", "Progressions.lsx")
shareddev_progressions_file: Final[str] = os.path.join(UNPACKED_MODS_DIR, "Shared", "Public", "SharedDev", "Progressions", "Progressions.lsx")

shared_progressions = ElementTree.parse(shared_progressions_file)
shareddev_progressions = ElementTree.parse(shareddev_progressions_file)

combined_nodes = collect_nodes(shared_progressions) | collect_nodes(shareddev_progressions)

# Remove the unused (and unusual) Cleric progression entry
UNUSED_CLERIC_KEY: Final[tuple[str, int, str]] = ("Cleric", 1, "2b249feb-bba5-4922-8385-c2dd9baaa049")
combined_nodes.pop(UNUSED_CLERIC_KEY, None)

feat_every_n_levels(combined_nodes, args.feats)
action_resources_multiplier(combined_nodes, args.actions)

sort_node_attributes(combined_nodes)

progressions_name = f"Progressions-F{args.feats}-A{args.actions}"

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
    [combined_nodes[key] for key in sorted(combined_nodes.keys())])
ElementTree.indent(progressions, space=" "*4)

progressions_file = os.path.join(mod_progressions_dir, "Progressions.lsx")
ElementTree.ElementTree(progressions).write(progressions_file, encoding="UTF-8", xml_declaration=True)