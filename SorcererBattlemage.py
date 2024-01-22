#!/usr/bin/env python3
"""
Generates files for the "ChromaticBlade" mod.
"""

import os

from modtools.lsx.actionresources import ActionResource, update_action_resources
from modtools.lsx.characterclasses import CharacterSubclasses
from modtools.lsx.progressions import (
    ProgressionKey,
    Progressions,
    PROGRESSIONS_LSX_PATH,
    PROGRESSIONS_DEV_LSX_PATH
)
from modtools.lsx.types import Node
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

loca = sorcerer_battlemage.get_localization()

progressions_lsx = Progressions.load(sorcerer_battlemage.get_cache_path(PROGRESSIONS_LSX_PATH),
                                     sorcerer_battlemage.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))

sorcerer_progression: dict[(str, int, bool), Node] = {
    ProgressionKey.for_node(node): node
    for node in progressions_lsx.filter(lambda node: node["Name"].value in CharacterSubclasses.SORCERER)
}

for _, node in sorted(sorcerer_progression.items()):
    if (boosts := node.get("Boosts")) is not None:
        boosts.value = update_action_resources(boosts.value,
                                               [ActionResource.SPELL_SLOTS, ActionResource.SORCERY_POINTS],
                                               lambda _resource, count, _level: count * 2)
    sorcerer_battlemage.add(node)

sorcerer_battlemage.build()
