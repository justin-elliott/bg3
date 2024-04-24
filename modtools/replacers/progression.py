#!/usr/bin/env python3
"""
A decorator for class/race progression replacement.
"""

from collections.abc import Callable, Iterable
from enum import IntEnum
from modtools.lsx.game import BASE_CHARACTER_CLASSES, CharacterClass, CharacterRace
from modtools.lsx import Lsx
from modtools.lsx.game import Progression
from modtools.replacers.replacer import Replacer


class DontIncludeProgression(BaseException):
    """Raised to exclude a progression from being updated."""
    pass


class _Classification(IntEnum):
    CLASS = 1
    RACE = 2
    OTHER = 3  # NPC classes, origin characters


type NameLevelKey = tuple[str, int, bool]
type MultiNameLevelKey = tuple[list[str], list[int], bool]
type ProgressionBuilder = Callable[[Replacer, Progression], None]
type ProgressionBuilderDict = dict[NameLevelKey, list[ProgressionBuilder]]


_PROGRESSIONS_LSX_PATH = "Shared.pak/Public/Shared/Progressions/Progressions.lsx"
_PROGRESSIONS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx"


def _by_uuid(progression: Progression) -> str:
    return progression.UUID


def _progression_order(progression: Progression) -> tuple[str, int, bool]:
    """Return a key ordering by classification, name, level, and multiclass."""
    name = progression.Name
    classification = _Classification.OTHER
    if name in CharacterClass:
        name = CharacterClass(progression.Name).name
        classification = _Classification.CLASS
    elif name in CharacterRace:
        name = CharacterRace(progression.Name).name
        classification = _Classification.RACE

    return (classification, name, progression.Level, progression.IsMulticlass or False)


def _load_progressions(replacer: Replacer) -> list[Progression]:
    """Load the game's Progressions from the .pak cache."""
    progressions_lsx = Lsx.load(replacer.get_cache_path(_PROGRESSIONS_LSX_PATH))
    progressions_dev_lsx = Lsx.load(replacer.get_cache_path(_PROGRESSIONS_DEV_LSX_PATH))
    progressions_lsx.children.update(progressions_dev_lsx.children, key=_by_uuid)
    progressions_lsx.children.sort(key=_progression_order)
    return list(progressions_lsx.children)


def _make_builders(progression_builders: list[ProgressionBuilder]) -> ProgressionBuilderDict:
    """Make a ProgressionBuilderDict from the decorated progression builders."""
    builders: ProgressionBuilderDict = dict()

    for progression_builder in progression_builders:
        multi_class_level_keys = getattr(progression_builder, "progression")
        for names, levels, is_multiclass in multi_class_level_keys:
            for name in names:
                for level in levels:
                    builder_fns = builders.setdefault((name, level, is_multiclass), [])
                    builder_fns.append(progression_builder)

    return builders


def _update_progressions(replacer: Replacer,
                         progressions: list[Progression],
                         builders: ProgressionBuilderDict,
                         tableUuid: dict[str, str],
                         updated_progressions: set[Progression]):
    """Update progressions that match our builder keys."""
    for progression in progressions:
        if progression.TableUUID:  # Ignore the one entry without a TableUUID
            tableUuid[progression.Name] = progression.TableUUID
            progression_key = (progression.Name, progression.Level, progression.IsMulticlass or False)
            if builder_fns := builders.get(progression_key):
                was_updated = False
                for builder_fn in builder_fns:
                    try:
                        builder_fn(replacer, progression)
                        was_updated = True
                    except DontIncludeProgression:  # Can still be updated by another builder_fn
                        pass
                del builders[progression_key]
                if was_updated:
                    updated_progressions.add(progression)


def _create_progressions(replacer: Replacer,
                         builders: ProgressionBuilderDict,
                         tableUuid: dict[str, str],
                         updated_progressions: set[Progression]):
    """Create and build progressions for builders that did not match existing progressions."""
    for progression_key, builder_fns in builders.items():
        name, level, is_multiclass = progression_key

        if name in CharacterRace:
            progression_type_number = 2
        elif name in CharacterClass and name not in BASE_CHARACTER_CLASSES:
            progression_type_number = 1
        else:
            progression_type_number = 0

        progression = Progression(
            Name=name,
            Level=level,
            IsMulticlass=True if is_multiclass else None,
            ProgressionType=progression_type_number,
            TableUUID=tableUuid[name],
            UUID=replacer.make_uuid(f"Progression:{name}:{level}")
        )
        was_updated = False

        for builder_fn in builder_fns:
            if not getattr(builder_fn, "only_existing_progressions", False):
                try:
                    builder_fn(replacer, progression)
                    was_updated = True
                except DontIncludeProgression:  # Can still be updated by another builder_fn
                    pass

        if was_updated:
            updated_progressions.add(progression)


def _progression_builder(replacer: Replacer, progression_builders: list[ProgressionBuilder]) -> None:
    """Update and/or extend an existing character progression."""
    builders = _make_builders(progression_builders)
    tableUuid: dict[str, str] = dict()

    progressions = _load_progressions(replacer)
    updated_progressions: set[Progression] = set()

    _update_progressions(replacer, progressions, builders, tableUuid, updated_progressions)
    _create_progressions(replacer, builders, tableUuid, updated_progressions)

    # Save the new progression
    for progression in sorted(updated_progressions, key=_progression_order):
        replacer.mod.add(progression)


def progression(names: str | Iterable[str],
                levels: int | Iterable[int],
                *,
                is_multiclass: bool = False) -> ProgressionBuilder:
    """A decorator mapping class and level combinations to their progression builder function."""
    if isinstance(names, str) or not isinstance(names, Iterable):
        names = [names]
    if not isinstance(levels, Iterable):
        levels = [levels]

    def decorate(fn: ProgressionBuilder) -> ProgressionBuilder:
        setattr(fn, "builder", _progression_builder)
        multi_class_level_keys: list[MultiNameLevelKey] = getattr(fn, "progression", [])
        multi_class_level_keys.append((names, levels, is_multiclass))
        setattr(fn, "progression", multi_class_level_keys)
        return fn

    return decorate


def only_existing_progressions(fn: ProgressionBuilder) -> ProgressionBuilder:
    """A decorator used to indicate that new progressions should not be created for its builder."""
    setattr(fn, "only_existing_progressions", True)
    return fn
