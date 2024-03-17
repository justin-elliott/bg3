#!/usr/bin/env python3
"""
Generates files for the "ItemTweaks" mod.
"""

import os

from modtools.gamedata import Armor, PassiveData
from modtools.mod import Mod
from uuid import UUID

item_tweaks = Mod(os.path.dirname(__file__),
                  author="justin-elliott",
                  name="ItemTweaks",
                  mod_uuid=UUID("0e8ef3be-8daa-4c7f-a41d-3a72ae00c33d"),
                  description="Tweaks various game items.")

loca = item_tweaks.get_localization()

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

# The Gloves of Power no longer depend on bearing the Absolute's Mark.
item_tweaks.add(Armor(
    "DEN_RaidingParty_GoblinCaptain_Gloves",
    using="DEN_RaidingParty_GoblinCaptain_Gloves",
    Boosts=["Skill(SleightOfHand,2)"],
))

loca["DEN_RaidingParty_GoblinCaptain_Gloves_Passive_Description"] = {"en": """
    When making an attack, possibly inflict a [1] penalty to the target's
    <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag> and <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>.
    """}

item_tweaks.add(PassiveData(
    "DEN_RaidingParty_GoblinCaptain_Gloves_Passive",
    using="DEN_RaidingParty_GoblinCaptain_Gloves_Passive",
    Description=loca["DEN_RaidingParty_GoblinCaptain_Gloves_Passive_Description"],
    Conditions="IsAttack() and Character() and not Item()",
    StatsFunctors=["ApplyStatus(BANE,100,2,,,,not SavingThrow(Ability.Charisma,11))"],
))

# The Luminous Armour combines the effects of the Armour of Agility
item_tweaks.add(Armor(
    "MAG_Radiant_RadiatingOrb_Armor",
    using="MAG_Radiant_RadiatingOrb_Armor",
    Rarity="VeryRare",
    Boosts=["RollBonus(SavingThrow, 2)"],
    PassivesOnEquip=["MAG_ExoticMaterial_MediumArmor_Passive"],
    StatusOnEquip=["MAG_EXOTIC_MATERIAL_ARMOR_TECHNICAL"],
    Ability_Modifier_Cap="",
))

item_tweaks.build()
