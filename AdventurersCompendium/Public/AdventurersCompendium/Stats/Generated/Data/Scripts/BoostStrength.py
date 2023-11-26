#!/usr/bin/env python3

import os
import sys
import textwrap

from typing import Final, TextIO

MAX_VALUE: int = 20
SPELL: Final[str] = "AdventurersCompendium_BoostStrength"

PREAMBLE: Final[str] = f"""\
new entry "{SPELL}"
type "SpellData"
data "SpellType" "Shout"
data "Level" "0"
data "SpellSchool" "Transmutation"
data "ContainerSpells" "{";".join([f"{SPELL}_{count:02}" for count in range(MAX_VALUE + 1)])}"
data "TargetConditions" "Self()"
data "Icon" "Spell_Transmutation_EnhanceAbility_BullsStrenght"
data "DisplayName" "AdventurersCompendium_BoostStrength_DisplayName"
data "Description" "AdventurersCompendium_BoostStrength_Description"
data "CastTextEvent" "Cast"
data "UseCosts" "ActionPoint:1"
data "SpellAnimation" "03496c4a-49e0-4132-b585-3e5ecd1ad8e5,,;,,;8252328a-66dd-4dc0-bbe0-00eea3204922,,;982d842b-5d44-4ef6-ab33-14d5ae514a50,,;a9682ef9-5d9e-4ac0-8144-2c7fe6eb868c,,;,,;32fb4d91-7fde-4b05-9144-ea87b9a4284a,,;dada6495-752c-4f30-a503-f05b8c811e2b,,;8ce53f9b-b559-49cd-9607-1991545060d7,,"
data "SpellFlags" "HasVerbalComponent;HasSomaticComponent;IsSpell;IsMelee;IsLinkedSpellContainer;IgnorePreviouslyPickedEntities"
data "HitAnimationType" "MagicalNonDamage"
data "CastSound" "Spell_Cast_Buff_EnhanceAbilityBearsEndurance_L1to3"
data "TargetSound" "Spell_Impact_Buff_EnhanceAbilityBearsEndurance_L1to3"
data "VerbalIntent" "Buff"
data "PrepareEffect" "15908bab-2ec3-4abc-a282-c3bf5f2b1387"
data "CastEffect" "bcd66fb0-b0bc-41d0-abba-ad443d63dd72"
data "TargetEffect" "4d80e719-6b5a-4a77-829c-f9b7f38fd966"

new entry "{SPELL.upper()}"
type "StatusData"
data "StatusType" "BOOST"
data "DisplayName" "AdventurersCompendium_BoostStrength_DisplayName"
data "Description" "AdventurersCompendium_BoostStrength_Description"
data "Icon" "Spell_Transmutation_EnhanceAbility_BullsStrenght"
data "StackId" "{SPELL.upper()}"
data "StackType" "Overwrite"
data "Boosts" "Ability(Strength,1,30)"
data "StatusPropertyFlags" "MultiplyEffectsByDuration;FreezeDuration;DisableOverhead;DisableCombatlog;DisablePortraitIndicator;IgnoreResting"

new entry "{SPELL}_00"
type "SpellData"
data "SpellType" "Shout"
using "{SPELL}"
data "SpellContainerID" "{SPELL}"
data "ContainerSpells" ""
data "SpellProperties" "RemoveStatus({SPELL.upper()})"
data "Icon" "PassiveFeature_Portent"
data "DisplayName" "AdventurersCompendium_BoostStrength_Reset_DisplayName"
data "Description" "AdventurersCompendium_BoostStrength_Reset_Description"
data "TooltipStatusApply" "RemoveStatus({SPELL.upper()})"
"""

def writeEntry(f: TextIO, count: int) -> None:
    f.write(textwrap.dedent(f"""\
    
    new entry "{SPELL}_{count:02}"
    type "SpellData"
    data "SpellType" "Shout"
    using "{SPELL}"
    data "SpellContainerID" "{SPELL}"
    data "ContainerSpells" ""
    data "SpellProperties" "ApplyStatus({SPELL.upper()},100,{count})"
    data "Icon" "PassiveFeature_Portent_{count}"
    data "DisplayName" "AdventurersCompendium_BoostStrength_Value_DisplayName"
    data "Description" "AdventurersCompendium_BoostStrength_Value_Description"
    data "DescriptionParams" "{count}"
    data "TooltipStatusApply" "ApplyStatus({SPELL.upper()},100,{count})"
    """))

SCRIPTS_DIR: str = os.path.dirname(os.path.abspath(sys.argv[0]))
DATA_DIR: str = os.path.normpath(os.path.join(SCRIPTS_DIR, ".."))
SPELL_FILE: str = os.path.join(DATA_DIR, "BoostStrength.txt")

with open(SPELL_FILE, "w") as f:
    f.write(PREAMBLE)
    for count in range(1, MAX_VALUE + 1):
        writeEntry(f, count)