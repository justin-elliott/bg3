#!/usr/bin/env python3
"""
A class representing ValueLists, together with definitions parsed from ValueLists.txt.
"""

from enum import StrEnum


class AIFlags(StrEnum):
    CANNOTTARGETFROZEN = "CanNotTargetFrozen"
    CANNOTUSE = "CanNotUse"
    GRANTSRESOURCES = "GrantsResources"
    IGNOREBUFF = "IgnoreBuff"
    IGNORECONTROL = "IgnoreControl"
    IGNOREDEBUFF = "IgnoreDebuff"
    IGNORESELF = "IgnoreSelf"
    STATUSISSECONDARY = "StatusIsSecondary"
    USEASSEEKACTIONONLY = "UseAsSeekActionOnly"
    USEASSUPPORTINGACTIONONLY = "UseAsSupportingActionOnly"


class Ability(StrEnum):
    CHARISMA = "Charisma"
    CONSTITUTION = "Constitution"
    DEXTERITY = "Dexterity"
    INTELLIGENCE = "Intelligence"
    NONE = "None"
    STRENGTH = "Strength"
    WISDOM = "Wisdom"


class AbilityFlags(StrEnum):
    CHARISMA = "Charisma"
    CONSTITUTION = "Constitution"
    DEXTERITY = "Dexterity"
    INTELLIGENCE = "Intelligence"
    NONE = "None"
    STRENGTH = "Strength"
    WISDOM = "Wisdom"


class Act(str):
    _VALID_VALUES = {
        "1",
    }

    def __new__(cls, value: str):
        value = str(value)
        if value not in cls._VALID_VALUES:
            raise KeyError(f"{value} is not a member of Act")
        return super().__new__(cls, value)


class ActionType(StrEnum):
    BONUS = "Bonus"
    REGULAR = "Regular"


class AlchemyCombinationType(StrEnum):
    EXTRACTTOSOLUTION = "ExtractToSolution"
    INGREDIENTSTOEXTRACT = "IngredientsToExtract"
    NONE = "None"


class ArmorType(StrEnum):
    BREASTPLATE = "BreastPlate"
    CHAINMAIL = "ChainMail"
    CHAINSHIRT = "ChainShirt"
    CLOTH = "Cloth"
    HALFPLATE = "HalfPlate"
    HIDE = "Hide"
    LEATHER = "Leather"
    NONE = "None"
    PADDED = "Padded"
    PLATE = "Plate"
    RINGMAIL = "RingMail"
    SCALEMAIL = "ScaleMail"
    SPLINT = "Splint"
    STUDDEDLEATHER = "StuddedLeather"


class AtmosphereType(StrEnum):
    NONE = "None"
    RAIN = "Rain"
    STORM = "Storm"


class AttributeFlags(StrEnum):
    ARROW = "Arrow"
    BACKSTAB = "Backstab"
    BACKSTABIMMUNITY = "BackstabImmunity"
    ENABLEOBSCURITYEVENTS = "EnableObscurityEvents"
    FLOATING = "Floating"
    FLOATINGWHILEMOVING = "FloatingWhileMoving"
    FORCEMAINHANDALTERNATIVEEQUIPBONES = "ForceMainhandAlternativeEquipBones"
    GROUNDED = "Grounded"
    IGNORECLOUDS = "IgnoreClouds"
    INVENTORYBOUND = "InventoryBound"
    INVISIBILITYIMMUNITY = "InvisibilityImmunity"
    INVULNERABLEANDINTERACTIVE = "InvulnerableAndInteractive"
    LOOTABLEWHENEQUIPPED = "LootableWhenEquipped"
    LOSEDURABILITYONCHARACTERHIT = "LoseDurabilityOnCharacterHit"
    NONE = "None"
    OBSCURITYWITHOUTSNEAKING = "ObscurityWithoutSneaking"
    PICKPOCKETABLEWHENEQUIPPED = "PickpocketableWhenEquipped"
    REALLYARMOR = "ReallyArmor"
    SLIPPINGIMMUNITY = "SlippingImmunity"
    THROWNIMMUNITY = "ThrownImmunity"
    TORCH = "Torch"
    UNBREAKABLE = "Unbreakable"
    UNREPAIRABLE = "Unrepairable"
    UNSTORABLE = "Unstorable"
    USEMUSICALINSTRUMENTFORCASTING = "UseMusicalInstrumentForCasting"


class AuraFlags(StrEnum):
    AIIGNOREONSELF = "AIIgnoreOnSelf"
    CANAFFECTINVISIBLEITEMS = "CanAffectInvisibleItems"
    NONE = "None"
    SHOULDCHECKLOS = "ShouldCheckLOS"


class BigQualifier(str):
    _VALID_VALUES = {
        "1",
        "10",
        "100",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "2",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "3",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "4",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "5",
        "50",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "6",
        "60",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "69",
        "7",
        "70",
        "71",
        "72",
        "73",
        "74",
        "75",
        "76",
        "77",
        "78",
        "79",
        "8",
        "80",
        "81",
        "82",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "9",
        "90",
        "91",
        "92",
        "93",
        "94",
        "95",
        "96",
        "97",
        "98",
        "99",
        "None",
    }

    def __new__(cls, value: str):
        value = str(value)
        if value not in cls._VALID_VALUES:
            raise KeyError(f"{value} is not a member of BigQualifier")
        return super().__new__(cls, value)


class CastCheckType(StrEnum):
    DAMAGETYPE = "DamageType"
    DISTANCE = "Distance"
    NONE = "None"
    TARGETSURFACETYPE = "TargetSurfaceType"


class CinematicArenaFlags(StrEnum):
    ALWAYSSHOW = "AlwaysShow"
    IGNORE = "Ignore"
    NONE = "None"


class Conditions(str):
    pass


class ConstantFloat(str):
    pass


class ConstantInt(str):
    pass


class CooldownType(StrEnum):
    NONE = "None"
    ONCEPERCOMBAT = "OncePerCombat"
    ONCEPERREST = "OncePerRest"
    ONCEPERRESTPERITEM = "OncePerRestPerItem"
    ONCEPERSHORTREST = "OncePerShortRest"
    ONCEPERSHORTRESTPERITEM = "OncePerShortRestPerItem"
    ONCEPERTURN = "OncePerTurn"
    ONCEPERTURNNOREALTIME = "OncePerTurnNoRealtime"


class CursorMode(StrEnum):
    ARROW = "Arrow"
    ARROW_WARNING = "Arrow_Warning"
    BACKSTAB = "BackStab"
    BACKSTAB_WARNING = "BackStab_Warning"
    BOW = "Bow"
    BOW_GROUND = "Bow_Ground"
    BOW_WARNING = "Bow_Warning"
    CAMERAROTATION = "CameraRotation"
    CAST = "Cast"
    CAST_WARNING = "Cast_Warning"
    COMBINE = "Combine"
    COMBINE_INVALID = "Combine_Invalid"
    COMBINE_WARNING = "Combine_Warning"
    CROSS = "Cross"
    IDENTIFY = "Identify"
    IDENTIFY_WARNING = "Identify_Warning"
    ITEMMOVE = "ItemMove"
    ITEMMOVE_WARNING = "ItemMove_Warning"
    ITEMPICKUP = "ItemPickup"
    ITEMPICKUP_WARNING = "ItemPickup_Warning"
    ITEMUSE = "ItemUse"
    ITEMUSE_WARNING = "ItemUse_Warning"
    LISTEN = "Listen"
    LISTEN_WARNING = "Listen_Warning"
    LOCK = "Lock"
    LOCK_WARNING = "Lock_Warning"
    MELEE = "Melee"
    MELEE_GROUND = "Melee_Ground"
    MELEE_WARNING = "Melee_Warning"
    NONE = "None"
    OPENCONTAINER = "OpenContainer"
    OPENCONTAINER_NEW = "OpenContainer_New"
    OPENCONTAINER_WARNING = "OpenContainer_Warning"
    OPENDOOR = "OpenDoor"
    OPENDOOR_WARNING = "OpenDoor_Warning"
    PICKPOCKET = "PickPocket"
    PICKPOCKET_WARNING = "PickPocket_Warning"
    REPAIR = "Repair"
    REPAIR_WARNING = "Repair_Warning"
    SHOVEL = "Shovel"
    SHOVEL_WARNING = "Shovel_Warning"
    SYSTEM = "System"
    TALK = "Talk"
    TALK_WARNING = "Talk_Warning"
    WALK = "Walk"
    WALK_WARNING = "Walk_Warning"
    WAND = "Wand"
    WAND_GROUND = "Wand_Ground"
    WAND_WARNING = "Wand_Warning"


class CustomProperties(StrEnum):
    ALWAYSBACKSTAB = "AlwaysBackstab"
    ALWAYSHIGHGROUND = "AlwaysHighGround"
    CANBACKSTAB = "CanBackstab"
    NONE = "None"
    UNBREAKABLE = "Unbreakable"


class DamageType(StrEnum):
    ACID = "Acid"
    BLUDGEONING = "Bludgeoning"
    COLD = "Cold"
    FIRE = "Fire"
    FORCE = "Force"
    LIGHTNING = "Lightning"
    NECROTIC = "Necrotic"
    NONE = "None"
    PIERCING = "Piercing"
    POISON = "Poison"
    PSYCHIC = "Psychic"
    RADIANT = "Radiant"
    SLASHING = "Slashing"
    THUNDER = "Thunder"


class DamageSourceType(StrEnum):
    AVERAGELEVELDAMGE = "AverageLevelDamge"
    BASELEVELDAMAGE = "BaseLevelDamage"
    MONSTERWEAPONDAMAGE = "MonsterWeaponDamage"
    SOURCECURRENTMAGICARMOR = "SourceCurrentMagicArmor"
    SOURCECURRENTPHYSICALARMOR = "SourceCurrentPhysicalArmor"
    SOURCECURRENTVITALITY = "SourceCurrentVitality"
    SOURCEMAXIMUMMAGICARMOR = "SourceMaximumMagicArmor"
    SOURCEMAXIMUMPHYSICALARMOR = "SourceMaximumPhysicalArmor"
    SOURCEMAXIMUMVITALITY = "SourceMaximumVitality"
    SOURCESHIELDPHYSICALARMOR = "SourceShieldPhysicalArmor"
    TARGETCURRENTMAGICARMOR = "TargetCurrentMagicArmor"
    TARGETCURRENTPHYSICALARMOR = "TargetCurrentPhysicalArmor"
    TARGETCURRENTVITALITY = "TargetCurrentVitality"
    TARGETMAXIMUMMAGICARMOR = "TargetMaximumMagicArmor"
    TARGETMAXIMUMPHYSICALARMOR = "TargetMaximumPhysicalArmor"
    TARGETMAXIMUMVITALITY = "TargetMaximumVitality"


class DeathType(StrEnum):
    ACID = "Acid"
    CHASM = "Chasm"
    CINEMATICDEATH = "CinematicDeath"
    COLD = "Cold"
    DISINTEGRATE = "Disintegrate"
    DOT = "DoT"
    ELECTROCUTION = "Electrocution"
    EXPLODE = "Explode"
    FALLING = "Falling"
    INCINERATE = "Incinerate"
    KNOCKEDDOWN = "KnockedDown"
    LIFETIME = "Lifetime"
    NECROTIC = "Necrotic"
    NONE = "None"
    PHYSICAL = "Physical"
    PSYCHIC = "Psychic"
    RADIANT = "Radiant"


class DieType(StrEnum):
    NONE = "None"
    D10 = "d10"
    D100 = "d100"
    D12 = "d12"
    D20 = "d20"
    D4 = "d4"
    D6 = "d6"
    D8 = "d8"


class DisturbanceDialogueCapability(StrEnum):
    EXCL_CANTALK = "Excl_CanTalk"
    INCL_OTHERCANNOTTALK = "Incl_OtherCannotTalk"
    INCL_SUMMON = "Incl_Summon"
    INCL_WILDSHAPE = "Incl_Wildshape"


class DisturbanceInvestigationKind(StrEnum):
    FORCEINVESTIGATECRIMINALREACT = "ForceInvestigateCriminalReact"
    FORCEINVESTIGATEINTERROGATE = "ForceInvestigateInterrogate"
    FORCEINVESTIGATESCENEREACT = "ForceInvestigateSceneReact"
    FORCEINVESTIGATESUSPECTREACT = "ForceInvestigateSuspectReact"
    FORCESCENEREACT = "ForceSceneReact"
    INVESTIGATECRIMINALREACT = "InvestigateCriminalReact"
    INVESTIGATEINTERROGATE = "InvestigateInterrogate"
    INVESTIGATEONLY = "InvestigateOnly"
    INVESTIGATESCENEREACT = "InvestigateSceneReact"
    INVESTIGATESUSPECTREACT = "InvestigateSuspectReact"
    NONE = "None"


class DisturbanceMergeConditions(StrEnum):
    NEVER = "Never"
    SAMENONNULLVICTIMORCOMMONEVIDENCE = "SameNonNullVictimOrCommonEvidence"
    SAMEVICTIM = "SameVictim"
    SAMEVICTIMANDCOMMONEVIDENCE = "SameVictimAndCommonEvidence"


class DisturbanceYesNoIgnoreStats(StrEnum):
    NO = "No"
    YES = "Yes"
    YESIGNORESTATS = "YesIgnoreStats"


class FixedString(str):
    pass


class FlagType(StrEnum):
    CHARACTER = "Character"
    DIALOG = "Dialog"
    GLOBAL = "Global"
    INVALID = "Invalid"
    LOCAL = "Local"
    PARTY = "Party"
    USER = "User"


class FormatStringColor(StrEnum):
    AIR = "Air"
    BLACK = "Black"
    BLACKROCK = "Blackrock"
    BLUE = "Blue"
    BROWN = "Brown"
    CHARM = "Charm"
    DARKBLUE = "DarkBlue"
    DARKGRAY = "DarkGray"
    DECAY = "Decay"
    EARTH = "Earth"
    FIRE = "Fire"
    GOLD = "Gold"
    GRAY = "Gray"
    GREEN = "Green"
    HEALING = "Healing"
    LIGHTBLUE = "LightBlue"
    LIGHTGRAY = "LightGray"
    NORMAL = "Normal"
    ORANGE = "Orange"
    PINK = "Pink"
    POISON = "Poison"
    POISONGREEN = "PoisonGreen"
    POLYMORPH = "Polymorph"
    PURPLE = "Purple"
    RANGER = "Ranger"
    RED = "Red"
    ROGUE = "Rogue"
    SOURCE = "Source"
    SPECIAL = "Special"
    STORYITEM = "StoryItem"
    SUMMONER = "Summoner"
    VOID = "Void"
    WARRIOR = "Warrior"
    WATER = "Water"
    WHITE = "White"
    YELLOW = "Yellow"


class GameAction(StrEnum):
    CREATECONESURFACE = "CreateConeSurface"
    CREATESURFACE = "CreateSurface"
    DOUSE = "Douse"
    EQUALIZE = "Equalize"
    NONE = "None"
    PICKUP = "Pickup"
    SWAPPLACES = "SwapPlaces"
    TARGETCREATESURFACE = "TargetCreateSurface"


class Guid(str):
    pass


class Handedness(str):
    _VALID_VALUES = {
        "1",
        "2",
        "Any",
    }

    def __new__(cls, value: str):
        value = str(value)
        if value not in cls._VALID_VALUES:
            raise KeyError(f"{value} is not a member of Handedness")
        return super().__new__(cls, value)


class HealValueType(StrEnum):
    DAMAGEPERCENTAGE = "DamagePercentage"
    FIXEDVALUE = "FixedValue"
    PERCENTAGE = "Percentage"
    QUALIFIER = "Qualifier"
    SHIELD = "Shield"
    TARGETDEPENDENT = "TargetDependent"


class HitAnimationType(StrEnum):
    ANIMATIONSETOVERRIDE = "AnimationSetOverride"
    DEFAULT = "Default"
    MAGICALDAMAGE_ELECTRIC = "MagicalDamage_Electric"
    MAGICALDAMAGE_EXTERNAL = "MagicalDamage_External"
    MAGICALDAMAGE_INTERNAL = "MagicalDamage_Internal"
    MAGICALDAMAGE_PSYCHIC = "MagicalDamage_Psychic"
    MAGICALNONDAMAGE = "MagicalNonDamage"
    NONE = "None"
    PHYSICALDAMAGE = "PhysicalDamage"


class IngredientCombineType(StrEnum):
    ADDITIVE = "Additive"
    BASE = "Base"
    NONE = "None"


class IngredientTransformType(StrEnum):
    CONSUME = "Consume"
    DYE = "Dye"
    NONE = "None"
    POISON = "Poison"
    TRANSFORM = "Transform"


class IngredientType(StrEnum):
    CATEGORY = "Category"
    NONE = "None"
    OBJECT = "Object"
    PROPERTY = "Property"


class InstrumentType(StrEnum):
    BAGPIPES = "Bagpipes"
    DRUM = "Drum"
    DULCIMER = "Dulcimer"
    FLUTE = "Flute"
    HORN = "Horn"
    LUTE = "Lute"
    LYRE = "Lyre"
    MUSICBOX = "Musicbox"
    NONE = "None"
    SAXOPHONE = "Saxophone"
    SHAWM = "Shawm"
    VIOLIN = "Violin"


class InterruptContext(StrEnum):
    NONE = "None"
    ONCASTHIT = "OnCastHit"
    ONDEATH = "OnDeath"
    ONENTERATTACKRANGE = "OnEnterAttackRange"
    ONLEAVEATTACKRANGE = "OnLeaveAttackRange"
    ONPOSTROLL = "OnPostRoll"
    ONPREDAMAGE = "OnPreDamage"
    ONSPELLCAST = "OnSpellCast"
    ONSTATUSAPPLIED = "OnStatusApplied"


class InterruptContextScope(StrEnum):
    NEARBY = "Nearby"
    NONE = "None"
    SELF = "Self"


class InterruptDefaultValue(StrEnum):
    ASK = "Ask"
    ENABLED = "Enabled"
    NONE = "None"


class InterruptFlagsList(StrEnum):
    INTERRUPTWHILEINVISIBLE = "InterruptWhileInvisible"
    NONE = "None"


class InventoryTabs(StrEnum):
    AUTO = "Auto"
    BOOKSANDKEYS = "BooksAndKeys"
    CONSUMABLE = "Consumable"
    EQUIPMENT = "Equipment"
    HIDDEN = "Hidden"
    INGREDIENT = "Ingredient"
    MAGICAL = "Magical"
    MISC = "Misc"


class ItemUseTypes(StrEnum):
    ARROW = "Arrow"
    COMMON = "Common"
    CONSUMABLE = "Consumable"
    GRENADE = "Grenade"
    NONE = "None"
    POTION = "Potion"
    SCROLL = "Scroll"
    THROWABLE = "Throwable"


class Itemslot(StrEnum):
    AMULET = "Amulet"
    BOOTS = "Boots"
    BREAST = "Breast"
    CLOAK = "Cloak"
    GLOVES = "Gloves"
    HELMET = "Helmet"
    HORNS = "Horns"
    MELEEMAINWEAPON = "Melee Main Weapon"
    MELEEOFFHANDWEAPON = "Melee Offhand Weapon"
    MUSICALINSTRUMENT = "MusicalInstrument"
    OVERHEAD = "Overhead"
    RANGEDMAINWEAPON = "Ranged Main Weapon"
    RANGEDOFFHANDWEAPON = "Ranged Offhand Weapon"
    RING = "Ring"
    RING2 = "Ring2"
    UNDERWEAR = "Underwear"
    VANITYBODY = "VanityBody"
    VANITYBOOTS = "VanityBoots"
    WINGS = "Wings"


class LEDEffectType(StrEnum):
    CHARMED = "Charmed"
    CRAFTING = "Crafting"
    CRITICAL = "Critical"
    DEATH = "Death"
    DIALOG = "Dialog"
    DRUNK = "Drunk"
    ENEMYKILLED = "EnemyKilled"
    FROZEN = "Frozen"
    KNOCKEDDOWN = "KnockedDown"
    LEVELUP = "LevelUp"
    LOADING = "Loading"
    LOADINGPROGRESS = "LoadingProgress"
    NONE = "NONE"
    OFF = "OFF"
    PETRIFIED = "Petrified"
    POSSESSED = "Possessed"
    QUESTCOMPLETED = "QuestCompleted"
    SAVEFAILED = "SaveFailed"
    SAVESUCCESS = "SaveSuccess"
    SPELLCAST = "SpellCast"
    SPELLPREPARE = "SpellPrepare"
    SPOTTED = "Spotted"
    STEALTHMODE = "StealthMode"
    STUNNED = "Stunned"
    TERRIFIED = "Terrified"


class LineOfSightFlags(StrEnum):
    ADDSOURCEHEIGHT = "AddSourceHeight"
    NONE = "None"


class ManagedStatusEffectType(StrEnum):
    NEGATIVE = "Negative"
    POSITIVE = "Positive"


class MaterialType(StrEnum):
    FADINGOVERLAY = "FadingOverlay"
    NONE = "None"
    OVERLAY = "Overlay"
    REPLACEMENT = "Replacement"


class MemorizationRequirements(str):
    pass


class ModifierType(StrEnum):
    BOOST = "Boost"
    CHARM = "Charm"
    CRYSTAL = "Crystal"
    FOOD = "Food"
    ITEM = "Item"
    SKILL = "Skill"


class ObjectSize(StrEnum):
    GARGANTUAN = "Gargantuan"
    HUGE = "Huge"
    LARGE = "Large"
    MEDIUM = "Medium"
    SMALL = "Small"
    TINY = "Tiny"


class OsirisTask(StrEnum):
    NONE = "None"
    RESURRECT = "Resurrect"


class PassiveFlags(StrEnum):
    DISPLAYBOOSTINTOOLTIP = "DisplayBoostInTooltip"
    EXECUTEONCE = "ExecuteOnce"
    FORCESHOWINCC = "ForceShowInCC"
    HIGHLIGHTED = "Highlighted"
    ISHIDDEN = "IsHidden"
    ISTOGGLED = "IsToggled"
    METAMAGIC = "MetaMagic"
    NONE = "None"
    ONCEPERATTACK = "OncePerAttack"
    ONCEPERCOMBAT = "OncePerCombat"
    ONCEPERLONGREST = "OncePerLongRest"
    ONCEPERLONGRESTPERITEM = "OncePerLongRestPerItem"
    ONCEPERSHORTREST = "OncePerShortRest"
    ONCEPERSHORTRESTPERITEM = "OncePerShortRestPerItem"
    ONCEPERTURN = "OncePerTurn"
    TEMPORARY = "Temporary"
    TOGGLEFORPARTY = "ToggleForParty"
    TOGGLEDDEFAULTADDTOHOTBAR = "ToggledDefaultAddToHotbar"
    TOGGLEDDEFAULTON = "ToggledDefaultOn"


class PenaltyPreciseQualifier(str):
    _VALID_VALUES = {
        "-0.1",
        "-0.2",
        "-0.3",
        "-0.4",
        "-0.5",
        "-0.6",
        "-0.7",
        "-0.8",
        "-0.9",
        "-1",
        "-1.1",
        "-1.2",
        "-1.3",
        "-1.4",
        "-1.5",
        "-1.6",
        "-1.7",
        "-1.8",
        "-1.9",
        "-10",
        "-2",
        "-2.1",
        "-2.2",
        "-2.3",
        "-2.4",
        "-2.5",
        "-2.6",
        "-2.7",
        "-2.8",
        "-2.9",
        "-3",
        "-3.1",
        "-3.2",
        "-3.3",
        "-3.4",
        "-3.5",
        "-3.6",
        "-3.7",
        "-3.8",
        "-3.9",
        "-4",
        "-4.1",
        "-4.2",
        "-4.3",
        "-4.4",
        "-4.5",
        "-4.6",
        "-4.7",
        "-4.8",
        "-4.9",
        "-5",
        "-5.1",
        "-5.2",
        "-5.3",
        "-5.4",
        "-5.5",
        "-5.6",
        "-5.7",
        "-5.8",
        "-5.9",
        "-6",
        "-6.1",
        "-6.2",
        "-6.3",
        "-6.4",
        "-6.5",
        "-6.6",
        "-6.7",
        "-6.8",
        "-6.9",
        "-7",
        "-7.1",
        "-7.2",
        "-7.3",
        "-7.4",
        "-7.5",
        "-7.6",
        "-7.7",
        "-7.8",
        "-7.9",
        "-8",
        "-8.1",
        "-8.2",
        "-8.3",
        "-8.4",
        "-8.5",
        "-8.6",
        "-8.7",
        "-8.8",
        "-8.9",
        "-9",
        "-9.1",
        "-9.2",
        "-9.3",
        "-9.4",
        "-9.5",
        "-9.6",
        "-9.7",
        "-9.8",
        "-9.9",
        "0",
        "0.1",
        "0.2",
        "0.3",
        "0.4",
        "0.5",
        "0.6",
        "0.7",
        "0.8",
        "0.9",
        "1",
        "1.1",
        "1.2",
        "1.3",
        "1.4",
        "1.5",
        "1.6",
        "1.7",
        "1.8",
        "1.9",
        "10",
        "2",
        "2.1",
        "2.2",
        "2.3",
        "2.4",
        "2.5",
        "2.6",
        "2.7",
        "2.8",
        "2.9",
        "3",
        "3.1",
        "3.2",
        "3.3",
        "3.4",
        "3.5",
        "3.6",
        "3.7",
        "3.8",
        "3.9",
        "4",
        "4.1",
        "4.2",
        "4.3",
        "4.4",
        "4.5",
        "4.6",
        "4.7",
        "4.8",
        "4.9",
        "5",
        "5.1",
        "5.2",
        "5.3",
        "5.4",
        "5.5",
        "5.6",
        "5.7",
        "5.8",
        "5.9",
        "6",
        "6.1",
        "6.2",
        "6.3",
        "6.4",
        "6.5",
        "6.6",
        "6.7",
        "6.8",
        "6.9",
        "7",
        "7.1",
        "7.2",
        "7.3",
        "7.4",
        "7.5",
        "7.6",
        "7.7",
        "7.8",
        "7.9",
        "8",
        "8.1",
        "8.2",
        "8.3",
        "8.4",
        "8.5",
        "8.6",
        "8.7",
        "8.8",
        "8.9",
        "9",
        "9.1",
        "9.2",
        "9.3",
        "9.4",
        "9.5",
        "9.6",
        "9.7",
        "9.8",
        "9.9",
        "None",
    }

    def __new__(cls, value: str):
        value = str(value)
        if value not in cls._VALID_VALUES:
            raise KeyError(f"{value} is not a member of PenaltyPreciseQualifier")
        return super().__new__(cls, value)


class PenaltyQualifier(str):
    _VALID_VALUES = {
        "-1",
        "-10",
        "-2",
        "-3",
        "-4",
        "-5",
        "-6",
        "-7",
        "-8",
        "-9",
        "0",
        "1",
        "10",
        "100",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "None",
    }

    def __new__(cls, value: str):
        value = str(value)
        if value not in cls._VALID_VALUES:
            raise KeyError(f"{value} is not a member of PenaltyQualifier")
        return super().__new__(cls, value)


class PickingState(StrEnum):
    DEAD = "Dead"
    DEFAULT = "Default"
    LYING = "Lying"
    MAX = "MAX"
    SITTING = "Sitting"
    SNEAKING = "Sneaking"
    TOMBSTONE = "Tombstone"


class PreciseQualifier(str):
    _VALID_VALUES = {
        "0",
        "0.1",
        "0.2",
        "0.3",
        "0.4",
        "0.5",
        "0.6",
        "0.7",
        "0.8",
        "0.9",
        "1",
        "1.1",
        "1.2",
        "1.3",
        "1.4",
        "1.5",
        "1.6",
        "1.7",
        "1.8",
        "1.9",
        "10",
        "2",
        "2.1",
        "2.2",
        "2.3",
        "2.4",
        "2.5",
        "2.6",
        "2.7",
        "2.8",
        "2.9",
        "3",
        "3.1",
        "3.2",
        "3.3",
        "3.4",
        "3.5",
        "3.6",
        "3.7",
        "3.8",
        "3.9",
        "4",
        "4.1",
        "4.2",
        "4.3",
        "4.4",
        "4.5",
        "4.6",
        "4.7",
        "4.8",
        "4.9",
        "5",
        "5.1",
        "5.2",
        "5.3",
        "5.4",
        "5.5",
        "5.6",
        "5.7",
        "5.8",
        "5.9",
        "6",
        "6.1",
        "6.2",
        "6.3",
        "6.4",
        "6.5",
        "6.6",
        "6.7",
        "6.8",
        "6.9",
        "7",
        "7.1",
        "7.2",
        "7.3",
        "7.4",
        "7.5",
        "7.6",
        "7.7",
        "7.8",
        "7.9",
        "8",
        "8.1",
        "8.2",
        "8.3",
        "8.4",
        "8.5",
        "8.6",
        "8.7",
        "8.8",
        "8.9",
        "9",
        "9.1",
        "9.2",
        "9.3",
        "9.4",
        "9.5",
        "9.6",
        "9.7",
        "9.8",
        "9.9",
        "None",
    }

    def __new__(cls, value: str):
        value = str(value)
        if value not in cls._VALID_VALUES:
            raise KeyError(f"{value} is not a member of PreciseQualifier")
        return super().__new__(cls, value)


class ProficiencyGroupFlags(StrEnum):
    BATTLEAXES = "Battleaxes"
    CLUBS = "Clubs"
    DAGGERS = "Daggers"
    DARTS = "Darts"
    FLAILS = "Flails"
    GLAIVES = "Glaives"
    GREATAXES = "Greataxes"
    GREATCLUBS = "Greatclubs"
    GREATSWORDS = "Greatswords"
    HALBERDS = "Halberds"
    HANDCROSSBOWS = "HandCrossbows"
    HANDAXES = "Handaxes"
    HEAVYARMOR = "HeavyArmor"
    HEAVYCROSSBOWS = "HeavyCrossbows"
    JAVELINS = "Javelins"
    LIGHTARMOR = "LightArmor"
    LIGHTCROSSBOWS = "LightCrossbows"
    LIGHTHAMMERS = "LightHammers"
    LONGBOWS = "Longbows"
    LONGSWORDS = "Longswords"
    MACES = "Maces"
    MARTIALWEAPONS = "MartialWeapons"
    MAULS = "Mauls"
    MEDIUMARMOR = "MediumArmor"
    MORNINGSTARS = "Morningstars"
    MUSICALINSTRUMENT = "MusicalInstrument"
    NONE = "None"
    PIKES = "Pikes"
    QUARTERSTAFFS = "Quarterstaffs"
    RAPIERS = "Rapiers"
    SCIMITARS = "Scimitars"
    SHIELDS = "Shields"
    SHORTBOWS = "Shortbows"
    SHORTSWORDS = "Shortswords"
    SICKLES = "Sickles"
    SIMPLEWEAPONS = "SimpleWeapons"
    SLINGS = "Slings"
    SPEARS = "Spears"
    TRIDENTS = "Tridents"
    WARHAMMERS = "Warhammers"
    WARPICKS = "Warpicks"


class ProgressionType(StrEnum):
    CHALLENGERATING = "ChallengeRating"
    LEVEL = "Level"


class ProjectileDistribution(StrEnum):
    EDGE = "Edge"
    EDGECENTER = "EdgeCenter"
    NORMAL = "Normal"
    RANDOM = "Random"


class ProjectileType(StrEnum):
    ARROW = "Arrow"
    GRENADE = "Grenade"
    NONE = "None"


class Properties(str):
    pass


class Qualifier(str):
    _VALID_VALUES = {
        "0",
        "1",
        "10",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "None",
    }

    def __new__(cls, value: str):
        value = str(value)
        if value not in cls._VALID_VALUES:
            raise KeyError(f"{value} is not a member of Qualifier")
        return super().__new__(cls, value)


class Rarity(StrEnum):
    COMMON = "Common"
    LEGENDARY = "Legendary"
    RARE = "Rare"
    UNCOMMON = "Uncommon"
    VERYRARE = "VeryRare"


class Relation(StrEnum):
    ALLY = "Ally"
    ENEMY = "Enemy"
    NEUTRAL = "Neutral"
    PERSISTENTNEUTRAL = "Persistent Neutral"


class Requirements(str):
    pass


class ResistanceFlags(StrEnum):
    IMMUNE = "Immune"
    IMMUNETOMAGICAL = "ImmuneToMagical"
    IMMUNETONONMAGICAL = "ImmuneToNonMagical"
    NONE = "None"
    RESISTANT = "Resistant"
    RESISTANTTOMAGICAL = "ResistantToMagical"
    RESISTANTTONONMAGICAL = "ResistantToNonMagical"
    VULNERABLE = "Vulnerable"
    VULNERABLETOMAGICAL = "VulnerableToMagical"
    VULNERABLETONONMAGICAL = "VulnerableToNonMagical"


class RestErrorFlags(StrEnum):
    COMBAT = "Combat"
    DIALOG = "Dialog"
    DOWNEDORDEAD = "DownedOrDead"
    FTB = "FTB"
    GLOBALDISABLED = "GlobalDisabled"
    NONE = "None"
    NOTENOUGHRESOURCES = "NotEnoughResources"
    SCRIPT = "Script"


class RollConditions(str):
    pass


class Skill(StrEnum):
    ACROBATICS = "Acrobatics"
    AIRSPECIALIST = "AirSpecialist"
    ANIMALHANDLING = "AnimalHandling"
    ARCANA = "Arcana"
    ATHLETICS = "Athletics"
    BREWMASTER = "Brewmaster"
    CRAFTING = "Crafting"
    DECEPTION = "Deception"
    DUALWIELDING = "DualWielding"
    FIRESPECIALIST = "FireSpecialist"
    HISTORY = "History"
    INSIGHT = "Insight"
    INTIMIDATION = "Intimidation"
    INVESTIGATION = "Investigation"
    LEADERSHIP = "Leadership"
    LUCK = "Luck"
    MAGICARMORMASTERY = "MagicArmorMastery"
    MEDICINE = "Medicine"
    NONE = "None"
    PERCEPTION = "Perception"
    PERFORMANCE = "Performance"
    PERSEVERANCE = "Perseverance"
    PERSUASION = "Persuasion"
    PHYSICALARMORMASTERY = "PhysicalArmorMastery"
    POLYMORPH = "Polymorph"
    RANGED = "Ranged"
    RANGERLORE = "RangerLore"
    REASON = "Reason"
    RELIGION = "Religion"
    REPAIR = "Repair"
    ROGUELORE = "RogueLore"
    RUNECRAFTING = "Runecrafting"
    SHIELD = "Shield"
    SINGLEHANDED = "SingleHanded"
    SLEIGHTOFHAND = "SleightOfHand"
    STEALTH = "Stealth"
    SULFUROLOGY = "Sulfurology"
    SURVIVAL = "Survival"
    THIEVERY = "Thievery"
    TWOHANDED = "TwoHanded"
    WAND = "Wand"
    WARRIORLORE = "WarriorLore"
    WATERSPECIALIST = "WaterSpecialist"


class SoundVocalType(StrEnum):
    ALERT = "ALERT"
    ANGRY = "ANGRY"
    ANTICIPATION = "ANTICIPATION"
    ATTACK = "ATTACK"
    AWAKE = "AWAKE"
    BORED = "BORED"
    BUFF = "BUFF"
    DEATH = "DEATH"
    DODGE = "DODGE"
    EFFORTS = "EFFORTS"
    EXHAUSTED = "EXHAUSTED"
    FALL = "FALL"
    GASP = "GASP"
    IDLE1 = "IDLE1"
    IDLE2 = "IDLE2"
    IDLE3 = "IDLE3"
    IDLECOMBAT1 = "IDLECOMBAT1"
    IDLECOMBAT2 = "IDLECOMBAT2"
    IDLECOMBAT3 = "IDLECOMBAT3"
    INITIATIVE = "INITIATIVE"
    LAUGHTER = "LAUGHTER"
    LAUGHTERMANIACAL = "LAUGHTERMANIACAL"
    MAX = "MAX"
    NONE = "NONE"
    PAIN = "PAIN"
    REBORN = "REBORN"
    RECOVER = "RECOVER"
    RELAXED = "RELAXED"
    SHOUT = "SHOUT"
    SNORE = "SNORE"
    SPAWN = "SPAWN"
    VICTORY = "VICTORY"
    WEAK = "WEAK"


class SpellAttackType(StrEnum):
    DIRECTHIT = "DirectHit"
    MELEESPELLATTACK = "MeleeSpellAttack"
    MELEEWEAPONATTACK = "MeleeWeaponAttack"
    RANGEDSPELLATTACK = "RangedSpellAttack"
    RANGEDWEAPONATTACK = "RangedWeaponAttack"


class SpellActionType(StrEnum):
    DASH = "Dash"
    DIP = "Dip"
    DISENGAGE = "Disengage"
    DISMISS = "Dismiss"
    DISTRACT = "Distract"
    HELP = "Help"
    HIDE = "Hide"
    IMPROVISEDWEAPON = "ImprovisedWeapon"
    JUMP = "Jump"
    KNOCKOUT = "Knockout"
    NONE = "None"
    SHOVE = "Shove"
    THROW = "Throw"


class SpellAnimationIntentType(StrEnum):
    ACTION = "Action"
    AGGRESSIVE = "Aggressive"
    NONE = "None"
    PEACEFUL = "Peaceful"


class SpellAnimationType(StrEnum):
    ASSISTING = "Assisting"
    DIPPING = "Dipping"
    IMPROVISEDWEAPON = "ImprovisedWeapon"
    JUMPING = "Jumping"
    NONE = "None"
    RESTRAIN = "Restrain"
    SHOVING = "Shoving"
    TELEKINESIS = "Telekinesis"
    THROWING = "Throwing"


class SpellCategoryFlags(StrEnum):
    SC_DASH = "SC_Dash"
    SC_DETECTTHOUGHTS = "SC_DetectThoughts"
    SC_INTENTBUFF = "SC_IntentBuff"
    SC_INTENTDAMAGE = "SC_IntentDamage"
    SC_INTENTDEBUFF = "SC_IntentDebuff"
    SC_INTENTHEALING = "SC_IntentHealing"
    SC_INTENTUTILITY = "SC_IntentUtility"
    SC_JUMP = "SC_Jump"
    SC_NONE = "SC_None"
    SC_TARGETAOE = "SC_TargetAoE"
    SC_TARGETMULTISELECT = "SC_TargetMultiselect"
    SC_TARGETSINGLE = "SC_TargetSingle"


class SpellElement(StrEnum):
    NONE = "None"


class SpellFlagList(StrEnum):
    ABORTONSECONDARYSPELLROLLFAIL = "AbortOnSecondarySpellRollFail"
    ABORTONSPELLROLLFAIL = "AbortOnSpellRollFail"
    ADDFALLDAMAGEONLAND = "AddFallDamageOnLand"
    ADDWEAPONRANGE = "AddWeaponRange"
    ALLOWMOVEANDCAST = "AllowMoveAndCast"
    CALLALLIESSPELL = "CallAlliesSpell"
    CANAREADAMAGEEVADE = "CanAreaDamageEvade"
    CANDUALWIELD = "CanDualWield"
    CANNOTROTATE = "CannotRotate"
    CANNOTTARGETCHARACTER = "CannotTargetCharacter"
    CANNOTTARGETITEMS = "CannotTargetItems"
    CANNOTTARGETTERRAIN = "CannotTargetTerrain"
    COMBATLOGSETSINGLELINEROLL = "CombatLogSetSingleLineRoll"
    CONCENTRATIONIGNORESRESTING = "ConcentrationIgnoresResting"
    DISABLEBLOOD = "DisableBlood"
    DISPLAYDAMAGEMODIFIERS = "DisplayDamageModifiers"
    DISPLAYINITEMTOOLTIP = "DisplayInItemTooltip"
    DONTABORTPERFORMING = "DontAbortPerforming"
    HASHIGHGROUNDRANGEEXTENSION = "HasHighGroundRangeExtension"
    HASSOMATICCOMPONENT = "HasSomaticComponent"
    HASVERBALCOMPONENT = "HasVerbalComponent"
    HIDEINITEMTOOLTIP = "HideInItemTooltip"
    IGNOREAOO = "IgnoreAoO"
    IGNOREPREVIOUSLYPICKEDENTITIES = "IgnorePreviouslyPickedEntities"
    IGNORESILENCE = "IgnoreSilence"
    IGNOREVISIONBLOCK = "IgnoreVisionBlock"
    IMMEDIATECAST = "ImmediateCast"
    INVENTORYSELECTION = "InventorySelection"
    INVISIBLE = "Invisible"
    ISATTACK = "IsAttack"
    ISCONCENTRATION = "IsConcentration"
    ISDEFAULTWEAPONACTION = "IsDefaultWeaponAction"
    ISENEMYSPELL = "IsEnemySpell"
    ISHARMFUL = "IsHarmful"
    ISJUMP = "IsJump"
    ISLINKEDSPELLCONTAINER = "IsLinkedSpellContainer"
    ISMELEE = "IsMelee"
    ISSPELL = "IsSpell"
    ISSWARMATTACK = "IsSwarmAttack"
    ISTRAP = "IsTrap"
    NOAOEDAMAGEONLAND = "NoAOEDamageOnLand"
    NOCAMERAMOVE = "NoCameraMove"
    NOCOOLDOWNONMISS = "NoCooldownOnMiss"
    NOSURPRISE = "NoSurprise"
    NONE = "None"
    PICKUPENTITYANDMOVE = "PickupEntityAndMove"
    RANGEIGNOREBLINDNESS = "RangeIgnoreBlindness"
    RANGEIGNORESOURCEBOUNDS = "RangeIgnoreSourceBounds"
    RANGEIGNORETARGETBOUNDS = "RangeIgnoreTargetBounds"
    RANGEIGNOREVERTICALTHRESHOLD = "RangeIgnoreVerticalThreshold"
    STEALTH = "Stealth"
    TARGETCLOSESTEQUALGROUNDSURFACE = "TargetClosestEqualGroundSurface"
    TEMPORARY = "Temporary"
    TRAJECTORYRULES = "TrajectoryRules"
    UNUSED_D = "UNUSED_D"
    UNUSED_E = "UNUSED_E"
    UNAVAILABLEINDIALOGS = "UnavailableInDialogs"
    WILDSHAPE = "Wildshape"


class SpellJumpType(StrEnum):
    FLIGHT = "Flight"
    JUMP = "Jump"
    NONE = "None"
    POUNCE = "Pounce"


class SpellRequirement(StrEnum):
    ARROWWEAPON = "ArrowWeapon"
    DAGGERWEAPON = "DaggerWeapon"
    MELEEWEAPON = "MeleeWeapon"
    NONE = "None"
    RANGEDWEAPON = "RangedWeapon"
    RIFLEWEAPON = "RifleWeapon"
    SHIELDWEAPON = "ShieldWeapon"
    STAFFWEAPON = "StaffWeapon"


class SpellSchool(StrEnum):
    ABJURATION = "Abjuration"
    CONJURATION = "Conjuration"
    DIVINATION = "Divination"
    ENCHANTMENT = "Enchantment"
    EVOCATION = "Evocation"
    ILLUSION = "Illusion"
    NECROMANCY = "Necromancy"
    NONE = "None"
    TRANSMUTATION = "Transmutation"


class SpellSheathing(StrEnum):
    DONTCHANGE = "DontChange"
    INSTRUMENT = "Instrument"
    MELEE = "Melee"
    RANGED = "Ranged"
    SHEATHED = "Sheathed"
    SOMATIC = "Somatic"
    WEAPONSET = "WeaponSet"


class SpellSoundMagnitude(StrEnum):
    BIG = "Big"
    NONE = "None"
    NORMAL = "Normal"
    SMALL = "Small"


class SpellStyleGroup(StrEnum):
    CLASS = "Class"
    CLASS_INTENT = "Class_Intent"
    INTENT = "Intent"


class StatsFunctorContext(StrEnum):
    AOE = "AOE"
    AIIGNORE = "AiIgnore"
    AIONLY = "AiOnly"
    GROUND = "Ground"
    NONE = "None"
    ONABILITYCHECK = "OnAbilityCheck"
    ONACTIONRESOURCESCHANGED = "OnActionResourcesChanged"
    ONATTACK = "OnAttack"
    ONATTACKED = "OnAttacked"
    ONCAST = "OnCast"
    ONCASTRESOLVED = "OnCastResolved"
    ONCOMBATENDED = "OnCombatEnded"
    ONCOMBATSTARTED = "OnCombatStarted"
    ONCREATE = "OnCreate"
    ONDAMAGE = "OnDamage"
    ONDAMAGEPREVENTED = "OnDamagePrevented"
    ONDAMAGED = "OnDamaged"
    ONDAMAGEDPREVENTED = "OnDamagedPrevented"
    ONENTERATTACKRANGE = "OnEnterAttackRange"
    ONENTITYATTACKEDWITHINMELEERANGE = "OnEntityAttackedWithinMeleeRange"
    ONENTITYATTACKINGWITHINMELEERANGE = "OnEntityAttackingWithinMeleeRange"
    ONEQUIP = "OnEquip"
    ONHEAL = "OnHeal"
    ONHEALED = "OnHealed"
    ONINTERRUPTUSED = "OnInterruptUsed"
    ONINVENTORYCHANGED = "OnInventoryChanged"
    ONLEAVEATTACKRANGE = "OnLeaveAttackRange"
    ONLOCKPICKINGSUCCEEDED = "OnLockpickingSucceeded"
    ONLONGREST = "OnLongRest"
    ONMOVEDDISTANCE = "OnMovedDistance"
    ONOBSCURITYCHANGED = "OnObscurityChanged"
    ONPROFICIENCYCHANGE = "OnProficiencyChange"
    ONPROJECTILEEXPLODED = "OnProjectileExploded"
    ONPUSH = "OnPush"
    ONPUSHED = "OnPushed"
    ONROUND = "OnRound"
    ONSHORTREST = "OnShortRest"
    ONSTATUSAPPLIED = "OnStatusApplied"
    ONSTATUSAPPLY = "OnStatusApply"
    ONSTATUSREMOVE = "OnStatusRemove"
    ONSTATUSREMOVED = "OnStatusRemoved"
    ONSURFACEENTER = "OnSurfaceEnter"
    ONTURN = "OnTurn"
    TARGET = "Target"


class StatsFunctors(str):
    pass


class StatusAnimationType(StrEnum):
    BLINDED = "Blinded"
    CHANNELING = "Channeling"
    CLIMBING = "Climbing"
    DANCING = "Dancing"
    DAZED = "Dazed"
    DOWNED = "Downed"
    FEARED = "Feared"
    FRIGHTENED = "Frightened"
    GRAPPLED = "Grappled"
    GRAPPLING = "Grappling"
    KO = "KO"
    KO_FALLEN = "KO_Fallen"
    LAUGHING = "Laughing"
    LAUGHING_HIDEOUS = "Laughing_Hideous"
    LONGREST = "LongRest"
    MENTAL = "Mental"
    NONE = "None"
    PERFORMING1 = "Performing1"
    PERFORMING10 = "Performing10"
    PERFORMING2 = "Performing2"
    PERFORMING3 = "Performing3"
    PERFORMING4 = "Performing4"
    PERFORMING5 = "Performing5"
    PERFORMING6 = "Performing6"
    PERFORMING7 = "Performing7"
    PERFORMING8 = "Performing8"
    PERFORMING9 = "Performing9"
    PERFORMINGFAIL = "PerformingFail"
    PETRIFIED = "Petrified"
    SHOUTING = "Shouting"
    SITTING = "Sitting"
    SLEEPING = "Sleeping"
    SNARED = "Snared"
    SNEAKING = "Sneaking"
    SUFFOCATING = "Suffocating"
    SWAPPED = "Swapped"
    WEAKENED = "Weakened"


class StatusEvent(StrEnum):
    NONE = "None"
    ONAPPLY = "OnApply"
    ONAPPLYANDTURN = "OnApplyAndTurn"
    ONATTACK = "OnAttack"
    ONATTACKED = "OnAttacked"
    ONCOMBATENDED = "OnCombatEnded"
    ONDAMAGE = "OnDamage"
    ONDISARMINGFINISHED = "OnDisarmingFinished"
    ONENTITYDRAG = "OnEntityDrag"
    ONENTITYDROP = "OnEntityDrop"
    ONENTITYPICKUP = "OnEntityPickUp"
    ONEQUIP = "OnEquip"
    ONFACTIONCHANGED = "OnFactionChanged"
    ONHEAL = "OnHeal"
    ONLOCKPICKINGFINISHED = "OnLockpickingFinished"
    ONLOCKPICKINGSUCCEEDED = "OnLockpickingSucceeded"
    ONMOVE = "OnMove"
    ONOBSCURITYCHANGED = "OnObscurityChanged"
    ONREMOVE = "OnRemove"
    ONREMOVEPERFORMANCEREQUEST = "OnRemovePerformanceRequest"
    ONSOURCEDEATH = "OnSourceDeath"
    ONSOURCESTATUSAPPLIED = "OnSourceStatusApplied"
    ONSPELLCAST = "OnSpellCast"
    ONSTATUSAPPLIED = "OnStatusApplied"
    ONSTATUSREMOVED = "OnStatusRemoved"
    ONSURFACEENTER = "OnSurfaceEnter"
    ONTURN = "OnTurn"
    ONUNEQUIP = "OnUnequip"
    UNUSED1 = "UNUSED1"


class StatusGroupFlags(StrEnum):
    SG_APPROACHING = "SG_Approaching"
    SG_BLINDED = "SG_Blinded"
    SG_CANBEPICKEDUP = "SG_CanBePickedUp"
    SG_CHARMED = "SG_Charmed"
    SG_CHARMED_SUBTLE = "SG_Charmed_Subtle"
    SG_CONDITION = "SG_Condition"
    SG_CONFUSED = "SG_Confused"
    SG_CURSED = "SG_Cursed"
    SG_DETECTTHOUGHTS = "SG_DetectThoughts"
    SG_DIFFICULTTERRAIN = "SG_DifficultTerrain"
    SG_DISEASE = "SG_Disease"
    SG_DISGUISE = "SG_Disguise"
    SG_DOMINATED = "SG_Dominated"
    SG_DOPPELGANGER = "SG_Doppelganger"
    SG_DROPFORNONMUTINGDIALOG = "SG_DropForNonMutingDialog"
    SG_DRUNK = "SG_Drunk"
    SG_EXHAUSTED = "SG_Exhausted"
    SG_FLEEING = "SG_Fleeing"
    SG_FRIGHTENED = "SG_Frightened"
    SG_HELPABLE_CONDITION = "SG_Helpable_Condition"
    SG_HEXBLADECURSE = "SG_HexbladeCurse"
    SG_IGNORE_AOO = "SG_Ignore_AOO"
    SG_INCAPACITATED = "SG_Incapacitated"
    SG_INVISIBLE = "SG_Invisible"
    SG_LIGHT = "SG_Light"
    SG_MAD = "SG_Mad"
    SG_NONE = "SG_None"
    SG_PARALYZED = "SG_Paralyzed"
    SG_PETRIFIED = "SG_Petrified"
    SG_POISONED = "SG_Poisoned"
    SG_POISONED_STORY_NONREMOVABLE = "SG_Poisoned_Story_Nonremovable"
    SG_POISONED_STORY_REMOVABLE = "SG_Poisoned_Story_Removable"
    SG_POLYMORPH = "SG_Polymorph"
    SG_POLYMORPH_BEASTSHAPE = "SG_Polymorph_BeastShape"
    SG_POLYMORPH_BEASTSHAPE_NPC = "SG_Polymorph_BeastShape_NPC"
    SG_POSSESSED = "SG_Possessed"
    SG_PRONE = "SG_Prone"
    SG_RAGE = "SG_Rage"
    SG_REMOVEONRESPEC = "SG_RemoveOnRespec"
    SG_RESTRAINED = "SG_Restrained"
    SG_SCRIPTEDPEACEBEHAVIOUR = "SG_ScriptedPeaceBehaviour"
    SG_SLEEPING = "SG_Sleeping"
    SG_STUNNED = "SG_Stunned"
    SG_SURFACE = "SG_Surface"
    SG_TAUNTED = "SG_Taunted"
    SG_UNCONSCIOUS = "SG_Unconscious"
    SG_WEAPONCOATING = "SG_WeaponCoating"


class StatusHealType(StrEnum):
    ALL = "All"
    ALLARMOR = "AllArmor"
    MAGICARMOR = "MagicArmor"
    NONE = "None"
    PHYSICALARMOR = "PhysicalArmor"
    SOURCE = "Source"
    VITALITY = "Vitality"


class StatusIDs(str):
    pass


class StatusPropertyFlags(StrEnum):
    ALLOWLEAVECOMBAT = "AllowLeaveCombat"
    ALLOWLEAVEDISALLOWJOINCOMBAT = "AllowLeaveDisallowJoinCombat"
    APPLYTODEAD = "ApplyToDead"
    BLIND = "Blind"
    BRINGINTOCOMBAT = "BringIntoCombat"
    BURNING = "Burning"
    DISABLECAPABILITIESMESSAGE = "DisableCapabilitiesMessage"
    DISABLECOMBATLOG = "DisableCombatlog"
    DISABLEIMMUNITYOVERHEAD = "DisableImmunityOverhead"
    DISABLEINTERACTIONS = "DisableInteractions"
    DISABLEOVERHEAD = "DisableOverhead"
    DISABLEPORTRAITINDICATOR = "DisablePortraitIndicator"
    EXCLUDEFROMPORTRAITRENDERING = "ExcludeFromPortraitRendering"
    EXECUTEFUNCTORSONOWNER = "ExecuteFunctorsOnOwner"
    FORCENEUTRALINTERACTIONS = "ForceNeutralInteractions"
    FORCEOVERHEAD = "ForceOverhead"
    FREEZEDURATION = "FreezeDuration"
    GIVEEXP = "GiveExp"
    IGNORERESTING = "IgnoreResting"
    IGNOREDBYIMMOBILIZED = "IgnoredByImmobilized"
    INDICATEDARKNESS = "IndicateDarkness"
    INITIATECOMBAT = "InitiateCombat"
    ISCHANNELED = "IsChanneled"
    ISINVULNERABLE = "IsInvulnerable"
    ISINVULNERABLEVISIBLE = "IsInvulnerableVisible"
    LOSECONTROL = "LoseControl"
    LOSECONTROLFRIENDLY = "LoseControlFriendly"
    MULTIPLYEFFECTSBYDURATION = "MultiplyEffectsByDuration"
    NONEXTENDABLE = "NonExtendable"
    NONE = "None"
    OVERHEADONTURN = "OverheadOnTurn"
    PEACEONLY = "PeaceOnly"
    PERFORMING = "Performing"
    TICKINGWITHSOURCE = "TickingWithSource"
    TOGGLE = "Toggle"
    UNAVAILABLEINACTIVEROLL = "UnavailableInActiveRoll"
    UNSHEATHINSTRUMENT = "UnsheathInstrument"


class StatusSheathing(StrEnum):
    INSTRUMENT = "Instrument"
    MELEE = "Melee"
    NONE = "None"
    RANGED = "Ranged"
    SHEATHED = "Sheathed"


class StatusStackType(StrEnum):
    ADDITIVE = "Additive"
    DEACTIVATE = "Deactivate"
    IGNORE = "Ignore"
    OVERWRITE = "Overwrite"
    STACK = "Stack"
    VARIABLE = "Variable"


class StepsType(StrEnum):
    BARE = "Bare"
    BONE = "Bone"
    CLAWED = "Clawed"
    HOOVES = "Hooves"
    LEATHER = "Leather"
    METAL = "Metal"
    SPIDER = "Spider"


class StillAnimPriority(StrEnum):
    BLINDED = "Blinded"
    DANCE = "Dance"
    DAZED = "Dazed"
    DOWNED = "Downed"
    FEARED = "Feared"
    FRIGHTENED = "Frightened"
    KO = "KO"
    KO_FALLEN = "KO_Fallen"
    LAUGHING = "Laughing"
    MENTAL = "Mental"
    PERFORMING = "Performing"
    SHOUTING = "Shouting"
    SITTING = "Sitting"
    SLEEPING = "Sleeping"
    SNARED = "Snared"
    SNEAKING = "Sneaking"
    SUFFOCATING = "Suffocating"
    WEAKENED = "Weakened"


class SurfaceChange(StrEnum):
    CLEAR = "Clear"
    CONDENSE = "Condense"
    DAYLIGHT = "Daylight"
    DEELECTRIFY = "Deelectrify"
    DESTROYWATER = "DestroyWater"
    DOUSE = "Douse"
    ELECTRIFY = "Electrify"
    FREEZE = "Freeze"
    IGNITE = "Ignite"
    MELT = "Melt"
    NONE = "None"
    TURNHELLFIRE = "TurnHellfire"
    UNTURNHELLFIRE = "UnturnHellfire"
    VAPORIZE = "Vaporize"


class SurfaceType(StrEnum):
    ACID = "Acid"
    ALCOHOL = "Alcohol"
    ALIENOIL = "Alienoil"
    ASH = "Ash"
    BLACKPOWDERDETONATIONCLOUD = "BlackPowderDetonationCloud"
    BLACKTENTACLES = "BlackTentacles"
    BLACKPOWDER = "Blackpowder"
    BLADEBARRIER = "BladeBarrier"
    BLOOD = "Blood"
    BLOODCLOUD = "BloodCloud"
    BLOODELECTRIFIED = "BloodElectrified"
    BLOODEXPLODING = "BloodExploding"
    BLOODFROZEN = "BloodFrozen"
    BLOODSILVER = "BloodSilver"
    CAUSTICBRINE = "CausticBrine"
    CHASM = "Chasm"
    CLOUDKILL6CLOUD = "Cloudkill6Cloud"
    CLOUDKILLCLOUD = "CloudkillCloud"
    CRAWLERMUCUSCLOUD = "CrawlerMucusCloud"
    DARKNESSCLOUD = "DarknessCloud"
    DEEPWATER = "Deepwater"
    DROWPOISONCLOUD = "DrowPoisonCloud"
    EXPLOSIONCLOUD = "ExplosionCloud"
    FIRE = "Fire"
    FOGCLOUD = "FogCloud"
    GITHPHEROMONEGASCLOUD = "GithPheromoneGasCloud"
    GREASE = "Grease"
    HELLFIRE = "Hellfire"
    HOLYFIRE = "HolyFire"
    ICECLOUD = "IceCloud"
    INVISIBLEGITHACID = "InvisibleGithAcid"
    INVISIBLEWEB = "InvisibleWeb"
    LAVA = "Lava"
    MALICECLOUD = "MaliceCloud"
    MUD = "Mud"
    NONE = "None"
    OIL = "Oil"
    OVERGROWTH = "Overgrowth"
    POISON = "Poison"
    POISONCLOUD = "PoisonCloud"
    POTIONANTITOXINCLOUD = "PotionAntitoxinCloud"
    POTIONHEALINGCLOUD = "PotionHealingCloud"
    POTIONHEALINGGREATERCLOUD = "PotionHealingGreaterCloud"
    POTIONHEALINGSUPERIORCLOUD = "PotionHealingSuperiorCloud"
    POTIONHEALINGSUPREMECLOUD = "PotionHealingSupremeCloud"
    POTIONINVISIBILITYCLOUD = "PotionInvisibilityCloud"
    POTIONRESISTANCEACIDCLOUD = "PotionResistanceAcidCloud"
    POTIONRESISTANCECOLDCLOUD = "PotionResistanceColdCloud"
    POTIONRESISTANCEFIRECLOUD = "PotionResistanceFireCloud"
    POTIONRESISTANCEFORCECLOUD = "PotionResistanceForceCloud"
    POTIONRESISTANCELIGHTNINGCLOUD = "PotionResistanceLightningCloud"
    POTIONRESISTANCEPOISONCLOUD = "PotionResistancePoisonCloud"
    POTIONSPEEDCLOUD = "PotionSpeedCloud"
    POTIONVITALITYCLOUD = "PotionVitalityCloud"
    PURPLEWORMPOISON = "PurpleWormPoison"
    SENTINEL = "Sentinel"
    SERPENTVENOM = "SerpentVenom"
    SEWER = "Sewer"
    SHADOWCURSEDVINES = "ShadowCursedVines"
    SHOCKWAVECLOUD = "ShockwaveCloud"
    SPIKEGROWTH = "SpikeGrowth"
    SPOREBLACKCLOUD = "SporeBlackCloud"
    SPOREGREENCLOUD = "SporeGreenCloud"
    SPOREPINKCLOUD = "SporePinkCloud"
    SPOREWHITECLOUD = "SporeWhiteCloud"
    STINKINGCLOUD = "StinkingCloud"
    TRIALFIRE = "TrialFire"
    VINES = "Vines"
    VOIDCLOUD = "VoidCloud"
    WATER = "Water"
    WATERCLOUD = "WaterCloud"
    WATERCLOUDELECTRIFIED = "WaterCloudElectrified"
    WATERELECTRIFIED = "WaterElectrified"
    WATERFROZEN = "WaterFrozen"
    WEB = "Web"
    WYVERNPOISON = "WyvernPoison"


class SurfaceCollisionFlags(str):
    pass


class TagCategory(StrEnum):
    CODE = "Code"
    DIALOG = "Dialog"
    GENDER = "Gender"
    NONE = "None"
    ORIGIN = "Origin"
    PROFESSION = "Profession"
    RACE = "Race"
    STORY = "Story"
    VOICE = "Voice"


class TargetConditions(str):
    pass


class Tension(StrEnum):
    ANY = "any"
    HIGH = "high"
    LOW = "low"


class ThrowOrigin(StrEnum):
    CASTER = "Caster"
    TARGET = "Target"


class TickType(StrEnum):
    ENDROUND = "EndRound"
    ENDTURN = "EndTurn"
    STARTROUND = "StartRound"
    STARTTURN = "StartTurn"


class TranslatedString(str):
    pass


class VerbalIntent(StrEnum):
    BUFF = "Buff"
    CONTROL = "Control"
    DAMAGE = "Damage"
    DEBUFF = "Debuff"
    HEALING = "Healing"
    NONE = "None"
    SUMMON = "Summon"
    UTILITY = "Utility"


class WeaponGroup(StrEnum):
    MARTIALMELEEWEAPON = "MartialMeleeWeapon"
    MARTIALRANGEDWEAPON = "MartialRangedWeapon"
    SIMPLEMELEEWEAPON = "SimpleMeleeWeapon"
    SIMPLERANGEDWEAPON = "SimpleRangedWeapon"


class WeaponFlags(StrEnum):
    ADDTOHOTBAR = "AddToHotbar"
    AMMUNITION = "Ammunition"
    DIPPABLE = "Dippable"
    FINESSE = "Finesse"
    HEAVY = "Heavy"
    LANCE = "Lance"
    LIGHT = "Light"
    LOADING = "Loading"
    MAGICAL = "Magical"
    MELEE = "Melee"
    NEEDDUALWIELDINGBOOST = "NeedDualWieldingBoost"
    NET = "Net"
    NODUALWIELD = "NoDualWield"
    NONE = "None"
    NOTSHEATHABLE = "NotSheathable"
    RANGE = "Range"
    REACH = "Reach"
    THROWN = "Thrown"
    TORCH = "Torch"
    TWOHANDED = "Twohanded"
    UNSTOWABLE = "Unstowable"
    VERSATILE = "Versatile"


class WeaponSet(StrEnum):
    MELEE = "Melee"
    RANGED = "Ranged"


class YesNo(StrEnum):
    NO = "No"
    YES = "Yes"


VALUELISTS = [
    AIFlags,
    Ability,
    AbilityFlags,
    Act,
    ActionType,
    AlchemyCombinationType,
    ArmorType,
    AtmosphereType,
    AttributeFlags,
    AuraFlags,
    BigQualifier,
    CastCheckType,
    CinematicArenaFlags,
    Conditions,
    ConstantFloat,
    ConstantInt,
    CooldownType,
    CursorMode,
    CustomProperties,
    DamageType,
    DamageSourceType,
    DeathType,
    DieType,
    DisturbanceDialogueCapability,
    DisturbanceInvestigationKind,
    DisturbanceMergeConditions,
    DisturbanceYesNoIgnoreStats,
    FixedString,
    FlagType,
    FormatStringColor,
    GameAction,
    Guid,
    Handedness,
    HealValueType,
    HitAnimationType,
    IngredientCombineType,
    IngredientTransformType,
    IngredientType,
    InstrumentType,
    InterruptContext,
    InterruptContextScope,
    InterruptDefaultValue,
    InterruptFlagsList,
    InventoryTabs,
    ItemUseTypes,
    Itemslot,
    LEDEffectType,
    LineOfSightFlags,
    ManagedStatusEffectType,
    MaterialType,
    MemorizationRequirements,
    ModifierType,
    ObjectSize,
    OsirisTask,
    PassiveFlags,
    PenaltyPreciseQualifier,
    PenaltyQualifier,
    PickingState,
    PreciseQualifier,
    ProficiencyGroupFlags,
    ProgressionType,
    ProjectileDistribution,
    ProjectileType,
    Properties,
    Qualifier,
    Rarity,
    Relation,
    Requirements,
    ResistanceFlags,
    RestErrorFlags,
    RollConditions,
    Skill,
    SoundVocalType,
    SpellAttackType,
    SpellActionType,
    SpellAnimationIntentType,
    SpellAnimationType,
    SpellCategoryFlags,
    SpellElement,
    SpellFlagList,
    SpellJumpType,
    SpellRequirement,
    SpellSchool,
    SpellSheathing,
    SpellSoundMagnitude,
    SpellStyleGroup,
    StatsFunctorContext,
    StatsFunctors,
    StatusAnimationType,
    StatusEvent,
    StatusGroupFlags,
    StatusHealType,
    StatusIDs,
    StatusPropertyFlags,
    StatusSheathing,
    StatusStackType,
    StepsType,
    StillAnimPriority,
    SurfaceChange,
    SurfaceType,
    SurfaceCollisionFlags,
    TagCategory,
    TargetConditions,
    Tension,
    ThrowOrigin,
    TickType,
    TranslatedString,
    VerbalIntent,
    WeaponGroup,
    WeaponFlags,
    WeaponSet,
    YesNo,
]
