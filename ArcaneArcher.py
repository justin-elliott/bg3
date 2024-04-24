#!/usr/bin/env python3
"""
Generates files for the "ArcaneArcher" mod.
"""

import argparse
import os

from dataclasses import dataclass
from moddb import (
    BattleMagic,
    EmpoweredSpells,
    Movement,
    multiply_resources,
    spells_always_prepared,
)
from modtools.lsx.game import (
    ActionResource,
    CharacterAbility,
    CharacterClass,
    ClassDescription,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    DontIncludeProgression,
    Replacer,
    class_description,
    progression,
)
from uuid import UUID


class ArcaneArcher(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots

    WIZARD_CANTRIP_SPELL_LIST = UUID("3cae2e56-9871-4cef-bba6-96845ea765fa")
    WIZARD_LEVEL_1_SPELL_LIST = UUID("11f331b0-e8b7-473b-9d1f-19e8e4178d7d")
    WIZARD_LEVEL_2_SPELL_LIST = UUID("80c6b070-c3a6-4864-84ca-e78626784eb4")
    WIZARD_LEVEL_3_SPELL_LIST = UUID("22755771-ca11-49f4-b772-13d8b8fecd93")
    WIZARD_LEVEL_4_SPELL_LIST = UUID("820b1220-0385-426d-ae15-458dc8a6f5c0")
    WIZARD_LEVEL_5_SPELL_LIST = UUID("f781a25e-d288-43b4-bf5d-3d8d98846687")
    WIZARD_LEVEL_6_SPELL_LIST = UUID("bc917f22-7f71-4a25-9a77-7d2f91a96a65")

    _args: Args
    _feat_levels: set[int]

    _spell_slots: dict[int, list[str]]

    _battle_magic: str
    _empowered_spells: str
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="ArcaneArcher",
                         description="A replacer for Hunter Rangers.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        self._spell_slots = {}

        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)

        movement = Movement(self.mod)
        self._fast_movement_30 = movement.add_fast_movement(3.0)
        self._fast_movement_45 = movement.add_fast_movement(4.5)
        self._fast_movement_60 = movement.add_fast_movement(6.0)

    @class_description(CharacterClass.RANGER)
    def ranger_description(self, class_description: ClassDescription) -> None:
        class_description.CanLearnSpells = True
        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.MustPrepareSpells = True
        class_description.children.append(ClassDescription.Tags(
            Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
        ))

    @class_description(CharacterClass.RANGER_HUNTER)
    def hunter_description(self, class_description: ClassDescription) -> None:
        class_description.MustPrepareSpells = True

    @progression(CharacterClass.RANGER, 1)
    def level_1_ranger(self, progression: Progression) -> None:
        selectors = progression.Selectors or []
        selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
        selectors.extend([
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @progression(CharacterClass.RANGER, range(1, 13))
    @progression(CharacterClass.RANGER, 1, is_multiclass=True)
    def level_1_to_12_ranger(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        spells_always_prepared(progression)

        if progression.Level >= 3:
            self._spell_slots[progression.Level] = [
                boost for boost in (progression.Boosts or []) if boost.startswith("ActionResource(SpellSlot,")
            ]
            progression.Boosts = [
                boost for boost in (progression.Boosts or []) if not boost.startswith("ActionResource(SpellSlot,")
            ] or None

    @progression(CharacterClass.RANGER_BEASTMASTER, range(3, 13))
    @progression(CharacterClass.RANGER_GLOOMSTALKER, range(3, 13))
    def level_3_to_12_spell_slots(self, progression: Progression) -> None:
        if spell_slots := self._spell_slots[progression.Level]:
            progression.Boosts = (progression.Boosts or []) + spell_slots
        else:
            raise DontIncludeProgression()

    @progression(CharacterClass.RANGER_BEASTMASTER, range(3, 13))
    @progression(CharacterClass.RANGER_GLOOMSTALKER, range(3, 13))
    @progression(CharacterClass.RANGER_HUNTER, range(3, 13))
    def level_3_to_12_add_spells(self, progression: Progression) -> None:
        if not spells_always_prepared(progression):
            raise DontIncludeProgression()

    @progression(CharacterClass.RANGER_HUNTER, 3)
    def level_3(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{2 * self._args.spells},1)",
            f"ActionResource(SpellSlot,{2 * self._args.spells},2)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._battle_magic,
            self._fast_movement_30,
            "SculptSpells",
            "UnlockedSpellSlotLevel2",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_CANTRIP_SPELL_LIST},4,0,,,,AlwaysPrepared)",
            f"SelectSpells({self.WIZARD_LEVEL_2_SPELL_LIST},3,0)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 4)
    def level_4(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},2)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_LEVEL_2_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{2 * self._args.spells},3)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["UnlockedSpellSlotLevel3"]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_LEVEL_3_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 6)
    def level_6(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},3)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_45,
            "PotentCantrip",
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_30,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_LEVEL_3_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_LEVEL_4_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 8)
    def level_8(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_LEVEL_4_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 9)
    def level_9(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},4)",
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_60,
            "BrutalCritical",
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_45,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_LEVEL_5_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 10)
    def level_10(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},5)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._empowered_spells]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_LEVEL_5_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ExtraAttack_2"]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + ["ExtraAttack"]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_LEVEL_6_SPELL_LIST},1,0)",
        ]

    @progression(CharacterClass.RANGER_HUNTER, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self.WIZARD_LEVEL_6_SPELL_LIST},1,0)",
        ]


def main():
    parser = argparse.ArgumentParser(description="A replacer for Hunter Rangers.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=1,
                        help="Feat progression every n levels (defaulting to 1; feat every level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    args = ArcaneArcher.Args(**vars(parser.parse_args()))

    arcane_archer = ArcaneArcher(args)
    arcane_archer.build()


if __name__ == "__main__":
    main()
