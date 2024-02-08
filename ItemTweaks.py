#!/usr/bin/env python3
"""
Generates files for the "ItemTweaks" mod.
"""

import os

from modtools.gamedata_v2 import Armor
from modtools.mod import Mod
from uuid import UUID

item_tweaks = Mod(os.path.dirname(__file__),
                  author="justin-elliott",
                  name="ItemTweaks",
                  mod_uuid=UUID("0e8ef3be-8daa-4c7f-a41d-3a72ae00c33d"),
                  description="Tweaks various game items.")

# The Smuggler's Ring now provides advantage on dexterity checks, and boosts all dexterity-based skills.
item_tweaks.add(Armor(
    "PLA_SmugglerRing",
    using="PLA_SmugglerRing",
    Boosts=[
        "Skill(Acrobatics,2)"
        "Skill(SleightOfHand,2)",
        "Skill(Stealth,2)",
        "Advantage(Ability,Dexterity)",
    ],
))

item_tweaks.build()
