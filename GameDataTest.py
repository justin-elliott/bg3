#!/usr/bin/env python3
"""
Test code for modtools.lsx_v2.
"""

import modtools.valuelists_v2 as VL
from modtools.gamedata_v2 import Armor, SpellData


armor = Armor("MyArmor")
armor.DurabilityDegradeSpeed = 5
armor.Shield = VL.YesNo.YES
print(armor)

armor = Armor(
    "AlsoMyArmor",
    using="MyArmor",
    DurabilityDegradeSpeed=5,
    Shield="No",
    Flags=[VL.AttributeFlags.GROUNDED, VL.AttributeFlags.BACKSTABIMMUNITY, VL.AttributeFlags.UNBREAKABLE]
)
print(armor)

spell_data = SpellData(
    "MySpell",
    SpellType="Shout",
)
print(spell_data)
