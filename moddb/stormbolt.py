#!/usr/bin/env python3
"""
Add the Storm Bolt cantrip.
"""


from modtools.gamedata import SpellData
from modtools.mod import Mod


def storm_bolt(mod: Mod) -> None:
    """Add the Storm Bolt cantrip, returning its name."""
    name = f"{mod.get_prefix()}_StormBolt"

    loca = mod.get_localization()
    loca[f"{name}_DisplayName"] = {"en": "Storm Bolt"}
    loca[f"{name}_Description"] = {"en": "Project a bolt of lightning."}

    mod.add(SpellData(
        name,
        using="Projectile_WitchBolt",
        SpellType="Projectile",
        Level="",
        ConcentrationSpellID="",
        DisplayName=loca[f"{name}_Description"],
        Description=loca[f"{name}_Description"],
        Icon="GenericIcon_DamageType_Lightning",
        SpellProperties=["GROUND:DealDamage(LevelMapValue(D10Cantrip),Lightning)"],
        SpellSuccess=["DealDamage(LevelMapValue(D10Cantrip),Lightning,Magical)"],
        TooltipDamageList=["DealDamage(LevelMapValue(D10Cantrip),Lightning)"],
        TooltipStatusApply="",
        TooltipUpcastDescription="",
        TooltipUpcastDescriptionParams="",
        SpellFlags=[
            "HasVerbalComponent",
            "HasSomaticComponent",
            "IsSpell",
            "HasHighGroundRangeExtension",
            "RangeIgnoreVerticalThreshold",
            "IsHarmful",
        ],
        UseCosts="ActionPoint:1",
    ))

    return name
