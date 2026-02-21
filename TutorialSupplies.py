#!/usr/bin/env python3

from dataclasses import dataclass
from functools import cached_property
from typing import Iterable
from uuid import UUID

from moddb import Bolster, Knowledge
from modtools.gamedata import (
    Armor,
    ObjectData,
    StatusData,
)
from modtools.lsx.game import GameObjects
from modtools.replacers import Mod
from modtools.text import ItemCombinations, TreasureTable

import os


class TutorialSupplies(Mod):
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
        ])

    @cached_property
    def _camp_clothing(self) -> TreasureChest:
        return self.TreasureChest(
            name="CampClothing",
            display_name="Camp Clothing",
            description="Contains a selection of camp clothing.",
            items=[
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
            ],
        )

    @cached_property
    def _camp_shoes(self) -> TreasureChest:
        return self.TreasureChest(
            name="CampShoes",
            display_name="Camp Shoes",
            description="Contains a selection of camp shoes.",
            items=[
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
                self._bolster_potion,
                self._knowledge_potion,
                self._overpowering_potion,
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
    def _knowledge_of_the_ages(self) -> None:
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
            passives: list[str] = None,
            stack_id: str = None,
            status_property_flags: list[str] = None) -> str:
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
            Passives=passives,
            StackId=name.upper() if stack_id is None else stack_id,
            StatusPropertyFlags=status_property_flags,
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


if __name__ == "__main__":
    tutorial_supplies = TutorialSupplies()
    tutorial_supplies.build()