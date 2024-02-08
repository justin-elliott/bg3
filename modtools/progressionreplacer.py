#!/usr/bin/env python3
"""
A base class for character progression replacers.
"""

from collections.abc import Callable, Container, Iterable
from modtools.lsx.game import CharacterClass
from modtools.lsx import Lsx
from modtools.lsx.game import ClassDescription, Progression
from modtools.mod import Mod
from typing import ClassVar
from uuid import UUID


type ClassLevelKey = tuple[CharacterClass, int, bool]
type MultiClassLevelKey = tuple[list[CharacterClass], list[int], bool]
type ProgressionBuilder = Callable[[object, Progression], None]
type ClassDescriptionBuilder = Callable[[object, ClassDescription], None]


def class_description(character_classes: CharacterClass | Iterable[CharacterClass]) -> ClassDescriptionBuilder:
    """A decorator mapping classes to their class description builder function."""
    if isinstance(character_classes, CharacterClass):
        character_classes = [character_classes]

    def decorate(fn: ClassDescriptionBuilder) -> ClassDescriptionBuilder:
        class_description_classes: list[CharacterClass] = getattr(fn, "class_description_classes", [])
        class_description_classes.extend(character_classes)
        setattr(fn, "class_description_classes", class_description_classes)
        return fn

    return decorate


def class_level(character_classes: CharacterClass | Iterable[CharacterClass],
                levels: int | Iterable[int],
                *,
                is_multiclass: bool = False) -> ProgressionBuilder:
    """A decorator mapping class/level combinations to their progression builder function."""
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

    CLASS_DESCRIPTIONS_LSX_PATH = "Shared.pak/Public/Shared/ClassDescriptions/ClassDescriptions.lsx"
    CLASS_DESCRIPTIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/ClassDescriptions/ClassDescriptions.lsx"

    PROGRESSIONS_LSX_PATH = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
    PROGRESSIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"

    _class_description: ClassVar[dict[CharacterClass, ClassDescriptionBuilder]] = {}
    _class_level: ClassVar[dict[ClassLevelKey, ProgressionBuilder]] = {}

    _mod: Mod
    _classes: Container[CharacterClass]

    def __new__(cls, *args, **kwds):
        """Create the class, populating the _class_level dictionary."""
        for prop in cls.__dict__.values():
            # ClassDescription builders
            class_description_classes: list[CharacterClass]
            if class_description_classes := getattr(prop, "class_description_classes", None):
                fn: ClassDescriptionBuilder = prop
                for character_class in class_description_classes:
                    cls._class_description[character_class] = fn

            # Progression builders
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

    def mod(self) -> Mod:
        """Return our Mod."""
        return self._mod

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
        if self._class_description:
            class_descriptions = self._load_class_descriptions()
            for class_description in class_descriptions:
                if builder := self._class_description.get(CharacterClass(class_description.Name)):
                    builder(self, class_description)
                    self._mod.add(class_description)

        class_level = dict(self._class_level)
        progressions = self._load_progressions()
        updated_progressions: list[Progression] = []

        self.preprocess(progressions)

        # Pass the existing progression to the defined builder functions
        for progression in progressions:
            key = (CharacterClass(progression.Name), progression.Level, progression.IsMulticlass or False)
            if builder := class_level.get(key):
                builder(self, progression)
                updated_progressions.append(progression)
                del class_level[key]

        # Call the builder functions that did not match an existing progression
        for key, builder in class_level.items():
            character_class, level, is_multiclass = key
            progression = self.make_progression(character_class, level)
            if is_multiclass:
                progression.IsMulticlass = True
            progressions.append(progression)
            builder(self, progression)
            updated_progressions.append(progression)

        updated_progressions.sort(key=self._by_name_level_multiclass)
        self.postprocess(updated_progressions)

        for progression in updated_progressions:
            self._mod.add(progression)

        self._mod.build()

    def _load_class_descriptions(self) -> list[ClassDescription]:
        """Load the game's ClassDescriptions from the .pak cache."""
        def by_name(class_description: ClassDescription) -> str:
            return CharacterClass(class_description.Name).name

        def by_uuid(class_description: ClassDescription) -> UUID:
            return class_description.UUID

        def is_one_of_our_classes(class_description: ClassDescription) -> bool:
            return class_description.Name in self._class_description

        class_descriptions_lsx = Lsx.load(self._mod.get_cache_path(self.CLASS_DESCRIPTIONS_LSX_PATH))
        class_descriptions_dev_lsx = Lsx.load(self._mod.get_cache_path(self.CLASS_DESCRIPTIONS_DEV_LSX_PATH))
        class_descriptions_lsx.children.update(class_descriptions_dev_lsx.children, key=by_uuid)

        class_descriptions_lsx.children.keepall(is_one_of_our_classes)
        class_descriptions_lsx.children.sort(key=by_name)

        return list(class_descriptions_lsx.children)

    def _load_progressions(self) -> list[Progression]:
        """Load the game's Progressions from the .pak cache."""
        def by_uuid(progression: Progression) -> UUID:
            return progression.UUID

        def is_one_of_our_classes(progression: Progression) -> bool:
            return progression.Name in self._classes

        progressions_lsx = Lsx.load(self._mod.get_cache_path(self.PROGRESSIONS_LSX_PATH))
        progressions_dev_lsx = Lsx.load(self._mod.get_cache_path(self.PROGRESSIONS_DEV_LSX_PATH))
        progressions_lsx.children.update(progressions_dev_lsx.children, key=by_uuid)

        progressions_lsx.children.keepall(is_one_of_our_classes)
        progressions_lsx.children.sort(key=self._by_name_level_multiclass)

        return list(progressions_lsx.children)

    @staticmethod
    def _by_name_level_multiclass(progression: Progression) -> tuple[str, int, bool]:
        return (CharacterClass(progression.Name).name, progression.Level, progression.IsMulticlass or False)
