#!/usr/bin/env python3
"""
A decorator for class description replacement.
"""

from collections.abc import Callable, Iterable
from modtools.lsx.game import CharacterClass
from modtools.lsx import Lsx
from modtools.lsx.game import ClassDescription
from modtools.replacers.replacer import Replacer
from uuid import UUID


type ClassDescriptionBuilder = Callable[[Replacer, ClassDescription], None]
type ClassDescriptionBuilderDict = dict[CharacterClass, ClassDescriptionBuilder]


_CLASS_DESCRIPTIONS_LSX_PATH = "Shared.pak/Public/Shared/ClassDescriptions/ClassDescriptions.lsx"
_CLASS_DESCRIPTIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/ClassDescriptions/ClassDescriptions.lsx"


def _by_name(class_description: ClassDescription) -> str:
    return class_description.Name


def _by_uuid(class_description: ClassDescription) -> UUID:
    return class_description.UUID


def _load_class_descriptions(replacer: Replacer) -> list[ClassDescription]:
    """Load the game's Progressions from the .pak cache."""
    class_descriptions_lsx = Lsx.load(replacer.get_cache_path(_CLASS_DESCRIPTIONS_LSX_PATH))
    class_descriptions_dev_lsx = Lsx.load(replacer.get_cache_path(_CLASS_DESCRIPTIONS_DEV_LSX_PATH))
    class_descriptions_lsx.children.update(class_descriptions_dev_lsx.children, key=_by_uuid)
    class_descriptions_lsx.children.sort(key=_by_name)
    return list(class_descriptions_lsx.children)


def _make_builders(class_description_builders: list[ClassDescriptionBuilder]) -> ClassDescriptionBuilderDict:
    """Make a ClassDescriptionBuilderDict from the decorated class description builders."""
    builders: ClassDescriptionBuilderDict = dict()

    for class_description_builder in class_description_builders:
        class_description_classes = getattr(class_description_builder, "class_description_classes")
        for character_class in class_description_classes:
            builders[character_class] = class_description_builder

    return builders


def _update_class_descriptions(replacer: Replacer,
                               class_descriptions: list[ClassDescription],
                               builders: ClassDescriptionBuilderDict,
                               updated_class_descriptions: set[ClassDescription]):
    """Update class descriptions that match our builder classes."""
    for class_description in class_descriptions:
        if builder_fn := builders.get(class_description.Name):
            builder_fn(replacer, class_description)
            updated_class_descriptions.add(class_description)


def _class_description_builder(replacer: Replacer, class_description_builders: list[ClassDescriptionBuilder]) -> None:
    """Update existing class descriptions."""
    builders = _make_builders(class_description_builders)

    class_descriptions = _load_class_descriptions(replacer)
    updated_class_descriptions: set[ClassDescription] = set()

    _update_class_descriptions(replacer, class_descriptions, builders, updated_class_descriptions)

    # Save the updated class descriptions
    for class_description in sorted(updated_class_descriptions, key=_by_name):
        replacer.mod.add(class_description)


def class_description(character_classes: CharacterClass | Iterable[CharacterClass]) -> ClassDescriptionBuilder:
    """A decorator mapping classes to their class description builder function."""
    if isinstance(character_classes, str) or not isinstance(character_classes, Iterable):
        character_classes = [character_classes]

    def decorate(fn: ClassDescriptionBuilder) -> ClassDescriptionBuilder:
        setattr(fn, "builder", _class_description_builder)
        class_description_classes: list[CharacterClass] = getattr(fn, "class_description_classes", [])
        class_description_classes.extend(character_classes)
        setattr(fn, "class_description_classes", class_description_classes)
        return fn

    return decorate
