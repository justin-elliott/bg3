#!/usr/bin/env python3
"""
Generates files for the "Pyromancy" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    Bolster,
    Defense,
    PackMule,
    multiply_resources,
    spells_always_prepared,
)
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    ClassDescription,
)
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    class_description,
    progression,
    Replacer,
)


class Pyromancy(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Sorcery Points)

    _args: Args
    _feat_levels: set[int]

    # Passives
    _pack_mule: str
    _warding: str

    # spells
    _bolster: str

    @cached_property
    def _firewalk(self) -> str:
        """Add the Firewalk spell, returning its name."""
        pass

    @cached_property
    def _forged_in_flames(self) -> str:
        """Add the Forged in Flames passive, returning its name."""
        name = f"{self._mod.get_prefix()}_ForgedInFlames"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Forged in Flames"}
        loca[f"{name}_Description"] = {"en": """
            You have <LSTag Tooltip="Resistant">Resistance</LSTag> to Fire damage, and cannot be
            <LSTag Type="Status" Tooltip="BURNING">Burned</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Gold",
            Properties=["Highlighted"],
            Boosts=[
                "Resistance(Fire,Resistant);StatusImmunity(BURNING)",
            ],
        ))

        return name

    @cached_property
    def _overheat(self) -> str:
        """Add the Overheat passive, returning its name."""
        name = f"{self._mod.get_prefix()}_Overheat"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Overheat"}
        loca[f"{name}_Description"] = {"en": """
            Your fire spells burn hotter, ignoring resistance, and dealing additional damage equal to your
            <LSTag Tooltip="Charisma">Charisma</LSTag> <LSTag Tooltip="AbilityModifier">Modifier</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Brass",
            Properties=["Highlighted"],
            Boosts=[
                "IgnoreResistance(Fire,Resistant)",
                "IF(IsSpell() and IsDamageTypeFire()):DamageBonus(max(0,CharismaModifier))",
            ],
        ))

        return name

    @cached_property
    def _level_1_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_1_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Sorcerer level 1",
            Spells=[self._bolster, "Projectile_FireBolt", "Shout_HellishRebuke", "Zone_BurningHands"],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_3_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_3_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Sorcerer level 3",
            Spells=["Target_HeatMetal", "Projectile_ScorchingRay"],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_5_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_5_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Sorcerer level 5",
            Spells=["Projectile_Fireball"],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_7_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_7_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Sorcerer level 7",
            Spells=["Shout_FireShield", "Wall_WallOfFire"],
            UUID=spelllist,
        ))
        return spelllist

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Pyromancy",
                         description="A replacer for Wild Magic Sorcery.")

        self._args = args
        self._feat_levels = frozenset(range(max(args.feats, 2), 13, args.feats))

        self._pack_mule = PackMule(self.mod).add_pack_mule(2.0)
        self._warding = Defense(self.mod).add_warding()

        self._bolster = Bolster(self.mod).add_bolster()

    @class_description(CharacterClass.SORCERER)
    def sorcerer_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6

    @class_description(CharacterClass.SORCERER_WILDMAGIC)
    def sorcerer_pyromancy_description(self, class_description: ClassDescription) -> None:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_DisplayName"] = {"en": "Pyromancy"}
        loca[f"{self.mod.get_prefix()}_Description"] = {"en": """
            Flickering flames dance in your fingertips, a primal power yearning to be unleashed. You are not just a
            sorcerer, but a conduit, channeling the raw essence of fire into searing spells and devastating displays.
            Heat thrums within you, a constant ember waiting to ignite. Are you a fiery prodigy, born with an innate
            connection to the inferno? Or did you forge your bond through desperation, pushing the boundaries of magic
            until it burned bright as the sun?
            """}

        class_description.DisplayName = loca[f"{self.mod.get_prefix()}_DisplayName"]
        class_description.Description = loca[f"{self.mod.get_prefix()}_Description"]

    @progression(CharacterClass.SORCERER, 1)
    def level_1_sorcerer(self, progression: Progression) -> None:
        selectors = progression.Selectors or []
        selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
        selectors.extend([
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @progression(CharacterClass.SORCERER, range(1, 13))
    @progression(CharacterClass.SORCERER, 1, is_multiclass=True)
    def level_1_to_12_sorcerer(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression, [ActionResource.SORCERY_POINTS], self._args.actions)
        spells_always_prepared(progression)

    @progression(CharacterClass.SORCERER_WILDMAGIC, 1)
    def level_1(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            self._forged_in_flames,
            self._pack_mule,
            self._warding,
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"AddSpells({self._level_1_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 2)
    def level_2(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.SORCERER_WILDMAGIC, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [
            "Blindsight",
            "SuperiorDarkvision",
        ]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self._level_3_spell_list},3,0,,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["JackOfAllTrades"]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 5)
    def level_5(self, progression: Progression) -> None:
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self._level_5_spell_list},1,0)",
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + [self._overheat]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ImprovedCritical"]
        progression.Selectors = (progression.Selectors or []) + [
            f"SelectSpells({self._level_7_spell_list},1,0)",
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 8)
    def level_8(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.SORCERER_WILDMAGIC, 9)
    def level_9(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.SORCERER_WILDMAGIC, 10)
    def level_10(self, progression: Progression) -> None:
        pass

    @progression(CharacterClass.SORCERER_WILDMAGIC, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = (progression.PassivesAdded or []) + ["ReliableTalent"]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 12)
    def level_12(self, progression: Progression) -> None:
        pass


def main():
    parser = argparse.ArgumentParser(description="A replacer for Wild Magic Sorcery.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=1,
                        help="Feat progression every n levels (defaulting to 1; feat every level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Sorcery Points) multiplier (defaulting to 2; double points)")
    args = Pyromancy.Args(**vars(parser.parse_args()))

    pyromancy = Pyromancy(args)
    pyromancy.build()


if __name__ == "__main__":
    main()
