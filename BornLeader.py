#!/usr/bin/env python3
"""
Generates files for Born Leader, a mod to give all races optional bonus features.
"""

from functools import cache, cached_property
import os

from collections.abc import Iterable
from moddb import (
    Bolster,
)
from modtools.gamedata import PassiveData, StatusData, SpellData
from modtools.lsx.game import (
    BASE_CHARACTER_RACES,
    CharacterAbility,
    CharacterClass,
    PassiveList,
    PassivesDefaultValue,
    Progression,
    ProgressionDescription,
    Skills,
)
from modtools.replacers import (
    progression,
    Replacer,
)


class BornLeader(Replacer):
    _no_selection_ids: set[str]
    _passive_list_uuids: set[str]
    _loca_handles: dict[str, str]

    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="BornLeader",
                         description="Optional born leader feature for any race.",
                         **kwds)
    
        self._no_selection_ids = set()
        self._passive_list_uuids = set()
        self._loca_handles = {}

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
        self.add(PassivesDefaultValue(
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
    def _ability_improvement(self, ability: CharacterAbility | None, name: str) -> str:
        ability_name = ability.name.title() if ability is not None else "None"
        passive_name = self.make_name(f"AbilityImprovement_{ability_name}_{name}")

        display_name = f"Ability Improvement: {ability_name}"
        if (display_name_handle := self._loca_handles.get(display_name)) is None:
            self.loca[f"{passive_name}_DisplayName"] = display_name
            display_name_handle = self.loca[f"{passive_name}_DisplayName"]
            self._loca_handles[display_name] = display_name_handle
    
        description = (
            f"Increase your {ability_name} by {self._ability_bonus}, to a maximum of 30."
            if ability else "No ability increase."
        )
        if (description_handle := self._loca_handles.get(description)) is None:
            self.loca[f"{passive_name}_Description"] = description
            description_handle = self.loca[f"{passive_name}_Description"]
            self._loca_handles[description] = description_handle

        self.add(PassiveData(
            passive_name,
            DisplayName=display_name_handle,
            Description=description_handle,
            Boosts=[f"Ability({ability_name},{self._ability_bonus},30)"] if ability is not None else None,
            Properties=["IsHidden"],
        ))

        return passive_name

    @cached_property
    def _ability_improvement_display_name(self) -> str:
        self.loca["AbilityImprovement_DisplayName"] = "Ability Improvement"
        return self.loca["AbilityImprovement_DisplayName"]

    @cached_property
    def _ability_improvement_description(self) -> str:
        self.loca["AbilityImprovement_Description"] = f"""
            Increase one of your abilities by {self._ability_bonus}, to a maximum of 30.
        """
        return self.loca["AbilityImprovement_Description"]

    @cache
    def _ability_improvement_passive_list(self, progress: Progression) -> tuple[str, str]:
        list_name = f"Ability Improvement Level {progress.Level}"
        list_uuid = self.make_uuid(list_name)
        level_id = f"Level_{progress.Level}"
        selector_id = self.make_name(f"{progress.Name}AbilityImprovement_{level_id}")

        none_passive = self._ability_improvement(None, level_id)

        if list_uuid not in self._passive_list_uuids:
            self.add(PassiveList(
                Name=list_name,
                Passives=[
                    none_passive,
                    *[self._ability_improvement(ability, level_id) for ability in CharacterAbility]
                ],
                UUID=list_uuid,
            ))
            self._passive_list_uuids.add(list_uuid)

        self.add(PassivesDefaultValue(
            Add=none_passive,
            Level=progress.Level,
            SelectorId=selector_id,
            TableUUID=progress.TableUUID,
            UUID=self.make_uuid(selector_id),
        ))

        self.add(ProgressionDescription(
            DisplayName=self._ability_improvement_display_name,
            Description=self._ability_improvement_description,
            ProgressionTableId=progress.TableUUID,
            SelectorId=selector_id,
            UUID=self.make_uuid(f"{selector_id} Description"),
        ))
        
        return (str(list_uuid), selector_id)

    def _ability_improvement_for_abilities(self, name: str, abilities: Iterable[CharacterAbility]) -> str:
        list_name = f"Ability Improvement {name}"
        list_uuid = self.make_uuid(list_name)

        if list_uuid not in self._passive_list_uuids:
            self.add(PassiveList(
                Name=list_name,
                Passives=[self._ability_improvement(ability, name) for ability in abilities],
                UUID=list_uuid,
            ))
            self._passive_list_uuids.add(list_uuid)
        
        return str(list_uuid)

    @cache
    def _no_selection(self, progress: Progression) -> str:
        name = self.make_name(f"NoSelection_Level_{progress.Level}")
        if name not in self._no_selection_ids:
            self.loca["NoSelection_DisplayName"] = "None"
            self.loca["NoSelection_Description"] = "Decline born leader features."
            self.add(PassiveData(
                name,
                DisplayName=self.loca["NoSelection_DisplayName"],
                Description=self.loca["NoSelection_Description"],
                Properties=["IsHidden"],
            ))
            self._no_selection_ids.add(name)
        return name

    @cached_property
    def _born_leader(self) -> str:
        name = self.make_name("BornLeader")

        levels = [5, 9, 12] if not self.args.level_20 else [5, 9, 13, 17]  # ensure parity with Alert if not L20
        initiative_boosts = [
            "Initiative(2)",
            *[f"IF(CharacterLevelGreaterThan({level - 1})):Initiative(1)" for level in levels],
        ]

        skills = [
            (Skills.ATHLETICS,       Skills.ATHLETICS),
            (Skills.SLEIGHT_OF_HAND, "Sleight of Hand"),
            (Skills.STEALTH,         Skills.STEALTH),
            (Skills.INSIGHT,         Skills.INSIGHT),
            (Skills.PERCEPTION,      Skills.PERCEPTION),
            (Skills.SURVIVAL,        Skills.SURVIVAL),
            (Skills.DECEPTION,       Skills.DECEPTION),
            (Skills.INTIMIDATION,    Skills.INTIMIDATION),
            (Skills.PERFORMANCE,     Skills.PERFORMANCE),
            (Skills.PERSUASION,      Skills.PERSUASION),
        ]

        self.add(PassiveData(
            name,
            DisplayName=self.loca(f"{name}_DisplayName", "Born Leader"),
            Description=self.loca(f"{name}_Description", f"""
                You are an <LSTag Tooltip="Expertise">Expert</LSTag> in
                {", ".join(f"""<LSTag Tooltip="{skill}">{name}</LSTag>""" for skill, name in skills[:-1])}{
                    f""", and <LSTag Tooltip="{skills[-1][0]}">{skills[-1][1]}</LSTag>"""}.
                
                Your <LSTag Tooltip="ProficiencyBonus">Proficiency Bonus</LSTag> is added to your Initiative rolls,
                and you can't be <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>.

                You can cast <LSTag Type="Spell" Tooltip="{self._bolster}">Bolster</LSTag>.
            """),
            Icon="Action_CommandersStrike",
            Boosts=[
                *[f"ProficiencyBonus(Skill,{skill})" for skill, _ in skills],
                *[f"ExpertiseBonus({skill})" for skill, _ in skills],
                *initiative_boosts,
                "StatusImmunity(SURPRISED)",
                f"UnlockSpell({self._bolster})",
            ],
            Properties=["Highlighted"],
        ))
        return name

    @cache
    def _born_leader_optional(self, progress: Progression) -> tuple[str, str]:
        list_name = f"Born Leader Level {progress.Level}"
        list_uuid = self.make_uuid(list_name)
        selector_id = self.make_name(f"{progress.Name}BornLeader_Level_{progress.Level}")
        
        if list_uuid not in self._passive_list_uuids:
            self.add(PassiveList(
                Name=list_name,
                Passives=[
                    self._no_selection(progress),
                    self._born_leader,
                ],
                UUID=list_uuid,
            ))
            self._passive_list_uuids.add(list_uuid)

        self.add(PassivesDefaultValue(
            Add=self._no_selection(progress),
            Level=progress.Level,
            SelectorId=selector_id,
            TableUUID=progress.TableUUID,
            UUID=self.make_uuid(selector_id),
        ))

        self.loca["BornLeader_DisplayName"] = f"Born Leader"
        self.loca["BornLeader_Description"] = f"Select whether this character is a born leader."

        self.add(ProgressionDescription(
            DisplayName=self.loca["BornLeader_DisplayName"],
            Description=self.loca["BornLeader_Description"],
            ProgressionTableId=progress.TableUUID,
            SelectorId=selector_id,
            UUID=self.make_uuid(f"{selector_id} Description"),
        ))
        
        return (str(list_uuid), selector_id)

    @cached_property
    def _bolster(self) -> str:
        return Bolster(self.mod).add_bolster()

    @progression(BASE_CHARACTER_RACES, 1)
    def level_1(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives({},1,{})".format(*self._abilities_bonus_passive_list(progress)),
            "SelectPassives({},1,{})".format(*self._born_leader_optional(progress)),
        ]

if __name__ == "__main__":
    born_leader = BornLeader(
        classes=[CharacterClass.ROGUE],  # Ignored, but prevents multiclass slots from being updated
        level_20=True,
    )
    born_leader.build()
