#!/usr/bin/env python3

import os
import sys
import textwrap

from typing import Final

SCRIPTS_DIR: Final[str] = os.path.dirname(os.path.abspath(sys.argv[0]))
DATA_DIR: Final[str] = os.path.normpath(os.path.join(SCRIPTS_DIR, ".."))

def writeSpellFile(short_name: str, display_name: str, description: str, icon: str,
                   cast_sound: str, target_sound: str,
                   prepare_effect: str, cast_effect: str, target_effect: str,
                   boosts: str,
                   first_value: int = 1,
                   last_value: int = 20,
                   step_value: int = 1):
    assert 0 < first_value <= 20
    assert 0 < last_value <= 20
    assert 0 < step_value <= 20

    spell_name = f"AdventurersCompendium_{short_name}"
    value_range = range(first_value, last_value + 1, step_value)
    container_spells = [f"{spell_name}_00"] + [f"{spell_name}_{value:02}" for value in value_range]

    spell = textwrap.dedent(f"""\
        new entry "{spell_name}"
        type "SpellData"
        data "SpellType" "Shout"
        data "Level" "0"
        data "SpellSchool" "Transmutation"
        data "ContainerSpells" "{";".join(container_spells)}"
        data "TargetConditions" "Self()"
        data "Icon" "{icon}"
        data "DisplayName" "{display_name}"
        data "Description" "{description}"
        data "CastTextEvent" "Cast"
        data "UseCosts" "ActionPoint:1"
        data "SpellAnimation" "03496c4a-49e0-4132-b585-3e5ecd1ad8e5,,;,,;8252328a-66dd-4dc0-bbe0-00eea3204922,,;982d842b-5d44-4ef6-ab33-14d5ae514a50,,;a9682ef9-5d9e-4ac0-8144-2c7fe6eb868c,,;,,;32fb4d91-7fde-4b05-9144-ea87b9a4284a,,;dada6495-752c-4f30-a503-f05b8c811e2b,,;8ce53f9b-b559-49cd-9607-1991545060d7,,"
        data "SpellFlags" "HasVerbalComponent;HasSomaticComponent;IsSpell;IsMelee;IsLinkedSpellContainer;IgnorePreviouslyPickedEntities"
        data "HitAnimationType" "MagicalNonDamage"
        data "CastSound" "{cast_sound}"
        data "TargetSound" "{target_sound}"
        data "VerbalIntent" "Buff"
        data "PrepareEffect" "{prepare_effect}"
        data "CastEffect" "{cast_effect}"
        data "TargetEffect" "{target_effect}"

        new entry "{spell_name.upper()}"
        type "StatusData"
        data "StatusType" "BOOST"
        data "DisplayName" "{display_name}"
        data "Description" "{description}"
        data "Icon" "Spell_Transmutation_EnhanceAbility_BullsStrenght"
        data "StackId" "{spell_name.upper()}"
        data "StackType" "Overwrite"
        data "Boosts" "{boosts}"
        data "StatusPropertyFlags" "MultiplyEffectsByDuration;FreezeDuration;DisableOverhead;DisableCombatlog;DisablePortraitIndicator;IgnoreResting"

        new entry "{spell_name}_00"
        type "SpellData"
        data "SpellType" "Shout"
        using "{spell_name}"
        data "SpellContainerID" "{spell_name}"
        data "ContainerSpells" ""
        data "SpellProperties" "RemoveStatus({spell_name.upper()})"
        data "Icon" "PassiveFeature_Portent"
        data "DisplayName" "AdventurersCompendium_Boost_Reset_DisplayName"
        data "Description" "AdventurersCompendium_Boost_Reset_Description"
        data "TooltipStatusApply" "RemoveStatus({spell_name.upper()})"
        """)

    for value in value_range:
        spell += textwrap.dedent(f"""\

            new entry "{spell_name}_{value:02}"
            type "SpellData"
            data "SpellType" "Shout"
            using "{spell_name}"
            data "SpellContainerID" "{spell_name}"
            data "ContainerSpells" ""
            data "SpellProperties" "ApplyStatus({spell_name.upper()},100,{value})"
            data "Icon" "PassiveFeature_Portent_{value}"
            data "DisplayName" "AdventurersCompendium_Boost_Value_DisplayName"
            data "Description" "AdventurersCompendium_Boost_Value_Description"
            data "DescriptionParams" "{value}"
            data "TooltipStatusApply" "ApplyStatus({spell_name.upper()},100,{value})"
            """)

    spell_file = os.path.join(DATA_DIR, f"{short_name}.txt")
    with open(spell_file, "w") as f:
        f.write(spell)

writeSpellFile("BoostStrength",
               display_name="AdventurersCompendium_BoostStrength_DisplayName",
               description="AdventurersCompendium_BoostStrength_Description",
               icon="Spell_Transmutation_EnhanceAbility_BullsStrenght",
               cast_sound="Spell_Cast_Buff_EnhanceAbilityBearsEndurance_L1to3",
               target_sound="Spell_Impact_Buff_EnhanceAbilityBearsEndurance_L1to3",
               prepare_effect="5ea8f8f4-ba5f-4417-82f6-ed2ce4ffe264",
               cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
               target_effect="fbb955f8-a644-451b-89bd-7950ad4cebad",
               boosts="Ability(Strength,1,30)")
writeSpellFile("BoostDexterity",
               display_name="AdventurersCompendium_BoostDexterity_DisplayName",
               description="AdventurersCompendium_BoostDexterity_Description",
               icon="Spell_Transmutation_EnhanceAbility_CatsGrace",
               cast_sound="Spell_Cast_Buff_EnhanceAbilityCatsGrace_L1to3",
               target_sound="Spell_Impact_Buff_EnhanceAbilityCatsGrace_L1to3",
               prepare_effect="fbce561c-fd42-4626-bf04-8461f46dfbc8",
               cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
               target_effect="474d55bf-bce6-401b-872a-1922c8d54d99",
               boosts="Ability(Dexterity,1,30)")
