#!/usr/bin/env python3
"""
Generates files for the "Pyromancy" mod.
"""

import argparse
import os

from dataclasses import dataclass
from functools import cached_property
from moddb import (
    Bolster,
    Defense,
    multiply_resources,
)
from modtools.gamedata import (
    PassiveData,
    SpellData,
    StatusData,
)
from modtools.lsx.game import (
    ActionResource,
    CharacterClass,
    ClassDescription,
)
from modtools.lsx.game import (
    Progression,
    SpellList,
    Tags,
    TooltipUpcastDescription,
)
from modtools.replacers import (
    class_description,
    progression,
    Replacer,
    tag,
)
from modtools.text import Equipment


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-g265.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class Pyromancy(Replacer):
    @dataclass
    class Args:
        feats: int    # Feats every n levels
        spells: int   # Multiplier for spell slots
        actions: int  # Multiplier for other action resources (Sorcery Points)

    _args: Args
    _feat_levels: set[int]

    # Passives
    _warding: str

    # spells
    _bolster: str

    @cached_property
    def _pyromancy_display_name(self) -> str:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_DisplayName"] = {"en": "Pyromancy"}
        return loca[f"{self.mod.get_prefix()}_DisplayName"]

    @cached_property
    def _pyromancy_description(self) -> str:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_Description"] = {"en": """
            Flickering flames dance on your fingertips, a primal power yearning to be unleashed. You are not just a
            sorcerer, but a conduit, channeling the raw essence of fire into searing spells and devastating displays.
            """}
        return loca[f"{self.mod.get_prefix()}_Description"]

    @cached_property
    def _firewalk(self) -> str:
        """Add the Firewalk spell, returning its name."""
        name = f"{self._mod.get_prefix()}_Firewalk"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Firewalk"}
        loca[f"{name}_Description"] = {"en": """
            You step through the hells, reappearing in another location.
            """}

        self._mod.add(SpellData(
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
    def _forged_in_flames(self) -> str:
        """Add the Forged in Flames passive, returning its name."""
        name = f"{self._mod.get_prefix()}_ForgedInFlames"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Forged in Flames"}
        loca[f"{name}_Description"] = {"en": """
            You have <LSTag Tooltip="Resistant">Resistance</LSTag> to Fire damage, and cannot be
            <LSTag Type="Status" Tooltip="BURNING">Burned</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Gold",
            Properties=["Highlighted"],
            Boosts=[
                "Resistance(Fire,Resistant)",
                "StatusImmunity(BURNING)",
                "StatusImmunity(WILD_MAGIC_BURNING)",
            ],
        ))

        return name

    @cached_property
    def _overheat(self) -> str:
        """Add the Overheat passive, returning its name."""
        name = f"{self._mod.get_prefix()}_Overheat"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Overheat"}
        loca[f"{name}_Description"] = {"en": """
            Your fire spells burn hotter, ignoring resistance, and dealing additional damage equal to your
            <LSTag Tooltip="Charisma">Charisma</LSTag> <LSTag Tooltip="AbilityModifier">Modifier</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Brass",
            Properties=["Highlighted"],
            Boosts=[
                "IgnoreResistance(Fire,Resistant)",
                "IF(SpellDamageTypeIs(DamageType.Fire)):DamageBonus(max(0,CharismaModifier))",
            ],
        ))

        return name

    @cached_property
    def _hellfire(self) -> str:
        """Add the Hellfire passive, returning its name."""
        name = f"{self._mod.get_prefix()}_Hellfire"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Hellfire"}
        loca[f"{name}_Description"] = {"en": """
            Your fire spells burn as hot as the hells, overcoming resistance and immunity, and dealing additional damage
            equal to twice your <LSTag Tooltip="Charisma">Charisma</LSTag>
            <LSTag Tooltip="AbilityModifier">Modifier</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Brass",
            Properties=["Highlighted"],
            Boosts=[
                "IgnoreResistance(Fire,Immune)",
                "IgnoreResistance(Fire,Resistant)",
                "IF(SpellDamageTypeIs(DamageType.Fire)):DamageBonus(max(0,CharismaModifier*2))",
            ],
        ))

        return name

    @cached_property
    def _ignite_weapon(self) -> str:
        loca = self.mod.get_localization()
        name = f"{self.mod.get_prefix()}_IgniteWeapon"

        loca[f"{name}_DisplayName"] = {"en": "Ignite Weapon"}
        loca[f"{name}_Description"] = {"en": """
            Infuse the weapon in your main hand with fire. The weapon becomes magical, preventing it from being
            disarmed. It receives a +[1] bonus to <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>,
            <LSTag Tooltip="SpellDifficultyClass">Spell Save DC</LSTag>, and Damage Rolls, and deals an additional [2].
            """}
        loca[f"{name}_StatusDescription"] = {"en": """
            Weapon has become magical, preventing it from being disarmed. It receives a +[1] bonus to
            <LSTag Tooltip="AttackRoll">Attack Rolls</LSTag>,
            <LSTag Tooltip="SpellDifficultyClass">Spell Save DC</LSTag>, and Damage Rolls, and deals an additional [2].
            """}
        loca[f"{name}_UpcastDescription"] = {"en": """
            Casting this spell using a 4th or 5th level spell slot will increase the Attack and Damage bonus to [1], and
            a 6th level spell slot will increase it to [2].
            """}

        upcast_description = TooltipUpcastDescription(
            Name="Ignite Weapon",
            Text=loca[f"{name}_UpcastDescription"],
            UUID=self.make_uuid("Upcast Ignite Weapon"),
        )
        self.mod.add(upcast_description)

        self.mod.add(SpellData(
            name,
            SpellType="Shout",
            Level="2",
            SpellSchool="Abjuration",
            AIFlags="CanNotUse",
            SpellProperties=[
                f"ApplyStatus({name.upper()}_CASTER,100,-1)",
                f"ApplyEquipmentStatus(MainHand,{name.upper()}_WEAPON,100,-1)",
            ],
            TargetConditions="Self() and HasWeaponInMainHand()",
            Icon="Spell_Evocation_FlameBlade",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["1", "DealDamage(1d4,Fire)"],
            TooltipStatusApply=f"ApplyStatus({name.upper()}_WEAPON,100,-1)",
            TooltipUpcastDescription=upcast_description.UUID,
            TooltipUpcastDescriptionParams=["2", "3"],
            PrepareSound="Spell_Prepare_Buff_ElementalWeaponFire_L1to3",
            PrepareLoopSound="Spell_Loop_Buff_ElementalWeaponFire_L1to3L1to3",
            CastSound="Spell_Cast_Buff_ElementalWeaponFire_L1to3",
            TargetSound="Spell_Impact_Buff_ElementalWeaponFire_L1to3",
            VocalComponentSound="Vocal_Component_EnchantWeapon",
            PreviewCursor="Cast",
            CastTextEvent="Cast",
            UseCosts="ActionPoint:1;SpellSlotsGroup:1:1:2",
            SpellAnimation=[
                "554a18f7-952e-494a-b301-7702a85d4bc9,,",
                ",,",
                "a4da186a-0872-461e-ae5e-93d5b32b9bef,,",
                "527ca082-4ffa-4edb-a23f-5e7fa798a6ce,,",
                "22dfbbf4-f417-4c84-b39e-2039315961e6,,",
                ",,",
                "5bfbe9f9-4fc3-4f26-b112-43d404db6a89,,",
                "499b7945-9eff-40a2-9911-73b8963108e4,,",
                "1d3a29f0-9409-462e-81cd-3f24944f63ca,,",
            ],
            VerbalIntent="Buff",
            SpellFlags=["IsSpell", "HasVerbalComponent", "HasSomaticComponent"],
            PrepareEffect="6e0c79d5-f724-4628-8669-da3d766e9b83",
            CastEffect="d8ed1647-82eb-4079-a914-1b2c2a89f153",
        ))

        self.mod.add(StatusData(
            f"{name.upper()}_CASTER",
            StatusType="BOOST",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_StatusDescription"],
            DescriptionParams=["1", "DealDamage(1d4,Fire)"],
            Icon="Spell_Transmutation_MagicWeapon",
            StackId=f"{name.upper()}_CASTER",
            StackPriority="0",
            Boosts=[
                "SpellSaveDC(1)",
                "RollBonus(MeleeSpellAttack,1)",
                "RollBonus(RangedSpellAttack,1)",
            ],
            StatusGroups="SG_RemoveOnRespec",
            StatusPropertyFlags=["DisableCombatlog", "DisableOverhead", "DisablePortraitIndicator"],
            ApplyEffect="6994e8dc-14ac-48a5-9c8e-c1925031e852",
        ))

        self.mod.add(StatusData(
            f"{name.upper()}_WEAPON",
            StatusType="BOOST",
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_StatusDescription"],
            DescriptionParams=["1", "DealDamage(1d4,Fire)"],
            Icon="Spell_Transmutation_MagicWeapon",
            StackId=f"{name.upper()}_WEAPON",
            StackPriority="0",
            Boosts=[
                "CannotBeDisarmed()",
                "WeaponDamage(1d4,Fire,Magical)",
                "WeaponEnchantment(1)",
                "WeaponProperty(Magical)",
            ],
            StatusGroups="SG_RemoveOnRespec",
            ApplyEffect="6994e8dc-14ac-48a5-9c8e-c1925031e852",
            StatusEffect="44d77ebf-fc9e-407d-b20f-257019351f2a",
        ))

        for level in range(3, 7):
            self.mod.add(SpellData(
                f"{name}_{level}",
                using=name,
                SpellType="Shout",
                PowerLevel=f"{level}",
                RootSpellID=name,
                SpellProperties=[
                    f"ApplyStatus({name.upper()}_CASTER_{level},100,-1)",
                    f"ApplyEquipmentStatus(MainHand,{name.upper()}_WEAPON_{level},100,-1)",
                ],
                TooltipStatusApply=f"ApplyStatus({name.upper()}_WEAPON_{level},100,-1)",
                UseCosts=["ActionPoint:1", f"SpellSlotsGroup:1:1:{level}"],
            ))

            self.mod.add(StatusData(
                f"{name.upper()}_CASTER_{level}",
                using=f"{name.upper()}_CASTER",
                StatusType="BOOST",
                DescriptionParams=[f"{level // 2}", f"DealDamage({level - 1}d4,Fire)"],
                Boosts=[
                    f"SpellSaveDC({level // 2})",
                    f"RollBonus(MeleeSpellAttack,{level // 2})",
                    f"RollBonus(RangedSpellAttack,{level // 2})",
                ],
            ))

            self.mod.add(StatusData(
                f"{name.upper()}_WEAPON_{level}",
                using=f"{name.upper()}_WEAPON",
                StatusType="BOOST",
                DescriptionParams=[f"{level // 2}", f"DealDamage({level - 1}d4,Fire)"],
                Boosts=[
                    "CannotBeDisarmed()",
                    f"WeaponDamage({level - 1}d4,Fire,Magical)",
                    f"WeaponEnchantment({level // 2})",
                    "WeaponProperty(Magical)",
                ],
            ))

        return name

    @cached_property
    def _class_equipment(self) -> str:
        name = f"{self.mod.get_prefix()}_ClassEquipment"

        self.mod.add(Equipment(f"""
            new equipment "{name}"
            add initialweaponset "Melee"
            add equipmentgroup
            add equipment entry "WPN_Katana"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "ARM_Boots_Metal"
            add equipmentgroup
            add equipment entry "ARM_Breastplate_Body_1"
            add equipmentgroup
            add equipment entry "OBJ_Scroll_Revivify"
            add equipmentgroup
            add equipment entry "OBJ_Keychain"
            add equipmentgroup
            add equipment entry "OBJ_Bag_AlchemyPouch"
            add equipmentgroup
            add equipment entry "ARM_Camp_Body"
            add equipmentgroup
            add equipment entry "ARM_Camp_Shoes"
            add equipmentgroup
            add equipment entry "OBJ_Backpack_CampSupplies"
            """))

        return name

    @cached_property
    def _level_1_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_1_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Sorcerer level 1",
            Spells=[self._bolster, "Projectile_FireBolt", "Shout_HellishRebuke", "Zone_BurningHands"],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_3_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_3_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Sorcerer level 3",
            Spells=["Target_HeatMetal", self._ignite_weapon, "Projectile_ScorchingRay"],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_5_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_5_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Sorcerer level 5",
            Spells=["Projectile_Fireball", self._firewalk],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_7_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_7_spelllist"))
        self.mod.add(SpellList(
            Comment="Spells gained at Sorcerer level 7",
            Spells=["Shout_FireShield", "Wall_WallOfFire"],
            UUID=spelllist,
        ))
        return spelllist

    def __init__(self, args: Args):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Pyromancy",
                         description="A replacer for Wild Magic Sorcery.")

        self._args = args
        self._feat_levels = {*range(max(args.feats, 2), 21, args.feats)}
        if 20 in self._feat_levels:
            self._feat_levels.remove(20)
            self._feat_levels.add(19)

        self._warding = Defense(self.mod).add_warding()
        self._bolster = Bolster(self.mod).add_bolster()

    @class_description(CharacterClass.SORCERER)
    def sorcerer_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6

    @class_description(CharacterClass.SORCERER_WILDMAGIC)
    def sorcerer_pyromancy_description(self, class_description: ClassDescription) -> None:
        class_description.ClassEquipment = self._class_equipment
        class_description.DisplayName = self._pyromancy_display_name
        class_description.Description = self._pyromancy_description

    @tag("885f8675-e400-4d53-924d-6204ff1d9558")
    def wild_magic_tag(self, tag: Tags.Tags) -> None:
        tag.DisplayName = self._pyromancy_display_name
        tag.DisplayDescription = self._pyromancy_description

    @progression(CharacterClass.SORCERER, 1)
    def level_1_sorcerer(self, progression: Progression) -> None:
        selectors = progression.Selectors or []
        selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
        selectors.extend([
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,5)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @progression(CharacterClass.SORCERER, range(1, 21))
    @progression(CharacterClass.SORCERER, 1, is_multiclass=True)
    def level_1_to_20_sorcerer(self, progression: Progression) -> None:
        progression.AllowImprovement = True if progression.Level in self._feat_levels else None
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self._args.spells)
        multiply_resources(progression, [ActionResource.SORCERY_POINTS], self._args.actions)

    @progression(CharacterClass.SORCERER_WILDMAGIC, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = [
            "Proficiency(LightArmor)",
            "Proficiency(MediumArmor)",
            "Proficiency(HeavyArmor)",
            "Proficiency(Shields)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
        ]
        progression.PassivesAdded = [
            self._forged_in_flames,
            self._warding,
        ]
        progression.Selectors = [
            f"AddSpells({self._level_1_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 2)
    def level_2(self, progression: Progression) -> None:
        progression.PassivesAdded = ["JackOfAllTrades"]
        progression.Selectors = None

    @progression(CharacterClass.SORCERER_WILDMAGIC, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = ["DevilsSight"]
        progression.Selectors = [
            f"AddSpells({self._level_3_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = ["SculptSpells"]
        progression.Selectors = None

    @progression(CharacterClass.SORCERER_WILDMAGIC, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = None
        progression.Selectors = [
            f"AddSpells({self._level_5_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._overheat]
        progression.Selectors = None

    @progression(CharacterClass.SORCERER_WILDMAGIC, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ImprovedCritical"]
        progression.Selectors = [
            f"AddSpells({self._level_7_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 8)
    def level_8(self, progression: Progression) -> None:
        progression.PassivesAdded = [
            "LandsStride_DifficultTerrain",
            "LandsStride_Surfaces",
            "LandsStride_Advantage",
            "FOR_NightWalkers_WebImmunity",
        ]
        progression.Selectors = None

    @progression(CharacterClass.SORCERER_WILDMAGIC, 9)
    def level_9(self, progression: Progression) -> None:
        progression.PassivesAdded = ["PotentCantrip"]
        progression.Selectors = None

    @progression(CharacterClass.SORCERER_WILDMAGIC, 10)
    def level_10(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._hellfire]
        progression.PassivesRemoved = [self._overheat]
        progression.Selectors = None

    @progression(CharacterClass.SORCERER_WILDMAGIC, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ReliableTalent"]
        progression.Selectors = None

    @progression(CharacterClass.SORCERER_WILDMAGIC, 12)
    def level_12(self, progression: Progression) -> None:
        progression.PassivesAdded = None
        progression.Selectors = None


def main():
    parser = argparse.ArgumentParser(description="A replacer for Wild Magic Sorcery.")
    parser.add_argument("-f", "--feats", type=int, choices=range(1, 5), default=1,
                        help="Feat progression every n levels (defaulting to 1; feat every level)")
    parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=2,
                        help="Spell slot multiplier (defaulting to 2; double spell slots)")
    parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=2,
                        help="Action resource (Sorcery Points) multiplier (defaulting to 2; double points)")
    args = Pyromancy.Args(**vars(parser.parse_args()))

    pyromancy = Pyromancy(args)
    pyromancy.build()


if __name__ == "__main__":
    main()
