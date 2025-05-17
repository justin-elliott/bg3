#!/usr/bin/env python3
"""
Generates files for the "ChromaticSorcerer" mod.
"""

import argparse
import os
import re

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    Bolster,
    multiply_resources,
    PackMule,
)
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    Dependencies,
    Progression,
)
from modtools.replacers import (
    only_existing_progressions,
    progression,
    Replacer,
)
from typing import Final


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class ChromaticSorcerer(Replacer):
    @dataclass
    class Args:
        feats: int             # Feats every n levels
        spells_per_level: int  # Multiplier for spells per level
        spells: int            # Multiplier for spell slots
        actions: int           # Multiplier for other action resources (Sorcery Points)
        skills: int            # Number of skills to select at character creation
        expertise: int         # Number of skill expertises to select at character creation

    _SELECT_SORCERER_SPELLS: Final = re.compile(
        r"^\s*SelectSpells\(\s*(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*SorcererSpell\s*\)\s*$")

    _args: Args
    _feat_levels: set[int]

    # Passives
    _pack_mule: str

    # Spells
    _bolster: str

    def _draconic_ancestry(self):
        name = "DraconicAncestry_Copper"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Draconic Ancestry: Chromatic"}
        loca[f"{name}_Description"] = {"en": """
            At Level 6, your spells are more powerful, and you are resistant to all damage.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Copper",
            Properties="Highlighted",
            Boosts=[
                f"UnlockSpell({self._bolster},AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf,,Charisma)",
                "UnlockSpell(Target_Command_Container,AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf,,Charisma)",
                "UnlockSpell(Projectile_EldritchBlast,AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf,,Charisma)",
            ],
        ))

    def _draconic_resilience(self):
        name = "DraconicResilience"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Draconic Resilience"}
        loca[f"{name}_Description"] = {"en": """
            Dragon-like scales cover parts of your skin. Your base <LSTag Tooltip="ArmourClass">Armour Class</LSTag> is
            increased by [1], and all damage that you take is reduced by [2].
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["3", "RegainHitPoints(ProficiencyBonus)"],
            Icon="PassiveFeature_DraconicResilience",
            Properties="Highlighted",
            BoostContext=["OnEquip", "OnCreate"],
            Boosts=["AC(3)", "DamageReduction(All,Flat,ProficiencyBonus)"],
        ))

    def _elemental_affinity(self):
        loca = self.mod.get_localization()

        affinities = [
            (["Black"], "ACID", "Resistance(Acid,Resistant)"),
            (["Copper"], "CHROMATIC", "Resistance(All,Resistant)"),
            (["Silver", "White"], "COLD", "Resistance(Cold,Resistant)"),
            (["Red", "Gold", "Brass"], "FIRE", "Resistance(Fire,Resistant)"),
            (["Blue", "Bronze"], "LIGHTNING", "Resistance(Lightning,Resistant)"),
            (["Green"], "POISON", "Resistance(Poison,Resistant)"),
        ]

        damage_stats_functors = []
        resistance_stats_functors = []

        for passives, affinity, _ in affinities:
            has_passives = " or ".join([f"HasPassive('DraconicAncestry_{passive}')" for passive in passives])
            damage_stats_functors += [
                f"IF({has_passives}):ApplyStatus(ELEMENTALAFFINITY_{affinity}_EXTRA_DAMAGE_TECHNICAL,100,-1)"
            ]
            resistance_stats_functors += [
                f"IF({has_passives}):ApplyStatus(ELEMENTALAFFINITY_{affinity}_RESISTANCE_TECHNICAL,100,-1)"
            ]

        self.mod.add(PassiveData(
            "ElementalAffinity_Damage",
            DisplayName="h5288bd8fg7e82g4c6cgae28gacd825b1f8e9;3",
            Description="hf32ca0b3g8a45g43f6gaf4ag5f343ed8eaa6;5",
            Icon="PassiveFeature_ElementalAffinity_ExtraDamage",
            Properties="Highlighted",
            StatsFunctorContext="OnCreate",
            StatsFunctors=damage_stats_functors,
        ))

        loca["ELEMENTALAFFINITY_CHROMATIC_EXTRA_DAMAGE_TECHNICAL"] = {"en": """
            Elemental Affinity: Additional Spell Damage
            """}

        self.mod.add(StatusData(
            "ELEMENTALAFFINITY_CHROMATIC_EXTRA_DAMAGE_TECHNICAL",
            StatusType="BOOST",
            DisplayName=loca["ELEMENTALAFFINITY_CHROMATIC_EXTRA_DAMAGE_TECHNICAL"],
            Icon="PassiveFeature_ElementalAffinity_ExtraDamage",
            StackId="ELEMENTALAFFINITY_CHROMATIC_EXTRA_DAMAGE_TECHNICAL",
            Boosts="IF(IsSpell()):DamageBonus(max(0,CharismaModifier))",
            StatusPropertyFlags=[
                "DisableOverhead", "DisableCombatlog", "DisablePortraitIndicator", "ApplyToDead", "IgnoreResting"
            ],
            StatusGroups="SG_RemoveOnRespec",
        ))

        loca["ElementalAffinity_Resistance_Check_Description"] = {"en": """
            You are <LSTag Tooltip="Resistant">Resistant</LSTag> to the damage type associated with your draconic
            ancestry.
            """}

        self.mod.add(PassiveData(
            "ElementalAffinity_Resistance_Check",
            DisplayName="h6948c0efg778bg41d3g88e4g9f4c658120a4;2",
            Description=loca["ElementalAffinity_Resistance_Check_Description"],
            Icon="Skill_Sorcerer_Passive_ElementalAffinity_Resistance",
            Properties="Highlighted",
            StatsFunctorContext="OnCreate",
            StatsFunctors=resistance_stats_functors,
        ))

        for _, affinity, resistance in affinities:
            loca[f"ELEMENTALAFFINITY_{affinity}_RESISTANCE_TECHNICAL"] = {"en": f"""
                Elemental Affinity: {affinity.title()} Resistance
                """}

            self.mod.add(StatusData(
                f"ELEMENTALAFFINITY_{affinity}_RESISTANCE_TECHNICAL",
                StatusType="BOOST",
                DisplayName=loca[f"ELEMENTALAFFINITY_{affinity}_RESISTANCE_TECHNICAL"],
                Icon="PassiveFeature_ElementalAffinity_ExtraDamage",
                StackId="ELEMENTALAFFINITY_CHROMATIC_EXTRA_DAMAGE_TECHNICAL",
                Boosts=resistance,
                StatusPropertyFlags=[
                    "DisableOverhead", "DisableCombatlog", "DisablePortraitIndicator", "ApplyToDead", "IgnoreResting"
                ],
                StatusGroups="SG_RemoveOnRespec",
            ))

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="ChromaticSorcerer",
                         description="Changes the Copper Draconic Sorcerer subclass to a Chromatic Draconic Sorcerer.")

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

        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)
        self._bolster = Bolster(self.mod).add_bolster()

        self._draconic_ancestry()
        self._draconic_resilience()
        self._elemental_affinity()

    @progression(CharacterClass.SORCERER, range(1, 21))
    @only_existing_progressions
    def level_1_to_20_resources(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression, [ActionResource.SORCERY_POINTS], self._args.actions)
        selectors = []
        for selector in progression.Selectors:
            if (match := self._SELECT_SORCERER_SPELLS.match(selector)) is not None:
                spelllist, new_count, replace_count = match.groups()
                updated_count = (int(new_count) or 1) * self._args.spells_per_level
                selector = f"SelectSpells({spelllist},{updated_count},{replace_count},SorcererSpell)"
            selectors.append(selector)
        progression.Selectors = selectors

    @progression(CharacterClass.SORCERER, 1)
    def level_1_skills(self, progression: Progression) -> None:
        progression.PassivesAdded += [self._pack_mule]
        selectors = progression.Selectors
        if self._args.skills is not None:
            selectors = [selector for selector in selectors if not selector.startswith("SelectSkills(")]
            selectors.append(f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self._args.skills})")
        if self._args.expertise is not None:
            selectors = [selector for selector in selectors if not selector.startswith("SelectSkillsExpertise(")]
            selectors.append(f"SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self._args.expertise})")
        progression.Selectors = selectors

    @progression(CharacterClass.SORCERER_DRACONIC, 1)
    def level_1(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 2)
    def level_2(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 3)
    def level_3(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 4)
    def level_4(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 5)
    def level_5(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 6)
    def level_6(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 7)
    def level_7(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 8)
    def level_8(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 9)
    def level_9(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 10)
    def level_10(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 11)
    def level_11(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 12)
    def level_12(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 13)
    def level_13(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 14)
    def level_14(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 15)
    def level_15(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 16)
    def level_16(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 17)
    def level_17(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 18)
    def level_18(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 19)
    def level_19(self, progression: Progression) -> None:
        ...

    @progression(CharacterClass.SORCERER_DRACONIC, 20)
    def level_20(self, progression: Progression) -> None:
        ...


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Changes the Copper Draconic Sorcerer subclass to a Chromatic Draconic Sorcerer.")
    parser.add_argument("-f", "--feats", type=level_list, default=set(),
                        help="Feat progression every n levels (defaulting to double progression)")
    parser.add_argument("-l", "--spells-per-level", type=int, choices=range(1, 9), default=2,
                        help="Spells per level multiplier (defaulting to 2)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=4,
                        help="Spell slot multiplier (defaulting to 4)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=4,
                        help="Action resource (Sorcery Point) multiplier (defaulting to 4)")
    parser.add_argument("-k", "--skills", type=int, default=6,
                        help="Number of skills to select at character creation (defaulting to 6)")
    parser.add_argument("-e", "--expertise", type=int, default=3,
                        help="Number of skill expertises to select at character creation (defaulting to 3)")
    args = ChromaticSorcerer.Args(**vars(parser.parse_args()))

    chromatic_sorcerer = ChromaticSorcerer(args)
    chromatic_sorcerer.build()
