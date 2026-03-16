#!/usr/bin/env python3
"""
Add the Storm Bolt cantrip.
"""


from modtools.gamedata import SpellData
from modtools.mod import Mod


def storm_bolt(mod: Mod) -> str:
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
        DisplayName=loca[f"{name}_DisplayName"],
        Description=loca[f"{name}_Description"],
        Icon="Spell_Evocation_ActivateWitchBolt",
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


def storm_bolts(mod: Mod) -> str:
    """Add the Storm Bolts cantrip, returning its name."""
    name = mod.make_name("StormBolts")

    mod.loca[f"{name}_DisplayName"] = "Storm Bolts"
    mod.loca[f"{name}_Description"] = "Project [1] bolt(s) of lightning."

    mod.add(SpellData(
        name,
        using="Projectile_WitchBolt",
        SpellType="Projectile",
        Level="",
        ConcentrationSpellID="",
        DisplayName=mod.loca[f"{name}_DisplayName"],
        Description=mod.loca[f"{name}_Description"],
        DescriptionParams=["LevelMapValue(EldritchBlast)"],
        Icon="Spell_Evocation_ActivateWitchBolt",
        AmountOfTargets=["LevelMapValue(EldritchBlast)"],
        SpellProperties=["GROUND:DealDamage(1d10,Lightning)"],
        SpellSuccess=["DealDamage(1d10,Lightning,Magical)"],
        TooltipDamageList=["DealDamage(1d10,Lightning)"],
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
        UseCosts=["ActionPoint:1"],
    ))

    return name
