
from functools import cached_property
import os

from moddb import (
    Attack,
    Bolster,
    CunningActions,
    PackMule,
)
from modtools.gamedata import PassiveData, StatusData
from modtools.lsx.game import Progression, SpellList
from modtools.replacers import (
    CharacterClass,
    DontIncludeProgression,
    progression,
    Replacer,
)


class GiantPath(Replacer):
    # Passives
    _dash_bonus_action: str
    _running_jump: str

    # Spells
    _bolster: str
    _brutal_cleave: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="GiantPath",
                         description="A class replacer for GiantPath.",
                         **kwds)
        
        self._dash_bonus_action = CunningActions(self.mod).add_dash_bonus_action()
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)
        self._running_jump = CunningActions(self.mod).add_running_jump()

        self._bolster = Bolster(self.mod).add_bolster()
        self._brutal_cleave = Attack(self.mod).add_brutal_cleave()

        self._rage_giant()

    @cached_property
    def _rage_giant_extra_resistances(self) -> str:
        name = f"{self.mod.get_prefix()}_RageGiantExtraResistances"
        self.mod.add(PassiveData(
            name,
            Properties=["IsHidden"],
            BoostContext=["OnEquip", "OnCreate"],
            BoostConditions=["not HasHeavyArmor(context.Source)"],
            Boosts=[
                "Resistance(Acid,Resistant)",
                "Resistance(Cold,Resistant)",
                "Resistance(Fire,Resistant)",
                "Resistance(Force,Resistant)",
                "Resistance(Lightning,Resistant)",
                "Resistance(Necrotic,Resistant)",
                "Resistance(Poison,Resistant)",
                "Resistance(Psychic,Resistant)",
                "Resistance(Radiant,Resistant)",
                "Resistance(Thunder,Resistant)",
            ],
        ))
        return name

    def _rage_giant(self) -> None:
        self.mod.add(StatusData(
            "RAGE_GIANT",
            StatusType="BOOST",
            using="RAGE_GIANT",
            Passives=[
                "Rage_Rage_Boosts",
                "Rage_Attack",
                "Rage_Damaged",
                "Rage_NoHeavyArmour_VFX",
                "EnlargeWeightMedium",
                "EnlargeWeightLarge",
                self._rage_giant_extra_resistances,
            ],
        ))

    @cached_property
    def _level_3_spells(self) -> SpellList:
        spells = SpellList(
            Name="Barbarian level 3 spells",
            Spells=[
                "Shout_ActionSurge",
                self._bolster,
                self._brutal_cleave,
                self._dash_bonus_action,
            ],
            UUID=self.make_uuid("level_3_spells"),
        )
        self.mod.add(spells)
        return spells

    @progression(CharacterClass.BARBARIAN_GIANT, 1)
    def giantpath_level_1(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 2)
    def giantpath_level_2(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 3)
    def giantpath_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + [
            "FastHands",
            "ImprovedCritical",
            "JackOfAllTrades",
            self._running_jump,
        ]
        progress.Selectors = (progress.Selectors or []) + [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
            f"AddSpells({self._level_3_spells.UUID})",
        ]

    @progression(CharacterClass.BARBARIAN_GIANT, 4)
    def giantpath_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 5)
    def giantpath_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["UncannyDodge"]

    @progression(CharacterClass.BARBARIAN_GIANT, 6)
    def giantpath_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 7)
    def giantpath_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["Evasion"]

    @progression(CharacterClass.BARBARIAN_GIANT, 8)
    def giantpath_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 9)
    def giantpath_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 10)
    def giantpath_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 11)
    def giantpath_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_2", "ReliableTalent"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack"]

    @progression(CharacterClass.BARBARIAN_GIANT, 12)
    def giantpath_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 13)
    def giantpath_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 14)
    def giantpath_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 15)
    def giantpath_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 16)
    def giantpath_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 17)
    def giantpath_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 18)
    def giantpath_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 19)
    def giantpath_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.BARBARIAN_GIANT, 20)
    def giantpath_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = (progress.PassivesAdded or []) + ["ExtraAttack_3"]
        progress.PassivesRemoved = (progress.PassivesRemoved or []) + ["ExtraAttack_2"]


def main() -> None:
    giant_path = GiantPath(
        classes=[CharacterClass.BARBARIAN_GIANT],
        feats=2,
        actions=4,
    )
    giant_path.build()


if __name__ == "__main__":
    main()
