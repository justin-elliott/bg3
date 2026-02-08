#!/usr/bin/env python3
"""
Generates files for Exceptional Elves, a mod to give Elves and Half-Elves bonus features.
"""

from functools import cache, cached_property
import os

from moddb import Bolster, Knowledge
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    CharacterAbility,
    CharacterClass,
    CharacterRace,
    DefaultValue,
    PassiveList,
    Progression,
    ProgressionDescription,
    SpellList,
)
from modtools.replacers import (
    progression,
    Replacer,
)


class ExceptionalElves(Replacer):
    _no_selection_ids: set[str]
    _passive_list_uuids: set[str]

    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="ExceptionalElves",
                         description="Enhancements for Elf and Half-Elf races.",
                         **kwds)
        
        self._no_selection_ids = set()
        self._passive_list_uuids = set()

    @cached_property
    def _spell_list(self) -> str:
        name = f"Exceptional Elves spells"
        uuid = self.make_uuid(name)
        self.add(SpellList(
            Name=name,
            Spells=[
                Bolster(self.mod).add_bolster(),
                Knowledge(self.mod).add_knowledge_of_the_ages(),
            ],
            UUID=uuid
        ))
        return uuid

    @cache
    def _abilities_bonus_passive(self, bonus: int) -> str:
        passive_name = self.make_name(f"AbilitiesBonus_{bonus}")

        self.loca[f"{passive_name}_DisplayName"] = f"Abilities +{bonus}"
        self.loca[f"{passive_name}_Description"] = f"""
            Increase all of your abilities by {bonus}, to a maximum of 30.
            """

        self.add(PassiveData(
            passive_name,
            DisplayName=self.loca[f"{passive_name}_DisplayName"],
            Description=self.loca[f"{passive_name}_Description"],
            Boosts=[f"Ability({ability.name.title()},{bonus},30)" for ability in CharacterAbility]
                if bonus > 0 else None,
            Properties=["IsHidden"],
        ))

        return passive_name

    @cache
    def _abilities_bonus_passive_list(self, progress: Progression) -> tuple[str, str]:
        list_name = "Abilities Bonus"
        list_uuid = self.make_uuid(list_name)
        selector_id = self.make_name(f"{progress.Name}AbilitiesBonus")

        if list_uuid not in self._passive_list_uuids:
            self.add(PassiveList(
                Name=list_name,
                Passives=[self._abilities_bonus_passive(bonus) for bonus in range(0, 18)],
                UUID=list_uuid,
            ))
            self._passive_list_uuids.add(list_uuid)

        default_passive = self._abilities_bonus_passive(0)
        self.add(DefaultValue(
            Add=default_passive,
            Level=1,
            SelectorId=selector_id,
            TableUUID=progress.TableUUID,
            UUID=self.make_uuid(selector_id),
        ))

        self.loca["AbilitiesBonus_DisplayName"] = f"Abilities Bonus"
        self.loca["AbilitiesBonus_Description"] = f"Increase all of your abilities, to a maximum of 30."

        self.add(ProgressionDescription(
            DisplayName=self.loca["AbilitiesBonus_DisplayName"],
            Description=self.loca["AbilitiesBonus_Description"],
            ProgressionTableId=progress.TableUUID,
            SelectorId=selector_id,
            UUID=self.make_uuid(f"{selector_id} Description"),
        ))
        
        return (str(list_uuid), selector_id)

    @cache
    def _no_selection(self, progress: Progression) -> str:
        name = self.make_name(f"NoSelection_Level_{progress.Level}")
        if name not in self._no_selection_ids:
            self.loca["NoSelection_DisplayName"] = "None"
            self.loca["NoSelection_Description"] = "Decline any racial ability at this level."
            self.add(PassiveData(
                name,
                DisplayName=self.loca["NoSelection_DisplayName"],
                Description=self.loca["NoSelection_Description"],
                Properties=["IsHidden"],
            ))
            self._no_selection_ids.add(name)
        return name

    @cached_property
    def _archer(self) -> str:
        name = self.make_name("Archer")
        self.loca[f"{name}_DisplayName"] = "Archer"
        self.loca[f"{name}_Description"] = """
            You are proficient with all bows, and gain a +2 bonus to
            <LSTag Tooltip="RangedWeaponAttack">ranged weapon attacks</LSTag> and damage.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[
                "Proficiency(HandCrossbows)",
                "Proficiency(LightCrossbows)",
                "Proficiency(HeavyCrossbows)",
                "Proficiency(Shortbows)",
                "Proficiency(Longbows)",
                "RollBonus(RangedWeaponAttack,2)",
                "RollBonus(RangedOffHandWeaponAttack,2)",
                "IF(IsRangedWeaponAttack()):CharacterWeaponDamage(2)",
            ],
            Icon="PassiveFeature_FightingStyle_Archery",
        ))
        return name

    @cached_property
    def _mistwalker(self) -> str:
        name = self.make_name("Mistwalker")
        self.loca[f"{name}_DisplayName"] = "Mistwalker"
        self.loca[f"{name}_Description"] = "Surrounded by silver mist, you teleport to an unoccupied space you can see."
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=["UnlockSpell(Target_MistyStep_Githyanki,Singular,,OncePerTurnNoRealtime)"],
            Icon="Spell_Conjuration_MistyStep",
            Properties=["IsHidden"],
        ))
        return name

    @cached_property
    def _pickpocket(self) -> str:
        name = self.make_name("Pickpocket")
        self.loca[f"{name}_DisplayName"] = "Pickpocket"
        self.loca[f"{name}_Description"] = """
            You gain <LSTag Tooltip="Expertise">Expertise</LSTag> in
            <LSTag Tooltip="SleightOfHand">Sleight of Hand</LSTag>.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=["ProficiencyBonus(Skill,SleightOfHand)", "ExpertiseBonus(SleightOfHand)"],
            Icon="Spell_Conjuration_MageHand",
        ))
        return name

    @cached_property
    def _well_practiced(self) -> str:
        name = self.make_name("WellPracticed")
        self.loca[f"{name}_DisplayName"] = "Well-Practiced"
        self.add(PassiveData(
            name,
            using="ReliableTalent",
            DisplayName=self.loca[f"{name}_DisplayName"],
        ))
        return name

    @cached_property
    def _racial_passives(self) -> list[tuple[int, str, str]]:
        return sorted([
            ( 1, "Archer",              self._archer),
            ( 1, "Naturally Stealthy",  "Halfling_LightfootStealth"),
            ( 1, "Pickpocket",          self._pickpocket),
            ( 3, "Jack of All Trades",  "JackOfAllTrades"),
            ( 5, "Mistwalker",          self._mistwalker),
            (11, "Well-Practiced",      self._well_practiced),
        ], key=lambda item: item[1])

    @cache
    def _racial_passive_list(self, progress: Progression) -> tuple[str, str]:
        list_name = f"Racial Abilities Level {progress.Level}"
        list_uuid = self.make_uuid(list_name)
        selector_id = self.make_name(f"{progress.Name}RacialAbilities_Level_{progress.Level}")
        
        if list_uuid not in self._passive_list_uuids:
            self.add(PassiveList(
                Name=list_name,
                Passives=[
                    self._no_selection(progress),
                    *[passive for level, _, passive in self._racial_passives if progress.Level >= level],
                ],
                UUID=list_uuid,
            ))
            self._passive_list_uuids.add(list_uuid)

        self.add(DefaultValue(
            Add=self._no_selection(progress),
            Level=progress.Level,
            SelectorId=selector_id,
            TableUUID=progress.TableUUID,
            UUID=self.make_uuid(selector_id),
        ))

        self.loca["RacialAbilities_DisplayName"] = f"Racial Abilities"
        self.loca["RacialAbilities_Description"] = f"Select a racial ability."

        self.add(ProgressionDescription(
            DisplayName=self.loca["RacialAbilities_DisplayName"],
            Description=self.loca["RacialAbilities_Description"],
            ProgressionTableId=progress.TableUUID,
            SelectorId=selector_id,
            UUID=self.make_uuid(f"{selector_id} Description"),
        ))
        
        return (str(list_uuid), selector_id)

    @progression(CharacterRace.DROW, 1)
    @progression(CharacterRace.ELF, 1)
    @progression(CharacterRace.HALF_ELF, 1)
    def elf_level_1(self, progress: Progression) -> None:
        progress.Selectors = [
            f"AddSpells({self._spell_list},,Intelligence,,AlwaysPrepared)",
            "SelectPassives({},1,{})".format(*self._abilities_bonus_passive_list(progress)),
        ]

    @progression(CharacterRace.DROW, range(1, 21, 2))
    @progression(CharacterRace.ELF, range(1, 21, 2))
    @progression(CharacterRace.HALF_ELF, range(1, 21, 2))
    def elf_odd_levels(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives({},1,{})".format(*self._racial_passive_list(progress)),
        ]

if __name__ == "__main__":
    exceptional_elves = ExceptionalElves(
        classes=[CharacterClass.ROGUE],  # Ignored, but prevents multiclass slots from being updated
    )
    exceptional_elves.build()
