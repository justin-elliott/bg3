#!/usr/bin/env python3
"""
Generates files for the "EldritchBattlemage" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import Movement, spells_always_prepared
from modtools.gamedata import PassiveData, SpellData, StatusData
from modtools.lsx.game import (
    CharacterAbility,
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


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4fh7.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class EldritchBattlemage(Replacer):
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
    def _war_magic(self) -> str:
        """Add the War Magic passive, returning its name."""
        name = f"{self._mod.get_prefix()}_WarMagic"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "War Magic"}
        loca[f"{name}_Description"] = {"en": """
            After making a weapon or unarmed attack, you can cast a cantrip as a
            <LSTag Type="ActionResource" Tooltip="BonusActionPoint">bonus action</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_WarMagic",
            Properties=["Highlighted", "OncePerTurn"],
            StatsFunctorContext="OnAttack",
            Conditions="IsWeaponAttack() or IsUnarmedAttack()",
            StatsFunctors=f"ApplyStatus(SELF,{name.upper()},100,1)"
        ))

        self._mod.add(StatusData(
            name.upper(),
            StatusType="BOOST",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_WarMagic",
            Boosts=[
                "UnlockSpellVariant(QuickenedCantripCheck(),ModifyUseCosts(Replace,BonusActionPoint,1,0,ActionPoint),"
                + "ModifyIconGlow(),ModifyTooltipDescription())",
                "UnlockSpellVariant(RangedSpellAttackCheck(),ModifySpellRoll('AttackType.RangedSpellAttack',"
                + "'AttackType.MeleeSpellAttack'))"
            ],
            RemoveConditions="IsSpell()",
            RemoveEvents="OnSpellCast",
            StackId=name.upper(),
            StatusPropertyFlags=[
                "DisableOverhead",
                "DisableCombatlog",
                "DisablePortraitIndicator",
            ],
        ))

        return name

    @cached_property
    def _improved_war_magic(self) -> str:
        """Add the War Magic passive, returning its name."""
        name = f"{self._mod.get_prefix()}_ImprovedWarMagic"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Improved War Magic"}
        loca[f"{name}_Description"] = {"en": """
            After making a weapon or unarmed attack, you can cast a spell as a
            <LSTag Type="ActionResource" Tooltip="BonusActionPoint">bonus action</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            using=self._war_magic,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            StatsFunctors=f"ApplyStatus(SELF,{name.upper()},100,1)"
        ))

        self._mod.add(StatusData(
            name.upper(),
            using=self._war_magic.upper(),
            StatusType="BOOST",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Boosts=[
                "UnlockSpellVariant(QuickenedSpellCheck(),ModifyUseCosts(Replace,BonusActionPoint,1,0,ActionPoint),"
                + "ModifyIconGlow(),ModifyTooltipDescription())",
                "UnlockSpellVariant(RangedSpellAttackCheck(),ModifySpellRoll('AttackType.RangedSpellAttack',"
                + "'AttackType.MeleeSpellAttack'))"
            ],
        ))

        return name

    def _dual_weapon_bond(self) -> None:
        weapon_bond_offhand = f"{self.mod.get_prefix()}_WEAPON_BOND_OFFHAND"

        self.mod.add(SpellData(
            "Shout_WeaponBond",
            using="Shout_WeaponBond",
            SpellType="Shout",
            SpellProperties=[
                "ApplyEquipmentStatus(MainHand,WEAPON_BOND,100,-1)",
                f"ApplyEquipmentStatus(OffHand,{weapon_bond_offhand},100,-1)",
            ],
        ))

        self.mod.add(StatusData(
            weapon_bond_offhand,
            using="WEAPON_BOND",
            StatusType="BOOST",
            StackId=weapon_bond_offhand,
        ))

    @cached_property
    def _level_3_spell_list(self) -> SpellList:
        spells = SpellList(
            Comment="Eldritch Knight level 3 abilities",
            Spells=[
                "Projectile_EldritchBlast",
            ],
            UUID=self.make_uuid("Eldritch Knight level 3 abilities"),
        )
        self.mod.add(spells)
        return spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="EldritchBattlemage",
                         description="Enhancements for the Eldritch Knight subclass.")

        self._args = args

        if len(args.feats) == 0:
            self._feat_levels = frozenset([4, 6, 8, 12, 16, 19])
        elif len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            self._feat_levels = frozenset(
                {*range(max(feat_level, 2), 20, feat_level)} | ({19} if 20 % feat_level == 0 else {}))
        else:
            self._feat_levels = args.feats - frozenset([1])

        self._dual_weapon_bond()

    @class_description(CharacterClass.FIGHTER)
    def fighter_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.MustPrepareSpells = True
        class_description.SpellCastingAbility = CharacterAbility.CHARISMA

    @class_description(CharacterClass.FIGHTER_ELDRITCHKNIGHT)
    def eldritch_knight_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.MustPrepareSpells = True
        class_description.SpellCastingAbility = CharacterAbility.CHARISMA
        class_description.SpellList = "beb9389e-24f8-49b0-86a5-e8d08b6fdc2e"

    @progression(CharacterClass.FIGHTER, range(2, 21))
    @only_existing_progressions
    def level_2_to_20_fighter(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None

    @progression(CharacterClass.FIGHTER, range(1, 21))
    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, range(1, 21))
    @progression(CharacterClass.FIGHTER, 1, is_multiclass=True)
    @only_existing_progressions
    def level_1_to_20_fighter(self, progression: Progression) -> None:
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
            and not selector.startswith(f"SelectSpells({wizard_level_3_spells(self).UUID}")
            and not selector.startswith(f"SelectSpells({wizard_level_4_spells(self).UUID}")
        ] or None

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{4 * self._args.spells},1)",
            f"ActionResource(SpellSlot,{2 * self._args.spells},2)",
            "Tag(WIZARD)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "AgonizingBlast",
            "SculptSpells",
            "UnlockedSpellSlotLevel1",
            "UnlockedSpellSlotLevel2",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_3_spell_list.UUID},,,,AlwaysPrepared)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,18)",
            f"SelectSpells({wizard_cantrips(self).UUID},3,0,,,,AlwaysPrepared)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},6,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},2)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "DevilsSight",
            "ImprovedCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,18)",
            f"SelectSpells({wizard_level_2_spells(self).UUID},2,0)",
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
            f"SelectSpells({wizard_level_3_spells(self).UUID},2,0)",
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
            f"SelectSpells({wizard_level_3_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]
        passives_added = [passive for passive in progression.PassivesAdded if passive != "WarMagic"]
        progression.PassivesAdded = passives_added + [
            "Evasion",
            "RemarkableAthlete_Jump",
            "RemarkableAthlete_Proficiency",
            self._remarkable_athlete_run,
            self._war_magic,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_4_spells(self).UUID},2,0)",
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
            f"SelectSpells({wizard_level_4_spells(self).UUID},2,0)",
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
            f"SelectSpells({wizard_level_5_spells(self).UUID},2,0)",
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
            f"SelectSpells({wizard_level_5_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ReliableTalent",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 13)
    def level_13(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},7)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 14)
    def level_14(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 15)
    def level_15(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},8)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 16)
    def level_16(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 17)
    def level_17(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},9)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 18)
    def level_18(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        passives_added = [passive for passive in progression.PassivesAdded if passive != "WarMagicImproved"]
        progression.PassivesAdded = passives_added + [
            self._improved_war_magic,
        ]
        passives_removed = [passive for passive in progression.PassivesRemoved if passive != "WarMagic"]
        progression.PassivesRemoved = passives_removed + [
            self._war_magic,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 19)
    def level_19(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]

    @progression(CharacterClass.FIGHTER_ELDRITCHKNIGHT, 20)
    def level_20(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},7)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({wizard_level_6_spells(self).UUID},2,0)",
        ]


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 12))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="Enhancements for the Ranger class.")
    parser.add_argument("-f", "--feats", type=level_list, default=frozenset([2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 19]),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    args = EldritchBattlemage.Args(**vars(parser.parse_args()))

    eldritch_battlemage = EldritchBattlemage(args)
    eldritch_battlemage.build()


if __name__ == "__main__":
    main()
