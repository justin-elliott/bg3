
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
    spell_list,
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
    def _armour_of_avernus(self) -> str:
        """Add the Armour of Avernus spell, returning its name."""
        name = f"{self.mod.get_prefix()}_ArmourOfAvernus"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Armour of Avernus"}

        self.mod.add(SpellData(
            name,
            SpellType="Shout",
            using="Shout_ArmorOfAgathys",
            Icon="Spell_Evocation_FireShield_Warm",
            DisplayName=loca[f"{name}_DisplayName"],
            DescriptionParams=["GainTemporaryHitPoints(5)", "DealDamage(5,Fire)"],
            TooltipUpcastDescriptionParams=["GainTemporaryHitPoints(5)", "DealDamage(5,Fire)"],
            TooltipStatusApply=[f"ApplyStatus({name.upper()},100,-1)"],
            SpellProperties=[f"ApplyStatus({name.upper()},100,-1)"],
            CastSound="Spell_Cast_Utility_FireshieldWarm_L4to5",
            TargetSound="Spell_Impact_Utility_FireshieldWarm_L4to5",
            PrepareEffect="ab9a9a13-7ceb-46ee-bd9e-74c044516fb1",
            CastEffect="859bdcb8-c4dc-487d-8e44-452b1be1c034",
        ))

        self.mod.add(StatusData(
            name.upper(),
            StatusType="BOOST",
            using="ARMOR_OF_AGATHYS",
            Icon="Spell_Evocation_FireShield_Warm",
            DisplayName=loca[f"{name}_DisplayName"],
            DescriptionParams=["DealDamage(5,Fire)", "5"],
            Passives=[f"{name}_Passive"],
            OnApplyFunctors=[f"AI_ONLY:IF(not HasStatus('{name.upper()}')):ApplyStatus(AI_HELPER_BUFF,100,1)"],
            # StatusEffect="393ae64d-5014-4614-b25c-82ff744c0f31",  # ORI_KARLACH_BURNING_LOWLEVEL_VFX
            # StatusEffect="2156dd48-f83b-4060-9a4e-cab994da8857",  # BURNING
            # StatusEffect="c3da0783-72b5-4054-9516-9d1acdc8db93",  # BURNING_HELLFIRE
            # StatusEffect="9055845d-c778-44ba-a671-b0a112bacf61",  # BURNING_HOLY
            StatusEffect="a25f92a9-7078-4a5f-8648-c0bb9f4fee39",  # FIRE_SHIELD_WARM
        ))

        self.mod.add(PassiveData(
            f"{name}_Passive",
            using="ArmorOfAgathys",
            Icon="Spell_Evocation_FireShield_Warm",
            DisplayName=loca[f"{name}_DisplayName"],
            Description="hb6cc3a06gbe30g4fc9gada9gc8d15a7d9f8e;1",
            DescriptionParams=["DealDamage(5,Fire)"],
            StatsFunctors=[
                "ApplyStatus(PASSIVE_FIRE_SHIELD_WARM,100,0)",
                "ApplyStatus(SELF,PASSIVE_FIRE_SHIELD_WARM_ATTACKER,100,0)",
                "DealDamage(SWAP,5,Fire,Magical)",
            ],
        ))

        for level in range(2, 6):
            self.mod.add(SpellData(
                f"{name}_{level}",
                SpellType="Shout",
                using=name,
                DescriptionParams=[f"GainTemporaryHitPoints({5 * level})", f"DealDamage({5 * level},Fire)"],
                TooltipStatusApply=[f"ApplyStatus({name.upper()}_{level},100,-1)"],
                SpellProperties=[f"ApplyStatus({name.upper()}_{level},100,-1)"],
                PowerLevel=level,
                RootSpellID=name,
                UseCosts=["ActionPoint:1", f"SpellSlotsGroup:1:1:{level}"],
            ))

            self.mod.add(StatusData(
                f"{name.upper()}_{level}",
                StatusType="BOOST",
                using=name.upper(),
                DescriptionParams=[f"DealDamage({5 * level},Fire)", f"{5 * level}"],
                Boosts=[f"TemporaryHP({5 * level})"],
                Passives=[f"{name}_Passive_{level}"],
            ))

            self.mod.add(PassiveData(
                f"{name}_Passive_{level}",
                using=f"{name}_Passive",
                DescriptionParams=[f"DealDamage({5 * level},Fire)"],
                StatsFunctors=[
                    "ApplyStatus(PASSIVE_FIRE_SHIELD_WARM,100,0)",
                    "ApplyStatus(SELF,PASSIVE_FIRE_SHIELD_WARM_ATTACKER,100,0)",
                    f"DealDamage(SWAP,{5 * level},Fire,Magical)",
                ],
            ))

        return name

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
        ))

        return name

    @cached_property
    def _hells_guidance(self) -> str:
        """Add the Hells' Guidance spell."""
        hells_guidance = f"{self.mod.get_name()}_HellsGuidance"

        loca = self.mod.get_localization()
        loca[f"{hells_guidance}_DisplayName"] = {"en": "Hells' Guidance"}
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
            Spells=["Projectile_ScorchingRay"],
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
            Spells=["Wall_WallOfFire"],
            UUID=self.make_uuid(name),
        )
        self.mod.add(spells)
        return str(spells.UUID)

    @spell_list("Warlock Hexblade SLevel 1")
    @spell_list("Warlock Hexblade SLevel 2")
    @spell_list("Warlock Hexblade SLevel 3")
    @spell_list("Warlock Hexblade SLevel 4")
    @spell_list("Warlock Hexblade SLevel 5")
    def warlock_hexblade_spells_level_1(self, spells: SpellList) -> None:
        spells.Spells = [
            self._armour_of_avernus if spell == "Shout_ArmorOfAgathys" else spell for spell in spells.Spells
        ]

    @class_description(CharacterClass.WARLOCK_HEXBLADE)
    def warlock_hexblade_class_description(self, class_description: ClassDescription) -> None:
        class_description.children.append(ClassDescription.Tags(
            Object="18266c0b-efbc-4c80-8784-ada4a37218d7"  # SORCERER
        ))

    @progression(CharacterClass.WARLOCK_HEXBLADE, 1)
    def warlock_hexblade_level_1(self, progress: Progression) -> None:
        progress.Boosts = ["ProficiencyBonus(SavingThrow,Constitution)"]
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
    def warlock_hexblade_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ReliableTalent"]

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
