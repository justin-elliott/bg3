
import os

from functools import cached_property
from moddb import character_level_range, CunningActions, Movement
from modtools.gamedata import Armor, PassiveData, SpellData, Weapon
from modtools.lsx.game import ClassDescription, Dependencies, Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    class_description,
    DontIncludeProgression,
    progression,
    Replacer,
)


class Spartan(Replacer):
    # Passives
    _bonus_action_dash: str
    _remarkable_athlete_run: str
    _running_jump: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Spartan",
                         description="A class replacer for GiantPath.",
                         **kwds)

        self._mod.add(Dependencies.ShortModuleDesc(
            Folder="SPRtnarmr_dc350aa5-ddc0-5d9a-07a9-65e77a7ac82f",
            MD5="33c5be4ed131380bbf5d0213c73b9323",
            Name="Spartan Warrior Set",
            PublishHandle=5219033,
            UUID="dc350aa5-ddc0-5d9a-07a9-65e77a7ac82f",
            Version64=36028797018963972,
        ))

        loca = self._mod.get_localization()
        run_display_name = f"{self.mod.get_prefix()}_RemarkableAthleteRun_DisplayName"
        loca[run_display_name] = {"en": "Remarkable Athlete: Run"}
        self._remarkable_athlete_run = Movement(self.mod).add_fast_movement(3.0, display_name=loca[run_display_name])

        self._bonus_action_dash = CunningActions(self.mod).add_dash_bonus_action()
        self._running_jump = CunningActions(self.mod).add_running_jump()

        self.mod.add(character_level_range)
        self._armor_body()
        self._shield()
        self._shield_bash()
        self._shortsword()
        self._spartan_kick()
        self._spear()
        self._spear_instrument()
        self._tavern_brawler()

    def _weapon_boosts(self, damage_type: str, die_sides: int) -> list[str]:
        return [
            "WeaponProperty(Magical)",
            "CannotBeDisarmed()",
            "ItemReturnToOwner()",
            "IF(CharacterLevelRange(1,4)):WeaponEnchantment(1)",
            "IF(CharacterLevelRange(5,8)):WeaponEnchantment(2)",
            "IF(CharacterLevelRange(9,20)):WeaponEnchantment(3)",
            f"IF(CharacterLevelRange(5,8)):WeaponDamage(1d{die_sides},{damage_type},Magical)",
            f"IF(CharacterLevelRange(9,12)):WeaponDamage(2d{die_sides},{damage_type},Magical)",
            f"IF(CharacterLevelRange(13,16)):WeaponDamage(3d{die_sides},{damage_type},Magical)",
            f"IF(CharacterLevelRange(17,20)):WeaponDamage(4d{die_sides},{damage_type},Magical)",
        ]

    def _armor_body(self) -> None:
        self.mod.add(Armor(
            "ARM_SPR_Body",
            using="ARM_SPR_Body",
            PassivesOnEquip=[
                "SPR_Unarmored",
                "MAG_Bhaalist_Aura_Of_Murder_Passive",
                "ARM_Ambusher_2_Passive",
                "MAG_Bhaalist_Aura_Of_Murder_DeadRevival_Passive",
            ],
            StatusOnEquip=["MAG_BHAALIST_ARMOR_TECHNICAL"],
        ))

    def _shield(self) -> None:
        self.mod.add(Weapon(
            "WPN_SPR_Shield",
            using="WPN_SPR_Shield",
            DefaultBoosts=self._weapon_boosts("Bludgeoning", 4),
        ))
    
    def _shield_bash(self) -> None:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_ShieldBash_Description"] = {"en": """
            Perform an offhand attack with your shield.
            """}

        self.mod.add(SpellData(
            "Target_SPR_Shield_Bash",
            using="Target_Bash",
            SpellType="Target",
            Description=loca[f"{self.mod.get_prefix()}_ShieldBash_Description"],
            TooltipDamageList=["DealDamage(OffhandMeleeWeapon,OffhandMeleeWeaponDamageType)"],
            TooltipAttackSave=["MeleeWeaponAttack"],
            TooltipStatusApply=[],
            SpellRoll=["Attack(AttackType.MeleeOffHandWeaponAttack)"],
            SpellSuccess=[
                "DealDamage(max(1,OffhandMeleeWeapon),OffhandMeleeWeaponDamageType)",
                "ExecuteWeaponFunctors(OffHand)",
            ],
            SpellFail=["ApplyStatus(SAVED_AGAINST_HOSTILE_SPELL,100,0)"],
            TargetConditions=["not Self() and not Dead()"],
        ))
    
    def _shortsword(self) -> None:
        self.mod.add(Weapon(
            "WPN_SPR_Shortsword",
            using="WPN_SPR_Shortsword",
            DefaultBoosts=self._weapon_boosts("Piercing", 4),
            PassivesOnEquip=[],
        ))

    def _spartan_kick(self) -> None:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_SpartanKick_DisplayName"] = {"en": "Spartan Kick"}

        self.mod.add(SpellData(
            "Target_BootOfTheGiants",
            using="Target_BootOfTheGiants",
            SpellType="Target",
            DisplayName=loca[f"{self.mod.get_prefix()}_SpartanKick_DisplayName"],
        ))
    
    def _spear(self) -> None:
        self.mod.add(Weapon(
            "WPN_SPR_Spear",
            using="WPN_SPR_Spear",
            DefaultBoosts=self._weapon_boosts("Piercing", 4),
        ))

    def _spear_instrument(self) -> None:
        self.mod.add(Armor(
            "INS_SPR_Spear",
            using="INS_SPR_Spear",
            Boosts=[
                "UnlockSpell(Projectile_SPR_RangedAttack)",
                "UnlockSpell(Shout_Bard_Perform_Whistle)",
            ],
        ))

    def _tavern_brawler(self) -> None:
        self.mod.add(PassiveData(
            "TavernBrawler",
            using="TavernBrawler",
            Conditions=[(
                "(IsRangedUnarmedAttack() or SpellId('Throw_ImprovisedWeapon') or " +
                "SpellId('Throw_ImprovisedWeaponBerserker') or SpellId('Projectile_SPR_RangedAttack')) " +
                "and HasDamageEffectFlag(DamageFlags.Hit)"
            )],
        ))

    @cached_property
    def _bonus_action_dash_spell_list(self) -> str:
        name = "Bonus Action Dash"
        spells = SpellList(
            Name=name,
            Spells=[self._bonus_action_dash],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return spells.UUID

    @class_description(CharacterClass.BARBARIAN_GIANT)
    def spartan_class_description(self, desc: ClassDescription) -> None:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_DisplayName"] = {"en": "Spartan"}
        loca[f"{self.mod.get_prefix()}_Description"] = {"en": """
            Your body is a chiseled monument to discipline, every scar a testament to your unbreakable will. You are
            ready to embrace glory or death without a whisper of fear.
            """}
        desc.DisplayName = loca[f"{self.mod.get_prefix()}_DisplayName"]
        desc.Description = loca[f"{self.mod.get_prefix()}_Description"]

    @progression(CharacterClass.BARBARIAN_GIANT, 3)
    def spartan_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded += ["ImprovedCritical", "JackOfAllTrades", self._remarkable_athlete_run]
        progress.Selectors += [
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.BARBARIAN_GIANT, 4)
    def spartan_level_4(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._running_jump]
        progress.Selectors = [
            f"AddSpells({self._bonus_action_dash_spell_list})",
        ]

    @progression(CharacterClass.BARBARIAN_GIANT, 5)
    def spartan_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["UncannyDodge"]

    @progression(CharacterClass.BARBARIAN_GIANT, 6)
    def spartan_level_6(self, progress: Progression) -> None:
        progress.Selectors = []

    @progression(CharacterClass.BARBARIAN_GIANT, 7)
    def spartan_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            "Evasion",
            "RemarkableAthlete_Proficiency",
            "RemarkableAthlete_Jump",
        ]

    @progression(CharacterClass.BARBARIAN_GIANT, 8)
    def spartan_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 9)
    def spartan_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 10)
    def spartan_level_10(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)",
        ]

    @progression(CharacterClass.BARBARIAN_GIANT, 11)
    def spartan_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2"]
        progress.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.BARBARIAN_GIANT, 12)
    def spartan_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 13)
    def spartan_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 14)
    def spartan_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 15)
    def spartan_level_15(self, progress: Progression) -> None:
        progress.PassivesAdded = ["SuperiorCritical"]

    @progression(CharacterClass.BARBARIAN_GIANT, 16)
    def spartan_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 17)
    def spartan_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 18)
    def spartan_level_18(self, progress: Progression) -> None:
        progress.PassivesAdded = ["Survivor"]

    @progression(CharacterClass.BARBARIAN_GIANT, 19)
    def spartan_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 20)
    def spartan_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]


def main() -> None:
    spartan = Spartan(
        classes=[CharacterClass.BARBARIAN_GIANT],
    )
    spartan.build()


if __name__ == "__main__":
    main()
