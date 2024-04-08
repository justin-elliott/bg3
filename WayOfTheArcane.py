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
from modtools.replacers import (
    DontIncludeSpellList,
    Replacer,
    class_description,
    progression,
    spell_list,
)
from uuid import UUID


class WayOfTheArcane(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Channel Divinity charges)

    CLERIC_CANTRIP_SPELL_LIST = UUID("2f43a103-5bf1-4534-b14f-663decc0c525")
    CLERIC_LEVEL_1_SPELL_LIST = UUID("269d1a3b-eed8-4131-8901-a562238f5289")
    CLERIC_LEVEL_2_SPELL_LIST = UUID("2968a3e6-6c8a-4c2e-882a-ad295a2ad8ac")
    CLERIC_LEVEL_3_SPELL_LIST = UUID("21be0992-499f-4c7a-a77a-4430085e947a")
    CLERIC_LEVEL_4_SPELL_LIST = UUID("37e9b20b-5fd1-45c5-b1c5-159c42397c83")
    CLERIC_LEVEL_5_SPELL_LIST = UUID("b73aeea5-1ff9-4cac-b61d-b5aa6dfe31c2")
    CLERIC_LEVEL_6_SPELL_LIST = UUID("f8ba7b05-1237-4eaa-97fa-1d3623d5862b")

    DRUID_CANTRIP_SPELL_LIST = UUID("b8faf12f-ca42-45c0-84f8-6951b526182a")
    DRUID_LEVEL_1_SPELL_LIST = UUID("2cd54137-2fe5-4100-aad3-df64735a8145")
    DRUID_LEVEL_2_SPELL_LIST = UUID("92126d17-7f1a-41d2-ae6c-a8d254d2b135")
    DRUID_LEVEL_3_SPELL_LIST = UUID("3156daf5-9266-41d0-b52c-5bc559a98654")
    DRUID_LEVEL_4_SPELL_LIST = UUID("09c326c9-672c-4198-a4c0-6f07323bde27")
    DRUID_LEVEL_5_SPELL_LIST = UUID("ff711c12-b59f-4fde-b9ea-6e5c38ec8f23")
    DRUID_LEVEL_6_SPELL_LIST = UUID("6a4e2167-55f3-4ba8-900f-14666b293e93")

    WARLOCK_CANTRIP_SPELL_LIST = UUID("f5c4af9c-5d8d-4526-9057-94a4b243cd40")
    WARLOCK_LEVEL_1_SPELL_LIST = UUID("4823a292-f584-4f7f-8434-6630c72e5411")
    WARLOCK_LEVEL_2_SPELL_LIST = UUID("835aeca7-c64a-4aaa-a25c-143aa14a5cec")
    WARLOCK_LEVEL_3_SPELL_LIST = UUID("5dec41aa-f16a-434e-b209-50c07e64e4ed")
    WARLOCK_LEVEL_4_SPELL_LIST = UUID("7ad7dbd0-751b-4bcd-8034-53bcc7bfb19d")
    WARLOCK_LEVEL_5_SPELL_LIST = UUID("deab57bf-4eec-4085-82f7-87335bce3f5d")

    WIZARD_CANTRIP_SPELL_LIST = UUID("3cae2e56-9871-4cef-bba6-96845ea765fa")
    WIZARD_LEVEL_1_SPELL_LIST = UUID("11f331b0-e8b7-473b-9d1f-19e8e4178d7d")
    WIZARD_LEVEL_2_SPELL_LIST = UUID("80c6b070-c3a6-4864-84ca-e78626784eb4")
    WIZARD_LEVEL_3_SPELL_LIST = UUID("22755771-ca11-49f4-b772-13d8b8fecd93")
    WIZARD_LEVEL_4_SPELL_LIST = UUID("820b1220-0385-426d-ae15-458dc8a6f5c0")
    WIZARD_LEVEL_5_SPELL_LIST = UUID("f781a25e-d288-43b4-bf5d-3d8d98846687")
    WIZARD_LEVEL_6_SPELL_LIST = UUID("bc917f22-7f71-4a25-9a77-7d2f91a96a65")

    FLURRY_OF_BLOWS_SPELL_LIST = UUID("6566d841-ef96-4e13-ac40-c40f44c5e08b")
    WHOLENESS_OF_BODY_SPELL_LIST = UUID("9487f3bd-1763-4c7f-913d-8cb7eb9052c5")
    FLY_SPELL_LIST = UUID("12150e11-267a-4ecc-a3cc-292c9e2a198d")

    _args: Args
    _feat_levels: set[int]

    # Passives
    _battle_magic: str
    _empowered_spells: str
    _pack_mule: str
    _warding: str

    # spells
    _bolster: str
    _shadow_step: str

    _cantrip_spell_list: SpellList
    _level_1_spell_list: SpellList
    _level_2_spell_list: SpellList
    _level_3_spell_list: SpellList
    _level_4_spell_list: SpellList
    _level_5_spell_list: SpellList
    _level_6_spell_list: SpellList

    @cached_property
    def _shadow_step_spell_list(self) -> str:
        spell_list = str(self.make_uuid("shadow_step_spell_list"))
        self.mod.add(SpellList(
            Comment="Monk Shadow Step spell list",
            Spells=[self._shadow_step],
            UUID=spell_list,
        ))
        return spell_list

    @cached_property
    def _arcane_manifestation(self) -> str:
        """Add the Arcane Manifestation passive, returning its name."""
        name = f"{self.mod.get_prefix()}_ArcaneManifestation"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Arcane Manifestation"}
        loca[f"{name}_Description"] = {"en": """
            Arcane energy infuses your strikes. Your unarmed attacks deal an additional [1].
            """}

        self.mod.add(PassiveData(
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

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="WayOfTheArcane",
                         description="Replaces the Way of Shadow Monk subclass with the Way of the Arcane.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)
        self._pack_mule = PackMule(self.mod).add_pack_mule(2.0)
        self._warding = Defense(self.mod).add_warding()

        self._bolster = Bolster(self.mod).add_bolster()
        self._shadow_step = Movement(self.mod).add_shadow_step_monk("Movement:Distance*0.5")

        self._cantrip_spell_list = SpellList(
            Comment="Monk cantrips",
            Spells=[self._bolster],
            UUID=self.make_uuid("cantrip_spell_list"),
        )
        self.mod.add(self._cantrip_spell_list)

        self._level_1_spell_list = SpellList(
            Comment="Monk level 1 spells",
            Spells=[],
            UUID=self.make_uuid("level_1_spell_list"),
        )
        self.mod.add(self._level_1_spell_list)

        self._level_2_spell_list = SpellList(
            Comment="Monk level 2 spells",
            Spells=[],
            UUID=self.make_uuid("level_2_spell_list"),
        )
        self.mod.add(self._level_2_spell_list)

        self._level_3_spell_list = SpellList(
            Comment="Monk level 3 spells",
            Spells=[],
            UUID=self.make_uuid("level_3_spell_list"),
        )
        self.mod.add(self._level_3_spell_list)

        self._level_4_spell_list = SpellList(
            Comment="Monk level 4 spells",
            Spells=[],
            UUID=self.make_uuid("level_4_spell_list"),
        )
        self.mod.add(self._level_4_spell_list)

        self._level_5_spell_list = SpellList(
            Comment="Monk level 5 spells",
            Spells=[],
            UUID=self.make_uuid("level_5_spell_list"),
        )
        self.mod.add(self._level_5_spell_list)

        self._level_6_spell_list = SpellList(
            Comment="Monk level 6 spells",
            Spells=[],
            UUID=self.make_uuid("level_6_spell_list"),
        )
        self.mod.add(self._level_6_spell_list)

    @class_description(CharacterClass.MONK)
    def monk_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6

        class_description.CanLearnSpells = False
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

    def _update_spell_list(self,
                           destination_spell_list: SpellList,
                           source_spell_list: SpellList,
                           exclude_spell_lists: list[SpellList] = []) -> None:
        spells = set(destination_spell_list.Spells) | set(source_spell_list.Spells)
        for exclude_spell_list in exclude_spell_lists:
            spells -= set(exclude_spell_list.Spells)
        destination_spell_list.Spells = [spell for spell in sorted(spells)]
        raise DontIncludeSpellList()

    @spell_list(CLERIC_CANTRIP_SPELL_LIST)
    @spell_list(DRUID_CANTRIP_SPELL_LIST)
    @spell_list(WARLOCK_CANTRIP_SPELL_LIST)
    @spell_list(WIZARD_CANTRIP_SPELL_LIST)
    def _update_cantrip_spell_list(self, source_spell_list: SpellList) -> str:
        self._update_spell_list(self._cantrip_spell_list, source_spell_list)

    @spell_list(CLERIC_LEVEL_1_SPELL_LIST)
    @spell_list(DRUID_LEVEL_1_SPELL_LIST)
    @spell_list(WARLOCK_LEVEL_1_SPELL_LIST)
    @spell_list(WIZARD_LEVEL_1_SPELL_LIST)
    def _update_level_1_spell_list(self, source_spell_list: SpellList) -> str:
        self._update_spell_list(self._level_1_spell_list, source_spell_list)

    @spell_list(CLERIC_LEVEL_2_SPELL_LIST)
    @spell_list(DRUID_LEVEL_2_SPELL_LIST)
    @spell_list(WARLOCK_LEVEL_2_SPELL_LIST)
    @spell_list(WIZARD_LEVEL_2_SPELL_LIST)
    def _update_level_2_spell_list(self, source_spell_list: SpellList) -> str:
        self._update_spell_list(self._level_2_spell_list, source_spell_list,
                                [self._level_1_spell_list])

    @spell_list(CLERIC_LEVEL_3_SPELL_LIST)
    @spell_list(DRUID_LEVEL_3_SPELL_LIST)
    @spell_list(WARLOCK_LEVEL_3_SPELL_LIST)
    @spell_list(WIZARD_LEVEL_3_SPELL_LIST)
    def _update_level_3_spell_list(self, source_spell_list: SpellList) -> str:
        self._update_spell_list(self._level_3_spell_list, source_spell_list,
                                [self._level_1_spell_list, self._level_2_spell_list])

    @spell_list(CLERIC_LEVEL_4_SPELL_LIST)
    @spell_list(DRUID_LEVEL_4_SPELL_LIST)
    @spell_list(WARLOCK_LEVEL_4_SPELL_LIST)
    @spell_list(WIZARD_LEVEL_4_SPELL_LIST)
    def _update_level_4_spell_list(self, source_spell_list: SpellList) -> str:
        self._update_spell_list(self._level_4_spell_list, source_spell_list,
                                [self._level_1_spell_list, self._level_2_spell_list, self._level_3_spell_list])

    @spell_list(CLERIC_LEVEL_5_SPELL_LIST)
    @spell_list(DRUID_LEVEL_5_SPELL_LIST)
    @spell_list(WARLOCK_LEVEL_5_SPELL_LIST)
    @spell_list(WIZARD_LEVEL_5_SPELL_LIST)
    def _update_level_5_spell_list(self, source_spell_list: SpellList) -> str:
        self._update_spell_list(self._level_5_spell_list, source_spell_list,
                                [self._level_1_spell_list, self._level_2_spell_list, self._level_3_spell_list,
                                 self._level_4_spell_list])

    @spell_list(CLERIC_LEVEL_6_SPELL_LIST)
    @spell_list(DRUID_LEVEL_6_SPELL_LIST)
    @spell_list(WIZARD_LEVEL_6_SPELL_LIST)
    def _update_level_6_spell_list(self, source_spell_list: SpellList) -> str:
        self._update_spell_list(self._level_6_spell_list, source_spell_list,
                                [self._level_1_spell_list, self._level_2_spell_list, self._level_3_spell_list,
                                 self._level_4_spell_list, self._level_5_spell_list])

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
        progression.children = [
            Progression.Subclasses(children=[
                Progression.Subclasses.Subclass(Object="22894c32-54cf-49ea-b366-44bfcf01bb2a"),
                Progression.Subclasses.Subclass(Object="2a5e3097-384c-4d29-8d6e-054fdfd26b80"),
                Progression.Subclasses.Subclass(Object="bf46d73f-d406-4cb8-9a1d-e6e758ca02c7"),
            ]),
        ]

    @progression(CharacterClass.MONK, range(1, 13))
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
            self._pack_mule,
            self._warding,
        ]
        progression.Selectors = [
            f"SelectSpells({self._cantrip_spell_list.UUID},4,0,,,,AlwaysPrepared)",
            f"AddSpells({self._level_1_spell_list.UUID})",
        ]

    @progression(CharacterClass.MONK_SHADOW, 2)
    def level_2(self, progression: Progression) -> None:
        progression.Boosts = [
            f"ActionResource(SpellSlot,{1 * self._args.spells},1)",
        ]
        progression.PassivesAdded = ["SculptSpells"]
        progression.Selectors = None

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
        ]
        progression.Selectors = [
            f"AddSpells({self._level_2_spell_list.UUID})",
            f"AddSpells({self.FLURRY_OF_BLOWS_SPELL_LIST},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},2)"]
        progression.PassivesAdded = None
        progression.Selectors = [
            f"SelectSpells({self._cantrip_spell_list.UUID},1,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{2 * self._args.spells},3)"]
        progression.PassivesAdded = ["UnlockedSpellSlotLevel3"]
        progression.Selectors = [
            f"AddSpells({self._level_3_spell_list.UUID})",
            f"AddSpells({self._shadow_step_spell_list},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},3)"]
        progression.PassivesAdded = [self._arcane_manifestation]
        progression.Selectors = [
            f"AddSpells({self.WHOLENESS_OF_BODY_SPELL_LIST},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},4)"]
        progression.PassivesAdded = ["ImprovedCritical"]
        progression.Selectors = [
            f"AddSpells({self._level_4_spell_list.UUID})",
        ]

    @progression(CharacterClass.MONK_SHADOW, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},4)"]
        progression.PassivesAdded = None
        progression.Selectors = None

    @progression(CharacterClass.MONK_SHADOW, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.PassivesAdded = ["BrutalCritical"]
        progression.Selectors = [
            f"AddSpells({self._level_5_spell_list.UUID})",
        ]

    @progression(CharacterClass.MONK_SHADOW, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},5)"]
        progression.PassivesAdded = [self._empowered_spells]
        progression.Selectors = [
            f"SelectSpells({self._cantrip_spell_list.UUID},1,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},6)"]
        progression.PassivesAdded = ["ExtraAttack_2"]
        progression.PassivesRemoved = ["ExtraAttack"]
        progression.Selectors = [
            f"AddSpells({self.FLY_SPELL_LIST},,,,AlwaysPrepared)",
            f"AddSpells({self._level_6_spell_list.UUID})",
        ]

    @progression(CharacterClass.MONK_SHADOW, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = [f"ActionResource(SpellSlot,{1 * self._args.spells},6)"]
        progression.PassivesAdded = ["ReliableTalent"]
        progression.Selectors = None


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
