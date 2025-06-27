
import os

from moddb import (
    Awareness,
    BattleMagic,
    Bolster,
    Defense,
    EmpoweredSpells,
    Movement,
    PackMule,
)
from modtools.lsx.game import (
    CharacterAbility,
    ClassDescription,
    Progression,
)
from modtools.replacers import (
    CharacterClass,
    class_description,
    progression,
    Replacer,
    wizard_cantrips,
    wizard_level_1_spells,
    wizard_level_2_spells,
    wizard_level_3_spells,
    wizard_level_4_spells,
    wizard_level_5_spells,
    wizard_level_6_spells,
)


class PaladinFullCaster(Replacer):
    # Passives
    _awareness: str
    _battle_magic: str
    _empowered_spells: str
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str
    _fast_movement_75: str
    _pack_mule: str
    _warding: str

    # Spells
    _bolster: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="PaladinFullCaster",
                         description="A class replacer for Paladin.",
                         **kwds)

        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(4.5)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(6.0)
        self._fast_movement_75 = Movement(self.mod).add_fast_movement(7.5)

        self._awareness = Awareness(self.mod).add_awareness(5)
        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.CHARISMA)
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)
        self._warding = Defense(self.mod).add_warding()

        self._bolster = Bolster(self.mod).add_bolster_spell_list()

    @class_description(CharacterClass.PALADIN)
    def paladin_class_description(self, description: ClassDescription) -> None:
        description.CanLearnSpells = True
        description.MulticlassSpellcasterModifier = 1.0
        description.children.append(ClassDescription.Tags(
            Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
        ))

    @progression(CharacterClass.PALADIN, 1)
    def paladin_level_1(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            "DevilsSight",
            self._battle_magic,
            self._pack_mule,
            self._warding,
        ]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._bolster},,,,AlwaysPrepared)",
            f"SelectSpells({wizard_cantrips(self).UUID},3,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_1_spells(self).UUID},6,0)",
        ]

    @progression(CharacterClass.PALADIN, 2)
    def paladin_level_2(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            "SculptSpells",
            self._fast_movement_30,
        ]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_1_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 3)
    def paladin_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [self._awareness]
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 4)
    def paladin_level_4(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 5)
    def paladin_level_5(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_3_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 6)
    def paladin_level_6(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["PotentCantrip"]
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
            f"SelectSpells({wizard_level_3_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 7)
    def paladin_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [self._fast_movement_45]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + [self._fast_movement_30]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 8)
    def paladin_level_8(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 9)
    def paladin_level_9(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
            f"SelectSpells({wizard_level_5_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 10)
    def paladin_level_10(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [self._empowered_spells]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_5_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 11)
    def paladin_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            "ExtraAttack_2",
            "ReliableTalent",
        ]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 12)
    def paladin_level_12(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [self._fast_movement_60]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + [self._fast_movement_45]
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 13)
    def paladin_level_13(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 14)
    def paladin_level_14(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 15)
    def paladin_level_15(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 16)
    def paladin_level_16(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 17)
    def paladin_level_17(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [self._fast_movement_75]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + [self._fast_movement_60]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 18)
    def paladin_level_18(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 19)
    def paladin_level_19(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.PALADIN, 20)
    def paladin_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_3"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack_2"]
        progress.Selectors = (progress.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]


def main() -> None:
    paladin_full_caster = PaladinFullCaster(
        classes=[CharacterClass.PALADIN],
        feats=2,
        spells=2,
        warlock_spells=2,
        actions=2,
        skills=4,
        expertise=2,
        full_caster=True,
    )
    paladin_full_caster.build()


if __name__ == "__main__":
    main()
