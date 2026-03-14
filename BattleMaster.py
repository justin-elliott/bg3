#!/usr/bin/env python3

import os

from modtools.gamedata import InterruptData, PassiveData, SpellData
from modtools.lsx.game import Progression
from modtools.replacers import (
    CharacterClass,
    progression,
    Replacer,
)


class BattleMaster(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="BattleMaster",
                         description="A class replacer for BattleMaster.",
                         **kwds)
        
        self._update_precision_attack()
        self._update_sweeping_attack()

    def _update_precision_attack(self) -> None:
        passive_name = "PrecisionAttack"
        interrupt_name = self.make_name("Interrupt_PrecisionAttack")

        self.loca[f"{passive_name}_DisplayName"] = "Precision Attack"
        self.loca[f"{passive_name}_Description"] = """
            On a miss, you can spend a <LSTag Type="ActionResource" Tooltip="SuperiorityDie">Superiority Die</LSTag> to
            add it to the result of the <LSTag Tooltip="AttackRoll">Attack Roll</LSTag>, possibly making it hit.
        """
        self.add(PassiveData(
            passive_name,
            DisplayName=self.loca[f"{passive_name}_DisplayName"],
            Description=self.loca[f"{passive_name}_Description"],
            Icon="Action_PrecisionAttack",
            Boosts=[f"UnlockInterrupt({interrupt_name})"],
        ))

        self.loca[f"{interrupt_name}_Description"] = """
            Add a <LSTag Type="ActionResource" Tooltip="SuperiorityDie">Superiority Die</LSTag> to
            your <LSTag Tooltip="AttackRoll">Attack Roll</LSTag>.
        """
        self.add(InterruptData(
            interrupt_name,
            DisplayName=self.loca[f"{passive_name}_DisplayName"],
            Description=self.loca[f"{interrupt_name}_Description"],
            Icon="Action_PrecisionAttack",
            InterruptContext="OnPostRoll",
            InterruptContextScope="Self",
            Container="YesNoDecision",
            Conditions=[
                "Self(context.Source,context.Observer)"
                + " and not Dead(context.Observer)"
                + " and HasInterruptedAttack()"
                + " and not AnyEntityIsItem()"
                + " and ((not CharacterLevelGreaterThan(9) and IsFlatValueInterruptInteresting(8,context.Source))"
                +       " or (CharacterLevelGreaterThan(9) and IsFlatValueInterruptInteresting(10,context.Source)))",
            ],
            Properties=["AdjustRoll(OBSERVER_OBSERVER,LevelMapValue(SuperiorityDie))"],
            Cost="SuperiorityDie:1",
            InterruptDefaultValue=["Ask", "Enabled"],
            EnableCondition=[
                "not HasStatus('SG_Polymorph')"
                + " or HasAnyStatus({"
                +       "'SG_Disguise',"
                +       "'WILDSHAPE_STARRY_ARCHER_PLAYER',"
                +       "'WILDSHAPE_STARRY_CHALICE_PLAYER',"
                +       "'WILDSHAPE_STARRY_DRAGON_PLAYER'"
                +       "})",
            ],
            EnableContext=["OnStatusApplied", "OnStatusRemoved"],
        ))

    def _update_sweeping_attack(self) -> None:
        passive_name = "SweepingAttack"
        spell_name = "Zone_SweepingAttack"

        self.loca[f"{passive_name}_Description"] = """
            Swing your weapon in a rapid, sweeping arc to attack multiple enemies at once, dealing an additional [1].
        """
        self.add(PassiveData(
            passive_name,
            using=passive_name,
            Description=self.loca[f"{passive_name}_Description"],
            DescriptionParams=["LevelMapValue(SuperiorityDie)"],
        ))

        self.add(SpellData(
            spell_name,
            using=spell_name,
            SpellType="Zone",
            SpellProperties=[
                "GROUND:DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "GROUND:ExecuteWeaponFunctors(MainHand)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
            ],
            SpellSuccess=[
                "DealDamage(MainMeleeWeapon+LevelMapValue(SuperiorityDie),MainMeleeWeaponDamageType)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TooltipDamageList=["DealDamage(MainMeleeWeapon+LevelMapValue(SuperiorityDie),MainMeleeWeaponDamageType)"],
        ))

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 3)
    def battlemaster_level_3(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,3,0)"]
        progress.PassivesAdded = ["ImprovedCritical"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 4)
    def battlemaster_level_4(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 5)
    def battlemaster_level_5(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 6)
    def battlemaster_level_6(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 7)
    def battlemaster_level_7(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]
        progress.PassivesAdded = ["RemarkableAthlete_Proficiency", "RemarkableAthlete_Jump"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 8)
    def battlemaster_level_8(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 9)
    def battlemaster_level_9(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 10)
    def battlemaster_level_10(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]
        progress.Selectors += ["SelectPassives(da3203d8-750a-4de1-b8eb-1eccfccddf46,1,FightingStyle)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 11)
    def battlemaster_level_11(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]

    @progression(CharacterClass.FIGHTER_BATTLEMASTER, 12)
    def battlemaster_level_12(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(SuperiorityDie,1,0)"]


def main() -> None:
    battle_master = BattleMaster(
        classes=[CharacterClass.FIGHTER_BATTLEMASTER],
        actions=2,
    )
    battle_master.build()


if __name__ == "__main__":
    main()
