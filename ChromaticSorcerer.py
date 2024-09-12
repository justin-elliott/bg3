#!/usr/bin/env python3
"""
Generates files for the "ChromaticSorcerer" mod.
"""

import os

from functools import cached_property
from moddb import (
    Bolster,
    Movement,
    multiply_resources,
    spells_always_prepared,
)
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    CharacterSubclasses,
    ClassDescription,
    Progression,
    SpellList,
)
from modtools.replacers import (
    class_description,
    only_existing_progressions,
    progression,
    Replacer,
)


class ChromaticSorcerer(Replacer):
    _ACTION_RESOURCES = frozenset([ActionResource.SPELL_SLOTS, ActionResource.SORCERY_POINTS])

    # Passives
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str

    # Spells
    _bolster: str

    def _draconic_ancestry(self):
        name = "DraconicAncestry_Copper"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Draconic Ancestry: Chromatic"}
        loca[f"{name}_Description"] = {"en": """
            At Level 6, your spells are more powerful, and you take half damage from all spells.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Copper",
            Properties="Highlighted",
            Boosts="UnlockSpell(Projectile_EldritchBlast,AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf,,Charisma)",
        ))

    def _draconic_resilience(self):
        name = "DraconicResilience"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Draconic Resilience"}
        loca[f"{name}_Description"] = {"en": """
            Dragon-like scales cover parts of your skin. Your base <LSTag Tooltip="ArmourClass">Armour Class</LSTag> is
            increased by [1].
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["3"],
            Icon="PassiveFeature_DraconicResilience",
            Properties="Highlighted",
            BoostContext=["OnEquip", "OnCreate"],
            Boosts=["AC(3)"],
        ))

    def _elemental_affinity(self):
        loca = self.mod.get_localization()

        affinities = [
            (["Black"], "ACID", "Resistance(Acid,Resistant)"),
            (["Copper"], "CHROMATIC", "SpellResistance(Resistant)"),
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

    @cached_property
    def _draconic_abilities(self) -> str:
        name = f"{self._mod.get_prefix()}_DraconicAbilities"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Draconic Abilities"}
        loca[f"{name}_Description"] = {"en": """
            Due to your draconic ancestry, all of your <LSTag Tooltip="AbilityScore">Ability Scores</LSTag> are
            increased by [1].
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["4"],
            Icon="Spell_Transmutation_EnhanceAbility",
            Properties=["Highlighted"],
            Boosts=[f"Ability({ability.name.title()},4)" for ability in CharacterAbility],
        ))

        return name

    @cached_property
    def _level_1_spell_list(self) -> str:
        spell_list = str(self.make_uuid("level_1_spell_list"))
        self.mod.add(SpellList(
            Comment="Chromatic Draconic Sorcerer level 1 spells",
            Spells=[self._bolster],
            UUID=spell_list,
        ))
        return spell_list

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="ChromaticSorcerer",
                         description="Changes the Copper Draconic Sorcerer subclass to a Chromatic Draconic Sorcerer.")

        self._draconic_ancestry()
        self._draconic_resilience()
        self._elemental_affinity()

        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(4.5)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(6.0)

        self._bolster = Bolster(self.mod).add_bolster()

    @class_description(CharacterClass.SORCERER)
    def sorcerer_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6
        class_description.MustPrepareSpells = True

    @class_description(CharacterClass.SORCERER_DRACONIC)
    def sorcerer_subclass_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.MustPrepareSpells = True

    @progression(CharacterSubclasses.SORCERER, range(1, 13))
    @only_existing_progressions
    def level_1_to_20_resources(self, progression: Progression) -> None:
        multiply_resources(progression, self._ACTION_RESOURCES, 2)
        spells_always_prepared(progression)

    @progression(CharacterClass.SORCERER, [2, 4, 6, 8, 10, 12, 14, 16, 18, 19])
    def level_2_to_20_improvement(self, progression: Progression) -> None:
        progression.AllowImprovement = True

    @progression(CharacterClass.SORCERER_DRACONIC, 1)
    def level_1(self, progression: Progression) -> None:
        for proficiency in ["LightArmor", "MediumArmor", "Shields", "SimpleWeapons", "MartialWeapons"]:
            progression.Boosts.append(f"Proficiency({proficiency})")

        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._draconic_abilities,
            self._fast_movement_30,
        ]
        progression.Selectors += [
            f"AddSpells({self._level_1_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_DRACONIC, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["Blindsight", "SuperiorDarkvision"]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
        ]

    @progression(CharacterClass.SORCERER_DRACONIC, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["JackOfAllTrades"]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.SORCERER_DRACONIC, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]

    @progression(CharacterClass.SORCERER_DRACONIC, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._fast_movement_45]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [self._fast_movement_30]

    @progression(CharacterClass.SORCERER_DRACONIC, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["PotentCantrip"]

    @progression(CharacterClass.SORCERER_DRACONIC, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain", "LandsStride_Surfaces", "LandsStride_Advantage"]

    @progression(CharacterClass.SORCERER_DRACONIC, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + []

    @progression(CharacterClass.SORCERER_DRACONIC, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._fast_movement_60]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [self._fast_movement_45]

    @progression(CharacterClass.SORCERER_DRACONIC, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + []

    @progression(CharacterClass.SORCERER_DRACONIC, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + []
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.SORCERER_DRACONIC, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]
        progression.Selectors = (progression.Selectors or []) + [
        ]

    @progression(CharacterClass.SORCERER, 13)
    def level_13(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ActionResource(SpellSlot,2,7)",
            "ActionResource(SorceryPoint,2,0)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSpells(1270a6db-980b-4e3b-bf26-2924da61dfd5,1,2,SorcererSpell)"
        ]

    @progression(CharacterClass.SORCERER, 14)
    def level_14(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ActionResource(SorceryPoint,2,0)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSpells(1270a6db-980b-4e3b-bf26-2924da61dfd5,1,2,SorcererSpell)"
        ]

    @progression(CharacterClass.SORCERER, 15)
    def level_15(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ActionResource(SpellSlot,2,8)",
            "ActionResource(SorceryPoint,2,0)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSpells(1270a6db-980b-4e3b-bf26-2924da61dfd5,1,2,SorcererSpell)"
        ]

    @progression(CharacterClass.SORCERER, 16)
    def level_16(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ActionResource(SorceryPoint,2,0)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSpells(1270a6db-980b-4e3b-bf26-2924da61dfd5,1,2,SorcererSpell)"
        ]

    @progression(CharacterClass.SORCERER, 17)
    def level_17(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ActionResource(SpellSlot,2,9)",
            "ActionResource(SorceryPoint,2,0)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSpells(1270a6db-980b-4e3b-bf26-2924da61dfd5,1,2,SorcererSpell)",
            "SelectPassives(c3506532-36eb-4d18-823e-497a537a9619,1,Metamagic)",
        ]

    @progression(CharacterClass.SORCERER, 18)
    def level_18(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ActionResource(SpellSlot,2,5)",
            "ActionResource(SorceryPoint,2,0)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSpells(1270a6db-980b-4e3b-bf26-2924da61dfd5,1,2,SorcererSpell)"
        ]

    @progression(CharacterClass.SORCERER, 19)
    def level_19(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ActionResource(SpellSlot,2,6)",
            "ActionResource(SorceryPoint,2,0)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSpells(1270a6db-980b-4e3b-bf26-2924da61dfd5,1,2,SorcererSpell)"
        ]

    @progression(CharacterClass.SORCERER, 20)
    def level_20(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ActionResource(SpellSlot,2,7)",
            "ActionResource(SorceryPoint,2,0)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            "SelectSpells(1270a6db-980b-4e3b-bf26-2924da61dfd5,1,2,SorcererSpell)"
        ]


if __name__ == "__main__":
    chromatic_sorcerer = ChromaticSorcerer()
    chromatic_sorcerer.build()
