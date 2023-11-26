#!/usr/bin/env python3

from Boost import Boost

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
boost.generate_spell_file()