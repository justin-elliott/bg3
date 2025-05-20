#!/usr/bin/env python3
"""
Generates files for the "WayOfShadowMagic" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    BattleMagic,
    Bolster,
    Defense,
    EmpoweredSpells,
    multiply_resources,
    PackMule,
)
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    SpellList,
)
from modtools.lsx.game import Dependencies, Progression
from modtools.replacers import (
    Replacer,
    progression,
)


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class WayOfShadowMagic(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Ki Points)

    _args: Args
    _feat_levels: set[int]

    # Passives
    _battle_magic: str
    _empowered_spells: str
    _pack_mule: str
    _unarmored_defense: str
    _warding: str

    # Spells
    _bolster: str

    @cached_property
    def _manifestation_of_shadow(self) -> str:
        """Add the Manifestation of Shadow passive, returning its name."""
        name = f"{self.mod.get_prefix()}_ManifestationOfShadow"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Manifestation of Shadow"}
        loca[f"{name}_Description"] = {"en": """
            You draw upon the shadows to empower your strikes. Your melee unarmed attacks deal an additional [1].

            Whenever you deal damage with a melee unarmed attack, you gain
            <LSTag Type="Status" Tooltip="MAG_GISH_ARCANE_ACUITY">Arcane Acuity</LSTag> for 2 turns.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["DealDamage(1d4+WisdomModifier,Psychic)"],
            Icon="Action_Barbarian_MagicAwareness",
            Properties="Highlighted",
            Boosts=[
                "IF(IsMeleeUnarmedAttack()):CharacterUnarmedDamage(1d4+WisdomModifier,Psychic)",
                "UnlockSpellVariant(MeleeUnarmedAttackCheck(),ModifyTargetRadius(Multiplicative,1))",
            ],
            StatsFunctorContext="OnDamage",
            Conditions="IsMeleeUnarmedAttack()",
            StatsFunctors=[
                "ApplyStatus(SELF,MAG_GISH_ARCANE_ACUITY,100,2)",
                "ApplyStatus(SELF,MAG_GISH_ARCANE_ACUITY_DURATION_TECHNICAL,100,1)",
            ],
        ))

        return name

    @cached_property
    def _bonus_unarmed_strike(self) -> str:
        """Adds a bonus unarmed strike."""
        name = f"{self.mod.get_prefix()}_BonusUnarmedStrike"

        self.mod.add(SpellData(
            name,
            using="Target_UnarmedStrike_Monk",
            SpellType="Target",
            SpellFlags=["IsMelee", "IsHarmful", "DisableBlood"],
        ))

        return name

    @cached_property
    def _slow_fall(self) -> str:
        """Slow Fall as a passive."""
        name = f"{self.mod.get_prefix()}_SlowFall"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Slow Fall"}
        loca[f"{name}_Description"] = {"en": """
            You only take half damage from falling.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_SlowFall",
            Properties=["Highlighted"],
            Boosts=["FallDamageMultiplier(0.5)"],
        ))

        return name

    @cached_property
    def _stillness_of_mind(self) -> str:
        """Stillness of Mind as a passive."""
        name = f"{self.mod.get_prefix()}_StillnessOfMind"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Stillness of Mind"}
        loca[f"{name}_Description"] = {"en": """
            You are immune to being <LSTag Tooltip="CharmedGroup">Charmed</LSTag> or
            <LSTag Type="Status" Tooltip="FRIGHTENED">Frightened</LSTag>.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_StillnessOfMind",
            Properties=["Highlighted"],
            Boosts=[
                "StatusImmunity(SG_Charmed)",
                "StatusImmunity(SG_Frightened)",
            ],
        ))

        return name

    @cached_property
    def _level_1_spells_always_prepared(self) -> str:
        spell_list = str(self.make_uuid("level_1_spells_always_prepared"))
        self.mod.add(SpellList(
            Name="Way of Shadow Magic level 1 spells that are always prepared",
            Spells=[self._bolster],
            UUID=spell_list,
        ))
        return spell_list

    @cached_property
    def _flurry_of_blows_spell_list(self) -> str:
        spell_list = str(self.make_uuid("flurry_of_blows_spell_list"))
        self.mod.add(SpellList(
            Name="Way of Shadow Magic Flurry of Blows",
            Spells=[
                self._bonus_unarmed_strike,
                "Target_OpenHandTechnique_Knock",
                "Target_OpenHandTechnique_NoReactions",
                "Target_OpenHandTechnique_Push",
            ],
            UUID=spell_list,
        ))
        return spell_list

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="WayOfShadowMagic",
                         description="Adds monk features to the Shadow Magic Sorcerer subclass.")

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
        self._unarmored_defense = Defense(self.mod).add_unarmored_defense(CharacterAbility.CHARISMA)
        self._warding = Defense(self.mod).add_warding()

    @progression(CharacterClass.SORCERER, range(1, 21))
    @progression(CharacterClass.SORCERER, 1, is_multiclass=True)
    def level_1_to_20_sorcerer(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SORCERY_POINTS], self._args.actions)

    @progression(CharacterClass.SORCERER, 1)
    def level_1_sorcerer(self, progression: Progression) -> None:
        progression.Selectors = [
            *[selector for selector in progression.Selectors if not selector.startswith("SelectSkills(")],
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{2*self._args.actions},0)"]
        progression.PassivesAdded += [
            "DevilsSight",
            "MartialArts_DextrousUnarmedAttacks",
            "MartialArts_UnarmedDamage",
            "Monk_SoundSwitch",
            self._battle_magic,
            self._pack_mule,
            self._unarmored_defense,
            self._warding,
        ]
        progression.Selectors = [f"AddSpells({self._level_1_spells_always_prepared},,,,AlwaysPrepared)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 2)
    def level_2(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["SculptSpells", "UnarmoredMovement_1"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["DeflectMissiles"]
        progression.Selectors += [f"AddSpells({self._flurry_of_blows_spell_list},,,,AlwaysPrepared)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = [self._slow_fall]
        progression.Selectors = ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["ExtraAttack"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = [
            "UnarmoredMovement_2",
            "KiEmpoweredStrikes",
            self._manifestation_of_shadow,
        ]
        progression.PassivesRemoved = ["UnarmoredMovement_1"]
        progression.Selectors += ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["Evasion", self._stillness_of_mind]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["ImprovedCritical"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["Indomitable", "UnarmoredMovement_DifficultTerrain"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["UnarmoredMovement_3", "PurityOfBody", self._empowered_spells]
        progression.PassivesRemoved = ["UnarmoredMovement_2"]
        progression.Selectors = ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["ExtraAttack_2"]
        progression.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["ReliableTalent"]
        progression.Selectors = ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 13)
    def level_13(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["Indomitable_2", "TongueOfTheSunAndMoon"]
        progression.PassivesRemoved = ["Indomitable"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 14)
    def level_14(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["UnarmoredMovement_4"]
        progression.PassivesRemoved = ["UnarmoredMovement_3"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 15)
    def level_15(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 16)
    def level_16(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.Selectors = ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 17)
    def level_17(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["Indomitable_3"]
        progression.PassivesRemoved = ["Indomitable_2"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 18)
    def level_18(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["UnarmoredMovement_5"]
        progression.PassivesRemoved = ["UnarmoredMovement_4"]
        progression.Selectors = ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 19)
    def level_19(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]

    @progression(CharacterClass.SORCERER_SHADOWMAGIC, 20)
    def level_20(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(KiPoint,{self._args.actions},0)"]
        progression.PassivesAdded = ["ExtraAttack_3", "PerfectSelf"]
        progression.PassivesRemoved = ["ExtraAttack_2"]


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


def main():
    parser = argparse.ArgumentParser(description="A replacer for Way of Shadow Monks.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Ki and Sorcery Points) multiplier (defaulting to 2)")
    args = WayOfShadowMagic.Args(**vars(parser.parse_args()))

    way_of_shadow_magic = WayOfShadowMagic(args)
    way_of_shadow_magic.build()


if __name__ == "__main__":
    main()
