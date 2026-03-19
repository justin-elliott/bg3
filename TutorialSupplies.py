#!/usr/bin/env python3

from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar, Iterable
from uuid import UUID

from moddb import (
    Awareness,
    Bolster,
    ElementalWeapon,
    Knowledge,
    storm_bolts,
)
from modtools.gamedata import (
    Armor,
    ObjectData,
    PassiveData,
    SpellData,
    StatusData,
    Weapon,
)
from modtools.lsx.game import GameObjects
from modtools.replacers import Mod
from modtools.text import ItemCombinations, TreasureTable

import os


class TutorialSupplies(Mod):
    __KATANA_TEMPLATE_ID: ClassVar[UUID] = UUID("7050c02e-f0e1-46b8-9400-2514805ecd2e")

    @dataclass
    class TreasureChest:
        name: str
        display_name: str
        description: str
        items: list[str]

    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="TutorialSupplies",
                         description="Supplies for the tutorial chest.",
                         **kwds)

        self._add_treasure_chests([
            self._camp_clothing,
            self._camp_shoes,
            self._underwear,
            self._daisy,
            self._potions,
            self._dyes,
            self._armor,
            self._weapons,
            self._abazigals_goods,
        ])

        self._update_helmet_of_arcane_acuity()

    def _reduce_weight(self, armor: list[str]) -> list[str]:
        for item in armor:
            self.add(Armor(
                item,
                using=item,
                Weight="0.1",
            ))
        return armor

    @cached_property
    def _camp_clothing(self) -> TreasureChest:
        return self.TreasureChest(
            name="CampClothing",
            display_name="Camp Clothing",
            description="Contains a selection of camp clothing.",
            items=self._reduce_weight([
                "ARM_Camp_Body_Astarion",
                "ARM_Camp_Body_Gale",
                "ARM_Camp_Body_Halsin",
                "ARM_Camp_Body_Jaheira",
                "ARM_Camp_Body_Karlach",
                "ARM_Camp_Body_Laezel",
                "ARM_Camp_Body_Minsc",
                "ARM_Camp_Body_Minthara",
                "ARM_Camp_Body_Shadowheart",
                "ARM_Camp_Body_Wyll",
                "CampClothes_DaisyBody",
                "ARM_Vanity_Body_Aristocrat_Brown",
                "ARM_Vanity_Body_Aristocrat_White",
                "ARM_Vanity_Body_Aristocrat",
                "ARM_Vanity_Body_Circus_B",
                "ARM_Vanity_Body_Circus",
                "ARM_Vanity_Body_Citizen_B_Teal",
                "ARM_Vanity_Body_Citizen_B",
                "ARM_Vanity_Body_Citizen_Black",
                "ARM_Vanity_Body_Citizen_C_Blue",
                "ARM_Vanity_Body_Citizen_C_Green",
                "ARM_Vanity_Body_Citizen_C_Red",
                "ARM_Vanity_Body_Citizen_C",
                "ARM_Vanity_Body_Citizen_Purple",
                "ARM_Vanity_Body_Citizen",
                "ARM_Vanity_Body_Cultist",
                "ARM_Vanity_Body_Deva",
                "ARM_Vanity_Body_Drow",
                "ARM_Vanity_Body_Leather_Black",
                "ARM_Vanity_Body_Leather_Bright",
                "ARM_Vanity_Body_Leather_Rich_Blue",
                "ARM_Vanity_Body_Leather_Rich_Green",
                "ARM_Vanity_Body_Leather_Rich",
                "ARM_Vanity_Body_Leather",
                "ARM_Vanity_Body_Pants",
                "ARM_Vanity_Body_Patriars_Black",
                "ARM_Vanity_Body_Patriars_Blue",
                "ARM_Vanity_Body_Patriars_Green",
                "ARM_Vanity_Body_Patriars_Red",
                "ARM_Vanity_Body_Patriars",
                "ARM_Vanity_Body_Prison",
                "ARM_Vanity_Body_Refugee_Gray",
                "ARM_Vanity_Body_Refugee_Green",
                "ARM_Vanity_Body_Refugee",
                "ARM_Vanity_Body_Rich_B_Purple",
                "ARM_Vanity_Body_Rich_B",
                "ARM_Vanity_Body_Rich_B1_Beige",
                "ARM_Vanity_Body_Rich_B1",
                "ARM_Vanity_Body_Rich_C_Blue",
                "ARM_Vanity_Body_Rich_C_Red",
                "ARM_Vanity_Body_Rich_C",
                "ARM_Vanity_Body_Rich_D_Blue",
                "ARM_Vanity_Body_Rich_D_Green",
                "ARM_Vanity_Body_Rich_D_Purple",
                "ARM_Vanity_Body_Rich_D_White",
                "ARM_Vanity_Body_Rich_D",
                "ARM_Vanity_Body_Rich_E_GreenPink",
                "ARM_Vanity_Body_Rich_E_Teal",
                "ARM_Vanity_Body_Rich_E",
                "ARM_Vanity_Body_Rich_F_Blue",
                "ARM_Vanity_Body_Rich_F",
                "ARM_Vanity_Body_Rich_G_Black",
                "ARM_Vanity_Body_Rich_G_Bright",
                "ARM_Vanity_Body_Rich_G_Brown",
                "ARM_Vanity_Body_Rich_G_Red",
                "ARM_Vanity_Body_Rich_G",
                "ARM_Vanity_Body_Rich_G2_Blue",
                "ARM_Vanity_Body_Rich_G2_Green",
                "ARM_Vanity_Body_Rich_G2_Purple",
                "ARM_Vanity_Body_Rich_G2_White",
                "ARM_Vanity_Body_Rich_G2",
                "ARM_Vanity_Body_Rich_Gold",
                "ARM_Vanity_Body_Rich_Green",
                "ARM_Vanity_Body_Rich_Teal",
                "ARM_Vanity_Body_Rich",
                "ARM_Vanity_Body_Shar",
                "ARM_Vanity_Body_Shirt_Black",
                "ARM_Vanity_Body_Shirt_Blue",
                "ARM_Vanity_Body_Shirt_Green",
                "ARM_Vanity_Body_Shirt_Purple",
                "ARM_Vanity_Body_Shirt_Red",
                "ARM_Vanity_ElegantRobe",
                "ARM_Vanity_Prison_Poor",
            ]),
        )

    @cached_property
    def _camp_shoes(self) -> TreasureChest:
        return self.TreasureChest(
            name="CampShoes",
            display_name="Camp Shoes",
            description="Contains a selection of camp shoes.",
            items=self._reduce_weight([
                "ARM_Camp_Sandals_A1_Black",
                "ARM_Camp_Sandals_A1",
                "ARM_Camp_Sandals_B_Red",
                "ARM_Camp_Sandals_B",
                "ARM_Camp_Sandals_Blue",
                "ARM_Camp_Sandals_C",
                "ARM_Camp_Sandals",
                "ARM_Camp_Shoes_B",
                "ARM_Camp_Shoes_C",
                "ARM_Camp_Shoes_E",
                "ARM_Camp_Shoes_F",
                "ARM_Camp_Shoes",
                "ARM_Camp_Shoes_Astarion",
                "ARM_Camp_Shoes_Gale",
                "ARM_Camp_Shoes_Halsin",
                "ARM_Camp_Shoes_Jaheira",
                "ARM_Camp_Shoes_Karlach",
                "ARM_Camp_Shoes_Laezel",
                "ARM_Camp_Shoes_Minsc",
                "ARM_Camp_Shoes_Minthara",
                "ARM_Camp_Shoes_Shadowheart",
                "ARM_Camp_Shoes_Wyll",
                "ARM_Vanity_Deva_Shoes",
                "ARM_Vanity_Shoes_Circus",
            ]) + [
                self._comfortable_boots,
            ],
        )

    @cached_property
    def _underwear(self) -> TreasureChest:
        return self.TreasureChest(
            name="Underwear",
            display_name="Underwear",
            description="Contains a selection of underwear.",
            items=[
                "ARM_Underwear_Dragonborn_Bronze",
                "ARM_Underwear_Dragonborn",
                "ARM_Underwear_Dwarves_Green",
                "ARM_Underwear_Dwarves",
                "ARM_Underwear_Elves_Blue",
                "ARM_Underwear_Elves_Purple",
                "ARM_Underwear_Elves",
                "ARM_Underwear_Githyanki_Black",
                "ARM_Underwear_Githyanki",
                "ARM_Underwear_Gnomes_Blue",
                "ARM_Underwear_Gnomes",
                "ARM_Underwear_Halflings",
                "ARM_Underwear_HalfOrcs_Orange",
                "ARM_Underwear_HalfOrcs",
                "ARM_Underwear_Humans_B",
                "ARM_Underwear_Humans_C",
                "ARM_Underwear_Humans",
                "ARM_Underwear_Incubus",
                "ARM_Underwear_Tieflings",
                "ARM_Underwear_Astarion",
                "ARM_Underwear_Gale",
                "ARM_Underwear_Halsin",
                "ARM_Underwear_Jaheira",
                "ARM_Underwear_Karlach",
                "ARM_Underwear_Laezel",
                "ARM_Underwear_Minsc",
                "ARM_Underwear_Minthara",
                "ARM_Underwear_Shadowheart",
                "ARM_Underwear_Wyll",
            ],
        )

    @cached_property
    def _daisy(self) -> TreasureChest:
        return self.TreasureChest(
            name="Daisy",
            display_name="Dream Guardian Armour",
            description="Contains a selection of Dream Guardian armour.",
            items=[
                self._daisy_body,
                self._daisy_gloves,
                self._daisy_boots,
                "UNI_DaisyPlaysuit",
                "UNI_Daisy_Gloves",
            ],
        )
    @cached_property
    def _potions(self) -> TreasureChest:
        return self.TreasureChest(
            name="Potions",
            display_name="Potions",
            description="Contains a selection of potions.",
            items=[
                self._awareness_potion,
                self._bolster_potion,
                self._elemental_weapon_potion,
                self._knowledge_potion,
                self._flying_potion,
                self._overpowering_potion,
                self._splinters_of_frost_potion,
                self._storm_bolts_potion,
            ],
        )

    @cached_property
    def _dyes(self) -> TreasureChest:
        base_dyes = [
            ("OBJ_Dye_Azure", "85fc7553-b1ca-cb0c-600c-2d0a1fb4c06c"),
            ("OBJ_Dye_BlackBlue", "3a87940e-c9a2-494c-0026-a94a2087e128"),
            ("OBJ_Dye_BlackGreen", "88d7c30f-c736-cc70-d005-d1169f73a58f"),
            ("OBJ_Dye_BlackPink", "cfada95a-0ef4-0e97-5330-42fff41a7cbe"),
            ("OBJ_Dye_BlackRed", "59e211f9-38bf-2013-a66b-27f075a7a057"),
            ("OBJ_Dye_BlackTeal", "5f97bbfc-7dca-37b4-0285-768fd66f11e8"),
            ("OBJ_Dye_Blue", "5bf267b7-cbba-02f6-64f1-6b7600b6d641"),
            ("OBJ_Dye_BlueGreen", "9b822fd0-36ea-d24f-efff-f24e2b1c78c7"),
            ("OBJ_Dye_BluePurple", "854e37e1-a840-ac3f-948b-a6630187d3e7"),
            ("OBJ_Dye_BlueYellow", "ddc1e83b-8727-7900-94bc-72dc6e78d89a"),
            ("OBJ_Dye_BlueYellow_02", "9d88e168-e638-65fa-feb3-9573ba3e3608"),
            ("OBJ_Dye_Golden", "4157e913-f20d-037e-db5c-33a38d2b1e81"),
            ("OBJ_Dye_Green", "a8690bc5-9f17-5672-28e2-41c1ab3018ea"),
            ("OBJ_Dye_Green_02", "ea44dc42-196e-5bbf-56e3-10fe5a21eb82"),
            ("OBJ_Dye_GreenSage", "a9895745-150c-5621-bc1a-c05ea59224e1"),
            ("OBJ_Dye_GreenSwamp", "7922733b-ebb1-1d40-2e5d-f68a1a450571"),
            ("OBJ_Dye_GreenPink", "84b1e032-4013-a304-5e1b-867c4c07fc72"),
            ("OBJ_Dye_IceCream", "baf0cd87-d867-0e2a-570f-67162f0c242b"),
            ("OBJ_Dye_IceCream_02", "428e99ed-6fd8-c81a-d856-be32f8d2df84"),
            ("OBJ_Dye_IceCream_03", "7c32bee2-2804-ba2f-9421-479fb068dd74"),
            ("OBJ_Dye_IceCream_04", "16febc6c-1fb8-970f-9d3d-73ab5bc3dc73"),
            ("OBJ_Dye_Maroon", "1cdd0db3-f51e-b310-1cf8-06b05ae6213b"),
            ("OBJ_Dye_Ocean", "8b2bc234-5b59-1dac-ad0b-981dcaadf1f8"),
            ("OBJ_Dye_Orange", "d5c2b4ee-0d01-35c4-efe1-97a590cf1b33"),
            ("OBJ_Dye_OrangeBlue", "81347759-e898-e086-4e85-8ff9b006f3de"),
            ("OBJ_Dye_Pink", "dcda84b0-4981-90a0-0372-626285920845"),
            ("OBJ_Dye_Purple", "27e27bb5-ec6d-f79d-6144-ab19625f99ee"),
            ("OBJ_Dye_Purple_02", "323abe30-af8f-38b1-a0bd-bdbf1f30a4ac"),
            ("OBJ_Dye_Purple_03", "3973c28b-e2ce-0fe6-0548-d8e9157a4b0e"),
            ("OBJ_Dye_Purple_04", "7c8ae356-9720-d6b2-02e6-70479f45adec"),
            ("OBJ_Dye_PurpleRed", "cca868e6-4720-6a07-8db7-1c117564e4e4"),
            ("OBJ_Dye_Red", "980bdb9c-b9d0-5c57-8b9b-e4ac0db125ec"),
            ("OBJ_Dye_RedBrown", "86668c08-3811-9f97-1a82-a7a2bc3da66d"),
            ("OBJ_Dye_RedWhite", "ef743f2d-2d6c-74a9-c1e7-8f477269e6be"),
            ("OBJ_Dye_RichRed", "51d9244b-3f97-a169-63bb-cd5773dfc47a"),
            ("OBJ_Dye_RoyalBlue", "25f9b6dc-e7ab-ac6a-1d5a-529d02a36358"),
            ("OBJ_Dye_Teal", "8b78d035-f64f-5e03-9fa9-ec44a3dc7832"),
            ("OBJ_Dye_WhiteBlack", "455c4b21-4cda-3fec-7425-a557d140b972"),
            ("OBJ_Dye_WhiteBrown", "612865e1-ac2c-30b7-dc50-207c95d3901f"),
            ("OBJ_Dye_WhiteRed", "33f7e7b9-7e66-7893-b18f-e080f39fe3e3"),
            ("DLC_OBJ_Dye_Larian", "68d055b3-c3df-ab42-857d-cfe747e4a85b"),
            ("OBJ_Dye_Remover", None),
        ]

        def item_combination(name: str, object_name: str, dye_resource: str | None) -> None:
            self.add(ItemCombinations(f"""
                new ItemCombination "{name}"
                data "Type 1" "Object"
                data "Object 1" "{object_name}"
                data "Transform 1" "None"
                data "Type 2" "Category"
                data "Object 2" "DyableArmor"
                data "Transform 2" "Dye"
                {f'data "DyeColorPresetResource" "{dye_resource}"\n' if dye_resource else ''}
                new ItemCombinationResult "{name}_1"
                data "ResultAmount 1" "1"
            """))

        for dye, dye_resource in base_dyes:
            item_combination(dye, dye, dye_resource)
        
        # The Drake General dye is a special case where the name and object name do not match.
        item_combination("OBJ_Dye_DLC_Larian", "DLC_OBJ_Dye_Larian", "68d055b3-c3df-ab42-857d-cfe747e4a85b")
    
        return self.TreasureChest(
            name="Dyes",
            display_name="Dyes",
            description="Contains a selection of dyes.",
            items=[dye for dye, _ in base_dyes],
        )

    @cached_property
    def _awareness(self) -> str:
        return Awareness(self).add_awareness()

    @cached_property
    def _awareness_potion(self) -> str:
        return self._add_potion(
            "AwarenessPotion",
            display_name="Elixir of Awareness",
            description=f"""
                Drinking this elixir grants <LSTag Type="Passive" Tooltip="{self._awareness}">Awareness</LSTag>.
            """,
            icon="Item_ALCH_Solution_Potion_FeatherFall",
            passives=[self._awareness],
        )

    @cached_property
    def _bolster(self) -> str:
        return Bolster(self).add_bolster()

    @cached_property
    def _bolster_potion(self) -> str:
        return self._add_potion(
            "BolsterPotion",
            display_name="Elixir of Bolstering",
            description=f"""
                Drinking this elixir grants the <LSTag Type="Spell" Tooltip="{self._bolster}">Bolster</LSTag> spell.
            """,
            icon="Item_CONS_Drink_Potion_B",
            boosts=[f"UnlockSpell({self._bolster})"],
        )
    
    @cached_property
    def _elemental_weapon(self) -> str:
        return ElementalWeapon(self).add_elemental_weapon()

    @cached_property
    def _elemental_weapon_potion(self) -> str:
        return self._add_potion(
            "ElementalWeaponPotion",
            display_name="Elixir of Elemental Weaponry",
            description=f"""
                Drinking this elixir grants the
                <LSTag Type="Spell" Tooltip="{self._elemental_weapon}">Elemental Weapon</LSTag> spell.
            """,
            icon="Item_CONS_Potion_FireBreath_A",
            boosts=[f"UnlockSpell({self._elemental_weapon})"],
        )
    
    @cached_property
    def _flying_potion(self) -> str:
        return self._add_potion(
            "FlyingPotion",
            display_name="Elixir of Flying",
            description="""
                Drinking this elixir grants <LSTag Type="Spell" Tooltip="Projectile_Fly">Fly</LSTag>.
            """,
            icon="Item_ALCH_Solution_Potion_Flying",
            boosts=["UnlockSpell(Projectile_Fly)"],
        )

    @cached_property
    def _knowledge_potion(self) -> str:
        return self._add_potion(
            "KnowledgePotion",
            display_name="Elixir of Knowledge",
            description=f"""
                Drinking this elixir grants
                <LSTag Type="Spell" Tooltip="{self._knowledge_of_the_ages}">Knowledge of the Ages</LSTag>, and
                <LSTag Type="Passive" Tooltip="JackOfAllTrades">Jack of All Trades</LSTag>.
            """,
            icon="Item_CONS_Potion_Invulnerability",
            boosts=[f"UnlockSpell({self._knowledge_of_the_ages})"],
            passives=["JackOfAllTrades"],
        )
    
    @cached_property
    def _overpowering_potion(self) -> str:
        return self._add_potion(
        "OverpoweringPotion",
        display_name="Potion of Overpowering",
        description="""
            Temporarily gain a significant boost to your strength, health, armor class, attack rolls, damage rolls, and
            saving throws.
        """,
        icon="Item_CONS_Drug_Dreammist_A",
        status_duration=10,
        boosts=[
            "AbilityOverrideMinimum(Strength,30)",
            "AC(20)",
            "DamageBonus(200)",
            "IncreaseMaxHP(50)",
            "Initiative(10)",
            "RollBonus(Attack,20)",
            "RollBonus(SavingThrow,20)",
            "SpellSaveDC(20)",
            "IgnoreResistance(Bludgeoning,Resistant)",
            "IgnoreResistance(Piercing,Resistant)",
            "IgnoreResistance(Slashing,Resistant)",
            "CriticalHit(AttackTarget,Success,Never)",
        ],
        status_property_flags=[],
    )

    @cached_property
    def _splinters_of_frost_potion(self) -> str:
        return self._add_potion(
            "SplintersOfFrostPotion",
            display_name="Potion of Splinters of Frost",
            description=f"""
                Drinking this elixir grants the
                <LSTag Type="Spell" Tooltip="{self._splinters_of_frost}">Splinters of Frost</LSTag> cantrip.
            """,
            icon="Item_LOOT_Alchemy_Myconid_Grenade_Water",
            boosts=[f"UnlockSpell({self._splinters_of_frost})"],
        )

    @cached_property
    def _storm_bolts_potion(self) -> str:
        storm_bolts_spell = storm_bolts(self)
        return self._add_potion(
            "StormBoltsPotion",
            display_name="Potion of Storm Bolts",
            description=f"""
                Drinking this elixir grants the
                <LSTag Type="Spell" Tooltip="{storm_bolts_spell}">Storm Bolts</LSTag> cantrip.
            """,
            icon="Item_ALCH_Solution_Grenade_Light_2",
            boosts=[f"UnlockSpell({storm_bolts_spell})"],
        )

    @cached_property
    def _knowledge_of_the_ages(self) -> str:
        return Knowledge(self).add_knowledge_of_the_ages()

    def _add_treasure_chests(self, chests: Iterable[TreasureChest]) -> None:
        """Add treasure chests to the tutorial chest."""
        tutorial_chest_entries = []
        treasure_tables = []

        for chest in chests:
            name = self.make_name(chest.name)
            chest_uuid = self.make_uuid(name)

            self._add_chest_game_object(name, chest_uuid, chest.display_name, chest.description)
            self._add_chest_container(name, chest_uuid)

            tutorial_chest_entries += [f"""\
                new subtable "1,1"
                object category "I_{name}",1,0,0,0,0,0,0,0
            """]
            treasure_table_items = [f"""\
                new subtable "1,1"
                object category "I_{item}",1,0,0,0,0,0,0,0
            """ for item in chest.items]
            treasure_tables += [f"""\
                new treasuretable "{name}_TreasureTable"
                CanMerge 1
                {"".join(treasure_table_items)}
            """]
        
        self.add(TreasureTable("\n".join(line.lstrip() for line in
            f"""\
                new treasuretable "TUT_Chest_Potions"
                CanMerge 1
                new subtable "10000,1"
                object category "Gold",1,0,0,0,0,0,0,0
                {"".join(tutorial_chest_entries)}
                {"".join(treasure_tables)}
            """.splitlines())))
    
    def _add_chest_game_object(self,
                               name: str,
                               chest_uuid: UUID,
                               display_name: str | dict[str, str],
                               description: str | dict[str, str]) -> None:
        self.loca[f"{name}_DisplayName"] = display_name
        self.loca[f"{name}_Description"] = description

        self.add(GameObjects(
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Icon="Item_CONT_GEN_Chest_Travel_A_Small_A",
            LevelName="",
            MapKey=chest_uuid,
            Name=name,
            ParentTemplateId="47805d79-88f1-4933-86eb-f78f67cbc33f",
            Stats=name,
            Type="item",
            children=[
                GameObjects.InventoryList(children=[
                    GameObjects.InventoryList.InventoryItem(
                        Object=f"{name}_TreasureTable",
                    ),
                ]),
            ],
        ))
    
    def _add_chest_container(self, name: str, chest_uuid: UUID) -> None:
        self.add(ObjectData(
            name,
            using="_Container",
            RootTemplate=chest_uuid,
            Weight=0.01,
        ))
    
    def _add_potion(
            self,
            short_name: str,
            *,
            display_name: str | dict[str, str],
            description: str | dict[str, str],
            icon: str,
            status_duration: int = -1,
            boosts: list[str] = None,
            on_apply_functors: list[str] = None,
            on_remove_functors: list[str] = None,
            passives: list[str] = None,
            stack_id: str = None,
            stack_type: str = None,
            status_property_flags: list[str] = None,
            tick_type: str = None) -> str:
        name = self.make_name(short_name)
        uuid = self.make_uuid(name)

        self.loca[f"{name}_DisplayName"] = display_name
        self.loca[f"{name}_Description"] = description

        self.add(GameObjects(
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Flag_int32=0,
            Icon=icon,
            LevelName="",
            MapKey=uuid,
            Name=name,
            OnUseDescription=("hc857245cg5f9dg4f90g88d4g604f596d85ca", 1),
            ParentTemplateId="8e660fd9-489d-42ff-a762-e4392e826666",
            Stats=name,
            Type="item",
            VisualTemplate="a93bcc13-e31b-f6a6-7076-e64fe7771d9e",
            children=[
                GameObjects.Bounds(children=[
                    GameObjects.Bounds.Bound(
                        Height=0.418184,
                        Max="0.21 0.62 0.2",
                        Min="-0.21 0 -0.2",
                        Radius=0.114147,
                        Shape=1,
                        Type=1,
                    ),
                    GameObjects.Bounds.Bound(
                        Height=0.418184,
                        Max="0.21 0.62 0.2",
                        Min="-0.21 0 -0.2",
                        Radius=0.114147,
                        Shape=1,
                        Type=2,
                    ),
                    GameObjects.Bounds.Bound(
                        Height=0.418184,
                        Max="0.21 0.62 0.2",
                        Min="-0.21 0 -0.2",
                        Radius=0.114147,
                        Shape=1,
                        Type=0,
                    ),
                ]),
                GameObjects.InventoryList(),
                GameObjects.OnDestroyActions(children=[
                    GameObjects.OnDestroyActions.Action(
                        ActionType=26,
                        children=[
                            GameObjects.OnDestroyActions.Action.Attributes(
                                ActivateSoundEvent="3ea82655-5140-4287-9ab8-794559f182d3",
                                Animation="",
                                Conditions="",
                                PlayOnHUD=False,
                            ),
                        ],
                    ),
                    GameObjects.OnDestroyActions.Action(
                        ActionType=5,
                        children=[
                            GameObjects.OnDestroyActions.Action.Attributes(
                                Animation="",
                                Conditions="",
                                ExplodeFX="df744de3-fb7f-4808-6881-fd466107d27f",
                                FadeOutDelay=0,
                                FadeOutFX="",
                                SnapToGround=True,
                                TargetItemState=0,
                                VisualWithDynamicPhysics="",
                                templateAfterDestruction="",
                                visualDestruction="00000000-0000-0000-0000-000000000000",
                            ),
                        ],
                    ),
                ]),
                GameObjects.OnUsePeaceActions(children=[
                    GameObjects.OnUsePeaceActions.Action(
                        ActionType=7,
                        children=[
                            GameObjects.OnUsePeaceActions.Action.Attributes(
                                Animation="",
                                Conditions="",
                                Consume=False,
                                IsHiddenStatus=True,
                                StatsId=name.upper(),
                                StatusDuration=status_duration,
                            ),
                        ],
                    ),
                ]),
            ],
        ))

        self.add(ObjectData(
            name,
            using=self._base_potion,
            RootTemplate=uuid,
        ))

        if status_property_flags is None:
            status_property_flags = [
                "DisableOverhead",
                "IgnoreResting",
                "DisableCombatlog",
                "DisablePortraitIndicator",
            ]

        self.add(StatusData(
            name.upper(),
            StatusType="BOOST",
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Icon=icon,
            Boosts=boosts,
            OnApplyFunctors=on_apply_functors,
            OnRemoveFunctors=on_remove_functors,
            Passives=passives,
            StackId=name.upper() if stack_id is None else stack_id,
            StackType=stack_type,
            StatusPropertyFlags=status_property_flags,
            TickType=tick_type,
        ))

        return name

    @cached_property
    def _base_potion(self) -> str:
        name = self.make_name("BasePotion")
        self.add(ObjectData(
            name,
            using="OBJ_Bottle",
            ValueUUID="4c5217d8-0232-4592-9e32-2fd729123f53",
            ValueOverride="3",
            Rarity="Legendary",
            ObjectCategory="",
        ))
        return name

    @cached_property
    def _comfortable_boots(self) -> str:
        name = self.make_name("ComfortableBoots")
        uuid = self.make_uuid(name)

        loca = self.get_localization()
        loca[f"{name}_DisplayName"] = "Comfortable Boots"
        loca[f"{name}_Description"] = """
            Made of soft, sheepskin-lined leather, these are the perfect boots to wear around the campfire on a chilly
            night.
            """

        self.add(GameObjects(
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            LevelName="",
            MapKey=uuid,
            Name=name,
            ParentTemplateId="cf987856-1381-477e-88db-6b359f7e19e8",
            Stats=name,
            Type="item",
        ))

        self.add(Armor(
            name,
            using="ARM_Camp_Shoes",
            RootTemplate=uuid,
            Weight="0.1",
        ))

        return name
    
    @cached_property
    def _daisy_body(self) -> str:
        name = self.make_name("DaisyBody")
        self.add(Armor(
            name,
            using="ARM_Camp_Body",
            RootTemplate="aa0917ea-5f66-4a22-97de-654228484128",
        ))
        return name

    @cached_property
    def _daisy_boots(self) -> str:
        name = self.make_name("DaisyBoots")
        self.add(Armor(
            name,
            using="ARM_Camp_Shoes",
            RootTemplate="216f0362-f77b-420c-84cb-d84853aa173d",
        ))
        return name

    @cached_property
    def _daisy_gloves(self) -> str:
        name = self.make_name("DaisyGloves")
        self.add(Armor(
            name,
            using="ARM_Underwear",
            RootTemplate="5a0ee632-9145-48b2-9b92-97c32c2ccbd9",
        ))
        return name

    @cached_property
    def _armor(self) -> TreasureChest:
        return self.TreasureChest(
            name="Armor",
            display_name="Armour",
            description="Contains a selection of armor",
            items=self._reduce_weight([
                "ARM_Robe_FlamingFist",
                "ARM_Leather_FlamingFist",
                "ARM_ScaleMail_FlamingFist",
                "ARM_HalfPlate_FlamingFist",
                "ARM_StuddedLeather_Body",
                "ARM_HalfPlate_Body",
                "ARM_ScaleMail_Body_Paladin_Crown",
                "ARM_Splint_Body",
            ]),
        )

    @cached_property
    def _weapons(self) -> TreasureChest:
        return self.TreasureChest(
            name="Weapons",
            display_name="Weapons",
            description="Contains a selection of weapons.",
            items=[
                self._arcane_rapier,
                self._blade_of_the_banshee,
                self._radiant_silver_sword,
                self._sword_of_storms,
            ],
        )

    @cached_property
    def _lightning_weapon(self) -> str:
        name = self.make_name("Lightning_Weapon").upper()
        self.loca[f"{name}_DisplayName"] = "Lightning Weapon"
        self.loca[f"{name}_Description"] = "Lightning arcs along the length of the weapon"
        self.add(StatusData(
            name,
            StatusType="BOOST",
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Icon="statIcons_LightningCharge",
            Boosts=["WeaponDamage(1d4,Lightning)"],
            StackId=name,
            StackPriority=10,
            StatusEffectOverrideForItems="7905bb82-0284-46b8-855b-24f17560fe4a",
            StatusPropertyFlags=["DisableOverhead", "IgnoreResting", "DisableCombatlog", "DisablePortraitIndicator"],
        ))
        return name

    @cached_property
    def _sword_of_storms(self) -> str:
        return self._add_adamantine_weapon(
            "SwordOfStorms",
            parent_template_id=self.__KATANA_TEMPLATE_ID,
            display_name="Sword of Storms",
            description="""
                Forged from gleaming silver, this elegant sword constantly pulses with jagged arcs of blue electricity
                and hums with the low rumble of distant thunder.
            """,
            extra_passives_on_equip=[
                "MAG_ChargedLightning_Charge_OnSpellDamage_Passive",
                self._weapon_enchantment,
                self._weapon_kereskas_favour,
            ],
            extra_weapon_statuses=[self._lightning_weapon],
            status_on_equip=["MAG_THE_CHROMATIC_TECHNICAL"],
            ignore_slashing_resistance=False,
            proficiency_group="",
        )

    @cached_property
    def _radiant_silver_sword(self) -> str:
        voss_silver_sword_template_id = UUID("20c66f8d-f455-42fc-8e48-543512247e75")
        return self._add_adamantine_weapon(
            "RadiantSilverSword",
            parent_template_id=voss_silver_sword_template_id,
            display_name="Radiant Silver Sword",
            description="""
                This heavy silver sword pulses with a gentle light.
            """,
            bonus_damage_type="Radiant",
            extra_boosts_on_equip_main_hand=["UnlockSpell(Target_MAG_WeaponAction_FlashingDawn)"],
            extra_passives_on_equip=["MAG_Radiant_RadiatingOrb_Melee_OnDamage_Passive"],
        )

    def _add_adamantine_weapon(
            self,
            base_name: str,
            *,
            parent_template_id: UUID,
            display_name: str,
            description: str,
            using: str | None = None,
            bonus_damage: str | None = None,
            bonus_damage_type: str | None = None,
            boosts: list[str] | None = None,
            extra_boosts_on_equip_main_hand: list[str] | None = None,
            extra_passives_on_equip: list[str] | None = None,
            extra_weapon_statuses: list[str] | None = None,
            ignore_bludgeoning_resistance: bool = False,
            ignore_piercing_resistance: bool = False,
            ignore_slashing_resistance: bool = True,
            critical_vs_items: bool = False,
            proficiency_group: str | None = None,
            status_on_equip: list[str] | None = None,
            weapon_functors: list[str] | None = None) -> str:
        return self._add_weapon(
            base_name,
            parent_template_id=parent_template_id,
            display_name=display_name,
            description=description,
            using=using,
            bonus_damage=bonus_damage or ("1d4" if bonus_damage_type else None),
            bonus_damage_type=bonus_damage_type,
            boosts=boosts,
            boosts_on_equip_main_hand=[
                "CannotBeDisarmed()",
                "UnlockSpell(Target_OpeningAttack)",
                "UnlockSpell(Target_Slash_New)",
                "UnlockSpell(Rush_SpringAttack)",
                *(extra_boosts_on_equip_main_hand or []),
            ],
            passives_on_equip=[
                *(["MAG_IgnoreBludgeoningResistance_Passive"] if ignore_bludgeoning_resistance else []),
                *(["MAG_IgnorePiercingResistance_Passive"] if ignore_piercing_resistance else []),
                *(["MAG_IgnoreSlashingResistance_Passive"] if ignore_slashing_resistance else []),
                *(["UNI_Adamantine_CriticalVsItems_Passive"] if critical_vs_items else []),
                *(extra_passives_on_equip or []),
            ],
            proficiency_group=proficiency_group,
            status_on_equip=status_on_equip,
            weapon_functors=weapon_functors,
            weapon_properties=["Dippable", "Finesse", "Magical", "Melee", "Versatile"],
            weapon_statuses=[
                *(["MAG_BYPASS_BLUDGEONING_RESISTANCE_TECHNICAL"] if ignore_bludgeoning_resistance else []),
                *(["MAG_BYPASS_PIERCING_RESISTANCE_TECHNICAL"] if ignore_piercing_resistance else []),
                *(["MAG_BYPASS_SLASHING_RESISTANCE_TECHNICAL"] if ignore_slashing_resistance else []),
                *(["MAG_DIAMONDSBANE_TECHNICAL"] if critical_vs_items else []),
                *(extra_weapon_statuses or []),
            ],
        )

    @cached_property
    def _arcane_rapier(self) -> str:
        und_nere_sword = UUID("df6698d2-b690-4aea-be83-956d3b2ea97e")
        return self._add_weapon(
            base_name="ArcaneRapier",
            using="WPN_Rapier",
            parent_template_id=und_nere_sword,
            display_name="Arcane Rapier",
            description="""
                This slender, elegant rapier features intricate runes etched along its shimmering blade and an ornate
                basket hilt designed to channel and focus raw magical energy.
            """,
            bonus_damage="1d4",
            bonus_damage_type="Force",
            boosts=[self._weapon_kerekas_favour_boost],
            passives_on_equip=[
                "MAG_Critical_Force_Critical_Passive",
                self._weapon_enchantment_progression,
                self._weapon_kereskas_favour,
            ],
            proficiency_group="",
            status_on_equip=["MAG_THE_CHROMATIC_TECHNICAL"],
        )

    @cached_property
    def _blade_of_the_banshee(self) -> str:
        return self._add_weapon(
            "BladeOfTheBanshee",
            using="WPN_Katana",
            parent_template_id=self.__KATANA_TEMPLATE_ID,
            display_name="Blade of the Banshee",
            description="""
                This slender katana possesses a blade that seems to emit a faint, ghostly chill when drawn. Its tsuba is
                carved in the likeness of a weeping woman, and when swung through the air, it emits a low, mournful wail
                that chills the blood of any who hear it.
            """,
            bonus_damage="1d4",
            bonus_damage_type="Psychic",
            boosts=[self._weapon_kerekas_favour_boost],
            passives_on_equip=[
                "MAG_BansheeBless_Passive",
                self._weapon_enchantment_progression,
                self._weapon_kereskas_favour,
                self._life_stealing,
            ],
            status_on_equip=["MAG_THE_CHROMATIC_TECHNICAL"],
            weapon_functors=["ApplyStatus(FRIGHTENED,100,2,,,,not SavingThrow(Ability.Wisdom,12))"],
            weapon_properties=["Dippable", "Finesse", "Magical", "Melee", "Versatile"],
        )

    @cached_property
    def _splinters_of_frost(self) -> str:
        name = self.make_name("SplintersOfFrost")
        status_name = self.make_name("Splinters_of_Frost").upper()
        icon = "Action_Monster_ElementalWater_WintersBreath"
        
        self.loca[f"{name}_DisplayName"] = "Splinters of Frost"
        self.loca[f"{name}_Description"] = """
            Conjure [1] splinter(s) of ice.
            Reduces the target's <LSTag Tooltip="MovementSpeed">movement speed</LSTag> by [2].
        """
        self.add(SpellData(
            name,
            SpellType="Projectile",
            using="Projectile_RayOfFrost",
            AmountOfTargets=["LevelMapValue(EldritchBlast)"],
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            DescriptionParams=["LevelMapValue(EldritchBlast)", "Distance(3)"],
            Icon=icon,
            SpellSuccess=[
                "DealDamage(1d8,Cold,Magical)",
                f"ApplyStatus({status_name},100,1)",
            ],
            TooltipStatusApply=[f"ApplyStatus({status_name},100,1)"],
        ))

        self.add(StatusData(
            status_name,
            StatusType="BOOST",
            using="RAY_OF_FROST",
            DisplayName=self.loca[f"{name}_DisplayName"],
            Icon=icon,
        ))

        return name

    @cached_property
    def _frozen_rapier(self) -> str:
        harmonic_dueller_id = UUID("530a5c21-0f52-428f-bf41-ef33fd6c447b")
        return self._add_weapon(
            base_name="FrozenRapier",
            using="WPN_Rapier",
            parent_template_id=harmonic_dueller_id,
            display_name="Frozen Rapier",
            description="""
                Sculpted from a single shard of perpetually freezing glacial ice, this elegant rapier features a
                needle-sharp blade that shimmers with frost and exhales a deadly chill.
            """,
            bonus_damage="1d4",
            bonus_damage_type="Cold",
            boosts=[f"UnlockSpell({self._splinters_of_frost})"],
            passives_on_equip=[
                "MAG_Cold_IncreaseColdDamageOnCast_Passive",
                "MAG_Cold_ChilledOnSpellDamage_Passive",
            ],
            status_on_equip=["MAG_LEGENDARY_CHROMATIC_ATTUNEMENT_COLD"],
            weapon_statuses=["MAG_FROST_FROST_WEAPON"],
        )

    def _add_weapon(
            self,
            base_name: str,
            *,
            parent_template_id: UUID,
            display_name: str,
            description: str,
            bonus_damage: str | None = None,
            bonus_damage_type: str | None = None,
            using: str | None = None,
            visual_template: str | None = None,
            boosts: list[str] | None = None,
            boosts_on_equip_main_hand: list[str] | None = None,
            boosts_on_equip_off_hand: list[str] | None = None,
            default_boosts: list[str] | None = None,
            passives_on_equip: list[str] | None = None,
            proficiency_group: str | None = None,
            weapon_properties: list[str] | None = None,
            status_on_equip: list[str] | None = None,
            weapon_functors: list[str] | None = None,
            weapon_statuses: list[str] | None = None,
            is_magic: bool = True,
            is_progressive: bool = True,
            is_unique: bool = True) -> None:
        """Add a custom weapon."""
        name = self.make_name(base_name)
        game_objects_uuid = self.make_uuid(name)

        self.add(GameObjects(
            DisplayName=self.loca(f"{name}_DisplayName", display_name),
            Description=self.loca(f"{name}_Description", description),
            LevelName="",
            MapKey=game_objects_uuid,
            Name=name,
            ParentTemplateId=parent_template_id,
            Stats=name,
            Type="item",
            VisualTemplate=visual_template,
            children=[
                GameObjects.StatusList(
                    children=[
                        GameObjects.StatusList.Status(Object=status) for status in (weapon_statuses or [])
                    ],
                ),
            ],
        ))

        self.add(Weapon(
            name,
            using=using or "WPN_Longsword",
            Boosts=boosts,
            BoostsOnEquipMainHand=boosts_on_equip_main_hand,
            BoostsOnEquipOffHand=boosts_on_equip_off_hand,
            DefaultBoosts=[
                *(["WeaponProperty(Magical)"] if is_magic else []),
                *(["IF(CharacterLevelGreaterThan(2) and not CharacterLevelGreaterThan(6)):WeaponEnchantment(1)",
                   "IF(CharacterLevelGreaterThan(6) and not CharacterLevelGreaterThan(10)):WeaponEnchantment(2)",
                   "IF(CharacterLevelGreaterThan(10)):WeaponEnchantment(3)"] if is_progressive else []),
                *([f"WeaponDamage({bonus_damage},{bonus_damage_type})"] if bonus_damage and bonus_damage_type else []),
                *(default_boosts if default_boosts else []),
            ],
            PassivesOnEquip=passives_on_equip,
            Proficiency_Group=proficiency_group,
            Rarity="Legendary",
            RootTemplate=game_objects_uuid,
            StatusOnEquip=status_on_equip,
            Unique="1" if is_unique else None,
            WeaponFunctors=weapon_functors,
            Weapon_Properties=weapon_properties,
            ValueUUID="d24c441f-7ebe-4229-8522-cf34c257ff20",  # Legendary Weapon
        ))

        return name
    
    @cached_property
    def _weapon_enchantment(self) -> str:
        name = self.make_name("WeaponEnchantment")
        self.loca[f"{name}_DisplayName"] = "Enchanted Blade"
        self.loca[f"{name}_Description"] = """
            Gain +1 to <LSTag Tooltip="AttackRoll">Spell Attack</LSTag>, Damage, and
            <LSTag Tooltip="SpellDifficultyClass">Save DC</LSTag> rolls.
        """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[
                "SpellSaveDC(1)",
                "RollBonus(MeleeSpellAttack,1)",
                "RollBonus(RangedSpellAttack,1)",
                "IF(IsSpell()):DamageBonus(1)",
            ],
        ))
        return name

    @cached_property
    def _weapon_enchantment_progression(self) -> str:
        name = self.make_name("WeaponEnchantmentProgression")
        self.loca[f"{name}_DisplayName"] = "Enchanted Blade"
        self.loca[f"{name}_Description"] = """
            Gain +1 to <LSTag Tooltip="AttackRoll">Spell Attack</LSTag>, Damage, and
            <LSTag Tooltip="SpellDifficultyClass">Save DC</LSTag> rolls. This increases to +2 at
            <LSTag>Level 5</LSTag>, and +3 at <LSTag>Level 9</LSTag>.
        """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[
                "IF(not CharacterLevelGreaterThan(4)):SpellSaveDC(1)",
                "IF(not CharacterLevelGreaterThan(4)):RollBonus(MeleeSpellAttack,1)",
                "IF(not CharacterLevelGreaterThan(4)):RollBonus(RangedSpellAttack,1)",
                "IF(not CharacterLevelGreaterThan(4) and IsSpell()):DamageBonus(1)",
                "IF(CharacterLevelGreaterThan(4) and not CharacterLevelGreaterThan(8)):SpellSaveDC(2)",
                "IF(CharacterLevelGreaterThan(4) and not CharacterLevelGreaterThan(8)):RollBonus(MeleeSpellAttack,2)",
                "IF(CharacterLevelGreaterThan(4) and not CharacterLevelGreaterThan(8)):RollBonus(RangedSpellAttack,2)",
                "IF(CharacterLevelGreaterThan(4) and not CharacterLevelGreaterThan(8) and IsSpell()):DamageBonus(2)",
                "IF(CharacterLevelGreaterThan(8)):SpellSaveDC(3)",
                "IF(CharacterLevelGreaterThan(8)):RollBonus(MeleeSpellAttack,3)",
                "IF(CharacterLevelGreaterThan(8)):RollBonus(RangedSpellAttack,3)",
                "IF(CharacterLevelGreaterThan(8) and IsSpell()):DamageBonus(3)",
            ],
        ))
        return name

    @cached_property
    def _weapon_kereskas_favour(self) -> str:
        name = self.make_name("WeaponKereskasFavour")
        self.loca[f"{name}_DisplayName"] = "Kereska's Favour"
        self.loca[f"{name}_Description"] = """
            At <LSTag>Level 9</LSTag> you gain
            <LSTag Type="Spell" Tooltip="Shout_MAG_TheChromatic_ChromaticAttunement">Kereska's Favour</LSTag>.
        """
        self.add(PassiveData(
            name,
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            Boosts=[
                "IF(CharacterLevelGreaterThan(8)):UnlockSpell(Shout_MAG_TheChromatic_ChromaticAttunement)",
            ],
        ))
        return name
    
    @cached_property
    def _weapon_kerekas_favour_boost(self) -> str:
        return "IF(not CharacterLevelGreaterThan(0)):UnlockSpell(Shout_MAG_TheChromatic_ChromaticAttunement)"

    @cached_property
    def _cleave(self) -> str:
        name = self.make_name("Cleave")
        self.add(SpellData(
            name,
            using="Zone_Cleave",
            SpellType="Zone",
            Cooldown="None",
            SpellSuccess=["DealDamage(MainMeleeWeapon,MainWeaponDamageType)", "GROUND:ExecuteWeaponFunctors(MainHand)"],
            TooltipDamageList=["DealDamage(MainMeleeWeapon,MainWeaponDamageType)"],
        ))
        return name

    @cached_property
    def _life_stealing(self) -> str:
        name = self.make_name("LifeStealing")
        self.add(PassiveData(
            name,
            using="MAG_Sarevok_OfChaos_Greatsword_Leeching_Passive",
            DisplayName=self.loca(f"{name}_DisplayName", "Life Stealing"),
        ))
        return name

    @cached_property
    def _abazigals_goods(self) -> TreasureChest:
        return self.TreasureChest(
            "AbazigalsGoods",
            "Abazigal's Goods",
            description="Contains a selection of items sold by the Echo of Abazigal.",
            items=[
                "MAG_Bhaalist_Gloves",
                "MAG_Bhaalist_Armor",
                "MAG_Bhaalist_Hat",
                "MAG_Critical_Force_Gloves",
                "MAG_Vicious_Battleaxe",
                "MAG_Vicious_Dagger",
                "MAG_Zhentarim_SleeperDagger",
                "MAG_LC_Fleshrend_Shortsword",
                "MAG_Vicious_Shortbow",
            ],
        )
    
    def _update_helmet_of_arcane_acuity(self) -> None:
        armor_name = "MAG_ElementalGish_ArcaneAcuity_Helmet"
        self.add(Armor(
            armor_name,
            using=armor_name,
            Proficiency_Group="",
        ))

        passive_name = "MAG_ElementalGish_ArcaneAcuity_Helmet_Passive"
        self.loca[f"{passive_name}_Description"] = """
            Whenever you deal damage with an attack, you gain
            <LSTag Type="Status" Tooltip="MAG_GISH_ARCANE_ACUITY">Arcane Acuity</LSTag> for 2 turns.
        """
        self.add(PassiveData(
            passive_name,
            using=passive_name,
            Description=self.loca[f"{passive_name}_Description"],
            Conditions=["IsAttack()"],
        ))


if __name__ == "__main__":
    tutorial_supplies = TutorialSupplies()
    tutorial_supplies.build()