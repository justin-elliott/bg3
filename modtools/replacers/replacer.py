#!/usr/bin/env python3
"""
A base class for character progression replacers.
"""

import argparse
import os

from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from moddb import multiply_resources
from modtools.lsx.game import (
    ActionResource,
    BASE_CHARACTER_CLASSES,
    CharacterClass,
    CharacterSubclasses,
    Dependencies,
    Progression,
)
from modtools.mod import Mod
from typing import ClassVar, Final
from uuid import UUID


class Replacer:
    """Base class for game content replacers."""
    @dataclass
    class Args:
        name: str                                      # Mod name
        classes: list[CharacterClass]                  # Class progressions to replace
        feats: set[int]                                # Feat improvement levels
        spells: int                                    # Multiplier for spell slots
        warlock_spells: int                            # Multiplier for Warlock spell slots
        actions: int                                   # Multiplier for other action resources
        skills: int                                    # Number of skills to select at character creation
        expertise: int                                 # Number of skill expertises to select at character creation
        full_caster: bool = False                      # Update spell slot progression to be a full caster
        include: list[str] = None                      # Third-party mods to include
        fighter_feats: set[int] = None                 # Fighter feat improvement levels
        rogue_feats: set[int] = None                   # Rogue feat improvement levels
        other_feats: set[int] = None                   # All other classes feat improvement levels
        included_classes: list[CharacterClass] = None  # The classes belonging together with the named classes

    ACTION_RESOURCES: Final[set[ActionResource]] = frozenset([
        ActionResource.ARCANE_RECOVERY_CHARGES,
        ActionResource.ARCANE_SHOT_CHARGES,
        ActionResource.BARDIC_INSPIRATION_CHARGES,
        ActionResource.BLADESONG_CHARGES,
        ActionResource.CHANNEL_DIVINITY_CHARGES,
        ActionResource.CHANNEL_OATH_CHARGES,
        ActionResource.COSMIC_OMEN_POINTS,
        ActionResource.FUNGAL_INFESTATION_CHARGES,
        ActionResource.KI_POINTS,
        ActionResource.LAY_ON_HANDS_CHARGES,
        ActionResource.NATURAL_RECOVERY_CHARGES,
        ActionResource.RAGE_CHARGES,
        ActionResource.SORCERY_POINTS,
        ActionResource.STAR_MAP_POINTS,
        ActionResource.SUPERIORITY_DICE,
        ActionResource.SWARM_CHARGES,
        ActionResource.WAR_PRIEST_CHARGES,
        ActionResource.WILD_SHAPE_CHARGES,
        ActionResource.WRITHING_TIDE_POINTS,
    ])

    _FIGHTER_EXTRA_FEATS: Final[dict[int, set[int]]] = {
        1: set(),
        2: {3, 5, 13},
        3: {5, 14},
        4: {6, 14},
    }

    _ROGUE_EXTRA_FEATS: Final[dict[int, set[int]]] = {
        1: set(),
        2: {3, 9},
        3: {10},
        4: {10},
    }

    # Spell slots for a full caster
    _SPELL_SLOTS: Final[dict[int, list[int]]] = {
        0: [],
        1: [2],
        2: [3],
        3: [4, 2],
        4: [4, 3],
        5: [4, 3, 2],
        6: [4, 3, 3],
        7: [4, 3, 3, 1],
        8: [4, 3, 3, 2],
        9: [4, 3, 3, 3, 1],
        10: [4, 3, 3, 3, 2],
        11: [4, 3, 3, 3, 2, 1],
        12: [4, 3, 3, 3, 2, 1],
        13: [4, 3, 3, 3, 2, 1, 1],
        14: [4, 3, 3, 3, 2, 1, 1],
        15: [4, 3, 3, 3, 2, 1, 1, 1],
        16: [4, 3, 3, 3, 2, 1, 1, 1],
        17: [4, 3, 3, 3, 2, 1, 1, 1, 1],
        18: [4, 3, 3, 3, 3, 1, 1, 1, 1],
        19: [4, 3, 3, 3, 3, 2, 1, 1, 1],
        20: [4, 3, 3, 3, 3, 2, 2, 1, 1],
    }

    _SPELL_SLOT_DELTA: Final[dict[int, list[int]]]

    _LIMITED_CASTERS: Final[set[CharacterClass]] = {
        CharacterClass.PALADIN,
        CharacterClass.RANGER,
        CharacterClass.ROGUE_ARCANETRICKSTER,
        CharacterClass.FIGHTER_ELDRITCHKNIGHT,
    }

    _NON_CASTERS: Final[set[CharacterClass]] = (
        CharacterSubclasses.BARBARIAN |
        (CharacterSubclasses.FIGHTER - {CharacterClass.FIGHTER_ELDRITCHKNIGHT}) |
        CharacterSubclasses.MONK |
        (CharacterSubclasses.ROGUE - {CharacterClass.ROGUE_ARCANETRICKSTER})
    )

    _builders: ClassVar[dict[Callable, list[Callable]]]

    _args: Args
    _mod: Mod

    def __new__(cls, *args: str, **kwds: str):
        """Create the class, populating the _builders list."""
        cls._builders = dict()

        # Find all of the builders that have been declared and add them to the _builders dictionary.
        for field in cls.__dict__.values():
            if builder := getattr(field, "builder", None):
                fns = cls._builders.setdefault(builder, [])
                fns.append(field)

        return super().__new__(cls)

    def __init__(self, base_dir: str, *, author: str, **kwds: str):
        self._parse_arguments(**kwds)
        self._mod = Mod(base_dir,
                        author=author,
                        name=self.args.name,
                        mod_uuid=kwds.get("mod_uuid"),
                        description=kwds.get("description", ""),
                        folder=kwds.get("folder"),
                        version=kwds.get("version", (4, 1, 1, 1)),
                        cache_dir=kwds.get("cache_dir"))

        self._mod.add(Dependencies.ShortModuleDesc(
            Folder="UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            MD5="f94d034502139cf8b65a1597554e7236",
            Name="UnlockLevelCurve",
            PublishHandle=4166963,
            UUID="a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            Version64=72057594037927960,
        ))

    @staticmethod
    def _class_list(s: str) -> list[CharacterClass]:
        classes = [CharacterClass(cc) for cc in s.split(",")]
        if not set(classes).issubset(CharacterSubclasses.ALL):
            raise "Invalid class names"
        return classes

    @staticmethod
    def _level_list(s: str) -> set[int]:
        levels = frozenset([int(level) for level in s.split(",")])
        if not levels.issubset(range(1, 21)):
            raise "Invalid feat levels"
        if len(levels) == 1 and not levels.issubset(range(1, 5)):
            raise "Feat level must be in the range 1 to 4"
        return levels

    def _update_feat_levels(self) -> None:
        if len(self.args.feats) in range(0, 2):
            feat_level = next(level for level in self.args.feats) if len(self.args.feats) == 1 else 4
            self.args.other_feats = frozenset(
                {*range(max(feat_level, 2), 20, feat_level)} | ({19} if 20 % feat_level == 0 else set()))
            self.args.fighter_feats = self.args.other_feats | self._FIGHTER_EXTRA_FEATS[feat_level]
            self.args.rogue_feats = self.args.other_feats | self._ROGUE_EXTRA_FEATS[feat_level]
        else:
            self.args.other_feats = self.args.feats - frozenset([1, 20])
            self.args.fighter_feats = self.args.other_feats
            self.args.rogue_feats = self.args.other_feats

    def _update_classes(self) -> None:
        classes: OrderedDict[CharacterClass, None] = OrderedDict()
        included_classes: OrderedDict[CharacterClass, None] = OrderedDict()

        if len(self.args.classes) == 0:
            self.args.classes = sorted(CharacterSubclasses.ALL)

        for character_class in self.args.classes:
            classes[character_class] = None

            if character_class in BASE_CHARACTER_CLASSES:
                included_classes[character_class] = None
                for subclass in sorted(vars(CharacterSubclasses)[character_class.name] - {character_class}):
                    included_classes[subclass] = None
            else:
                included_classes[[base_class for base_class in BASE_CHARACTER_CLASSES
                                if character_class in vars(CharacterSubclasses)[base_class.name]][0]] = None
                included_classes[character_class] = None
        
        self.args.classes = [*classes.keys()]
        self.args.included_classes = [*included_classes.keys()]

    def _parse_arguments(self, **kwds: str) -> None:
        name = kwds.get("name")
        classes = kwds.get("classes", list())
        feats = kwds.get("feats", 4)
        feats = set(feats) if isinstance(feats, list) else {feats}
        spells = kwds.get("spells", 1)
        warlock_spells = kwds.get("warlock_spells", 1)
        actions = kwds.get("actions", 1)
        skills = kwds.get("skills")
        expertise = kwds.get("expertise")
        full_caster = kwds.get("full_caster", False)
        include = kwds.get("include", None)

        parser = argparse.ArgumentParser(description="A mod replacer.")
        parser.add_argument("-n", "--name", type=str, default=name,
                            help="Mod name")
        parser.add_argument("-c", "--classes", type=self._class_list, default=classes,
                            help=f"Classes to include in the progression (default: {
                                ", ".join([cls.value for cls in classes])})")
        parser.add_argument("-f", "--feats", type=self._level_list, default=feats,
                            help=f"Feat progression every n levels (default: {", ".join(map(str, sorted(feats)))})")
        parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=spells,
                            help=f"Spell slot multiplier (default: {spells})")
        parser.add_argument("-w", "--warlock_spells", type=int, choices=range(1, 17), default=warlock_spells,
                            help=f"Warlock spell slot multiplier (default: {warlock_spells})")
        parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=actions,
                            help=f"Action resource multiplier (default: {actions})")
        parser.add_argument("-k", "--skills", type=int, default=skills,
                            help=f"Number of skills to select at level 1 (default: {skills})")
        parser.add_argument("-e", "--expertise", type=int, default=expertise,
                            help=f"Number of skills with expertise to select at level 1 (default: {expertise})")
        parser.add_argument("--full-caster", action="store_true", default=full_caster,
                            help=f"Update spell slot progression to be a full caster")
        parser.add_argument("--include", type=str, action="append", default=include,
                            help="Include a third-party mod in the progression.")
        self._args = Replacer.Args(**vars(parser.parse_args()))

        if self.args.name is None:
            if (name := self.make_name()) is None:
                parser.error("the name argument is required: -n/--name")
            self.args.name = name
        self._update_feat_levels()
        self._update_classes()

    def make_name(self) -> str:
        """Generate a name for the Mod."""
        return None

    @property
    def args(self) -> Args:
        """Return our arguments."""
        return self._args

    @property
    def mod(self) -> Mod:
        """Return our Mod."""
        return self._mod

    def get_cache_path(self, lsx_path: os.PathLike) -> os.PathLike:
        """Get the path of a file in the unpak cache."""
        return self._mod.get_cache_path(lsx_path)

    def make_name(self, suffix: str) -> str:
        return self._mod.make_name(suffix)

    def make_uuid(self, key: str) -> UUID:
        """Generate a UUID for the given key."""
        return self._mod.make_uuid("Replacer:" + key)

    def allow_improvement(self, progression: Progression) -> bool:
        if progression.Name not in BASE_CHARACTER_CLASSES or progression.Level == 1:
            return False
        character_class = CharacterClass(progression.Name)
        if character_class not in self.args.included_classes:
            return False
        feats = (self.args.rogue_feats if character_class == CharacterClass.ROGUE
                else self.args.fighter_feats if character_class == CharacterClass.FIGHTER
                else self.args.other_feats)
        allow_improvement = progression.AllowImprovement
        progression.AllowImprovement = (progression.Level in feats) or (False if allow_improvement == False else None)
        return allow_improvement != progression.AllowImprovement

    def adjust_resources(self, progression: Progression) -> bool:
        if progression.Name not in CharacterClass:
            return False
        character_class = CharacterClass(progression.Name)
        if character_class not in self.args.included_classes:
            return False
        existing_boosts = progression.Boosts
        existing_passives = progression.PassivesAdded
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self.args.spells)
        multiply_resources(progression, [ActionResource.WARLOCK_SPELL_SLOTS], self.args.warlock_spells)
        multiply_resources(progression, self.ACTION_RESOURCES, self.args.actions)
        if self.args.full_caster:
            self._adjust_resources_full_caster(character_class, progression)
        progression.Boosts = progression.Boosts or None
        progression.PassivesAdded = progression.PassivesAdded or None
        return existing_boosts != progression.Boosts or existing_passives != progression.PassivesAdded
    
    def _adjust_resources_full_caster(self, character_class: CharacterClass, progression: Progression) -> None:
        if (character_class in self._LIMITED_CASTERS or
            (character_class in self.args.classes and character_class in self._NON_CASTERS)):
            progression.Boosts = [
                *[boost for boost in (progression.Boosts or []) if not boost.startswith("ActionResource(SpellSlot")],
                *[
                    f"ActionResource(SpellSlot,{self.args.spells * delta},{spell_level})"
                    for spell_level in range(1, 10)
                    if (delta := self._SPELL_SLOT_DELTA[progression.Level][spell_level - 1]) > 0
                ],
            ]
            progression.PassivesAdded = [
                *[
                    passive for passive in (progression.PassivesAdded or [])
                    if not passive.startswith("UnlockedSpellSlotLevel")
                ],
                *(
                    [f"UnlockedSpellSlotLevel{(progression.Level + 1) // 2}"]
                    if progression.Level in (1, 3, 5, 7, 9) else []
                ),
            ]

    def adjust_skills(self, progression: Progression) -> bool:
        if progression.Name not in BASE_CHARACTER_CLASSES or progression.Level != 1 or progression.IsMulticlass:
            return False
        character_class = CharacterClass(progression.Name)
        if character_class not in self.args.included_classes:
            return False
        selectors = progression.Selectors
        if self.args.skills is not None:
            selectors = [selector for selector in (selectors or []) if not selector.startswith("SelectSkills(")]
            selectors.append(f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self.args.skills})")
        if self.args.expertise is not None:
            selectors = [selector for selector in selectors if not selector.startswith("SelectSkillsExpertise(")]
            selectors.append(f"SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self.args.expertise})")
        if progression.Selectors == selectors:
            return False
        progression.Selectors = selectors
        return True

    def build(self) -> None:
        """Build the mod."""
        for builder, fns in self._builders.items():
            builder(self, fns)
        self._mod.build()

Replacer._SPELL_SLOT_DELTA = {
    level: [
        (Replacer._SPELL_SLOTS[level][i] if i < len(Replacer._SPELL_SLOTS[level]) else 0) -
        (Replacer._SPELL_SLOTS[level - 1][i] if i < len(Replacer._SPELL_SLOTS[level - 1]) else 0)
        for i in range(0, 9)
    ] for level in range(1, 21)
}
