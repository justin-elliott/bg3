#!/usr/bin/env python3

import textwrap

from typing import TextIO

class Boost:
    def __init__(self,
                 short_name: str,
                 display_name: str,
                 description: str,
                 icon: str,
                 cast_sound: str,
                 target_sound: str,
                 prepare_effect: str,
                 cast_effect: str,
                 target_effect: str,
                 boosts: str,
                 max_value: int = 20):
        assert 0 < max_value <= 20
        self.short_name = short_name
        self.spell_name = f"AdventurersCompendium_{self.short_name}"
        self.display_name = display_name
        self.description = description
        self.icon = icon
        self.cast_sound = cast_sound
        self.target_sound = target_sound
        self.prepare_effect = prepare_effect
        self.cast_effect = cast_effect
        self.target_effect = target_effect
        self.boosts = boosts
        self.max_value = max_value
    
    def write(self, f: TextIO):
        f.write(self.__get_spell())
        f.write("\n")
        f.write(self.__get_status())
        f.write("\n")
        f.write(self.__get_boost_reset())
        for value in range(1, self.max_value + 1):
            f.write("\n")
            f.write(self.__get_boost_by_value(value))
    
    def __get_spell(self) -> str:
        return textwrap.dedent(f"""\
            new entry "{self.spell_name}"
            type "SpellData"
            data "SpellType" "Shout"
            data "Level" "0"
            data "SpellSchool" "Transmutation"
            data "ContainerSpells" "{";".join([f"{self.spell_name}_{count:02}" for count in range(self.max_value + 1)])}"
            data "TargetConditions" "Self()"
            data "Icon" "{self.icon}"
            data "DisplayName" "{self.display_name}"
            data "Description" "{self.description}"
            data "CastTextEvent" "Cast"
            data "UseCosts" "ActionPoint:1"
            data "SpellAnimation" "03496c4a-49e0-4132-b585-3e5ecd1ad8e5,,;,,;8252328a-66dd-4dc0-bbe0-00eea3204922,,;982d842b-5d44-4ef6-ab33-14d5ae514a50,,;a9682ef9-5d9e-4ac0-8144-2c7fe6eb868c,,;,,;32fb4d91-7fde-4b05-9144-ea87b9a4284a,,;dada6495-752c-4f30-a503-f05b8c811e2b,,;8ce53f9b-b559-49cd-9607-1991545060d7,,"
            data "SpellFlags" "HasVerbalComponent;HasSomaticComponent;IsSpell;IsMelee;IsLinkedSpellContainer;IgnorePreviouslyPickedEntities"
            data "HitAnimationType" "MagicalNonDamage"
            data "CastSound" "{self.cast_sound}"
            data "TargetSound" "{self.target_sound}"
            data "VerbalIntent" "Buff"
            data "PrepareEffect" "{self.prepare_effect}"
            data "CastEffect" "{self.cast_effect}"
            data "TargetEffect" "{self.target_effect}"
            """)

    def __get_status(self) -> str:
        return textwrap.dedent(f"""\
            new entry "{self.spell_name.upper()}"
            type "StatusData"
            data "StatusType" "BOOST"
            data "DisplayName" "{self.display_name}"
            data "Description" "{self.description}"
            data "Icon" "Spell_Transmutation_EnhanceAbility_BullsStrenght"
            data "StackId" "{self.spell_name.upper()}"
            data "StackType" "Overwrite"
            data "Boosts" "{self.boosts}"
            data "StatusPropertyFlags" "MultiplyEffectsByDuration;FreezeDuration;DisableOverhead;DisableCombatlog;DisablePortraitIndicator;IgnoreResting"
            """)

    def __get_boost_reset(self) -> str:
        return textwrap.dedent(f"""\
            new entry "{self.spell_name}_00"
            type "SpellData"
            data "SpellType" "Shout"
            using "{self.spell_name}"
            data "SpellContainerID" "{self.spell_name}"
            data "ContainerSpells" ""
            data "SpellProperties" "RemoveStatus({self.spell_name.upper()})"
            data "Icon" "PassiveFeature_Portent"
            data "DisplayName" "AdventurersCompendium_Boost_Reset_DisplayName"
            data "Description" "AdventurersCompendium_Boost_Reset_Description"
            data "TooltipStatusApply" "RemoveStatus({self.spell_name.upper()})"
            """)

    def __get_boost_by_value(self, value: int) -> str:
        assert 0 < value <= 20
        return textwrap.dedent(f"""\
            new entry "{self.spell_name}_{value:02}"
            type "SpellData"
            data "SpellType" "Shout"
            using "{self.spell_name}"
            data "SpellContainerID" "{self.spell_name}"
            data "ContainerSpells" ""
            data "SpellProperties" "ApplyStatus({self.spell_name.upper()},100,{value})"
            data "Icon" "PassiveFeature_Portent_{value}"
            data "DisplayName" "AdventurersCompendium_Boost_Value_DisplayName"
            data "Description" "AdventurersCompendium_Boost_Value_Description"
            data "DescriptionParams" "{value}"
            data "TooltipStatusApply" "ApplyStatus({self.spell_name.upper()},100,{value})"
            """)
