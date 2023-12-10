#!/usr/bin/env python3

import os.path
import textwrap

base_dir = os.path.dirname(__file__) or '.'

# Generate the passives
with open(os.path.join(base_dir, "Public", "Serenade", "Stats", "Generated", "Data", "Medley.txt"), "w") as f:
    recovery_passives = [f"Serenade_Recovery_{level}" for level in range(1, 10)]
    warlock_recovery_passives = [f"Serenade_WarlockRecovery_{level}" for level in range(1, 6)]

    recover_spell_slots = [f"IF(RemoveCause(StatusRemoveCause.TimeOut) and IsFirstUsedSpellSlot({level})):RestoreResource(SpellSlot,1,{level})" for level in range(9, 0, -1)]
    recover_warlock_spell_slots = [f"IF(RemoveCause(StatusRemoveCause.TimeOut) and IsWarlockSpellLevel({level})):RestoreResource(WarlockSpellSlot,1,{level})" for level in range(5, 0, -1)]

    f.write(textwrap.dedent(f"""\
        new entry "Serenade_Medley"
        type "SpellData"
        data "SpellType" "Shout"
        using "Shout_SongOfRest"
        data "AreaRadius" "9"
        data "Cooldown" ""
        data "DisplayName" "Serenade_Medley_DisplayName"
        data "Description" "Serenade_Medley_Description"
        data "Icon" "Action_Song_SingForMe"
        data "Level" "0"
        data "RequirementConditions" ""
        data "SpellProperties" "ApplyStatus(SERENADE_MEDLEY,100,-1);ApplyStatus(LONGSTRIDER,100,-1);ApplyStatus(PETPAL,100,-1);IF(not WearingArmor()):ApplyStatus(MAGE_ARMOR,100,-1)"
        data "TargetConditions" "Character() and Ally()"
        data "TooltipStatusApply" "ApplyStatus(SERENADE_MEDLEY,100,-1);ApplyStatus(LONGSTRIDER,100,-1);ApplyStatus(PETPAL,100,-1);ApplyStatus(MAGE_ARMOR,100,-1)"
        data "VerbalIntent" "Buff"

        new entry "SERENADE_MEDLEY"
        type "StatusData"
        data "StatusType" "BOOST"
        data "DisplayName" "Serenade_Medley_DisplayName"
        data "Description" "Serenade_MedleyBoost_Description"
        data "DescriptionParams" "LevelMapValue(Serenade_AidValue);RegainHitPoints(LevelMapValue(D4Cantrip));Distance(24)"
        data "Icon" "Action_Song_SingForMe"
        data "StackId" "AID"
        data "StackType" "Overwrite"
        data "Boosts" "IncreaseMaxHP(LevelMapValue(Serenade_AidValue));Reroll(Attack,1,true);Reroll(SkillCheck,1,true);Reroll(RawAbility,1,true);Reroll(SavingThrow,1,true);DarkvisionRangeMin(24);ActiveCharacterLight(c46e7ba8-e746-7020-5146-287474d7b9f7)"
        data "Passives" "{";".join(recovery_passives)};{";".join(warlock_recovery_passives)}"
        data "TickType" "StartTurn"
        data "TickFunctors" "IF(HasHPPercentageLessThan(100)):RegainHitPoints(LevelMapValue(D4Cantrip))"
        data "StatusGroups" "SG_RemoveOnRespec"

        new entry "SERENADE_RECOVERY"
        type "StatusData"
        data "StatusType" "BOOST"
        data "DisplayName" "Serenade_Recovery_DisplayName"
        data "Description" "Serenade_Recovery_Description"
        data "Icon" "Skill_Wizard_ArcaneRecovery"
        data "OnRemoveFunctors" "{";".join(recover_spell_slots)}"
        data "StackId" "SERENADE_RECOVERY"
        data "StackType" "Overwrite"
        data "StatusGroups" "SG_RemoveOnRespec"
        data "StatusPropertyFlags" "DisableOverhead;DisablePortraitIndicator;DisableCombatlog"

        new entry "SERENADE_WARLOCKRECOVERY"
        type "StatusData"
        data "StatusType" "BOOST"
        data "DisplayName" "Serenade_Recovery_DisplayName"
        data "Description" "Serenade_Recovery_Description"
        data "Icon" "Skill_Wizard_ArcaneRecovery"
        data "OnRemoveFunctors" "{";".join(recover_warlock_spell_slots)}"
        data "StackId" "SERENADE_WARLOCKRECOVERY"
        data "StackType" "Overwrite"
        data "StatusGroups" "SG_RemoveOnRespec"
        data "StatusPropertyFlags" "DisableOverhead;DisablePortraitIndicator;DisableCombatlog"
        """))

    for level in range(1, 10):
        f.write(textwrap.dedent(f"""\

            new entry "Serenade_Recovery_{level}"
            type "PassiveData"
            data "Properties" "IsHidden"
            data "StatsFunctorContext" "OnCreate;OnActionResourcesChanged"
            data "StatsFunctors" "IF(CanRecoverSpellSlot({level},'SERENADE_RECOVERY')):ApplyStatus(SERENADE_RECOVERY,100,{level})"
            """))

    for level in range(1, 6):
        f.write(textwrap.dedent(f"""\

            new entry "Serenade_WarlockRecovery_{level}"
            type "PassiveData"
            data "Properties" "IsHidden"
            data "StatsFunctorContext" "OnCreate;OnActionResourcesChanged"
            data "StatsFunctors" "IF(CanRecoverWarlockSpellSlot({level},'SERENADE_WARLOCKRECOVERY')):ApplyStatus(SERENADE_WARLOCKRECOVERY,100,{level})"
            """))
