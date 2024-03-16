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
    Bolster,
    EmpoweredSpells,
    Movement,
    PackMule,
    multiply_resources,
)
from modtools.gamedata import SpellData
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    LevelMapSeries,
    ProgressionDescription,
    SpellList,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    progression,
    Replacer,
)
from modtools.text import Equipment


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
    _pack_mule: str

    # Spells
    _bolster: str

    @cached_property
    def _level_1_spell_list(self) -> str:
        spell_list_id = str(self.make_uuid("level_1_spell_list"))
        self.mod.add(SpellList(
            Comment="Spells gained at Trickery Domain Cleric level 1",
            Spells=[
                self._bolster,
                self._sneak_attack_melee,
                self._sneak_attack_ranged,
                "Projectile_EldritchBlast",
            ],
            UUID=spell_list_id,
        ))
        return spell_list_id

    @cached_property
    def _level_6_spell_list(self) -> str:
        spell_list_id = str(self.make_uuid("level_6_spell_list"))
        self.mod.add(SpellList(
            Comment="Spells gained at Trickery Domain Cleric level 6",
            Spells=[self._shadow_step],
            UUID=spell_list_id,
        ))
        return spell_list_id

    @cached_property
    def _warlock_spells_description(self) -> str:
        name = f"{self.mod.get_prefix()}_WarlockSpells"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Warlock Spells"}
        loca[f"{name}_Description"] = {"en": """
            Choose additional spells from the Warlock spell list.
            """}

        self.mod.add(ProgressionDescription(
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            SelectorId=name,
            UUID=self.make_uuid("WarlockSpells"),
        ))

        return name

    def _select_warlock_spells(self, list_uuid: str, count: int = 1) -> str:
        return f"SelectSpells({list_uuid},{count},0,{self._warlock_spells_description},,,AlwaysPrepared)"

    @cached_property
    def _shadow_step(self) -> str:
        """A combined Shadow Step/Cloak of Shadows cantrip."""
        name = f"{self._mod.get_prefix()}_ShadowStep"
        self._mod.add(SpellData(
            name,
            using="Target_ShadowStep",
            SpellType="Target",
            Level="",
            SpellProperties="GROUND:TeleportSource();ApplyStatus(CLOAK_OF_SHADOWS,100,2)",
            RequirementConditions="",
            RequirementEvents="",
            SpellFlags=[
                "HasVerbalComponent",
                "IsSpell",
                "HasHighGroundRangeExtension",
                "RangeIgnoreVerticalThreshold",
                "Stealth",
                "Invisible",
            ],
            TargetConditions="",
            TooltipStatusApply="ApplyStatus(CLOAK_OF_SHADOWS,100,2)",
            UseCosts="Movement:Distance*0.5",
        ))
        return name

    @cached_property
    def _sneak_attack_melee(self) -> str:
        name = f"{self._mod.get_prefix()}_SneakAttackMelee"
        self._mod.add(SpellData(
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
        name = f"{self._mod.get_prefix()}_SneakAttackRanged"
        self._mod.add(SpellData(
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
        name = f"{self._mod.get_prefix()}_SneakAttack"
        self.mod.add(LevelMapSeries(
            **{f"Level{level}": f"{(level + 1) // 2}d6" for level in range(1, 13)},
            Name=name,
            PreferredClassUUID="044e4e07-6980-479f-80e5-3c4a84e691d1",  # Trickery Domain
            UUID=self.mod.make_uuid("SneakAttack"),
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
        self._pack_mule = PackMule(self.mod).add_pack_mule(2.0)

        # Spells
        self._bolster = Bolster(self.mod).add_bolster()

        # Shadowheart's equipment
        self.mod.add(Equipment("""
            new equipment "EQ_Shadowheart"
            add initialweaponset "Melee"
            add equipmentgroup
            add equipment entry "WPN_Shortsword"
            add equipmentgroup
            add equipment entry "WPN_Shortsword"
            add equipmentgroup
            add equipment entry "ARM_Boots_Leather"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "ARM_ChainShirt_Body_Shar"
            add equipmentgroup
            add equipment entry "UNI_ShadowheartCirclet"
            add equipmentgroup
            add equipment entry "OBJ_Camp_Pack"
            add equipmentgroup
            add equipment entry "OBJ_Keychain"
            add equipmentgroup
            add equipment entry "OBJ_Bag_AlchemyPouch"
            add equipmentgroup
            add equipment entry "ARM_Camp_Body_Shadowheart"
            add equipmentgroup
            add equipment entry "ARM_Camp_Shoes_Shadowheart"
            add equipmentgroup
            add equipment entry "OBJ_Backpack_CampSupplies"
            add equipmentgroup
            add equipment entry "ARM_Underwear_Shadowheart"
            add equipmentgroup
            add equipment entry "OBJ_Scroll_Revivify"
        """))

    @progression(CharacterClass.CLERIC, range(1, 13))
    def level_1_to_12_cleric(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression, [ActionResource.CHANNEL_DIVINITY_CHARGES], self._args.actions)

    @progression(CharacterClass.CLERIC_TRICKERY, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "Proficiency(MartialWeapons)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._battle_magic,
            self._fast_movement_30,
            "SculptSpells",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_1_spell_list},,,,AlwaysPrepared)",
            self._select_warlock_spells("4823a292-f584-4f7f-8434-6630c72e5411", 2),  # Fiend level 1 spells
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 2)
    def level_2(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(2dc120ff-903b-494b-8dc8-38721098ce38,,,,AlwaysPrepared)",  # Rogue cunning actions
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
            "SelectPassives(333fb1b0-9398-4ca8-953e-6c0f9a59bbed,2,WarlockInvocations)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
            self._select_warlock_spells("4823a292-f584-4f7f-8434-6630c72e5411"),  # Fiend level 1 spells
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Assassinate_Initiative",
            "Assassinate_Ambush",
            "Assassinate_Resource",
            "FastHands",
            "PactOfTheBlade",
            "SecondStoryWork",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            self._select_warlock_spells("835aeca7-c64a-4aaa-a25c-143aa14a5cec"),  # Fiend level 2 spells
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            self._select_warlock_spells("835aeca7-c64a-4aaa-a25c-143aa14a5cec"),  # Fiend level 2 spells
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_45,
            "ThirstingBlade_Blade",
            "UncannyDodge",
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_30,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectPassives(8adab8f9-e360-4f79-851b-2c7e050ca23d,1,WarlockInvocations)",
            self._select_warlock_spells("5dec41aa-f16a-434e-b209-50c07e64e4ed"),  # Fiend level 3 spells
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 6)
    def level_6(self, progression: Progression) -> None:
        # Remove Cloak of Shadows
        selectors = [sel for sel in progression.Selectors if "90acd47f-3475-4c85-99ea-7fd503591be4" not in sel]

        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_6_spell_list},,,,AlwaysPrepared)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            self._select_warlock_spells("5dec41aa-f16a-434e-b209-50c07e64e4ed"),  # Fiend level 3 spells
        ]

        progression.Selectors = selectors

    @progression(CharacterClass.CLERIC_TRICKERY, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Evasion",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectPassives(39efef92-9987-46e2-8c43-54052c1be535,1,WarlockInvocations)",
            self._select_warlock_spells("7ad7dbd0-751b-4bcd-8034-53bcc7bfb19d"),  # Fiend level 4 spells
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            self._select_warlock_spells("7ad7dbd0-751b-4bcd-8034-53bcc7bfb19d"),  # Fiend level 4 spells
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
            "SelectPassives(a2d72748-0792-4f1e-a798-713a66d648eb,1,WarlockInvocations)",
            self._select_warlock_spells("deab57bf-4eec-4085-82f7-87335bce3f5d"),  # Fiend level 5 spells
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._empowered_spells]
        progression.Selectors = (progression.Selectors or []) + [
            self._select_warlock_spells("deab57bf-4eec-4085-82f7-87335bce3f5d"),  # Fiend level 5 spells
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ReliableTalent",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
            self._select_warlock_spells("deab57bf-4eec-4085-82f7-87335bce3f5d"),  # Fiend level 5 spells
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "SelectPassives(ab56f79f-95ec-48e5-bd83-e80ba9afc844,1,WarlockInvocations)",
            self._select_warlock_spells("deab57bf-4eec-4085-82f7-87335bce3f5d"),  # Fiend level 5 spells
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
