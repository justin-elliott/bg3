#!/usr/bin/env python3
"""
Generates files for Bonus Features, a mod to give all races optional bonus features.
"""

from functools import cache, cached_property
import os

from moddb import (
    Awareness,
    BattleMagic,
    Movement,
)
from modtools.gamedata import PassiveData
from modtools.lsx.game import (
    BASE_CHARACTER_RACES,
    CharacterAbility,
    CharacterClass,
    DefaultValue,
    PassiveList,
    Progression,
    ProgressionDescription,
)
from modtools.replacers import (
    progression,
    Replacer,
)


class BonusFeatures(Replacer):
    _no_selection_ids: set[str]
    _passive_list_uuids: set[str]

    def __init__(self, **kwds: str):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="BonusFeatures",
                         description="Optional bonus features for all races.",
                         **kwds)
        
        self._no_selection_ids = set()
        self._passive_list_uuids = set()

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
        self.add(DefaultValue(
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
    def _awareness(self) -> str:
        return Awareness(self.mod).add_awareness()

    @cached_property
    def _battle_magic(self) -> str:
        return BattleMagic(self.mod).add_battle_magic()

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
    def _resilience(self) -> str:
        name = self.make_name("Resilience")
        BONUS = "ProficiencyBonus"
        self.loca[f"{name}_DisplayName"] = "Resilience"
        self.loca[f"{name}_Description"] = """
            You shrug off attacks, taking [1] less damage from all sources.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            DescriptionParams=[f"{BONUS}"],
            Boosts=[f"DamageReduction(All,Flat,{BONUS})"],
            Icon="PassiveFeature_UnarmoredDefense_Barbarian",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _fire_walk(self) -> str:
        name = self.make_name("FireWalk")
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
    def _fleet_of_foot(self) -> str:
        self.loca["FleetOfFoot"] = "Fleet of Foot"
        return Movement(self.mod).add_fast_movement(3.0, self.loca["FleetOfFoot"])

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
        name = self.make_name("WildernessExplorer")
        self.loca[f"{name}_DisplayName"] = "Wilderness Explorer"
        self.loca[f"{name}_Description"] = """
            You have become an expert at moving through the wilderness.
            <LSTag Type="Status" Tooltip="DIFFICULT_TERRAIN">Difficult Terrain</LSTag> no longer slows you down, and
            you can't slip on grease or ice.
            """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[
                "StatusImmunity(SG_DifficultTerrain)",
                "StatusImmunity(PRONE_GREASE)",
                "StatusImmunity(PRONE_ICE)",
            ],
            Icon="PassiveFeature_LandsStride_DifficultTerrain",
            Properties=["Highlighted"],
        ))
        return name

    @cached_property
    def _bonus_passives(self) -> list[tuple[int, str, str]]:
        return sorted([
            ( 1, "Arcane Adept",        self._arcane_adept),
            ( 1, "Archer",              self._archer),
            ( 1, "Athlete",             "Athlete_StandUp"),
            ( 1, "Devil's Sight",       "DevilsSight"),
            ( 1, "Light-Fingered",      self._light_fingered),
            ( 1, "Naturally Stealthy",  "Halfling_LightfootStealth"),
            ( 1, "Savage Attacks",      "SavageAttacks"),
            ( 1, "Weaponmaster",        self._weaponmaster),
            ( 1, "Two-Weapon Fighting", "FightingStyle_TwoWeaponFighting"),
            ( 3, "Battle Magic",        self._battle_magic),
            ( 3, "Cunning Actions",     self._cunning_actions),
            ( 3, "Fast Hands",          "FastHands"),
            ( 3, "Fleet of Foot",       self._fleet_of_foot),
            ( 3, "Improved Critical",   "ImprovedCritical"),
            ( 3, "Jack of All Trades",  "JackOfAllTrades"),
            ( 3, "Resilience",          self._resilience),
            ( 5, "Awareness",           self._awareness),
            ( 5, "Uncanny Dodge",       "UncannyDodge"),
            ( 5, "Extra Attack",        "ExtraAttack"),
            ( 5, "Fire Walk",           self._fire_walk),
            ( 5, "Misty Step",          self._misty_step),
            ( 7, "Evasion",             "Evasion"),
            ( 7, "Wilderness Explorer", self._wilderness_explorer),
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

        self.add(DefaultValue(
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

    @progression(BASE_CHARACTER_RACES, 1)
    def level_1(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectPassives({},1,{})".format(*self._abilities_bonus_passive_list(progress)),
        ]

    @progression(BASE_CHARACTER_RACES, range(1, 21, 2))
    def odd_levels(self, progress: Progression) -> None:
        progress.Selectors = (progress.Selectors or []) + [
            "SelectPassives({},1,{})".format(*self._bonus_passive_list(progress)),
        ]

if __name__ == "__main__":
    bonus_features = BonusFeatures(
        classes=[CharacterClass.ROGUE],  # Ignored, but prevents multiclass slots from being updated
    )
    bonus_features.build()
