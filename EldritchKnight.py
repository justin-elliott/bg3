#!/usr/bin/env python3
"""
Generates files for the "EldritchKnight" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    ActionResource,
    Attack,
    BattleMagic,
    Movement,
    PackMule,
    multiply_resources,
    spells_always_prepared,
)
from modtools.gamedata import SpellData
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


class EldritchKnight(Replacer):
    @dataclass
    class Args:
        feats: set[int]  # Feat improvement levels
        spells: int      # Multiplier for spell slots

    _args: Args
    _feat_levels: set[int]

    @cached_property
    def _remarkable_athlete_run(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_RemarkableAthlete_Run"
        loca[name] = {"en": "Remarkable Athlete: Run"}
        return Movement(self.mod).add_fast_movement(3.0, loca[name])

    @cached_property
    def _mighty_throw_spell(self) -> str:
        loca = self.mod.get_localization()

        name = f"{self._mod.get_prefix()}_MightyThrow"
        loca[name] = {"en": "Mighty Throw"}

        self.mod.add(SpellData(
            name,
            using="Throw_FrenziedThrow",
            SpellType="Throw",
            DisplayName=loca[name],
            RequirementConditions=[],
        ))

        return name

    @cached_property
    def _level_3_spell_list(self) -> SpellList:
        spells = SpellList(
            Comment="Eldritch Knight level 3 abilities",
            Spells=[
                "Projectile_EldritchBlast",
                Attack(self.mod).add_brutal_cleave(),
                self._mighty_throw_spell,
            ],
            UUID=self.make_uuid("Eldritch Knight level 3 abilities"),
        )
        self.mod.add(spells)
        return spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="EldritchKnight",
                         description="Enhancements for the Eldritch Knight subclass.")

        self._args = args

        if len(args.feats) == 0:
            self._feat_levels = frozenset([4, 6, 8, 12])
        elif len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            self._feat_levels = frozenset(range(max(feat_level, 2), 13, feat_level))
        else:
            self._feat_levels = args.feats - frozenset([1])

    @class_description(CharacterClass.FIGHTER)
    @class_description(CharacterClass.FIGHTER_ELDRITCHKNIGHT)
    def ranger_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.MustPrepareSpells = True

    @progression(CharacterClass.FIGHTER, range(1, 13))
    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, range(1, 13))
    @progression(CharacterClass.FIGHTER, 1, is_multiclass=True)
    @only_existing_progressions
    def level_1_to_12_ranger(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        spells_always_prepared(progression)
        progression.Boosts = [
            boost for boost in (progression.Boosts or []) if not boost.startswith("ActionResource(SpellSlot,")
        ]
        progression.PassivesAdded = [
            passive for passive in (progression.PassivesAdded or []) if not passive.startswith("UnlockedSpellSlotLevel")
        ]
        progression.Selectors = [
            selector for selector in (progression.Selectors or [])
            if not selector.startswith(f"SelectSpells({eldritch_knight_cantrips(self).UUID}")
            and not selector.startswith(f"SelectSpells({eldritch_knight_level_1_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({eldritch_knight_level_2_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_cantrips(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_1_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_2_spells(self).UUID}")
        ] or None

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{4 * self._args.spells},1)",
            f"ActionResource(SpellSlot,{2 * self._args.spells},2)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            BattleMagic(self.mod).add_battle_magic(),
            PackMule(self.mod).add_pack_mule(5.0),
            self._remarkable_athlete_run,
            "SculptSpells",
            "UnlockedSpellSlotLevel1",
            "UnlockedSpellSlotLevel2",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_3_spell_list.UUID},,,,AlwaysPrepared)",
            "SelectAbilities(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,4,2,FeatASI)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            f"SelectSpells({wizard_cantrips(self).UUID},3,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},2)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "FeralInstinct",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{2 * self._args.spells},3)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "UncannyDodge",
            "UnlockedSpellSlotLevel3",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectAbilities(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,4,2,FeatASI)",
            f"SelectSpells({wizard_level_3_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},3)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "PotentCantrip",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_3_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Evasion",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectAbilities(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,4,2,FeatASI)",
            f"SelectSpells({wizard_level_4_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "BrutalCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectAbilities(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,4,2,FeatASI)",
            f"SelectSpells({wizard_level_5_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "EmpoweredEvocation",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_5_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
            "SelectAbilities(b9149c8e-52c8-46e5-9cb6-fc39301c05fe,4,2,FeatASI)",
            f"SelectSpells({wizard_level_6_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ReliableTalent",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},3,0,,,,AlwaysPrepared)",
        ]


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 12))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="Enhancements for the Ranger class.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to normal progression)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    args = EldritchKnight.Args(**vars(parser.parse_args()))

    eldritch_knight = EldritchKnight(args)
    eldritch_knight.build()


if __name__ == "__main__":
    main()