#!/usr/bin/env python3
"""
Generates files for the "ChromaticBlade" mod.
"""

import os

from modtools.lsx.progressions import (
    Progression,
    Progressions,
    PROGRESSIONS_LSX_PATH,
    PROGRESSIONS_DEV_LSX_PATH
)
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

progressions_lsx = Progressions.load(sorcerer_battlemage.get_pak_path("Shared", PROGRESSIONS_LSX_PATH),
                                     sorcerer_battlemage.get_pak_path("Shared", PROGRESSIONS_DEV_LSX_PATH))

sorcerer_battlemage.build()
