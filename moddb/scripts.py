#!/usr/bin/env python3
"""
Scripts for Baldur's Gate 3 mods.
"""

from modtools.text import Script


character_level_range = Script("""
-- Test that the character's level is in the closed interval [firstLevel, lastLevel].
function CharacterLevelRange(firstLevel, lastLevel, entity)
    entity = entity or context.Source
    return ConditionResult(entity.Level >= firstLevel and entity.Level <= lastLevel)
end
""")

__MANEUVER_SPELLS = " | ".join(f"SpellId('{spell}')" for spell in [
    "Target_CommandersStrike",
    "Target_DisarmingAttack",
    "Projectile_DisarmingAttack",
    "Target_DistractingStrike",
    "Projectile_DistractingStrike",
    "Shout_EvasiveFootwork",
    "Target_FeintingAttack",
    "Target_GoadingAttack",
    "Projectile_GoadingAttack",
    "Target_ManeuveringAttack",
    "Projectile_ManeuveringAttack",
    "Target_MenacingAttack",
    "Projectile_MenacingAttack",
    "Shout_PrecisionAttack",
    "Target_PushingAttack",
    "Projectile_PushingAttack",
    "Target_Rally",
    "Interrupt_Riposte",
    "Zone_SweepingAttack",
    "Target_TripAttack",
    "Projectile_TripAttack",
])

is_battle_master_maneuver = Script(f"""
-- Check for a Battle Master Maneuver.
function IsBattleMasterManeuver()
    return {__MANEUVER_SPELLS}
end
""")
