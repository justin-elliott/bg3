#!/usr/bin/env python3
"""
Generates files for the "HexbladeExtended" mod.
"""

import argparse
import os
import re

from dataclasses import dataclass
from functools import cache, cached_property
from moddb import (
    BattleMagic,
    Bolster,
    EmpoweredSpells,
    multiply_resources,
    PackMule,
    spells_always_prepared,
)
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    ClassDescription,
    SpellList,
)
from modtools.lsx.game import Dependencies, Progression
from modtools.replacers import (
    Replacer,
    class_description,
    progression,
)
from uuid import UUID


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class HexbladeExtended(Replacer):
    @dataclass
    class Args:
        feats: int   # Feats every n levels
        spells: int  # Multiplier for spell slots

    _REQ_ARG = r"(?:,([^,)]+))"
    _OPT_ARG = r"(?:,([^,)]*))?"
    _SELECT_SPELLS = re.compile(r"SelectSpells\(([^,)]+)" + _OPT_ARG * 4 + _REQ_ARG + r"\)")

    _args: Args
    _feat_levels: set[int]

    # Passives
    _battle_magic: str
    _empowered_spells: str
    _pack_mule: str

    # Spells
    _bolster: str

    @cached_property
    def _eldritch_strike(self) -> str:
        """Adds the Eldritch Strike spell."""
        name = f"{self.mod.get_prefix()}_EldritchStrike"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Eldritch Strike"}
        loca[f"{name}_Description"] = {"en": """
            Strike with your melee weapon, empowering the blow with eldritch force.
            """}

        self.mod.add(SpellData(
            name,
            using="Target_MainHandAttack",
            SpellType="Target",
            Level=1,
            SpellProperties=[
                "GROUND:DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "GROUND:ExecuteWeaponFunctors(MainHand)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
                "GROUND:DealDamage(1d8,Force)",
            ],
            SpellRoll="Attack(AttackType.MeleeWeaponAttack)",
            SpellSuccess=[
                "DealDamage(MainMeleeWeapon, MainMeleeWeaponDamageType)",
                "ExecuteWeaponFunctors(MainHand)",
                "DealDamage(1d8,Force,Magical)",
            ],
            TargetConditions="not Self()",
            Icon="Action_Charger_Attack",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            TooltipDamageList=[
                "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "DealDamage(1d8,Force)",
            ],
            TooltipOnMiss="4639a885-0f45-4bc9-93c7-1e0c39eb39ec",
            TooltipUpcastDescription="66388a6f-44dd-4c9f-a9e7-910c50e70755",
            TooltipUpcastDescriptionParams="DealDamage(1d8,Force)",
            CastSound="Spell_Cast_Damage_Thunder_ThunderousSmite_L1to3",
            TargetSound="Spell_Impact_Damage_Thunder_ThunderousSmite_L1to3",
            HitCosts="SpellSlotsGroup:1:1:1",
            SpellAnimation=[
                "71369b20-18f1-4d33-89ad-a99b10f0444c,,;48beee2b-7124-4fa1-b820-dab4d89198d4,,;bcecc5ce-e7c9-4391-b4b6-5f93872ba2e6,,;9add032c-e500-4e88-a2ea-ef6c905bd656,,;3b9da8d4-3eff-43bd-9eaa-1c13fba0045e,,;d9feef5a-3726-4e23-95e5-6ec295efdc96,,;0b07883a-08b8-43b6-ac18-84dc9e84ff50,,;,,;,,",
            ],
            DualWieldingSpellAnimation=[
                "71369b20-18f1-4d33-89ad-a99b10f0444c,,;48beee2b-7124-4fa1-b820-dab4d89198d4,,;bcecc5ce-e7c9-4391-b4b6-5f93872ba2e6,,;9add032c-e500-4e88-a2ea-ef6c905bd656,,;3b9da8d4-3eff-43bd-9eaa-1c13fba0045e,,;d9feef5a-3726-4e23-95e5-6ec295efdc96,,;0b07883a-08b8-43b6-ac18-84dc9e84ff50,,;,,;,,",
            ],
            VerbalIntent="Damage",
            SpellStyleGroup="Class",
            SpellFlags=["IsMelee", "IsHarmful"],
            HitAnimationType="MagicalDamage_Electric",
            PrepareEffect="3dd8cb62-d04e-449c-bd94-ed59f472ec5a",
            CastEffect="da03ffe6-2e75-4070-be9d-a637666f2e9e",
            TargetEffect="288e0f80-7d7c-4f36-b748-17182318180e",
            DamageType="Force",
        ))

        for spell_level in range(2, 7):
            self._mod.add(SpellData(
                f"{name}_{spell_level}",
                using=name,
                SpellType="Target",
                SpellProperties=[
                    "GROUND:DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                    "GROUND:ExecuteWeaponFunctors(MainHand)",
                    "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
                    f"GROUND:DealDamage({spell_level}d8,Force)",
                ],
                SpellSuccess=[
                    "DealDamage(MainMeleeWeapon, MainMeleeWeaponDamageType)",
                    "ExecuteWeaponFunctors(MainHand)",
                    f"DealDamage({spell_level}d8,Force,Magical)",
                ],
                TooltipDamageList=[
                    "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                    "DealDamage(1d8,Force)",
                ],
                HitCosts=f"SpellSlotsGroup:1:1:{spell_level}",
                RootSpellID=name,
                PowerLevel=spell_level,
            ))

        return name

    def _select_to_add_spells(self, progression: Progression) -> bool:
        """Change spell selection to adding the entire spell list."""
        was_updated = False

        if progression.Selectors:
            selectors = []
            for selector in progression.Selectors:
                if match := self._SELECT_SPELLS.match(selector):
                    args = match.groups("")
                    selector = f"AddSpells({args[0]})"
                    was_updated = True
                if progression.Level % 2 == 1 and progression.Level < 10:
                    selectors.append(selector)
            progression.Selectors = selectors or None

        return was_updated

    @cached_property
    def _level_1_spells_always_prepared(self) -> str:
        spell_list = str(self.make_uuid("level_1_spells_always_prepared"))
        self.mod.add(SpellList(
            Comment="Hexblade Extended level 1 spells that are always prepared",
            Spells=[self._bolster, self._eldritch_strike],
            UUID=spell_list,
        ))
        return spell_list

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="HexbladeExtended",
                         description="Enhancements for the Warlock Hexblade subclass.")

        self.mod.add(Dependencies.ShortModuleDesc(
            Folder="UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            MD5="f94d034502139cf8b65a1597554e7236",
            Name="UnlockLevelCurve",
            PublishHandle=4166963,
            UUID="a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            Version64=72057594037927960,
        ))

        self._args = args

        if len(args.feats) == 0:
            self._feat_levels = frozenset({*range(2, 20, 2)} | {19})
        elif len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            self._feat_levels = frozenset(
                {*range(max(feat_level, 2), 20, feat_level)} | ({19} if 20 % feat_level == 0 else {}))
        else:
            self._feat_levels = args.feats - frozenset([1])

        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.CHARISMA)
        self._bolster = Bolster(self.mod).add_bolster()
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)

    @class_description(CharacterClass.WARLOCK)
    def warlock_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6
        class_description.CanLearnSpells = True
        class_description.MustPrepareSpells = True

    @class_description(CharacterClass.WARLOCK_HEXBLADE)
    def warlock_hexblade_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.MustPrepareSpells = True

    @class_description(CharacterClass.WARLOCK_ARCHFEY)
    @class_description(CharacterClass.WARLOCK_FIEND)
    @class_description(CharacterClass.WARLOCK_GREATOLDONE)
    def warlock_other_descriptions(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = False
        class_description.MustPrepareSpells = False

    @progression(CharacterClass.WARLOCK, range(1, 21))
    @progression(CharacterClass.WARLOCK, 1, is_multiclass=True)
    def level_1_to_20_warlock(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.WARLOCK_SPELL_SLOTS], self._args.spells)

    @progression(CharacterClass.WARLOCK, range(1, 21))
    @progression(CharacterClass.WARLOCK_HEXBLADE, range(1, 21))
    @progression(CharacterClass.WARLOCK, 1, is_multiclass=True)
    def level_1_to_20_prepared(self, progression: Progression) -> None:
        spells_always_prepared(progression)

    @progression(CharacterClass.WARLOCK_HEXBLADE, range(1, 21))
    def level_1_to_20_select_to_add(self, progression: Progression) -> None:
        self._select_to_add_spells(progression)

    @progression(CharacterClass.WARLOCK_HEXBLADE, 1)
    def level_1(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            self._battle_magic,
            self._pack_mule,
        ]
        progression.Selectors = progression.Selectors + [
            f"AddSpells({self._level_1_spells_always_prepared},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 2)
    def level_2(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,14)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,18)",
        ]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 4)
    def level_4(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 5)
    def level_5(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 6)
    def level_6(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 7)
    def level_7(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 8)
    def level_8(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._empowered_spells]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 10)
    def level_10(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 11)
    def level_11(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 12)
    def level_12(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 13)
    def level_13(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 14)
    def level_14(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 15)
    def level_15(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 16)
    def level_16(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 17)
    def level_17(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 18)
    def level_18(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 19)
    def level_19(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK_HEXBLADE, 20)
    def level_20(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.WARLOCK, 11)
    def upgrade_to_level_6_spell_slots(self, progression: Progression) -> None:
        progression.Boosts = [
            f"ActionResource(WarlockSpellSlot,{3 * self._args.spells},6)",
            "ActionResourceOverride(WarlockSpellSlot,0,5)"
        ]
    
    @progression(CharacterClass.WARLOCK, [11, 13, 15, 17])
    def remove_mystic_arcanum(self, progression: Progression) -> None:
        progression.Selectors = [
            selector for selector in progression.Selectors if not selector.startswith("SelectSpells(")
        ] or None


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="Enhancements for the Warlock Hexblade subclass.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 17), default=8,
                        help="Spell slot multiplier (defaulting to 8; octuple spell slots)")
    args = HexbladeExtended.Args(**vars(parser.parse_args()))

    hexblade_extended = HexbladeExtended(args)
    hexblade_extended.build()


if __name__ == "__main__":
    main()
