#!/usr/bin/env python3
"""
Generates files for the "Swashbuckler" mod.
"""

import argparse
import os

from dataclasses import dataclass
from moddb import (
    Bolster,
    Defense,
    CunningActions,
    Movement,
    PackMule,
)
from modtools.lsx.game import (
    CharacterClass,
    Dependencies,
    Progression,
)
from modtools.replacers import (
    DontIncludeProgression,
    progression,
    Replacer,
)


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class Swashbuckler(Replacer):
    @dataclass
    class Args:
        feats: int  # Feats every n levels

    _ACTION_SURGE_SPELL_LIST = "964e765d-5881-463e-b1b0-4fc6b8035aa8"

    _args: Args
    _feat_levels: set[int]

    # Passives
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str
    _fast_movement_75: str
    _pack_mule: str
    _running_jump: str

    # Spells
    _bolster: str
    _counterspell: str

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Swashbuckler",
                         description="Enhancements for the Swashbuckler subclass.")

        self.mod.add(Dependencies.ShortModuleDesc(
            Folder="UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            MD5="f94d034502139cf8b65a1597554e7236",
            Name="UnlockLevelCurve",
            PublishHandle=4166963,
            UUID="a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            Version64=72057594037927960,
        ))

        self._args = args

        if len(args.feats) == 0:
            self._feat_levels = frozenset({*range(2, 20, 2)} | {3, 9, 19})
        elif len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            self._feat_levels = frozenset(
                {*range(max(feat_level, 2), 20, feat_level)} | ({19} if 20 % feat_level == 0 else {}))
        else:
            self._feat_levels = args.feats - frozenset([1])

        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)
        self._bolster = Bolster(self.mod).add_bolster_spell_list()
        self._running_jump = CunningActions(self.mod).add_running_jump()

        fleet_of_foot = f"{self._mod.get_prefix()}_FleetOfFoot"
        loca = self._mod.get_localization()
        loca[fleet_of_foot] = {"en": "Fleet of Foot"}
    
        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0, loca[fleet_of_foot])
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(4.5, loca[fleet_of_foot])
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(6.0, loca[fleet_of_foot])
        self._fast_movement_75 = Movement(self.mod).add_fast_movement(7.5, loca[fleet_of_foot])

        counterspell = f"{self._mod.get_prefix()}_Counterspell"
        loca[counterspell] = {"en": "Dirty Trick: Counterspell"}
        self._counterspell = Defense(self.mod).add_counterspell_spell_list(display_name_handle=loca[counterspell])

    @progression(CharacterClass.ROGUE, 1)
    def rogue_1(self, progression: Progression) -> None:
        progression.PassivesAdded += [self._pack_mule]
        progression.Selectors += [f"AddSpells({self._bolster},,,,AlwaysPrepared)"]

    @progression(CharacterClass.ROGUE, range(2, 21))
    def allow_improvement_rogue(self, progression: Progression) -> None:
        allow_improvement = progression.AllowImprovement
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        if allow_improvement == progression.AllowImprovement:
            raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded += [
            self._fast_movement_30,
            self._running_jump,
            "Athlete_StandUp",
        ]
        progression.Selectors = [f"AddSpells({self._ACTION_SURGE_SPELL_LIST},,,,AlwaysPrepared)"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Selectors += ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack"]
        progression.Selectors = [f"AddSpells({self._counterspell},,Charisma,,AlwaysPrepared)"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 6)
    def level_6(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 7)
    def level_7(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            self._fast_movement_45,
            "FOR_NightWalkers_WebImmunity",
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
        ]
        progression.PassivesRemoved = [self._fast_movement_30]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 9)
    def level_9(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Selectors = ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack_2"]
        progression.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Selectors = ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 13)
    def level_13(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._fast_movement_60]
        progression.PassivesRemoved = [self._fast_movement_45]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 14)
    def level_14(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 15)
    def level_15(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 16)
    def level_16(self, progression: Progression) -> None:
        progression.Selectors = ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 17)
    def level_17(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 18)
    def level_18(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._fast_movement_75]
        progression.PassivesRemoved = [self._fast_movement_60]
        progression.Selectors = ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 19)
    def level_19(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 20)
    def level_20(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack_3"]
        progression.PassivesRemoved = ["ExtraAttack_2"]


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Enhancements for the Swashbuckler subclass.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    args = Swashbuckler.Args(**vars(parser.parse_args()))

    swashbuckler = Swashbuckler(args)
    swashbuckler.build()
