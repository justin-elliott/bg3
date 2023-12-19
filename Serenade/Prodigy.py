#!/usr/bin/env python3

"""
Generates the files for the "Prodigy" ability enhancement feat.
"""

import os.path
import re
import textwrap

import xml.etree.ElementTree as ElementTree

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

    "Archer": {
        "Name": "Prodigy: Archer",
        "Description": """
            On selecting this training, you receive <LSTag Type="Passive" Tooltip="FightingStyle_Archery">Archery</LSTag>
            and <LSTag Type="Passive" Tooltip="Serenade_ProdigySharpshooterFeat">Sharpshooter</LSTag>.

            <br><br>At level 5, you receive <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Dash_CunningAction">Cunning Action: Dash</LSTag>.

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
                "Boosts": ["UnlockSpell(Shout_Dash_CunningAction)"],
            },
            range(9, 21): {
                "Passives": ["FastHands"],
                "Boosts": ["UnlockSpell(Target_Volley)"],
            },
            range(11, 21): {
                "Passives": ["ExtraAttack_2"],
                "Boosts": ["UnlockSpell(Shout_Dash_CunningAction)"],
            },
        },
    },

    "Athlete": {
        "Name": "Prodigy: Athlete",
        "Description": """
            At level 8, you receive
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyAthleteFeat">Athlete</LSTag>,
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyMobileFeat">Mobile</LSTag>, and
            <LSTag Type="Passive" Tooltip="Tough">Tough</LSTag>.
            """,
        "Icon": "PassiveFeature_RemarkableAthlete_Jump",
        "Progression": {
            range(8, 21): {
                "Passives": ["Athlete_StandUp",
                             "Mobile_PassiveBonuses",
                             "Mobile_CounterAttackOfOpportunity",
                             "Mobile_DashAcrossDifficultTerrain",
                             "Tough"],
            },
        },
    },

    "DualWielder": {
        "Name": "Prodigy: Dual Wielder",
        "Description": """
            On selecting this training, you receive <LSTag Type="Passive" Tooltip="FightingStyle_TwoWeaponFighting">Two-Weapon Fighting</LSTag>
            and <LSTag Type="Passive" Tooltip="Serenade_ProdigyDualWielderFeat">Dual Wielder</LSTag>.

            <br><br>At level 5, you receive <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Dash_CunningAction">Cunning Action: Dash</LSTag>.

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
                "Boosts": ["UnlockSpell(Shout_Dash_CunningAction)"],
            },
            range(9, 21): {
                "Passives": ["FastHands"],
                "Boosts": ["UnlockSpell(Shout_Whirlwind)"],
            },
            range(11, 21): {
                "Passives": ["ExtraAttack_2"],
                "Boosts": ["UnlockSpell(Shout_Dash_CunningAction)"],
            },
        },
    },

    "Duellist": {
        "Name": "Prodigy: Duellist",
        "Description": """
            On selecting this training, you receive
            <LSTag Type="Passive" Tooltip="FightingStyle_Dueling">Duelling</LSTag>,
            <LSTag Type="Passive" Tooltip="FightingStyle_Protection">Protection</LSTag>,
            <LSTag Type="Passive" Tooltip="DefensiveDuelist">Defensive Duellist</LSTag>, and
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyShieldMasterFeat">Shield Master</LSTag>.

            <br><br>At level 5, you receive <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Dash_CunningAction">Cunning Action: Dash</LSTag>.

            <br><br>At level 9, you receive <LSTag Type="Passive" Tooltip="FastHands">Fast Hands</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Whirlwind">Whirlwind</LSTag>.

            <br><br>Finally, at level 11, you receive <LSTag Type="Passive" Tooltip="ExtraAttack_2">Improved Extra Attack</LSTag>.
            """,
        "Icon": "PassiveFeature_FightingStyle_Duelling",
        "Progression": {
            range(1, 21): {
                "Passives": ["FightingStyle_Dueling",
                             "FightingStyle_Protection",
                             "DefensiveDuelist",
                             "ShieldMaster_PassiveBonuses",
                             "ShieldMaster_Block"],
            },
            range(5, 11): {
                "Passives": ["ExtraAttack"],
                "Boosts": ["UnlockSpell(Shout_Dash_CunningAction)"],
            },
            range(9, 21): {
                "Passives": ["FastHands"],
                "Boosts": ["UnlockSpell(Shout_Whirlwind)"],
            },
            range(11, 21): {
                "Passives": ["ExtraAttack_2"],
                "Boosts": ["UnlockSpell(Shout_Dash_CunningAction)"],
            },
        },
    },

    "GreatWeaponMaster": {
        "Name": "Prodigy: Great Weapon Master",
        "Description": """
            On selecting this training, you receive <LSTag Type="Passive" Tooltip="FightingStyle_GreatWeaponFighting">Great Weapon Fighting</LSTag>
            and <LSTag Type="Passive" Tooltip="Serenade_ProdigyGreatWeaponMasterFeat">Great Weapon Master</LSTag>.

            <br><br>At level 5, you receive <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Dash_CunningAction">Cunning Action: Dash</LSTag>.

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
                "Boosts": ["UnlockSpell(Shout_Dash_CunningAction)"],
            },
            range(9, 21): {
                "Passives": ["FastHands"],
                "Boosts": ["UnlockSpell(Shout_Whirlwind)"],
            },
            range(11, 21): {
                "Passives": ["ExtraAttack_2"],
                "Boosts": ["UnlockSpell(Shout_Dash_CunningAction)"],
            },
        },
    },

    "Metamage": {
        "Name": "Prodigy: Metamage",
        "Description": """
            On selecting this training, you receive
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyWarCasterFeat">War Caster</LSTag>, and
            <LSTag Type="Tooltip" Tooltip="ProficiencyBonus">Proficiency</LSTag> on
            <LSTag Tooltip="Constitution">Constitution</LSTag> <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>.

            <br><br>At level 4, you gain 5 <LSTag Type="ActionResource" Tooltip="SorceryPoint">Sorcery Points</LSTag>,
            <LSTag Type="Passive" Tooltip="Metamagic_Twinned">Twinned Spell</LSTag>, and
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyRestoreSorceryPoints">Restore Sorcery Points</LSTag>.

            <br><br>At level 7, you gain 5 additional Sorcery Points,
            <LSTag Type="Passive" Tooltip="Metamagic_Quickened">Quickened Spell</LSTag>, and
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyEmpoweredMagic">Empowered Magic</LSTag>.

            <br><br>At level 11, you gain a further 5 Sorcery Points,
            <LSTag Type="Passive" Tooltip="Metamagic_Heightened">Heightened Spell</LSTag>, and
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyIntensifySpell">Intensify Spell</LSTag>.
            """,
        "Icon": "Action_KnowledgeOfTheAges",
        "Progression": {
            range(1, 21): {
                "Passives": ["WarCaster_Bonuses",
                             "WarCaster_OpportunitySpell"],
                "Boosts": ["ProficiencyBonus(SavingThrow,Constitution)"],
            },
            range(4, 21): {
                "Passives": ["Metamagic_Twinned",
                             "Serenade_ProdigyRestoreSorceryPoints"],
                "Boosts": ["ActionResource(SorceryPoint,5,0)",
                           "Tag(SORCERER_METAMAGIC)"],
            },
            range(7, 21): {
                "Passives": ["Metamagic_Quickened",
                             "Serenade_ProdigyEmpoweredMagic"],
                "Boosts": ["ActionResource(SorceryPoint,5,0)"],
            },
            range(11, 21): {
                "Passives": ["Metamagic_Heightened",
                             "Serenade_ProdigyIntensifySpell"],
                "Boosts": ["ActionResource(SorceryPoint,5,0)"],
            },
            range(15, 21): {
                "Boosts": ["ActionResource(SorceryPoint,3,0)"],
            },
        },
    },

    "MartialArtist": {
        "Name": "Prodigy: Martial Artist",
        "Description": """
            On selecting this training, you receive
            <LSTag Type="Passive" Tooltip="MartialArts_BonusUnarmedStrike">Bonus Unarmed Strike</LSTag>,
            <LSTag Type="Passive" Tooltip="Serenade_ProdigyRestoreKiPoints">Restore Ki Points</LSTag>,
            <LSTag Type="Passive" Tooltip="TavernBrawler">Tavern Brawler</LSTag>, and
            <LSTag Type="Spell" Tooltip="Shout_Dash_StepOfTheWind">Step of the Wind: Dash</LSTag>. You also gain
            2 <LSTag Type="ActionResource" Tooltip="KiPoint">Ki Points</LSTag>.

            <br><br>At level 5, you receive <LSTag Type="Passive" Tooltip="ExtraAttack">Extra Attack</LSTag>.

            <br><br>At level 7, you receive <LSTag Type="Passive" Tooltip="FastHands">Fast Hands</LSTag>,
            <LSTag Type="Spell" Tooltip="Serenade_ProdigySpinningKick">Spinning Kick</LSTag>, and a further 2
            <LSTag Type="ActionResource" Tooltip="KiPoint">Ki Points</LSTag>.

            <br><br>Finally, at level 11, you receive
            <LSTag Type="Passive" Tooltip="ExtraAttack_2">Improved Extra Attack</LSTag>, and 2
            <LSTag Type="ActionResource" Tooltip="KiPoint">Ki Points</LSTag>.
            """,
        "Icon": "Action_Monk_FlurryOfBlows",
        "Progression": {
            range(1, 21): {
                "Passives": ["MartialArts_BonusUnarmedStrike",
                             "Serenade_ProdigyRestoreKiPoints",
                             "TavernBrawler"],
                "Boosts": ["ActionResource(KiPoint,2,0)",
                           "UnlockSpell(Shout_Dash_StepOfTheWind)"],
            },
            range(5, 11): {
                "Passives": ["ExtraAttack"],
            },
            range(7, 21): {
                "Passives": ["FastHands"],
                "Boosts": ["ActionResource(KiPoint,2,0)",
                           "UnlockSpell(Serenade_ProdigySpinningKick)"],
            },
            range(11, 21): {
                "Passives": ["ExtraAttack_2"],
                "Boosts": ["ActionResource(KiPoint,2,0)"],
            },
        },
    },

    "SavageAttacker": {
        "Name": "Prodigy: Savage Attacker",
        "Description": """
            At level 8, you receive
            <LSTag Type="Passive" Tooltip="SavageAttacks">Savage Attacks</LSTag>,
            <LSTag Type="Passive" Tooltip="SavageAttacker">Savage Attacker</LSTag>, and
            <LSTag Type="Passive" Tooltip="ImprovedCritical">Improved Critical Hit</LSTag>.
            """,
        "Icon": "PassiveFeature_SavageAttacker",
        "Progression": {
            range(8, 21): {
                "Passives": ["SavageAttacks",
                             "SavageAttacker",
                             "ImprovedCritical"],
            },
        },
    },

    "SpellSlots": {
        "Name": "Prodigy: Spell Slots",
        "Description": """
            In addition to any <LSTag Tooltip="SpellSlot">Spell Slots</LSTag> that you gain from your class, each level
            you also gain the number of spell slots that a full spellcaster would have.
            """,
        "Icon": "Action_KnowledgeOfTheAges",
        "Progression": {
            range(1, 21): {
                "Passives": ["UnlockedSpellSlotLevel1"],
                "Boosts": ["ActionResource(SpellSlot,2,1)"],
            },
            range(2, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,1)"],
            },
            range(3, 21): {
                "Passives": ["UnlockedSpellSlotLevel2"],
                "Boosts": ["ActionResource(SpellSlot,1,1)",
                           "ActionResource(SpellSlot,2,2)"],
            },
            range(4, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,2)"],
            },
            range(5, 21): {
                "Passives": ["UnlockedSpellSlotLevel3"],
                "Boosts": ["ActionResource(SpellSlot,2,3)"],
            },
            range(6, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,3)"],
            },
            range(7, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,4)"],
            },
            range(8, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,4)"],
            },
            range(9, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,4)",
                           "ActionResource(SpellSlot,1,5)"],
            },
            range(10, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,5)"],
            },
            range(11, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,6)"],
            },
            range(13, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,7)"],
            },
            range(15, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,8)"],
            },
            range(17, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,9)"],
            },
            range(18, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,5)"],
            },
            range(19, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,6)"],
            },
            range(20, 21): {
                "Boosts": ["ActionResource(SpellSlot,1,7)"],
            },
        },
        "Properties": "IsHidden",
    },
}

prodigy_training_keys = ["NoTraining",
                         "Archer",
                         "DualWielder",
                         "Duellist",
                         "GreatWeaponMaster",
                         "MartialArtist",
                         "Metamage"]
extra_training_keys = ["Archer",
                       "Athlete",
                       "DualWielder",
                       "Duellist",
                       "GreatWeaponMaster",
                       "MartialArtist",
                       "Metamage",
                       "SavageAttacker"]

spell_lists = {
    "NoSpells": {
        "Name": "Prodigy: No Spells",
        "Description": "No spell list selected.",
    },

    "Cold": {
        "Name": "Prodigy: Cold Spells",
        "Icon": "",
        "Passives": [("ElementalAdept_Cold", "Elemental Adept: Cold")],
        "Spells": {
            0: [("Projectile_RayOfFrost", "Ray of Frost")],
            1: [("Shout_ArmorOfAgathys", "Armour of Agathys"),
                ("Target_CreateDestroyWater", "Create or Destroy Water"),
                ("Target_FogCloud", "Fog Cloud"),
                ("Projectile_IceKnife", "Ice Knife")],
            2: [("Zone_GustOfWind", "Gust of Wind")],
            3: [("Target_HungerOfHadar", "Hunger of Hadar"),
                ("Target_SleetStorm", "Sleet Storm")],
            4: [("Target_IceStorm", "Ice Storm")],
            5: [("Zone_ConeOfCold", "Cone of Cold")],
            6: [("Target_FreezingSphere", "Otiluke's Freezing Sphere"),
                ("Wall_WallOfIce", "Wall of Ice")],
        },
    },

    "Defensive": {
        "Name": "Prodigy: Defensive Spells",
        "Icon": "Spell_Shield",
        "Spells": {
            0: [("Shout_BladeWard", "Blade Ward"),
                ("Target_Resistance", "Resistance")],
            1: [("Shout_ArmorOfAgathys", "Armour of Agathys"),
                ("Target_HealingWord", "Healing Word"),
                ("Target_ProtectionFromEvilAndGood", "Protection from Evil and Good"),
                ("Shout_Shield_Wizard", "Shield")],
            2: [("Shout_MirrorImage", "Mirror Image")],
            3: [("Target_Counterspell", "Counterspell")],
            4: [("Shout_FireShield", "Fire Shield")],
            5: [("Shout_DispelEvilAndGood", "Dispell Evil and Good")],
            6: [("Target_GlobeOfInvulnerability", "Globe of Invulnerability")],
        },
    },

    "Fire": {
        "Name": "Prodigy: Fire Spells",
        "Icon": "",
        "Passives": [("ElementalAdept_Fire", "Elemental Adept: Fire")],
        "Spells": {
            0: [("Projectile_FireBolt", "Fire Bolt"),
                ("Shout_ProduceFlame", "Produce Flame")],
            1: [("Zone_BurningHands", "Burning Hands"),
                ("Target_Grease", "Grease"),
                ("Shout_HellishRebuke", "Hellish Rebuke"),
                ("Target_Smite_Searing", "Searing Smite")],
            2: [("Shout_FlameBlade", "Flame Blade"),
                ("Target_FlamingSphere", "Flaming Sphere"),
                ("Projectile_ScorchingRay", "Scorching Ray")],
            3: [("Projectile_Fireball", "Fireball")],
            4: [("Shout_FireShield", "Fire Shield"),
                ("Wall_WallOfFire", "Wall of Fire")],
            5: [("Target_FlameStrike", "Flame Strike")],
        },
    },

    "Movement": {
        "Name": "Prodigy: Movement Spells",
        "Icon": "Spell_Conjuration_MistyStep",
        "Spells": {
            1: [("Target_Jump", "Enhance Leap"),
                ("Shout_ExpeditiousRetreat", "Expeditious Retreat"),
                ("Shout_FeatherFall", "Feather Fall"),
                ("Target_Longstrider", "Longstrider")],
            2: [("Target_MistyStep", "Misty Step")],
            3: [("Target_GaseousForm", "Gaseous Form"),
                ("Target_Fly", "Grant Flight")],
            4: [("Teleportation_DimensionDoor", "Dimension Door"),
                ("Target_FreedomOfMovement", "Freedom of Movement")],
            5: [("Projectile_Fly", "Fly")],
            6: [("Teleportation_ArcaneGate", "Arcane Gate"),
                ("Shout_WindWalk", "Wind Walk")],
        },
    },

    "Necromancy": {
        "Name": "Prodigy: Necromancy Spells",
        "Icon": "Spell_Necromancy_AnimateDead",
        "Spells": {
            0: [("Target_ChillTouch", "Bone Chill"),
                ("Projectile_EldritchBlast", "Eldritch Blast")],
            1: [("Shout_ArmorOfAgathys", "Armour of Agathys"),
                ("Shout_ArmsOfHadar", "Arms of Hadar"),
                ("Target_InflictWounds", "Inflict Wounds"),
                ("Projectile_RayOfSickness", "Ray of Sickness")],
            2: [("Target_Blindness", "Blindness")],
            3: [("Target_AnimateDead", "Animate Dead"),
                ("Target_SpeakWithDead", "Speak with Dead"),
                ("Target_VampiricTouch", "Vampiric Touch")],
            4: [("Target_Blight", "Blight")],
            5: [("Target_Contagion", "Contagion")],
            6: [("Target_CircleOfDeath", "Circle of Death"),
                ("Target_CreateUndead", "Create Undead"),
                ("Target_Harm", "Harm")],
        },
    },

    "Storm": {
        "Name": "Prodigy: Storm Spells",
        "Icon": "Spell_Evocation_LightningBolt",
        "Passives": [("ElementalAdept_Lightning", "Elemental Adept: Lightning"),
                     ("ElementalAdept_Thunder", "Elemental Adept: Thunder")],
        "Spells": {
            0: [("Serenade_ProdigyStormBolt", "Storm Bolt"),
                ("Target_ShockingGrasp", "Shocking Grasp")],
            1: [("Projectile_ChromaticOrb", "Chromatic Orb"),
                ("Target_CreateDestroyWater", "Create or Destroy Water"),
                ("Target_Smite_Thunderous", "Thunderous Smite"),
                ("Zone_Thunderwave", "Thunderwave")],
            2: [("Target_Shatter", "Shatter")],
            3: [("Zone_LightningBolt", "Lightning Bolt")],
            5: [("Shout_DestructiveWave", "Destructive Wave")],
            6: [("Projectile_ChainLightning", "Chain Lightning")],
        },
    },

    "Subterfuge": {
        "Name": "Prodigy: Subterfuge Spells",
        "Icon": "Spell_Illusion_DisguiseSelf",
        "Passives": [("DevilsSight", "Devil's Sight")],
        "Spells": {
            0: [("Target_MageHand", "Mage Hand"),
                ("Target_MinorIllusion", "Minor Illusion")],
            1: [("Shout_DisguiseSelf", "Disguise Self")],
            2: [("Target_Darkness", "Darkness"),
                ("Target_Invisibility", "Invisibility"),
                ("Shout_PassWithoutTrace", "Pass Without Trace"),
                ("Shout_SeeInvisibility", "See Invisibility")],
            3: [("Target_FeignDeath", "Feign Death")],
            4: [("Target_Invisibility_Greater", "Greater Invisibility")],
            5: [("Target_Seeming", "Seeming")],
        },
    },
}

spell_lists_spell_keys = [f"Serenade_ProdigySpellList{key}" for key in sorted(spell_lists.keys())
                          if key != "NoSpells"]
spell_lists_all_keys = ["Serenade_ProdigySpellListNoSpells"] + spell_lists_spell_keys


def list_to_comma_separated_str(str_list):
    last_entry = None
    if len(str_list) > 1:
        last_entry = str_list[-1]

    comma_str = ", ".join(str_list[0:-1] if len(str_list) > 1 else str_list)
    if last_entry:
        comma_str += ", and " + last_entry

    return comma_str


def spell_lists_to_training(lists):
    training_dict = {}
    level_1 = range(1, 21)

    for key, spell_list in lists.items():
        train = {
            "Name": spell_list["Name"],
            "Progression": {},
        }
        if (icon := spell_list.get("Icon", None)):
            train["Icon"] = icon
        if (description := spell_list.get("Description")):
            train["Description"] = description

        progression = train["Progression"]

        if (passives := spell_list.get("Passives", None)):
            progression[level_1] = {
                "Passives": [passive[0] for passive in passives],
            }

        if (spells := spell_list.get("Spells", None)):
            cantrips = spells.get(0, [])
            level_1_spells = spells.get(1, [])
            progression[level_1] = progression.get(level_1, {}) | {
                "Boosts": [f"UnlockSpell({cantrip[0]})" for cantrip in cantrips] +
                          [f"UnlockSpell({level_1_spell[0]},AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf)"
                           for level_1_spell in level_1_spells]
            }
            for level in range(2, 7):
                if (leveled_spells := spells.get(level, None)):
                    progression[range((level - 1) * 2 + 1, 21)] = {
                        "Boosts": [f"UnlockSpell({leveled_spell[0]},AddChildren,d136c5d9-0ff0-43da-acce-a74a07f8d6bf)"
                                   for leveled_spell in leveled_spells]
                    }
            if "Description" not in spell_list:
                spell_descriptions = []
                for level in range(0, 7):
                    if (leveled_spells := spells.get(level, None)):
                        spell_descriptions += [
                            f"""<LSTag Type="Spell" Tooltip="{leveled_spell[0]}">{leveled_spell[1]}</LSTag>"""
                            for leveled_spell in leveled_spells]

                description = ""
                if (passives := spell_list.get("Passives", None)):
                    passive_descriptions = [
                        f"""<LSTag Type="Passive" Tooltip="{passive[0]}">{passive[1]}</LSTag>"""
                        for passive in passives]
                    description += f"Taking this spell list grants {
                        list_to_comma_separated_str(passive_descriptions)}.<br><br>"

                description += f"Gain the following spells at the appropriate level: {
                    list_to_comma_separated_str(spell_descriptions)}."
                train["Description"] = description

        training_dict[f"SpellList{key}"] = train

    return training_dict


training |= spell_lists_to_training(spell_lists)


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
        data "Properties" "IsHidden"
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

        new entry "Serenade_ProdigyRestoreKiPoints"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyRestoreKiPoints_DisplayName"
        data "Description" "Serenade_ProdigyRestoreKiPoints_Description"
        data "Icon" "Action_Mag_KiRestoration_Lesser"
        data "Properties" "IsHidden"
        data "StatsFunctorContext" "OnCreate"
        data "StatsFunctors" "ApplyStatus(SELF,SERENADE_PRODIGYRESTOREKIPOINTS,100,-1)"

        new entry "SERENADE_PRODIGYRESTOREKIPOINTS"
        type "StatusData"
        data "StatusType" "BOOST"
        data "DisplayName" "Serenade_ProdigyRestoreKiPoints_DisplayName"
        data "Description" "Serenade_ProdigyRestoreKiPoints_Description"
        data "Icon" "Action_Mag_KiRestoration_Lesser"
        data "StackId" "SERENADE_PRODIGYRESTOREKIPOINTS"
        data "StackType" "Overwrite"
        data "TickType" "StartTurn"
        data "TickFunctors" "RestoreResource(KiPoint,1,0)"
        data "StatusGroups" "SG_RemoveOnRespec"
        data "StatusPropertyFlags" "DisableOverhead;DisableImmunityOverhead;DisablePortraitIndicator;DisableCombatlog;IgnoreResting"

        new entry "Serenade_ProdigyAthleteFeat"
        type "PassiveData"
        data "DisplayName" "h860bd485g72b2g45b8gbad7g02e8f5acdd3e;1"
        data "Description" "Serenade_ProdigyAthleteFeat_Description"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyDualWielderFeat"
        type "PassiveData"
        data "DisplayName" "h1d620270gba24g434egad17g5ee9b72a6e3e;1"
        data "Description" "h1909840bg87f1g4029g9be6g974d9233f516;4"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyGreatWeaponMasterFeat"
        type "PassiveData"
        data "DisplayName" "hf41eb2bag6496g4187g994dg62b9cb959e29;1"
        data "Description" "hea61c527gd53fg46fega454g2bc02f65d75f;5"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyMobileFeat"
        type "PassiveData"
        data "DisplayName" "hb434e5e8g23c2g439eg9703g2ac8fc9616ea;1"
        data "Description" "hea5b6476gaefcg412ag9d1dgb081d4e61c19;4"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyShieldMasterFeat"
        type "PassiveData"
        data "DisplayName" "h8d63974fgdcb8g463fg8bedg7e8f1ceb9722;1"
        data "Description" "h7d3721fbg8c06g47ceg8584g3b7b26d94174;3"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigySharpshooterFeat"
        type "PassiveData"
        data "DisplayName" "h7fd575c5g3a3ag46a8g9a40gcddf1cd2b044;1"
        data "Description" "h0bf50988g8a65g40c1ga9e1g2ad5b6387678;3"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyWarCasterFeat"
        type "PassiveData"
        data "DisplayName" "haadef5acg36f8g4affg8c7bg7901735048a8;2"
        data "Description" "h2967e308gd644g46d5g91e4g3de62873eef7;5"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyDefaultWeapons"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyDefaultWeapons_DisplayName"
        data "Description" "Serenade_ProdigyDefaultWeapons_Description"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigySimpleWeapons"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigySimpleWeapons_DisplayName"
        data "Description" "Serenade_ProdigySimpleWeapons_Description"
        data "Boosts" "Proficiency(SimpleWeapons)"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyMartialWeapons"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyMartialWeapons_DisplayName"
        data "Description" "Serenade_ProdigyMartialWeapons_Description"
        data "Boosts" "Proficiency(SimpleWeapons);Proficiency(MartialWeapons)"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyDefaultArmor"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyDefaultArmor_DisplayName"
        data "Description" "Serenade_ProdigyDefaultArmor_Description"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyLightArmor"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyLightArmor_DisplayName"
        data "Description" "Serenade_ProdigyLightArmor_Description"
        data "Boosts" "Proficiency(LightArmor)"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyMediumArmor"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyMediumArmor_DisplayName"
        data "Description" "Serenade_ProdigyMediumArmor_Description"
        data "Boosts" "Proficiency(LightArmor);Proficiency(MediumArmor)"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyHeavyArmor"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyHeavyArmor_DisplayName"
        data "Description" "Serenade_ProdigyHeavyArmor_Description"
        data "Boosts" "Proficiency(LightArmor);Proficiency(MediumArmor);Proficiency(HeavyArmor)"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyDefaultShields"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyDefaultShields_DisplayName"
        data "Description" "Serenade_ProdigyDefaultShields_Description"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyShields"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyShields_DisplayName"
        data "Description" "Serenade_ProdigyShields_Description"
        data "Boosts" "Proficiency(Shields)"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyEmpoweredMagic"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyEmpoweredMagic_DisplayName"
        data "Description" "Serenade_ProdigyEmpoweredMagic_Description"
        data "Boosts" "IF(IsSpell() and not (HasPassive('EmpoweredEvocation',context.Source) and IsSpellSchool(SpellSchool.Evocation)) and not (HasPassive('AgonizingBlast',context.Source) and SpellId('Projectile_EldritchBlast'))):DamageBonus(max(0, SpellCastingAbilityModifier))"
        data "Icon" "PassiveFeature_EmpoweredEvocation"
        data "Properties" "IsHidden"

        new entry "Serenade_ProdigyIntensifySpell"
        type "PassiveData"
        data "DisplayName" "Serenade_ProdigyIntensifySpell_DisplayName"
        data "Description" "Serenade_ProdigyIntensifySpell_Description"
        data "TooltipUseCosts" "SorceryPoint:3"
        data "Icon" "Skill_Sorcerer_Passive_Metamagic_EmpoweredSpell"
        data "Boosts" "UnlockInterrupt(Serenade_ProdigyIntensifySpellInterrupt)"
        data "Properties" "IsHidden"
        data "StatsFunctorContext" "OnCastResolved"
        data "StatsFunctors" "RemoveStatus(SERENADE_PRODIGYINTENSIFYSPELL)"

        new entry "Serenade_ProdigyIntensifySpellInterrupt"
        type "InterruptData"
        data "DisplayName" "Serenade_ProdigyIntensifySpell_DisplayName"
        data "Description" "Serenade_ProdigyIntensifySpell_Description"
        data "Icon" "Skill_Sorcerer_Passive_Metamagic_EmpoweredSpell"
        data "InterruptContext" "OnSpellCast"
        data "InterruptContextScope" "Self"
        data "Container" "YesNoDecision"
        data "Conditions" "Self(context.Source,context.Observer) and IntensifiedSpellCheck() and not AnyEntityIsItem()"
        data "Properties" "ApplyStatus(OBSERVER_OBSERVER,SERENADE_PRODIGYINTENSIFYSPELL,100,1)"
        data "Cost" "SorceryPoint:3"
        data "InterruptDefaultValue" "Ask;Enabled"
        data "EnableCondition" "not HasStatus('SG_Polymorph') or Tagged('MINDFLAYER') or HasStatus('SG_Disguise')"
        data "EnableContext" "OnStatusApplied;OnStatusRemoved"

        new entry "SERENADE_PRODIGYINTENSIFYSPELL"
        type "StatusData"
        data "StatusType" "BOOST"
        data "DisplayName" "Serenade_ProdigyIntensifySpell_DisplayName"
        data "StackId" "SERENADE_PRODIGYINTENSIFYSPELL"
        data "Boosts" "MinimumRollResult(Damage,20)"
        data "StatusPropertyFlags" "DisableOverhead;DisableCombatlog;DisablePortraitIndicator"
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
            data "Properties" "{train.get("Properties", "Highlighted" if "Progression" in train else "IsHidden")}"
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


xml_prologue = f"""\
<?xml version="1.0" encoding="UTF-8"?>
<!-- DO NOT EDIT: This file was automatically generated by {os.path.basename(__file__)} -->
"""


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
    prodigy_training_names = [f"Serenade_Prodigy{key}" for key in prodigy_training_keys]
    extra_training_names = [f"Serenade_Prodigy{key}" for key in extra_training_keys]

    document = ElementTree.fromstring(textwrap.dedent("""\
        <save>
            <version major="4" minor="1" revision="1" build="0"/>
            <region id="PassiveLists">
                <node id="root">
                    <children>
                    </children>
                </node>
            </region>
        </save>
        """))
    children = document.find("./region/node/children")

    def passive_list(passives, uuid):
        node = ElementTree.SubElement(children, "node", id="PassiveList")
        ElementTree.SubElement(node, "attribute", id="Passives", type="LSString", value=",".join(passives))
        ElementTree.SubElement(node, "attribute", id="UUID", type="guid", value=uuid)

    passive_list(prodigy_training_names, "b7d72358-f348-4c78-8e42-a743b16a2c2c")
    passive_list(extra_training_names, "3f273be9-a773-4473-b0d4-8f50697727a0")
    passive_list(["Serenade_ProdigyDefaultWeapons",
                  "Serenade_ProdigySimpleWeapons",
                  "Serenade_ProdigyMartialWeapons"],
                 "5b577b08-aec9-40f3-bac7-b189857428db")
    passive_list(["Serenade_ProdigyDefaultArmor",
                  "Serenade_ProdigyLightArmor",
                  "Serenade_ProdigyMediumArmor",
                  "Serenade_ProdigyHeavyArmor"],
                 "ec4fc950-14bb-414e-bd6d-27ee32c4f700")
    passive_list(["Serenade_ProdigyDefaultShields",
                  "Serenade_ProdigyShields"],
                 "1436faeb-4fb9-4bc3-a5cc-bd96a4e0509a")
    passive_list(spell_lists_all_keys, "a3bfea46-6fa4-4930-b7c9-098edac06fd4")
    passive_list(spell_lists_spell_keys, "3b3991c0-5e89-4dd0-8d21-3481ea149606")

    for attribute in attributes:
        attribute_bonuses = [f"Serenade_Prodigy{attribute}_{bonus}"
                             for bonus in range(0, max_attribute_bonus + attribute_step, attribute_step)]
        passive_list(attribute_bonuses, attribute_guid[attribute])

    roll_bonuses = [f"Serenade_ProdigyRollBonus_{bonus}"
                    for bonus in range(0, max_roll_bonus + roll_bonus_step, roll_bonus_step)]
    passive_list(roll_bonuses, "12b2f031-1837-46d6-ae05-50a3490b6065")

    ElementTree.indent(document, space=" "*4)

    f.write(xml_prologue)
    ElementTree.ElementTree(document).write(f, encoding="unicode")


def removeExtraWhitespace(s):
    return re.sub("\\s{2,}", " ", s.strip())


# Generate the English localization
with open(os.path.join(base_dir, "Localization", "English", "Prodigy.loca.xml"), "w") as f:
    content_list = ElementTree.Element("contentList")
    localization = ElementTree.ElementTree(content_list)

    def content(uid, text):
        element = ElementTree.SubElement(content_list, "content", contentuid=uid, version="1")
        element.text = text

    content("Serenade_Prodigy_NoBonus_DisplayName", """No Bonus""")
    content("Serenade_ProdigyRestoreSorceryPoints_DisplayName", """Prodigy: Restore Sorcery Points""")
    content("Serenade_ProdigyRestoreSorceryPoints_Description", """Every turn, you restore 1 <LSTag Type="ActionResource" Tooltip="SorceryPoint">Sorcery Point</LSTag>.""")
    content("Serenade_ProdigyRestoreKiPoints_DisplayName", """Prodigy: Restore Ki Points""")
    content("Serenade_ProdigyRestoreKiPoints_Description", """Every turn, you restore 1 <LSTag Type="ActionResource" Tooltip="KiPoint">Ki Point</LSTag>.""")
    content("Serenade_ProdigyDefaultWeapons_DisplayName", """Default""")
    content("Serenade_ProdigyDefaultWeapons_Description", """Default weapon proficiencies.""")
    content("Serenade_ProdigySimpleWeapons_DisplayName", """Prodigy: Simple Weapons""")
    content("Serenade_ProdigySimpleWeapons_Description", """Gain <LSTag Tooltip="WeaponProficiency">Weapon Proficiency</LSTag> with Simple Weapons.""")
    content("Serenade_ProdigyMartialWeapons_DisplayName", """Prodigy: Martial Weapons""")
    content("Serenade_ProdigyMartialWeapons_Description", """Gain <LSTag Tooltip="WeaponProficiency">Weapon Proficiency</LSTag> with Simple and Martial Weapons.""")
    content("Serenade_ProdigyDefaultArmor_DisplayName", """Default""")
    content("Serenade_ProdigyDefaultArmor_Description", """Default armor proficiencies.""")
    content("Serenade_ProdigyLightArmor_DisplayName", """Prodigy: Light Armour""")
    content("Serenade_ProdigyLightArmor_Description", """Gain <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Light Armour.""")
    content("Serenade_ProdigyMediumArmor_DisplayName", """Prodigy: Medium Armour""")
    content("Serenade_ProdigyMediumArmor_Description", """Gain <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Light and Medium Armour.""")
    content("Serenade_ProdigyHeavyArmor_DisplayName", """Prodigy: Heavy Armour""")
    content("Serenade_ProdigyHeavyArmor_Description", """Gain <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Light, Medium, and Heavy Armour.""")
    content("Serenade_ProdigyDefaultShields_DisplayName", """Default""")
    content("Serenade_ProdigyDefaultShields_Description", """Default shield proficiency.""")
    content("Serenade_ProdigyShields_DisplayName", """Prodigy: Shields""")
    content("Serenade_ProdigyShields_Description", """Gain <LSTag Tooltip="ArmourProficiency">Armour Proficiency</LSTag> with Shields.""")
    content("Serenade_ProdigyEmpoweredMagic_DisplayName", """Prodigy: Empowered Magic""")
    content("Serenade_ProdigyEmpoweredMagic_Description", """You add your <LSTag Tooltip="SpellcastingAbilityModifier">Spellcasting Ability</LSTag> <LSTag Tooltip="AbilityModifier">Modifier</LSTag> to your spell damage.<br><br>This does not stack with <LSTag Type="Passive" Tooltip="AgonizingBlast">Agonizing Blast</LSTag> or <LSTag Type="Passive" Tooltip="EmpoweredEvocation">Empowered Evocation</LSTag>.""")
    content("Serenade_ProdigyIntensifySpell_DisplayName", """Prodigy: Intensify Spell""")
    content("Serenade_ProdigyIntensifySpell_Description", """When you deal spell damage, you can use your <LSTag Type="ActionResource" Tooltip="SorceryPoint">Sorcery Points</LSTag> to deal maximum damage instead.""")
    content("Serenade_ProdigyAthleteFeat_Description", """When you are Prone, standing up uses significantly less movement. Your <LSTag Type="Spell" Tooltip="Projectile_Jump">Jump</LSTag> distance also increases by 50%.""")

    for attribute in attributes:
        content(f"Serenade_Prodigy{attribute}_DisplayName", f"""Prodigy: {attribute}""")
        content(f"Serenade_Prodigy{attribute}_Description", f"""Add a bonus to your <LSTag Tooltip="{attribute}">{attribute}</LSTag>.""")
        content(f"Serenade_Prodigy{attribute}_NoBonus_Description", f"""No bonus to <LSTag Tooltip="{attribute}">{attribute}</LSTag>.""")

        for bonus in range(attribute_step, max_attribute_bonus + attribute_step, attribute_step):
            content(f"Serenade_Prodigy{attribute}_{bonus}_DisplayName", f"""Prodigy: {attribute} +{bonus}""")
            content(f"Serenade_Prodigy{attribute}_{bonus}_Description", f"""Increase your <LSTag Tooltip="{attribute}">{attribute}</LSTag> by {bonus}, to a maximum of 30.""")

    content("Serenade_ProdigyRollBonus_DisplayName", """Prodigy: Roll Bonus""")
    content("Serenade_ProdigyRollBonus_Description", """Add a bonus to your <LSTag Tooltip="SkillCheck">Skill</LSTag> and <LSTag Tooltip="AbilityCheck">Ability</LSTag> checks.""")
    content("Serenade_ProdigyRollBonus_NoBonus_Description", """No bonus to your <LSTag Tooltip="SkillCheck">Skill</LSTag> and <LSTag Tooltip="AbilityCheck">Ability</LSTag> checks.""")

    for bonus in range(roll_bonus_step, max_roll_bonus + roll_bonus_step, roll_bonus_step):
        content(f"Serenade_ProdigyRollBonus_{bonus}_DisplayName", f"""Prodigy: Roll Bonus +{bonus}""")
        content(f"Serenade_ProdigyRollBonus_{bonus}_Description", f"""Add {bonus} to your <LSTag Tooltip="SkillCheck">Skill</LSTag> and <LSTag Tooltip="AbilityCheck">Ability</LSTag> checks.""")

    for key, train in training.items():
        content(f"Serenade_Prodigy{key}_DisplayName", f"""{train["Name"]}""")
        content(f"Serenade_Prodigy{key}_Description", f"""{removeExtraWhitespace(train["Description"])}""")

    ElementTree.indent(localization, space=" "*4)

    f.write(xml_prologue)
    localization.write(f, encoding="unicode")
