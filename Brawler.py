#!/usr/bin/env python3
"""
Generates files for the "Brawler" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import multiply_resources
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    ClassDescription,
    LevelMapSeries,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    Replacer,
    class_description,
    progression,
)
from uuid import UUID


class Brawler(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        actions: int  # Multiplier for other action resources (Rage Charges)

    FLURRY_OF_BLOWS_SPELL_LIST = UUID("6566d841-ef96-4e13-ac40-c40f44c5e08b")

    _args: Args
    _feat_levels: set[int]

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Brawler",
                         description="Replaces the Berserker Barbarian subclass with an unarmed Brawler.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

    @cached_property
    def unarmed_damage(self) -> str:
        name = f"{self.mod.get_prefix()}_UnarmedDamage"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Unarmed Damage"}
        loca[f"{name}_Description"] = {"en": """
            Unarmed attacks, and attacks with weapons with which you have
            <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag>, and which do not have the
            <LSTag Tooltip="TwoHanded">two-handed weapon</LSTag> or <LSTag Tooltip="Heavy">heavy</LSTag> properties,
            deal [1], unless their normal damage is higher.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=[f"DealDamage(LevelMapValue({name}_Level),Bludgeoning)"],
            Icon="PassiveFeature_MartialArts_UnarmedDamage",
            Properties=["Highlighted", "ForceShowInCC"],
            Boosts=[f"MonkWeaponDamageDiceOverride(LevelMapValue({name}_Level))"],
        ))

        self.mod.add(LevelMapSeries(
            **{f"Level{level}": "1d6" for level in range(1, 6)},
            **{f"Level{level}": "2d6" for level in range(6, 10)},
            **{f"Level{level}": "3d6" for level in range(10, 13)},
            Name=f"{name}_Level",
            UUID=self.make_uuid(f"{name}_Level"),
        ))

        return name

    @class_description(CharacterClass.BARBARIAN_BERSERKER)
    def brawler_description(self, class_description: ClassDescription) -> None:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_DisplayName"] = {"en": "Brawler"}
        loca[f"{self.mod.get_prefix()}_Description"] = {"en": """
            Forget fancy footwork and glittering swords. Brawlers are the bare-knuckle bruisers of the adventuring
            world. They specialize in raw, brutal fighting, turning their bodies into weapons and dominating the
            battlefield with punches, throws, and anything they can grab.
            """}

        class_description.DisplayName = loca[f"{self.mod.get_prefix()}_DisplayName"]
        class_description.Description = loca[f"{self.mod.get_prefix()}_Description"]

    @progression(CharacterClass.BARBARIAN, range(1, 13))
    @progression(CharacterClass.BARBARIAN, 1, is_multiclass=True)
    def level_1_to_12_barbarian(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.RAGE_CHARGES], self._args.actions)

    @progression(CharacterClass.BARBARIAN, 1)
    def feature_test(self, progression: Progression):
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self.unarmed_damage,
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = [
        ]
        progression.PassivesAdded = [
            self.unarmed_damage,
        ]
        progression.Selectors = [
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = [
        ]
        progression.PassivesAdded = [
        ]
        progression.Selectors = [
        ]

    @progression(CharacterClass.BARBARIAN_BERSERKER, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = [
        ]
        progression.PassivesAdded = [
        ]
        progression.Selectors = [
        ]


def main():
    parser = argparse.ArgumentParser(description="Replaces the Berserker Barbarian subclass with an unarmed Brawler.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=2,
                        help="Feat progression every n levels (defaulting to 2; feat every other level)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Rage charges) multiplier (defaulting to 2; double charges)")
    args = Brawler.Args(**vars(parser.parse_args()))

    brawler = Brawler(args)
    brawler.build()


if __name__ == "__main__":
    main()
