#!/usr/bin/env python3
"""
Bolster for Baldur's Gate 3 mods.
"""
from functools import cache

from modtools.gamedata import SpellData, StatusData
from modtools.mod import Mod
from modtools.lsx.game import LevelMapSeries, SpellList


class Bolster:
    """Adds the Bolster spell to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    @cache
    def add_bolster(self) -> str:
        """Add the Bolster spell, returning its name."""
        name = f"{self._mod.get_prefix()}_Bolster"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Bolster"}
        loca[f"{name}_Description"] = {"en": """
            Bolster your allies against the dangers that lie ahead.
            """}
        loca[f"{name}_StatusDescription"] = {"en": """
            Hit point maximum increased by [1].

            When you roll a 1 on an <LSTag Tooltip="AttackRoll">Attack Roll</LSTag>,
            <LSTag Tooltip="AbilityCheck">Ability Check</LSTag>, or
            <LSTag Tooltip="SavingThrow">Saving Throw</LSTag>,
            you can reroll the die and must use the new roll.

            You can see in the dark up to [2].
            """}

        self._mod.add(SpellData(
            name,
            using="Shout_Aid",
            SpellType="Shout",
            AreaRadius="36",
            Cooldown="None",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Level="",
            RequirementConditions="",
            Requirements="!Combat",
            SpellProperties=[
                f"ApplyStatus({name.upper()},100,-1)",
                "ApplyStatus(FEATHER_FALL,100,-1)",
                "ApplyStatus(LONGSTRIDER,100,-1)",
                "ApplyStatus(PETPAL,100,-1)",
                "IF(not WearingArmor()):ApplyStatus(MAGE_ARMOR,100,-1)",
            ],
            TargetConditions="Party() and not Dead()",
            TooltipStatusApply=[
                f"ApplyStatus({name.upper()},100,-1)",
                "ApplyStatus(FEATHER_FALL,100,-1)",
                "ApplyStatus(LONGSTRIDER,100,-1)",
                "ApplyStatus(PETPAL,100,-1)",
                "ApplyStatus(MAGE_ARMOR,100,-1)",
            ],
            UseCosts="ActionPoint:1",
            VerbalIntent="Buff",
        ))

        self._mod.add(StatusData(
            name.upper(),
            StatusType="BOOST",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_StatusDescription"],
            DescriptionParams=[
                f"LevelMapValue({name}_AidValue)",
                "Distance(12)",
            ],
            Icon="Spell_Abjuration_Aid",
            StackId="AID",  # Mutually exclusive with AID stacks
            Boosts=[
                f"IncreaseMaxHP(LevelMapValue({name}_AidValue))",
                "Reroll(Attack,1,true)",
                "Reroll(SkillCheck,1,true)",
                "Reroll(RawAbility,1,true)",
                "Reroll(SavingThrow,1,true)",
                "DarkvisionRangeMin(12)",
                "ActiveCharacterLight(051648e6-f05a-e41f-e398-ffd5cd148989)",
            ],
            StatusGroups="SG_RemoveOnRespec",
        ))

        self._mod.add(LevelMapSeries(
            **{f"Level{level}": f"{int(level * 2.5)}" for level in range(1, 21)},
            Name=f"{name}_AidValue",
            UUID=self._mod.make_uuid(f"{name}_AidValue"),
        ))

        return name

    @cache
    def add_bolster_spell_list(self) -> str:
        """Add a spell list containing the Bolster spell."""
        spell_list = str(self._mod.make_uuid("bolster_spell_list"))
        self._mod.add(SpellList(
            Comment="Bolster spell list",
            Spells=[self.add_bolster()],
            UUID=spell_list,
        ))
        return spell_list
