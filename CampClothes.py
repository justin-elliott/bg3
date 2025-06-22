#!/usr/bin/env python3
"""
Generates files for the "CampClothes" mod.
"""

import os

from moddb import (
    Bolster,
    character_level_range,
    Defense,
    PackMule,
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
from modtools.mod import Mod
from modtools.text import Text, TreasureTable
from uuid import UUID


class ItemCombinations(Text):
    @property
    def path(self) -> str:
        return "Public/{folder}/Stats/Generated/ItemCombos.txt"


camp_clothes = Mod(os.path.dirname(__file__),
                   author="justin-elliott",
                   name="CampClothes",
                   mod_uuid=UUID("a93f92ad-5b31-4c9c-ac66-41082788e567"),
                   description="Adds a selection of outfits to the tutorial chest.")

camp_clothes.add(character_level_range)

bolster = Bolster(camp_clothes).add_bolster()
pack_mule = PackMule(camp_clothes).add_pack_mule(5.0)

loca = camp_clothes.get_localization()

loca["CampClothes_ComfortableBoots_DisplayName"] = {"en": "Comfortable Boots"}
loca["CampClothes_ComfortableBoots_Description"] = {"en": """
    Made of soft, sheepskin-lined leather, these are the perfect boots to wear around the campfire on a chilly night.
    """}

arm_boots_leather_a = UUID("cf987856-1381-477e-88db-6b359f7e19e8")
comfortable_boots_game_objects_uuid = UUID("ffda4777-7b6b-4582-b128-5f0175419b4a")

camp_clothes.add(GameObjects(
    DisplayName=loca["CampClothes_ComfortableBoots_DisplayName"],
    Description=loca["CampClothes_ComfortableBoots_Description"],
    LevelName="",
    MapKey=comfortable_boots_game_objects_uuid,
    Name="CampClothes_ComfortableBoots",
    ParentTemplateId=arm_boots_leather_a,
    Stats="CampClothes_ComfortableBoots",
    Type="item",
))

camp_clothes.add(Armor(
    "CampClothes_ComfortableBoots",
    using="ARM_Camp_Shoes",
    RootTemplate=comfortable_boots_game_objects_uuid,
))

loot_gen_backpack_a_posed_a = UUID("47805d79-88f1-4933-86eb-f78f67cbc33f")


def camp_clothes_container(name: str) -> None:
    container_uuid = camp_clothes.make_uuid(name)

    camp_clothes.add(GameObjects(
        DisplayName=loca[f"{name}_DisplayName"],
        Description=loca[f"{name}_Description"],
        Icon="Item_CONT_GEN_Chest_Travel_A_Small_A",
        LevelName="",
        MapKey=container_uuid,
        Name=name,
        ParentTemplateId=loot_gen_backpack_a_posed_a,
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

    camp_clothes.add(ObjectData(
        name,
        using="_Container",
        RootTemplate=container_uuid,
        Weight=0.01,
    ))


base_potion_name = f"{camp_clothes.get_prefix()}_BasePotion"
camp_clothes.add(ObjectData(
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
        status_duration: int = -1,
        boosts: list[str] = None,
        passives: list[str] = None,
        stack_id: str = None,
        status_property_flags: list[str] = POTION_STATUS_PROPERTY_FLAGS) -> None:
    camp_clothes.add(GameObjects(
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

    camp_clothes.add(ObjectData(
        name,
        using=base_potion_name,
        RootTemplate=uuid,
    ))

    camp_clothes.add(StatusData(
        name.upper(),
        StatusType="BOOST",
        DisplayName=display_name,
        Description=description,
        Icon=icon,
        Boosts=boosts,
        Passives=passives,
        StackId=name.upper() if stack_id is None else stack_id,
        StatusPropertyFlags=status_property_flags,
    ))


abilities_potion_base_name = f"{camp_clothes.get_prefix()}_AbilitiesPotion"
loca[f"{abilities_potion_base_name}_DisplayName"] = {"en": f"Elixir of Abilities"}

abilities_potion_icons = [
    "Item_CONS_Potion_Acid_Resistance_2",
    "Item_CONS_Potion_Cold_Resistance_2",
    "Item_CONS_Potion_Fire_Resistance_2",
    "Item_CONS_Potion_Force_Resistance_2",
    "Item_CONS_Potion_Lightning_Resistance_2",
    "Item_CONS_Potion_Necrotic_Resistance_2",
    "Item_CONS_Potion_Poison_Resistance_2",
    "Item_CONS_Potion_Psychic_Resistance_2",
    "Item_CONS_Potion_Radiant_Resistance_2",
    "Item_CONS_Potion_Thunder_Resistance_2",
]

def add_abilities_potion(bonus: int) -> str:
    name = f"{abilities_potion_base_name}_{bonus}"
    ability_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_Description"] = {"en": f"""
        Drinking this elixir grants you +{bonus} on all of your ability scores.
        """}

    add_potion(
        name,
        uuid=ability_potion_uuid,
        display_name=loca[f"{abilities_potion_base_name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon=abilities_potion_icons.pop(0) if len(abilities_potion_icons) > 0 else "Item_CONS_Potion_Resistance",
        boosts=[
            f"Ability(Strength,{bonus})",
            f"Ability(Dexterity,{bonus})",
            f"Ability(Constitution,{bonus})",
            f"Ability(Intelligence,{bonus})",
            f"Ability(Wisdom,{bonus})",
            f"Ability(Charisma,{bonus})",
        ],
        stack_id=abilities_potion_base_name,
    )

    return name


def add_action_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_ActionPotion"
    action_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Action"}
    loca[f"{name}_Description"] = {"en": """
        Drinking this elixir grants the <LSTag Type="Spell" Tooltip="Shout_ActionSurge">Action Surge</LSTag> ability.
        Additionally, you gain the <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag> and
        <LSTag Type="Passive" Tooltip="FastHands">Fast Hands</LSTag> passives.
        """}

    add_potion(
        name,
        uuid=action_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_ALCH_Solution_Elixir_Darkvision",
        boosts=["UnlockSpell(Shout_ActionSurge)"],
        passives=["ExtraAttack", "FastHands"],
    )

    return name


def add_agility_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_AgilityPotion"
    agility_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Agility"}
    loca[f"{name}_Description"] = {"en": """
        Drinking this elixir grants you <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all
        <LSTag Tooltip="Dexterity">Dexterity</LSTag> Skills, and
        <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in
        Dexterity <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>.
        """}

    add_potion(
        name,
        uuid=agility_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_ALCH_Solution_Remedy",
        boosts=[
            "ProficiencyBonus(SavingThrow,Dexterity)",
            "ProficiencyBonus(Skill,Acrobatics)",
            "ExpertiseBonus(Acrobatics)",
            "ProficiencyBonus(Skill,SleightOfHand)",
            "ExpertiseBonus(SleightOfHand)",
            "ProficiencyBonus(Skill,Stealth)",
            "ExpertiseBonus(Stealth)",
        ],
    )

    return name


def add_bolster_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_BolsterPotion"
    bolster_potion_uuid = camp_clothes.make_uuid(name)

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
    name = f"{camp_clothes.get_prefix()}_FlyingPotion"
    flying_potion_uuid = camp_clothes.make_uuid(name)

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
    name = f"{camp_clothes.get_prefix()}_OverpoweringPotion"
    persuasion_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Potion of Overpowering"}
    loca[f"{name}_Description"] = {"en": """
        Temporarily gain a significant boost to your strength, health, armor class, attack rolls, damage rolls, and
        saving throws.
        """}

    add_potion(
        name,
        uuid=persuasion_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
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
        ],
        status_property_flags=None,
    )

    return name


def add_pack_mule_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_PackMulePotion"
    pack_mule_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of the Pack Mule"}
    loca[f"{name}_Description"] = {"en": f"""
        Drinking this elixir grants the <LSTag Type="Passive" Tooltip="{pack_mule}">Pack Mule</LSTag> passive.
        """}

    add_potion(
        name,
        uuid=pack_mule_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_CONS_Drink_Potion_A",
        passives=[pack_mule],
    )

    return name


def add_persuasion_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_PersuasionPotion"
    persuasion_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Persuasion"}
    loca[f"{name}_Description"] = {"en": """
        Drinking this elixir grants you <LSTag Type="Tooltip" Tooltip="Expertise">Expertise</LSTag> in all
        <LSTag Tooltip="Charisma">Charisma</LSTag> Skills, and the ability to play Musical Instruments.
        """}

    add_potion(
        name,
        uuid=persuasion_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_CONS_ElixirOfHealth",
        boosts=[
            "Proficiency(MusicalInstrument)",
            "ProficiencyBonus(Skill,Deception)",
            "ExpertiseBonus(Deception)",
            "ProficiencyBonus(Skill,Intimidation)",
            "ExpertiseBonus(Intimidation)",
            "ProficiencyBonus(Skill,Performance)",
            "ExpertiseBonus(Performance)",
            "ProficiencyBonus(Skill,Persuasion)",
            "ExpertiseBonus(Persuasion)",
        ],
    )

    return name


def add_rituals_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_RitualsPotion"
    rituals_potion_uuid = camp_clothes.make_uuid(name)

    disguise_self = f"{camp_clothes.get_prefix()}_RitualDisguiseSelf"
    enhance_leap = f"{camp_clothes.get_prefix()}_RitualEnhanceLeap"
    detect_thoughts = f"{camp_clothes.get_prefix()}_RitualDetectThoughts"
    speak_with_dead = f"{camp_clothes.get_prefix()}_RitualSpeakWithDead"

    ritual_spells: list[tuple[str, str]] = [
        (disguise_self, "Shout_DisguiseSelf"),
        (enhance_leap, "Target_Jump"),
        (detect_thoughts, "Shout_DetectThoughts"),
        (speak_with_dead, "Target_SpeakWithDead"),
    ]

    for ritual_spell, source_spell in ritual_spells:
        camp_clothes.add(SpellData(
            ritual_spell,
            SpellType=source_spell.partition("_")[0],
            using=source_spell,
            Level="",
            MemoryCost="",
            RitualCosts="ActionPoint:1",
            UseCosts="ActionPoint:1",
        ))

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Rituals"}
    loca[f"{name}_Description"] = {"en": f"""
        Drinking this elixir grants you the
        <LSTag Type="Spell" Tooltip="{disguise_self}">Disguise Self</LSTag>,
        <LSTag Type="Spell" Tooltip="{enhance_leap}">Enhance Leap</LSTag>,
        <LSTag Type="Spell" Tooltip="{detect_thoughts}">Detect Thoughts</LSTag>, and
        <LSTag Type="Spell" Tooltip="{speak_with_dead}">Speak with Dead</LSTag> ritual spells.
        """}

    add_potion(
        name,
        uuid=rituals_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_CONS_Poison_Malice",
        boosts=[
            f"UnlockSpell({ritual_spell})" for ritual_spell, _ in ritual_spells
        ],
    )

    return name


def add_warding_potion() -> str:
    name = f"{camp_clothes.get_prefix()}_WardingPotion"
    warding = Defense(camp_clothes).add_warding()
    warding_potion_uuid = camp_clothes.make_uuid(name)

    loca[f"{name}_DisplayName"] = {"en": "Elixir of Warding"}
    loca[f"{name}_Description"] = {"en": f"""
        Drinking this elixir grants the <LSTag Type="Passive" Tooltip="{warding}">Warding</LSTag> passive, and
        <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> in
        Constitution <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>.
        """}

    add_potion(
        name,
        uuid=warding_potion_uuid,
        display_name=loca[f"{name}_DisplayName"],
        description=loca[f"{name}_Description"],
        icon="Item_UNI_Apprentice_Antidote",
        passives=[warding],
        boosts=["ProficiencyBonus(SavingThrow,Constitution)"],
    )

    return name


def reduce_weight(items: list[str]) -> list[str]:
    new_items = []
    for item in items:
        name = "CampClothes" + item.removeprefix("ARM")
        camp_clothes.add(Armor(
            name,
            using=item,
            Weight=0.01,
        ))
        new_items.append(name)
    return new_items


astral_knowledge = f"{camp_clothes.get_prefix()}_AstralKnowledge"
astral_knowledge_spell_animation = [
    "2f0d97b9-4a1f-4bf3-a3c2-32efb563d601,,",
    ",,",
    "6a95a81d-62e7-4b68-9b45-7e42e538dbde,,",
    "815364ff-bbaa-4efc-b10e-f31043fafd6e,,",
    "57e449b3-b712-4508-afcf-f2e91dc473f6,,",
    ",,",
    "84f3727f-aabc-4e34-bf31-c6cd0160bec9,,",
    ",,",
    ",,",
]

def magic_underwear(items: list[str]) -> list[str]:
    new_items = []
    for item in items:
        name = "CampClothes" + item.removeprefix("ARM") + "_Magic"
        camp_clothes.add(Armor(
            name,
            using=item,
            Boosts=[
                f"UnlockSpell({bolster})",
                "ProficiencyBonus(SavingThrow,Constitution)",
            ],
            PassivesOnEquip=[pack_mule],
            Rarity="Legendary",
            Weight=0.01,
        ))
        new_items.append(name)
    return new_items


loca["CampClothes_Clothing_DisplayName"] = {"en": "Camp Clothes"}
loca["CampClothes_Clothing_Description"] = {"en": """
    Contains a selection of camp clothing.
    """}
camp_clothes_container("CampClothes_Clothing")

loca["CampClothes_Dyes_DisplayName"] = {"en": "Dyes"}
loca["CampClothes_Dyes_Description"] = {"en": """
    Contains a selection of dyes.
    """}
camp_clothes_container("CampClothes_Dyes")

loca["CampClothes_Shoes_DisplayName"] = {"en": "Camp Shoes"}
loca["CampClothes_Shoes_Description"] = {"en": """
    Contains a selection of camp shoes.
    """}
camp_clothes_container("CampClothes_Shoes")

loca["CampClothes_Underwear_DisplayName"] = {"en": "Underwear"}
loca["CampClothes_Underwear_Description"] = {"en": """
    Contains a selection of underwear.
    """}
camp_clothes_container("CampClothes_Underwear")

loca["CampClothes_Potions_DisplayName"] = {"en": "Potions"}
loca["CampClothes_Potions_Description"] = {"en": """
    Contains a selection of potions.
    """}
camp_clothes_container("CampClothes_Potions")

loca["CampClothes_Equipment_DisplayName"] = {"en": "Equipment"}
loca["CampClothes_Equipment_Description"] = {"en": """
    Contains a selection of equipment.
    """}
camp_clothes_container("CampClothes_Equipment")

camp_clothes.add(Armor(
    "CampClothes_DaisyBody",
    using="ARM_Camp_Body",
    RootTemplate="aa0917ea-5f66-4a22-97de-654228484128",
))

base_clothing = [
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
    "UNI_DaisyPlaysuit",
]

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
    ("OBJ_Dye_Remover", None),
]

camp_clothes.add(Armor(
    "CampClothes_DaisyBoots",
    using="ARM_Camp_Shoes",
    RootTemplate="216f0362-f77b-420c-84cb-d84853aa173d",
))

base_shoes = [
    "CampClothes_ComfortableBoots",
    "CampClothes_DaisyBoots",
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
]

camp_clothes.add(Armor(
    "CampClothes_DaisyGloves",
    using="ARM_Underwear",
    RootTemplate="5a0ee632-9145-48b2-9b92-97c32c2ccbd9",
))

base_underwear = [
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
    "CampClothes_DaisyGloves",
]

dyes = [dye for dye in base_dyes]

clothing = reduce_weight(base_clothing)
shoes = reduce_weight(base_shoes)
underwear = reduce_weight(base_underwear) + magic_underwear(base_underwear)

potions = [
    add_abilities_potion(2),
    add_abilities_potion(4),
    add_abilities_potion(6),
    add_abilities_potion(8),
    add_abilities_potion(10),
    add_action_potion(),
    add_agility_potion(),
    add_bolster_potion(),
    add_flying_potion(),
    add_overpowering_potion(),
    add_pack_mule_potion(),
    add_persuasion_potion(),
    add_rituals_potion(),
    add_warding_potion(),
]

camp_clothes.add(Weapon(
    "CampClothes_Crimson_Shortsword",
    using="MAG_TheCrimson_Shortsword",
    BoostsOnEquipMainHand=["UnlockSpell(Target_OpeningAttack)", "UnlockSpell(Target_Slash_New)"],
    PassivesMainHand=["MAG_TheCrimson_Vicious_Passive", "MAG_IgnorePiercingResistance_Passive"],
    PassivesOffHand=[],
))

camp_clothes.add(SpellData(
    "CampClothes_Belm_Cleave",
    using="Zone_Cleave",
    SpellType="Zone",
    Cooldown="None",
    SpellSuccess=["DealDamage(MainMeleeWeapon,MainWeaponDamageType)", "GROUND:ExecuteWeaponFunctors(MainHand)"],
    TooltipDamageList=["DealDamage(MainMeleeWeapon,MainWeaponDamageType)"],
))

loca["CampClothes_Belm_BonusAttack_Description"] = {"en": """
    Strike out with an adder's speed, the very exemplar of swiftness embodied in steel.
    """}

camp_clothes.add(SpellData(
    "CampClothes_Belm_BonusAttack",
    using="Target_MAG_PHB_ScimitarOfSpeed_BonusAttack",
    SpellType="Target",
    Cooldown="None",
    Description=loca["CampClothes_Belm_BonusAttack_Description"],
    RequirementConditions=["CanUseWeaponActions() and IsProficientWithEquippedWeapon()"],
    SpellFlags=["IsMelee", "IsHarmful", "IsDefaultWeaponAction"],
))

camp_clothes.add(Weapon(
    "CampClothes_Belm_Shortsword",
    using="MAG_PHB_OfSpeed_Scimitar",
    BoostsOnEquipMainHand=[],
    Boosts=["UnlockSpell(CampClothes_Belm_Cleave)", "UnlockSpell(CampClothes_Belm_BonusAttack)"],
    PassivesOffHand=["MAG_IgnorePiercingResistance_Passive"],
    Proficiency_Group=["Shortswords", "MartialWeapons", "Scimitars"],
    RootTemplate="5961d027-75fd-4ad7-964c-8b786b5839fb",
))

loca["CampClothes_Weapon_EnchantmentProgression_DisplayName"] = {"en": "Enchanted Blade"}
loca["CampClothes_Weapon_EnchantmentProgression_Description"] = {"en": """
    Gain +1 to <LSTag Tooltip="AttackRoll">Attack</LSTag>, Damage, and <LSTag Tooltip="SpellDifficultyClass">Spell Save
    DC</LSTag> rolls. This increases to +2 at <LSTag>Level 5</LSTag>, and +3 at <LSTag>Level 9</LSTag>.
    """}

camp_clothes.add(PassiveData(
    "CampClothes_Weapon_EnchantmentProgression",
    DisplayName=loca["CampClothes_Weapon_EnchantmentProgression_DisplayName"],
    Description=loca["CampClothes_Weapon_EnchantmentProgression_Description"],
    Boosts=[
        "IF(CharacterLevelRange(1,4)):SpellSaveDC(1)",
        "IF(CharacterLevelRange(1,4)):RollBonus(MeleeSpellAttack,1)",
        "IF(CharacterLevelRange(1,4)):RollBonus(RangedSpellAttack,1)",
        "IF(CharacterLevelRange(1,4) and (IsSpell() or IsMeleeWeaponAttack())):DamageBonus(1)",
        "IF(CharacterLevelRange(5,8)):SpellSaveDC(2)",
        "IF(CharacterLevelRange(5,8)):RollBonus(MeleeSpellAttack,2)",
        "IF(CharacterLevelRange(5,8)):RollBonus(RangedSpellAttack,2)",
        "IF(CharacterLevelRange(5,8) and (IsSpell() or IsMeleeWeaponAttack())):DamageBonus(2)",
        "IF(CharacterLevelRange(9,20)):SpellSaveDC(3)",
        "IF(CharacterLevelRange(9,20)):RollBonus(MeleeSpellAttack,3)",
        "IF(CharacterLevelRange(9,20)):RollBonus(RangedSpellAttack,3)",
        "IF(CharacterLevelRange(9,20) and (IsSpell() or IsMeleeWeaponAttack())):DamageBonus(3)",
    ],
))

loca["CampClothes_Weapon_SpellProgression_DisplayName"] = {"en": "Kereska's Favour"}
loca["CampClothes_Weapon_SpellProgression_Description"] = {"en": """
    At <LSTag>Level 9</LSTag> you gain
    <LSTag Type="Spell" Tooltip="Shout_MAG_TheChromatic_ChromaticAttunement">Kereska's Favour</LSTag>.
    """}

camp_clothes.add(PassiveData(
    "CampClothes_Weapon_SpellProgression",
    DisplayName=loca["CampClothes_Weapon_SpellProgression_DisplayName"],
    Description=loca["CampClothes_Weapon_SpellProgression_Description"],
    Boosts=[
        "IF(CharacterLevelRange(9,20)):UnlockSpell(Shout_MAG_TheChromatic_ChromaticAttunement)",
    ],
))

loca["CampClothes_Weapon_CriticalProgression_DisplayName"] = {"en": "Improved Critical"}
loca["CampClothes_Weapon_CriticalProgression_Description"] = {"en": """
    At <LSTag>Level 13</LSTag>, you reduce the number you need to roll a Critical Hit while attacking by 1. This is
    further reduced by 1 at <LSTag>Level 17</LSTag>.
    """}

camp_clothes.add(PassiveData(
    "CampClothes_Weapon_CriticalProgression",
    DisplayName=loca["CampClothes_Weapon_CriticalProgression_DisplayName"],
    Description=loca["CampClothes_Weapon_CriticalProgression_Description"],
    Boosts=[
        "IF(CharacterLevelRange(13,16)):ReduceCriticalAttackThreshold(1)",
        "IF(CharacterLevelRange(17,20)):ReduceCriticalAttackThreshold(2)",
    ],
))

def add_weapon(name: str,
               *,
               parent_template_id: UUID,
               display_name: str,
               description: str = "hccebbf40g138fg422ega113g7a0869715627",
               damage_type: str = "Slashing",
               bonus_damage_type: str = "Force",
               using: str = "WPN_Longsword",
               has_reach: bool = False,
               visual_template: str = None) -> None:
    camp_clothes_longsword_game_objects_uuid = camp_clothes.make_uuid(name)
    camp_clothes.add(GameObjects(
        DisplayName=display_name,
        Description=description,
        LevelName="",
        MapKey=camp_clothes_longsword_game_objects_uuid,
        Name=name,
        ParentTemplateId=parent_template_id,
        Stats=name,
        Type="item",
        VisualTemplate=visual_template,
        children=[
            GameObjects.StatusList(
                children=[
                    GameObjects.StatusList.Status(Object=f"MAG_BYPASS_{damage_type.upper()}_RESISTANCE_TECHNICAL"),
                    GameObjects.StatusList.Status(Object="MAG_DIAMONDSBANE_TECHNICAL"),
                ],
            ),
        ],
    ))

    camp_clothes.add(Weapon(
        name,
        using=using,
        BoostsOnEquipMainHand=[
            "CannotBeDisarmed()",
            "UnlockSpell(Target_OpeningAttack)",
            "UnlockSpell(Target_Slash_New)",
            "UnlockSpell(Rush_SpringAttack)",
        ],
        DefaultBoosts=[
            "WeaponProperty(Magical)",
            "IF(CharacterLevelRange(1,4)):WeaponEnchantment(1)",
            "IF(CharacterLevelRange(5,8)):WeaponEnchantment(2)",
            "IF(CharacterLevelRange(9,20)):WeaponEnchantment(3)",
            f"IF(CharacterLevelRange(1,4)):WeaponDamage(1d4,{bonus_damage_type})",
            f"IF(CharacterLevelRange(5,8)):WeaponDamage(1d6,{bonus_damage_type})",
            f"IF(CharacterLevelRange(9,12)):WeaponDamage(1d8,{bonus_damage_type})",
            f"IF(CharacterLevelRange(13,20)):WeaponDamage(1d10,{bonus_damage_type})",
        ],
        PassivesOnEquip=[
            "UNI_Adamantine_CriticalVsItems_Passive",
            f"MAG_Ignore{damage_type.title()}Resistance_Passive",
            "CampClothes_Weapon_EnchantmentProgression",
            "CampClothes_Weapon_SpellProgression",
            "CampClothes_Weapon_CriticalProgression",
        ],
        Rarity="Legendary",
        RootTemplate=str(camp_clothes_longsword_game_objects_uuid),
        Unique="1",
        Weapon_Properties=[
            "Dippable",
            "Finesse",
            "Magical",
            "Melee",
            *(["Reach"] if has_reach else []),
            "Versatile",
        ],
    ))

loca["CampClothes_Katana_DisplayName"] = {"en": "Adamantine Katana"}
katana_uuid = UUID("7050c02e-f0e1-46b8-9400-2514805ecd2e")
add_weapon("CampClothes_Katana",
           parent_template_id=katana_uuid,
           display_name=loca["CampClothes_Katana_DisplayName"])

loca["CampClothes_InfernalKatana_DisplayName"] = {"en": "Infernal Katana"}
add_weapon("CampClothes_InfernalKatana",
           parent_template_id=katana_uuid,
           display_name=loca["CampClothes_InfernalKatana_DisplayName"],
           bonus_damage_type="Fire")

loca["CampClothes_DancingBlade_DisplayName"] = {"en": "Dancing Blade"}
phalar_aluve_uuid = UUID("6d0d3206-50b5-48ed-af92-a146ed6b98f2")
add_weapon("CampClothes_DancingBlade",
           parent_template_id=phalar_aluve_uuid,
           display_name=loca["CampClothes_DancingBlade_DisplayName"])

loca["CampClothes_ChampionsSpear_DisplayName"] = {"en": "Champion's Spear"}
loca["CampClothes_ChampionsSpear_Description"] = {"en": """
    A powerful spear gifted by a king to an extraordinary Huntress. Ideal for melee combat.
    """}
add_weapon("CampClothes_ChampionsSpear",
           using="WPN_Spear",
           damage_type="Piercing",
           has_reach=True,
           parent_template_id="74d9758a-84e9-4244-9ae8-14acee76acb3",
           display_name=loca["CampClothes_ChampionsSpear_DisplayName"],
           description=loca["CampClothes_ChampionsSpear_Description"])

camp_clothes.add(Armor(
    "CampClothes_Boots_Isobel",
    using="ARM_Shoes",
    RootTemplate="6ea46549-90eb-45fc-8ece-238cf8c4065c",
))

equipment = [
    "CampClothes_Crimson_Shortsword",
    "CampClothes_Belm_Shortsword",
    "CampClothes_Katana",
    "CampClothes_InfernalKatana",
    "CampClothes_DancingBlade",
    "CampClothes_ChampionsSpear",
    "MAG_Bhaalist_Armor",
    "UNI_DarkUrge_Bhaal_Cloak",
    "ORI_Wyll_Infernal_Robe",
    "CampClothes_Boots_Isobel",
]

item_template = """\
new subtable "1,1"
object category I_{},1,0,0,0,0,0,0,0
"""

for dye, dye_resource in dyes:
    camp_clothes.add(ItemCombinations(f"""
    new ItemCombination "{dye}"
    data "Type 1" "Object"
    data "Object 1" "{dye}"
    data "Transform 1" "None"
    data "Type 2" "Category"
    data "Object 2" "DyableArmor"
    data "Transform 2" "Dye"
    {f'data "DyeColorPresetResource" "{dye_resource}"' if dye_resource else ''}
    """))
    camp_clothes.add(ItemCombinations(f"""
    new ItemCombinationResult "{dye}_1"
    data "ResultAmount 1" "1"
    """))

camp_clothes.add(TreasureTable(f"""
new treasuretable "TUT_Chest_Potions"
CanMerge 1
new subtable "1,1"
object category "I_CampClothes_Clothing",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_CampClothes_Dyes",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_CampClothes_Shoes",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_CampClothes_Underwear",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_CampClothes_Potions",1,0,0,0,0,0,0,0
new subtable "1,1"
object category "I_CampClothes_Equipment",1,0,0,0,0,0,0,0
new subtable "10000,1"
object category "Gold",1,0,0,0,0,0,0,0
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Clothing_TreasureTable"
CanMerge 1
{"".join(item_template.format(outfit) for outfit in clothing).rstrip()}
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Dyes_TreasureTable"
CanMerge 1
{"".join(item_template.format(dye) for dye, _ in dyes).rstrip()}
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Shoes_TreasureTable"
CanMerge 1
{"".join(item_template.format(outfit) for outfit in shoes).rstrip()}
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Underwear_TreasureTable"
CanMerge 1
{"".join(item_template.format(outfit) for outfit in underwear).rstrip()}
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Potions_TreasureTable"
CanMerge 1
{"".join(item_template.format(potion) for potion in potions).rstrip()}
"""))

camp_clothes.add(TreasureTable(f"""
new treasuretable "CampClothes_Equipment_TreasureTable"
CanMerge 1
{"".join(item_template.format(equip) for equip in equipment).rstrip()}
"""))

camp_clothes.build()
