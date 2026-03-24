#!/usr/bin/env python3
"""
Generates files for Bonus Features, a mod to give all races optional bonus features.
"""

from functools import cache, cached_property
import os

from collections.abc import Iterable
from moddb import (
    Awareness,
    Bolster,
    ElementalWeapon,
    EmpoweredSpells,
    Movement,
)
from modtools.gamedata import PassiveData, StatusData, SpellData
from modtools.lsx.game import (
    BASE_CHARACTER_RACES,
    CharacterAbility,
    CharacterClass,
    Feat,
    PassiveList,
    PassivesDefaultValue,
    Progression,
    ProgressionDescription,
    Skills,
    SkillsDefaultValue,
)
from modtools.replacers import (
    progression,
    Replacer,
)
from modtools.text import Script, SpellSet
from typing import Final


class BonusFeatures(Replacer):
    _SKILL_LIST: Final[list[str]] = [
        Skills.PERSUASION,
        Skills.SLEIGHT_OF_HAND,
        Skills.ATHLETICS,
        Skills.PERCEPTION,
        Skills.INSIGHT,
        Skills.INTIMIDATION,
        Skills.DECEPTION,
        Skills.STEALTH,
        Skills.ARCANA,
        Skills.HISTORY,
        Skills.INVESTIGATION,
        Skills.NATURE,
        Skills.RELIGION,
        Skills.ANIMAL_HANDLING,
        Skills.MEDICINE,
        Skills.SURVIVAL,
        Skills.PERFORMANCE,
        Skills.ACROBATICS,
    ]

    _no_selection_ids: set[str]
    _passive_list_uuids: set[str]
    _loca_handles: dict[str, str]
    _ability_bonus: int

    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="BonusFeatures",
                         description="Optional bonus features for all races.",
                         **kwds)
        
        self._no_selection_ids = set()
        self._passive_list_uuids = set()
        self._loca_handles = {}
        self._ability_bonus = 1 if self.args.level_20 else 2

        self._add_bonus_spells_to_common_player_actions()
        self._remove_asi_from_feats()

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
            self.loca["NoSelection_Description"] = "Decline any bonus ability at this level."
            self.add(PassiveData(
                name,
                DisplayName=self.loca["NoSelection_DisplayName"],
                Description=self.loca["NoSelection_Description"],
                Properties=["IsHidden"],
            ))
            self._no_selection_ids.add(name)
        return name

    @cached_property
    def _action_surge(self) -> str:
        name = self.make_name("ActionSurge")
        self.loca[f"{name}_DisplayName"] = "Action Surge"
        self.loca[f"{name}_Description"] = """
            Immediately gain an extra <LSTag Tooltip="Action">action</LSTag> to use this turn.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=["UnlockSpell(Shout_ActionSurge)"],
            Icon="Skill_Fighter_ActionSurge",
            Properties=["IsHidden"],
        ))
        return name

    @cached_property
    def _alacrity(self) -> str:
        name = self.make_name("Alacrity")
        self.loca[f"{name}_DisplayName"] = "Alacrity"
        self.add(PassiveData(
            name,
            using="Assassinate_Resource",
            DisplayName=self.loca[f"{name}_DisplayName"],
        ))
        return name
    
    @cached_property
    def _arcane_adept(self) -> str:
        name = self.make_name("ArcaneAdept")
        BONUS = 2
        self.loca[f"{name}_DisplayName"] = "Arcane Adept"
        self.loca[f"{name}_Description"] = """
            You gain a +[1] bonus to <LSTag Tooltip="SpellDifficultyClass">Spell Save DC</LSTag>, spell
            <LSTag Tooltip="AttackRoll">attack rolls</LSTag>, and spell damage.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            DescriptionParams=[f"{BONUS}"],
            Boosts=[
                f"SpellSaveDC({BONUS})",
                f"RollBonus(MeleeSpellAttack,{BONUS})",
                f"RollBonus(RangedSpellAttack,{BONUS})",
                f"IF(IsSpell()):DamageBonus({BONUS})",
            ],
            Icon="Spell_Evocation_DancingLights",
            Properties=["Highlighted"],
        ))
        return name
    
    @cached_property
    def _archer(self) -> str:
        name = self.make_name("Archer")
        BONUS = 2
        self.loca[f"{name}_DisplayName"] = "Archer"
        self.loca[f"{name}_Description"] = """
            You are proficient with all bows, and gain a +[1] bonus to
            <LSTag Tooltip="RangedWeaponAttack">ranged weapon attacks</LSTag> and damage.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            DescriptionParams=[f"{BONUS}"],
            Boosts=[
                "Proficiency(HandCrossbows)",
                "Proficiency(LightCrossbows)",
                "Proficiency(HeavyCrossbows)",
                "Proficiency(Shortbows)",
                "Proficiency(Longbows)",
                f"RollBonus(RangedWeaponAttack,{BONUS})",
                f"RollBonus(RangedOffHandWeaponAttack,{BONUS})",
                f"IF(IsRangedWeaponAttack()):CharacterWeaponDamage({BONUS})",
            ],
            Icon="PassiveFeature_FightingStyle_Archery",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _armored(self) -> str:
        name = self.make_name("Armored")
        self.loca[f"{name}_DisplayName"] = "Armoured"
        self.loca[f"{name}_Description"] = """
            You are proficient with all types of armour and shields. You gain a +1 bonus to
            <LSTag Tooltip="ArmourClass">Armour Class</LSTag> while wearing armour.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[
                "Proficiency(LightArmor)",
                "Proficiency(MediumArmor)",
                "Proficiency(HeavyArmor)",
                "Proficiency(Shields)",
                "IF(WearingArmor(context.Source)):AC(1)",
            ],
            Icon="PassiveFeature_HeavilyArmored",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _awareness(self) -> str:
        return Awareness(self.mod).add_awareness()

    @cached_property
    def _cunning_actions(self) -> str:
        name = self.make_name("CunningActions")
        self.loca[f"{name}_DisplayName"] = "Cunning Actions"
        self.loca[f"{name}_Description"] = """
            They'll never see you coming, until it's too late. As a bonus action, you can use
            <LSTag Type="Spell" Tooltip="Shout_Dash_CunningAction">Cunning Action: Dash</LSTag>,
            <LSTag Type="Spell" Tooltip="Shout_Hide_BonusAction">Cunning Action: Hide</LSTag>, or
            <LSTag Type="Spell" Tooltip="Shout_Disengage_CunningAction">Cunning Action: Disengage</LSTag>.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Icon="Action_Hide",
            Boosts=[
                "UnlockSpell(Shout_Dash_CunningAction)",
                "UnlockSpell(Shout_Hide_BonusAction)",
                "UnlockSpell(Shout_Disengage_CunningAction)",
            ],
            Properties=["IsHidden"],
        ))
        return name

    @cached_property
    def _duelist(self) -> str:
        name = self.make_name("Duelist")

        INITIATIVE_BONUS = "2"
        DAMAGE_BONUS = "ProficiencyBonus"
        AC_BONUS = "1"

        self.loca[f"{name}_DisplayName"] = "Duelist"
        self.loca[f"{name}_Description"] = """
            When you are wielding a melee weapon that is not Two-Handed in one hand, and no weapon in the other, you
            gain a +[1] bonus to Initiative Rolls, and deal additional damage equal to your
            <LSTag Tooltip="ProficiencyBonus">Proficiency Bonus</LSTag>.
            
            Additionally, if you are not carrying a shield, you gain a +[3] bonus to your
            <LSTag Tooltip="ArmourClass">Armour Class</LSTag>.
        """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            DescriptionParams=[INITIATIVE_BONUS, DAMAGE_BONUS, AC_BONUS],
            Boosts=[
                f"IF(FightingStyle_Dueling(context.Source)):Initiative({INITIATIVE_BONUS})",
                f"IF(FightingStyle_Dueling(context.Source)):CharacterWeaponDamage({DAMAGE_BONUS})",
                f"IF(FightingStyle_Dueling(context.Source) and not HasShieldEquipped(context.Source)):AC({AC_BONUS})",
            ],
            Icon="PassiveFeature_FightingStyle_Duelling",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _elemental_weapon(self) -> str:
        name = self.make_name("Elemental Weapon")
        self.loca[f"{name}_DisplayName"] = "Elemental Weapon"
        self.loca[f"{name}_Description"] = """
            Imbue a weapon with elemental power. It receives a +1 bonus to
            <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>, and deals an additional 1d4 damage of your choice.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[f"UnlockSpell({ElementalWeapon(self.mod).add_elemental_weapon()})"],
            Icon="Spell_Transmutation_ElementalWeapon",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _empowered_spells(self) -> str:
        return EmpoweredSpells(self.mod).add_empowered_spells()

    @staticmethod
    def __strip_white(text: str) -> str:
        return (
            " "
            .join(text.split())
            .strip()
            .replace("( ", "(")
            .replace(" )", ")")
            .replace("): ", "):")
        )

    @cached_property
    def _extra_attacks(self) -> str:
        extra_attacks = self.make_name("ExtraAttacks")
        extra_attacks_status = self.make_name("EXTRA_ATTACKS")

        extra_attack_1 = self.make_name("ExtraAttack_1")
        extra_attack_2 = self.make_name("ExtraAttack_2")
        extra_attack_3 = self.make_name("ExtraAttack_3")
    
        self.loca[f"{extra_attacks}_DisplayName"] = "Extra Attacks"
        self.loca[f"{extra_attacks}_Description"] = """
            Can make an additional free attack after making an unarmed or weapon attack. This increases to two
            additional free attacks at level 11, and three additional free attacks at level 20.
            
            If you gain the Extra Attack feature from more than one class, they don't add together.
        """

        self.add(PassiveData(
            extra_attacks,
            DisplayName=self.loca[f"{extra_attacks}_DisplayName"],
            Description=self.loca[f"{extra_attacks}_Description"],
            Icon="PassiveFeature_ExtraAttack",
            Properties=["Highlighted"],
            StatsFunctorContext=["OnCreate", "OnLongRest"],
            StatsFunctors=[f"ApplyStatus(SELF,{extra_attacks_status},100,-1)"],
        ))

        self.add(StatusData(
            extra_attacks_status,
            StatusType="BOOST",
            DisplayName=self.loca[f"{extra_attacks}_DisplayName"],
            Description=self.loca[f"{extra_attacks}_Description"],
            Icon="PassiveFeature_ExtraAttack",
            Passives=[extra_attack_1, extra_attack_2, extra_attack_3],
            StackId=extra_attacks_status,
            StackType="Ignore",
            StatusGroups=["SG_RemoveOnRespec"],
            StatusPropertyFlags=["DisableOverhead", "IgnoreResting", "DisableCombatlog", "DisablePortraitIndicator"],
        ))

        def conditions(levels: range, status: str) -> str:
            return self.__strip_white(f"""
                CharacterLevelGreaterThan({levels.start - 1})
                and not CharacterLevelGreaterThan({levels.stop - 1})
                and (
                    (
                        context.HasContextFlag(StatsFunctorContext.OnCast)
                        and ExtraAttackSpellCheck()
                        and HasUseCosts('ActionPoint',true)
                        and not Tagged('EXTRA_ATTACK_BLOCKED',context.Source)
                        and not HasStatus('SLAYER_PLAYER',context.Source)
                        and not HasStatus('SLAYER_PLAYER_10',context.Source)
                        and TurnBased(context.Source)
                    ) or (
                        context.HasContextFlag(StatsFunctorContext.OnStatusRemoved)
                        and StatusId('INITIAL_ATTACK_TECHNICAL')
                        and TurnBased()
                    ) or (
                        context.HasContextFlag(StatsFunctorContext.OnStatusApplied)
                        and StatusId('{status}_Q')
                    )
                )
            """)

        def stats_functors(status: str) -> list[str]:
            return [
                self.__strip_white(f"""
                    IF(context.HasContextFlag(StatsFunctorContext.OnCast)):
                        ApplyStatus(SELF,{status}_Q,100,1)
                """),
                self.__strip_white(f"""
                    IF(context.HasContextFlag(StatsFunctorContext.OnStatusRemoved)):
                        ApplyStatus({status}_Q,100,1)
                """),
                self.__strip_white(f"""
                    IF(
                        context.HasContextFlag(StatsFunctorContext.OnStatusApplied)
                        and not HasHigherPriorityExtraAttackQueued('{status}_Q')
                        and not HasAnyExtraAttack()
                    ):
                        ApplyStatus({status},100,1)
                """),
            ]

        self.add(PassiveData(
            extra_attack_1,
            using="ExtraAttack",
            Properties=["IsHidden"],
            StatsFunctorContext=["OnCast", "OnStatusRemoved", "OnStatusApplied"],
            Conditions=conditions(range(5, 11), "EXTRA_ATTACK"),
            StatsFunctors=stats_functors("EXTRA_ATTACK"),
        ))

        self.add(PassiveData(
            extra_attack_2,
            using=extra_attack_1,
            Conditions=conditions(range(11, 20), "EXTRA_ATTACK_2"),
            StatsFunctors=stats_functors("EXTRA_ATTACK_2"),
        ))

        self.add(PassiveData(
            extra_attack_3,
            using=extra_attack_1,
            Conditions=conditions(range(20, 21), "EXTRA_ATTACK_3"),
            StatsFunctors=stats_functors("EXTRA_ATTACK_3"),
        ))

        self.add(Script("""
            function HasHigherPriorityExtraAttackQueued(status, entity)
                local entity = entity or context.Target
                local eaQueuedStatuses = {
                      'EXTRA_ATTACK_3_Q'
                    , 'EXTRA_ATTACK_2_Q'
                    , 'EXTRA_ATTACK_Q'
                    , 'EXTRA_ATTACK_WAR_MAGIC_Q'
                    , 'MAG_MARTIAL_EXERTION_Q'
                    , 'WILDSTRIKE_EXTRA_ATTACK_Q'
                    , 'STALKERS_FLURRY_Q'
                    , 'EXTRA_ATTACK_THIRSTING_BLADE_Q'
                    , 'COMMANDERS_STRIKE_Q_D10'
                    , 'COMMANDERS_STRIKE_Q_D8'
                    , 'WILDSTRIKE_2_EXTRA_ATTACK_Q'
                    , 'EXTRA_ATTACK_WAR_PRIEST_Q'
                }
                for i,v in ipairs(eaQueuedStatuses) do
                    if (v == status) then
                        return ConditionResult(false)
                    end
                    if HasStatus(v, entity, context.Source, false).Result then
                        return ConditionResult(true)
                    end
                end
                return ConditionResult(false)
            end
        """))

        return extra_attacks

    @cached_property
    def _resilience(self) -> str:
        name = self.make_name("Resilience")
        self.loca[f"{name}_DisplayName"] = "Resilience"
        self.loca[f"{name}_Description"] = """
            You shrug off attacks, reducing damage from all sources by your
            <LSTag Tooltip="ProficiencyBonus">Proficiency Bonus</LSTag>.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[f"DamageReduction(All,Flat,ProficiencyBonus)"],
            Icon="PassiveFeature_UnarmoredDefense_Barbarian",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _fire_walk(self) -> str:
        name = self.make_name("FireWalkUnlock")
        self.loca[f"{name}_DisplayName"] = "Fire Walk"
        self.loca[f"{name}_Description"] = "You step through the hells, reappearing in another location."
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[f"UnlockSpell({Movement(self.mod).add_fire_walk()},Singular,,OncePerTurnNoRealtime)"],
            Icon="Target_MAG_Legendary_HellCrawler",
            Properties=["IsHidden"],
        ))
        return name

    @cached_property
    def _light_fingered(self) -> str:
        name = self.make_name("LightFingered")
        self.loca[f"{name}_DisplayName"] = "Light-Fingered"
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
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _martial_artist(self) -> str:
        name = self.make_name("MartialArtist")
        self.loca[f"{name}_DisplayName"] = "Martial Artist"
        self.loca[f"{name}_Description"] = """
            When you make melee unarmed attacks, your Dexterity <LSTag Tooltip="AbilityModifier">Modifier</LSTag> is
            added twice to the damage and <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>.
            Additionally, your damage dice are rolled twice and use the highest result.
        """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[
                "IF(IsMeleeUnarmedAttack()):RollBonus(Attack,DexterityModifier)",
                "IF(IsMeleeUnarmedAttack()):CharacterUnarmedDamage(DexterityModifier)",
                "IF(IsMeleeUnarmedAttack()):Reroll(Damage,20,false)",
            ],
            Icon="Action_Monk_FlurryOfBlows",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _misty_step(self) -> str:
        name = self.make_name("MistyStep")
        self.loca[f"{name}_DisplayName"] = "Misty Step"
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
    def _persuasive(self) -> str:
        name = self.make_name("Persuasive")
        self.loca[f"{name}_DisplayName"] = "Persuasive"
        self.loca[f"{name}_Description"] = """
            You gain <LSTag Tooltip="Expertise">Expertise</LSTag> in
            <LSTag Tooltip="Persuasion">Persuasion</LSTag>.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=["ProficiencyBonus(Skill,Persuasion)", "ExpertiseBonus(Persuasion)"],
            Icon="Spell_Enchantment_Tasha'sHideousLaughter",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _remarkable_athlete(self) -> str:
        return Movement(self.mod).add_remarkable_athlete()

    @cached_property
    def _sturdy(self) -> str:
        name = self.make_name("Sturdy")
        self.add(PassiveData(
            name,
            DisplayName=self.loca(f"{name}_DisplayName", "Sturdy"),
            Description=self.loca(f"{name}_Description", """
                Gain <LSTag Tooltip="Proficiency">Proficiency</LSTag> in Constitution
                <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>.
            """),
            Icon="PassiveFeature_Resilient",
            Properties=["Highlighted"],
            Boosts=["ProficiencyBonus(SavingThrow,Constitution)"],
        ))
        return name

    @cached_property
    def _two_weapon_fighting(self) -> str:
        name = self.make_name("TwoWeaponFighting")
        BONUS = 2
        self.loca[f"{name}_DisplayName"] = "Two-Weapon Fighting"
        self.loca[f"{name}_Description"] = """
            When you make an <LSTag Tooltip="AttackRoll">attack</LSTag> with your off-hand weapon, you can add your
            <LSTag Tooltip="AbilityModifier">Ability Modifier</LSTag> to the damage of the attack.

            While dual wielding, your weapons deal an additional [1] damage.
        """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            DescriptionParams=[f"{BONUS}"],
            Icon="PassiveFeature_FightingStyle_TwoWeaponFighting",
            Properties=["Highlighted"],
            Boosts=[
                "TwoWeaponFighting()",
                f"IF(DualWielder(context.Source)):CharacterWeaponDamage({BONUS})",
            ],
        ))
        return name

    @cached_property
    def _volley(self) -> str:
        name = self.make_name("Volley")
        self.loca[f"{name}_DisplayName"] = "Volley"
        self.loca[f"{name}_Description"] = """
            Strike multiple foes at once. You gain <LSTag Type="Spell" Tooltip="Target_Volley">Volley</LSTag> and
            <LSTag Type="Spell" Tooltip="Shout_Whirlwind">Whirlwind</LSTag>
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=["UnlockSpell(Target_Volley)", "UnlockSpell(Shout_Whirlwind)"],
            Icon="Action_Multiattack_Volley",
            Properties=["IsHidden"],
        ))
        return name

    @cached_property
    def _weapon_bond(self) -> str:
        name = self.make_name("WeaponBond")
        self.add(PassiveData(
            name,
            DisplayName=self.loca(f"{name}_DisplayName", "Weapon Bond"),
            Description=self.loca(f"{name}_Description", """
                Ritually bind the weapon in your main hand. The weapon can't be knocked out of your hand, and it
                automatically returns to you when <LSTag Type="Spell" Tooltip="Throw_Throw">Thrown</LSTag>.
            """),
            Boosts=["UnlockSpell(Shout_WeaponBond)"],
            Icon="Action_Cast_Fighter_WeaponBond",
            Properties=["IsHidden"],
        ))
        self.add(StatusData(
            "WEAPON_BOND",
            StatusType="BOOST",
            using="WEAPON_BOND",
            Boosts=["CannotBeDisarmed()", "ItemReturnToOwner()", "WeaponProperty(Magical)"],
            StatusPropertyFlags=["IgnoreResting"],
        ))
        return name

    @cached_property
    def _weaponmaster(self) -> str:
        name = self.make_name("Weaponmaster")
        BONUS = 2
        self.loca[f"{name}_DisplayName"] = "Weaponmaster"
        self.loca[f"{name}_Description"] = """
            You are proficient with all melee martial weapons, and gain a +[1] bonus to
            <LSTag Tooltip="MeleeWeaponAttack">melee weapon attacks</LSTag> and damage.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            DescriptionParams=[f"{BONUS}"],
            Boosts=[
                "Proficiency(Flails)",
                "Proficiency(Morningstars)",
                "Proficiency(Rapiers)",
                "Proficiency(Scimitars)",
                "Proficiency(Shortswords)",
                "Proficiency(Warpicks)",
                "Proficiency(Battleaxes)",
                "Proficiency(Longswords)",
                "Proficiency(Tridents)",
                "Proficiency(Warhammers)",
                "Proficiency(Glaives)",
                "Proficiency(Greataxes)",
                "Proficiency(Greatswords)",
                "Proficiency(Halberds)",
                "Proficiency(Mauls)",
                "Proficiency(Pikes)",
                f"RollBonus(MeleeWeaponAttack,{BONUS})",
                f"RollBonus(MeleeOffHandWeaponAttack,{BONUS})",
                f"IF(IsMeleeWeaponAttack()):CharacterWeaponDamage({BONUS})",
            ],
            Icon="PassiveFeature_RakishAudacity",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _wilderness_explorer(self) -> str:
        return Movement(self.mod).add_wilderness_explorer()

    @cached_property
    def _bonus_passives(self) -> list[tuple[int, str, str]]:
        return sorted([
            ( 1, "Arcane Adept",        self._arcane_adept),
            ( 1, "Archer",              self._archer),
            ( 1, "Armoured",            self._armored),
            ( 1, "Awareness",           self._awareness),
            ( 1, "Duelist",             self._duelist),
            ( 1, "Devil's Sight",       "DevilsSight"),
            ( 1, "Light-Fingered",      self._light_fingered),
            ( 1, "Martial Artist",      self._martial_artist),
            ( 1, "Mask of Many Faces",  "MaskOfManyFaces"),
            ( 1, "Naturally Stealthy",  "Halfling_LightfootStealth"),
            ( 1, "Persuasive",          self._persuasive),
            ( 1, "Savage Attacks",      "SavageAttacks"),
            ( 1, "Sturdy",              self._sturdy),
            ( 1, "Weaponmaster",        self._weaponmaster),
            ( 1, "Two-Weapon Fighting", self._two_weapon_fighting),
            ( 2, "Action Surge",        self._action_surge),
            ( 2, "Alacrity",            self._alacrity),
            ( 2, "Cunning Actions",     self._cunning_actions),
            ( 3, "Improved Critical",   "ImprovedCritical"),
            ( 3, "Jack of All Trades",  "JackOfAllTrades"),
            ( 3, "Fast Hands",          "FastHands"),
            ( 3, "Remarkable Athlete",  self._remarkable_athlete),
            ( 3, "Resilience",          self._resilience),
            ( 3, "Weapon Bond",         self._weapon_bond),
            ( 5, "Uncanny Dodge",       "UncannyDodge"),
            ( 5, "Extra Attack",        self._extra_attacks),
            ( 5, "Fire Walk",           self._fire_walk),
            ( 5, "Misty Step",          self._misty_step),
            ( 7, "Elemental Weapon",    self._elemental_weapon),
            ( 7, "Evasion",             "Evasion"),
            ( 7, "Wilderness Explorer", self._wilderness_explorer),
            ( 9, "Empowered Spells",    self._empowered_spells),
            ( 9, "Volley",              self._volley),
            (11, "Reliable Talent",     "ReliableTalent"),
        ], key=lambda item: item[1])

    @cache
    def _bonus_passive_list(self, progress: Progression) -> tuple[str, str]:
        list_name = f"Bonus Features Level {progress.Level}"
        list_uuid = self.make_uuid(list_name)
        selector_id = self.make_name(f"{progress.Name}BonusFeatures_Level_{progress.Level}")
        
        if list_uuid not in self._passive_list_uuids:
            self.add(PassiveList(
                Name=list_name,
                Passives=[
                    self._no_selection(progress),
                    *[passive for level, _, passive in self._bonus_passives if progress.Level >= level],
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

        self.loca["BonusFeatures_DisplayName"] = f"Bonus Features"
        self.loca["BonusFeatures_Description"] = f"Select a bonus feature."

        self.add(ProgressionDescription(
            DisplayName=self.loca["BonusFeatures_DisplayName"],
            Description=self.loca["BonusFeatures_Description"],
            ProgressionTableId=progress.TableUUID,
            SelectorId=selector_id,
            UUID=self.make_uuid(f"{selector_id} Description"),
        ))
        
        return (str(list_uuid), selector_id)

    def _remove_asi_from_feats(self) -> None:
        self.add(PassiveData(
            "Actor",
            using="Actor",
            DescriptionParams=[self._ability_bonus, 30],
            Boosts=[
                "ProficiencyBonus(Skill,Deception)",
                "ExpertiseBonus(Deception)",
                "ProficiencyBonus(Skill,Performance)",
                "ExpertiseBonus(Performance)",
                f"Ability(Charisma,{self._ability_bonus},30)",
            ],
        ))

        athlete_asi = self._ability_improvement_for_abilities(
            "Athlete",
            [CharacterAbility.STRENGTH, CharacterAbility.DEXTERITY]
        )
        self.add(Feat(
            Name="Athlete",
            PassivesAdded=["Athlete_StandUp"],
            Selectors=[f"SelectPassives({athlete_asi},1)"],
            UUID="d674aa33-8633-4b67-8623-b6788f0d5fc4",
        ))

        self.loca["Durable_Description"] = """
            You regain full <LSTag Tooltip="HitPoints">hit points</LSTag> when you
            <LSTag Tooltip="ShortRest">Short Rest</LSTag>. Your <LSTag Tooltip="Constitution">Constitution</LSTag> score
            is increased by [1], to a maximum of [2].
        """
        self.add(PassiveData(
            "Durable",
            using="Durable",
            Description=self.loca["Durable_Description"],
            DescriptionParams=[self._ability_bonus, 30],
            Boosts=[f"Ability(Constitution,{self._ability_bonus},30)"],
        ))

        self.loca["HeavilyArmored_Description"] = """
            You have <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Heavy Armour and your
            <LSTag Tooltip="Strength">Strength</LSTag> increases by [1], to a maximum of [2].
        """
        self.add(PassiveData(
            "HeavilyArmored",
            using="HeavilyArmored",
            Description=self.loca["HeavilyArmored_Description"],
            DescriptionParams=[self._ability_bonus, 30],
            Boosts=[f"Ability(Strength,{self._ability_bonus},30)", "Proficiency(HeavyArmor)"],
        ))

        self.add(PassiveData(
            "HeavyArmorMaster",
            using="HeavyArmorMaster",
            DescriptionParams=[self._ability_bonus, 30, 3],
            Boosts=[
                f"Ability(Strength,{self._ability_bonus},30)",
                "IF(HasHeavyArmor() and not HasDamageEffectFlag(DamageFlags.Magical)):DamageReduction(Slashing,Flat,3)",
                "IF(HasHeavyArmor() and not HasDamageEffectFlag(DamageFlags.Magical)):DamageReduction(Bludgeoning,Flat,3)",
                "IF(HasHeavyArmor() and not HasDamageEffectFlag(DamageFlags.Magical)):DamageReduction(Piercing,Flat,3)",
            ],
        ))

        lightly_armored_asi = self._ability_improvement_for_abilities(
            "LightlyArmored",
            [CharacterAbility.STRENGTH, CharacterAbility.DEXTERITY]
        )
        self.add(Feat(
            Name="LightlyArmored",
            PassivesAdded=["LightlyArmored"],
            Selectors=[f"SelectPassives({lightly_armored_asi},1)"],
            UUID="b441c722-e4d4-4702-861a-039bfd77c124",
        ))

        moderately_armored_asi = self._ability_improvement_for_abilities(
            "ModeratelyArmored",
            [CharacterAbility.STRENGTH, CharacterAbility.DEXTERITY]
        )
        self.add(Feat(
            Name="ModeratelyArmored",
            PassivesAdded=["ModeratelyArmored"],
            Requirements="FeatRequirementProficiency('LightArmor')",
            Selectors=[f"SelectPassives({moderately_armored_asi},1)"],
            UUID="681d5307-f0ed-4c94-8cf0-db0c51116f56",
        ))

        performer_asi = self._ability_improvement(CharacterAbility.CHARISMA, "Performer")
        self.add(Feat(
            Name="Performer",
            PassivesAdded=["Performer", performer_asi],
            UUID="60dfd716-3ba8-4611-90ee-018b59775b1d",
        ))

        for ability in CharacterAbility:
            ability_name = ability.name.title()
            resilient_passive = f"Resilient_{ability_name}"
            self.add(PassiveData(
                resilient_passive,
                using=resilient_passive,
                DescriptionParams=[self._ability_bonus],
                Boosts=[
                    f"Ability({ability_name},{self._ability_bonus},30)",
                    f"ProficiencyBonus(SavingThrow,{ability_name})",
                ],
            ))

        tavern_brawler_asi = self._ability_improvement_for_abilities(
            "TavernBrawler",
            [CharacterAbility.STRENGTH, CharacterAbility.CONSTITUTION]
        )
        self.add(Feat(
            Name="TavernBrawler",
            PassivesAdded=["TavernBrawler"],
            Selectors=[f"SelectPassives({tavern_brawler_asi},1)"],
            UUID="be0889d2-f9aa-472d-b942-592bff0f1ef3",
        ))

        weapon_master_asi = self._ability_improvement_for_abilities(
            "WeaponMaster",
            [CharacterAbility.STRENGTH, CharacterAbility.DEXTERITY]
        )
        self.add(Feat(
            Name="WeaponMaster",
            PassivesAdded=["WeaponMaster"],
            Selectors=[
                f"SelectPassives({weapon_master_asi},1)",
                "SelectPassives(f21e6b94-44e8-4ae0-a6f1-0c81abac03a2,4,WeaponMasterProficiencies)",
            ],
            UUID="b153e75c-27a2-4412-95cd-60b477121679",
        ))

    @cached_property
    def _bolster(self) -> str:
        return Bolster(self.mod).add_bolster()

    @cached_property
    def _restoration_display_name(self) -> str:
        name = self.make_name("Restoration")
        self.loca[f"{name}_DisplayName"] = "Restoration"
        return self.loca[f"{name}_DisplayName"]

    @cached_property
    def _restoration_description(self) -> str:
        name = self.make_name("Restoration")
        self.loca[f"{name}_Description"] = """
            You and nearby allies are revitalised as though you would have taken a
            <LSTag Tooltip="LongRest">Long Rest</LSTag>.
        """
        return self.loca[f"{name}_Description"]

    @cached_property
    def _restoration_description_after_combat(self) -> str:
        name = self.make_name("RestorationAfterCombat")
        self.loca[f"{name}_Description"] = """
            When combat ends, you are revitalised as though you would have taken a
            <LSTag Tooltip="LongRest">Long Rest</LSTag>.
        """
        return self.loca[f"{name}_Description"]

    @cached_property
    def _restoration_status(self) -> str:
        name = self.make_name("Restoration").upper()
        self.add(StatusData(
            name,
            StatusType="BOOST",
            DisplayName=self._restoration_display_name,
            Description=self._restoration_description,
            Icon="Action_RegainHP",
            StackId=name,
            StatusPropertyFlags=["DisableOverhead", "DisableCombatlog", "DisablePortraitIndicator"],
            ApplyEffect="4019eeae-d4e3-449b-ba4a-6d7422ec6807",
            OnApplyFunctors=[
                "RemoveStatus(SELF,DIRT_COVERED)",
                "RemoveStatus(SELF,DIRT_COVERED_FULL)",
                "RemoveStatus(SELF,DIRT_COVERED_SLIGHT)",
                "RemoveStatus(SELF,BLOOD_COVERED)",
                "RemoveStatus(SELF,BLOOD_COVERED_FULL)",
                "RemoveStatus(SELF,BLOOD_COVERED_SLIGHT)",
                "RemoveStatus(SELF,SMELLY)",
                "RemoveStatus(SELF,STENCH)",
                "RemoveStatus(SELF,STENCH_GHAST)",
                "ResetCooldowns(UntilRest)",
                "RegainHitPoints(Target.MaxHP)",
                "RestoreResource(SpellSlot,100%,1)",
                "RestoreResource(SpellSlot,100%,2)",
                "RestoreResource(SpellSlot,100%,3)",
                "RestoreResource(SpellSlot,100%,4)",
                "RestoreResource(SpellSlot,100%,5)",
                "RestoreResource(SpellSlot,100%,6)",
                "RestoreResource(SpellSlot,100%,7)",
                "RestoreResource(SpellSlot,100%,8)",
                "RestoreResource(SpellSlot,100%,9)",
                "RestoreResource(WarlockSpellSlot,100%,1)",
                "RestoreResource(WarlockSpellSlot,100%,2)",
                "RestoreResource(WarlockSpellSlot,100%,3)",
                "RestoreResource(WarlockSpellSlot,100%,4)",
                "RestoreResource(WarlockSpellSlot,100%,5)",
                "RestoreResource(WarlockSpellSlot,100%,6)",
                "RestoreResource(ShadowSpellSlot,100%,1)",
                "RestoreResource(SorceryPoint,100%,0)",
                "RestoreResource(ChannelDivinity,100%,0)",
                "RestoreResource(SuperiorityDie,100%,0)",
                "RestoreResource(KiPoint,100%,0)",
                "RestoreResource(WildShape,100%,0)",
                "RestoreResource(WeaponActionPoint,100%,0)",
                "RestoreResource(TidesOfChaos,100%,0)",
                "RestoreResource(ChannelOath,100%,0)",
                "RestoreResource(Rage,100%,0)",
                "RestoreResource(BardicInspiration,100%,0)",
                "RestoreResource(HitDice,100%,0)",
                "RestoreResource(ArcaneRecoveryPoint,100%,0)",
                "RestoreResource(NaturalRecoveryPoint,100%,0)",
                "RestoreResource(RitualPoint,100%,0)",
                "RestoreResource(LayOnHandsCharge,100%,0)",
                "RestoreResource(Interrupt_HellishRebukeTiefling_Charge,100%,0)",
                "RestoreResource(Interrupt_HellishRebukeWarlockMI_Charge,100%,0)",
                "RestoreResource(FungalInfestationCharge,100%,0)",
                "RestoreResource(LuckPoint,100%,0)",
                "RestoreResource(WarPriestActionPoint,100%,0)",
                "RestoreResource(ArcaneShot,100%,0)",
                "RestoreResource(StarMapPoint,100%,0)",
                "RestoreResource(CosmicOmen,100%,0)",
                "RestoreResource(WrithingTidePoint,100%,0)",
                "RestoreResource(Bladesong,100%,0)",
            ],
            SplatterDirtAmount=-2,
            SplatterBloodAmount=-2,
            SplatterSweatAmount=-2,
        ))
        return name

    @cached_property
    def _restoration(self) -> str:
        name = self.make_name("Restoration")
        self.add(SpellData(
            name,
            SpellType="Shout",
            DisplayName=self._restoration_display_name,
            Description=self._restoration_description,
            Icon="Action_RegainHP",
            SpellProperties=[f"ApplyStatus({self._restoration_status},100,1)"],
            AIFlags=["CanNotUse"],
            AreaRadius=36,
            TargetConditions=["Party() and not Dead()"],
            CastSound="Action_Cast_RegainHP",
            TargetSound="Action_Impact_RegainHP",
            CastTextEvent="Cast",
            PreviewCursor="Cast",
            UseCosts="ActionPoint:1",
            SpellAnimation=[
                "414bbf02-2918-4f01-83fb-1ddc7a588d88,,",
                ",,",
                "7abe77ed-9c77-4eac-872c-5b8caed070b6,,",
                "cb171bda-f065-4520-b470-e447f678ba1f,,",
                "0c5dcc83-fa78-41da-b6a5-440b5ea30936,,",
                ",,",
                "bea988a0-2ec5-40d8-a67e-ffbd7454bc53,,",
                ",,",
                ",,",
            ],
            VerbalIntent="Healing",
            SpellFlags=["Invisible", "Stealth"],
            HitAnimationType="None",
            Requirements=["!Combat"],
            PrepareEffect="96a51ac8-2e7e-4718-bb62-dcfd18964a02",
            CastEffect="9396e4e3-2af9-465e-adba-5714d97ce66f",
        ))
        return name

    @cached_property
    def _restoration_after_combat(self) -> str:
        name = self.make_name("RestorationAfterCombat")
        self.add(PassiveData(
            name,
            DisplayName=self._restoration_display_name,
            Description=self._restoration_description_after_combat,
            Icon="Action_RegainHP",
            StatsFunctorContext=["OnCombatEnded"],
            StatsFunctors=[f"ApplyStatus(SELF,{self._restoration_status},100,1)"],
            Properties=["IsToggled", "ToggledDefaultAddToHotbar", "ToggleForParty"],
        ))
        return name

    def _add_bonus_spells_to_common_player_actions(self) -> str:
        self.add(SpellSet(
            Name="CommonPlayerActions",
            Spells=[
                "Projectile_Jump",
                "Target_Dip",
                "Shout_Hide",
                "Target_Shove",
                "Throw_Throw",
                "Throw_ImprovisedWeapon",
                "Shout_Dash",
                "Target_Help",
                "Shout_Disengage",
                self._restoration,
                self._bolster,
            ],
        ))

    @progression(BASE_CHARACTER_RACES, 1)
    def level_1(self, progress: Progression) -> None:
        bonus_skills = 4 if progress.Name != "Human" else 6
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            self._restoration_after_combat,
        ]
        progress.Selectors = [s for s in (progress.Selectors or []) if not s.startswith("SelectSkills(")] + [
            f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{bonus_skills},{self.mod.get_name()})",
            "SelectPassives({},1,{})".format(*self._abilities_bonus_passive_list(progress)),
            "SelectPassives({},1,{})".format(*self._bonus_passive_list(progress)),
        ]
        self.add(SkillsDefaultValue(
            Add=self._SKILL_LIST,
            Level=1,
            SelectorId=self.mod.get_name(),
            TableUUID=progress.TableUUID,
            UUID=self.make_uuid(f"{progress.Name}_SkillsDefaultValue"),
        ))

    @progression(BASE_CHARACTER_RACES, 2)
    def level_2(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives({},1,{})".format(*self._ability_improvement_passive_list(progress)),
            "SelectPassives({},1,{})".format(*self._bonus_passive_list(progress)),
        ]

    @progression(BASE_CHARACTER_RACES, range(3, 21, 2))
    def odd_levels(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives({},1,{})".format(*self._ability_improvement_passive_list(progress)),
            "SelectPassives({},1,{})".format(*self._bonus_passive_list(progress)),
        ]

if __name__ == "__main__":
    bonus_features = BonusFeatures(
        classes=[CharacterClass.ROGUE],  # Ignored, but prevents multiclass slots from being updated
    )
    bonus_features.build()
