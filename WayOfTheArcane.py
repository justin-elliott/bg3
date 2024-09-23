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
    EmpoweredSpells,
    multiply_resources,
    spells_always_prepared,
)
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    ClassDescription,
    SpellList,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    Replacer,
    class_description,
    progression,
)
from uuid import UUID


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-g265.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class WayOfTheArcane(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Ki Points)

    WIZARD_CANTRIP_SPELL_LIST = UUID("3cae2e56-9871-4cef-bba6-96845ea765fa")
    WIZARD_LEVEL_1_SPELL_LIST = UUID("11f331b0-e8b7-473b-9d1f-19e8e4178d7d")
    WIZARD_LEVEL_2_SPELL_LIST = UUID("80c6b070-c3a6-4864-84ca-e78626784eb4")
    WIZARD_LEVEL_3_SPELL_LIST = UUID("22755771-ca11-49f4-b772-13d8b8fecd93")
    WIZARD_LEVEL_4_SPELL_LIST = UUID("820b1220-0385-426d-ae15-458dc8a6f5c0")
    WIZARD_LEVEL_5_SPELL_LIST = UUID("f781a25e-d288-43b4-bf5d-3d8d98846687")
    WIZARD_LEVEL_6_SPELL_LIST = UUID("bc917f22-7f71-4a25-9a77-7d2f91a96a65")

    ACTION_SURGE_SPELL_LIST = UUID("964e765d-5881-463e-b1b0-4fc6b8035aa8")
    FLY_SPELL_LIST = UUID("12150e11-267a-4ecc-a3cc-292c9e2a198d")

    _args: Args
    _feat_levels: set[int]

    # Passives
    _battle_magic: str
    _empowered_spells: str

    # Spells
    _bolster: str

    @cached_property
    def _arcane_manifestation(self) -> str:
        """Add the Arcane Manifestation passive, returning its name."""
        name = f"{self.mod.get_prefix()}_ArcaneManifestation"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Arcane Manifestation"}
        loca[f"{name}_Description"] = {"en": """
            Arcane energy infuses your strikes. Your melee unarmed attacks deal an additional [1].

            Whenever you deal damage with a melee unarmed attack, you gain
            <LSTag Type="Status" Tooltip="MAG_GISH_ARCANE_ACUITY">Arcane Acuity</LSTag> for 2 turns.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["DealDamage(1d4+WisdomModifier,Force)"],
            Icon="Action_Barbarian_MagicAwareness",
            Properties="Highlighted",
            Boosts=[
                "IF(IsMeleeUnarmedAttack()):CharacterUnarmedDamage(1d4+WisdomModifier,Force)",
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
        """Replaces the bonus unarmed strike class feature."""
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
        """The Slow Fall class feature as a passive."""
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
        """The Stillness of Mind class feature as a passive."""
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
    def _wholeness_of_body(self) -> str:
        """The Wholeness of Body subclass feature as a passive."""
        name = f"{self.mod.get_prefix()}_WholenessOfBody"

        HEALTH_PER_TURN = "1d4"
        KI_PER_TURN = "1"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Wholeness of Body"}
        loca[f"{name}_Description"] = {"en": """
            Gain an additional bonus action.

            While in combat, you heal [1] every turn, and restore [2]
            <LSTag Type="ActionResource" Tooltip="KiPoint">Ki Point(s)</LSTag>.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=[
                f"RegainHitPoints({HEALTH_PER_TURN})",
                str(KI_PER_TURN),
            ],
            Icon="Action_Monk_WholenessOfBody",
            Properties=["ForceShowInCC", "Highlighted", "OncePerTurn"],
            Boosts=["ActionResource(BonusActionPoint,1,0)"],
            StatsFunctorContext=["OnTurn"],
            Conditions=["not HasStatus('DOWNED') and not Dead() and Combat()"],
            StatsFunctors=[
                f"RegainHitPoints({HEALTH_PER_TURN})",
                f"RestoreResource(KiPoint,{KI_PER_TURN},0)",
            ],
        ))

        return name

    @cached_property
    def _level_1_spell_list(self) -> str:
        spell_list = str(self.make_uuid("level_1_spell_list"))
        self.mod.add(SpellList(
            Comment="Way of the Arcane level 1 spells",
            Spells=[self._bolster],
            UUID=spell_list,
        ))
        return spell_list

    @cached_property
    def _flurry_of_blows_spell_list(self) -> str:
        spell_list = str(self.make_uuid("flurry_of_blows_spell_list"))
        self.mod.add(SpellList(
            Comment="Way of the Arcane Flurry of Blows",
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
                         name="WayOfTheArcane",
                         description="Replaces the Way of Shadow Monk subclass with the Way of the Arcane.")

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
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)
        self._bolster = Bolster(self.mod).add_bolster()

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
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,6)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
        ])
        progression.Selectors = selectors

    @progression(CharacterClass.MONK, 1)
    @progression(CharacterClass.MONK, 1, is_multiclass=True)
    def level_1_multiclass(self, progression: Progression) -> None:
        progression.children = [
            Progression.Subclasses(children=[
                Progression.Subclasses.Subclass(Object="22894c32-54cf-49ea-b366-44bfcf01bb2a"),
                Progression.Subclasses.Subclass(Object="2a5e3097-384c-4d29-8d6e-054fdfd26b80"),
                Progression.Subclasses.Subclass(Object="bf46d73f-d406-4cb8-9a1d-e6e758ca02c7"),
            ]),
        ]

    @progression(CharacterClass.MONK, range(1, 21))
    @progression(CharacterClass.MONK, 1, is_multiclass=True)
    def level_1_to_12_monk(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.KI_POINTS], self._args.actions)
        spells_always_prepared(progression)

    @progression(CharacterClass.MONK, 3)
    def level_3_monk(self, progression: Progression) -> None:
        progression.children = None

    @progression(CharacterClass.MONK_SHADOW, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = [
            f"ActionResource(SpellSlot,{2 * self._args.spells},1)",
        ]
        progression.PassivesAdded = [
            "UnlockedSpellSlotLevel1",
            "Blindsight",
            "SuperiorDarkvision",
            self._battle_magic,
        ]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_CANTRIP_SPELL_LIST},3,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_1_SPELL_LIST},6,0)",
            f"AddSpells({self._level_1_spell_list},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 2)
    def level_2(self, progression: Progression) -> None:
        progression.Boosts = [
            f"ActionResource(SpellSlot,{1 * self._args.spells},1)",
        ]
        progression.PassivesAdded = ["SculptSpells"]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_LEVEL_1_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = [
            f"ActionResource(SpellSlot,{1 * self._args.spells},1)",
            f"ActionResource(SpellSlot,{2 * self._args.spells},2)",
        ]
        progression.PassivesAdded = [
            "UnlockedSpellSlotLevel2",
            "FastHands",
        ]
        progression.PassivesRemoved = [
            "FlurryOfBlowsUnlock",
            "MartialArts_BonusUnarmedStrike",
        ]
        progression.Selectors = [
            f"AddSpells({self._flurry_of_blows_spell_list},,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_2_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK, 4)
    def level_4_monk(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            *[passive for passive in progression.PassivesAdded if not passive == "SlowFall"],
            self._slow_fall,
        ]

    @progression(CharacterClass.MONK_SHADOW, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},2)"]
        progression.PassivesAdded = None
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_CANTRIP_SPELL_LIST},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_2_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{2 * self._args.spells},3)"]
        progression.PassivesAdded = ["UnlockedSpellSlotLevel3"]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_LEVEL_3_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},3)"]
        progression.PassivesAdded = [self._arcane_manifestation]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_LEVEL_3_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK, 7)
    def level_7_monk(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            *[passive for passive in progression.PassivesAdded if not passive == "StillnessOfMind"],
            self._stillness_of_mind,
        ]

    @progression(CharacterClass.MONK_SHADOW, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},4)"]
        progression.PassivesAdded = [self._wholeness_of_body]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_LEVEL_4_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},4)"]
        progression.PassivesAdded = None
        progression.Selectors = [
            f"AddSpells({self.ACTION_SURGE_SPELL_LIST},,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_4_SPELL_LIST},2,0)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,3)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.PassivesAdded = ["ImprovedCritical"]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_LEVEL_5_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},5)"]
        progression.PassivesAdded = [self._empowered_spells]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_CANTRIP_SPELL_LIST},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_5_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},6)"]
        progression.PassivesAdded = ["ExtraAttack_2"]
        progression.PassivesRemoved = ["ExtraAttack"]
        progression.Selectors = [
            f"AddSpells({self.FLY_SPELL_LIST},,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},6)"]
        progression.PassivesAdded = ["ReliableTalent"]
        progression.Selectors = [
            f"SelectSpells({self.WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]


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
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Ki) multiplier (defaulting to 2; double points)")
    args = WayOfTheArcane.Args(**vars(parser.parse_args()))

    way_of_the_arcane = WayOfTheArcane(args)
    way_of_the_arcane.build()


if __name__ == "__main__":
    main()
