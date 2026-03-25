#!/usr/bin/env python3

import os

from functools import cached_property
from moddb import Awareness, Movement
from modtools.gamedata import InterruptData, PassiveData, SpellData, StatusData
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class Assassin(Replacer):
    _movement: Movement

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Assassin",
                         description="A class replacer for Assassin.",
                         **kwds)

        self._movement = Movement(self.mod)

    @cached_property
    def _awareness(self) -> str:
        return Awareness(self.mod).add_awareness(icon="Action_Barbarian_MagicAwareness")

    @cached_property
    def _fast_movement_30(self) -> str:
        return self._movement.add_remarkable_athlete(display_name="Fast Movement",
                                                     passive_name="FastMovement_30",
                                                     movement_speed=3.0,
                                                     jump_distance=1.5)

    @cached_property
    def _fast_movement_45(self) -> str:
        return self._movement.add_remarkable_athlete(display_name="Fast Movement",
                                                     passive_name="FastMovement_45",
                                                     movement_speed=4.5,
                                                     jump_distance=3.0)

    @cached_property
    def _fast_movement_60(self) -> str:
        return self._movement.add_remarkable_athlete(display_name="Fast Movement",
                                                     passive_name="FastMovement_60",
                                                     movement_speed=6.0,
                                                     jump_distance=4.5)

    @cached_property
    def _sure_footed(self) -> str:
        return self._movement.add_wilderness_explorer(
            display_name="Sure-Footed",
            description="""
                You have become an expert at navigating hazards.
                <LSTag Type="Status" Tooltip="DIFFICULT_TERRAIN">Difficult Terrain</LSTag> no longer slows you down, and
                you can't slip on grease or ice.
            """)

    @cached_property
    def _disarming_attack(self) -> str:
        name = self.make_name("DisarmingAttack")
        self.add(SpellData(
            name,
            using="Target_DisarmingAttack",
            SpellType="Target",
            SpellSuccess=[
                "IF(not SavingThrow(Ability.Strength,ManeuverSaveDC())):ApplyStatus(DISARM,100,0)",
                "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TooltipDamageList=["DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)"],
            TooltipOnMiss="",
            HitCosts=[],
        ))
        return name

    @cached_property
    def _pommel_strike(self) -> str:
        name = self.make_name("PommelStrike")
        self.add(SpellData(
            name,
            using="Target_PommelStrike",
            SpellType="Target",
            Description=self.loca(f"{name}_Description", """
                Make an attack against an enemy and possibly <LSTag Type="Status" Tooltip="DAZED">Daze</LSTag> them.
            """),
            Cooldown="",
            SpellSuccess=[
                "IF(Character() and not SavingThrow(Ability.Constitution,ManeuverSaveDC())):ApplyStatus(DAZED,100,2)",
                "DealDamage(ImprovisedWeapon+max(DexterityModifier,StrengthModifier),Bludgeoning)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TargetConditions=["(Character() or Item()) and not Self() and not Dead()"],
            TooltipDamageList=["DealDamage(1d4+max(DexterityModifier,StrengthModifier),Bludgeoning)"],
            UseCosts=["ActionPoint:1"],
        ))
        return name

    @cached_property
    def _riposte_attack(self) -> str:
        name = self.make_name("RiposteAttack")
        self.add(SpellData(
            name,
            using="Target_Riposte",
            SpellType="Target",
            SpellSuccess=[
                "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TooltipDamageList=["DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)"],
        ))
        return name

    @cached_property
    def _sweeping_attack(self) -> str:
        name = self.make_name("SweepingAttack")
        self.add(SpellData(
            name,
            using="Zone_SweepingAttack",
            SpellType="Zone",
            Range=3,
            SpellProperties=[
                "GROUND:DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "GROUND:ExecuteWeaponFunctors(MainHand)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
            ],
            SpellSuccess=[
                "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TooltipDamageList=["DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)"],
            UseCosts=["ActionPoint:1"],
        ))
        return name

    @cached_property
    def _trip_attack(self) -> str:
        name = self.make_name("TripAttack")
        self.add(SpellData(
            name,
            using="Target_TripAttack",
            SpellType="Target",
            SpellSuccess=[
                "IF(not SavingThrow(Ability.Strength,ManeuverSaveDC())):ApplyStatus(PRONE,100,1)",
                "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TooltipDamageList=["DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)"],
            TooltipOnMiss="",
            HitCosts=[],
        ))
        return name

    @cached_property
    def _riposte_interrupt(self) -> str:
        name = self.make_name("RiposteInterrupt")
        self.add(InterruptData(
            name,
            using="Interrupt_Riposte",
            Description=self.loca(f"{name}_Description", """
                When a creature misses you with a melee attack, you can retaliate with your own strike if you are
                wielding a melee weapon.
            """),
            Properties=[
                f"UseSpell(SWAP,{self._riposte_attack},true,true,true)",
                "ApplyStatus(OBSERVER_OBSERVER,INTERRUPT_RIPOSTE,100,0)",
            ],
            Cost=["ReactionActionPoint:1"],
        ))
        return name

    @cached_property
    def _riposte_unlock(self) -> str:
        name = self.make_name("RiposteUnlock")
        self.add(PassiveData(
            name,
            Boosts=[f"UnlockInterrupt({self._riposte_interrupt})"],
            Properties=["IsHidden"],
        ))
        return name

    @cached_property
    def _sneak_attack_interrupt(self) -> str:
        name = self.make_name("SneakAttackInterrupt")
        self.add(InterruptData(
            name,
            using="Interrupt_SneakAttack_Rakish",
            DisplayName=self.loca(f"{name}_DisplayName", "Sneak Attack"),
            Icon="Action_SneakAttack_Melee",
        ))
        return name

    @cached_property
    def _sneak_attack_interrupt_critical(self) -> str:
        name = self.make_name("SneakAttackInterruptCritical")
        self.add(InterruptData(
            name,
            using="Interrupt_SneakAttack_Rakish_Critical",
            DisplayName=self.loca(f"{name}_DisplayName", "Sneak Attack (Critical Hit)"),
            Icon="Action_SneakAttack_Melee",
        ))
        return name

    @cached_property
    def _sneak_attack_melee(self) -> str:
        name = self.make_name("SneakAttackMelee")
        self.add(SpellData(
            name,
            using="Target_SneakAttack_Rakish",
            SpellType="Target",
            DisplayName=self.loca(f"{name}_DisplayName", "Sneak Attack (Melee)"),
            Icon="Action_SneakAttack_Melee",
        ))
        return name

    @cached_property
    def _sneak_attack_ranged(self) -> str:
        name = self.make_name("SneakAttackRanged")
        self.add(SpellData(
            name,
            using="Projectile_SneakAttack_Rakish",
            SpellType="Projectile",
            DisplayName=self.loca(f"{name}_DisplayName", "Sneak Attack (Ranged)"),
            Icon="Action_SneakAttack_Ranged",
        ))
        return name

    @cached_property
    def _sneak_attack_unlock(self) -> str:
        name = self.make_name("SneakAttackUnlock")
        self.add(PassiveData(
            name,
            DisplayName=self.loca(f"{name}_DisplayName", "Sneak Attack Unlock"),
            Properties=["IsHidden"],
            Boosts=[
                f"UnlockInterrupt({self._sneak_attack_interrupt})",
                f"UnlockInterrupt({self._sneak_attack_interrupt_critical})",
                f"UnlockSpell({self._sneak_attack_melee})",
                f"UnlockSpell({self._sneak_attack_ranged})",
            ],
        ))
        return name

    @cached_property
    def _maneuvers(self) -> str:
        name = "Assassin Maneuvers"
        uuid = self.make_uuid(name)
        self.add(SpellList(
            Name=name,
            Spells=[
                self._disarming_attack,
                self._pommel_strike,
                self._trip_attack,
                self._sweeping_attack,
            ],
            UUID=uuid,
        ))
        return uuid

    @progression(CharacterClass.ROGUE_ASSASSIN, 3)
    def assassin_level_3(self, progress: Progression) -> None:
        progress.Boosts = ["Advantage(Ability,Dexterity)"]
        progress.PassivesAdded += [
            self._awareness,
            "LOW_HouseOfGrief_Cultists_Sight",
            self._fast_movement_30,
            self._riposte_unlock,
            self._sneak_attack_unlock,
        ]
        progress.PassivesRemoved = ["SneakAttack_Unlock"]
        progress.Selectors = [f"AddSpells({self._maneuvers})"]

    @progression(CharacterClass.ROGUE_ASSASSIN, 4)
    def assassin_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_ASSASSIN, 5)
    def assassin_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack"]

    @progression(CharacterClass.ROGUE_ASSASSIN, 6)
    def assassin_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_ASSASSIN, 7)
    def assassin_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_ASSASSIN, 8)
    def assassin_level_8(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_45, self._sure_footed]
        progress.PassivesRemoved = [self._fast_movement_30]

    @progression(CharacterClass.ROGUE_ASSASSIN, 9)
    def assassin_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_ASSASSIN, 10)
    def assassin_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.ROGUE_ASSASSIN, 11)
    def assassin_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2"]
        progress.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.ROGUE_ASSASSIN, 12)
    def assassin_level_12(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_60]
        progress.PassivesRemoved = [self._fast_movement_45]


def main() -> None:
    assassin = Assassin(classes=[CharacterClass.ROGUE_ASSASSIN])
    assassin.build()


if __name__ == "__main__":
    main()
