#!/usr/bin/env python3

import os

from functools import cache, cached_property
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
    warlock_cantrips,
    warlock_combined_spells,
)

class ActuallyEldritchKnight(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="ActuallyEldritchKnight",
                         description="A class replacer for EldritchKnight.",
                         **kwds)

    @cached_property
    def __warlock_cantrips(self) -> str:
        return warlock_cantrips(self).UUID

    @cache
    def __warlock_spells(self, level: int) -> str:
        name = f"Actually Eldritch Knight Level {level} spells"
        uuid = self.make_uuid(name)
        self.mod.add(SpellList(
            Name=name,
            Spells=warlock_combined_spells(self, level),
            UUID=uuid,
        ))
        return uuid

    @class_description(CharacterClass.FIGHTER_ELDRITCHKNIGHT)
    def eldritchknight_description(self, class_description: ClassDescription) -> None:
        class_description.MulticlassSpellcasterModifier = None
        class_description.SpellCastingAbility = CharacterAbility.CHARISMA

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 3)
    def eldritchknight_level_3(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(WarlockSpellSlot,{self.args.warlock_spells},1)"]
        progress.PassivesAdded = ["UnlockedWarlockSpellSlotLevel1"]
        progress.Selectors = [
            "AddSpells(42c2f7ed-8d06-4347-a912-01172a0e318b,,,,AlwaysPrepared)",  # Weapon Bond
            f"SelectSpells({self.__warlock_cantrips},2,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.__warlock_spells(1)},2,0,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 4)
    def eldritchknight_level_4(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(1)},0,1,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 5)
    def eldritchknight_level_5(self, progress: Progression) -> None:
        progress.Boosts = [f"ActionResource(WarlockSpellSlot,{self.args.warlock_spells},1)"]
        progress.Selectors = [
            "SelectPassives(333fb1b0-9398-4ca8-953e-6c0f9a59bbed,2,WarlockInvocations)",
            f"SelectSpells({self.__warlock_spells(1)},1,2,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 6)
    def eldritchknight_level_6(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(1)},0,1,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 7)
    def eldritchknight_level_7(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(WarlockSpellSlot,{2 * self.args.warlock_spells},2)",
            "ActionResourceOverride(WarlockSpellSlot,0,1)",
        ]
        progress.PassivesAdded = ["WarMagic", "UnlockedWarlockSpellSlotLevel2"]
        progress.Selectors = [
            f"SelectSpells({self.__warlock_cantrips},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.__warlock_spells(2)},1,0,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 8)
    def eldritchknight_level_8(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(2)},0,1,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 9)
    def eldritchknight_level_9(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectPassives(8adab8f9-e360-4f79-851b-2c7e050ca23d,1,WarlockInvocations)",
            f"SelectSpells({self.__warlock_spells(2)},1,0,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 10)
    def eldritchknight_level_10(self, progress: Progression) -> None:
        progress.PassivesAdded = ["EldritchStrike"]
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(2)},0,1,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 11)
    def eldritchknight_level_11(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(WarlockSpellSlot,{2 * self.args.warlock_spells},3)",
            "ActionResourceOverride(WarlockSpellSlot,0,2)",
        ]
        progress.PassivesAdded = ["UnlockedWarlockSpellSlotLevel3"]
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(3)},1,0,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 12)
    def eldritchknight_level_12(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(3)},0,1,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 13)
    def eldritchknight_level_13(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectPassives(39efef92-9987-46e2-8c43-54052c1be535,1,WarlockInvocations)",
            f"SelectSpells({self.__warlock_spells(3)},1,0,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 14)
    def eldritchknight_level_14(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(3)},0,1,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 15)
    def eldritchknight_level_15(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(WarlockSpellSlot,{2 * self.args.warlock_spells},4)",
            "ActionResourceOverride(WarlockSpellSlot,0,3)",
        ]
        progress.Selectors = [
            f"SelectSpells({self.__warlock_cantrips},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.__warlock_spells(4)},1,0,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 16)
    def eldritchknight_level_16(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(4)},0,1,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 17)
    def eldritchknight_level_17(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectPassives(a2d72748-0792-4f1e-a798-713a66d648eb,1,WarlockInvocations)",
            f"SelectSpells({self.__warlock_spells(4)},1,0,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 18)
    def eldritchknight_level_18(self, progress: Progression) -> None:
        progress.PassivesAdded = ["WarMagicImproved"]
        progress.PassivesRemoved = ["WarMagic"]
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(4)},0,1,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 19)
    def eldritchknight_level_19(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(WarlockSpellSlot,{3 * self.args.warlock_spells},5)",
            "ActionResourceOverride(WarlockSpellSlot,0,4)",
        ]
        progress.Selectors = [
            f"SelectSpells({self.__warlock_spells(5)},1,0,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 20)
    def eldritchknight_level_20(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectPassives(ab56f79f-95ec-48e5-bd83-e80ba9afc844,1,WarlockInvocations)",
            f"SelectSpells({self.__warlock_spells(5)},0,1,,,e9127b70-22b7-42a1-b172-d02f828f260a)",
        ]


def main() -> None:
    actually_eldritch_knight = ActuallyEldritchKnight(
        classes=[CharacterClass.FIGHTER_ELDRITCHKNIGHT],
        warlock_spells=2,
        actions=2,
    )
    actually_eldritch_knight.build()


if __name__ == "__main__":
    main()
