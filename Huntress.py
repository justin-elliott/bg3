
import os

from modtools.lsx.game import (
    ClassDescription,
    Progression,
)
from modtools.replacers import (
    CharacterClass,
    class_description,
    DontIncludeProgression,
    progression,
    Replacer,
)


class Huntress(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Huntress",
                         description="A class replacer for Champion.",
                         **kwds)

    @class_description(CharacterClass.FIGHTER_CHAMPION)
    def huntress_description(self, class_description: ClassDescription) -> None:
        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.children += [
            ClassDescription.Tags(Object="37a733c1-a862-4157-b92a-9cff46232c6a"),  # RANGER
            ClassDescription.Tags(Object="5727fd64-090f-4932-a31c-c0e078b2146a"),  # RANGER_HUNTER
            ClassDescription.Tags(Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"),  # WIZARD
        ]

    @progression(CharacterClass.FIGHTER_CHAMPION, 1)
    def huntress_level_1(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 2)
    def huntress_level_2(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 3)
    def huntress_level_3(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 4)
    def huntress_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 5)
    def huntress_level_5(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 6)
    def huntress_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 7)
    def huntress_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 8)
    def huntress_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 9)
    def huntress_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 10)
    def huntress_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 11)
    def huntress_level_11(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 12)
    def huntress_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 13)
    def huntress_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 14)
    def huntress_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 15)
    def huntress_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 16)
    def huntress_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 17)
    def huntress_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 18)
    def huntress_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 19)
    def huntress_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.FIGHTER_CHAMPION, 20)
    def huntress_level_20(self, _: Progression) -> None:
        raise DontIncludeProgression()


def main() -> None:
    huntress = Huntress(
        classes=[CharacterClass.FIGHTER_CHAMPION],
        spells=2,
        actions=2,
        full_caster=True,
    )
    huntress.build()


if __name__ == "__main__":
    main()
