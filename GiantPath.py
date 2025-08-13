
from functools import cached_property
import os

from moddb import (
    Attack,
    Bolster,
    CunningActions,
    PackMule,
)
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class GiantPath(Replacer):
    # Passives
    _pack_mule: str
    _running_jump: str
    _warding: str

    # Spells
    _bolster: str
    _brutal_cleave: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="GiantPath",
                         description="A class replacer for GiantPath.",
                         **kwds)
        
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)
        self._running_jump = CunningActions(self.mod).add_running_jump()

        self._bolster = Bolster(self.mod).add_bolster()
        self._brutal_cleave = Attack(self.mod).add_brutal_cleave()

    @cached_property
    def _level_3_spells(self) -> SpellList:
        spells = SpellList(
            Name="Barbarian level 3 spells",
            Spells=[
                self._bolster,
                self._brutal_cleave,
            ],
            UUID=self.make_uuid("level_3_spells"),
        )
        self.mod.add(spells)
        return spells

    @progression(CharacterClass.BARBARIAN_GIANT, 1)
    def giantpath_level_1(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 2)
    def giantpath_level_2(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 3)
    def giantpath_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            "Shout_Dash_CunningAction",
            "FastHands",
            "JackOfAllTrades",
            self._pack_mule,
            self._running_jump,
        ]
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            f"AddSpells({self._level_3_spells.UUID})",
        ]

    @progression(CharacterClass.BARBARIAN_GIANT, 4)
    def giantpath_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 5)
    def giantpath_level_5(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 6)
    def giantpath_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 7)
    def giantpath_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 8)
    def giantpath_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 9)
    def giantpath_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 10)
    def giantpath_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 11)
    def giantpath_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_2", "ReliableTalent"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack"]

    @progression(CharacterClass.BARBARIAN_GIANT, 12)
    def giantpath_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 13)
    def giantpath_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 14)
    def giantpath_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 15)
    def giantpath_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 16)
    def giantpath_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 17)
    def giantpath_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 18)
    def giantpath_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 19)
    def giantpath_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 20)
    def giantpath_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_3"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack_2"]


def main() -> None:
    giant_path = GiantPath(
        classes=[CharacterClass.BARBARIAN_GIANT],
        feats=2,
        actions=4,
    )
    giant_path.build()


if __name__ == "__main__":
    main()
