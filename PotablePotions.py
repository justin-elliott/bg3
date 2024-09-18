#!/usr/bin/env python3
"""
Generates files for the "PotablePotions" mod.
"""

import os

from moddb import Bolster
from modtools.gamedata import ObjectData, StatusData
from modtools.lsx.game import GameObjects
from modtools.mod import Mod
from modtools.text import Text, TreasureTable
from uuid import UUID


class ItemCombinations(Text):
    @property
    def path(self) -> str:
        return "Public/{folder}/Stats/Generated/ItemCombos.txt"


potable_potions = Mod(os.path.dirname(__file__),
                      author="justin-elliott",
                      name="PotablePotions",
                      description="Adds a selection of potions to the tutorial chest.")

loca = potable_potions.get_localization()

base_potion_name = f"{potable_potions.get_prefix()}_BasePotion"
potable_potions.add(ObjectData(
    base_potion_name,
    using="OBJ_Bottle",
    ValueUUID="4c5217d8-0232-4592-9e32-2fd729123f53",
    ValueOverride="3",
    Rarity="Legendary",
    ObjectCategory="",
))

potion_parent_template_id = UUID("8e660fd9-489d-42ff-a762-e4392e826666")
POTION_STATUS_PROPERTY_FLAGS = [
    "DisableOverhead",
    "IgnoreResting",
    "DisableCombatlog",
    "DisablePortraitIndicator",
]


def add_potion(
        name: str,
        *,
        uuid: UUID,
        display_name: str,
        description: str,
        icon: str,
        consume: bool = True,
        status_duration: int = -1,
        boosts: list[str] = None,
        passives: list[str] = None,
        stack_id: str = None,
        stack_type: str = None,
        status_property_flags: list[str] = None) -> None:
    if status_property_flags is None:
        status_property_flags = POTION_STATUS_PROPERTY_FLAGS

    potable_potions.add(GameObjects(
        DisplayName=display_name,
        Description=description,
        Flag_int32=0,
        Icon=icon,
        LevelName="",
        MapKey=uuid,
        Name=name,
        OnUseDescription=("hc857245cg5f9dg4f90g88d4g604f596d85ca", 1),
        ParentTemplateId=potion_parent_template_id,
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
                            Consume=consume,
                            IsHiddenStatus=True,
                            StatsId=name.upper(),
                            StatusDuration=status_duration,
                        ),
                    ],
                ),
            ]),
        ],
    ))

    potable_potions.add(ObjectData(
        name,
        using=base_potion_name,
        RootTemplate=uuid,
    ))

    potable_potions.add(StatusData(
        name.upper(),
        StatusType="BOOST",
        DisplayName=display_name,
        Description=description,
        Icon=icon,
        Boosts=boosts,
        Passives=passives,
        StackId=stack_id,
        StackType=stack_type,
        StatusPropertyFlags=status_property_flags,
    ))


def add_bolster_potion() -> str:
    name = f"{potable_potions.get_prefix()}_BolsterPotion"
    bolster = Bolster(potable_potions).add_bolster()
    bolster_potion_uuid = potable_potions.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Bolstering"}
    loca[f"{name}_Description"] = {"en": f"""
        Drinking this elixir grants the <LSTag Type="Spell" Tooltip="{bolster}">Bolster</LSTag> spell.
        """}

    add_potion(
        name,
        uuid=bolster_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_CONS_Drink_Potion_B",
        boosts=[f"UnlockSpell({bolster})"],
    )

    return name


def add_flying_potion() -> str:
    name = f"{potable_potions.get_prefix()}_FlyingPotion"
    flying_potion_uuid = potable_potions.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Flying"}
    loca[f"{name}_Description"] = {"en": """
        Drinking this elixir grants <LSTag Type="Spell" Tooltip="Projectile_Fly">Fly</LSTag>.
        """}

    add_potion(
        name,
        uuid=flying_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_ALCH_Solution_Potion_Flying",
        boosts=["UnlockSpell(Projectile_Fly)"],
    )

    return name


def add_overpowering_potion() -> str:
    name = f"{potable_potions.get_prefix()}_OverpoweringPotion"
    persuasion_potion_uuid = potable_potions.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Potion of Overpowering"}
    loca[f"{name}_Description"] = {"en": """
        Temporarily gain a significant boost to your health, armor class, attack rolls, damage rolls, and saving throws.
        """}

    add_potion(
        name,
        uuid=persuasion_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_CONS_Drug_Dreammist_A",
        status_duration=16,
        boosts=[
            "AC(20)",
            "DamageBonus(8d4)",
            "IncreaseMaxHP(50)",
            "RollBonus(Attack,20)",
            "RollBonus(SavingThrow,20)",
            "SpellSaveDC(20)",
            "IgnoreResistance(Bludgeoning,Resistant)",
            "IgnoreResistance(Piercing,Resistant)",
            "IgnoreResistance(Slashing,Resistant)",
        ],
        status_property_flags=[],
    )

    return name


bolster_potion = add_bolster_potion()
flying_potion = add_flying_potion()
overpowering_potion = add_overpowering_potion()

potable_potions.add(TreasureTable(f"""
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_{bolster_potion}",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_{flying_potion}",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_{overpowering_potion}",1,0,0,0,0,0,0,0
new subtable "1600,1"
object category "Gold",1,0,0,0,0,0,0,0
"""))

potable_potions.build()
