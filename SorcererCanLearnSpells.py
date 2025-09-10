
import os

from moddb import spells_always_prepared
from modtools.lsx.game import ClassDescription, Progression
from modtools.replacers import (
    CharacterClass,
    class_description,
    DontIncludeProgression,
    progression,
    Replacer,
)


class SorcererCanLearnSpells(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="SorcererCanLearnSpells",
                         description="A class replacer for Sorcerer.",
                         **kwds)

    @class_description(CharacterClass.SORCERER)
    def sorcerer_can_learn_spells(self, description: ClassDescription) -> None:
        description.CanLearnSpells = True

    @class_description(CharacterClass.SORCERER)
    @class_description(CharacterClass.SORCERER_DRACONIC)
    @class_description(CharacterClass.SORCERER_SHADOWMAGIC)
    @class_description(CharacterClass.SORCERER_STORM)
    @class_description(CharacterClass.SORCERER_WILDMAGIC)
    def sorcerer_must_prepare_spells(self, description: ClassDescription) -> None:
        description.MustPrepareSpells = True

    @progression(CharacterClass.SORCERER, range(1, 21))
    @progression(CharacterClass.SORCERER, 1, is_multiclass=True)
    @progression(CharacterClass.SORCERER_DRACONIC, range(1, 21))
    @progression(CharacterClass.SORCERER_SHADOWMAGIC, range(1, 21))
    @progression(CharacterClass.SORCERER_STORM, range(1, 21))
    @progression(CharacterClass.SORCERER_WILDMAGIC, range(1, 21))
    def sorcerer_spells_always_prepared(self, progression: Progression) -> None:
        if not spells_always_prepared(progression):
            raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 1)
    def sorcerer_level_1(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 2)
    def sorcerer_level_2(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 3)
    def sorcerer_level_3(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 4)
    def sorcerer_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 5)
    def sorcerer_level_5(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 6)
    def sorcerer_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 7)
    def sorcerer_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 8)
    def sorcerer_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 9)
    def sorcerer_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 10)
    def sorcerer_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 11)
    def sorcerer_level_11(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 12)
    def sorcerer_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 13)
    def sorcerer_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 14)
    def sorcerer_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 15)
    def sorcerer_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 16)
    def sorcerer_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 17)
    def sorcerer_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 18)
    def sorcerer_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 19)
    def sorcerer_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER, 20)
    def sorcerer_level_20(self, _: Progression) -> None:
        raise DontIncludeProgression()


def main() -> None:
    sorcerer_can_learn_spells = SorcererCanLearnSpells(
        classes=[CharacterClass.SORCERER],
        feats=2,
        spells=2,
        actions=2,
        skills=4,
        expertise=2,
    )
    sorcerer_can_learn_spells.build()


if __name__ == "__main__":
    main()
