#!/usr/bin/env python3
"""
Generates files for the "Battlemage" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    Attack,
    Movement,
    PackMule,
    multiply_resources,
)
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    ClassDescription,
    Progression,
    SpellList,
    TooltipUpcastDescription,
)
from modtools.replacers import (
    class_description,
    only_existing_progressions,
    progression,
    Replacer,
)


class Battlemage(Replacer):
    @dataclass
    class Args:
        feats: set[int]  # Feat improvement levels
        spells: int      # Multiplier for spell slots

    _args: Args
    _feat_levels: set[int]

    @cached_property
    def _advancement(self) -> dict[int, str]:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_Advancement"
        loca[f"{name}_DisplayName"] = {"en": "Advancement"}
        loca[f"{name}_Description"] = {"en": """
            Your abilities improve by 2 at Battlemage levels 3, 5, 7, 9, and 11.
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
        loca[f"{name}_DisplayName"] = {"en": "Battlemage: Quickened Spell"}
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
            ToggleGroup=f"{self.mod.get_prefix()}_Metamagic",
            ToggleOnEffect="VFX_Spells_Cast_Sorcerer_Metamagic_Quickened_HeadFX_01:Dummy_HeadFX",
            ToggleOffContext="OnCastResolved",
        ))
        return name

    @cached_property
    def _twinned_spell(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_TwinnedSpell"
        loca[f"{name}_DisplayName"] = {"en": "Battlemage: Twinned Spell"}
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
            ToggleGroup=f"{self.mod.get_prefix()}_Metamagic",
            ToggleOnEffect="VFX_Spells_Cast_Sorcerer_Metamagic_Twinned_HeadFX_01:Dummy_HeadFX",
            ToggleOffContext="OnCastResolved",
        ))
        return name

    @cached_property
    def _arcane_weapon(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_ArcaneWeapon"
        loca[f"{name}_DisplayName"] = {"en": "Arcane Weapon"}
        loca[f"{name}_Description"] = {"en": """
            Infuse the weapon in your main hand with arcane energy. The weapon becomes magical, preventing it from being
            disarmed. It receives a +[1] bonus to <LSTag Tooltip="AttackRoll">Attack</LSTag> and Damage Rolls, and deals
            an additional [2].
            """}

        loca[f"{name}_UpcastDescription"] = {"en": """
            Casting this spell using a 4th or 5th level spell slot will increase the Attack and Damage bonus to [1], and
            a 6th level spell slot will increase it to [2].
            """}
        upcast_description = TooltipUpcastDescription(
            Name="Arcane Weapon",
            Text=loca[f"{name}_UpcastDescription"],
            UUID=self.make_uuid("Upcast Arcane Weapon"),
        )
        self.mod.add(upcast_description)

        return name

    @cached_property
    def _class_abilities_level_2(self) -> SpellList:
        spells = SpellList(
            Comment="Battlemage class abilities level 2",
            Spells=[
                Attack(self.mod).add_brutal_cleave(),
            ],
            UUID=self.make_uuid("Battlemage class abilities level 2"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _class_abilities_level_3(self) -> SpellList:
        spells = SpellList(
            Comment="Battlemage class abilities level 3",
            Spells=[
                self._arcane_weapon,
            ],
            UUID=self.make_uuid("Battlemage class abilities level 3"),
        )
        self.mod.add(spells)
        return spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Battlemage",
                         description="Enhancements for the Abjuration Wizard subclass.")

        self._args = args

        if len(args.feats) == 0:
            self._feat_levels = frozenset([4, 8, 12])
        elif len(args.feats) == 1:
            feat_level = next(level for level in args.feats)
            self._feat_levels = frozenset(range(max(feat_level, 2), 13, feat_level))
        else:
            self._feat_levels = args.feats - frozenset([1])

    @class_description(CharacterClass.WIZARD_ABJURATION)
    def battlemage_description(self, class_description: ClassDescription) -> None:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_ClassDescription"
        loca[f"{name}_DisplayName"] = {"en": "Battlemage"}
        loca[f"{name}_Description"] = {"en": """
            You twist and harden the Weave into arcane wards, while wading into the thick of battle.
            Learning Abjuration spells from scrolls only costs you 25g per spell level, not 50.
            """}
        class_description.DisplayName = loca[f"{name}_DisplayName"]
        class_description.Description = loca[f"{name}_Description"]

    @progression(CharacterClass.WIZARD, range(1, 13))
    @progression(CharacterClass.WIZARD_ABJURATION, range(1, 13))
    @progression(CharacterClass.WIZARD, 1, is_multiclass=True)
    @only_existing_progressions
    def level_1_to_12_wizard(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)

    @progression(CharacterClass.WIZARD_ABJURATION, 2)
    def level_2(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ProficiencyBonus(SavingThrow,Strength)",
            "ProficiencyBonus(SavingThrow,Dexterity)",
            "ProficiencyBonus(SavingThrow,Constitution)",
            "ProficiencyBonus(SavingThrow,Charisma)",
            "Proficiency(LightArmor)",
            "Proficiency(MediumArmor)",
            "Proficiency(HeavyArmor)",
            "Proficiency(Shields)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            Movement(self.mod).add_fast_movement(3.0),
            PackMule(self.mod).add_pack_mule(5.0),
            self._quickened_spell,
            self._twinned_spell,
            "SculptSpells",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._class_abilities_level_2.UUID},,,,AlwaysPrepared)",
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._advancement[3],
            "DevilsSight",
            "JackOfAllTrades",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._class_abilities_level_3.UUID},,,,AlwaysPrepared)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ImprovedCritical",
            "FeralInstinct",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._advancement[5],
            "UncannyDodge",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "PotentCantrip",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._advancement[7],
            "Evasion",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
            "FOR_NightWalkers_WebImmunity",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._advancement[9],
            "BrutalCritical",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "EmpoweredEvocation",
        ]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._advancement[11],
            "ReliableTalent",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
        ]

    @progression(CharacterClass.WIZARD_ABJURATION, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
        ]
        progression.Selectors = (progression.Selectors or []) + [
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
    args = Battlemage.Args(**vars(parser.parse_args()))

    battlemage = Battlemage(args)
    battlemage.build()


if __name__ == "__main__":
    main()
