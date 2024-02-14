#!/usr/bin/env python3
"""
A decorator for origin replacement.
"""

from collections.abc import Callable
from modtools.lsx import Lsx
from modtools.lsx.game import Origin
from modtools.replacers.replacer import Replacer
from uuid import UUID


type OriginBuilder = Callable[[Replacer, Origin], None]
type OriginBuilderDict = dict[str, OriginBuilder]


_ORIGINS_LSX_PATH = "Gustav.pak/Public/Gustav/Origins/Origins.lsx"
_ORIGINS_DEV_LSX_PATH = "Gustav.pak/Public/GustavDev/Origins/Origins.lsx"


def _by_name(origin: Origin) -> str:
    return origin.Name


def _by_uuid(origin: Origin) -> UUID:
    return origin.UUID


def _load_origins(replacer: Replacer) -> list[Origin]:
    """Load the game's Origins from the .pak cache."""
    origins_lsx = Lsx.load(replacer.get_cache_path(_ORIGINS_LSX_PATH))
    origins_dev_lsx = Lsx.load(replacer.get_cache_path(_ORIGINS_DEV_LSX_PATH))
    origins_lsx.children.update(origins_dev_lsx.children, key=_by_uuid)
    origins_lsx.children.sort(key=_by_name)
    return list(origins_lsx.children)


def _make_builders(origin_builders: list[OriginBuilder]) -> OriginBuilderDict:
    """Make a OriginBuilderDict from the decorated origin builders."""
    builders: OriginBuilderDict = dict()

    for origin_builder in origin_builders:
        names = getattr(origin_builder, "origins")
        for name in names:
            builders[name] = origin_builder

    return builders


def _update_origins(replacer: Replacer,
                    origins: list[Origin],
                    builders: OriginBuilderDict,
                    updated_origins: set[Origin]):
    """Update origins that match our builder names."""
    for origin in origins:
        if builder_fn := builders.get(origin.Name):
            builder_fn(replacer, origin)
            updated_origins.add(origin)


def _origin_builder(replacer: Replacer, origin_builders: list[OriginBuilder]) -> None:
    """Update existing origins."""
    builders = _make_builders(origin_builders)

    origins = _load_origins(replacer)
    updated_origins: set[Origin] = set()

    _update_origins(replacer, origins, builders, updated_origins)

    # Save the updated origins
    for origin in sorted(updated_origins, key=_by_name):
        replacer.mod.add(origin)


def origin(name: str) -> OriginBuilder:
    """A decorator mapping a named origin to its builder function."""
    def decorate(fn: OriginBuilder) -> OriginBuilder:
        setattr(fn, "builder", _origin_builder)
        origins: list[str] = getattr(fn, "origins", [])
        origins.append(name)
        setattr(fn, "origins", origins)
        return fn

    return decorate
