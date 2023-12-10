#!/usr/bin/env python3

import os.path
import textwrap

base_dir = os.path.dirname(__file__) or '.'
max_boost = 16

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

    for attribute in attribute_icon.keys():
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
