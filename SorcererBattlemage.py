#!/usr/bin/env python3
"""
Generates files for the "ChromaticBlade" mod.
"""

import os

from moddb.battlemagic import BattleMagic
from moddb.bolster import Bolster
from modtools.lsx.actionresources import ActionResource, update_action_resources
from modtools.lsx.characterclasses import CharacterClass, CharacterSubclasses
from modtools.lsx import Lsx
from modtools.lsx.game.progressions import Progressions
from modtools.lsx.game.spelllists import SpellList
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",

PROGRESSIONS_LSX_PATH = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
PROGRESSIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"

sorcerer_battlemage = Mod(os.path.dirname(__file__),
                          author="justin-elliott",
                          name="SorcererBattlemage",
                          mod_uuid=UUID("aa8aa79d-c67e-4fd8-98f7-392f549abf7e"),
                          description="Upgrades the Sorcerer class to a Battlemage.")

# Add passives and spells
battle_magic = BattleMagic(sorcerer_battlemage).add_battle_magic()
bolster = Bolster(sorcerer_battlemage).add_bolster()

# Load the game's Sorcerer progression, creating a dictionary indexed by (Name, Level, IsMulticlass)
progressions_lsx = Lsx.load(sorcerer_battlemage.get_cache_path(PROGRESSIONS_LSX_PATH))
progressions_dev_lsx = Lsx.load(sorcerer_battlemage.get_cache_path(PROGRESSIONS_DEV_LSX_PATH))
progressions_lsx.children.update(progressions_dev_lsx.children, key=lambda child: child.UUID)

sorcerer_progression = progressions_lsx.children.keepall(lambda child: child.Name in CharacterSubclasses.SORCERER)
sorcerer_progression.sort(key=lambda child: (CharacterClass(child.Name).name, child.Level, child.IsMulticlass or False))

# level_1_spelllist = str(sorcerer_battlemage.make_uuid("level_1_spelllist"))
# sorcerer_battlemage.add(SpellList(
#     Comment="Sorcerer Battlemage level 1 spells",
#     Spells=[bolster, "Target_CreateDestroyWater", "Projectile_EldritchBlast", "Target_Guidance"],
#     UUID=level_1_spelllist,
# ))

# level_2_spelllist = str(sorcerer_battlemage.make_uuid("level_2_spelllist"))
# sorcerer_battlemage.add(SpellList(
#     Comment="Sorcerer Battlemage level 2 spells",
#     Spells=["Target_EnhanceAbility"],
#     UUID=level_2_spelllist,
# ))


# def level_1():
#     """Add armor and weapon proficiencies, passives, skills, and spells."""
#     for is_multiclass in [False, True]:
#         node = sorcerer_progression[(CharacterClass.SORCERER.name, 1, is_multiclass)]

#         boosts = node["Boosts"].value if "Boosts" in node else []
#         boosts = [boost for boost in boosts if boost not in ["Proficiency(Daggers)",
#                                                              "Proficiency(Quarterstaffs)",
#                                                              "Proficiency(LightCrossbows)"]]
#         boosts.extend([
#             "Proficiency(LightArmor)",
#             "Proficiency(MediumArmor)",
#             "Proficiency(HeavyArmor)",
#             "Proficiency(Shields)",
#             "Proficiency(SimpleWeapons)",
#             "Proficiency(MartialWeapons)",
#         ])
#         node.set_value("Boosts", boosts)

#         passives_added = node["PassivesAdded"].value if "PassivesAdded" in node else []
#         passives_added.extend([battle_magic, "SculptSpells"])
#         node.set_value("PassivesAdded", passives_added)

#         selectors = node["Selectors"].value if "Selectors" in node else []
#         selectors.append(f"AddSpells({level_1_spelllist},,,,AlwaysPrepared)")
#         node.set_value("Selectors", selectors)

#     # Progression when Sorcerer is the class selected at level one
#     node = sorcerer_progression[(CharacterClass.SORCERER.name, 1, False)]

#     selectors = node["Selectors"].value if "Selectors" in node else []
#     selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
#     selectors.extend([
#         "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
#         "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
#     ])
#     node.set_value("Selectors", selectors)


# level_1()

for child in sorcerer_progression:
    if (boosts := child.Boosts) is not None:
        child.Boosts = update_action_resources(boosts,
                                               [ActionResource.SPELL_SLOTS, ActionResource.SORCERY_POINTS],
                                               lambda _resource, count, _level: count * 2)
    sorcerer_battlemage.add(child)

sorcerer_battlemage.build()
