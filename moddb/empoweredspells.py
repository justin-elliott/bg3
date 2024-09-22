#!/usr/bin/env python3
"""
Empowered Spells for Baldur's Gate 3 mods.
"""

from modtools.gamedata import PassiveData
from modtools.lsx.game import CharacterAbility
from modtools.mod import Mod


class EmpoweredSpells:
    """Adds the Empowered Spells passive to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    def add_empowered_spells(self, ability: CharacterAbility = None) -> str:
        """Add the Empowered Spells passive, returning its name. The damage bonus comes from the given 'ability'."""
        if ability is not None:
            ability_name = ability.name.title()
            modifier_name = f"{ability_name}Modifier"
            modifier_description = f"""
                <LSTag Tooltip="{ability_name}">{ability_name}</LSTag>
                <LSTag Tooltip="AbilityModifier">Modifier</LSTag>"
            """
        else:
            ability_name = "Spellcasting Modifier"
            modifier_name = "SpellcastingAbilityModifier"
            modifier_description = """
                <LSTag Tooltip="SpellcastingAbilityModifier">Spellcasting Modifier</LSTag>
            """

        name = f"{self._mod.get_prefix()}_EmpoweredSpells_{modifier_name}"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Empowered Spells"}
        loca[f"{name}_Description"] = {"en": f"""
            When you cast a damaging spell, add your {modifier_description} to the damage it deals.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_EmpoweredEvocation",
            Properties=["Highlighted"],
            Boosts=[f"IF(IsSpell()):DamageBonus(max(0,{modifier_name}))"],
        ))

        return name
