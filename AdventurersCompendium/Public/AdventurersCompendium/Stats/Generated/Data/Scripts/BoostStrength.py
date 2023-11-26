#!/usr/bin/env python3

import os
import sys

from Boost import Boost
from typing import Final

SCRIPTS_DIR: Final[str] = os.path.dirname(os.path.abspath(sys.argv[0]))
DATA_DIR: Final[str] = os.path.normpath(os.path.join(SCRIPTS_DIR, ".."))
SPELL_FILE: Final[str] = os.path.join(DATA_DIR, "BoostStrength.txt")

boost = Boost("BoostStrength",
              display_name="AdventurersCompendium_BoostStrength_DisplayName",
              description="AdventurersCompendium_BoostStrength_Description",
              icon="Spell_Transmutation_EnhanceAbility_BullsStrenght",
              cast_sound="Spell_Cast_Buff_EnhanceAbilityBearsEndurance_L1to3",
              target_sound="Spell_Impact_Buff_EnhanceAbilityBearsEndurance_L1to3",
              boosts="Ability(Strength,1,30)")

with open(SPELL_FILE, "w") as f:
    boost.write(f)