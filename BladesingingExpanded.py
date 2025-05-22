
import os

from modtools.lsx.game import Dependencies, Progression
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class BladesingingExpanded(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="BladesingingExpanded",
                         description="A class replacer for BladesingingSchool.",
                         **kwds)

    @progression(CharacterClass.WIZARD_BLADESINGING, 2)
    def wizard_bladesinging_level_2(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 3)
    def wizard_bladesinging_level_3(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 4)
    def wizard_bladesinging_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 5)
    def wizard_bladesinging_level_5(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 6)
    def wizard_bladesinging_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 7)
    def wizard_bladesinging_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 8)
    def wizard_bladesinging_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 9)
    def wizard_bladesinging_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 10)
    def wizard_bladesinging_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 11)
    def wizard_bladesinging_level_11(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 12)
    def wizard_bladesinging_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 13)
    def wizard_bladesinging_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 14)
    def wizard_bladesinging_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 15)
    def wizard_bladesinging_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 16)
    def wizard_bladesinging_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 17)
    def wizard_bladesinging_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 18)
    def wizard_bladesinging_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 19)
    def wizard_bladesinging_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WIZARD_BLADESINGING, 20)
    def wizard_bladesinging_level_20(self, _: Progression) -> None:
        raise DontIncludeProgression()


def main() -> None:
    bladesinging_expanded = BladesingingExpanded(
        classes=[
            CharacterClass.WIZARD_BLADESINGING
        ],
        feats=2,
        spells=2,
        warlock_spells=1,
        actions=2,
        skills=4,
        expertise=2,
    )
    bladesinging_expanded.build()


if __name__ == "__main__":
    main()
