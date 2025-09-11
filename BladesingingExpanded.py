
import os

from functools import cached_property
from moddb import (
    Awareness,
    Bolster,
    Defense,
    Guidance,
    Movement,
    PackMule,
)
from modtools.gamedata import SpellData, StatusData
from modtools.lsx.game import (
    CharacterAbility,
    ClassDescription,
    Progression,
    SpellList,
)
from modtools.replacers import (
    CharacterClass,
    class_description,
    progression,
    Replacer,
)
from typing import Final
from uuid import UUID


class BladesingingExpanded(Replacer):
    _METAMAGIC: Final[UUID] = UUID("c3506532-36eb-4d18-823e-497a537a9619")

    # Passives
    _awareness: str
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str
    _fast_movement_75: str
    _pack_mule: str
    _unarmored_defense: str
    _warding: str

    # Spells
    _arcane_guidance: str
    _bolster: str

    @cached_property
    def _spells_level_2(self) -> str:
        name = "Bladesinging spells gained at level 2"
        spells = SpellList(
            Name=name,
            Spells=[
                self._arcane_guidance,
                "Target_Command_Container",
                "Projectile_EldritchBlast",
            ],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return str(spells.UUID)

    @cached_property
    def _spells_level_3(self) -> str:
        name = "Bladesinging spells gained at level 3"
        spells = SpellList(
            Name=name,
            Spells=[
                "Shout_CreateSorceryPoints",
                "Shout_CreateSpellSlot",
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
                         name="BladesingingExpanded",
                         description="A class replacer for BladesingingSchool.",
                         **kwds)

        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_75 = Movement(self.mod).add_fast_movement(3.0)

        self._awareness = Awareness(self.mod).add_awareness(5)
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)
        self._unarmored_defense = Defense(self.mod).add_unarmored_defense(CharacterAbility.INTELLIGENCE)
        self._warding = Defense(self.mod).add_warding()

        self._arcane_guidance = Guidance(self.mod).add_arcane_guidance()
        self._bolster = Bolster(self.mod).add_bolster_spell_list()

    @class_description(CharacterClass.WIZARD_BLADESINGING)
    def wizard_bladesinging_class_description(self, class_description: ClassDescription) -> None:
        class_description.children.append(ClassDescription.Tags(
            Object="18266c0b-efbc-4c80-8784-ada4a37218d7"  # SORCERER
        ))

    @progression(CharacterClass.WIZARD, 1)
    def wizard_level_1(self, progress: Progression) -> None:
        progress.Selectors += [f"AddSpells({self._bolster},,,,AlwaysPrepared)"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 2)
    def wizard_bladesinging_level_2(self, progress: Progression) -> None:
        progress.Boosts += ["Tag(SORCERER_METAMAGIC)"]
        progress.PassivesAdded += [
            "DevilsSight",
            "JackOfAllTrades",
            "RepellingBlast",
            "SculptSpells",
            self._fast_movement_30,
            self._pack_mule,
            self._unarmored_defense,
            self._warding,
        ]
        progress.Selectors += [
            f"AddSpells({self._spells_level_2},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 3)
    def wizard_bladesinging_level_3(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{3 * self.args.actions},0)"]
        progress.PassivesAdded = [self._awareness]
        progress.Selectors += [
            f"AddSpells({self._spells_level_3},,,,AlwaysPrepared)",
            f"SelectPassives({self._METAMAGIC},4,Metamagic)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 4)
    def wizard_bladesinging_level_4(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 5)
    def wizard_bladesinging_level_5(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded = ["UncannyDodge"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 6)
    def wizard_bladesinging_level_6(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded += ["PotentCantrip"]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 7)
    def wizard_bladesinging_level_7(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded = ["Evasion", self._fast_movement_45]
        progress.PassivesRemoved = [self._fast_movement_30]

    @progression(CharacterClass.WIZARD_BLADESINGING, 8)
    def wizard_bladesinging_level_8(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded = [
            "FOR_NightWalkers_WebImmunity",
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 9)
    def wizard_bladesinging_level_9(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 10)
    def wizard_bladesinging_level_10(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded += ["EmpoweredEvocation"]
        progress.Selectors = [f"SelectPassives({self._METAMAGIC},1,Metamagic)"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 11)
    def wizard_bladesinging_level_11(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded += ["ReliableTalent"]
        progress.Selectors += [
            f"AddSpells({self._spells_level_11},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 12)
    def wizard_bladesinging_level_12(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded = ["ExtraAttack_2", self._fast_movement_60]
        progress.PassivesRemoved = ["ExtraAttack", self._fast_movement_45]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 13)
    def wizard_bladesinging_level_13(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 14)
    def wizard_bladesinging_level_14(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 15)
    def wizard_bladesinging_level_15(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 16)
    def wizard_bladesinging_level_16(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 17)
    def wizard_bladesinging_level_17(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded = [self._fast_movement_75]
        progress.PassivesRemoved = [self._fast_movement_60]
        progress.Selectors += [f"SelectPassives({self._METAMAGIC},1,Metamagic)"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 18)
    def wizard_bladesinging_level_18(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.WIZARD_BLADESINGING, 19)
    def wizard_bladesinging_level_19(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]

    @progression(CharacterClass.WIZARD_BLADESINGING, 20)
    def wizard_bladesinging_level_20(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]


def main() -> None:
    bladesinging_expanded = BladesingingExpanded(
        classes=[
            CharacterClass.WIZARD_BLADESINGING
        ],
        feats=2,
        spells=2,
        warlock_spells=2,
        actions=4,
        skills=4,
        expertise=2,
    )
    bladesinging_expanded.build()


if __name__ == "__main__":
    main()
