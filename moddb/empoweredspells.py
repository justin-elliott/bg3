#!/usr/bin/env python3
"""
Empowered Spells for Baldur's Gate 3 mods.
"""

from modtools.gamedata_v2 import PassiveData
from modtools.lsx.game import CharacterAbility
from modtools.mod import Mod


class EmpoweredSpells:
    """Adds the Empowered Spells passive to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    def add_empowered_spells(self, ability: CharacterAbility) -> str:
        """Add the Empowered Spells passive, returning its name. The damage bonus comes from the given 'ability'."""
        ability_name = ability.name.title()

        name = f"{self._mod.get_prefix()}_EmpoweredSpells_{ability_name}"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Empowered Spells"}
        loca[f"{name}_Description"] = {"en": f"""
            When you cast a damaging spell, add your <LSTag Tooltip="{ability_name}">{ability_name}</LSTag>
            <LSTag Tooltip="AbilityModifier">Modifier</LSTag> to the damage it deals.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_EmpoweredEvocation",
            Properties=["Highlighted"],
            Boosts=[f"IF(IsSpell()):DamageBonus(max(0,{ability_name}Modifier))"],
        ))

        return name
