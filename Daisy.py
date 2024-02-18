#!/usr/bin/env python3
"""
Generates files for the "Daisy" mod.
"""

import os

from modtools.gamedata import Armor
from modtools.mod import Mod
from modtools.text import TreasureTable
from uuid import UUID

daisy = Mod(os.path.dirname(__file__),
            author="justin-elliott",
            name="Daisy",
            mod_uuid=UUID("fc71b9c6-905c-40fe-8c16-5ad8345dfaa4"),
            description="Adds the Guardian armor to the tutorial chest.")

daisy.add(Armor(
    "Daisy_Clothing_Armor",
    using="ARM_Robe_Body",
    Rarity="Legendary",
    RootTemplate="aa0917ea-5f66-4a22-97de-654228484128",
))

daisy.add(Armor(
    "Daisy_Clothing_Boots",
    using="_Foot",
    Rarity="Legendary",
    RootTemplate="216f0362-f77b-420c-84cb-d84853aa173d",
))

daisy.add(Armor(
    "Daisy_Clothing_Gloves",
    using="_Hand",
    Rarity="Legendary",
    RootTemplate="5a0ee632-9145-48b2-9b92-97c32c2ccbd9",
))

daisy.add(TreasureTable("""
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_Daisy_Clothing_Armor",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_Daisy_Clothing_Boots",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_Daisy_Clothing_Gloves",1,0,0,0,0,0,0,0
"""))

daisy.build()
