#!/usr/bin/env python3
"""
Generates files for the "EldritchKnightFullCaster" mod.
"""

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
from modtools.lsx.game import (
    CharacterClass,
    ClassDescription,
    Progression,
    SpellList,
)
from modtools.replacers import (
    class_description,
    only_existing_progressions,
    progression,
    Replacer,
    eldritch_knight_cantrips,
    eldritch_knight_level_1_spells,
    eldritch_knight_level_2_spells,
    wizard_cantrips,
    wizard_level_1_spells,
    wizard_level_2_spells,
    wizard_level_3_spells,
    wizard_level_4_spells,
    wizard_level_5_spells,
    wizard_level_6_spells,
)
from typing import Final
from uuid import UUID


class EldritchKnightFullCaster(Replacer):
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

    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="EldritchKnightFullCaster",
                         description="Full casting for the Eldritch Knight subclass.",
                         **kwds)

        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_75 = Movement(self.mod).add_fast_movement(3.0)

        self._awareness = Awareness(self.mod).add_awareness(5)
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)
        self._warding = Defense(self.mod).add_warding()

        self._arcane_guidance = Guidance(self.mod).add_arcane_guidance()
        self._bolster = Bolster(self.mod).add_bolster_spell_list()

    @cached_property
    def _spells_level_3(self) -> str:
        name = "Eldritch Knight spells gained at level 3"
        spells = SpellList(
            Name=name,
            Spells=[
                self._arcane_guidance,
                self._bolster,
                "Target_Command_Container",
                "Projectile_EldritchBlast",
            ],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return str(spells.UUID)

    @cached_property
    def _spells_level_4(self) -> str:
        name = "Eldritch Knight spells gained at level 4"
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

    @class_description(CharacterClass.FIGHTER_ELDRITCHKNIGHT)
    def eldritch_knight_description(self, class_description: ClassDescription) -> None:
        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.children.append(ClassDescription.Tags(
            Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
        ))

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, range(3, 21))
    @only_existing_progressions
    def level_3_to_20(self, progress: Progression) -> None:
        progress.Selectors = [
            selector for selector in (progress.Selectors or [])
            if not selector.startswith(f"SelectSpells({eldritch_knight_cantrips(self).UUID}")
            and not selector.startswith(f"SelectSpells({eldritch_knight_level_1_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({eldritch_knight_level_2_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_cantrips(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_1_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_2_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_3_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_4_spells(self).UUID}")
        ] or None

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 3)
    def level_3(self, progress: Progression) -> None:
        progress.Boosts += ["Tag(SORCERER_METAMAGIC)"]
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            "DevilsSight",
            "RepellingBlast",
            "SculptSpells",
            self._awareness,
            self._fast_movement_30,
            self._pack_mule,
            self._warding
        ]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._spells_level_3},,,,AlwaysPrepared)",
            f"SelectSpells({wizard_cantrips(self).UUID},4,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},4,0)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 4)
    def level_4(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{4 * self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._spells_level_4},,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},1,1)",
            f"SelectPassives({self._METAMAGIC},4,Metamagic)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 5)
    def level_5(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded += ["UncannyDodge"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_3_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 6)
    def level_6(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_3_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["PotentCantrip"]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 7)
    def level_7(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded += ["Evasion", self._fast_movement_45]
        progress.PassivesRemoved = [self._fast_movement_30]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 8)
    def level_8(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 9)
    def level_9(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_5_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 10)
    def level_10(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_5_spells(self).UUID},1,1)",
            f"SelectPassives({self._METAMAGIC},1,Metamagic)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["EmpoweredEvocation"]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 11)
    def level_11(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ReliableTalent"]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 12)
    def level_12(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded = [self._fast_movement_60]
        progress.PassivesRemoved = [self._fast_movement_45]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 13)
    def level_13(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 14)
    def level_14(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 15)
    def level_15(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 16)
    def level_16(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 17)
    def level_17(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.PassivesAdded = [self._fast_movement_75]
        progress.PassivesRemoved = [self._fast_movement_60]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
            f"SelectPassives({self._METAMAGIC},1,Metamagic)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 18)
    def level_18(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)"
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 19)
    def level_19(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 20)
    def level_20(self, progress: Progression) -> None:
        progress.Boosts += [f"ActionResource(SorceryPoint,{self.args.actions},0)"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},1,1)",
        ]


def main():
    eldritch_knight_full_caster = EldritchKnightFullCaster(
        classes=[CharacterClass.FIGHTER_ELDRITCHKNIGHT],
        spells=2,
        full_caster=True,
    )
    eldritch_knight_full_caster.build()


if __name__ == "__main__":
    main()
