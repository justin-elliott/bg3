
import os

from functools import cached_property
from moddb import CunningActions
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class Wildheart(Replacer):
    # Passives
    _running_jump: str

    @cached_property
    def _bonus_action_dash(self) -> str:
        name = f"{self.mod.get_prefix()}_BonusActionDash"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Bonus Action: Dash"}

        self.mod.add(SpellData(
            name,
            using="Shout_Dash_BonusAction",
            SpellType="Shout",
            DisplayName=loca[f"{name}_DisplayName"],
            SpellFlags=["IgnoreSilence", "Stealth", "Invisible", "NoCameraMove"],
        ))
        return name

    @cached_property
    def _bash(self) -> str:
        name = f"{self.mod.get_prefix()}_Bash"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Bash"}
        loca[f"{name}_Description"] = {"en": """
            Bash your target, possibly <LSTag Type="Status" Tooltip="STUNNED">Stunning</LSTag> them.
            """}

        self.mod.add(SpellData(
            name,
            using="Target_ConcussiveSmash",
            SpellType="Target",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Cooldown="None",
            RequirementConditions=["HasStatus('SG_Rage')"],
            SpellSuccess=[
                "IF(not SavingThrow(Ability.Constitution,ManeuverSaveDC())):ApplyStatus(STUNNED,100,1)",
                "DealDamage(max(1,MainMeleeWeapon),Bludgeoning)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TargetConditions=[
                "not Self() and not Dead() and not (not Player(context.Source) and HasStatus('SG_Stunned'))",
            ],
            TooltipDamageList=["DealDamage(MainMeleeWeapon,Bludgeoning)"],
            TooltipStatusApply=["ApplyStatus(STUNNED,100,1)"],
        ))

        return name

    @cached_property
    def _brutal_cleave(self) -> str:
        name = f"{self.mod.get_prefix()}_BrutalCleave"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Brutal Cleave"}

        self.mod.add(SpellData(
            name,
            using="Zone_TigersBloodlust",
            SpellType="Zone",
            DisplayName=loca[f"{name}_DisplayName"],
            Icon="Action_Cleave_New",
        ))

        return name

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Wildheart",
                         description="A class replacer for Wildheart Barbarian.",
                         **kwds)

        self._running_jump = CunningActions(self.mod).add_running_jump()

        self.mod.add(PassiveData(
            "TotemSpirit_Bear",
            using="TotemSpirit_Bear",
            Boosts=[
                "UnlockSpell(Shout_Rage_Totem_Bear)",
                "UnlockSpell(Shout_FerociousAppetite)",
                f"UnlockSpell({self._bash})",
                f"UnlockSpell({self._brutal_cleave})",
                f"UnlockSpell({self._bonus_action_dash})",
            ],
        ))

    @progression(CharacterClass.BARBARIAN, 20)
    def barbarian_level_20(self, progress: Progression) -> None:
        progress.Boosts = ["ActionResource(Rage,87,0)"]  # Boost to 99

    @progression(CharacterClass.BARBARIAN_WILDHEART, 3)
    def totemwarriorpath_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            "FastHands",
            "ImprovedCritical",
            self._running_jump,
        ]
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.BARBARIAN_WILDHEART, 4)
    def totemwarriorpath_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_WILDHEART, 5)
    def totemwarriorpath_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["UncannyDodge"]

    @progression(CharacterClass.BARBARIAN_WILDHEART, 6)
    def totemwarriorpath_level_6(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.BARBARIAN_WILDHEART, 7)
    def totemwarriorpath_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = ["Evasion"]

    @progression(CharacterClass.BARBARIAN_WILDHEART, 8)
    def totemwarriorpath_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_WILDHEART, 9)
    def totemwarriorpath_level_9(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.BARBARIAN_WILDHEART, 10)
    def totemwarriorpath_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_WILDHEART, 11)
    def totemwarriorpath_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_2", "ReliableTalent"]
        progress.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.BARBARIAN_WILDHEART, 12)
    def totemwarriorpath_level_12(self, progress: Progression) -> None:
        progress.Selectors += [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.BARBARIAN_WILDHEART, 13)
    def totemwarriorpath_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_WILDHEART, 14)
    def totemwarriorpath_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_WILDHEART, 15)
    def totemwarriorpath_level_15(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.BARBARIAN_WILDHEART, 16)
    def totemwarriorpath_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_WILDHEART, 17)
    def totemwarriorpath_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_WILDHEART, 18)
    def totemwarriorpath_level_18(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,1)",
        ]

    @progression(CharacterClass.BARBARIAN_WILDHEART, 19)
    def totemwarriorpath_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_WILDHEART, 20)
    def totemwarriorpath_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]


def main() -> None:
    wildheart = Wildheart(
        classes=[CharacterClass.BARBARIAN_WILDHEART],
        feats=2,
        actions=2,
    )
    wildheart.build()


if __name__ == "__main__":
    main()
