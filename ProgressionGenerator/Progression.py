#!/usr/bin/env python3

import argparse
import os
import re
import sys

import xml.etree.ElementTree as ElementTree

from typing import AnyStr, Final, Pattern

parser = argparse.ArgumentParser(description='Combine the Progression.lsx tables, updating feat and resource definitions')
parser.add_argument("-f", "--feats", type=int, choices=range(1,5), default=4,
                    help="Feat progression every n levels")
parser.add_argument("-a", "--actions", type=int, choices=range(1,9), default=1,
                    help="Action resource multiplier")
args = parser.parse_args()

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

SCRIPTS_DIR: Final[str] = os.path.dirname(os.path.abspath(sys.argv[0]))
UNPACKED_MODS_DIR: Final[str] = os.path.normpath(os.path.join(SCRIPTS_DIR, "..", "..", "UnpackedMods"))

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

progressions_file = os.path.join(SCRIPTS_DIR, f"Progressions-F{args.feats}-A{args.actions}.lsx")
ElementTree.ElementTree(progressions).write(progressions_file, encoding="UTF-8", xml_declaration=True)