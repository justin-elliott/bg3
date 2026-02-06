#!/usr/bin/env python3
"""
Knowledge Of the Ages for Baldur's Gate 3 mods.
"""
from functools import cache
from typing import OrderedDict

from modtools.gamedata import SpellData, StatusData
from modtools.mod import Mod


class Knowledge:
    """Adds the Knowledge Of the Ages spell to a Baldur's Gate 3 mod."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize."""
        self._mod = mod

    @cache
    def add_knowledge_of_the_ages(self) -> None:
        """Add the Knowledge of the Ages spell, returning its name."""
        name = self._mod.make_name("KnowledgeOfTheAges")

        ability_skills: OrderedDict[str, list[str]] = OrderedDict([
            ("Charisma", ["Deception", "Intimidation", "Performance", "Persuasion"]),
            ("Dexterity", ["Acrobatics", "SleightOfHand", "Stealth"]),
            ("Intelligence", ["Arcana", "History", "Investigation", "Nature", "Religion"]),
            ("Strength", ["Athletics"]),
            ("Wisdom", ["AnimalHandling", "Insight", "Medicine", "Perception", "Survival"]),
        ])
        written_names: dict[str, str] = {
            "SleightOfHand": "Sleight of Hand",
            "AnimalHandling": "Animal Handling",
        }

        container_spells: list[SpellData] = []
        for ability in ability_skills.keys():
            container_spell_name = f"{name}_{ability}"
            status_name = container_spell_name.upper()

            skills = ability_skills[ability]
            written_skills = [written_names.get(skill, skill) for skill in skills]
            skill_list = ""
            if len(written_skills) == 1:
                skill_list = written_skills[0]
            else:
                skill_list = f"{", ".join(written_skills[:-1])}, and {written_skills[-1]}"
            
            self._mod.loca[f"{container_spell_name}_Description"] = f"""
                Gain <LSTag Tooltip="Expertise">Expertise</LSTag> in {skill_list}.
            """
            self._mod.loca[f"{status_name}_Description"] = f"""
                Has <LSTag Tooltip="Expertise">Expertise</LSTag> in {skill_list}.
            """

            self._mod.add(StatusData(
                status_name,
                using=f"KNOWLEDGE_OF_THE_AGES_{ability.upper()}",
                StatusType="BOOST",
                Description=self._mod.loca[f"{status_name}_Description"],
                Boosts=[
                    *[f"ProficiencyBonus(Skill,{skill})" for skill in skills],
                    *[f"ExpertiseBonus({skill})" for skill in skills],
                ],
                StatusEffect="",
                StatusPropertyFlags=["IgnoreResting"],
            ))

            container_spells.append(SpellData(
                container_spell_name,
                using=f"Shout_KnowledgeOfTheAges_{ability}",
                SpellType="Shout",
                Description=self._mod.loca[f"{container_spell_name}_Description"],
                SpellContainerID=name,
                SpellFlags=["HasVerbalComponent", "UnavailableInDialogs"],
                SpellProperties=[f"ApplyStatus({status_name},100,-1)"],
                TooltipStatusApply=[f"ApplyStatus({status_name},100,-1)"],
                UseCosts=["ActionPoint:1"],
            ))

        self._mod.loca[f"{name}_Description"] = """
            Gain <LSTag Tooltip="Expertise">Expertise</LSTag> in all <LSTag Tooltip="Skill">Skills</LSTag> of a chosen
            <LSTag Tooltip="Abilities">Ability</LSTag>.
        """

        self._mod.add(SpellData(
            name,
            using="Shout_KnowledgeOfTheAges",
            SpellType="Shout",
            Description=self._mod.loca[f"{name}_Description"],
            ContainerSpells=[spell.name for spell in container_spells],
            TooltipStatusApply=container_spells[0].TooltipStatusApply,
            UseCosts=["ActionPoint:1"],
        ))
        for spell in container_spells:
            self._mod.add(spell)
        
        return name
