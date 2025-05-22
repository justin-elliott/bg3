#!/usr/bin/env python3
"""
A base class for character progression replacers.
"""

import argparse
import os

from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from modtools.lsx.game import (
    ActionResource,
    BASE_CHARACTER_CLASSES,
    CharacterClass,
    CharacterSubclasses,
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

    _builders: ClassVar[dict[Callable, list[Callable]]]

    _args: Args
    _mod: Mod

    def __new__(cls, *args, **kwds):
        """Create the class, populating the _builders list."""
        cls._builders = dict()

        # Find all of the builders that have been declared and add them to the _builders dictionary.
        for field in cls.__dict__.values():
            if builder := getattr(field, "builder", None):
                fns = cls._builders.setdefault(builder, [])
                fns.append(field)

        return super().__new__(cls)

    def __init__(self, base_dir: str, *, author: str, **kwds: str):
        self._parse_arguments()
        self._mod = Mod(base_dir, author=author, name=self.args.name, **kwds)

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

        for name in self.args.classes:
            character_class = CharacterClass(name)
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

    def _parse_arguments(self) -> None:
        parser = argparse.ArgumentParser(description="A mod replacer.")
        parser.add_argument("-n", "--name", type=str,
                            help="Mod name")
        parser.add_argument("-c", "--classes", type=self._class_list, default=set(),
                            help="Classes to include in the progression (defaulting to all)")
        parser.add_argument("-f", "--feats", type=self._level_list, default=set(),
                            help="Feat progression every n levels (defaulting to normal progression)")
        parser.add_argument("-s", "--spells", type=int, choices=range(1, 9), default=1,
                            help="Spell slot multiplier (defaulting to 1; normal spell slots)")
        parser.add_argument("-w", "--warlock_spells", type=int, choices=range(1, 9), default=1,
                            help="Warlock spell slot multiplier (defaulting to 1; normal spell slots)")
        parser.add_argument("-a", "--actions", type=int, choices=range(1, 9), default=1,
                            help="Action resource multiplier (defaulting to 1; normal resources)")
        parser.add_argument("-k", "--skills", type=int,
                            help="Number of skills to select at level 1")
        parser.add_argument("-e", "--expertise", type=int,
                            help="Number of skills with expertise to select at level 1")
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

    def make_uuid(self, key: str) -> UUID:
        """Generate a UUID for the given key."""
        return self._mod.make_uuid("Replacer:" + key)

    def build(self) -> None:
        """Build the mod."""
        for builder, fns in self._builders.items():
            builder(self, fns)
        self._mod.build()
