#!/usr/bin/env python3
"""
Character class enumeration.
"""

from enum import StrEnum
from typing import Final


class CharacterClass(StrEnum):
    """Baldur's Gate 3 character classes as found in Progressions.lsx."""
    # Base classes
    BARBARIAN = "Barbarian"
    BARD = "Bard"
    CLERIC = "Cleric"
    DRUID = "Druid"
    FIGHTER = "Fighter"
    MONK = "Monk"
    PALADIN = "Paladin"
    RANGER = "Ranger"
    ROGUE = "Rogue"
    SORCERER = "Sorcerer"
    WARLOCK = "Warlock"
    WIZARD = "Wizard"

    # Subclasses
    BARBARIAN_BERSERKER = "BerserkerPath"
    BARBARIAN_GIANT = "GiantPath"
    BARBARIAN_WILDHEART = "TotemWarriorPath"
    BARBARIAN_WILDMAGIC = "WildMagicPath"

    BARD_GLAMOUR = "GlamourCollege"
    BARD_LORE = "LoreCollege"
    BARD_SWORDS = "SwordsCollege"
    BARD_VALOR = "ValorCollege"

    CLERIC_DEATH = "DeathDomain"
    CLERIC_KNOWLEDGE = "KnowledgeDomain"
    CLERIC_LIFE = "LifeDomain"
    CLERIC_LIGHT = "LightDomain"
    CLERIC_NATURE = "NatureDomain"
    CLERIC_TEMPEST = "TempestDomain"
    CLERIC_TRICKERY = "TrickeryDomain"
    CLERIC_WAR = "WarDomain"

    DRUID_LAND = "CircleOfTheLand"
    DRUID_MOON = "CircleOfTheMoon"
    DRUID_SPORES = "CircleOfTheSpores"
    DRUID_STARS = "CircleOfStars"

    FIGHTER_ARCANEARCHER = "ArcaneArcher"
    FIGHTER_BATTLEMASTER = "BattleMaster"
    FIGHTER_CHAMPION = "Champion"
    FIGHTER_ELDRITCHKNIGHT = "EldritchKnight"

    MONK_DRUNKENMASTER = "DrunkenMaster"
    MONK_FOURELEMENTS = "FourElements"
    MONK_OPENHAND = "OpenHand"
    MONK_SHADOW = "Shadow"

    PALADIN_ANCIENTS = "Ancients"
    PALADIN_CROWN = "Crown"
    PALADIN_DEVOTION = "Devotion"
    PALADIN_OATHBREAKER = "Oathbreaker"
    PALADIN_VENGEANCE = "Vengeance"

    RANGER_BEASTMASTER = "BeastMaster"
    RANGER_GLOOMSTALKER = "GloomStalker"
    RANGER_HUNTER = "Hunter"
    RANGER_SWARMKEEPER = "Swarmkeeper"

    ROGUE_ARCANETRICKSTER = "ArcaneTrickster"
    ROGUE_ASSASSIN = "Assassin"
    ROGUE_THIEF = "Thief"
    ROGUE_SWASHBUCKLER = "Swashbuckler"

    SORCERER_DRACONIC = "DraconicBloodline"
    SORCERER_SHADOWMAGIC = "ShadowMagic"
    SORCERER_STORM = "StormSorcery"
    SORCERER_WILDMAGIC = "WildMagic"

    WARLOCK_ARCHFEY = "Archfey"
    WARLOCK_FIEND = "Fiend"
    WARLOCK_GREATOLDONE = "GreatOldOne"
    WARLOCK_HEXBLADE = "Hexblade"

    WIZARD_ABJURATION = "AbjurationSchool"
    WIZARD_BLADESINGING = "BladesingingSchool"
    WIZARD_CONJURATION = "ConjurationSchool"
    WIZARD_DIVINATION = "DivinationSchool"
    WIZARD_ENCHANTMENT = "EnchantmentSchool"
    WIZARD_EVOCATION = "EvocationSchool"
    WIZARD_ILLUSION = "IllusionSchool"
    WIZARD_NECROMANCY = "NecromancySchool"
    WIZARD_TRANSMUTATION = "TransmutationSchool"

    # Pseudo class for multiclass spell slots
    MULTICLASS_SPELL_SLOTS = "MulticlassSpellSlots"


BASE_CHARACTER_CLASSES: Final = frozenset([
    CharacterClass.BARBARIAN,
    CharacterClass.BARD,
    CharacterClass.CLERIC,
    CharacterClass.DRUID,
    CharacterClass.FIGHTER,
    CharacterClass.MONK,
    CharacterClass.PALADIN,
    CharacterClass.RANGER,
    CharacterClass.ROGUE,
    CharacterClass.SORCERER,
    CharacterClass.WARLOCK,
    CharacterClass.WIZARD,
    CharacterClass.MULTICLASS_SPELL_SLOTS,
])


class CharacterSubclasses:
    """Sets of character class and subclasses by primary class."""
    BARBARIAN: Final = frozenset([
        CharacterClass.BARBARIAN,
        CharacterClass.BARBARIAN_BERSERKER,
        CharacterClass.BARBARIAN_GIANT,
        CharacterClass.BARBARIAN_WILDHEART,
        CharacterClass.BARBARIAN_WILDMAGIC,
    ])
    BARD: Final = frozenset([
        CharacterClass.BARD,
        CharacterClass.BARD_GLAMOUR,
        CharacterClass.BARD_LORE,
        CharacterClass.BARD_SWORDS,
        CharacterClass.BARD_VALOR,
    ])
    CLERIC: Final = frozenset([
        CharacterClass.CLERIC,
        CharacterClass.CLERIC_DEATH,
        CharacterClass.CLERIC_KNOWLEDGE,
        CharacterClass.CLERIC_LIFE,
        CharacterClass.CLERIC_LIGHT,
        CharacterClass.CLERIC_NATURE,
        CharacterClass.CLERIC_TEMPEST,
        CharacterClass.CLERIC_TRICKERY,
        CharacterClass.CLERIC_WAR,
    ])
    DRUID: Final = frozenset([
        CharacterClass.DRUID,
        CharacterClass.DRUID_LAND,
        CharacterClass.DRUID_MOON,
        CharacterClass.DRUID_SPORES,
        CharacterClass.DRUID_STARS,
    ])
    FIGHTER: Final = frozenset([
        CharacterClass.FIGHTER,
        CharacterClass.FIGHTER_ARCANEARCHER,
        CharacterClass.FIGHTER_BATTLEMASTER,
        CharacterClass.FIGHTER_CHAMPION,
        CharacterClass.FIGHTER_ELDRITCHKNIGHT,
    ])
    MONK: Final = frozenset([
        CharacterClass.MONK,
        CharacterClass.MONK_DRUNKENMASTER,
        CharacterClass.MONK_FOURELEMENTS,
        CharacterClass.MONK_OPENHAND,
        CharacterClass.MONK_SHADOW,
    ])
    PALADIN: Final = frozenset([
        CharacterClass.PALADIN,
        CharacterClass.PALADIN_ANCIENTS,
        CharacterClass.PALADIN_CROWN,
        CharacterClass.PALADIN_DEVOTION,
        CharacterClass.PALADIN_OATHBREAKER,
        CharacterClass.PALADIN_VENGEANCE,
    ])
    RANGER: Final = frozenset([
        CharacterClass.RANGER,
        CharacterClass.RANGER_BEASTMASTER,
        CharacterClass.RANGER_GLOOMSTALKER,
        CharacterClass.RANGER_HUNTER,
        CharacterClass.RANGER_SWARMKEEPER,
    ])
    ROGUE: Final = frozenset([
        CharacterClass.ROGUE,
        CharacterClass.ROGUE_ARCANETRICKSTER,
        CharacterClass.ROGUE_ASSASSIN,
        CharacterClass.ROGUE_THIEF,
        CharacterClass.ROGUE_SWASHBUCKLER,
    ])
    SORCERER: Final = frozenset([
        CharacterClass.SORCERER,
        CharacterClass.SORCERER_DRACONIC,
        CharacterClass.SORCERER_SHADOWMAGIC,
        CharacterClass.SORCERER_STORM,
        CharacterClass.SORCERER_WILDMAGIC,
    ])
    WARLOCK: Final = frozenset([
        CharacterClass.WARLOCK,
        CharacterClass.WARLOCK_ARCHFEY,
        CharacterClass.WARLOCK_FIEND,
        CharacterClass.WARLOCK_GREATOLDONE,
        CharacterClass.WARLOCK_HEXBLADE,
    ])
    WIZARD: Final = frozenset([
        CharacterClass.WIZARD,
        CharacterClass.WIZARD_ABJURATION,
        CharacterClass.WIZARD_BLADESINGING,
        CharacterClass.WIZARD_CONJURATION,
        CharacterClass.WIZARD_DIVINATION,
        CharacterClass.WIZARD_ENCHANTMENT,
        CharacterClass.WIZARD_EVOCATION,
        CharacterClass.WIZARD_ILLUSION,
        CharacterClass.WIZARD_NECROMANCY,
        CharacterClass.WIZARD_TRANSMUTATION,
    ])
    MULTICLASS_SPELL_SLOTS: Final = frozenset([
        CharacterClass.MULTICLASS_SPELL_SLOTS,
    ])
    ALL: Final = (BARBARIAN | BARD | CLERIC | DRUID | FIGHTER | MONK | PALADIN | RANGER | ROGUE | SORCERER | WARLOCK |
                  WIZARD | MULTICLASS_SPELL_SLOTS)
