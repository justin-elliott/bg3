#!/usr/bin/env python3

import os

from functools import cache, cached_property
from moddb import Awareness, Maneuvers, Movement
from modtools.gamedata import Armor, PassiveData
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    progression,
    Replacer,
    spelllist,
)

class DaughterOfDarkness(Replacer):
    _maneuvers: Maneuvers

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="DaughterOfDarkness",
                         description="A class replacer for TrickeryDomain.",
                         **kwds)

        self._maneuvers = Maneuvers(self.mod)
        self._update_shadowheart_chain_shirt()

    def _update_shadowheart_chain_shirt(self) -> str:
        name = "ARM_ChainShirt_Body_Shar"
        self.add(Armor(
            name,
            using=name,
            Ability_Modifier_Cap="",
            ArmorClass=17,
            Boosts=[
                "CriticalHit(AttackTarget,Success,Never)",
                "RollBonus(SavingThrow,2)",
            ],
            PassivesOnEquip=[
                "MAG_ExoticMaterial_MediumArmor_Passive",
                "MAG_MAG_EndGame_Plate_Armor_Passive",
            ],
            Rarity="Legendary",
            StatusOnEquip=[
                "MAG_EXOTIC_MATERIAL_ARMOR_TECHNICAL",
                "MAG_BLADE_WARD",
                "MAG_END_GAME_RESISTANCE",
            ],
        ))

    @cached_property
    def _awareness(self) -> str:
        return Awareness(self.mod).add_awareness()

    @cached_property
    def _quickened_spell(self) -> str:
        name = self.make_name("Quickened")
        self.add(PassiveData(
            name,
            using="Metamagic_Quickened",
            DisplayName=self.loca("Quickened_DisplayName", "Quickened Spell"),
            Description=self.loca("Quickened_Description", """
                Spells that cost an action cost a bonus action instead.
            """),
            Boosts=[
                "UnlockSpellVariant("
                +   "QuickenedSpellCheck(),"
                +   "ModifyUseCosts(Add,ChannelDivinity,1,0),"
                +   "ModifyUseCosts(Replace,BonusActionPoint,1,0,ActionPoint)"
                + ")",
            ],
            EnabledConditions=[],
        ))
        return name
    
    @cached_property
    def _twinned_spell(self) -> str:
        name = self.make_name("Twinned")
        self.add(PassiveData(
            name,
            using="Metamagic_Twinned",
            DisplayName=self.loca("Twinned_DisplayName", "Twinned Spell"),
            Description=self.loca("Twinned_Description", """
                Spells that only target 1 creature can target an additional creature.
            """),
            Boosts=[
                "UnlockSpellVariant("
                +   "TwinnedProjectileSpellCheck(),"
                +   "ModifyUseCosts(Add,ChannelDivinity,1,0),"
                +   "ModifyNumberOfTargets(AdditiveBase,1,false)"
                + ")",
                "UnlockSpellVariant("
                +   "TwinnedTargetSpellCheck(),"
                +   "ModifyUseCosts(Add,ChannelDivinity,1,0),"
                +   "ModifyNumberOfTargets(AdditiveBase,1,false)"
                + ")",
                "UnlockSpellVariant("
                +   "TwinnedTargetTouchSpellCheck(),"
                +   "ModifyUseCosts(Add,ChannelDivinity,1,0),"
                +   "ModifyNumberOfTargets(AdditiveBase,1,false)"
                + ")",
            ],
            EnabledConditions=[],
        ))
        return name
    
    @cached_property
    def _shadow_step(self) -> str:
        return Movement(self.mod).add_shadow_step("Movement:Distance*0.5")

    @cache
    def _wizard_spelllist(self, level: int) -> str:
        name = f"Trickery Domain Level {level} Wizard Spells"
        uuid = self.make_uuid(name)
        wizard_spells = spelllist.wizard_spells(self, level).Spells
        cleric_spells = (set(spelllist.cleric_spells(self, level).Spells) |
                         set(spelllist.trickery_domain_spells(self, level).Spells))
        unique_spells = [spell for spell in wizard_spells if spell not in cleric_spells]
        self.add(SpellList(
            Name=name,
            Spells=unique_spells,
            UUID=uuid,
        ))
        return uuid

    @cached_property
    def _shadow_step_spelllist(self) -> str:
        name = "Trickery Domain Shadow Step"
        uuid = self.make_uuid(name)
        self.add(SpellList(
            Name=name,
            Spells=[self._shadow_step],
            UUID=uuid,
        ))
        return uuid

    @progression(CharacterClass.CLERIC_TRICKERY, 1)
    def trickerydomain_level_1(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(SuperiorityDie,1,0)",
            "Proficiency(HeavyArmor)",
            "Proficiency(MartialWeapons)",
            "ProficiencyBonus(Skill,SleightOfHand)",
            "ExpertiseBonus(SleightOfHand)",
            "Advantage(Skill,SleightOfHand)",
            "ProficiencyBonus(Skill,Stealth)",
            "ExpertiseBonus(Stealth)",
            "Advantage(Skill,Stealth)",
            "ProficiencyBonus(Skill,Deception)",
            "ProficiencyBonus(Skill,Performance)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            self._awareness,
            "DevilsSight",
        ]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._wizard_spelllist(1)})",
            "SelectPassives(e51a2ef5-3663-43f9-8e74-5e28520323f1,3,Maneuvers)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 2)
    def trickerydomain_level_2(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._quickened_spell, self._twinned_spell]
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 3)
    def trickerydomain_level_3(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._wizard_spelllist(2)})",
            f"AddSpells({self._shadow_step_spelllist},,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 4)
    def trickerydomain_level_4(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 5)
    def trickerydomain_level_5(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack"]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._wizard_spelllist(3)})",
            "SelectPassives(e51a2ef5-3663-43f9-8e74-5e28520323f1,2,Maneuvers)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 6)
    def trickerydomain_level_6(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 7)
    def trickerydomain_level_7(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._wizard_spelllist(4)})",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 8)
    def trickerydomain_level_8(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 9)
    def trickerydomain_level_9(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ReliableTalent"]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._wizard_spelllist(5)})",
            "SelectPassives(e51a2ef5-3663-43f9-8e74-5e28520323f1,2,Maneuvers)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 10)
    def trickerydomain_level_10(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ImprovedCombatSuperiority"]

    @progression(CharacterClass.CLERIC_TRICKERY, 11)
    def trickerydomain_level_11(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_2"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack"]
        progress.Selectors = (progress.Selectors or []) + [
            f"AddSpells({self._wizard_spelllist(6)})",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 12)
    def trickerydomain_level_12(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]
        progress.PassivesAdded = (progress.PassivesAdded or []) + [self._maneuvers.relentless]

    @progression(CharacterClass.CLERIC_TRICKERY, 13)
    def trickerydomain_level_13(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 14)
    def trickerydomain_level_14(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 15)
    def trickerydomain_level_15(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 16)
    def trickerydomain_level_16(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 17)
    def trickerydomain_level_17(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 18)
    def trickerydomain_level_18(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 19)
    def trickerydomain_level_19(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]

    @progression(CharacterClass.CLERIC_TRICKERY, 20)
    def trickerydomain_level_20(self, progress: Progression) -> None:
        progress.Boosts = (progress.Boosts or []) + [
            "ActionResource(ChannelDivinity,1,0)",
            "ActionResource(SuperiorityDie,1,0)",
        ]


def main() -> None:
    daughter_of_darkness = DaughterOfDarkness(
        classes=[CharacterClass.CLERIC_TRICKERY],
    )
    daughter_of_darkness.build()


if __name__ == "__main__":
    main()
