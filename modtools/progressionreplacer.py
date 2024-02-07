#!/usr/bin/env python3
"""
A base class for character progression replacers.
"""

from collections.abc import Callable, Container, Iterable
from modtools.lsx.game import CharacterClass
from modtools.lsx import Lsx
from modtools.lsx.game import Progression
from modtools.mod import Mod
from typing import ClassVar
from uuid import UUID


type ClassLevelKey = tuple[CharacterClass, int, bool]
type MultiClassLevelKey = tuple[list[CharacterClass], list[int], bool]
type ProgressionBuilder = Callable[[object, Progression], None]


def class_level(character_classes: CharacterClass | Iterable[CharacterClass],
                levels: int | Iterable[int],
                *,
                is_multiclass: bool = False) -> ProgressionBuilder:
    """A decorator mapping class/level combinations to their builder function."""
    if isinstance(character_classes, CharacterClass):
        character_classes = [character_classes]
    if isinstance(levels, int):
        levels = [levels]

    def decorate(fn: ProgressionBuilder) -> ProgressionBuilder:
        class_levels: list[MultiClassLevelKey] = getattr(fn, "class_levels", [])
        class_levels.append((character_classes, levels, is_multiclass))
        setattr(fn, "class_levels", class_levels)
        return fn

    return decorate


class ProgressionReplacer:
    """Generate replacers for class progressions."""

    PROGRESSIONS_LSX_PATH = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
    PROGRESSIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"

    _class_level: ClassVar[dict[ClassLevelKey, ProgressionBuilder]] = {}

    _mod: Mod
    _classes: Container[CharacterClass]

    def __new__(cls, *args, **kwds):
        """Create the class, populating the _class_level dictionary."""
        for prop in cls.__dict__.values():
            class_levels: list[MultiClassLevelKey]
            if class_levels := getattr(prop, "class_levels", None):
                fn: ProgressionBuilder = prop
                for character_classes, levels, is_multiclass in class_levels:
                    for character_class in character_classes:
                        for level in levels:
                            key = ((character_class, level, is_multiclass))
                            if key in cls._class_level:
                                raise KeyError(f"{key} is already defined")
                            cls._class_level[key] = fn
        return super().__new__(cls)

    def __init__(self,
                 base_dir: str,
                 *,
                 author: str,
                 name: str,
                 classes: Container[CharacterClass],
                 **kwds: str):
        """Create a ProgressionReplacer instance for the given classes."""
        self._mod = Mod(base_dir, author=author, name=name, **kwds)
        self._classes = classes

    def make_uuid(self, key: str) -> UUID:
        """Generate a UUID for the given key."""
        return self._mod.make_uuid(f"ProgressionReplacer:{key}")

    def preprocess(self, progressions: Iterable[Progression]) -> None:
        """Apply any preprocessing steps to the loaded game progressions."""
        pass

    def postprocess(self, progressions: Iterable[Progression]) -> None:
        """Apply any postprocessing steps to the updated progressions."""
        pass

    def make_progression(self, character_class: CharacterClass, level: int) -> Progression:
        """Return a Progression for the given character class and level. """
        raise NotImplementedError("make_progression() must be overridden by a subclass")

    def build(self) -> None:
        """Build the new progression."""
        class_level = dict(self._class_level)
        progressions = self._load_game_progressions()

        self.preprocess(progressions)

        # Pass the existing progression to the defined builder functions
        for progression in progressions:
            key = (CharacterClass(progression.Name), progression.Level, progression.IsMulticlass or False)
            if builder := class_level.get(key):
                builder(self, progression)
                del class_level[key]

        # Call the builder functions that did not match an existing progression
        for key, builder in class_level.items():
            character_class, level, is_multiclass = key
            progression = self.make_progression(character_class, level)
            if is_multiclass:
                progression.IsMulticlass = True
            progressions.append(progression)
            builder(self, progression)

        progressions.sort(key=self._by_name_level_multiclass)
        self.postprocess(progressions)

        for progression in progressions:
            self._mod.add(progression)

        self._mod.build()

    def _load_game_progressions(self) -> list[Progression]:
        """Load the game configuration from the .pak cache."""
        progressions_lsx = Lsx.load(self._mod.get_cache_path(self.PROGRESSIONS_LSX_PATH))
        progressions_dev_lsx = Lsx.load(self._mod.get_cache_path(self.PROGRESSIONS_DEV_LSX_PATH))
        progressions_lsx.children.update(progressions_dev_lsx.children, key=self._by_uuid)

        progressions_lsx.children.keepall(self._is_one_of_our_classes)
        progressions_lsx.children.sort(key=self._by_name_level_multiclass)

        return list(progressions_lsx.children)

    @staticmethod
    def _by_uuid(progression: Progression) -> UUID:
        """Key by UUID."""
        return progression.UUID

    @staticmethod
    def _by_name_level_multiclass(progression: Progression) -> tuple[str, int, bool]:
        return (CharacterClass(progression.Name).name, progression.Level, progression.IsMulticlass or False)

    def _is_one_of_our_classes(self, progression: Progression) -> bool:
        """Determine if this one of the classes that we're replacing."""
        return progression.Name in self._classes
