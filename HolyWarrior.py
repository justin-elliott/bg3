#!/usr/bin/env python3
"""
Generates files for the "HolyWarrior" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    Movement,
    multiply_resources,
)
from modtools.gamedata import SpellData, StatusData
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    SpellList,
)
from modtools.lsx.game import Origin, Progression, ProgressionDescription
from modtools.replacers import Replacer, origin, progression


class HolyWarrior(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Channel Divinity, War Priest charges)

    AURA_RADIUS = 9

    _args: Args
    _feat_levels: set[int]

    # Passives
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str

    @cached_property
    def _aura_of_protection(self) -> SpellList:
        shout_name = f"{self.mod.get_prefix()}_AuraOfProtection"
        status_name = shout_name.upper()

        boosts = [
            "RollBonus(SavingThrow,max(1,Cause.WisdomModifier))",
            "RollBonus(DeathSavingThrow,max(1,Cause.WisdomModifier))",
        ]

        self.mod.add(SpellData(
            shout_name,
            using="Shout_AuraOf_Protection",
            SpellType="Shout",
            AreaRadius=self.AURA_RADIUS,
            SpellProperties=f"ApplyStatus({status_name},100,-1)",
            DescriptionParams="max(1,WisdomModifier)",
            TooltipStatusApply=f"ApplyStatus({status_name},100,-1)",
            RequirementConditions=f"not HasStatus('{status_name}')",
        ))

        self.mod.add(StatusData(
            status_name,
            using="AURA_OF_PROTECTION",
            StatusType="BOOST",
            DescriptionParams="max(1,Cause.WisdomModifier)",
            AuraRadius=self.AURA_RADIUS,
            AuraStatuses=f"IF(Ally() and not Tagged('INANIMATE')):ApplyStatus({status_name}_BUFF)",
            Boosts=boosts,
        ))

        self.mod.add(StatusData(
            f"{status_name}_BUFF",
            using="AURA_OF_PROTECTION_BUFF",
            StatusType="BOOST",
            DescriptionParams=[
                f"Distance({self.AURA_RADIUS})",
                "max(1,Cause.WisdomModifier)",
            ],
            Boosts=boosts,
        ))

        spells = SpellList(
            Comment="War Domain Cleric Aura of Protection",
            Spells=[shout_name],
            UUID=self.make_uuid(shout_name),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _aura_of_warding(self) -> SpellList:
        shout_name = f"{self.mod.get_prefix()}_AuraOfWarding"
        status_name = shout_name.upper()

        self.mod.add(SpellData(
            shout_name,
            using="Shout_AuraOf_Warding",
            SpellType="Shout",
            AreaRadius=self.AURA_RADIUS,
            SpellProperties=f"ApplyStatus({status_name},100,-1)",
            TooltipStatusApply=f"ApplyStatus({status_name},100,-1)",
            RequirementConditions=f"not HasStatus('{status_name}')",
        ))

        self.mod.add(StatusData(
            status_name,
            using="AURA_OF_WARDING",
            StatusType="BOOST",
            AuraRadius=self.AURA_RADIUS,
        ))

        self.mod.add(StatusData(
            f"{status_name}_BUFF",
            using="AURA_OF_WARDING_BUFF",
            StatusType="BOOST",
            DescriptionParams=f"Distance({self.AURA_RADIUS})",
        ))

        spells = SpellList(
            Comment="War Domain Cleric Aura of Warding",
            Spells=[shout_name],
            UUID=self.make_uuid(shout_name),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _counterspell(self) -> SpellList:
        spells = SpellList(
            Comment="War Domain Cleric Counterspell",
            Spells=["Target_Counterspell"],
            UUID=self.make_uuid("Counterspell"),
        )
        self.mod.add(spells)
        return spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="HolyWarrior",
                         description="Boosts War Domain Cleric.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        # Passives
        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(4.5)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(6.0)

    @origin("Shadowheart")
    def shadowheart(self, origin: Origin) -> None:
        origin.LockClass = None

    @progression(CharacterClass.CLERIC, range(1, 13))
    @progression(CharacterClass.CLERIC, 1, is_multiclass=True)
    def level_1_to_12_cleric(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression, [ActionResource.CHANNEL_DIVINITY_CHARGES], self._args.actions)

    @progression(CharacterClass.CLERIC_WAR, range(1, 13))
    def level_1_to_12_war_domain(self, progression: Progression) -> None:
        multiply_resources(progression, [ActionResource.WAR_PRIEST_CHARGES], self._args.actions)

    @progression(CharacterClass.CLERIC_WAR, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ProficiencyBonus(SavingThrow,Constitution)",
            "IncreaseMaxHP(ClassLevel(Cleric))",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_30,
        ]
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_DisplayName"] = {"en": "Holy Warrior"}
        loca[f"{self.mod.get_prefix()}_Description"] = {"en": """
            Your <LSTag Tooltip="HitPoints">hit point</LSTag> maximum increases by 1 for each Cleric level.
            """}
        self.mod.add(ProgressionDescription(
            DisplayName=loca[f"{self.mod.get_prefix()}_DisplayName"],
            Description=loca[f"{self.mod.get_prefix()}_Description"],
            ExactMatch="IncreaseMaxHP(ClassLevel(Cleric))",
            ProgressionId=progression.UUID,
            UUID=self.mod.make_uuid("IncreaseMaxHP"),
        ))

    @progression(CharacterClass.CLERIC_WAR, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Smite_Divine",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(58aef51d-a46c-44c8-8bed-df90870eb55f,,,,AlwaysPrepared)",  # Smite
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]

    @progression(CharacterClass.CLERIC_WAR, 3)
    def level_3(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.CLERIC_WAR, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(ChannelDivinity,{self._args.actions},0)",
        ]

    @progression(CharacterClass.CLERIC_WAR, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_45,
            "ExtraAttack",
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_30,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._counterspell.UUID},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_WAR, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ImprovedCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._aura_of_protection.UUID},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_WAR, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._aura_of_warding.UUID},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_WAR, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(ChannelDivinity,{self._args.actions},0)",
        ]

    @progression(CharacterClass.CLERIC_WAR, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_60,
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_45,
        ]

    @progression(CharacterClass.CLERIC_WAR, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(ChannelDivinity,{self._args.actions},0)",
        ]

    @progression(CharacterClass.CLERIC_WAR, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a,,,,AlwaysPrepared)",  # Volley, Whirlwind
        ]

    @progression(CharacterClass.CLERIC_WAR, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
            f"ActionResource(ChannelDivinity,{self._args.actions},0)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "BrutalCritical",
        ]


def main():
    parser = argparse.ArgumentParser(description="Boosts War Domain Cleric.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=1,
                        help="Feat progression every n levels (defaulting to 1; feat every level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Channel Divinity, War Priest charges) multiplier"
                             " (defaulting to 2; double charges)")
    args = HolyWarrior.Args(**vars(parser.parse_args()))

    holy_warrior = HolyWarrior(args)
    holy_warrior.build()


if __name__ == "__main__":
    main()
