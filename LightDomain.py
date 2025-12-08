
from functools import cached_property
import os

from moddb import BattleMagic, Movement
from modtools.lsx.game import (
    Progression,
    SpellList,
)
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class LightDomain(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="LightDomain",
                         description="A class replacer for LightDomain.",
                         **kwds)

    @cached_property
    def _battle_magic(self) -> str:
        return BattleMagic(self.mod).add_battle_magic()

    @cached_property
    def _misty_step(self) -> str:
        return Movement(self.mod).add_misty_step()

    @cached_property
    def _level_5_spell_list(self) -> str:
        name = "Light Domain Cleric Additional Level 5 Spell List"
        uuid = self.make_uuid(name)
        self.mod.add(SpellList(
            Name=name,
            Spells=["Target_Counterspell", self._misty_step],
            UUID=uuid,
        ))
        return uuid

    @progression(CharacterClass.CLERIC_LIGHT, 1)
    def lightdomain_level_1(self, progress: Progression) -> None:
        progress.Boosts = [
            "ProficiencyBonus(SavingThrow,Constitution)",
            "Proficiency(HeavyArmor)",
            "Proficiency(MartialWeapons)",
        ]
        progress.PassivesAdded += [self._battle_magic]

    @progression(CharacterClass.CLERIC_LIGHT, 2)
    def lightdomain_level_2(self, progress: Progression) -> None:
        progress.PassivesAdded = ["SculptSpells"]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.CLERIC_LIGHT, 3)
    def lightdomain_level_3(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 4)
    def lightdomain_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 5)
    def lightdomain_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack"]
        progress.Selectors += [
            f"AddSpells({self._level_5_spell_list},ClericLightDomainSpells,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_LIGHT, 6)
    def lightdomain_level_6(self, progress: Progression) -> None:
        progress.PassivesAdded += ["PotentCantrip"]

    @progression(CharacterClass.CLERIC_LIGHT, 7)
    def lightdomain_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 8)
    def lightdomain_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 9)
    def lightdomain_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 10)
    def lightdomain_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 11)
    def lightdomain_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2"]
        progress.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.CLERIC_LIGHT, 12)
    def lightdomain_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 13)
    def lightdomain_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 14)
    def lightdomain_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 15)
    def lightdomain_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 16)
    def lightdomain_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 17)
    def lightdomain_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 18)
    def lightdomain_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 19)
    def lightdomain_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.CLERIC_LIGHT, 20)
    def lightdomain_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]


def main() -> None:
    light_domain = LightDomain(
        classes=[CharacterClass.CLERIC_LIGHT],
        feats=2,
        spells=2,
        actions=2,
    )
    light_domain.build()


if __name__ == "__main__":
    main()
