from collections import OrderedDict
from functools import cached_property
from typing import Iterable
from uuid import UUID

from moddb import Bolster, Knowledge, level_map_ranges_format
from modtools.gamedata import (
    Armor,
    PassiveData,
    ObjectData,
    SpellData,
    StatusData,
)
from modtools.lsx.game import GameObjects, LevelMapSeries
from modtools.replacers import Mod
from modtools.text import TreasureTable

import os
import textwrap


class TutorialSupplies(Mod):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="TutorialSupplies",
                         description="Supplies for the tutorial chest.",
                         **kwds)

        self._equipment()

    def _equipment(self) -> None:
        self._add_treasure_chest(
            "Equipment",
            display_name="Equipment",
            description="Equipment.",
            items=[
                self._bolster_potion,
                self._knowledge_potion,
                self._overpowering_potion,
                self._underwear_of_giant_might,
            ],
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

    @cached_property
    def _underwear_of_giant_might(self) -> str:
        name = self.make_name("UnderwearOfGiantMight")
        underwear_uuid = self.make_uuid(name)

        self.loca[f"{name}_DisplayName"] = "Underwear of Giant Might"
        self.loca[f"{name}_Description"] = f"""
            These thick, surprisingly resilient undergarments look mundane, yet they hum with a faint, low tremor,
            granting the wearer the raw, unrefined might of a giant.
        """

        self.add(GameObjects(
            DisplayName=self.loca[f"{name}_DisplayName"],
            Description=self.loca[f"{name}_Description"],
            LevelName="",
            MapKey=underwear_uuid,
            ParentTemplateId="3caad2f1-719f-4070-b7f0-887c49c773d3",
            Name=name,
            Stats=name,
            Type="item",
        ))

        giant_might = self.make_name("GiantMight")

        self.add(Armor(
            name,
            using="ARM_Underwear",
            PassivesOnEquip=[giant_might],
            Rarity="Legendary",
            RootTemplate=underwear_uuid,
        ))

        strength_level_map = LevelMapSeries(
            Level1=22,
            Level6=24,
            Level11=26,
            Level16=28,
            Name=self.make_name("StrengthLevelMap"),
            UUID=self.make_uuid("StrengthLevelMap"),
        )
        self.add(strength_level_map)

        constitution_level_map = LevelMapSeries(
            Level1=20,
            Level6=22,
            Level11=24,
            Name=self.make_name("ConstitutionLevelMap"),
            UUID=self.make_uuid("ConstitutionLevelMap"),
        )
        self.add(constitution_level_map)

        self.loca[f"{giant_might}_DisplayName"] = "Giant Might"
        self.loca[f"{giant_might}_Description"] = f"""
            Your <LSTag Tooltip="Strength">Strength</LSTag> increases to [1], and your
            <LSTag Tooltip="Constitution">Constitution</LSTag> to [2].
        """

        self.add(PassiveData(
            giant_might,
            DisplayName=self.loca[f"{giant_might}_DisplayName"],
            Description=self.loca[f"{giant_might}_Description"],
            DescriptionParams=[
                f"LevelMapValue({strength_level_map.Name})",
                f"LevelMapValue({constitution_level_map.Name})",
            ],
            Boosts=[
                *level_map_ranges_format(self, strength_level_map, "AbilityOverrideMinimum(Strength,{})"),
                *level_map_ranges_format(self, constitution_level_map, "AbilityOverrideMinimum(Constitution,{})"),
            ],
        ))

        return name

    def _add_treasure_chest(self,
                            short_name: str,
                            *,
                            display_name: str | dict[str, str],
                            description: str | dict[str, str],
                            items: Iterable[str]) -> None:
        """Add a treasure chest to the tutorial chest."""
        name = self.make_name(short_name)
        chest_uuid = self.make_uuid(name)

        self._add_chest_game_object(name, chest_uuid, display_name, description)
        self._add_chest_container(name, chest_uuid)
        self._add_treasure_table(name, items)
    
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
    
    def _add_treasure_table(self, name: str, items: Iterable[str]) -> None:
        treasure_table = textwrap.dedent(f"""
            new treasuretable "TUT_Chest_Potions"
            CanMerge 1
            new subtable "1,1"
            object category "I_{name}",1,0,0,0,0,0,0,0

            new treasuretable "{name}_TreasureTable"
            CanMerge 1
        """)

        for item in items:
            treasure_table += textwrap.dedent(f"""
                new subtable "1,1"
                object category "I_{item}",1,0,0,0,0,0,0,0
            """).lstrip()

        self.add(TreasureTable(treasure_table))

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


if __name__ == "__main__":
    tutorial_supplies = TutorialSupplies()
    tutorial_supplies.build()