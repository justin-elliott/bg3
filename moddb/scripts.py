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
