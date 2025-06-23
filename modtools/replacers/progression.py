#!/usr/bin/env python3
"""
A decorator for class/race progression replacement.
"""

from collections.abc import Callable, Iterable
from enum import IntEnum
from modtools.lsx.game import BASE_CHARACTER_CLASSES, CharacterClass, CharacterRace
from modtools.lsx import Lsx
from modtools.lsx.game import Progression
from modtools.mod import Mod
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


_progression_lsx_paths = [
    "Shared.pak/Public/Shared/Progressions/Progressions.lsx",
    "Shared.pak/Public/SharedDev/Progressions/Progressions.lsx",
    "GustavX.pak/Public/GustavX/Progressions/Progressions.lsx",
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
]


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


def load_progressions(replacer_or_mod: Replacer | Mod) -> list[Progression]:
    """Load the game's Progressions from the .pak cache."""
    progressions_lsx = Lsx.load(replacer_or_mod.get_cache_path(_progression_lsx_paths[0]))
    for lsx_path in _progression_lsx_paths[1:]:
        lsx = Lsx.load(replacer_or_mod.get_cache_path(lsx_path))
        progressions_lsx.children.update(lsx.children, key=_by_uuid)
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
            was_updated = replacer.allow_improvement(progression)
            was_updated = replacer.adjust_resources(progression) or was_updated
            was_updated = replacer.adjust_skills(progression) or was_updated

            tableUuid[progression.Name] = progression.TableUUID
            progression_key = (progression.Name, progression.Level, progression.IsMulticlass or False)
            if builder_fns := builders.get(progression_key):
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
        was_updated = replacer.allow_improvement(progression)
        was_updated = replacer.adjust_resources(progression) or was_updated
        was_updated = replacer.adjust_skills(progression) or was_updated

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

    progressions = load_progressions(replacer)
    updated_progressions: set[Progression] = set()

    _update_progressions(replacer, progressions, builders, tableUuid, updated_progressions)
    _create_progressions(replacer, builders, tableUuid, updated_progressions)

    # Save the new progression
    for progression in sorted(updated_progressions, key=_progression_order):
        replacer.mod.add(progression)


class ProgressionDecorator:
    @staticmethod
    def __call__(names: str | Iterable[str],
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

    @staticmethod
    def include(pak_path: str) -> None:
        _progression_lsx_paths.append(pak_path)


progression = ProgressionDecorator()


def only_existing_progressions(fn: ProgressionBuilder) -> ProgressionBuilder:
    """A decorator used to indicate that new progressions should not be created for its builder."""
    setattr(fn, "only_existing_progressions", True)
    return fn
