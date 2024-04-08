#!/usr/bin/env python3
"""
Cunning action spells for Baldur's Gate 3 mods.
"""

from functools import cached_property
from modtools.gamedata import SpellData
from modtools.lsx.game import SpellList
from modtools.mod import Mod


class CunningActions:
    """Adds the cunning actions spell list to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    def spell_list(self, *, step_of_the_wind=True) -> str:
        """Adds the cunning actions spell list, returning its name."""
        cunning_actions = str(self._mod.make_uuid(f"{self._mod.get_prefix()}_CunningActions_SpellList"))
        self._mod.add(SpellList(
            Comment="Cunning Actions",
            Spells=[
                self.cunning_action_dash if step_of_the_wind else "Shout_Dash_CunningAction",
                "Shout_Hide_BonusAction",
                "Shout_Disengage_CunningAction",
            ],
            UUID=cunning_actions,
        ))
        return cunning_actions

    @cached_property
    def cunning_action_dash(self) -> str:
        """Add the Cunning Action: Dash + Step of the Wind spell, returning its name."""
        name = f"{self._mod.get_prefix()}_CunningActionDash"
        self._mod.add(SpellData(
            name,
            using="Shout_Dash_CunningAction",
            SpellType="Shout",
            SpellProperties=[
                "IF(HasStatus('DASH_STACKED')):ApplyStatus(DASH_STACKED_2,100,1)",
                "IF(not HasStatus('DASH_STACKED_2') and HasStatus('DASH')):ApplyStatus(DASH_STACKED,100,1)",
                "IF(not HasStatus('DASH_STACKED_2') and not HasStatus('DASH_STACKED') and not HasStatus('DASH')):"
                + "ApplyStatus(DASH,100,1)",
                "ApplyStatus(STEP_OF_THE_WIND,100,1)",
            ],
            SpellFlags=["IgnoreSilence", "Stealth", "Invisible", "NoCameraMove"],
            TooltipStatusApply=[
                "ApplyStatus(DASH,100,1)",
                "ApplyStatus(STEP_OF_THE_WIND,100,1)",
            ],
        ))
        return name
