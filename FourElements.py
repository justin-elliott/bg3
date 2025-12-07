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
        self._modify_spells()

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
    def _unarmed_acuity(self) -> str:
        name = self.make_name("UnarmedAcuity")

        self.loca[f"{name}_DisplayName"] = "Unarmed Acuity"
        self.loca[f"{name}_Description"] = """
            Whenever you deal damage with an unarmed attack, you gain
            <LSTag Type="Status" Tooltip="MAG_GISH_ARCANE_ACUITY">Arcane Acuity</LSTag> for 2 turns.
        """

        self.add(PassiveData(
            name,
            using="MAG_ElementalGish_ArcaneAcuity_Helmet_Passive",
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Icon="PassiveFeature_MartialArts_BonusUnarmedStrike",
            Conditions="IsUnarmedAttack()",
            Properties=["Highlighted"],
        ))

        return name

    @cached_property
    def _level_3_spell_list(self) -> UUID:
        name = "Way of the Four Elements level 3 spells"
        uuid = self.make_uuid(name)
        self.add(SpellList(
            Name=name,
            Spells=[
                self._flurry_of_blows,
                self._chill_of_the_mountain,
                self._fangs_of_the_fire_snake,
                self._touch_of_the_storm,
                "Shout_HarmonyOfFireAndWater",
            ],
            UUID=uuid,
        ))
        return uuid

    @cached_property
    def _flurry_of_blows(self) -> str:
        name = self.make_name("FlurryOfBlows")

        self.add(SpellData(
            name,
            using="Target_FlurryOfBlows",
            SpellType="Target",
            UseCosts=["BonusActionPoint:1"],
        ))

        return name

    @cached_property
    def _chill_of_the_mountain(self) -> str:
        chill_of_the_mountain = "Projectile_RayOfFrost_Monk"
        chill_of_the_mountain_status = self.make_name("CHILL_OF_THE_MOUNTAIN")

        self.loca[f"{chill_of_the_mountain}_Description"] = """
            Call forth the cold mountain winds and reduce the target's
            <LSTag Tooltip="MovementSpeed">movement speed</LSTag> by [1].
            Your next melee attacks deal an additional [2].
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
                "ApplyStatus(RAY_OF_FROST,100,1)",
            ],
            TooltipDamageList=[
                "DealDamage(MartialArtsUnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Cold)",
            ],
            TooltipStatusApply=[
                "ApplyStatus(RAY_OF_FROST,100,1)",
                f"ApplyStatus({chill_of_the_mountain_status},100,1)",
            ],
            UseCosts=["ActionPoint:1"],
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
            UseCosts=["ActionPoint:1"],
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
            The target cannot use reactions. This spell has <LSTag Tooltip="Advantage">Advantage</LSTag> on creatures
            with metal armour. Your next melee attacks deal an additional [1].
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
                "ApplyStatus(SHOCKING_GRASP,100,1)",
            ],
            TargetRadius=18,
            TooltipDamageList=[
                "DealDamage(MartialArtsUnarmedDamage,Bludgeoning)",
                f"DealDamage({self._cantrip_damage},Lightning)",
            ],
            TooltipStatusApply=[
                "ApplyStatus(SHOCKING_GRASP,100,1)",
                f"ApplyStatus({touch_of_the_storm_status},100,1)",
            ],
            UseCosts=["ActionPoint:1"],
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

    def _modify_spells(self) -> None:
        self.add(SpellData(
            "Projectile_Fireball_Monk",
            using="Projectile_Fireball_Monk",
            SpellType="Projectile",
        ))
        
        self.add(SpellData(
            "Shout_GaseousForm_Monk",
            using="Shout_GaseousForm_Monk",
            SpellType="Shout",
            RitualCosts=["ActionPoint:1"],
            SpellFlags=["HasSomaticComponent"],
        ))
        
        self.add(SpellData(
            "Shout_Fly_Monk",
            using="Shout_Fly_Monk",
            SpellType="Shout",
            RitualCosts=["ActionPoint:1"],
            SpellFlags=["HasSomaticComponent"],
        ))
        
        hold_monster_status = self.make_name("HOLD_MONSTER_MONK")

        self.add(SpellData(
            "Target_HoldPerson_Monk",
            using="Target_HoldMonster",
            SpellType="Target",
            Level="",
            SpellSuccess=[f"ApplyStatus({hold_monster_status},100,10)"],
            AmountOfTargets="LevelMapValue(HoldPerson_Monk)",
            DisplayName="hd82ec163ge78ag4ecbgae09g7fab45598d2d;2",
            TooltipStatusApply=[f"ApplyStatus({hold_monster_status},100,10)"],
            PrepareSound="Vocal_Component_Monk_Control",
            CastSound="Spell_Cast_Monk_ClenchoftheNorthwind_L1to3",
            TargetSound="Vocal_Component_Stop",
            VocalComponentSound="Vocal_Component_Stop",
            UseCosts=["ActionPoint:1", "KiPoint:3"],
            SpellAnimation=[
                "32456253-9787-49c8-9775-4cd93d602f05,,",
                ",,",
                "32415fee-295d-4fed-a7f4-d2f9218ff9c1,,",
                "05f29a9a-58d1-43d2-84cf-5a95ab5baa24,,",
                "5c9e3bb0-8963-4cc3-aa24-c0ba1c49494b,,",
                ",,",
                "c79f1495-5c5c-4e22-bed4-38beb3779b23,,",
                ",,",
                ",,",
            ],
            SpellStyleGroup="Class",
            SpellFlags=["HasVerbalComponent", "HasSomaticComponent", "HasHighGroundRangeExtension", "IsHarmful"],
            PrepareEffect="76154940-c4fc-4adb-b700-87051865380f",
            CastEffect="b05bd9fd-c2d2-44c9-ae77-c58b17aa2443",
            TargetEffect="57190c62-9877-46f5-acd4-ca35093a5e8a",
        ))
        
        self.add(StatusData(
            hold_monster_status,
            using="HOLD_MONSTER",
            StatusType="INCAPACITATED",
            StatusEffect="3c134510-649a-4aa7-a4bf-2dd243cc173b",
        ))

        self.add(SpellData(
            "Projectile_ScorchingRay_Monk",
            using="Projectile_ScorchingRay_Monk",
            SpellType="Projectile",
        ))
        
        self.add(SpellData(
            "Target_Shatter_Monk",
            using="Target_Shatter_Monk",
            SpellType="Target",
        ))
        
        self.add(SpellData(
            "Projectile_BladeOfTheRime",
            using="Projectile_BladeOfTheRime",
            SpellType="Projectile",
        ))
        
        self.add(SpellData(
            "Zone_Thunderwave_Monk",
            using="Zone_Thunderwave_Monk",
            SpellType="Zone",
        ))
        
        self.add(SpellData(
            "Target_FistOfUnbrokenAir",
            using="Target_FistOfUnbrokenAir",
            SpellType="Target",
        ))
        
        self.add(SpellData(
            "Zone_GustOfWind_Monk",
            using="Zone_GustOfWind_Monk",
            SpellType="Zone",
        ))
        
        self.add(SpellData(
            "Target_ShapeTheFlowingRiver_IceBlock",
            using="Target_ShapeTheFlowingRiver_IceBlock",
            SpellType="Target",
            RitualCosts=["ActionPoint:1"],
        ))
        
        self.add(SpellData(
            "Projectile_ChromaticOrb_Monk",
            using="Projectile_ChromaticOrb_Monk",
            SpellType="Projectile",
        ))

        for element in ["Acid", "Cold", "Fire", "Lightning", "Poison", "Thunder"]:
            self.add(SpellData(
                f"Projectile_ChromaticOrb_{element}_Monk",
                using=f"Projectile_ChromaticOrb_{element}_Monk",
                SpellType="Projectile",
            ))

        self.add(SpellData(
            "Zone_BurningHands_Monk",
            using="Zone_BurningHands_Monk",
            SpellType="Zone",
        ))
        
        self.add(SpellData(
            "Target_WaterWhip",
            using="Target_WaterWhip",
            SpellType="Target",
        ))

    @progression(CharacterClass.MONK_FOURELEMENTS, 3)
    def fourelements_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._awareness]
        progress.PassivesRemoved = ["MartialArts_BonusUnarmedStrike", "FlurryOfBlowsUnlock"]
        progress.Selectors = [
            f"AddSpells({self._level_3_spell_list})",
            "SelectSpells(9da8ef4f-676b-46f1-81e4-f7c3cfd1c34c,4,0,FourElements,,,AlwaysPrepared)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 4)
    def fourelements_level_4(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._unarmed_acuity]

    @progression(CharacterClass.MONK_FOURELEMENTS, 5)
    def fourelements_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["UncannyDodge"]

    @progression(CharacterClass.MONK_FOURELEMENTS, 6)
    def fourelements_level_6(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,3,0,FourElements,,,AlwaysPrepared)",
            "SelectSpells(9da8ef4f-676b-46f1-81e4-f7c3cfd1c34c,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 7)
    def fourelements_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = ["FastHands"]

    @progression(CharacterClass.MONK_FOURELEMENTS, 8)
    def fourelements_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 9)
    def fourelements_level_9(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,2,0,FourElements,,,AlwaysPrepared)",
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 10)
    def fourelements_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 11)
    def fourelements_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2", "ReliableTalent"]
        progress.PassivesRemoved = ["ExtraAttack"]
        progress.Selectors = [
            "SelectSpells(cf014f77-4d0a-4322-a2bf-95e38b89435b,2,0,FourElements,,,AlwaysPrepared)",
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 12)
    def fourelements_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 13)
    def fourelements_level_13(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 14)
    def fourelements_level_14(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSpells(cf014f77-4d0a-4322-a2bf-95e38b89435b,1,0,FourElements,,,AlwaysPrepared)",
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 15)
    def fourelements_level_15(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 16)
    def fourelements_level_16(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 17)
    def fourelements_level_17(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSpells(cf014f77-4d0a-4322-a2bf-95e38b89435b,1,0,FourElements,,,AlwaysPrepared)",
            "SelectSpells(cf014f77-4d0a-4322-a2bf-95e38b89435b,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 18)
    def fourelements_level_18(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 19)
    def fourelements_level_19(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSpells(c841dfad-9d3b-486d-ad6b-ac3eaebc2db4,0,1,FourElements,,,AlwaysPrepared)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 20)
    def fourelements_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]
        progress.Selectors = [
            "SelectSpells(cf014f77-4d0a-4322-a2bf-95e38b89435b,1,0,FourElements,,,AlwaysPrepared)",
        ]


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
