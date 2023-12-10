#!/usr/bin/env python3

import os.path
import textwrap

base_dir = os.path.dirname(__file__) or '.'
max_boost = 16
attributes = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

# Generate the passives
with open(os.path.join(base_dir, "Public", "Serenade", "Stats", "Generated", "Data", "Prodigy.txt"), "w") as f:
    f.write(textwrap.dedent("""\
        new entry "Serenade_Prodigy"
        type "PassiveData"
        data "DisplayName" "Serenade_Prodigy_DisplayName"
        data "Description" "Serenade_Prodigy_Description"
        data "Icon" "Action_KnowledgeOfTheAges"
        data "Properties" "Highlighted"

        """))

    attribute_icon = {
        "Strength":     "Spell_Transmutation_EnhanceAbility_BullsStrenght",
        "Dexterity":    "Spell_Transmutation_EnhanceAbility_CatsGrace",
        "Constitution": "Spell_Transmutation_EnhanceAbility_BearsEndurance",
        "Intelligence": "Spell_Transmutation_EnhanceAbility_FoxsCunning",
        "Wisdom":       "Spell_Transmutation_EnhanceAbility_OwlsWisdom",
        "Charisma":     "Spell_Transmutation_EnhanceAbility_EaglesSplendor",
    }

    for attribute in attributes:
        f.write(textwrap.dedent(f"""\
            new entry "Serenade_{attribute}_0"
            type "PassiveData"
            data "DisplayName" "Serenade_{attribute}_0_DisplayName"
            data "Description" "Serenade_{attribute}_0_Description"
            data "Icon" "{attribute_icon[attribute]}"
            data "Properties" "IsHidden"

            """))

        for boost in range(2, max_boost + 2, 2):
            f.write(textwrap.dedent(f"""\
                new entry "Serenade_{attribute}_{boost}"
                type "PassiveData"
                data "Boosts" "Ability({attribute}, {boost}, 30)
                data "DisplayName" "Serenade_{attribute}_{boost}_DisplayName"
                data "Description" "Serenade_{attribute}_{boost}_Description"
                data "Icon" "{attribute_icon[attribute]}"
                data "Properties" "IsHidden"

                """))

# Generate the passive lists
with open(os.path.join(base_dir, "Public", "Serenade", "Lists", "PassiveLists.lsx"), "w") as f:
    attribute_guid = {
        "Strength":     "522041f0-d2af-43b7-9662-f8199b0b96e5",
        "Dexterity":    "a81788e5-6949-474b-9700-87864c4c510c",
        "Constitution": "fb9a4b78-4964-4344-b6f7-510709ce6d76",
        "Intelligence": "4fff72e3-3cc4-4208-8f08-7a73501b3a81",
        "Wisdom":       "47418954-13db-4017-bcca-b8ca9a109a46",
        "Charisma":     "eb2ac0f3-1abf-43ac-aa51-afbfdc32b06a",
    }

    f.write(textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <save>
            <version major="4" minor="1" revision="1" build="0"/>
            <region id="PassiveLists">
                <node id="root">
                    <children>
        """))

    for attribute in attributes:
        boosts = [f"Serenade_{attribute}_{boost}" for boost in range(0, max_boost + 2, 2)]
        f.write(textwrap.indent(textwrap.dedent(f"""\
            <node id="PassiveList">
                <attribute id="Passives" type="LSString" value="{",".join(boosts)}"/>
                <attribute id="UUID" type="guid" value="{attribute_guid[attribute]}"/>
            </node>
            """),
                " " * 4 * 4))

    f.write(textwrap.dedent("""\
                    </children>
                </node>
            </region>
        </save>
        """))
