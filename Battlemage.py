
import os

from functools import cached_property
from moddb import (
    Awareness,
    BattleMagic,
    Defense,
    Movement,
)
from modtools.lsx.game import (
    CharacterAbility,
    Progression,
    SpellList,
)
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class Battlemage(Replacer):
    # Passives
    _awareness: str
    _battle_magic: str
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str
    _fast_movement_75: str
    _unarmored_defense: str
    _warding: str

    @cached_property
    def _spells_level_2(self) -> str:
        name = "Bladesinging spells gained at level 2"
        spells = SpellList(
            Name=name,
            Spells=[
                "Target_Command_Container",
                "Projectile_EldritchBlast",
            ],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return str(spells.UUID)

    @cached_property
    def _spells_level_11(self) -> str:
        name = "Bladesinging spells gained at level 11"
        spells = SpellList(
            Name=name,
            Spells=["Projectile_Fly"],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return str(spells.UUID)

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Battlemage",
                         description="A class replacer for BladesingingSchool.",
                         **kwds)

        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_75 = Movement(self.mod).add_fast_movement(3.0)

        self._awareness = Awareness(self.mod).add_awareness(5)
        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._unarmored_defense = Defense(self.mod).add_unarmored_defense(CharacterAbility.INTELLIGENCE)
        self._warding = Defense(self.mod).add_warding()

    @progression(CharacterClass.WIZARD_BLADESINGING, 2)
    def wizard_bladesinging_level_2(self, progress: Progression) -> None:
        progress.Boosts += ["IncreaseMaxHP(ClassLevel(Wizard))"]
        progress.PassivesAdded += [
            self._battle_magic,
            self._fast_movement_30,
            "SculptSpells",
            self._unarmored_defense,
            self._warding,
        ]
        progress.Selectors += [
            f"AddSpells({self._spells_level_2},,,,AlwaysPrepared)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 3)
    def wizard_bladesinging_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._awareness]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 4)
    def wizard_bladesinging_level_4(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            "DevilsSight",
            "JackOfAllTrades",
            "RepellingBlast",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 5)
    def wizard_bladesinging_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack", "UncannyDodge"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 6)
    def wizard_bladesinging_level_6(self, progress: Progression) -> None:
        progress.PassivesAdded += ["PotentCantrip"]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 7)
    def wizard_bladesinging_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = ["Evasion", self._fast_movement_45]
        progress.PassivesRemoved = [self._fast_movement_30]

    @progression(CharacterClass.WIZARD_BLADESINGING, 8)
    def wizard_bladesinging_level_8(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            "FOR_NightWalkers_WebImmunity",
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 9)
    def wizard_bladesinging_level_9(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 10)
    def wizard_bladesinging_level_10(self, progress: Progression) -> None:
        progress.PassivesAdded += ["EmpoweredEvocation"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 11)
    def wizard_bladesinging_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded += ["ReliableTalent"]
        progress.Selectors += [
            f"AddSpells({self._spells_level_11},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 12)
    def wizard_bladesinging_level_12(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2", self._fast_movement_60]
        progress.PassivesRemoved = ["ExtraAttack", self._fast_movement_45]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 13)
    def wizard_bladesinging_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 14)
    def wizard_bladesinging_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 15)
    def wizard_bladesinging_level_15(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 16)
    def wizard_bladesinging_level_16(self, progress: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 17)
    def wizard_bladesinging_level_17(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_75]
        progress.PassivesRemoved = [self._fast_movement_60]

    @progression(CharacterClass.WIZARD_BLADESINGING, 18)
    def wizard_bladesinging_level_18(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 19)
    def wizard_bladesinging_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 20)
    def wizard_bladesinging_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]


def main() -> None:
    battlemage = Battlemage(
        classes=[
            CharacterClass.WIZARD_BLADESINGING
        ],
        feats=2,
        spells=2,
        actions=2,
    )
    battlemage.build()


if __name__ == "__main__":
    main()
