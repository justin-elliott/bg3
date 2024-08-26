#!/usr/bin/env python3
"""
Generates files for the "EldritchKnight" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    Attack,
    Movement,
    PackMule,
    spells_always_prepared,
)
from modtools.gamedata import PassiveData
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
    def _advancement(self) -> dict[int, str]:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_Advancement"
        loca[f"{name}_DisplayName"] = {"en": "Advancement"}
        loca[f"{name}_Description"] = {"en": """
            Your abilities improve by 2 at Eldritch Knight levels 3, 5, 7, 9, and 11.
            """}

        advancement_names = {}

        for level in [3, 5, 7, 9, 11]:
            advancement_names[level] = f"{name}_{level}"
            self.mod.add(PassiveData(
                advancement_names[level],
                DisplayName=loca[f"{name}_DisplayName"],
                Description=loca[f"{name}_Description"],
                Icon="Spell_Transmutation_EnhanceAbility",
                Properties=["ForceShowInCC", "Highlighted"] if level == 3 else ["IsHidden"],
                Boosts=[
                    "Ability(Strength,2)",
                    "Ability(Dexterity,2)",
                    "Ability(Constitution,2)",
                    "Ability(Intelligence,2)",
                    "Ability(Wisdom,2)",
                    "Ability(Charisma,2)",
                ],
            ))

        return advancement_names

    @cached_property
    def _quickened_spell(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_QuickenedSpell"
        loca[f"{name}_DisplayName"] = {"en": "Eldritch: Quickened Spell"}
        loca[f"{name}_Description"] = {"en": """
            Spells that cost an action cost a bonus action instead.
            """}
        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="Skill_Sorcerer_Passive_Metamagic_QuickenedSpell",
            EnabledContext=["OnCastResolved", "OnLongRest", "OnActionResourcesChanged"],
            Properties=["IsToggled", "ToggledDefaultAddToHotbar"],
            Boosts=[
                "UnlockSpellVariant(QuickenedSpellCheck(),ModifyUseCosts(Replace,BonusActionPoint,1,0,ActionPoint))",
            ],
            ToggleOnEffect="VFX_Spells_Cast_Sorcerer_Metamagic_Quickened_HeadFX_01:Dummy_HeadFX",
            ToggleOffContext="OnCastResolved",
        ))
        return name

    @cached_property
    def _twinned_spell(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_TwinnedSpell"
        loca[f"{name}_DisplayName"] = {"en": "Eldritch: Twinned Spell"}
        loca[f"{name}_Description"] = {"en": """
            Spells that only target 1 creature can target an additional creature.
            """}
        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            ExtraDescription="h7f172d6cg6359g4158gb711gcd159662cc53;1",
            ExtraDescriptionParams="Distance(1.5)",
            Icon="Skill_Sorcerer_Passive_Metamagic_TwinnedSpell",
            EnabledContext=["OnCastResolved", "OnLongRest", "OnActionResourcesChanged"],
            Properties=["IsToggled", "ToggledDefaultAddToHotbar"],
            Boosts=[
                "UnlockSpellVariant(TwinnedProjectileSpellCheck(),ModifyNumberOfTargets(AdditiveBase,1,false))",
                "UnlockSpellVariant(TwinnedTargetSpellCheck(),ModifyNumberOfTargets(AdditiveBase,1,false))",
                "UnlockSpellVariant(TwinnedTargetTouchSpellCheck(),ModifyNumberOfTargets(AdditiveBase,1,false))",
            ],
            ToggleOnEffect="VFX_Spells_Cast_Sorcerer_Metamagic_Twinned_HeadFX_01:Dummy_HeadFX",
            ToggleOffContext="OnCastResolved",
        ))
        return name

    @cached_property
    def _level_3_spell_list(self) -> SpellList:
        spells = SpellList(
            Comment="Eldritch Knight level 3 abilities",
            Spells=[
                Attack(self.mod).add_brutal_cleave(),
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
    def fighter_description(self, class_description: ClassDescription) -> None:
        class_description.MustPrepareSpells = True
        class_description.SpellCastingAbility = 4

    @class_description(CharacterClass.FIGHTER_ELDRITCHKNIGHT)
    def eldritch_knight_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.MustPrepareSpells = True
        class_description.SpellList = "beb9389e-24f8-49b0-86a5-e8d08b6fdc2e"

    @progression(CharacterClass.FIGHTER, range(1, 13))
    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, range(1, 13))
    @progression(CharacterClass.FIGHTER, 1, is_multiclass=True)
    @only_existing_progressions
    def level_1_to_12_fighter(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        spells_always_prepared(progression)
        progression.Boosts = [
            boost for boost in (progression.Boosts or []) if not boost.startswith("ActionResource(SpellSlot,")
        ] or None
        progression.PassivesAdded = [
            passive for passive in (progression.PassivesAdded or []) if not passive.startswith("UnlockedSpellSlotLevel")
        ] or None
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
            "Tag(WIZARD)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            PackMule(self.mod).add_pack_mule(5.0),
            self._advancement[3],
            self._quickened_spell,
            self._twinned_spell,
            "SculptSpells",
            "UnlockedSpellSlotLevel1",
            "UnlockedSpellSlotLevel2",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_3_spell_list.UUID},,,,AlwaysPrepared)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            f"SelectSpells({wizard_cantrips(self).UUID},3,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},3,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},2)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "DevilsSight",
            "ImprovedCritical",
            "JackOfAllTrades",
            "FeralInstinct",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},3,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{2 * self._args.spells},3)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._advancement[5],
            "UncannyDodge",
            "UnlockedSpellSlotLevel3",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_3_spells(self).UUID},3,0)",
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
            f"SelectSpells({wizard_level_3_spells(self).UUID},3,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._advancement[7],
            "Evasion",
            "RemarkableAthlete_Jump",
            "RemarkableAthlete_Proficiency",
            self._remarkable_athlete_run,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},3,0)",
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
            "FOR_NightWalkers_WebImmunity",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},3,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._advancement[9],
            "BrutalCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_5_spells(self).UUID},3,0)",
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
            f"SelectSpells({wizard_level_5_spells(self).UUID},3,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._advancement[11],
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
            f"SelectSpells({wizard_level_6_spells(self).UUID},3,0)",
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
            f"SelectSpells({wizard_level_6_spells(self).UUID},3,0)",
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
