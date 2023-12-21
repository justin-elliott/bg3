#!/usr/bin/env python3
"""
Generates files for the "Serenade" mod.
"""

import os

from modtools.localization import Localization

localization = Localization()
en = localization.language("English")

en["Serenade_DisplayName"] = "Serenade"
en["Serenade_Description"] = """
    Curved wood and strings of gold,
    a treasure to behold.
    Fingertips on frets alight,
    awaken day or starry night.
    Sweet notes dance and gracefully soar,
    through halls and chambers, evermore.
    A tapestry of sound so fine,
    the lute's melody, truly divine.
    """

en["Serenade_Virtuoso_DisplayName"] = "Virtuoso"
en["Serenade_Virtuoso_Description"] = """
    You gain <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all
    <LSTag Tooltip="Charisma">Charisma</LSTag> Skills, and have
    <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in, and
    <LSTag Tooltip="Advantage">Advantage</LSTag> on, Charisma <LSTag Tooltip="AbilityCheck">Checks</LSTag>.
    """

en["Serenade_Medley_DisplayName"] = "Medley"
en["Serenade_Medley_Description"] = "Perform a medley of songs to inspire and fortify your allies."
en["Serenade_MedleyBoost_Description"] = """
    Hit point maximum increased by [1].

    Each turn, restore [2].

    When you roll a 1 on an <LSTag Tooltip="AttackRoll">Attack Roll</LSTag>,
    <LSTag Tooltip="AbilityCheck">Ability Check</LSTag>, or
    <LSTag Tooltip="SavingThrow">Saving Throw</LSTag>,
    you can reroll the die and must use the new roll.

    You can see in the dark up to [3].
    """


serenade_dir = os.path.join(os.path.dirname(__file__), "Serenade")
os.makedirs(serenade_dir, exist_ok=True)
localization.write(serenade_dir)
