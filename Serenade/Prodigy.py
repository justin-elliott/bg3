#!/usr/bin/env python3

"""
Generates the files for the "Prodigy" ability enhancement feat.
"""

import os.path
import re
import textwrap

base_dir = os.path.dirname(__file__) or '.'

attribute_step = 2
max_attribute_bonus = 12

roll_bonus_step = 4
max_roll_bonus = 20

attributes = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

training = {
    "NoTraining": {
        "Name": "No Training",
        "Description": "Do not select any training.",
    },

    "Brawler": {
        "Name": "Prodigy: Brawler",
        "Description": """
            On selecting this training, you receive <LSTag Type="Passive" Tooltip="Alert">Alert</LSTag>,
            <LSTag Type="Passive" Tooltip="MartialArts_BonusUnarmedStrike">Bonus Unarmed Strike</LSTag>, and
            <LSTag Type="Passive" Tooltip="TavernBrawler">Tavern Brawler</LSTag>.

            <br><br>At level 5, you receive <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Dash_BonusAction">Dash: Bonus Action</LSTag>.

            <br><br>At level 9, you receive <LSTag Type="Passive" Tooltip="FastHands">Fast Hands</LSTag>, and
            <LSTag Type="Spell" Tooltip="Serenade_ProdigySpinningKick">Spinning Kick</LSTag>.

            <br><br>Finally, at level 11, you receive <LSTag Type="Passive" Tooltip="ExtraAttack_2">Improved Extra Attack</LSTag>.
            """,
        "Icon": "Action_Monk_FlurryOfBlows",
        "Progression": {
            range(1, 21): {
                "Passives": ["Alert",
                             "MartialArts_BonusUnarmedStrike",
                             "TavernBrawler"],
            },
            range(5, 11): {
                "Passives": ["ExtraAttack"],
                "Boosts": ["UnlockSpell(Shout_Dash_BonusAction)"],
            },
            range(9, 21): {
                "Passives": ["FastHands"],
                "Boosts": ["UnlockSpell(Serenade_ProdigySpinningKick)"],
            },
            range(11, 21): {
                "Passives": ["ExtraAttack_2"],
            },
        },
    },

    "GreatWeapons": {
        "Name": "Prodigy: Great Weapons",
        "Description": """
            On selecting this training, you receive <LSTag Type="Passive" Tooltip="FightingStyle_GreatWeaponFighting">Great Weapon Fighting</LSTag>
            and <LSTag Type="Passive" Tooltip="Serenade_ProdigyGreatWeaponMaster">Great Weapon Master</LSTag>.

            <br><br>At level 5, you receive <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Dash_BonusAction">Dash: Bonus Action</LSTag>.

            <br><br>At level 9, you receive <LSTag Type="Passive" Tooltip="FastHands">Fast Hands</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Whirlwind">Whirlwind</LSTag>.

            <br><br>Finally, at level 11, you receive <LSTag Type="Passive" Tooltip="ExtraAttack_2">Improved Extra Attack</LSTag>.
            """,
        "Icon": "PassiveFeature_FightingStyle_GreatWeaponFighting",
        "Progression": {
            range(1, 21): {
                "Passives": ["FightingStyle_GreatWeaponFighting",
                             "GreatWeaponMaster_BonusAttack",
                             "GreatWeaponMaster_BonusDamage"],
            },
            range(5, 11): {
                "Passives": ["ExtraAttack"],
                "Boosts": ["UnlockSpell(Shout_Dash_BonusAction)"],
            },
            range(9, 21): {
                "Passives": ["FastHands"],
                "Boosts": ["UnlockSpell(Shout_Whirlwind)"],
            },
            range(11, 21): {
                "Passives": ["ExtraAttack_2"],
            },
        },
    },

    "DualWielding": {
        "Name": "Prodigy: Dual Wielding",
        "Description": """
            On selecting this training, you receive <LSTag Type="Passive" Tooltip="FightingStyle_TwoWeaponFighting">Two-Weapon Fighting</LSTag>
            and <LSTag Type="Passive" Tooltip="Serenade_ProdigyDualWielder">Dual Wielder</LSTag>.

            <br><br>At level 5, you receive <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Dash_BonusAction">Dash: Bonus Action</LSTag>.

            <br><br>At level 9, you receive <LSTag Type="Passive" Tooltip="FastHands">Fast Hands</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Whirlwind">Whirlwind</LSTag>.

            <br><br>Finally, at level 11, you receive <LSTag Type="Passive" Tooltip="ExtraAttack_2">Improved Extra Attack</LSTag>.
            """,
        "Icon": "PassiveFeature_FightingStyle_TwoWeaponFighting",
        "Progression": {
            range(1, 21): {
                "Passives": ["FightingStyle_TwoWeaponFighting",
                             "DualWielder_BonusAC",
                             "DualWielder_PassiveBonuses"],
            },
            range(5, 11): {
                "Passives": ["ExtraAttack"],
                "Boosts": ["UnlockSpell(Shout_Dash_BonusAction)"],
            },
            range(9, 21): {
                "Passives": ["FastHands"],
                "Boosts": ["UnlockSpell(Shout_Whirlwind)"],
            },
            range(11, 21): {
                "Passives": ["ExtraAttack_2"],
            },
        },
    },

    "Archery": {
        "Name": "Prodigy: Archery",
        "Description": """
            On selecting this training, you receive <LSTag Type="Passive" Tooltip="FightingStyle_Archery">Archery</LSTag>
            and <LSTag Type="Passive" Tooltip="Serenade_ProdigySharpshooter">Sharpshooter</LSTag>.

            <br><br>At level 5, you receive <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Dash_BonusAction">Dash: Bonus Action</LSTag>.

            <br><br>At level 9, you receive <LSTag Type="Passive" Tooltip="FastHands">Fast Hands</LSTag>, and
            <LSTag Type="Spell" Tooltip="Target_Volley">Volley</LSTag>.

            <br><br>Finally, at level 11, you receive <LSTag Type="Passive" Tooltip="ExtraAttack_2">Improved Extra Attack</LSTag>.
            """,
        "Icon": "PassiveFeature_FightingStyle_Archery",
        "Progression": {
            range(1, 21): {
                "Passives": ["FightingStyle_Archery",
                             "Sharpshooter_AllIn",
                             "Sharpshooter_Bonuses"],
            },
            range(5, 11): {
                "Passives": ["ExtraAttack"],
                "Boosts": ["UnlockSpell(Shout_Dash_BonusAction)"],
            },
            range(9, 21): {
                "Passives": ["FastHands"],
                "Boosts": ["UnlockSpell(Target_Volley)"],
            },
            range(11, 21): {
                "Passives": ["ExtraAttack_2"],
            },
        },
    },

    "Magic": {
        "Name": "Prodigy: Magic",
        "Description": """
            On selecting this training, you receive <LSTag Type="Passive" Tooltip="Alert">Alert</LSTag>,
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyWarCaster">War Caster</LSTag>,
            <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> on
            <LSTag Tooltip="Constitution">Constitution</LSTag> <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>, and
            2 level 1 <LSTag Tooltip="SpellSlot">Spell Slots</LSTag>. At every successive odd level, including levels
            already attained when you take this training, you gain an additional spell slot of the appropriate level for
            a full spellcaster.

            <br><br>At level 4, you gain 3 <LSTag Type="ActionResource" Tooltip="SorceryPoint">Sorcery Points</LSTag>,
            <LSTag Type="Passive" Tooltip="Metamagic_Twinned">Twinned Spell</LSTag> and
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyRestoreSorceryPoints">Restore Sorcery Points</LSTag>.

            <br><br>At level 7, you gain 3 additional Sorcery Points and
            <LSTag Type="Passive" Tooltip="Metamagic_Quickened">Quickened Spell</LSTag>. At level 11, you gain a further
            3 Sorcery Points and <LSTag Type="Passive" Tooltip="Metamagic_Heightened">Heightened Spell</LSTag>.
            """,
        "Icon": "Action_KnowledgeOfTheAges",
        "Progression": {
            range(1, 21): {
                "Passives": ["Alert",
                             "WarCaster_Bonuses",
                             "WarCaster_OpportunitySpell",
                             "UnlockedSpellSlotLevel1"],
                "Boosts": ["ActionResource(SpellSlot,2,1)",
                           "ProficiencyBonus(SavingThrow,Constitution)"],
            },
            range(3, 21): {
                "Passives": ["UnlockedSpellSlotLevel2"],
                "Boosts": ["ActionResource(SpellSlot,1,2)"],
            },
            range(4, 21): {
                "Passives": ["Metamagic_Twinned",
                             "Serenade_ProdigyRestoreSorceryPoints"],
                "Boosts": ["ActionResource(SorceryPoint,3,0)",
                           "Tag(SORCERER_METAMAGIC)"],
            },
            range(5, 21): {
                "Passives": ["UnlockedSpellSlotLevel3"],
                "Boosts": ["ActionResource(SpellSlot,1,3)"],
            },
            range(7, 21): {
                "Passives": ["Metamagic_Quickened"],
                "Boosts": ["ActionResource(SpellSlot,1,4)",
                           "ActionResource(SorceryPoint,3,0)"],
            },
            range(9, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,5)"],
            },
            range(11, 21): {
                "Passives": ["Metamagic_Heightened"],
                "Boosts": ["ActionResource(SpellSlot,1,6)",
                           "ActionResource(SorceryPoint,3,0)"],
            },
            range(13, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,7)"],
            },
            range(15, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,8)",
                           "ActionResource(SorceryPoint,3,0)"],
            },
            range(17, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,9)"],
            },
        },
    },
}

# Generate the passives
with open(os.path.join(base_dir, "Public", "Serenade", "Stats", "Generated", "Data", "Prodigy.txt"), "w") as f:
    f.write(textwrap.dedent(f"""\
        // DO NOT EDIT: This file was automatically generated by {os.path.basename(__file__)}

        new entry "Serenade_Prodigy"
        type "PassiveData"
        data "DisplayName" "Serenade_Prodigy_DisplayName"
        data "Description" "Serenade_Prodigy_Description"
        data "Icon" "Action_KnowledgeOfTheAges"
        data "Properties" "Highlighted"
        data "StatsFunctorContext" "OnCreate;OnShortRest;OnLongRest;OnStatusApplied;OnStatusRemoved"
        data "StatsFunctors" "ApplyStatus(SERENADE_PRODIGY,100,1)"

        new entry "SERENADE_PRODIGY"
        type "StatusData"
        data "StatusType" "BOOST"
        data "DisplayName" "Serenade_Prodigy_DisplayName"
        data "Description" "Serenade_Prodigy_Description"
        data "Icon" "Action_KnowledgeOfTheAges"
        data "StackId" "SERENADE_PRODIGY"
        data "StackType" "Ignore"
        data "StatusGroups" "SG_RemoveOnRespec"
        data "StatusPropertyFlags" "DisableOverhead;DisableImmunityOverhead;DisablePortraitIndicator;DisableCombatlog;IgnoreResting"

        new entry "Serenade_ProdigyRestoreSorceryPoints"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyRestoreSorceryPoints_DisplayName"
        data "Description" "Serenade_ProdigyRestoreSorceryPoints_Description"
        data "Icon" "Skill_Sorcerer_CreateSorceryPoints_1"
        data "Properties" "Highlighted"
        data "StatsFunctorContext" "OnCreate"
        data "StatsFunctors" "ApplyStatus(SELF,SERENADE_PRODIGYRESTORESORCERYPOINTS,100,-1)"

        new entry "SERENADE_PRODIGYRESTORESORCERYPOINTS"
        type "StatusData"
        data "StatusType" "BOOST"
        data "DisplayName" "Serenade_ProdigyRestoreSorceryPoints_DisplayName"
        data "Description" "Serenade_ProdigyRestoreSorceryPoints_Description"
        data "Icon" "Skill_Sorcerer_CreateSorceryPoints_1"
        data "StackId" "SERENADE_PRODIGYRESTORESORCERYPOINTS"
        data "StackType" "Overwrite"
        data "TickType" "StartTurn"
        data "TickFunctors" "RestoreResource(SorceryPoint,1,0)"
        data "StatusGroups" "SG_RemoveOnRespec"
        data "StatusPropertyFlags" "DisableOverhead;DisableImmunityOverhead;DisablePortraitIndicator;DisableCombatlog;IgnoreResting"

        new entry "Serenade_ProdigyGreatWeaponMaster"
        type "PassiveData"
        data "DisplayName" "hf41eb2bag6496g4187g994dg62b9cb959e29;1"
        data "Description" "hea61c527gd53fg46fega454g2bc02f65d75f;5"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyDualWielder"
        type "PassiveData"
        data "DisplayName" "h1d620270gba24g434egad17g5ee9b72a6e3e;1"
        data "Description" "h1909840bg87f1g4029g9be6g974d9233f516;4"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigySharpshooter"
        type "PassiveData"
        data "DisplayName" "h7fd575c5g3a3ag46a8g9a40gcddf1cd2b044;1"
        data "Description" "h0bf50988g8a65g40c1ga9e1g2ad5b6387678;3"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyWarCaster"
        type "PassiveData"
        data "DisplayName" "haadef5acg36f8g4affg8c7bg7901735048a8;2"
        data "Description" "h2967e308gd644g46d5g91e4g3de62873eef7;5"
        data "Properties" "IsHidden"
        """))

    attribute_icon = {
        "Strength":     "Spell_Transmutation_EnhanceAbility_BullsStrenght",
        "Dexterity":    "Spell_Transmutation_EnhanceAbility_CatsGrace",
        "Constitution": "Spell_Transmutation_EnhanceAbility_BearsEndurance",
        "Intelligence": "Spell_Transmutation_EnhanceAbility_FoxsCunning",
        "Wisdom":       "Spell_Transmutation_EnhanceAbility_OwlsWisdom",
        "Charisma":     "Spell_Transmutation_EnhanceAbility_EaglesSplendor",
    }

    # Attribute bonuses
    for attribute in attributes:
        f.write(textwrap.dedent(f"""\

            new entry "Serenade_Prodigy{attribute}_0"
            type "PassiveData"
            data "DisplayName" "Serenade_Prodigy_NoBonus_DisplayName"
            data "Description" "Serenade_Prodigy{attribute}_NoBonus_Description"
            data "Icon" "{attribute_icon[attribute]}"
            data "Properties" "IsHidden"
            """))

        for bonus in range(attribute_step, max_attribute_bonus + attribute_step, attribute_step):
            f.write(textwrap.dedent(f"""\

                new entry "Serenade_Prodigy{attribute}_{bonus}"
                type "PassiveData"
                data "Boosts" "Ability({attribute},{bonus},30)"
                data "DisplayName" "Serenade_Prodigy{attribute}_{bonus}_DisplayName"
                data "Description" "Serenade_Prodigy{attribute}_{bonus}_Description"
                data "Icon" "{attribute_icon[attribute]}"
                data "Properties" "IsHidden"
                """))

        f.write(textwrap.dedent("""\

            new entry "Serenade_ProdigyRollBonus_0"
            type "PassiveData"
            data "DisplayName" "Serenade_Prodigy_NoBonus_DisplayName"
            data "Description" "Serenade_ProdigyRollBonus_NoBonus_Description"
            data "Icon" "PassiveFeature_Portent"
            data "Properties" "IsHidden"
            """))

    # Skill and ability bonuses
    for bonus in range(roll_bonus_step, max_roll_bonus + roll_bonus_step, roll_bonus_step):
        f.write(textwrap.dedent(f"""\

            new entry "Serenade_ProdigyRollBonus_{bonus}"
            type "PassiveData"
            data "Boosts" "RollBonus(SkillCheck,{bonus});RollBonus(RawAbility,{bonus})"
            data "DisplayName" "Serenade_ProdigyRollBonus_{bonus}_DisplayName"
            data "Description" "Serenade_ProdigyRollBonus_{bonus}_Description"
            data "Icon" "{f"PassiveFeature_Portent_{bonus}" if bonus <= 20 else f"PassiveFeature_Portent"}"
            data "Properties" "IsHidden"
            """))

    # Training
    for key, train in training.items():
        f.write(textwrap.dedent(f"""\

            new entry "Serenade_Prodigy{key}"
            type "PassiveData"
            data "DisplayName" "Serenade_Prodigy{key}_DisplayName"
            data "Description" "Serenade_Prodigy{key}_Description"
            data "Properties" "{"Highlighted" if "Progression" in train else "IsHidden"}"
            """))

        if (icon := train.get("Icon", None)):
            f.write(f"""data "Icon" "{icon}"\n""")

        levels = set()
        if (progression := train.get("Progression", None)):
            f.write("""data "StatsFunctorContext" "OnCreate;OnShortRest;OnLongRest;OnStatusApplied;OnStatusRemoved"\n""")
            levels = set([r.start for r in progression.keys()])
            boosts = [f"SERENADE_PRODIGY{key.upper()}_{level}" for level in sorted(levels)]
            f.write(f"""data "StatsFunctors" "{";".join([f"ApplyStatus({boost},100,-1)" for boost in boosts])}"\n""")

        for level in sorted(levels):
            f.write(textwrap.dedent(f"""\

                new entry "SERENADE_PRODIGY{key.upper()}_{level}"
                type "StatusData"
                data "StatusType" "BOOST"
                data "DisplayName" "Serenade_Prodigy{key}_DisplayName"
                data "Description" "Serenade_Prodigy{key}_Description"
                data "StackId" "SERENADE_PRODIGY{key.upper()}_{level}"
                data "StackType" "Ignore"
                data "StatusGroups" "SG_RemoveOnRespec"
                data "StatusPropertyFlags" "DisableOverhead;DisableImmunityOverhead;DisablePortraitIndicator;DisableCombatlog;IgnoreResting"
                """))
            if (icon := train.get("Icon", None)):
                f.write(f"""data "Icon" "{icon}"\n""")

            for level_range, settings in progression.items():
                if level_range.start == level:
                    conditions_list = []
                    if (level_range.start > 1):
                        conditions_list.append(f"CharacterLevelGreaterThan({level_range.start - 1})")
                    if (level_range.stop < 21):
                        conditions_list.append(f"not CharacterLevelGreaterThan({level_range.stop - 1})")
                    conditions = " and ".join(conditions_list)
                    if len(conditions) > 0:
                        f.write(f"""data "OnApplyConditions" "{conditions}"\n""")
                    if (passives := settings.get("Passives", None)):
                        f.write(f"""data "Passives" "{";".join(passives)}"\n""")

                    if (boosts := settings.get("Boosts", None)):
                        f.write(f"""data "Boosts" "{";".join([
                                    f"IF({conditions}):{boost}" for boost in boosts
                                ] if len(conditions) > 0 else boosts)}"\n""")

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

    # No Training always comes first
    training_names = [f"Serenade_Prodigy{key}" for key in sorted(training.keys(),
                                                                 key=lambda k: (1, k) if k != "NoTraining" else (0, k))]

    f.write(textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!-- DO NOT EDIT: This file was automatically generated by {os.path.basename(__file__)} -->
        <save>
            <version major="4" minor="1" revision="1" build="0"/>
            <region id="PassiveLists">
                <node id="root">
                    <children>
                        <node id="PassiveList">
                            <attribute id="Passives" type="LSString" value="{",".join(training_names)}"/>
                            <attribute id="UUID" type="guid" value="b7d72358-f348-4c78-8e42-a743b16a2c2c"/>
                        </node>
        """))

    for attribute in attributes:
        attribute_bonuses = [f"Serenade_Prodigy{attribute}_{bonus}"
                             for bonus in range(0, max_attribute_bonus + attribute_step, attribute_step)]
        f.write(textwrap.indent(textwrap.dedent(f"""\
            <node id="PassiveList">
                <attribute id="Passives" type="LSString" value="{",".join(attribute_bonuses)}"/>
                <attribute id="UUID" type="guid" value="{attribute_guid[attribute]}"/>
            </node>
            """),
                " " * 4 * 4))

    roll_bonuses = [f"Serenade_ProdigyRollBonus_{bonus}"
                    for bonus in range(0, max_roll_bonus + roll_bonus_step, roll_bonus_step)]
    f.write(textwrap.dedent(f"""\
                        <node id="PassiveList">
                            <attribute id="Passives" type="LSString" value="{",".join(roll_bonuses)}"/>
                            <attribute id="UUID" type="guid" value="12b2f031-1837-46d6-ae05-50a3490b6065"/>
                        </node>
                    </children>
                </node>
            </region>
        </save>
        """))


def xmlString(s):
    s = re.sub("\\s{2,}", " ", s.strip())
    s = re.sub("<", "&lt;", s)
    s = re.sub(">", "&gt;", s)
    return s


# Generate the English localization
with open(os.path.join(base_dir, "Localization", "English", "Prodigy.loca.xml"), "w") as f:
    f.write(textwrap.dedent(f"""\
        <?xml version="1.0" encoding="utf-8"?>
        <!-- DO NOT EDIT: This file was automatically generated by {os.path.basename(__file__)} -->
        <contentList>
            <content contentuid="Serenade_Prodigy_NoBonus_DisplayName" version="1">No Bonus</content>
            <content contentuid="Serenade_ProdigyRestoreSorceryPoints_DisplayName" version="1">Prodigy: Restore Sorcery Points</content>
            <content contentuid="Serenade_ProdigyRestoreSorceryPoints_Description" version="1">Every turn, you restore 1 &lt;LSTag Type="ActionResource" Tooltip="SorceryPoint"&gt;Sorcery Point&lt;/LSTag&gt;.</content>
        """))

    for attribute in attributes:
        f.write(textwrap.indent(textwrap.dedent(f"""\
            <content contentuid="Serenade_Prodigy{attribute}_DisplayName" version="1">Prodigy: {attribute}</content>
            <content contentuid="Serenade_Prodigy{attribute}_Description" version="1">Add a bonus to your &lt;LSTag Tooltip="{attribute}"&gt;{attribute}&lt;/LSTag&gt;.</content>
            <content contentuid="Serenade_Prodigy{attribute}_NoBonus_Description" version="1">No bonus to &lt;LSTag Tooltip="{attribute}"&gt;{attribute}&lt;/LSTag&gt;.</content>
            """),
                " " * 4 * 1))

        for bonus in range(attribute_step, max_attribute_bonus + attribute_step, attribute_step):
            f.write(textwrap.indent(textwrap.dedent(f"""\
                <content contentuid="Serenade_Prodigy{attribute}_{bonus}_DisplayName" version="1">Prodigy: {attribute} +{bonus}</content>
                <content contentuid="Serenade_Prodigy{attribute}_{bonus}_Description" version="1">Increase your &lt;LSTag Tooltip="{attribute}"&gt;{attribute}&lt;/LSTag&gt; by {bonus}, to a maximum of 30.</content>
                """),
                    " " * 4 * 1))

    f.write(textwrap.indent(textwrap.dedent("""\
        <content contentuid="Serenade_ProdigyRollBonus_DisplayName" version="1">Prodigy: Roll Bonus</content>
        <content contentuid="Serenade_ProdigyRollBonus_Description" version="1">Add a bonus to your &lt;LSTag Tooltip="SkillCheck"&gt;Skill&lt;/LSTag&gt; and &lt;LSTag Tooltip="AbilityCheck"&gt;Ability&lt;/LSTag&gt; checks.</content>
        <content contentuid="Serenade_ProdigyRollBonus_NoBonus_Description" version="1">No bonus to your &lt;LSTag Tooltip="SkillCheck"&gt;Skill&lt;/LSTag&gt; and &lt;LSTag Tooltip="AbilityCheck"&gt;Ability&lt;/LSTag&gt; checks.</content>
        """),
            " " * 4 * 1))

    for bonus in range(roll_bonus_step, max_roll_bonus + roll_bonus_step, roll_bonus_step):
        f.write(textwrap.indent(textwrap.dedent(f"""\
            <content contentuid="Serenade_ProdigyRollBonus_{bonus}_DisplayName" version="1">Prodigy: Roll Bonus +{bonus}</content>
            <content contentuid="Serenade_ProdigyRollBonus_{bonus}_Description" version="1">Add {bonus} to your &lt;LSTag Tooltip="SkillCheck"&gt;Skill&lt;/LSTag&gt; and &lt;LSTag Tooltip="AbilityCheck"&gt;Ability&lt;/LSTag&gt; checks.</content>
            """),
                " " * 4 * 1))

    for key, train in training.items():
        f.write(textwrap.indent(textwrap.dedent(f"""\
            <content contentuid="Serenade_Prodigy{key}_DisplayName" version="1">{train["Name"]}</content>
            <content contentuid="Serenade_Prodigy{key}_Description" version="1">{xmlString(train["Description"])}</content>
            """),
                " " * 4 * 1))

    f.write(textwrap.dedent("""\
        </contentList>
        """))
