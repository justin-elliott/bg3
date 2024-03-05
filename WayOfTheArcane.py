#!/usr/bin/env python3
"""
Generates files for the "WayOfTheArcane" mod.
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
    Movement,
    PackMule,
    multiply_resources,
    spells_always_prepared,
)
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    ClassDescription,
)
from modtools.lsx.game import Progression, SpellList
from modtools.mod import Mod
from modtools.replacers import (
    class_description,
    progression,
    Replacer,
)
from uuid import UUID


def arcane_manifestation(mod: Mod) -> str:
    """Add the Arcane Manifestation passive, returning its name."""
    name = f"{mod.get_prefix()}_ArcaneManifestation"

    loca = mod.get_localization()
    loca[f"{name}_DisplayName"] = {"en": "Arcane Manifestation"}
    loca[f"{name}_Description"] = {"en": """
        Arcane energy infuses your strikes. Your unarmed attacks deal an additional [1].
        """}

    mod.add(PassiveData(
        name,
        DisplayName=loca[f"{name}_DisplayName"],
        Description=loca[f"{name}_Description"],
        DescriptionParams="DealDamage(1d4+WisdomModifier,Force)",
        Icon="Action_Barbarian_MagicAwareness",
        Properties="Highlighted",
        Boosts=[
            "IF(IsMeleeUnarmedAttack()):CharacterUnarmedDamage(1d4+WisdomModifier,Force)",
            "UnlockSpellVariant(MeleeUnarmedAttackCheck(),ModifyTargetRadius(Multiplicative,1))",
        ],
    ))

    return name


class WayOfTheArcane(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Channel Divinity charges)

    WIZARD_CANTRIP_SPELL_LIST = UUID("3cae2e56-9871-4cef-bba6-96845ea765fa")
    WIZARD_LEVEL_1_SPELL_LIST = UUID("11f331b0-e8b7-473b-9d1f-19e8e4178d7d")
    WIZARD_LEVEL_2_SPELL_LIST = UUID("80c6b070-c3a6-4864-84ca-e78626784eb4")
    WIZARD_LEVEL_3_SPELL_LIST = UUID("22755771-ca11-49f4-b772-13d8b8fecd93")
    WIZARD_LEVEL_4_SPELL_LIST = UUID("820b1220-0385-426d-ae15-458dc8a6f5c0")
    WIZARD_LEVEL_5_SPELL_LIST = UUID("f781a25e-d288-43b4-bf5d-3d8d98846687")
    WIZARD_LEVEL_6_SPELL_LIST = UUID("bc917f22-7f71-4a25-9a77-7d2f91a96a65")

    WHOLENESS_OF_BODY_SPELL_LIST = UUID("9487f3bd-1763-4c7f-913d-8cb7eb9052c5")
    FLY_SPELL_LIST = UUID("12150e11-267a-4ecc-a3cc-292c9e2a198d")

    _args: Args
    _feat_levels: set[int]

    # Passives
    _battle_magic: str
    _empowered_spells: str
    _arcane_manifestation: str
    _pack_mule: str
    _warding: str

    # spells
    _bolster: str
    _shadow_step: str

    @cached_property
    def _level_1_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_1_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Monk level 1",
            Spells=[self._bolster],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_5_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_5_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Monk level 5",
            Spells=[self._shadow_step],
            UUID=spelllist,
        ))
        return spelllist

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="WayOfTheArcane",
                         description="Replaces the Way of Shadow Monk subclass with the Way of the Arcane.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)
        self._arcane_manifestation = arcane_manifestation(self.mod)
        self._pack_mule = PackMule(self.mod).add_pack_mule(2.0)
        self._warding = Defense(self.mod).add_warding()

        self._bolster = Bolster(self.mod).add_bolster()
        self._shadow_step = Movement(self.mod).add_shadow_step("Movement:Distance*0.5")

    @class_description(CharacterClass.MONK)
    def monk_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6

        class_description.CanLearnSpells = True
        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.MustPrepareSpells = True

        class_description.children.append(ClassDescription.Tags(
            Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
        ))

    @class_description(CharacterClass.MONK_SHADOW)
    def monk_shadow_description(self, class_description: ClassDescription) -> None:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_DisplayName"] = {"en": "Way of the Arcane"}
        loca[f"{self.mod.get_prefix()}_Description"] = {"en": """
            You seek mastery over mind and body. Your Ki connects you to the Weave.
            """}

        class_description.DisplayName = loca[f"{self.mod.get_prefix()}_DisplayName"]
        class_description.Description = loca[f"{self.mod.get_prefix()}_Description"]

        class_description.MustPrepareSpells = True

    @progression(CharacterClass.MONK, 1)
    def level_1_monk(self, progression: Progression) -> None:
        selectors = progression.Selectors or []
        selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
        selectors.extend([
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @progression(CharacterClass.MONK, 1)
    @progression(CharacterClass.MONK, 1, is_multiclass=True)
    def level_1_multiclass(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_1_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.MONK, range(1, 13))
    @progression(CharacterClass.MONK, 1, is_multiclass=True)
    def level_1_to_12_monk(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.KI_POINTS], self._args.actions)
        spells_always_prepared(progression)

    @progression(CharacterClass.MONK_SHADOW, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = [
            f"ActionResource(SpellSlot,{4 * self._args.spells},1)"
            f"ActionResource(SpellSlot,{2 * self._args.spells},2)"
        ]
        progression.PassivesAdded = [
            "UnlockedSpellSlotLevel1",
            "UnlockedSpellSlotLevel2",
            "Blindsight",
            "SuperiorDarkvision",
            self._battle_magic,
            self._pack_mule,
            self._warding
        ]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_CANTRIP_SPELL_LIST},3,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_2_SPELL_LIST},3,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},2)"]
        progression.PassivesAdded = ["JackOfAllTrades"]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_CANTRIP_SPELL_LIST},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_2_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{2 * self._args.spells},3)"]
        progression.PassivesAdded = ["UnlockedSpellSlotLevel3"]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_LEVEL_3_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},3)"]
        progression.PassivesAdded = [self._arcane_manifestation]
        progression.Selectors = [
            f"AddSpells({self.WHOLENESS_OF_BODY_SPELL_LIST},,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_3_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},4)"]
        progression.PassivesAdded = ["ImprovedCritical"]
        progression.Selectors = [f"SelectSpells({self.WIZARD_LEVEL_4_SPELL_LIST},1,0)"]

    @progression(CharacterClass.MONK_SHADOW, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},4)"]
        progression.PassivesAdded = ["FastHands"]
        progression.Selectors = [f"SelectSpells({self.WIZARD_LEVEL_4_SPELL_LIST},1,0)"]

    @progression(CharacterClass.MONK_SHADOW, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)"
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)"
        ]
        progression.PassivesAdded = ["BrutalCritical"]
        progression.Selectors = [f"SelectSpells({self.WIZARD_LEVEL_5_SPELL_LIST},1,0)"]

    @progression(CharacterClass.MONK_SHADOW, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},5)"]
        progression.PassivesAdded = [self._empowered_spells]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_CANTRIP_SPELL_LIST},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_5_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},6)"]
        progression.PassivesAdded = ["ExtraAttack_2"]
        progression.PassivesRemoved = ["ExtraAttack"]
        progression.Selectors = [
            f"AddSpells({self.FLY_SPELL_LIST},,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_6_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},6)"]
        progression.PassivesAdded = ["ReliableTalent"]
        progression.Selectors = [f"SelectSpells({self.WIZARD_LEVEL_6_SPELL_LIST},1,0)"]


def main():
    parser = argparse.ArgumentParser(description="A replacer for Way of Shadow Monks.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=1,
                        help="Feat progression every n levels (defaulting to 1; feat every level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Ki) multiplier (defaulting to 2; double points)")
    args = WayOfTheArcane.Args(**vars(parser.parse_args()))

    way_of_the_arcane = WayOfTheArcane(args)
    way_of_the_arcane.build()


if __name__ == "__main__":
    main()
