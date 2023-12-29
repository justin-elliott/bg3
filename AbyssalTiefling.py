#!/usr/bin/env python3
"""
Generates files for the "AbyssalTiefling" mod.
"""

import os

from modtools.lsx import Lsx
from modtools.mod import Mod
from uuid import UUID

# <attribute id="([^"]*)"\s*type="([^"]*)"\s*value="([^"]*)"\s*/>
# Lsx.Attribute("$1", "$2", value="$3"),

# data\s*"([^"]*)"\s*"([^"]*)"
# $1="$2",

abyssal_tiefling = Mod(os.path.dirname(__file__),
                       author="justin-elliott",
                       name="AbyssalTiefling",
                       mod_uuid=UUID("c6ecdb0d-431a-4d0e-b9ef-12bae7ac476c"),
                       description="Adds the Abyssal Tiefling sub-race.")

loca = abyssal_tiefling.get_localization()
loca.add_language("en", "English")

loca["AbyssalTiefling_DisplayName"] = {"en": "Abyssal Tiefling"}
loca["AbyssalTiefling_Description"] = {"en": """
    You are an outcast among outcasts; your bloodline hails not from the Nine Hells, but from the Infinite Layers of the
    Abyss.
    """}

loca["AbyssalTiefling_DemonicResilience_DisplayName"] = {"en": "Demonic Resilience"}
loca["AbyssalTiefling_DemonicResilience_Description"] = {"en": """
    Your <LSTag Tooltip="ArmorClass">Armour Class</LSTag> increases by 1.
    Your <LSTag Tooltip="HitPoints">hit point</LSTag> maximum increases by 2 for each level.
    """}

progression_table_uuid = UUID("fca5d92b-b012-4d99-880c-776c1028fa66")
progression_table_level_1_uuid = UUID("e7111142-9200-4b09-88cf-8faf4d3ff17f")

abyssal_tiefling_spells_level_1_uuid = UUID("15cf6370-2079-4afe-ab46-bc173f6c555d")
abyssal_tiefling_spells_level_5_uuid = UUID("969a3605-ff33-46b5-9501-fb06f53ff4df")
abyssal_tiefling_spells_level_7_uuid = UUID("3eba0261-7d82-4100-99a8-c234b204b43a")

abyssal_tiefling.add_progression_descriptions([
    Lsx.Node("ProgressionDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["AbyssalTiefling_DisplayName"], version=1),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["AbyssalTiefling_Description"], version=1),
        Lsx.Attribute("ProgressionTableId", "guid", value=str(progression_table_uuid)),
        Lsx.Attribute("Type", "FixedString", value="AbyssalTiefling"),
        Lsx.Attribute("UUID", "guid", "f7de8c05-f4b4-4c26-b944-a073c6155386"),
    ]),
    Lsx.Node("ProgressionDescription", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["AbyssalTiefling_DemonicResilience_DisplayName"], version=1),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["AbyssalTiefling_DemonicResilience_Description"], version=1),
        Lsx.Attribute("ExactMatch", "FixedString", value="IncreaseMaxHP(Level*2)"),
        Lsx.Attribute("ProgressionId", "guid", value=str(progression_table_level_1_uuid)),
        Lsx.Attribute("Type", "FixedString", value="AbyssalTiefling"),
        Lsx.Attribute("UUID", "guid", "a70f3a8a-fa30-4f02-8114-da7605a855b2"),
    ]),
])

abyssal_tiefling.add_progressions([
    Lsx.Node("Progression", [
        Lsx.Attribute("Boosts", "LSString", value=[
            "AC(1)",
            "ActionResource(Movement,1.5,0)",
            "IncreaseMaxHP(Level*2)",
        ]),
        Lsx.Attribute("Level", "uint8", value="1"),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling"),
        Lsx.Attribute("PassivesAdded", "LSString", value=["AbyssalTiefling_Blindsight"]),
        Lsx.Attribute("ProgressionType", "uint8", value="2"),
        Lsx.Attribute("Selectors", "LSString", value=[
            f"AddSpells({str(abyssal_tiefling_spells_level_1_uuid)})",
        ]),
        Lsx.Attribute("TableUUID", "guid", value=str(progression_table_uuid)),
        Lsx.Attribute("UUID", "guid", value=str(progression_table_level_1_uuid)),
    ]),
    Lsx.Node("Progression", [
        Lsx.Attribute("Level", "uint8", value="3"),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling"),
        Lsx.Attribute("PassivesAdded", "LSString", value=["FastHands"]),
        Lsx.Attribute("ProgressionType", "uint8", value="2"),
        Lsx.Attribute("TableUUID", "guid", value=str(progression_table_uuid)),
        Lsx.Attribute("UUID", "guid", value="3e7d1f8a-0c4c-49fd-bcc4-45d5369bbf2f"),
    ]),
    Lsx.Node("Progression", [
        Lsx.Attribute("Level", "uint8", value="5"),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling"),
        Lsx.Attribute("PassivesAdded", "LSString", value=["ExtraAttack"]),
        Lsx.Attribute("ProgressionType", "uint8", value="2"),
        Lsx.Attribute("Selectors", "LSString", value=[
            f"AddSpells({str(abyssal_tiefling_spells_level_5_uuid)})",
        ]),
        Lsx.Attribute("TableUUID", "guid", value=str(progression_table_uuid)),
        Lsx.Attribute("UUID", "guid", value="30a1f5ab-1fe3-48a7-bff3-4cef3acf6b9f"),
    ]),
    Lsx.Node("Progression", [
        Lsx.Attribute("Level", "uint8", value="7"),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling"),
        Lsx.Attribute("ProgressionType", "uint8", value="2"),
        Lsx.Attribute("Selectors", "LSString", value=[
            f"AddSpells({str(abyssal_tiefling_spells_level_7_uuid)})",
        ]),
        Lsx.Attribute("TableUUID", "guid", value=str(progression_table_uuid)),
        Lsx.Attribute("UUID", "guid", value="76f287d4-2387-46b9-94cd-aec7c9bfa21a"),
    ]),
    Lsx.Node("Progression", [
        Lsx.Attribute("Level", "uint8", value="9"),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling"),
        Lsx.Attribute("PassivesAdded", "LSString", value=["ImprovedCritical"]),
        Lsx.Attribute("ProgressionType", "uint8", value="2"),
        Lsx.Attribute("TableUUID", "guid", value=str(progression_table_uuid)),
        Lsx.Attribute("UUID", "guid", value="a21e3cfe-b2f5-42aa-a612-c1764f15c06c"),
    ]),
    Lsx.Node("Progression", [
        Lsx.Attribute("Level", "uint8", value="11"),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling"),
        Lsx.Attribute("PassivesAdded", "LSString", value=["ExtraAttack_2"]),
        Lsx.Attribute("PassivesRemoved", "LSString", value=["ExtraAttack"]),
        Lsx.Attribute("ProgressionType", "uint8", value="2"),
        Lsx.Attribute("TableUUID", "guid", value=str(progression_table_uuid)),
        Lsx.Attribute("UUID", "guid", value="91a1b0f9-831f-4b40-9446-b95387e94899"),
    ]),
])

abyssal_tiefling.add_level_maps([
    Lsx.Node("LevelMapSeries", [
        *[Lsx.Attribute(f"Level{level}", "LSString", value=f"1d{int((level + 3) / 4) * 2 + 2}")
            for level in range(1, 21)],
        Lsx.Attribute("Name", "FixedString", value="AbyssalTiefling_Claws_Value"),
        Lsx.Attribute("UUID", "guid", value="89918fbb-1395-46b8-b764-3ef5b56a4ea2"),
    ]),
])

loca["AbyssalTiefling_Blindsight_Description"] = {"en": """
    You can perceive your surroundings without relying on sight.
    """}

abyssal_tiefling.add_passive_data(
    "AbyssalTiefling_Blindsight",
    using="Blindsight",
    Description=loca["AbyssalTiefling_Blindsight_Description"],
    Properties="Highlighted",
)

loca["AbyssalTiefling_Claws_DisplayName"] = {"en": "Claws"}
loca["AbyssalTiefling_Claws_Description"] = {"en": """
    Lash out with deadly claws and make your enemy <LSTag Type="Status" Tooltip="BLEEDING">Bleed</LSTag>.
    """}

abyssal_tiefling.add_spell_data(
    "AbyssalTiefling_Claws",
    using="Target_Claws_Imp",
    SpellType="Target",
    DisplayName=loca["AbyssalTiefling_Claws_DisplayName"],
    Description=loca["AbyssalTiefling_Claws_Description"],
    SpellSuccess=[
        "DealDamage(max(1,LevelMapValue(AbyssalTiefling_Claws_Value)+UnarmedMeleeAbilityModifier),Slashing,Magical)",
        "IF(Character()):ApplyStatus(BLEEDING,100,2)",
    ],
    TooltipDamageList=[
        "DealDamage(LevelMapValue(AbyssalTiefling_Claws_Value)+UnarmedMeleeAbilityModifier,Slashing)"
    ],
    TooltipStatusApply="ApplyStatus(BLEEDING,100,2)",
    Sheathing="Sheathed",
)

loca["AbyssalTiefling_AbyssalStep_DisplayName"] = {"en": "Abyssal Step"}
loca["AbyssalTiefling_AbyssalStep_Description"] = {"en": """
    Stepping between planes, you teleport to an unoccupied space you can see.
    """}

abyssal_tiefling.add_spell_data(
    "AbyssalTiefling_AbyssalStep",
    using="Target_MistyStep",
    SpellType="Target",
    DisplayName=loca["AbyssalTiefling_AbyssalStep_DisplayName"],
    Description=loca["AbyssalTiefling_AbyssalStep_Description"],
    Icon="Action_Warlock_OneWithShadows",
    Level="",
    SpellSchool="None",
    Sheathing="Sheathed",
    SpellStyleGroup="Class",
    UseCosts="Movement:Distance*0.5",
    PrepareEffect="a0458d31-f8ef-419a-8708-5715c81e91d3",
    CastEffect="52af7a1d-d5d9-4506-85ce-d124f1ef9ea5",
)

loca["AbyssalTiefling_Swipe_DisplayName"] = {"en": "Swipe"}
loca["AbyssalTiefling_Swipe_Description"] = {"en": """
    Lash out with your claws to strike up to [1] enemies at once and make them
    <LSTag Type="Status" Tooltip="BLEEDING">Bleed</LSTag>.
    """}

abyssal_tiefling.add_spell_data(
    "AbyssalTiefling_Swipe",
    using="Zone_Cleave",
    SpellType="Zone",
    DisplayName=loca["AbyssalTiefling_Swipe_DisplayName"],
    Description=loca["AbyssalTiefling_Swipe_Description"],
    DescriptionParams="3",
    Icon="Action_Monster_ElementalEarth_MultiAttack",
    Cooldown="None",
    RequirementConditions="",
    SpellRoll="Attack(AttackType.MeleeUnarmedAttack)",
    SpellSuccess=[
        "DealDamage(max(1,(LevelMapValue(AbyssalTiefling_Claws_Value)+UnarmedMeleeAbilityModifier)/2),Slashing,Magical)",
        "IF(Character()):ApplyStatus(BLEEDING,100,2)",
    ],
    TooltipAttackSave="MeleeUnarmedAttack",
    TooltipDamageList=[
        "DealDamage((LevelMapValue(AbyssalTiefling_Claws_Value)+UnarmedMeleeAbilityModifier)/2,Slashing)",
    ],
    TooltipStatusApply="ApplyStatus(BLEEDING,100,2)",
    PrepareSound="CrSpell_Prepare_Claw",
    CastSound="CrSpell_Cast_Claw",
    TargetSound="CrSpell_Impact_Claw",
    SpellFlags=[
        "IsMelee",
        "IsHarmful",
    ],
    CastEffect="456c19a5-ca43-4f93-b5a7-bb01fa8d1240",
    Sheathing="Sheathed",
    WeaponTypes="None",
)

abyssal_tiefling.add_spell_lists([
    Lsx.Node("SpellList", [
        Lsx.Attribute("Comment", "LSString", value="Abyssal Tiefling spells granted at level 1"),
        Lsx.Attribute("Spells", "LSString", value=[
            "AbyssalTiefling_Claws",
        ]),
        Lsx.Attribute("UUID", "guid", value=str(abyssal_tiefling_spells_level_1_uuid)),
    ]),
    Lsx.Node("SpellList", [
        Lsx.Attribute("Comment", "LSString", value="Abyssal Tiefling spells granted at level 5"),
        Lsx.Attribute("Spells", "LSString", value=[
            "AbyssalTiefling_AbyssalStep",
        ]),
        Lsx.Attribute("UUID", "guid", value=str(abyssal_tiefling_spells_level_5_uuid)),
    ]),
    Lsx.Node("SpellList", [
        Lsx.Attribute("Comment", "LSString", value="Abyssal Tiefling spells granted at level 7"),
        Lsx.Attribute("Spells", "LSString", value=[
            "AbyssalTiefling_Swipe",
        ]),
        Lsx.Attribute("UUID", "guid", value=str(abyssal_tiefling_spells_level_7_uuid)),
    ]),
])

abyssal_tiefling_race_uuid = UUID("89e36a3c-6249-48fd-af3d-31e7a9a99406")
abyssal_tiefling_tag_uuid = UUID("e8185e91-8340-42f1-81ca-92adb140d637")

abyssal_tiefling.add_races([
    Lsx.Node("Race", [
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["AbyssalTiefling_DisplayName"], version=1),
        Lsx.Attribute("Description", "TranslatedString", handle=loca["AbyssalTiefling_Description"], version=1),
        Lsx.Attribute("DisplayTypeUUID", "guid", value="899d275e-9893-490a-9cd5-be856794929f"),
        Lsx.Attribute("Name", "FixedString", value="AbyssalTiefling"),
        Lsx.Attribute("ParentGuid", "guid", value="b6dccbed-30f3-424b-a181-c4540cf38197"),
        Lsx.Attribute("ProgressionTableUUID", "guid", value=str(progression_table_uuid)),
        Lsx.Attribute("RaceSoundSwitch", "FixedString", value="Tiefling"),
        Lsx.Attribute("UUID", "guid", value=str(abyssal_tiefling_race_uuid)),
    ], children=[
        *[Lsx.Node("MakeupColors", [
                Lsx.Attribute("Object", "guid", value=guid)
            ])
            for guid in [
                "2d0b5625-5820-4e1e-a239-7c1ccfc2e1a0",
                "238621c9-e7db-4634-99de-73bf3cb322fd",
                "188558ca-609b-40ed-8e73-171f191c5b5e",
                "434a8d29-b343-4b0a-a2e4-f923e42c74f6",
                "50ea0b01-6403-4f57-b5c9-81f5e983dcd2",
                "1e695d21-98e3-4674-a58c-d0562f92d32e",
                "96c8182d-ef3c-44b6-b492-e9eebc8170ff",
                "82a12016-5aef-46c1-ab36-8072acba7e6f",
                "7c6fb12e-f490-4c0e-981f-7aa48ca99d8d",
                "22ccccc4-c26a-447d-bb89-a5ba46e7c3d2",
                "feed9335-fa15-4cc9-83b4-6258d50b23c7",
                "af459a00-5464-443b-aced-0df16ed976fc",
                "4c0e8bb2-06d5-4744-aecd-e5b94753de76",
                "19801e9f-e229-42c1-89ef-628eaf906c94",
                "836a1079-f6aa-4071-a5f8-997a38ce35f6",
                "b8d05d26-50ef-448b-a6db-adf10670582d",
                "058460e6-4188-4efa-ae1d-a44f19592ded",
                "e54080f1-c1b7-4880-ac95-38fa3f77a383",
                "deae8f09-e739-43c4-9bb3-7b1f8dda8379",
                "848d10e1-285a-4133-9808-e5b7360b616f",
                "81ef59ed-4b6d-4b61-876d-c78539c8e892",
                "9dc406eb-49e3-4439-a678-39e8bdfb037f",
                "e8ca07c7-96cb-4fc6-872b-6c4fb0221c93",
                "6c33e4e6-bd6c-4b7e-8892-dc08c472a88e",
                "1388f71d-8c72-4bdf-bae1-cf33e93cd5ed",
                "ed328d7a-f856-42c9-96d9-50e9becd7470",
                "c2e5bc51-23c0-466a-9d4e-7802767bf67c",
                "a5fdd68c-6036-4248-a8d3-ac02244700f2",
                "f632c596-d3be-44ca-be60-070a6f5c6abc",
                "719801e5-8e2b-48e7-ab11-6761cd1d9c33",
                "6d90761a-6977-460d-8f8c-dd7a65e7931a",
                "f29aef85-dde1-46b2-9fbb-5d77bd7c3058",
                "7ba7ba2b-11ec-4bf7-944f-9e8a358ade89",
                "04ef6910-8d2c-485e-b52c-621e3ce3900e",
                "6b0a0476-b138-467f-a806-5b5982f9ee4d",
                "fd54da24-978b-4791-bb53-d6d7d8a71c4d",
                "7f71d965-27bc-41f6-b07d-f9e7f291fb41",
                "3343577a-4eab-4885-81cc-41d1bc063034",
                "7c61df3d-063e-4c59-b65b-29517e14cbe5",
                "3ea649b0-d802-4113-a483-ff3ed600c3ef",
                "f1f685c0-776a-46a5-9f2b-41037f1ed04c",
                "59bd162e-a8cf-47b1-98ae-a7317d256209",
                "f85370dc-5dea-4f58-9a7f-0b2493a9b959",
                "7e8eedd6-183c-4a84-8eef-05ebddfa0b3b",
                "5a3b40fd-374e-4d77-848e-e44f4a16f3cc",
                "1f50b39a-668d-47cd-a3ad-7352ef289afe",
                "e355c6ce-2ed7-4759-9f88-b3973faa1efd",
                "0b73291f-a147-486c-a890-0153d3385deb",
                "c5a55b73-cdc0-4d90-84f2-44aeab166e7e",
                "a0845f28-4a39-48ab-bcc2-ed437084924b",
                "d2292210-2894-4b89-8165-400d9bdc558a",
                "8dd11981-af36-465d-8819-0243b11d8fcc",
                "db930324-a62c-49a8-9761-735a400211c4",
                "7df87268-0e2c-41f3-b607-b4d7c84ae8c4",
                "4456a2ed-b56a-4cdc-a01e-30a2c558908e",
                "dc318ab2-12e5-42c5-a6fb-0f9a97dd3004",
                "fcf1bd0f-b601-45ac-85da-796c802ed7e4",
                "f9090693-325c-44e3-8141-9d3c2be2d15b",
                "f60887be-96b3-4238-91ab-7cd7bb73de29",
                "93de91f7-525b-43a8-9d1b-52f05b1d356b",
                "32c9de7d-9708-42f7-810b-885648de13c3",
                "5d701fc3-7f94-4b25-8c40-248ba3aeb89b",
                "b519f7f1-91eb-49ca-8734-0eda699a5b80",
                "68677cb0-9f2c-4a2d-bb33-6bcfb823aec9",
                "0497da47-7bbf-4d78-8589-710b81f7ad14",
                "0388e821-3217-44d1-a0dd-90fb4fb77fbc",
                "68da7d75-5381-4d04-bd4e-b822a0258a86",
                "9413a7c2-eb80-4bc0-965e-5fc9d556d27e",
                "4e462cf6-dd12-49ec-96a0-42afb506d9a6",
                "7d8b9a32-fc1c-4752-b256-1e6b708bac9f",
                "1a72b092-615c-47b2-9729-2c36e790406e",
                "cdf42879-fe3c-45fc-9764-93d858df5c6e",
                "482aa378-c75f-485b-8253-67b0556df3ad",
                "2258a240-6a08-4d2e-9e03-b5e95b74ca0e",
                "2fd79426-9b16-4aa8-85e6-92ac0742035a",
                "36b85265-4907-4c51-b141-49dfc2aa0f2f",
                "55e5caa0-3ad7-4d33-b45c-625b6e7494ba",
                "523abbd1-6745-49b8-beb1-3188e95f0fe9",
                "703a950a-330d-4e70-9d42-440641af7da1",
                "4da645ad-0d5a-499a-a011-e699c8ef16b7",
                "6063d773-48da-4dbb-b2c1-be8a8b8fffbf",
                "ea75a2e4-6cf7-4f76-8288-aa37b41e7e56",
                "aad2e0a8-e557-4a83-b8c7-192ff7a9878f",
                "ea682d85-93f0-4754-b23a-d953f9fe4f85",
                "0db72b77-f44e-4702-8b20-8c8add3741d7",
                "c9a03963-34f8-4899-a1ee-fcd51c165610",
                "fb9c05ec-59e8-44b4-a314-4859a195ddac",
                "e3ae2505-7932-48c8-bab5-07363e271284",
                "926ff86c-72bc-4e95-9940-23abb9dba06b",
                "10bd4271-19ac-4d06-bd90-595a23c3c9c8",
                "46e655a9-8975-401f-8099-c8f3735eb15b",
                "9f62d712-03fa-43c6-9c87-4925497dfea1",
                "cf7e70e4-9192-46c4-a6a6-471cc46ee3e1",
                "e2a2383e-4c83-45f4-9fd0-4cb215897c35",
            ]],
        *[Lsx.Node("SkinColors", [
                Lsx.Attribute("Object", "guid", value=guid)
            ])
            for guid in [
                "0b5c0530-856d-4ad0-9f9f-f2b977dd90ed",
                "5340217e-f1ab-42ab-9598-bf6f4a254568",
                "49f9f241-c0fd-43f3-a24b-8a598ff0f184",
                "9a0dbef3-2bd0-48a6-bd0b-ae0e72fce174",
                "68101886-efe0-44de-b95a-ef6eab4da57a",
                "3b284d60-6ffa-4f12-a241-09a841628711",
                "1aaa5598-3f16-4497-b6b4-b4af66d6ec07",
                "41839704-896f-4b29-a49f-c1d34ecee3cc",
                "df7eeaf4-8d2e-4c49-8bdd-5ce16847de53",
                "3e80bdc4-4e83-4578-acc8-190b6e53b86d",
                "3131f1c6-7b0a-4bcb-b690-bd1a54943b75",
                "acd2eae4-132f-4db6-9faa-4f06fe80f024",
                "ae667c9f-4405-4d1b-b24d-37ae6bcd697d",
                "ebf8afb9-3ca1-4e35-aa43-135bf1a2aaec",
                "bb1ba359-6cfa-4b45-88fb-8248f6f182c5",
                "f4d62207-d421-44e6-8430-cd92ba8edc56",
            ]],
        Lsx.Node("Tags", [
            Lsx.Attribute("Object", "guid", value=str(abyssal_tiefling_tag_uuid))
        ]),
        *[Lsx.Node("TattooColors", [
                Lsx.Attribute("Object", "guid", value=guid)
            ])
            for guid in [
                "a8f8292a-8a5c-4b82-8e59-d81a7e827e71",
                "17c6ac4b-72f5-4687-a2bb-c6fca472e8b3",
                "f7ba1aba-556c-4638-ba11-8c663d268a23",
                "8f8019ae-4c7d-4871-8479-1219fbf6ba7e",
                "f148e5ed-7b11-4226-bd7f-ec28b4e25cdc",
                "1c1d5081-97cd-46ca-a711-b1a1f57061f6",
                "b859dd0b-d42a-47ff-8288-efe3260957ca",
                "91408f62-3631-4374-98c2-01898dcab051",
                "2870c53c-ba6d-4eca-bfc4-d611dc05fac2",
                "3604fdeb-f956-424f-a073-899246213833",
            ]],
    ]),
])

abyssal_tiefling.add_tags([
    Lsx.Node("Tags", [
        Lsx.Attribute("Description", "LSString", value="|Abyssal Tiefling|"),
        Lsx.Attribute("DisplayName", "TranslatedString", handle=loca["AbyssalTiefling_DisplayName"], version=1),
        Lsx.Attribute("DisplayDescription", "TranslatedString", handle=loca["AbyssalTiefling_Description"], version=1),
        Lsx.Attribute("Icon", "FixedString", value=""),
        Lsx.Attribute("Name", "FixedString", value="ABYSSALTIEFLING"),
        Lsx.Attribute("UUID", "guid", value=str(abyssal_tiefling_tag_uuid)),
    ], children=[
        Lsx.Node("Categories", children=[
            *[Lsx.Node("Category", [
                Lsx.Attribute("Name", "LSString", value=value)
                ])
                for value in ["Code", "Dialog", "Race", "PlayerRace", "CharacterSheet"]]
        ])
    ])
])

abyssal_tiefling_female_base_uuid = UUID("4cc6e3f3-d9c8-47e0-b955-4e37599d220e")
abyssal_tiefling_female_player_uuid = UUID("e47cecf9-f806-4a17-8647-7c3ac8f4be09")
abyssal_tiefling_female_player_strong_uuid = UUID("f14e076f-88f9-45cf-92dd-1bd10c069be7")

abyssal_tiefling_male_base_uuid = UUID("0763377f-b980-4854-9130-93432fae426b")
abyssal_tiefling_male_player_uuid = UUID("dd126fba-c403-466e-ba7d-6776de2f2330")
abyssal_tiefling_male_player_strong_uuid = UUID("31d78139-8c6d-452d-ab5c-8e63eddec776")

abyssal_tiefling.add_character_creation_presets([
    Lsx.Node("CharacterCreationPreset", [
        Lsx.Attribute("BodyShape", "uint8", value="0"),
        Lsx.Attribute("BodyType", "uint8", value="1"),
        Lsx.Attribute("CloseUpA", "LSString", value="TIF_F_Camera_Closeup_A"),
        Lsx.Attribute("CloseUpB", "LSString", value="TIF_F_Camera_Closeup_B"),
        Lsx.Attribute("Overview", "LSString", value="TIF_F_Camera_Overview_A"),
        Lsx.Attribute("RaceUUID", "guid", value="b6dccbed-30f3-424b-a181-c4540cf38197"),
        Lsx.Attribute("RootTemplate", "guid", value=str(abyssal_tiefling_female_player_uuid)),
        Lsx.Attribute("SubRaceUUID", "guid", value=str(abyssal_tiefling_race_uuid)),
        Lsx.Attribute("UUID", "guid", value="de521499-5342-4835-a3a6-de7eda4d1dd6"),
        Lsx.Attribute("VOLinesTableUUID", "guid", value="14df8f45-90af-4bd0-8024-42624da9976e"),
    ]),
    Lsx.Node("CharacterCreationPreset", [
        Lsx.Attribute("BodyShape", "uint8", value="1"),
        Lsx.Attribute("BodyType", "uint8", value="1"),
        Lsx.Attribute("CloseUpA", "LSString", value="HUM_FB_Camera_Closeup_A"),
        Lsx.Attribute("CloseUpB", "LSString", value="HUM_FB_Camera_Closeup_B"),
        Lsx.Attribute("Overview", "LSString", value="HUM_FB_Camera_Overview_A"),
        Lsx.Attribute("RaceUUID", "guid", value="b6dccbed-30f3-424b-a181-c4540cf38197"),
        Lsx.Attribute("RootTemplate", "guid", value=str(abyssal_tiefling_female_player_strong_uuid)),
        Lsx.Attribute("SubRaceUUID", "guid", value=str(abyssal_tiefling_race_uuid)),
        Lsx.Attribute("UUID", "guid", value="4aefdf83-cd73-4314-8b26-73c88bfc7aa0"),
        Lsx.Attribute("VOLinesTableUUID", "guid", value="14df8f45-90af-4bd0-8024-42624da9976e"),
    ]),
    Lsx.Node("CharacterCreationPreset", [
        Lsx.Attribute("BodyShape", "uint8", value="0"),
        Lsx.Attribute("BodyType", "uint8", value="0"),
        Lsx.Attribute("CloseUpA", "LSString", value="TIF_M_Camera_Closeup_A"),
        Lsx.Attribute("CloseUpB", "LSString", value="TIF_M_Camera_Closeup_B"),
        Lsx.Attribute("Overview", "LSString", value="TIF_M_Camera_Overview_A"),
        Lsx.Attribute("RaceUUID", "guid", value="b6dccbed-30f3-424b-a181-c4540cf38197"),
        Lsx.Attribute("RootTemplate", "guid", value=str(abyssal_tiefling_male_player_uuid)),
        Lsx.Attribute("SubRaceUUID", "guid", value=str(abyssal_tiefling_race_uuid)),
        Lsx.Attribute("UUID", "guid", value="5ed61425-1515-4e30-a7a7-864131e71ac1"),
        Lsx.Attribute("VOLinesTableUUID", "guid", value="14df8f45-90af-4bd0-8024-42624da9976e"),
    ]),
    Lsx.Node("CharacterCreationPreset", [
        Lsx.Attribute("BodyShape", "uint8", value="1"),
        Lsx.Attribute("BodyType", "uint8", value="0"),
        Lsx.Attribute("CloseUpA", "LSString", value="HUM_MB_Camera_Closeup_A"),
        Lsx.Attribute("CloseUpB", "LSString", value="HUM_MB_Camera_Closeup_B"),
        Lsx.Attribute("Overview", "LSString", value="HUM_MB_Camera_Overview_A"),
        Lsx.Attribute("RaceUUID", "guid", value="b6dccbed-30f3-424b-a181-c4540cf38197"),
        Lsx.Attribute("RootTemplate", "guid", value=str(abyssal_tiefling_male_player_strong_uuid)),
        Lsx.Attribute("SubRaceUUID", "guid", value=str(abyssal_tiefling_race_uuid)),
        Lsx.Attribute("UUID", "guid", value="e4efca8b-8dbf-4560-97fd-e927d9521fe0"),
        Lsx.Attribute("VOLinesTableUUID", "guid", value="14df8f45-90af-4bd0-8024-42624da9976e"),
    ]),
])

abyssal_tiefling.add_root_templates([
    # Abyssal Tiefling Female Base
    Lsx.Node("GameObjects", [
        Lsx.Attribute("CharacterVisualResourceID", "FixedString", value="0d301a8e-ba30-4616-266f-82d4e7ef46ef"),
        Lsx.Attribute("GeneratePortrait", "LSString", value="Icon_Tiefling_Female"),
        Lsx.Attribute("Icon", "FixedString", value="0d301a8e-ba30-4616-266f-82d4e7ef46ef-_(Icon_Tiefling_Female)"),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(abyssal_tiefling_female_base_uuid)),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling_Female_Base"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value="5b11557c-90b8-4e7b-bf46-1fb23454a79d"),
        Lsx.Attribute("Race", "guid", value=str(abyssal_tiefling_race_uuid)),
        Lsx.Attribute("Type", "FixedString", value="character"),
        Lsx.Attribute("VisualTemplate", "FixedString", value="32c30a04-896d-33fd-69eb-5c5ab5dfa284"),
        Lsx.Attribute("_OriginalFileVersion_", "int64", value="1"),
    ], children=[
        Lsx.Node("GameMaster"),
        Lsx.Node("LocomotionParams"),
    ]),

    # Abyssal Tiefling Female Player
    Lsx.Node("GameObjects", [
        Lsx.Attribute("CharacterVisualResourceID", "FixedString", value="0a902841-1c5b-7acc-9620-91b284a65436"),
        Lsx.Attribute("Icon", "FixedString", value="0a902841-1c5b-7acc-9620-91b284a65436-_(Icon_Tiefling_Female)"),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(abyssal_tiefling_female_player_uuid)),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling_Female_Player"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value=str(abyssal_tiefling_female_base_uuid)),
        Lsx.Attribute("PortraitVisualResourceID", "FixedString", value="41ac6638-8590-4c25-2789-44cdc8ef87d8"),
        Lsx.Attribute("SpellSet", "FixedString", value="CommonPlayerActions"),
        Lsx.Attribute("Stats", "FixedString", value="HeroTieflingFemale"),
        Lsx.Attribute("Type", "FixedString", value="character"),
        Lsx.Attribute("_OriginalFileVersion_", "int64", value="1"),
    ], children=[
        Lsx.Node("LocomotionParams"),
        Lsx.Node("SpeakerGroupList", children=[
            Lsx.Node("SpeakerGroup", [
                Lsx.Attribute("Object", "guid", value="02cdc15e-1dc3-5eb4-f73c-9458b4f90b9f"),
            ]),
            Lsx.Node("SpeakerGroup", [
                Lsx.Attribute("Object", "guid", value="e0d1ff71-04a8-4340-ae64-9684d846eb83"),
            ]),
        ]),
    ]),

    # Abyssal Tiefling Female Player Strong
    Lsx.Node("GameObjects", [
        Lsx.Attribute("CharacterVisualResourceID", "FixedString", value="fcff3667-ddc0-1b32-2b7f-1acedfa0cf50"),
        Lsx.Attribute("EquipmentRace", "guid", value="a5789cd3-ecd6-411b-a53a-368b659bc04a"),
        Lsx.Attribute("GeneratePortrait", "LSString", value="Icon_Human_Female_Strong"),
        Lsx.Attribute("Icon", "FixedString", value="fcff3667-ddc0-1b32-2b7f-1acedfa0cf50-_(Icon_Human_Female_Strong)"),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(abyssal_tiefling_female_player_strong_uuid)),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling_Female_Player_Strong"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value=str(abyssal_tiefling_female_player_uuid)),
        Lsx.Attribute("PortraitVisualResourceID", "FixedString", value="f1cdcf6d-7469-14ec-380f-3cb5df440340"),
        Lsx.Attribute("Type", "FixedString", value="character"),
        Lsx.Attribute("_OriginalFileVersion_", "int64", value="144115207403209034"),
    ], children=[
        Lsx.Node("LocomotionParams"),
        Lsx.Node("Tags", children=[
            Lsx.Node("Tag", [
                Lsx.Attribute("Object", "guid", value="d3116e58-c55a-4853-a700-bee996207397"),
            ]),
        ]),
    ]),

    # Abyssal Tiefling Male Base
    Lsx.Node("GameObjects", [
        Lsx.Attribute("CharacterVisualResourceID", "FixedString", value="576a9e8f-88f2-fbdc-5103-4591553e6bef"),
        Lsx.Attribute("GeneratePortrait", "LSString", value="Icon_Tiefling_Male"),
        Lsx.Attribute("Icon", "FixedString", value="576a9e8f-88f2-fbdc-5103-4591553e6bef-_(Icon_Tiefling_Male)"),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(abyssal_tiefling_male_base_uuid)),
        Lsx.Attribute("Name", "LSString", value="AbyssalTiefling_Male_Base"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value="b63752c4-0fad-4c1b-8da2-fee201253734"),
        Lsx.Attribute("Race", "guid", value=str(abyssal_tiefling_race_uuid)),
        Lsx.Attribute("Type", "FixedString", value="character"),
        Lsx.Attribute("_OriginalFileVersion_", "int64", value="1"),
    ], children=[
        Lsx.Node("GameMaster"),
        Lsx.Node("LocomotionParams"),
    ]),

    # Abyssal Tiefling Male Player
    Lsx.Node("GameObjects", [
        Lsx.Attribute("CharacterVisualResourceID", "FixedString", value="a178a41d-05c3-3bc8-4879-15d2effe3300"),
        Lsx.Attribute("Icon", "FixedString", value="a178a41d-05c3-3bc8-4879-15d2effe3300-_(Icon_Tiefling_Male)"),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(abyssal_tiefling_male_player_uuid)),
        Lsx.Attribute("Name", "LSString", value="Tieflings_Male_Asmodeus_Player"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value=str(abyssal_tiefling_male_base_uuid)),
        Lsx.Attribute("PortraitVisualResourceID", "FixedString", value="35fa926e-18f4-2d3e-872a-04ab9e95b76c"),
        Lsx.Attribute("SpellSet", "FixedString", value="CommonPlayerActions"),
        Lsx.Attribute("Stats", "FixedString", value="HeroTieflingMale"),
        Lsx.Attribute("Type", "FixedString", value="character"),
        Lsx.Attribute("_OriginalFileVersion_", "int64", value="144115207403209034"),
    ], children=[
        Lsx.Node("LocomotionParams"),
        Lsx.Node("SpeakerGroupList", children=[
            Lsx.Node("SpeakerGroup", [
                Lsx.Attribute("Object", "guid", value="02cdc15e-1dc3-5eb4-f73c-9458b4f90b9f"),
            ]),
            Lsx.Node("SpeakerGroup", [
                Lsx.Attribute("Object", "guid", value="e0d1ff71-04a8-4340-ae64-9684d846eb83"),
            ]),
        ]),
    ]),

    # Abyssal Tiefling Male Player Strong
    Lsx.Node("GameObjects", [
        Lsx.Attribute("CharacterVisualResourceID", "FixedString", value="351d13d4-a4de-0dd0-24df-3a194285c7e6"),
        Lsx.Attribute("EquipmentRace", "guid", value="f625476d-29ec-4a6d-9086-42209af0cf6f"),
        Lsx.Attribute("GeneratePortrait", "LSString", value="Icon_Human_Male_Strong"),
        Lsx.Attribute("Icon", "FixedString", value="351d13d4-a4de-0dd0-24df-3a194285c7e6-_(Icon_Human_Male_Strong)"),
        Lsx.Attribute("LevelName", "FixedString", value=""),
        Lsx.Attribute("MapKey", "FixedString", value=str(abyssal_tiefling_male_player_strong_uuid)),
        Lsx.Attribute("Name", "LSString", value="Tieflings_Male_Asmodeus_Player_Strong"),
        Lsx.Attribute("ParentTemplateId", "FixedString", value=str(abyssal_tiefling_male_player_uuid)),
        Lsx.Attribute("PortraitVisualResourceID", "FixedString", value="a9afff3b-121d-085e-12af-9e9fb07c788f"),
        Lsx.Attribute("Type", "FixedString", value="character"),
        Lsx.Attribute("_OriginalFileVersion_", "int64", value="144115207403209034"),
    ], children=[
        Lsx.Node("LocomotionParams"),
        Lsx.Node("Tags", children=[
            Lsx.Node("Tag", [
                Lsx.Attribute("Object", "guid", value="d3116e58-c55a-4853-a700-bee996207397"),
            ]),
        ]),
    ]),
])

abyssal_tiefling.build()
