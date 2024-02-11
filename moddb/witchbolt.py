#!/usr/bin/env python3
"""
Convert Witch Bolt into a cantrip.
"""


from modtools.gamedata import SpellData
from modtools.mod import Mod


def witch_bolt_to_cantrip(mod: Mod) -> None:
    """Replace the existing Witch Bolt spell with a cantrip."""

    loca = mod.get_localization()
    loca["Projectile_WitchBolt_Description"] = {"en": "Project a bolt of lightning."}

    mod.add(SpellData(
        "Projectile_WitchBolt",
        using="Projectile_WitchBolt",
        SpellType="Projectile",
        Level="",
        ConcentrationSpellID="",
        Description=loca["Projectile_WitchBolt_Description"],
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

    # Replace upcast spells with no-ops
    for level in range(2, 7):
        mod.add(SpellData(f"Projectile_WitchBolt_{level}", SpellType="Projectile"))
