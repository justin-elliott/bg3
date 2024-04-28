#!/usr/bin/env python3
"""
Generates files for the "DaughterOfDarkness" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    BattleMagic,
    CunningActions,
    Movement,
    multiply_resources,
)
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    ClassDescription,
    Origin,
    SpellList,
)
from modtools.lsx.game import Progression
from modtools.replacers import (
    class_description,
    cleric_cantrips,
    cleric_level_1_spells,
    cleric_level_2_spells,
    cleric_level_3_spells,
    cleric_level_4_spells,
    cleric_level_5_spells,
    cleric_level_6_spells,
    origin,
    progression,
    wizard_cantrips,
    wizard_level_1_spells,
    wizard_level_2_spells,
    wizard_level_3_spells,
    wizard_level_4_spells,
    wizard_level_5_spells,
    Replacer,
)


class DaughterOfDarkness(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Channel Divinity charges)

    _args: Args
    _feat_levels: set[int]

    # Passives
    _battle_magic: str
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str

    # Spell lists
    _cunning_actions: SpellList

    @cached_property
    def _cantrips(self) -> SpellList:
        cantrips = SpellList(
            Comment="Cleric cantrips",
            Spells=sorted(set([
                *cleric_cantrips(self).Spells,
                *wizard_cantrips(self).Spells,
            ])),
            UUID=self.make_uuid("cantrips"),
        )
        self.mod.add(cantrips)
        return cantrips

    @cached_property
    def _eldritch_blast(self) -> SpellList:
        eldritch_blast = SpellList(
            Comment="Cleric Eldritch Blast cantrip",
            Spells=[
                "Projectile_EldritchBlast",
            ],
            UUID=self.make_uuid("eldritch_blast"),
        )
        self.mod.add(eldritch_blast)
        return eldritch_blast

    @cached_property
    def _level_1_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Cleric level 1 spells",
            Spells=sorted(set([
                *cleric_level_1_spells(self).Spells,
                *wizard_level_1_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_1_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_2_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Cleric level 2 spells",
            Spells=sorted(set([
                *cleric_level_2_spells(self).Spells,
                *wizard_level_2_spells(self).Spells,
            ]) - set([
                *wizard_level_1_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_2_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_3_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Cleric level 3 spells",
            Spells=sorted(set([
                *cleric_level_3_spells(self).Spells,
                *wizard_level_3_spells(self).Spells,
            ]) - set([
                *wizard_level_2_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_3_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_4_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Cleric level 4 spells",
            Spells=sorted(set([
                *cleric_level_4_spells(self).Spells,
                *wizard_level_4_spells(self).Spells,
            ]) - set([
                *wizard_level_3_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_4_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_5_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Cleric level 5 spells",
            Spells=sorted(set([
                *cleric_level_5_spells(self).Spells,
                *wizard_level_5_spells(self).Spells,
            ]) - set([
                *wizard_level_4_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_5_spells"),
        )
        self.mod.add(spells)
        return spells

    @cached_property
    def _level_6_spells(self) -> SpellList:
        spells = SpellList(
            Comment="Cleric level 6 spells",
            Spells=sorted(set([
                *cleric_level_6_spells(self).Spells,
            ])),
            UUID=self.make_uuid("level_6_spells"),
        )
        self.mod.add(spells)
        return spells

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="DaughterOfDarkness",
                         description="Changes Trickery Domain Cleric to a Cleric/Rogue/Wizard hybrid.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        # Passives
        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(4.5)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(6.0)

    @origin("Shadowheart")
    def shadowheart(self, origin: Origin) -> None:
        origin.LockClass = None

    @class_description(CharacterClass.CLERIC)
    def cleric_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6
        class_description.children.append(ClassDescription.Tags(
            Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
        ))

    @progression(CharacterClass.CLERIC, range(1, 13))
    @progression(CharacterClass.CLERIC, 1, is_multiclass=True)
    def level_1_to_12_cleric(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression, [ActionResource.CHANNEL_DIVINITY_CHARGES], self._args.actions)
        progression.Selectors = [
            selector for selector in (progression.Selectors or [])
            if not selector.startswith(f"SelectSpells({cleric_cantrips(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_1_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_2_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_3_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_4_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_5_spells(self).UUID}")
            and not selector.startswith(f"AddSpells({cleric_level_6_spells(self).UUID}")
        ] or None

    @progression(CharacterClass.CLERIC, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            "ProficiencyBonus(SavingThrow,Constitution)",
            "ActionResource(SneakAttack_Charge,1,0)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._battle_magic,
            self._fast_movement_30,
            "SculptSpells",
        ]
        progression.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            *[selector for selector in progression.Selectors if not selector.startswith("SelectSkills(")],
            f"SelectSpells({self._cantrips.UUID},4,0,,,,AlwaysPrepared)",
            f"AddSpells({self._eldritch_blast.UUID},,,,AlwaysPrepared)",
            f"AddSpells({self._level_1_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "AgonizingBlast",
            "RepellingBlast",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({CunningActions.SPELL_LIST},,,,AlwaysPrepared)",
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]

    @progression(CharacterClass.CLERIC, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "FastHands",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_2_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "DevilsSight",
        ]

    @progression(CharacterClass.CLERIC, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_45,
            "ExtraAttack",
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_30,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_3_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "ImprovedCritical",
        ]

    @progression(CharacterClass.CLERIC, 7)
    def level_7(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_4_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
        ]

    @progression(CharacterClass.CLERIC, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._fast_movement_60,
        ]
        progression.PassivesRemoved = (progression.PassivesRemoved or []) + [
            self._fast_movement_45,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_5_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "NaturesWard",
        ]

    @progression(CharacterClass.CLERIC, 11)
    def level_11(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
            "AddSpells(49cfa35d-94c9-4092-a5c6-337b7f16fd3a,,,,AlwaysPrepared)",  # Volley, Whirlwind
            f"AddSpells({self._level_6_spells.UUID})",
        ]

    @progression(CharacterClass.CLERIC, 12)
    def level_12(self, progression: Progression) -> None:
        progression.Boosts = (progression.Boosts or []) + [
            f"ActionResource(SpellSlot,{1 * self._args.spells},6)",
        ]
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "BrutalCritical",
        ]


def main():
    parser = argparse.ArgumentParser(description="A replacer for Trickery Domain Clerics.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=1,
                        help="Feat progression every n levels (defaulting to 1; feat every level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Channel Divinity) multiplier (defaulting to 2; double charges)")
    args = DaughterOfDarkness.Args(**vars(parser.parse_args()))

    daughter_of_darkness = DaughterOfDarkness(args)
    daughter_of_darkness.build()


if __name__ == "__main__":
    main()
