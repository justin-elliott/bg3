
import os

from functools import cached_property
from moddb import (
    Awareness,
    BattleMagic,
    Bolster,
    Defense,
    Movement,
    PackMule,
)
from modtools.gamedata import (
    PassiveData,
    SpellData,
    StatusData,
)
from modtools.lsx.game import (
    ClassDescription,
    Progression,
    SpellList,
)
from modtools.replacers import (
    CharacterClass,
    class_description,
    DontIncludeProgression,
    progression,
    Replacer,
)


class Hellblade(Replacer):
    # Passives
    _awareness: str
    _battle_magic: str
    _fast_movement_30: str
    _fast_movement_45: str
    _fast_movement_60: str
    _fast_movement_75: str
    _pack_mule: str
    _warding: str

    # Spells
    _bolster: str

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="Hellblade",
                         description="A class replacer for Hexblade.",
                         **kwds)

        self._fast_movement_30 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_45 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_60 = Movement(self.mod).add_fast_movement(3.0)
        self._fast_movement_75 = Movement(self.mod).add_fast_movement(3.0)

        self._awareness = Awareness(self.mod).add_awareness()
        self._battle_magic = BattleMagic(self.mod).add_battle_magic()
        self._pack_mule = PackMule(self.mod).add_pack_mule(5.0)
        self._warding = Defense(self.mod).add_warding()

        self._bolster = Bolster(self.mod).add_bolster()

    @cached_property
    def _fire_walk(self) -> str:
        """Add the Fire Walk spell, returning its name."""
        name = f"{self.mod.get_prefix()}_FireWalk"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Fire Walk"}
        loca[f"{name}_Description"] = {"en": """
            You step through the hells, reappearing in another location.
            """}

        self.mod.add(SpellData(
            name,
            SpellType="Target",
            using="Target_MAG_Legendary_HellCrawler",
            Cooldown="",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams="",
            SpellProperties=["GROUND:TeleportSource()"],
            UseCosts=["Movement:Distance*0.5"],
        ))

        return name

    @cached_property
    def _hells_guidance(self) -> str:
        """Add the Hell's Guidance spell."""
        hells_guidance = f"{self.mod.get_name()}_HellsGuidance"

        loca = self.mod.get_localization()
        loca[f"{hells_guidance}_DisplayName"] = {"en": "Hell's Guidance"}
        loca[f"{hells_guidance}_Description"] = {"en": """
            The target gains a +1d4 bonus to <LSTag Tooltip="AbilityCheck">Ability Checks</LSTag> and
            <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>, and has <LSTag Tooltip="Advantage">Advantage</LSTag> on
            <LSTag Tooltip="Charisma">Charisma</LSTag> checks.
            """}

        self.mod.add(SpellData(
            hells_guidance,
            SpellType="Target",
            using="Target_Guidance",
            DisplayName=loca[f"{hells_guidance}_DisplayName"],
            Description=loca[f"{hells_guidance}_Description"],
            SpellProperties=[f"ApplyStatus({hells_guidance.upper()},100,10)"],
            TooltipStatusApply=[f"ApplyStatus({hells_guidance.upper()},100,10)"],
        ))
        self.mod.add(StatusData(
            hells_guidance.upper(),
            StatusType="BOOST",
            using="GUIDANCE",
            DisplayName=loca[f"{hells_guidance}_DisplayName"],
            Description=loca[f"{hells_guidance}_Description"],
            Boosts=[
                "RollBonus(SkillCheck,1d4)",
                "RollBonus(RawAbility,1d4)",
                "RollBonus(SavingThrow,1d4)",
                "RollBonus(DeathSavingThrow,1d4)",
                "Advantage(Ability,Charisma)",
            ],
            StackId=hells_guidance.upper(),
        ))

        return hells_guidance

    @cached_property
    def _infernal_blade(self) -> str:
        """Add the Infernal Blade spell, returning its name."""
        name = f"{self.mod.get_prefix()}_InfernalBlade"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Infernal Blade"}
        loca[f"{name}_Description"] = {"en": """
            Strike with your weapon, dealing an additional [1].
            """}

        self.mod.add(SpellData(
            name,
            SpellType="Target",
            using="Target_Slash_New",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["DealDamage(LevelMapValue(D8Cantrip),Fire)"],
            ExtraDescription="",
            Icon="Spell_Evocation_FlameBlade",
            SpellSchool="Evocation",
            Cooldown="None",
            SpellProperties=[
                "GROUND:DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "GROUND:ExecuteWeaponFunctors(MainHand)",
                "CastOffhand[" +
                    "GROUND:DealDamage(OffhandMeleeWeapon,OffhandMeleeWeaponDamageType)" +
                    "GROUND:ExecuteWeaponFunctors(OffHand)" +
                "]",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
            ],
            SpellSuccess=[
                "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "DealDamage(LevelMapValue(D8Cantrip),Fire)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            SpellFlags=["IsMelee", "IsHarmful", "IsDefaultWeaponAction", "IsSpell"],
            TooltipAttackSave="MeleeWeaponAttack",
            TooltipDamageList=[
                "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "DealDamage(LevelMapValue(D8Cantrip),Fire)",
            ],
            TooltipStatusApply="",
            SpellAnimation=[
                "71369b20-18f1-4d33-89ad-a99b10f0444c,,",
                "c12054bc-4d96-47c5-8483-989afde03bd4,,",
                "20aaabc2-067d-4355-86a0-40901d3938d8,,",
                "2a3d2709-24d3-4c6d-ae25-546d1fd4ccb2,,",
                "3b9da8d4-3eff-43bd-9eaa-1c13fba0045e,,",
                "4c38bf59-cfbd-4389-954f-81290ca30476,,",
                "0b07883a-08b8-43b6-ac18-84dc9e84ff50,,",
                ",,",
                ",,",
            ],
            DualWieldingSpellAnimation=[
                "71369b20-18f1-4d33-89ad-a99b10f0444c,,",
                "c12054bc-4d96-47c5-8483-989afde03bd4,,",
                "20aaabc2-067d-4355-86a0-40901d3938d8,,",
                "2a3d2709-24d3-4c6d-ae25-546d1fd4ccb2,,",
                "3b9da8d4-3eff-43bd-9eaa-1c13fba0045e,,",
                "4c38bf59-cfbd-4389-954f-81290ca30476,,",
                "0b07883a-08b8-43b6-ac18-84dc9e84ff50,,",
                ",,",
                ",,",
            ],
            PrepareSound="Spell_Prepare_Damage_Fire_Gen_L1to3",
            PrepareLoopSound="CrSpell_Loop_Azer_SearingSmite",
            CastSound="Spell_Cast_Damage_SearingSmite_L1to3",
            TargetSound="Spell_Impact_Damage_SearingSmite_L1to3",
            PrepareEffect="d2ed4f24-55f8-4c70-9bd1-8da22deb8e83",
            CastEffect="b5b24254-75d3-4575-af9f-ba3575a2f8b7",
            TargetEffect="d5f54cd9-9252-4bcd-9e04-7e63d071eac6",
        ))

        return name

    @cached_property
    def _searing_blast(self) -> str:
        """Add the Searing Blast passive, augmenting Eldritch Blast with fire damage."""
        name = f"{self.mod.get_prefix()}_SearingBlast"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Searing Blast"}
        loca[f"{name}_Description"] = {"en": """
            Each beam of your <LSTag Type="Spell" Tooltip="Projectile_EldritchBlast">Eldritch Blast</LSTag> deals an
            additional [1].
            """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["DealDamage(max(CharismaModifier,1),Fire)"],
            Icon="Spell_Evocation_FireBolt",
            Properties=["Highlighted", "DisplayBoostInTooltip"],
            Boosts=["IF(SpellId('Projectile_EldritchBlast')):DamageBonus(max(CharismaModifier,1),Fire)"],
        ))

        return name

    @cached_property
    def _spells_level_1(self) -> str:
        name = "Hellblade spells gained at level 1"
        spells = SpellList(
            Name=name,
            Spells=[
                self._bolster,
                "Zone_BurningHands",
                "Target_Command_Container",
                self._hells_guidance,
                self._infernal_blade,
            ],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return str(spells.UUID)

    @cached_property
    def _spells_level_3(self) -> str:
        name = "Hellblade spells gained at level 3"
        spells = SpellList(
            Name=name,
            Spells=["Target_HeatMetal", "Projectile_ScorchingRay"],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return str(spells.UUID)

    @cached_property
    def _spells_level_5(self) -> str:
        name = "Hellblade spells gained at level 5"
        spells = SpellList(
            Name=name,
            Spells=["Projectile_Fireball", self._fire_walk],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return str(spells.UUID)

    @cached_property
    def _spells_level_7(self) -> str:
        name = "Hellblade spells gained at level 7"
        spells = SpellList(
            Name=name,
            Spells=["Shout_FireShield", "Wall_WallOfFire"],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return str(spells.UUID)

    @class_description(CharacterClass.WARLOCK_HEXBLADE)
    def wizard_bladesinging_class_description(self, class_description: ClassDescription) -> None:
        class_description.children.append(ClassDescription.Tags(
            Object="18266c0b-efbc-4c80-8784-ada4a37218d7"  # SORCERER
        ))

    @progression(CharacterClass.WARLOCK_HEXBLADE, 1)
    def warlock_hexblade_level_1(self, progress: Progression) -> None:
        progress.PassivesAdded += [
            self._battle_magic,
            self._pack_mule,
            self._searing_blast,
            self._warding,
        ]
        progress.Selectors += [f"AddSpells({self._spells_level_1})"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 2)
    def warlock_hexblade_level_2(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_30]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 3)
    def warlock_hexblade_level_3(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._awareness]
        progress.Selectors += [f"AddSpells({self._spells_level_3})"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 4)
    def warlock_hexblade_level_4(self, progress: Progression) -> None:
        progress.Selectors += ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 5)
    def warlock_hexblade_level_5(self, progress: Progression) -> None:
        progress.Selectors += [f"AddSpells({self._spells_level_5})"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 6)
    def warlock_hexblade_level_6(self, progress: Progression) -> None:
        progress.PassivesAdded += ["ElementalAdept_Fire"]
        progress.Selectors += ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 7)
    def warlock_hexblade_level_7(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_45]
        progress.PassivesRemoved = [self._fast_movement_30]
        progress.Selectors += [f"AddSpells({self._spells_level_7})"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 8)
    def warlock_hexblade_level_8(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WARLOCK_HEXBLADE, 9)
    def warlock_hexblade_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WARLOCK_HEXBLADE, 10)
    def warlock_hexblade_level_10(self, progress: Progression) -> None:
        progress.Selectors += ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 11)
    def warlock_hexblade_level_11(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WARLOCK_HEXBLADE, 12)
    def warlock_hexblade_level_12(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_60]
        progress.PassivesRemoved = [self._fast_movement_45]
        progress.Selectors += ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 13)
    def warlock_hexblade_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WARLOCK_HEXBLADE, 14)
    def warlock_hexblade_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WARLOCK_HEXBLADE, 15)
    def warlock_hexblade_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WARLOCK_HEXBLADE, 16)
    def warlock_hexblade_level_16(self, progress: Progression) -> None:
        progress.Selectors += ["SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 17)
    def warlock_hexblade_level_17(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._fast_movement_75]
        progress.PassivesRemoved = [self._fast_movement_60]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 18)
    def warlock_hexblade_level_18(self, progress: Progression) -> None:
        progress.Selectors += ["SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2,true)"]

    @progression(CharacterClass.WARLOCK_HEXBLADE, 19)
    def warlock_hexblade_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.WARLOCK_HEXBLADE, 20)
    def warlock_hexblade_level_20(self, _: Progression) -> None:
        raise DontIncludeProgression()


def main() -> None:
    hellblade = Hellblade(
        classes=[
            CharacterClass.WARLOCK_HEXBLADE
        ],
        feats=2,
        spells=2,
        warlock_spells=4,
        actions=2,
        skills=4,
        expertise=2,
    )
    hellblade.build()


if __name__ == "__main__":
    main()
