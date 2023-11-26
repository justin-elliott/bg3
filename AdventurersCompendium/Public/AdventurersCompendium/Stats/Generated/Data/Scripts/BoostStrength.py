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
              prepare_effect="5ea8f8f4-ba5f-4417-82f6-ed2ce4ffe264",
              cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
              target_effect="fbb955f8-a644-451b-89bd-7950ad4cebad",
              boosts="Ability(Strength,1,30)")

with open(SPELL_FILE, "w") as f:
    boost.write(f)