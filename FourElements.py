import os

from functools import cached_property
from moddb import character_level_range
from modtools.gamedata import PassiveData, SpellData, StatusData
from modtools.lsx.game import LevelMapSeries, Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)
from typing import ClassVar
from uuid import UUID


class FourElements(Replacer):
    _fangs_of_the_fire_snake_status: ClassVar[str] = "FANGS_OF_THE_FIRE_SNAKE"
    _cantrip_damage: ClassVar[str] = "1d10"
    _cantrip_status_damage: ClassVar[str] = "LevelMapValue(MartialArts)"

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="FourElements",
                         description="A class replacer for FourElements.",
                         **kwds)

        self.add(character_level_range)

    @cached_property
    def _awareness(self) -> str:
        """The Awareness passive, a variant of Alert."""
        name = self.make_name("Awareness")
        awareness_level_map = f"{name}_LevelMap"

        self.loca[f"{name}_DisplayName"] = "Awareness"
        self.loca[f"{name}_Description"] = """
            You have honed your senses to the utmost degree. You gain a +[1] bonus to Initiative, can't be
            <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>, and attackers can't land
            <LSTag Tooltip="CriticalHit">Critical Hits</LSTag> against you.
            """

        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            DescriptionParams=[f"LevelMapValue({awareness_level_map})"],
            Icon="Action_Barbarian_MagicAwareness",
            Properties=["ForceShowInCC", "Highlighted"],
            Boosts=[
                "IF(CharacterLevelRange(1,4)):Initiative(1)",
                "IF(CharacterLevelRange(5,6)):Initiative(2)",
                "IF(CharacterLevelRange(7,8)):Initiative(3)",
                "IF(CharacterLevelRange(9,10)):Initiative(4)",
                "IF(CharacterLevelRange(11,20)):Initiative(5)",
                "StatusImmunity(SURPRISED)",
                "CriticalHit(AttackTarget,Success,Never)",
            ],
        ))

        self.add(LevelMapSeries(
            **{f"Level{level}": 1 for level in range(1, 3)},
            **{f"Level{level}": int((level - 1) / 2) for level in range(3, 12)},
            **{f"Level{level}": 5 for level in range(12, 21)},
            Name=awareness_level_map,
            UUID=self.make_uuid(awareness_level_map),
        ))

        return name

    @cached_property
    def _level_3_spell_list(self) -> UUID:
        name = "Way of the Four Elements level 3 spells"
        uuid = self.make_uuid(name)
        self.add(SpellList(
            Name=name,
            Spells=[
                self._chill_of_the_mountain,
                self._fangs_of_the_fire_snake,
                self._touch_of_the_storm,
                self._crash_of_thunder,
                "Target_FlurryOfBlows",
                self._bonus_unarmed_strike,
                self._harmony_of_fire_and_water,
            ],
            UUID=uuid,
        ))
        return uuid

    @cached_property
    def _harmony_of_fire_and_water(self) -> str:
        name = self.make_name("HarmonyOfFireAndWater")

        self.add(SpellData(
            name,
            using="Shout_HarmonyOfFireAndWater",
            SpellType="Shout",
            Description="h004d056bga0c0g4211g864fgd0a167f0cf2d;4",  # Song of Rest description
            SpellProperties=["ShortRest()"],
            VerbalIntent="Healing",
            SpellFlags=["HasVerbalComponent"],
            RequirementConditions=["CanShortRest('NotEnoughResources')"],
            RequirementEvents=["OnTurn", "OnCombatEnded"],
            Requirements=[],
        ))

        return name

    @cached_property
    def _bonus_unarmed_strike(self) -> str:
        name = self.make_name("BonusUnarmedStrike")

        self.add(SpellData(
            name,
            using="Target_UnarmedStrike_Monk",
            SpellType="Target",
            SpellFlags=["IsMelee", "IsHarmful", "DisableBlood"],
        ))

        return name

    @cached_property
    def _chill_of_the_mountain(self) -> str:
        chill_of_the_mountain = "Projectile_RayOfFrost_Monk"
        chill_of_the_mountain_status = self.make_name("CHILL_OF_THE_MOUNTAIN")

        self.loca[f"{chill_of_the_mountain}_Description"] = """
            Call forth the cold mountain winds. Your next melee attacks deal an additional [2].
        """

        self.add(SpellData(
            chill_of_the_mountain,
            using=chill_of_the_mountain,
            SpellType="Projectile",
            Description=self.loca[f"{chill_of_the_mountain}_Description"],
            DescriptionParams=["Distance(3)", f"DealDamage({self._cantrip_status_damage},Cold)"],
            SpellProperties=[
                "GROUND:SurfaceChange(Freeze)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
                f"ApplyStatus(SELF,{chill_of_the_mountain_status},100,1)",
            ],
            SpellRoll="Attack(AttackType.MeleeUnarmedAttack)",
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Cold,Magical)",
            ],
            TooltipDamageList=[
                "DealDamage(MartialArtsUnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Cold)",
            ],
            TooltipStatusApply=[
                f"ApplyStatus({chill_of_the_mountain_status},100,1)",
            ],
            UseCosts=["ActionPoint:1", "KiPoint:1"],
        ))

        self.loca[f"{chill_of_the_mountain_status}_DisplayName"] = "Chill of the Mountain"
        self.loca[f"{chill_of_the_mountain_status}_Description"] = """
            Affected entity's fists are glistening with frost. Its melee attacks deal an additional [1].
        """
        
        self.add(StatusData(
            chill_of_the_mountain_status,
            using=self._fangs_of_the_fire_snake_status,
            StatusType="BOOST",
            Boosts=[
                f"CharacterWeaponDamage({self._cantrip_status_damage},Cold)",
                f"CharacterUnarmedDamage({self._cantrip_status_damage},Cold)",
            ],
            DisplayName=self.loca[f"{chill_of_the_mountain_status}_DisplayName"],
            Description=self.loca[f"{chill_of_the_mountain_status}_Description"],
            DescriptionParams=[f"DealDamage({self._cantrip_status_damage},Cold)"],
            Icon="Spell_Evocation_ChromaticOrb_Cold",
            StatusEffect="6648ef67-84a4-4191-ad6b-3d2538a983c6",
        ))

        return chill_of_the_mountain

    @cached_property
    def _fangs_of_the_fire_snake(self) -> str:
        fangs_of_the_fire_snake = "Projectile_FangsOfTheFireSnake"

        self.add(SpellData(
            fangs_of_the_fire_snake,
            using=fangs_of_the_fire_snake,
            SpellType="Projectile",
            DescriptionParams=[f"DealDamage({self._cantrip_status_damage},Fire)"],
            SpellProperties=[
                f"GROUND:DealDamage({self._cantrip_damage},Fire)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
                f"ApplyStatus(SELF,{self._fangs_of_the_fire_snake_status},100,1)",
            ],
            SpellRoll="Attack(AttackType.MeleeUnarmedAttack)",
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Fire,Magical)",
            ],
            TargetRadius=18,
            TooltipDamageList=[
                "DealDamage(MartialArtsUnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Fire)",
            ],
            UseCosts=["ActionPoint:1", "KiPoint:1"],
        ))

        self.add(StatusData(
            self._fangs_of_the_fire_snake_status,
            using=self._fangs_of_the_fire_snake_status,
            StatusType="BOOST",
            Boosts=[
                f"CharacterWeaponDamage({self._cantrip_status_damage},Fire)",
                f"CharacterUnarmedDamage({self._cantrip_status_damage},Fire)",
            ],
            DescriptionParams=[f"DealDamage({self._cantrip_status_damage},Fire)"],
            StatusEffect="43d61721-9a1a-4cef-bc33-8bb54f30de9d",
        ))

        return fangs_of_the_fire_snake

    @cached_property
    def _touch_of_the_storm(self) -> str:
        touch_of_the_storm = "Target_ShockingGrasp_Monk"
        touch_of_the_storm_status = self.make_name("TOUCH_OF_THE_STORM")

        self.loca[f"{touch_of_the_storm}_DisplayName"] = "Strike of the Storm"
        self.loca[f"{touch_of_the_storm}_Description"] = """
            Strike with the power of the storms. This attack has <LSTag Tooltip="Advantage">Advantage</LSTag> on
            creatures with metal armour. Your next melee attacks deal an additional [1].
        """

        self.add(SpellData(
            touch_of_the_storm,
            using=touch_of_the_storm,
            SpellType="Target",
            DisplayName=self.loca[f"{touch_of_the_storm}_DisplayName"],
            Description=self.loca[f"{touch_of_the_storm}_Description"],
            DescriptionParams=[f"DealDamage({self._cantrip_status_damage},Lightning)"],
            Icon="Spell_Evocation_WitchBolt",
            SpellProperties=[
                "GROUND:SurfaceChange(Electrify)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
                f"ApplyStatus(SELF,{touch_of_the_storm_status},100,1)",
            ],
            SpellRoll="Attack(AttackType.MeleeUnarmedAttack,HasMetalArmor() or IsMetalCharacter())",
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Lightning,Magical)",
            ],
            TargetRadius=18,
            TooltipDamageList=[
                "DealDamage(MartialArtsUnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Lightning)",
            ],
            TooltipStatusApply=[
                f"ApplyStatus({touch_of_the_storm_status},100,1)",
            ],
            UseCosts=["ActionPoint:1", "KiPoint:1"],
        ))

        self.loca[f"{touch_of_the_storm_status}_Description"] = """
            Affected entity's fists are sparking with lightning. Its melee attacks deal an additional [1].
        """
        
        self.add(StatusData(
            touch_of_the_storm_status,
            using=self._fangs_of_the_fire_snake_status,
            StatusType="BOOST",
            Boosts=[
                f"CharacterWeaponDamage({self._cantrip_status_damage},Lightning)",
                f"CharacterUnarmedDamage({self._cantrip_status_damage},Lightning)",
            ],
            DisplayName=self.loca[f"{touch_of_the_storm}_DisplayName"],
            Description=self.loca[f"{touch_of_the_storm_status}_Description"],
            DescriptionParams=[f"DealDamage({self._cantrip_status_damage},Lightning)"],
            Icon="Spell_Evocation_ChromaticOrb_Lightning",
            StatusEffect="18143f47-3bb2-48eb-bf3d-a0be7c712d00",
        ))

        return touch_of_the_storm

    @cached_property
    def _crash_of_thunder(self) -> str:
        crash_of_thunder = self.make_name("CrashOfThunder")
        crash_of_thunder_status = self.make_name("CRASH_OF_THUNDER")

        self.loca[f"{crash_of_thunder}_DisplayName"] = "Crash of Thunder"
        self.loca[f"{crash_of_thunder}_Description"] = """
            Shake your target with a crash of thunder. Your next melee attacks deal an additional [1].
        """

        self.add(SpellData(
            crash_of_thunder,
            using="Projectile_ChromaticOrb_Thunder",
            SpellType="Target",
            Level="",
            DisplayName=self.loca[f"{crash_of_thunder}_DisplayName"],
            Description=self.loca[f"{crash_of_thunder}_Description"],
            DescriptionParams=[f"DealDamage({self._cantrip_status_damage},Thunder)"],
            SpellProperties=[
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
                f"ApplyStatus(SELF,{crash_of_thunder_status},100,1)",
            ],
            SpellRoll="Attack(AttackType.MeleeUnarmedAttack)",
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Thunder,Magical)",
            ],
            TargetRadius=18,
            TooltipDamageList=[
                "DealDamage(MartialArtsUnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Thunder)",
            ],
            TooltipStatusApply=[
                f"ApplyStatus({crash_of_thunder_status},100,1)",
            ],
            TooltipUpcastDescription="",
            TooltipUpcastDescriptionParams=[],
            UseCosts=["ActionPoint:1", "KiPoint:1"],
        ))

        self.loca[f"{crash_of_thunder_status}_Description"] = """
            Affected entity's fists are echoing with thunder. Its melee attacks deal an additional [1].
        """
        
        self.add(StatusData(
            crash_of_thunder_status,
            using=self._fangs_of_the_fire_snake_status,
            StatusType="BOOST",
            Boosts=[
                f"CharacterWeaponDamage({self._cantrip_status_damage},Thunder)",
                f"CharacterUnarmedDamage({self._cantrip_status_damage},Thunder)",
            ],
            DisplayName=self.loca[f"{crash_of_thunder}_DisplayName"],
            Description=self.loca[f"{crash_of_thunder_status}_Description"],
            DescriptionParams=[f"DealDamage({self._cantrip_status_damage},Thunder)"],
            Icon="Spell_Evocation_ChromaticOrb_Thunder",
            StatusEffect="64153d5b-c66f-41a8-a4f6-73b801888be7",
        ))

        return crash_of_thunder

    @progression(CharacterClass.MONK_FOURELEMENTS, 3)
    def fourelements_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._awareness]
        progress.PassivesRemoved = ["MartialArts_BonusUnarmedStrike", "FlurryOfBlowsUnlock"]
        progress.Selectors = [
            f"AddSpells({self._level_3_spell_list})",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 4)
    def fourelements_level_4(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 5)
    def fourelements_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["UncannyDodge"]
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 6)
    def fourelements_level_6(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 7)
    def fourelements_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = ["FastHands"]
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 8)
    def fourelements_level_8(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 9)
    def fourelements_level_9(self, progress: Progression) -> None:
        progress.PassivesAdded = []
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 10)
    def fourelements_level_10(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 11)
    def fourelements_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2", "ReliableTalent"]
        progress.PassivesRemoved = ["ExtraAttack"]
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 12)
    def fourelements_level_12(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 13)
    def fourelements_level_13(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 14)
    def fourelements_level_14(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 15)
    def fourelements_level_15(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 16)
    def fourelements_level_16(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 17)
    def fourelements_level_17(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 18)
    def fourelements_level_18(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 19)
    def fourelements_level_19(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.MONK_FOURELEMENTS, 20)
    def fourelements_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]
        progress.Selectors = []


def main() -> None:
    four_elements = FourElements(
        classes=[CharacterClass.MONK_FOURELEMENTS],
        feats=2,
        spells=2,
        warlock_spells=2,
        actions=2,
        skills=None,
        expertise=None,
        full_caster=False,
    )
    four_elements.build()


if __name__ == "__main__":
    main()
