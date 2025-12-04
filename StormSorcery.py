
from functools import cached_property
import os

from moddb import (
    BattleMagic,
    Bolster,
    EmpoweredSpells,
    spells_always_prepared,
)
from modtools.gamedata import Armor, PassiveData
from modtools.lsx.game import (
    CharacterAbility,
    ClassDescription,
    GameObjects,
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
from modtools.text import Equipment


class StormSorcery(Replacer):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="StormSorcery",
                         description="A class replacer for StormSorcery.",
                         **kwds)

    @cached_property
    def _equipment(self) -> str:
        name = f"{self.mod.get_prefix()}_Equipment"

        self.mod.add(Equipment(f"""
            new equipment "{name}"
            add initialweaponset "Melee"
            add equipmentgroup
            add equipment entry "WPN_Quarterstaff"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "OBJ_Potion_Healing"
            add equipmentgroup
            add equipment entry "ARM_Shoes"
            add equipmentgroup
            add equipment entry "ARM_Robe_Body_Sorcerer_StormSorcery"
            add equipmentgroup
            add equipment entry "{self._ring_of_frost_giant_strength}"
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
    def _ring_of_frost_giant_strength(self) -> str:
        name = f"{self.mod.get_prefix()}_RingOfFrostGiantStrength"

        strength = "23"
        damage_bonus = "1d4,Cold"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Ring of Frost Giant Strength"}
        loca[f"{name}_Description"] = {"en": f"""
            Forged from polished silver and etched with icy runes, this ring is painfully cold to the touch, granting
            the wearer the massive, chilling strength of a frost giant.
        """}

        ring_uuid = self.mod.make_uuid(name)
        self.mod.add(GameObjects(
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="Item_MAG_PHB_Ring_Of_Protection",
            LevelName="",
            MapKey=ring_uuid,
            ParentTemplateId="1abd032b-c138-45ee-b85e-62b5bbb6ea2d",
            Name=name,
            Stats=name,
            Type="item",
        ))

        hill_giant_strength = f"{self.mod.get_prefix()}_HillGiantStrength"
        chilling_blows = f"{self.mod.get_prefix()}_ChillingBlows"

        self.mod.add(Armor(
            name,
            using="_Ring_Magic",
            PassivesOnEquip=[hill_giant_strength, chilling_blows],
            Rarity="Legendary",
            RootTemplate=ring_uuid,
        ))

        loca[f"{hill_giant_strength}_DisplayName"] = {"en": "Hill Giant Strength"}
        loca[f"{hill_giant_strength}_Description"] = {"en": f"""
            Your <LSTag Tooltip="Strength">Strength</LSTag> increases to [1].
        """}

        self.mod.add(PassiveData(
            hill_giant_strength,
            DisplayName=loca[f"{hill_giant_strength}_DisplayName"],
            Description=loca[f"{hill_giant_strength}_Description"],
            DescriptionParams=[strength],
            Boosts=[f"AbilityOverrideMinimum(Strength,{strength})"]
        ))

        loca[f"{chilling_blows}_DisplayName"] = {"en": "Chilling Blows"}
        loca[f"{chilling_blows}_Description"] = {"en": f"""
            Your melee weapon and unarmed attacks deal an additional [1].
        """}

        self.mod.add(PassiveData(
            chilling_blows,
            DisplayName=loca[f"{chilling_blows}_DisplayName"],
            Description=loca[f"{chilling_blows}_Description"],
            DescriptionParams=[f"DealDamage({damage_bonus})"],
            Boosts=[f"IF(IsMeleeWeaponAttack() or IsMeleeUnarmedAttack()):DamageBonus({damage_bonus})"]
        ))

        return name

    @cached_property
    def _battle_magic(self) -> str:
        return BattleMagic(self.mod).add_battle_magic()

    @cached_property
    def _bolster(self) -> str:
        return Bolster(self.mod).add_bolster()

    @cached_property
    def _empowered_spells(self) -> str:
        return EmpoweredSpells(self.mod).add_empowered_spells(CharacterAbility.CHARISMA)

    @cached_property
    def _electrostatic_generator(self) -> str:
        name = f"{self.mod.get_prefix()}_ElectrostaticGenerator"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Electrostatic Generator"}
        loca[f"{name}_Description"] = {"en": """
            Every turn while in combat, you generate [1]
            <LSTag Type="Status" Tooltip="MAG_CHARGED_LIGHTNING">Lightning Charges</LSTag>.
        """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["2"],
            Icon="statIcons_LightningCharge",
            Properties=["Highlighted", "OncePerTurn"],
            StatsFunctorContext=["OnTurn"],
            Conditions=["Combat()"],
            StatsFunctors=[
                "IF(not HasStatus('MAG_CHARGED_LIGHTNING',context.Source)):" +
                    "ApplyStatus(SELF,MAG_CHARGED_LIGHTNING_LIGHTNING_DAMAGE_ONCE_TECHNICAL,100,0)",
                "ApplyStatus(MAG_CHARGED_LIGHTNING_GENERATE_CHARGE_FX,100,0)",
                "IF(not IsDischargingLightning(context.Source)):ApplyStatus(MAG_CHARGED_LIGHTNING,100,2)",
                "ApplyStatus(MAG_CHARGED_LIGHTNING_DURATION_TECHNICAL,100,1)",
            ],
        ))

        return name

    @cached_property
    def _wintry_mix(self) -> str:
        name = f"{self.mod.get_prefix()}_WintryMix"

        loca = self.mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Wintry Mix"}
        loca[f"{name}_Description"] = {"en": """
            When you deal Cold damage, you inflict [1] turns of <LSTag Type="Status" Tooltip="WET">Wet</LSTag> on the
            target.
        """}

        self.mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            DescriptionParams=["3"],
            Icon="Spell_Conjuration_SleetStorm",
            Properties=["Highlighted"],
            StatsFunctorContext=["OnDamage"],
            Conditions=["IsDamageTypeCold()"],
            StatsFunctors=["ApplyStatus(WET,100,3)"],
        ))

        return name

    @cached_property
    def _spelllist_level_1(self) -> str:
        name = f"{self.mod.get_prefix()} level 1 spells"
        uuid = self.make_uuid(name)
        self.mod.add(SpellList(
            Name=name,
            Spells=[
                "Shout_ArmorOfAgathys",
                self._bolster,
                "Target_BoomingBlade",
                "Projectile_RayOfFrost",
                "Target_ShockingGrasp",
            ],
            UUID=uuid,
        ))
        return uuid

    @class_description(CharacterClass.SORCERER)
    @class_description(CharacterClass.SORCERER_DRACONIC)
    @class_description(CharacterClass.SORCERER_SHADOWMAGIC)
    @class_description(CharacterClass.SORCERER_STORM)
    @class_description(CharacterClass.SORCERER_WILDMAGIC)
    def sorcerer_can_learn_spells(self, desc: ClassDescription) -> None:
        desc.CanLearnSpells = True
        desc.MustPrepareSpells = True

    @class_description(CharacterClass.SORCERER_STORM)
    def stormsorcery_equipment(self, desc: ClassDescription) -> None:
        desc.ClassEquipment = self._equipment

    @progression(CharacterClass.SORCERER, range(1, 21))
    @progression(CharacterClass.SORCERER, 1, is_multiclass=True)
    @progression(CharacterClass.SORCERER_DRACONIC, range(1, 21))
    @progression(CharacterClass.SORCERER_SHADOWMAGIC, range(1, 21))
    @progression(CharacterClass.SORCERER_STORM, range(1, 21))
    @progression(CharacterClass.SORCERER_WILDMAGIC, range(1, 21))
    def sorcerer_spells_always_prepared(self, progress: Progression) -> None:
        if not spells_always_prepared(progress):
            raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 1)
    def stormsorcery_level_1(self, progress: Progression) -> None:
        progress.PassivesAdded = [
            self._battle_magic,
            self._electrostatic_generator,
            self._wintry_mix,
        ]
        progress.Selectors = [
            f"AddSpells({self._spelllist_level_1},,,,AlwaysPrepared)",
            "AddSpells(12150e11-267a-4ecc-a3cc-292c9e2a198d,,,,AlwaysPrepared)",  # Fly
        ]

    @progression(CharacterClass.SORCERER_STORM, 2)
    def stormsorcery_level_2(self, progress: Progression) -> None:
        progress.PassivesAdded = ["JackOfAllTrades", "SculptSpells"]
        progress.Selectors = [
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,4)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ]

    @progression(CharacterClass.SORCERER_STORM, 3)
    def stormsorcery_level_3(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 4)
    def stormsorcery_level_4(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 5)
    def stormsorcery_level_5(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack"]

    @progression(CharacterClass.SORCERER_STORM, 6)
    def stormsorcery_level_6(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 7)
    def stormsorcery_level_7(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 8)
    def stormsorcery_level_8(self, progress: Progression) -> None:
        progress.PassivesAdded = [self._empowered_spells]

    @progression(CharacterClass.SORCERER_STORM, 9)
    def stormsorcery_level_9(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 10)
    def stormsorcery_level_10(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 11)
    def stormsorcery_level_11(self, progress: Progression) -> None:
        progress.PassivesAdded += ["ExtraAttack_2"]
        progress.PassivesRemoved = ["ExtraAttack"]

    @progression(CharacterClass.SORCERER_STORM, 12)
    def stormsorcery_level_12(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 13)
    def stormsorcery_level_13(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 14)
    def stormsorcery_level_14(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 15)
    def stormsorcery_level_15(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 16)
    def stormsorcery_level_16(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 17)
    def stormsorcery_level_17(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 18)
    def stormsorcery_level_18(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 19)
    def stormsorcery_level_19(self, _: Progression) -> None:
        raise DontIncludeProgression()

    @progression(CharacterClass.SORCERER_STORM, 20)
    def stormsorcery_level_20(self, progress: Progression) -> None:
        progress.PassivesAdded = ["ExtraAttack_3"]
        progress.PassivesRemoved = ["ExtraAttack_2"]


def main() -> None:
    storm_sorcery = StormSorcery(
        classes=[CharacterClass.SORCERER_STORM],
        feats=2,
        spells=2,
        warlock_spells=2,
        actions=2,
    )
    storm_sorcery.build()


if __name__ == "__main__":
    main()
