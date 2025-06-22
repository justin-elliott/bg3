
import os

from functools import cached_property
from moddb import (
    Awareness,
    BattleMagic,
    Bolster,
    Defense,
    PackMule,
    Movement,
)
from modtools.gamedata import SpellData
from modtools.lsx.game import (
    ClassDescription,
    Progression,
    SpellList,
)
from modtools.replacers import (
    CharacterClass,
    class_description,
    DontIncludeProgression,
    progression,
    Replacer,
)


class Sorcadin(Replacer):
    # Passives
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str
    _fast_movement_75: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Sorcadin",
                         description="A class replacer for Sorcerer.",
                         **kwds)

        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_75 = Movement(self.mod).add_fast_movement(3.0)

    @cached_property
    def _searing_smite(self) -> str:
        """Add the Searing Smite spell without the concentration or bonus action cost."""
        name = f"{self.mod.get_prefix()}_SearingSmite"

        self.mod.add(SpellData(
            name,
            SpellType="Target",
            using="Target_Smite_Searing",
            HitCosts=["SpellSlotsGroup:1:1:1"],
            SpellFlags=["HasVerbalComponent", "IsHarmful", "IsMelee", "IsSpell"],
        ))

        for level in range(2, 10):
            self.mod.add(SpellData(
                f"{name}_{level}",
                SpellType="Target",
                using=f"Target_Smite_Searing_{level}",
                HitCosts=[f"SpellSlotsGroup:1:1:{level}"],
                RootSpellID=name,
                SpellFlags=["HasVerbalComponent", "IsHarmful", "IsMelee", "IsSpell"],
            ))

        return name

    @cached_property
    def _thunderous_smite(self) -> str:
        """Add the Thunderous Smite spell without the bonus action cost."""
        name = f"{self.mod.get_prefix()}_ThunderousSmite"

        self.mod.add(SpellData(
            name,
            SpellType="Target",
            using="Target_Smite_Thunderous",
            HitCosts=["SpellSlotsGroup:1:1:1"],
        ))

        for level in range(2, 10):
            self.mod.add(SpellData(
                f"{name}_{level}",
                SpellType="Target",
                using=f"Target_Smite_Thunderous_{level}",
                HitCosts=[f"SpellSlotsGroup:1:1:{level}"],
                RootSpellID=name,
            ))

        return name

    @cached_property
    def _wrathful_smite(self) -> str:
        """Add the Wrathful Smite spell without the concentration or bonus action cost."""
        name = f"{self.mod.get_prefix()}_WrathfulSmite"

        self.mod.add(SpellData(
            name,
            SpellType="Target",
            using="Target_Smite_Wrathful",
            HitCosts=["SpellSlotsGroup:1:1:1"],
            SpellFlags=["HasVerbalComponent", "IsHarmful", "IsMelee", "IsSpell"],
        ))

        for level in range(2, 10):
            self.mod.add(SpellData(
                f"{name}_{level}",
                SpellType="Target",
                using=f"Target_Smite_Wrathful_{level}",
                HitCosts=[f"SpellSlotsGroup:1:1:{level}"],
                RootSpellID=name,
                SpellFlags=["HasVerbalComponent", "IsHarmful", "IsMelee", "IsSpell"],
            ))

        return name

    @cached_property
    def _spells_level_1(self) -> str:
        name = "Sorcadin spells gained at level 1"
        spells = SpellList(
            Name=name,
            Spells=[
                Bolster(self.mod).add_bolster(),
                "Target_Command_Container",
                "Target_Guidance",
                "Target_HealingWord",
                "Target_Resistance",
            ],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return spells.UUID

    @cached_property
    def _spells_level_2(self) -> str:
        name = "Sorcadin spells gained at level 2"
        spells = SpellList(
            Name=name,
            Spells=[
                "Target_Smite_Divine",
                "Target_Smite_Divine_Unlock",
                "Target_Smite_Divine_Critical_Unlock",
                self._searing_smite,
                self._thunderous_smite,
                self._wrathful_smite,
            ],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return spells.UUID

    @class_description
    def sorcerer_class_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6

    @progression(CharacterClass.SORCERER, 1)
    def sorcerer_level_1(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{2 * self.args.spells},1)",
            "ProficiencyBonus(SavingThrow,Constitution)",
            "ProficiencyBonus(SavingThrow,Wisdom)",
            "ProficiencyBonus(SavingThrow,Charisma)",
            "Proficiency(LightArmor)",
            "Proficiency(MediumArmor)",
            "Proficiency(HeavyArmor)",
            "Proficiency(Shields)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
        ]
        progress.PassivesAdded += [
            Awareness(self.mod).add_awareness(5),
            BattleMagic(self.mod).add_battle_magic(),
            PackMule(self.mod).add_pack_mule(5.0),
            Defense(self.mod).add_warding(),
        ]
        progress.Selectors += [f"AddSpells({self._spells_level_1})"]

    @progression(CharacterClass.SORCERER, 2)
    def sorcerer_level_2(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            "DevilsSight",
            "SculptSpells",
            "Smite_Divine",
            self._fast_movement_30,
        ]
        progress.Selectors += [f"AddSpells({self._spells_level_2})"]

    @progression(CharacterClass.SORCERER, 3)
    def sorcerer_level_3(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1,true)",
        ]

    @progression(CharacterClass.SORCERER, 4)
    def sorcerer_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 5)
    def sorcerer_level_5(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 6)
    def sorcerer_level_6(self, progress: Progression) -> None:
        progress.PassivesAdded = ["PotentCantrip"]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1,true)",
        ]

    @progression(CharacterClass.SORCERER, 7)
    def sorcerer_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_45]
        progress.PassivesRemoved = [self._fast_movement_30]

    @progression(CharacterClass.SORCERER, 8)
    def sorcerer_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 9)
    def sorcerer_level_9(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1,true)",
        ]

    @progression(CharacterClass.SORCERER, 10)
    def sorcerer_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 11)
    def sorcerer_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2", "ReliableTalent"]
        progress.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.SORCERER, 12)
    def sorcerer_level_12(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_60]
        progress.PassivesRemoved = [self._fast_movement_45]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1,true)",
        ]

    @progression(CharacterClass.SORCERER, 13)
    def sorcerer_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 14)
    def sorcerer_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 15)
    def sorcerer_level_15(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1,true)",
        ]

    @progression(CharacterClass.SORCERER, 16)
    def sorcerer_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 17)
    def sorcerer_level_17(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_75]
        progress.PassivesRemoved = [self._fast_movement_60]

    @progression(CharacterClass.SORCERER, 18)
    def sorcerer_level_18(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1,true)",
        ]

    @progression(CharacterClass.SORCERER, 19)
    def sorcerer_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 20)
    def sorcerer_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded += ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]


def main() -> None:
    sorcadin = Sorcadin(
        classes=[
            CharacterClass.SORCERER
        ],
        feats=2,
        spells=2,
        warlock_spells=2,
        actions=2,
        skills=4,
        expertise=2,
        full_caster=False,
    )
    sorcadin.build()


if __name__ == "__main__":
    main()
