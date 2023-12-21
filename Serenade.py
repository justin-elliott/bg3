#!/usr/bin/env python3
"""
Generates files for the "Serenade" mod.
"""

import os
from uuid import UUID

from modtools.localization import Localization

loca = Localization(UUID("a1c3d65c-3c00-4c7e-8aab-3ef7dd1593f1"))
loca.add_language("en", "English")

loca["Serenade_DisplayName"] = {"en": "Serenade"}
loca["Serenade_Description"] = {"en": """
    Curved wood and strings of gold,
    a treasure to behold.
    Fingertips on frets alight,
    awaken day or starry night.
    Sweet notes dance and gracefully soar,
    through halls and chambers, evermore.
    A tapestry of sound so fine,
    the lute's melody, truly divine.
    """}

loca["Virtuoso_DisplayName"] = {"en": "Virtuoso"}
loca["Virtuoso_Description"] = {"en": """
    You gain <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all
    <LSTag Tooltip="Charisma">Charisma</LSTag> Skills, and have
    <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in, and
    <LSTag Tooltip="Advantage">Advantage</LSTag> on, Charisma <LSTag Tooltip="AbilityCheck">Checks</LSTag>.
    """}

loca["Medley_DisplayName"] = {"en": "Medley"}
loca["Medley_Description"] = {"en": "Perform a medley of songs to inspire and fortify your allies."}
loca["Medley_Boost_Description"] = {"en": """
    Hit point maximum increased by [1].

    Each turn, restore [2].

    When you roll a 1 on an <LSTag Tooltip="AttackRoll">Attack Roll</LSTag>,
    <LSTag Tooltip="AbilityCheck">Ability Check</LSTag>, or
    <LSTag Tooltip="SavingThrow">Saving Throw</LSTag>,
    you can reroll the die and must use the new roll.

    You can see in the dark up to [3].
    """}


serenade_dir = os.path.join(os.path.dirname(__file__), "Serenade")
os.makedirs(serenade_dir, exist_ok=True)
loca.build(serenade_dir)
