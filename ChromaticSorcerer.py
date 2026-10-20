
import os

from moddb import spells_always_prepared
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import ClassDescription, Progression
from modtools.replacers import (
    CharacterClass,
    class_description,
    DontIncludeProgression,
    progression,
    Replacer,
)


class ChromaticSorcerer(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="ChromaticSorcerer",
                         description="A class replacer for DraconicBloodline.",
                         **kwds)

        self._draconic_ancestry()
        self._elemental_affinity()

    def _draconic_ancestry(self):
        name = "DraconicAncestry_Gold"

        self.mod.add(PassiveData(
            name,
            DisplayName=self.loca(f"{name}_DisplayName", "Draconic Ancestry: Chromatic"),
            Description=self.loca(f"{name}_Description", """
                At Level 6, your spells are more powerful, and you are resistant to all damage.
            """),
            Icon="PassiveFeature_DraconicAncestry_Gold",
            Properties="Highlighted",
            Boosts=[
                "UnlockSpell(Target_Command_Container,AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf,,Charisma)",
                "UnlockSpell(Projectile_EldritchBlast,AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf,,Charisma)",
            ],
        ))

    def _elemental_affinity(self):
        damage_types = [
            "Acid",
            "Bludgeoning",
            "Cold",
            "Fire",
            "Force",
            "Lightning",
            "Necrotic",
            "Piercing",
            "Poison",
            "Psychic",
            "Radiant",
            "Slashing",
            "Thunder",
        ]
        affinities = [
            (["Black", "Copper"], "ACID", ["Resistance(Acid,Resistant)"]),
            (["Gold"], "CHROMATIC", [f"Resistance({damage_type},Resistant)" for damage_type in damage_types]),
            (["Silver", "White"], "COLD", ["Resistance(Cold,Resistant)"]),
            (["Red", "Brass"], "FIRE", ["Resistance(Fire,Resistant)"]),
            (["Blue", "Bronze"], "LIGHTNING", ["Resistance(Lightning,Resistant)"]),
            (["Green"], "POISON", ["Resistance(Poison,Resistant)"]),
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

        self.mod.add(StatusData(
            "ELEMENTALAFFINITY_CHROMATIC_EXTRA_DAMAGE_TECHNICAL",
            StatusType="BOOST",
            DisplayName=self.loca("ELEMENTALAFFINITY_CHROMATIC_EXTRA_DAMAGE_TECHNICAL", """
                Elemental Affinity: Additional Spell Damage
            """),
            Icon="PassiveFeature_ElementalAffinity_ExtraDamage",
            StackId="ELEMENTALAFFINITY_CHROMATIC_EXTRA_DAMAGE_TECHNICAL",
            Boosts="IF(IsSpell()):DamageBonus(max(0,CharismaModifier))",
            StatusPropertyFlags=[
                "DisableOverhead", "DisableCombatlog", "DisablePortraitIndicator", "ApplyToDead", "IgnoreResting"
            ],
            StatusGroups="SG_RemoveOnRespec",
        ))

        self.mod.add(PassiveData(
            "ElementalAffinity_Resistance_Check",
            DisplayName="h6948c0efg778bg41d3g88e4g9f4c658120a4;2",
            Description=self.loca("ElementalAffinity_Resistance_Check_Description", """
                You are <LSTag Tooltip="Resistant">Resistant</LSTag> to the damage type(s) associated with your draconic
                ancestry.
            """),
            Icon="Skill_Sorcerer_Passive_ElementalAffinity_Resistance",
            Properties="Highlighted",
            StatsFunctorContext="OnCreate",
            StatsFunctors=resistance_stats_functors,
        ))

        for _, affinity, resistance in affinities:
            self.mod.add(StatusData(
                f"ELEMENTALAFFINITY_{affinity}_RESISTANCE_TECHNICAL",
                StatusType="BOOST",
                DisplayName=self.loca(f"ELEMENTALAFFINITY_{affinity}_RESISTANCE_TECHNICAL", f"""
                    Elemental Affinity: {affinity.title()} Resistance
                """),
                Icon="PassiveFeature_ElementalAffinity_ExtraDamage",
                StackId="ELEMENTALAFFINITY_CHROMATIC_EXTRA_DAMAGE_TECHNICAL",
                Boosts=resistance,
                StatusPropertyFlags=[
                    "DisableOverhead", "DisableCombatlog", "DisablePortraitIndicator", "ApplyToDead", "IgnoreResting"
                ],
                StatusGroups="SG_RemoveOnRespec",
            ))

    @class_description(CharacterClass.SORCERER)
    @class_description(CharacterClass.SORCERER_DRACONIC)
    @class_description(CharacterClass.SORCERER_SHADOWMAGIC)
    @class_description(CharacterClass.SORCERER_STORM)
    @class_description(CharacterClass.SORCERER_WILDMAGIC)
    def sorcerer_can_learn_spells(self, description: ClassDescription) -> None:
        description.CanLearnSpells = True
        description.MustPrepareSpells = True

    @progression(CharacterClass.SORCERER, range(1, 21))
    @progression(CharacterClass.SORCERER, 1, is_multiclass=True)
    @progression(CharacterClass.SORCERER_DRACONIC, range(1, 21))
    @progression(CharacterClass.SORCERER_SHADOWMAGIC, range(1, 21))
    @progression(CharacterClass.SORCERER_STORM, range(1, 21))
    @progression(CharacterClass.SORCERER_WILDMAGIC, range(1, 21))
    def sorcerer_spells_always_prepared(self, progress: Progression) -> None:
        if not spells_always_prepared(progress):
            raise DontIncludeProgression()


def main() -> None:
    chromatic_sorcerer = ChromaticSorcerer(
        classes=[CharacterClass.SORCERER_DRACONIC],
        spells=2,
        actions=4,
        level_20=True,
    )
    chromatic_sorcerer.build()


if __name__ == "__main__":
    main()
