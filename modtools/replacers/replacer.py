#!/usr/bin/env python3
"""
A base class for character progression replacers.
"""

import os

from collections.abc import Callable
from modtools.mod import Mod
from typing import ClassVar
from uuid import UUID


class Replacer:
    """Base class for game content replacers."""

    _builders: ClassVar[dict[Callable, list[Callable]]]

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

    def __init__(self, base_dir: str, *, author: str, name: str, **kwds: str):
        self._mod = Mod(base_dir, author=author, name=name, **kwds)

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
