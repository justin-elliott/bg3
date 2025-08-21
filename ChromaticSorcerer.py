
import os

from moddb import (
    Bolster,
    Movement,
    PackMule,
)
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
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

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Draconic Ancestry: Chromatic"}
        loca[f"{name}_Description"] = {"en": """
            At Level 6, your spells are more powerful, and you are resistant to all damage.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Gold",
            Properties="Highlighted",
            Boosts=[
                "UnlockSpell(Target_Command_Container,AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf,,Charisma)",
                "UnlockSpell(Projectile_EldritchBlast,AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf,,Charisma)",
            ],
        ))

    def _elemental_affinity(self):
        loca = self.mod.get_localization()

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

    @progression(CharacterClass.SORCERER_DRACONIC, 1)
    def draconicbloodline_level_1(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 2)
    def draconicbloodline_level_2(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 3)
    def draconicbloodline_level_3(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 4)
    def draconicbloodline_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 5)
    def draconicbloodline_level_5(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 6)
    def draconicbloodline_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 7)
    def draconicbloodline_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 8)
    def draconicbloodline_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 9)
    def draconicbloodline_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 10)
    def draconicbloodline_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 11)
    def draconicbloodline_level_11(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 12)
    def draconicbloodline_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 13)
    def draconicbloodline_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 14)
    def draconicbloodline_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 15)
    def draconicbloodline_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 16)
    def draconicbloodline_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 17)
    def draconicbloodline_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 18)
    def draconicbloodline_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 19)
    def draconicbloodline_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_DRACONIC, 20)
    def draconicbloodline_level_20(self, _: Progression) -> None:
        raise DontIncludeProgression()


def main() -> None:
    chromatic_sorcerer = ChromaticSorcerer(
        classes=[CharacterClass.SORCERER_DRACONIC],
        feats=2,
        spells=2,
        warlock_spells=1,
        actions=2,
        skills=None,
        expertise=None,
        full_caster=False,
    )
    chromatic_sorcerer.build()


if __name__ == "__main__":
    main()
