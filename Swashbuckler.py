#!/usr/bin/env python3
"""
Generates files for the "Swashbuckler" mod.
"""

import os

from moddb import (
    Bolster,
    Defense,
    CunningActions,
    Movement,
    PackMule,
)
from modtools.lsx.game import (
    CharacterClass,
    Progression,
)
from modtools.replacers import (
    DontIncludeProgression,
    progression,
    Replacer,
)


class Swashbuckler(Replacer):
    _ACTION_SURGE_SPELL_LIST = "964e765d-5881-463e-b1b0-4fc6b8035aa8"

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

    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Swashbuckler",
                         description="Enhancements for the Swashbuckler subclass.",
                         **kwds)

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
    def level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 7)
    def level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

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
    def level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

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
    def level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 15)
    def level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 16)
    def level_16(self, progression: Progression) -> None:
        progression.Selectors = ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 17)
    def level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 18)
    def level_18(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._fast_movement_75]
        progression.PassivesRemoved = [self._fast_movement_60]
        progression.Selectors = ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"]

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 19)
    def level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_SWASHBUCKLER, 20)
    def level_20(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ExtraAttack_3"]
        progression.PassivesRemoved = ["ExtraAttack_2"]


if __name__ == "__main__":
    swashbuckler = Swashbuckler(classes=[CharacterClass.ROGUE_SWASHBUCKLER], feats=2)
    swashbuckler.build()
