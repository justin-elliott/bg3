#!/usr/bin/env python3

import textwrap
from typing import Final, TextIO

MAX_VALUE: int = 20
SPELL: Final[str] = "AdventurersCompendium_BoostStrength"

PREAMBLE: Final[str] = f"""\
new entry "{SPELL}"
type "SpellData"
data "SpellType" "Target"
data "Level" "0"
data "SpellSchool" "Transmutation"
data "ContainerSpells" "{";".join([f"{SPELL}_{count:02}" for count in range(MAX_VALUE + 1)])}"
data "TargetRadius" "1.5"
data "TargetConditions" "Self()"
data "Icon" "Spell_Transmutation_EnhanceAbility_BullsStrenght"
data "DisplayName" "hb96346d0gcce3g4e34gb211geae8f98a3de0;1"
data "Description" "h8c9e7f4cg38deg4a95gb3e0g304b024930bb;1"
data "TooltipUpcastDescription" "04cc3403-f67a-4747-b49e-a1802cc7a6ad"
data "CastTextEvent" "Cast"
data "UseCosts" "ActionPoint:1"
data "SpellAnimation" "03496c4a-49e0-4132-b585-3e5ecd1ad8e5,,;,,;8252328a-66dd-4dc0-bbe0-00eea3204922,,;982d842b-5d44-4ef6-ab33-14d5ae514a50,,;a9682ef9-5d9e-4ac0-8144-2c7fe6eb868c,,;,,;32fb4d91-7fde-4b05-9144-ea87b9a4284a,,;dada6495-752c-4f30-a503-f05b8c811e2b,,;8ce53f9b-b559-49cd-9607-1991545060d7,,"
data "VerbalIntent" "Buff"
data "SpellFlags" "HasVerbalComponent;HasSomaticComponent;IsSpell;IsMelee;IsLinkedSpellContainer;IgnorePreviouslyPickedEntities"
data "HitAnimationType" "MagicalNonDamage"
data "MemoryCost" "1"

new entry "{SPELL.upper()}"
type "StatusData"
data "StatusType" "BOOST"
data "DisplayName" "hdf50f2a0g3756g4a90g97c9g9fb25fc3bc0f;1"
data "Description" "ha95811b7g5b47g4921g8a3bg8a424bb2f69c;3"
data "DescriptionParams" "1"
data "Icon" "Status_ArcaneWard"
data "SoundLoop" "Spell_Status_ArcaneWard_MO"
data "SoundStop" "Spell_Status_ArcaneWard_Depleted"
data "StackId" "{SPELL.upper()}"
data "StackType" "Overwrite"
data "Boosts" "Ability(Strength,1,30)"
data "StatusPropertyFlags" "MultiplyEffectsByDuration;FreezeDuration;DisableOverhead;DisableCombatlog;DisablePortraitIndicator;IgnoreResting"
data "StatusEffect" "370b3339-9668-49e8-bdc6-ff0a4444f8dd"

new entry "{SPELL}_00"
type "SpellData"
data "SpellType" "Target"
using "{SPELL}"
data "SpellContainerID" "{SPELL}"
data "ContainerSpells" ""
data "Autocast" "Yes"
data "SpellProperties" "RemoveStatus({SPELL.upper()})"
data "Icon" "PassiveFeature_Portent"
data "DisplayName" "h48782d39g2876g455bg8c41g89ff7982cbd0;2"
data "Description" "hbe072411gcda7g45e4g8d35g39d276270cb0;2"
data "TooltipStatusApply" "RemoveStatus({SPELL.upper()})"
"""

def writeEntry(f: TextIO, count: int) -> None:
    f.write(textwrap.dedent(f"""\
    
    new entry "{SPELL}_{count:02}"
    type "SpellData"
    data "SpellType" "Target"
    using "{SPELL}"
    data "SpellContainerID" "{SPELL}"
    data "ContainerSpells" ""
    data "Autocast" "Yes"
    data "SpellProperties" "ApplyStatus({SPELL.upper()},100,{count})"
    data "Icon" "PassiveFeature_Portent_{count}"
    data "DisplayName" "h48782d39g2876g455bg8c41g89ff7982cbd0;2"
    data "Description" "hbe072411gcda7g45e4g8d35g39d276270cb0;2"
    data "TooltipStatusApply" "ApplyStatus({SPELL.upper()},100,{count})"
    """))

with open("BoostStrength.txt", "w") as f:
    f.write(PREAMBLE)
    for count in range(1, MAX_VALUE + 1):
        writeEntry(f, count)