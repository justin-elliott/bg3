#!/usr/bin/env python3
"""
Generates files for the "DaughterOfDarkness" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    BattleMagic,
    CunningActions,
    EmpoweredSpells,
    Movement,
    multiply_resources,
)
from modtools.gamedata import (
    InterruptData,
    PassiveData,
    SpellData,
)
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    LevelMapSeries,
    SpellList,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    cleric_cantrips,
    cleric_level_1_spells,
    cleric_level_2_spells,
    cleric_level_3_spells,
    cleric_level_4_spells,
    cleric_level_5_spells,
    cleric_level_6_spells,
    progression,
    warlock_cantrips,
    warlock_level_1_spells,
    warlock_level_2_spells,
    warlock_level_3_spells,
    warlock_level_4_spells,
    warlock_level_5_spells,
    Replacer,
)


class DaughterOfDarkness(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Channel Divinity charges)

    _args: Args
    _feat_levels: set[int]

    # Passives
    _battle_magic: str
    _empowered_spells: str
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str

    # Spell lists
    _cunning_actions: SpellList

    @cached_property
    def _cantrips(self) -> SpellList:
        cantrips = SpellList(
            Comment="Trickery Domain Cleric cantrips",
            Spells=sorted(set([
                *cleric_cantrips(self).Spells,
                *warlock_cantrips(self).Spells,
            ])),
            UUID=self.make_uuid("cantrips"),
        )
        self.mod.add(cantrips)
        return cantrips

    @cached_property
    def _level_1_abilities(self) -> SpellList:
        abilities = SpellList(
            Comment="Trickery Domain Cleric level 1 abilities",
            Spells=[
                self._sneak_attack_melee,
                self._sneak_attack_ranged,
            ],
            UUID=self.make_uuid("level_1_abilities"),
        )
        self.mod.add(abilities)
        return abilities

    @cached_property
    def _level_1_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Trickery Domain Cleric level 1 spells",
            Spells=sorted(set([
                "Shout_Shield_Wizard",
                *cleric_level_1_spells(self).Spells,
                *warlock_level_1_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_1_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_2_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Trickery Domain Cleric level 2 spells",
            Spells=sorted(set([
                *cleric_level_2_spells(self).Spells,
                *warlock_level_2_spells(self).Spells,
            ]) - set([
                *warlock_level_1_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_2_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_3_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Trickery Domain Cleric level 3 spells",
            Spells=sorted(set([
                *cleric_level_3_spells(self).Spells,
                *warlock_level_3_spells(self).Spells,
            ]) - set([
                *warlock_level_2_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_3_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_4_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Trickery Domain Cleric level 4 spells",
            Spells=sorted(set([
                *cleric_level_4_spells(self).Spells,
                *warlock_level_4_spells(self).Spells,
            ]) - set([
                *warlock_level_3_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_4_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_5_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Trickery Domain Cleric level 5 spells",
            Spells=sorted(set([
                *cleric_level_5_spells(self).Spells,
                *warlock_level_5_spells(self).Spells,
            ]) - set([
                *warlock_level_4_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_5_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_6_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Trickery Domain Cleric level 6 spells",
            Spells=sorted(set([
                *cleric_level_6_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_6_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _sneak_attack_melee(self) -> str:
        name = f"{self.mod.get_prefix()}_SneakAttackMelee"
        self.mod.add(SpellData(
            name,
            using="Target_SneakAttack",
            SpellType="Target",
            SpellSuccess=[
                f"DealDamage(MainMeleeWeapon+LevelMapValue({self._sneak_attack_level}),MainMeleeWeaponDamageType)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TooltipDamageList=[
                f"DealDamage(MainMeleeWeapon+LevelMapValue({self._sneak_attack_level}),MainMeleeWeaponDamageType)",
            ],
        ))
        return name

    @cached_property
    def _sneak_attack_ranged(self) -> str:
        name = f"{self.mod.get_prefix()}_SneakAttackRanged"
        self.mod.add(SpellData(
            name,
            using="Projectile_SneakAttack",
            SpellType="Projectile",
            SpellSuccess=[
                f"DealDamage(MainRangedWeapon+LevelMapValue({self._sneak_attack_level}),MainRangedWeaponDamageType)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TooltipDamageList=[
                f"DealDamage(MainRangedWeapon+LevelMapValue({self._sneak_attack_level}),MainRangedWeaponDamageType)",
            ],
        ))
        return name

    @cached_property
    def _sneak_attack_level(self) -> str:
        name = f"{self.mod.get_prefix()}_SneakAttackLevel"
        self.mod.add(LevelMapSeries(
            **{f"Level{level}": f"{(level + 1) // 2}d6" for level in range(1, 13)},
            Name=name,
            PreferredClassUUID="114e7aee-d1d4-4371-8d90-8a2080592faf",  # Cleric
            UUID=self.mod.make_uuid("SneakAttackLevel"),
        ))
        return name

    @cached_property
    def _sneak_attack_unlock(self) -> str:
        name = f"{self.mod.get_prefix()}_SneakAttackUnlock"
        interrupt_name = f"{self.mod.get_prefix()}_SneakAttackInterrupt"
        critical_interrupt_name = f"{self.mod.get_prefix()}_SneakAttackCriticalInterrupt"

        self.mod.add(PassiveData(
            name,
            DisplayName="hc4558204g2c77g4b58gafb6g0ba6b3995c49;1",
            Properties="IsHidden",
            Boosts=[
                f"UnlockInterrupt({interrupt_name})",
                f"UnlockInterrupt({critical_interrupt_name})",
            ],
        ))

        damage_properties = [
            f"IF(IsMeleeAttack()):DealDamage(LevelMapValue({self._sneak_attack_level}),MainMeleeWeaponDamageType)",
            f"IF(IsRangedAttack()):DealDamage(LevelMapValue({self._sneak_attack_level}),MainRangedWeaponDamageType)",
        ]

        self.mod.add(InterruptData(
            interrupt_name,
            using="Interrupt_SneakAttack",
            Properties=damage_properties,
        ))

        self.mod.add(InterruptData(
            critical_interrupt_name,
            using="Interrupt_SneakAttack_Critical",
            Properties=damage_properties,
        ))

        return name

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="DaughterOfDarkness",
                         description="Changes Trickery Domain Cleric to a Cleric/Rogue/Warlock hybrid.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        # Passives
        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)
        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(4.5)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(6.0)

        # Spell lists
        self._cunning_actions = CunningActions(self.mod).spell_list()

    @progression(CharacterClass.CLERIC, range(1, 13))
    @progression(CharacterClass.CLERIC, 1, is_multiclass=True)
    def level_1_to_12_cleric(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression, [ActionResource.CHANNEL_DIVINITY_CHARGES], self._args.actions)
        progression.Selectors = [
            selector for selector in (progression.Selectors or [])
            if not selector.startswith(f"SelectSpells({cleric_cantrips(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_1_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_2_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_3_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_4_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_5_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_6_spells(self).UUID}")
        ] or None

    @progression(CharacterClass.CLERIC_KNOWLEDGE, 1)
    @progression(CharacterClass.CLERIC_LIFE, 1)
    @progression(CharacterClass.CLERIC_LIGHT, 1)
    @progression(CharacterClass.CLERIC_NATURE, 1)
    @progression(CharacterClass.CLERIC_TEMPEST, 1)
    @progression(CharacterClass.CLERIC_WAR, 1)
    def move_spells_1(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({cleric_cantrips(self).UUID},3,0,,,,AlwaysPrepared)",
            f"AddSpells({cleric_level_1_spells(self).UUID})",
        ]

    @progression(CharacterClass.CLERIC_KNOWLEDGE, 3)
    @progression(CharacterClass.CLERIC_LIFE, 3)
    @progression(CharacterClass.CLERIC_LIGHT, 3)
    @progression(CharacterClass.CLERIC_NATURE, 3)
    @progression(CharacterClass.CLERIC_TEMPEST, 3)
    @progression(CharacterClass.CLERIC_WAR, 3)
    def move_spells_3(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({cleric_level_2_spells(self).UUID})",
        ]

    @progression(CharacterClass.CLERIC_KNOWLEDGE, 4)
    @progression(CharacterClass.CLERIC_LIFE, 4)
    @progression(CharacterClass.CLERIC_LIGHT, 4)
    @progression(CharacterClass.CLERIC_NATURE, 4)
    @progression(CharacterClass.CLERIC_TEMPEST, 4)
    @progression(CharacterClass.CLERIC_WAR, 4)
    def move_spells_4(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({cleric_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_KNOWLEDGE, 5)
    @progression(CharacterClass.CLERIC_LIFE, 5)
    @progression(CharacterClass.CLERIC_LIGHT, 5)
    @progression(CharacterClass.CLERIC_NATURE, 5)
    @progression(CharacterClass.CLERIC_TEMPEST, 5)
    @progression(CharacterClass.CLERIC_WAR, 5)
    def move_spells_5(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({cleric_level_3_spells(self).UUID})",
        ]

    @progression(CharacterClass.CLERIC_KNOWLEDGE, 7)
    @progression(CharacterClass.CLERIC_LIFE, 7)
    @progression(CharacterClass.CLERIC_LIGHT, 7)
    @progression(CharacterClass.CLERIC_NATURE, 7)
    @progression(CharacterClass.CLERIC_TEMPEST, 7)
    @progression(CharacterClass.CLERIC_WAR, 7)
    def move_spells_7(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({cleric_level_4_spells(self).UUID})",
        ]

    @progression(CharacterClass.CLERIC_KNOWLEDGE, 9)
    @progression(CharacterClass.CLERIC_LIFE, 9)
    @progression(CharacterClass.CLERIC_LIGHT, 9)
    @progression(CharacterClass.CLERIC_NATURE, 9)
    @progression(CharacterClass.CLERIC_TEMPEST, 9)
    @progression(CharacterClass.CLERIC_WAR, 9)
    def move_spells_9(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({cleric_level_5_spells(self).UUID})",
        ]

    @progression(CharacterClass.CLERIC_KNOWLEDGE, 10)
    @progression(CharacterClass.CLERIC_LIFE, 10)
    @progression(CharacterClass.CLERIC_LIGHT, 10)
    @progression(CharacterClass.CLERIC_NATURE, 10)
    @progression(CharacterClass.CLERIC_TEMPEST, 10)
    @progression(CharacterClass.CLERIC_WAR, 10)
    def move_spells_10(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({cleric_cantrips(self).UUID},1,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_KNOWLEDGE, 11)
    @progression(CharacterClass.CLERIC_LIFE, 11)
    @progression(CharacterClass.CLERIC_LIGHT, 11)
    @progression(CharacterClass.CLERIC_NATURE, 11)
    @progression(CharacterClass.CLERIC_TEMPEST, 11)
    @progression(CharacterClass.CLERIC_WAR, 11)
    def move_spells_11(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({cleric_level_6_spells(self).UUID})",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
            "ProficiencyBonus(SavingThrow,Constitution)",
            "ActionResource(SneakAttack_Charge,1,0)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._battle_magic,
            self._fast_movement_30,
            self._sneak_attack_unlock,
            "Blindsight",
            "SculptSpells",
            "SuperiorDarkvision",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self._cantrips.UUID},4,0,,,,AlwaysPrepared)",
            f"AddSpells({self._level_1_abilities.UUID},,,,AlwaysPrepared)",
            f"AddSpells({self._level_1_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 2)
    def level_2(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._cunning_actions.UUID},,,,AlwaysPrepared)",
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "FastHands",
            "SecondStoryWork",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            f"AddSpells({self._level_2_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Assassinate_Initiative",
            "Assassinate_Ambush",
            "Assassinate_Resource",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_45,
            "ExtraAttack",
            "UncannyDodge",
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_30,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_3_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ImprovedCritical",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Evasion",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_4_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_60,
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_45,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_5_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._empowered_spells,
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ReliableTalent",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
            "AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a,,,,AlwaysPrepared)",  # Volley, Whirlwind
            f"AddSpells({self._level_6_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "BrutalCritical",
        ]


def main():
    parser = argparse.ArgumentParser(description="A replacer for Trickery Domain Clerics.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=1,
                        help="Feat progression every n levels (defaulting to 1; feat every level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Channel Divinity) multiplier (defaulting to 2; double charges)")
    args = DaughterOfDarkness.Args(**vars(parser.parse_args()))

    daughter_of_darkness = DaughterOfDarkness(args)
    daughter_of_darkness.build()


if __name__ == "__main__":
    main()
