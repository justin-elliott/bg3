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
                   boostFormatStr: str,
                   first_value: int = 2,
                   last_value: int = 20,
                   step_value: int = 2):
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
        data "ContainerSpells" "{";".join(container_spells)}"
        data "CycleConditions" "Self()"
        data "TargetConditions" "Self()"
        data "Icon" "{icon}"
        data "DisplayName" "{display_name}"
        data "Description" "{description}"
        data "CastTextEvent" "Cast"
        data "UseCosts" ""
        data "SpellAnimation" "03496c4a-49e0-4132-b585-3e5ecd1ad8e5,,;,,;8252328a-66dd-4dc0-bbe0-00eea3204922,,;982d842b-5d44-4ef6-ab33-14d5ae514a50,,;a9682ef9-5d9e-4ac0-8144-2c7fe6eb868c,,;,,;32fb4d91-7fde-4b05-9144-ea87b9a4284a,,;dada6495-752c-4f30-a503-f05b8c811e2b,,;8ce53f9b-b559-49cd-9607-1991545060d7,,"
        data "SpellFlags" "IsLinkedSpellContainer;IgnorePreviouslyPickedEntities"
        data "HitAnimationType" "MagicalNonDamage"
        data "CastSound" "{cast_sound}"
        data "TargetSound" "{target_sound}"
        data "VerbalIntent" "Buff"
        data "PrepareEffect" "{prepare_effect}"
        data "CastEffect" "{cast_effect}"
        data "TargetEffect" "{target_effect}"

        new entry "{spell_name}_00"
        type "SpellData"
        data "SpellType" "Shout"
        using "{spell_name}"
        data "SpellContainerID" "{spell_name}"
        data "ContainerSpells" ""
            data "SpellProperties" "ApplyStatus({spell_name.upper()}_00,100,-1)"
        data "Icon" "PassiveFeature_Portent"
        data "DisplayName" "AdventurersCompendium_Boost_Reset_DisplayName"
        data "Description" "AdventurersCompendium_Boost_Reset_Description"
        data "TooltipStatusApply" "ApplyStatus({spell_name.upper()}_00,100,-1)"

        new entry "{spell_name.upper()}_00"
        type "StatusData"
        data "StatusType" "BOOST"
        data "DisplayName" "{display_name}"
        data "Description" "{description}"
        data "Icon" "{icon}"
        data "StackId" "{spell_name.upper()}"
        data "StackType" "Overwrite"
        data "Boosts" "{boostFormatStr.format(0)}"
        data "StatusPropertyFlags" "DisableOverhead;DisableCombatlog;DisablePortraitIndicator;IgnoreResting"
        """)

    for value in value_range:
        spell += textwrap.dedent(f"""\

            new entry "{spell_name}_{value:02}"
            type "SpellData"
            data "SpellType" "Shout"
            using "{spell_name}"
            data "SpellContainerID" "{spell_name}"
            data "ContainerSpells" ""
            data "SpellProperties" "ApplyStatus({spell_name.upper()}_{value:02},100,-1)"
            data "Icon" "PassiveFeature_Portent_{value}"
            data "DisplayName" "AdventurersCompendium_Boost_Value_DisplayName"
            data "Description" "AdventurersCompendium_Boost_Value_Description"
            data "DescriptionParams" "{value}"
            data "TooltipStatusApply" "ApplyStatus({spell_name.upper()}_{value:02},100,-1)"

            new entry "{spell_name.upper()}_{value:02}"
            type "StatusData"
            data "StatusType" "BOOST"
            data "DisplayName" "{display_name}"
            data "Description" "{description}"
            data "Icon" "{icon}"
            data "StackId" "{spell_name.upper()}"
            data "StackType" "Overwrite"
            data "Boosts" "{boostFormatStr.format(value)}"
            data "StatusPropertyFlags" "DisableOverhead;DisableCombatlog;DisablePortraitIndicator;IgnoreResting"
            """)

    spell_file = os.path.join(DATA_DIR, f"{short_name}.txt")
    with open(spell_file, "w") as f:
        f.write(spell)

writeSpellFile("BoostStrength",
               display_name="AdventurersCompendium_BoostStrength_DisplayName",
               description="AdventurersCompendium_BoostStrength_Description",
               icon="Spell_Transmutation_EnhanceAbility_BullsStrenght",
               cast_sound="Spell_Cast_Buff_EnhanceAbilityBullsStrength_L1to3",
               target_sound="Spell_Impact_Buff_EnhanceAbilityBullsStrength_L1to3",
               prepare_effect="5ea8f8f4-ba5f-4417-82f6-ed2ce4ffe264",
               cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
               target_effect="fbb955f8-a644-451b-89bd-7950ad4cebad",
               boostFormatStr="Ability(Strength,{0},30)")
writeSpellFile("BoostDexterity",
               display_name="AdventurersCompendium_BoostDexterity_DisplayName",
               description="AdventurersCompendium_BoostDexterity_Description",
               icon="Spell_Transmutation_EnhanceAbility_CatsGrace",
               cast_sound="Spell_Cast_Buff_EnhanceAbilityCatsGrace_L1to3",
               target_sound="Spell_Impact_Buff_EnhanceAbilityCatsGrace_L1to3",
               prepare_effect="fbce561c-fd42-4626-bf04-8461f46dfbc8",
               cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
               target_effect="474d55bf-bce6-401b-872a-1922c8d54d99",
               boostFormatStr="Ability(Dexterity,{0},30)")
writeSpellFile("BoostConstitution",
               display_name="AdventurersCompendium_BoostConstitution_DisplayName",
               description="AdventurersCompendium_BoostConstitution_Description",
               icon="Spell_Transmutation_EnhanceAbility_BearsEndurance",
               cast_sound="Spell_Cast_Buff_EnhanceAbilityBearsEndurance_L1to3",
               target_sound="Spell_Impact_Buff_EnhanceAbilityBearsEndurance_L1to3",
               prepare_effect="15908bab-2ec3-4abc-a282-c3bf5f2b1387",
               cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
               target_effect="4d80e719-6b5a-4a77-829c-f9b7f38fd966",
               boostFormatStr="Ability(Constitution,{0},30)")
writeSpellFile("BoostIntelligence",
               display_name="AdventurersCompendium_BoostIntelligence_DisplayName",
               description="AdventurersCompendium_BoostIntelligence_Description",
               icon="Spell_Transmutation_EnhanceAbility_FoxsCunning",
               cast_sound="Spell_Cast_Buff_EnhanceAbilityFoxsCunning_L1to3",
               target_sound="Spell_Impact_Buff_EnhanceAbilityFoxsCunning_L1to3",
               prepare_effect="1ee00587-5c1a-4068-aba3-6bfd5cb8f92f",
               cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
               target_effect="587df9a6-10c6-4125-ab0a-73c477018a4b",
               boostFormatStr="Ability(Intelligence,{0},30)")
writeSpellFile("BoostWisdom",
               display_name="AdventurersCompendium_BoostWisdom_DisplayName",
               description="AdventurersCompendium_BoostWisdom_Description",
               icon="Spell_Transmutation_EnhanceAbility_OwlsWisdom",
               cast_sound="Spell_Cast_Buff_EnhanceAbilityOwlsWisdom_L1to3",
               target_sound="Spell_Impact_Buff_EnhanceAbilityOwlsWisdom_L1to3",
               prepare_effect="1082b19d-920d-423f-b787-3c66da153f47",
               cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
               target_effect="b01d8d96-abb3-4e88-8e41-ce12c7dbf30a",
               boostFormatStr="Ability(Wisdom,{0},30)")
writeSpellFile("BoostCharisma",
               display_name="AdventurersCompendium_BoostCharisma_DisplayName",
               description="AdventurersCompendium_BoostCharisma_Description",
               icon="Spell_Transmutation_EnhanceAbility_EaglesSplendor",
               cast_sound="Spell_Cast_Buff_EnhanceAbilityEaglesSplendor_L1to3",
               target_sound="Spell_Impact_Buff_EnhanceAbilityEaglesSplendor_L1to3",
               prepare_effect="fa18f4ad-7f12-47fc-9fe7-3a157e0ee260",
               cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
               target_effect="70d8d0dc-e4ff-42ed-8503-09bbf2fbbeda",
               boostFormatStr="Ability(Charisma,{0},30)")
writeSpellFile("BoostAbilities",
               display_name="AdventurersCompendium_BoostAbilities_DisplayName",
               description="AdventurersCompendium_BoostAbilities_Description",
               icon="Spell_Transmutation_EnhanceAbility",
               cast_sound="Spell_Cast_Buff_EnhanceAbilityBearsEndurance_L1to3",
               target_sound="Spell_Impact_Buff_EnhanceAbilityBearsEndurance_L1to3",
               prepare_effect="15908bab-2ec3-4abc-a282-c3bf5f2b1387",
               cast_effect="bcd66fb0-b0bc-41d0-abba-ad443d63dd72",
               target_effect="4d80e719-6b5a-4a77-829c-f9b7f38fd966",
               boostFormatStr="Ability(Strength,{0},30);Ability(Dexterity,{0},30);Ability(Constitution,{0},30);Ability(Intelligence,{0},30);Ability(Wisdom,{0},30);Ability(Charisma,{0},30)")
writeSpellFile("BoostSkills",
               display_name="AdventurersCompendium_BoostSkills_DisplayName",
               description="AdventurersCompendium_BoostSkills_Description",
               icon="PassiveFeature_JackOfAllTrades",
               cast_sound="Spell_Cast_Buff_DivineFavor_L1to3",
               target_sound="Spell_Impact_Buff_DivineFavor_L1to3",
               prepare_effect="747ac7e5-c52e-4e5a-be78-1f9de85b55ea",
               cast_effect="1516f4b2-5a53-4adf-bf85-d6e46826cffe",
               target_effect="1516f4b2-5a53-4adf-bf85-d6e46826cffe",
               boostFormatStr="RollBonus(SkillCheck,{0});RollBonus(RawAbility,{0})")
