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
    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="ExceptionalElves",
                         description="Enhancements for Elf and Half-Elf races.",
                         **kwds)

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

        self.add(PassiveList(
            Name=list_name,
            Passives=[self._abilities_bonus_passive(bonus) for bonus in range(0, 18)],
            UUID=list_uuid,
        ))

        default_passive = self._abilities_bonus_passive(0)
        self.add(DefaultValue(
            Add=default_passive,
            Level=1,
            SelectorId=selector_id,
            TableUUID=progress.TableUUID,
            UUID=self.make_uuid(selector_id),
        ))

        self.loca[f"{selector_id}_DisplayName"] = f"Abilities Bonus"
        self.loca[f"{selector_id}_Description"] = f"Increase all of your abilities, to a maximum of 30."

        self.add(ProgressionDescription(
            DisplayName=self.loca[f"{selector_id}_DisplayName"],
            Description=self.loca[f"{selector_id}_Description"],
            ProgressionTableId=progress.TableUUID,
            SelectorId=selector_id,
            UUID=self.make_uuid(f"{selector_id} Description"),
        ))
        
        return (str(list_uuid), selector_id)

    @progression(CharacterRace.ELF, 1)
    @progression(CharacterRace.HALF_ELF, 1)
    def elf_level_1(self, progress: Progression) -> None:
        list_uuid, selector_id = self._abilities_bonus_passive_list(progress)
        progress.Selectors = [
            f"AddSpells({self._spell_list},,Intelligence,,AlwaysPrepared)",
            f"SelectPassives({list_uuid},1,{selector_id})",
        ]


if __name__ == "__main__":
    exceptional_elves = ExceptionalElves(
        classes=[CharacterClass.ROGUE],  # Ignored, but prevents multiclass slots from being updated
    )
    exceptional_elves.build()
