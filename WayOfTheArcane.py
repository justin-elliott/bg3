
import os

from functools import cached_property
from moddb import (
    BattleMagic,
    Bolster,
    Defense,
    EmpoweredSpells,
    PackMule,
    spells_always_prepared,
)
from modtools.gamedata import PassiveData, SpellData
from modtools.lsx.game import (
    CharacterAbility,
    ClassDescription,
    Progression,
    SpellList,
)
from modtools.replacers import (
    CharacterClass,
    class_description,
    progression,
    Replacer,
)
from uuid import UUID


class WayOfTheArcane(Replacer):
    _WIZARD_CANTRIP_SPELL_LIST = UUID("3cae2e56-9871-4cef-bba6-96845ea765fa")
    _WIZARD_LEVEL_1_SPELL_LIST = UUID("11f331b0-e8b7-473b-9d1f-19e8e4178d7d")
    _WIZARD_LEVEL_2_SPELL_LIST = UUID("80c6b070-c3a6-4864-84ca-e78626784eb4")
    _WIZARD_LEVEL_3_SPELL_LIST = UUID("22755771-ca11-49f4-b772-13d8b8fecd93")
    _WIZARD_LEVEL_4_SPELL_LIST = UUID("820b1220-0385-426d-ae15-458dc8a6f5c0")
    _WIZARD_LEVEL_5_SPELL_LIST = UUID("f781a25e-d288-43b4-bf5d-3d8d98846687")
    _WIZARD_LEVEL_6_SPELL_LIST = UUID("bc917f22-7f71-4a25-9a77-7d2f91a96a65")

    _ACTION_SURGE_SPELL_LIST = UUID("964e765d-5881-463e-b1b0-4fc6b8035aa8")


    # Passives
    _battle_magic: str
    _empowered_spells: str
    _pack_mule: str
    _warding: str

    # Spells
    _bolster_spell_list: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="WayOfTheArcane",
                         description="A class replacer for Shadow.",
                         **kwds)

        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._empowered_spells = EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.WISDOM)
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)
        self._warding = Defense(self.mod).add_warding()

        self._bolster_spell_list = Bolster(self.mod).add_bolster_spell_list()

    @cached_property
    def _arcane_manifestation(self) -> str:
        """Add the Arcane Manifestation passive, returning its name."""
        name = f"{self.mod.get_prefix()}_ArcaneManifestation"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Arcane Manifestation"}
        loca[f"{name}_Description"] = {"en": """
            Arcane energy infuses your strikes. Your melee unarmed attacks deal an additional [1].

            Whenever you deal damage with a melee unarmed attack, you gain
            <LSTag Type="Status" Tooltip="MAG_GISH_ARCANE_ACUITY">Arcane Acuity</LSTag> for 2 turns.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["DealDamage(1d4+WisdomModifier,Force)"],
            Icon="Action_Barbarian_MagicAwareness",
            Properties="Highlighted",
            Boosts=[
                "IF(IsMeleeUnarmedAttack()):CharacterUnarmedDamage(1d4+WisdomModifier,Force)",
                "UnlockSpellVariant(MeleeUnarmedAttackCheck(),ModifyTargetRadius(Multiplicative,1))",
            ],
            StatsFunctorContext="OnDamage",
            Conditions="IsMeleeUnarmedAttack()",
            StatsFunctors=[
                "ApplyStatus(SELF,MAG_GISH_ARCANE_ACUITY,100,2)",
                "ApplyStatus(SELF,MAG_GISH_ARCANE_ACUITY_DURATION_TECHNICAL,100,1)",
            ],
        ))

        return name

    @cached_property
    def _awareness(self) -> str:
        """The Awareness passive, a variant of Alert."""
        name = f"{self.mod.get_prefix()}_Awareness"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Awareness"}
        loca[f"{name}_Description"] = {"en": """
            You have honed your senses to the utmost degree. You gain a +[1] bonus to Initiative, can't be
            <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>, and attackers can't land
            <LSTag Tooltip="CriticalHit">Critical Hits</LSTag> against you.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["5"],
            Icon="Action_Barbarian_MagicAwareness",
            Properties=["ForceShowInCC", "Highlighted"],
            Boosts=[
                "Initiative(5)",
                "StatusImmunity(SURPRISED)",
                "CriticalHit(AttackTarget,Success,Never)",
            ],
        ))

        return name

    @cached_property
    def _bonus_unarmed_strike(self) -> str:
        """Replaces the bonus unarmed strike class feature."""
        name = f"{self.mod.get_prefix()}_BonusUnarmedStrike"

        self.mod.add(SpellData(
            name,
            using="Target_UnarmedStrike_Monk",
            SpellType="Target",
            SpellFlags=["IsMelee", "IsHarmful", "DisableBlood"],
        ))

        return name

    @cached_property
    def _flurry_of_blows_spell_list(self) -> str:
        spell_list = str(self.make_uuid("flurry_of_blows_spell_list"))
        self.mod.add(SpellList(
            Name="Way of the Arcane Flurry of Blows",
            Spells=[
                self._bonus_unarmed_strike,
                "Target_OpenHandTechnique_Knock",
                "Target_OpenHandTechnique_NoReactions",
                "Target_OpenHandTechnique_Push",
            ],
            UUID=spell_list,
        ))
        return spell_list

    @cached_property
    def _slow_fall(self) -> str:
        """The Slow Fall class feature as a passive."""
        name = f"{self.mod.get_prefix()}_SlowFall"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Slow Fall"}
        loca[f"{name}_Description"] = {"en": """
            You only take half damage from falling.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_SlowFall",
            Properties=["Highlighted"],
            Boosts=["FallDamageMultiplier(0.5)"],
        ))

        return name

    @cached_property
    def _stillness_of_mind(self) -> str:
        """The Stillness of Mind class feature as a passive."""
        name = f"{self.mod.get_prefix()}_StillnessOfMind"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Stillness of Mind"}
        loca[f"{name}_Description"] = {"en": """
            You are immune to being <LSTag Tooltip="CharmedGroup">Charmed</LSTag> or
            <LSTag Type="Status" Tooltip="FRIGHTENED">Frightened</LSTag>.
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_StillnessOfMind",
            Properties=["ForceShowInCC", "Highlighted"],
            Boosts=["StatusImmunity(SG_Charmed)", "StatusImmunity(SG_Frightened)"],
        ))

        return name

    @cached_property
    def _wholeness_of_body(self) -> str:
        """The Wholeness of Body subclass feature as a passive."""
        name = f"{self.mod.get_prefix()}_WholenessOfBody"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Wholeness of Body"}
        loca[f"{name}_Description"] = {"en": """
            While in combat, you heal [1] every turn, and restore [2]
            <LSTag Type="ActionResource" Tooltip="KiPoint">Ki Point(s)</LSTag>.
            """}
    
        HEALTH_PER_TURN = "1d4"
        KI_PER_TURN = 1

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=[
                f"RegainHitPoints({HEALTH_PER_TURN})",
                str(KI_PER_TURN),
            ],
            Icon="Action_Monk_WholenessOfBody",
            Properties=["ForceShowInCC", "Highlighted", "OncePerTurn"],
            StatsFunctorContext=["OnTurn"],
            Conditions=["not HasStatus('DOWNED') and not Dead() and Combat()"],
            StatsFunctors=[
                f"RegainHitPoints({HEALTH_PER_TURN})",
                f"RestoreResource(KiPoint,{KI_PER_TURN},0)",
            ],
        ))

        return name

    @class_description(CharacterClass.MONK)
    def monk_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6

        class_description.MulticlassSpellcasterModifier = 1.0
        class_description.MustPrepareSpells = True

        class_description.children.append(ClassDescription.Tags(
            Object="6fe3ae27-dc6c-4fc9-9245-710c790c396c"  # WIZARD
        ))

    @class_description(CharacterClass.MONK_SHADOW)
    def monk_shadow_description(self, class_description: ClassDescription) -> None:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_DisplayName"] = {"en": "Way of the Arcane"}
        loca[f"{self.mod.get_prefix()}_Description"] = {"en": """
            You seek mastery over mind and body. Your Ki connects you to the Weave.
            """}

        class_description.DisplayName = loca[f"{self.mod.get_prefix()}_DisplayName"]
        class_description.Description = loca[f"{self.mod.get_prefix()}_Description"]

        class_description.CanLearnSpells = True
        class_description.MustPrepareSpells = True

    @progression(CharacterClass.MONK, 1)
    @progression(CharacterClass.MONK, 1, is_multiclass=True)
    def monk_level_1_add_subclasses(self, progress: Progression) -> None:
        progress.children = [
            Progression.Subclasses(children=[
                Progression.Subclasses.Subclass(Object="22894c32-54cf-49ea-b366-44bfcf01bb2a"),
                Progression.Subclasses.Subclass(Object="2a5e3097-384c-4d29-8d6e-054fdfd26b80"),
                Progression.Subclasses.Subclass(Object="bf46d73f-d406-4cb8-9a1d-e6e758ca02c7"),
                Progression.Subclasses.Subclass(Object="d8d9e1e3-cbd6-4240-ab1e-bd3626cb5532"),
            ]),
        ]

    @progression(CharacterClass.MONK, range(1, 21))
    @progression(CharacterClass.MONK, 1, is_multiclass=True)
    def monk_level_1_to_20(self, progress: Progression) -> None:
        spells_always_prepared(progress)

    @progression(CharacterClass.MONK, 3)
    def monk_level_3_remove_subclasses(self, progress: Progression) -> None:
        progress.children = None

    @progression(CharacterClass.MONK, 4)
    def monk_level_4_replace_slow_fall(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            *[passive for passive in progress.PassivesAdded if not passive == "SlowFall"],
            self._slow_fall,
        ]

    @progression(CharacterClass.MONK, 7)
    def monk_level_7_replace_stillness_of_mind(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            *[passive for passive in progress.PassivesAdded if not passive == "StillnessOfMind"],
            self._stillness_of_mind,
        ]

    @progression(CharacterClass.MONK_SHADOW, 1)
    def monk_shadow_level_1(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{2 * self.args.spells},1)",
        ]
        progress.PassivesAdded = [
            "UnlockedSpellSlotLevel1",
            "DevilsSight",
            self._battle_magic,
            self._pack_mule,
            self._warding,
        ]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_CANTRIP_SPELL_LIST},3,0,,,,AlwaysPrepared)",
            f"SelectSpells({self._WIZARD_LEVEL_1_SPELL_LIST},6,0)",
            "Tag(WIZARD)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 2)
    def monk_shadow_level_2(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},1)",
        ]
        progress.PassivesAdded = ["SculptSpells"]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_1_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 3)
    def monk_shadow_level_3(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},1)",
            f"ActionResource(SpellSlot,{2 * self.args.spells},2)",
        ]
        progress.PassivesAdded = [
            "FastHands",
            "UnlockedSpellSlotLevel2",
            self._awareness,
        ]
        progress.PassivesRemoved = [
            "FlurryOfBlowsUnlock",
            "MartialArts_BonusUnarmedStrike",
        ]
        progress.Selectors = [
            f"AddSpells({self._flurry_of_blows_spell_list},,,,AlwaysPrepared)",
            f"SelectSpells({self._WIZARD_LEVEL_2_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 4)
    def monk_shadow_level_4(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},2)",
        ]
        progress.PassivesAdded = None
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            f"SelectSpells({self._WIZARD_CANTRIP_SPELL_LIST},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({self._WIZARD_LEVEL_2_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 5)
    def monk_shadow_level_5(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{2 * self.args.spells},3)",
        ]
        progress.PassivesAdded = ["UnlockedSpellSlotLevel3"]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_3_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 6)
    def monk_shadow_level_6(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},3)",
        ]
        progress.PassivesAdded = [self._arcane_manifestation]
        progress.Selectors = [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)",
            f"SelectSpells({self._WIZARD_LEVEL_3_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 7)
    def monk_shadow_level_7(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},4)",
        ]
        progress.PassivesAdded = [self._wholeness_of_body]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_4_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 8)
    def monk_shadow_level_8(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},4)",
        ]
        progress.PassivesAdded = ["ImprovedCritical"]
        progress.Selectors = [
            f"AddSpells({self._ACTION_SURGE_SPELL_LIST},,,,AlwaysPrepared)",
            f"SelectSpells({self._WIZARD_LEVEL_4_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 9)
    def monk_shadow_level_9(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},4)",
            f"ActionResource(SpellSlot,{1 * self.args.spells},5)",
        ]
        progress.PassivesAdded = ["Indomitable"]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_5_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 10)
    def monk_shadow_level_10(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},5)",
        ]
        progress.PassivesAdded = [self._empowered_spells]
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            f"SelectSpells({self._WIZARD_CANTRIP_SPELL_LIST},1,0,,,,AlwaysPrepared)",
            f"SelectSpells({self._WIZARD_LEVEL_5_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 11)
    def monk_shadow_level_11(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},6)",
        ]
        progress.PassivesAdded = ["ExtraAttack_2"]
        progress.PassivesRemoved = ["ExtraAttack"]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 12)
    def monk_shadow_level_12(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ReliableTalent"]
        progress.Selectors = [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)",
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 13)
    def monk_shadow_level_13(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},7)",
        ]
        progress.PassivesAdded = ["Indomitable_2"]
        progress.PassivesRemoved = ["Indomitable"]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 14)
    def monk_shadow_level_14(self, progress: Progression) -> None:
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 15)
    def monk_shadow_level_15(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},8)",
        ]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 16)
    def monk_shadow_level_16(self, progress: Progression) -> None:
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 17)
    def monk_shadow_level_17(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},9)",
        ]
        progress.PassivesAdded = ["Indomitable_3"]
        progress.PassivesRemoved = ["Indomitable_2"]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 18)
    def monk_shadow_level_18(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},5)",
        ]
        progress.Selectors = [
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)",
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 19)
    def monk_shadow_level_19(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},6)",
        ]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]

    @progression(CharacterClass.MONK_SHADOW, 20)
    def monk_shadow_level_20(self, progress: Progression) -> None:
        progress.Boosts = [
            f"ActionResource(SpellSlot,{1 * self.args.spells},7)",
        ]
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]
        progress.Selectors = [
            f"SelectSpells({self._WIZARD_LEVEL_6_SPELL_LIST},2,0)",
        ]


def main() -> None:
    way_of_the_arcane = WayOfTheArcane(
        classes=[
            CharacterClass.MONK_SHADOW
        ],
        feats=2,
        spells=2,
        warlock_spells=2,
        actions=2,
        skills=4,
        expertise=2,
    )
    way_of_the_arcane.build()


if __name__ == "__main__":
    main()
