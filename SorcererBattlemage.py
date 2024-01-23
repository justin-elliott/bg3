#!/usr/bin/env python3
"""
Generates files for the "ChromaticBlade" mod.
"""

import os

from moddb.battlemagic import BattleMagic
from modtools.lsx.actionresources import ActionResource, update_action_resources
from modtools.lsx.characterclasses import CharacterClass, CharacterSubclasses
from modtools.lsx.progressions import (
    Progressions,
    PROGRESSIONS_LSX_PATH,
    PROGRESSIONS_DEV_LSX_PATH
)
from modtools.lsx.types import Attribute, DataType, Node
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",


sorcerer_battlemage = Mod(os.path.dirname(__file__),
                          author="justin-elliott",
                          name="SorcererBattlemage",
                          mod_uuid=UUID("aa8aa79d-c67e-4fd8-98f7-392f549abf7e"),
                          description="Upgrades the Sorcerer class to a Battlemage.")

battle_magic = BattleMagic(sorcerer_battlemage).add_battle_magic()

loca = sorcerer_battlemage.get_localization()

# Load the game's Sorcerer progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Progressions.load(sorcerer_battlemage.get_cache_path(PROGRESSIONS_LSX_PATH),
                                     sorcerer_battlemage.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
sorcerer_progression: dict[(str, int, bool), Node] = {
    (CharacterClass(node["Name"].value).name,
     int(node["Level"].value),
     node["IsMulticlass"].value.lower() == "true" if "IsMulticlass" in node else False): node
    for node in progressions_lsx.filter(lambda node: node["Name"].value in CharacterSubclasses.SORCERER)
}


def level_1():
    """Add armor and weapon proficiencies, passives, skills, and spells."""
    for is_multiclass in [False, True]:
        node = sorcerer_progression[(CharacterClass.SORCERER.name, 1, is_multiclass)]

        boosts = node.get("Boosts", Attribute(DataType.LSSTRING, [])).value
        boosts = [boost for boost in boosts if boost not in ["Proficiency(Daggers)",
                                                             "Proficiency(Quarterstaffs)",
                                                             "Proficiency(LightCrossbows)"]]
        boosts.extend([
            "Proficiency(LightArmor)",
            "Proficiency(MediumArmor)",
            "Proficiency(HeavyArmor)",
            "Proficiency(Shields)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
        ])
        node.set_value("Boosts", boosts)

        passives_added = node["PassivesAdded"].value if "PassivesAdded" in node else []
        passives_added.extend([battle_magic, "SculptSpells"])
        node.set_value("PassivesAdded", passives_added)


level_1()

for _, node in sorted(sorcerer_progression.items()):
    if (boosts := node.get("Boosts")) is not None:
        boosts.value = update_action_resources(boosts.value,
                                               [ActionResource.SPELL_SLOTS, ActionResource.SORCERY_POINTS],
                                               lambda _resource, count, _level: count * 2)
    sorcerer_battlemage.add(node)

sorcerer_battlemage.build()
