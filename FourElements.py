import os

from functools import cached_property
from modtools.gamedata import SpellData, StatusData
from modtools.lsx.game import Progression, SpellList
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

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="FourElements",
                         description="A class replacer for FourElements.",
                         **kwds)

    @cached_property
    def _level_3_spell_list(self) -> UUID:
        name = "Way of the Four Elements level 3 spells"
        uuid = self.make_uuid(name)
        self.mod.add(SpellList(
            Name=name,
            Spells=[
                self._chill_of_the_mountain_bonus_action,
                self._fangs_of_the_fire_snake_bonus_action,
                self._touch_of_the_storm_bonus_action,
            ],
            UUID=uuid,
        ))
        return uuid

    @cached_property
    def _chill_of_the_mountain_bonus_action(self) -> str:
        chill_of_the_mountain = "Projectile_RayOfFrost_Monk"
        chill_of_the_mountain_status = self.make_name("CHILL_OF_THE_MOUNTAIN")

        self.mod.loca[f"{chill_of_the_mountain}_Description"] = """
            Call forth the cold mountain winds and reduce the target's
            <LSTag Tooltip="MovementSpeed">movement speed</LSTag> by [1].
            Your next melee attacks deal an additional [2].
        """

        self.mod.add(SpellData(
            chill_of_the_mountain,
            using=chill_of_the_mountain,
            SpellType="Projectile",
            Description=self.mod.loca[f"{chill_of_the_mountain}_Description"],
            DescriptionParams=["Distance(3)", "DealDamage(LevelMapValue(D4Cantrip),Cold)"],
            SpellProperties=[
                "GROUND:SurfaceChange(Freeze)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
                f"ApplyStatus(SELF,{chill_of_the_mountain_status},100,1)",
            ],
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                "DealDamage(LevelMapValue(D10Cantrip),Cold,Magical)",
                "ApplyStatus(RAY_OF_FROST,100,1)",
            ],
            TargetRadius=9,
            TooltipDamageList=[
                "DealDamage(MartialArtsUnarmedDamage,Bludgeoning)",
                "DealDamage(LevelMapValue(D10Cantrip),Cold)",
            ],
            UseCosts=["BonusActionPoint:1"],
        ))

        self.mod.loca[f"{chill_of_the_mountain_status}_DisplayName"] = "Chill of the Mountain"
        self.mod.loca[f"{chill_of_the_mountain_status}_Description"] = """
            Affected entity's fists are glistening with frost. Its melee attacks deal an additional [1].
        """
        
        self.mod.add(StatusData(
            chill_of_the_mountain_status,
            using=self._fangs_of_the_fire_snake_status,
            StatusType="BOOST",
            Boosts=[
                "CharacterWeaponDamage(LevelMapValue(D4Cantrip),Cold)",
                "CharacterUnarmedDamage(LevelMapValue(D4Cantrip),Cold)",
            ],
            DisplayName=self.mod.loca[f"{chill_of_the_mountain_status}_DisplayName"],
            Description=self.mod.loca[f"{chill_of_the_mountain_status}_Description"],
            DescriptionParams=["DealDamage(LevelMapValue(D4Cantrip),Cold)"],
            Icon="Spell_Evocation_RayOfFrost",
        ))

        return chill_of_the_mountain

    @cached_property
    def _fangs_of_the_fire_snake_bonus_action(self) -> str:
        fangs_of_the_fire_snake = "Projectile_FangsOfTheFireSnake"

        self.mod.add(SpellData(
            fangs_of_the_fire_snake,
            using=fangs_of_the_fire_snake,
            SpellType="Projectile",
            DescriptionParams=["DealDamage(LevelMapValue(D4Cantrip),Fire)"],
            SpellProperties=[
                "GROUND:DealDamage(LevelMapValue(D10Cantrip),Fire)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
                f"ApplyStatus(SELF,{self._fangs_of_the_fire_snake_status},100,1)",
            ],
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                "DealDamage(LevelMapValue(D10Cantrip),Fire,Magical)",
            ],
            TargetRadius=9,
            TooltipDamageList=[
                "DealDamage(MartialArtsUnarmedDamage,Bludgeoning)",
                "DealDamage(LevelMapValue(D10Cantrip),Fire)",
            ],
            UseCosts=["BonusActionPoint:1"],
        ))

        self.mod.add(StatusData(
            self._fangs_of_the_fire_snake_status,
            using=self._fangs_of_the_fire_snake_status,
            StatusType="BOOST",
            Boosts=[
                "CharacterWeaponDamage(LevelMapValue(D4Cantrip),Fire)",
                "CharacterUnarmedDamage(LevelMapValue(D4Cantrip),Fire)",
            ],
            DescriptionParams=["DealDamage(LevelMapValue(D4Cantrip),Fire)"],
        ))

        return fangs_of_the_fire_snake

    @cached_property
    def _touch_of_the_storm_bonus_action(self) -> str:
        touch_of_the_storm = "Target_ShockingGrasp_Monk"
        touch_of_the_storm_status = self.make_name("TOUCH_OF_THE_STORM")

        self.mod.loca[f"{touch_of_the_storm}_Description"] = """
            The target cannot use reactions. This spell has <LSTag Tooltip="Advantage">Advantage</LSTag> on creatures
            with metal armour.
            Your next melee attacks deal an additional [1].
        """

        self.mod.add(SpellData(
            touch_of_the_storm,
            using=touch_of_the_storm,
            SpellType="Target",
            Description=self.mod.loca[f"{touch_of_the_storm}_Description"],
            DescriptionParams=["DealDamage(LevelMapValue(D4Cantrip),Lightning)"],
            SpellProperties=[
                "GROUND:SurfaceChange(Electrify)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
                f"ApplyStatus(SELF,{touch_of_the_storm_status},100,1)",
            ],
            SpellSuccess=[
                "DealDamage(UnarmedDamage,Bludgeoning)",
                "DealDamage(LevelMapValue(D10Cantrip),Lightning,Magical)",
                "ApplyStatus(SHOCKING_GRASP,100,1)",
            ],
            TargetRadius=9,
            TooltipDamageList=[
                "DealDamage(MartialArtsUnarmedDamage,Bludgeoning)",
                "DealDamage(LevelMapValue(D10Cantrip),Lightning)",
            ],
            UseCosts=["BonusActionPoint:1"],
        ))

        self.mod.loca[f"{touch_of_the_storm_status}_DisplayName"] = "Touch of the Storm"
        self.mod.loca[f"{touch_of_the_storm_status}_Description"] = """
            Affected entity's fists are sparking with lightning. Its melee attacks deal an additional [1].
        """
        
        self.mod.add(StatusData(
            touch_of_the_storm_status,
            using=self._fangs_of_the_fire_snake_status,
            StatusType="BOOST",
            Boosts=[
                "CharacterWeaponDamage(LevelMapValue(D4Cantrip),Lightning)",
                "CharacterUnarmedDamage(LevelMapValue(D4Cantrip),Lightning)",
            ],
            DisplayName=self.mod.loca[f"{touch_of_the_storm_status}_DisplayName"],
            Description=self.mod.loca[f"{touch_of_the_storm_status}_Description"],
            DescriptionParams=["DealDamage(LevelMapValue(D4Cantrip),Lightning)"],
            Icon="Spell_Evocation_ShockingGrasp",
        ))

        return touch_of_the_storm

    @progression(CharacterClass.MONK_FOURELEMENTS, 3)
    def fourelements_level_3(self, progress: Progression) -> None:
        progress.PassivesRemoved = ["MartialArts_BonusUnarmedStrike", "FlurryOfBlowsUnlock"]
        progress.Selectors += [
            f"AddSpells({self._level_3_spell_list})",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.MONK_FOURELEMENTS, 4)
    def fourelements_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 5)
    def fourelements_level_5(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 6)
    def fourelements_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 7)
    def fourelements_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = ["FastHands"]

    @progression(CharacterClass.MONK_FOURELEMENTS, 8)
    def fourelements_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 9)
    def fourelements_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 10)
    def fourelements_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 11)
    def fourelements_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2", "ReliableTalent"]
        progress.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.MONK_FOURELEMENTS, 12)
    def fourelements_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 13)
    def fourelements_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 14)
    def fourelements_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 15)
    def fourelements_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 16)
    def fourelements_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 17)
    def fourelements_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 18)
    def fourelements_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 19)
    def fourelements_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.MONK_FOURELEMENTS, 20)
    def fourelements_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]


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
