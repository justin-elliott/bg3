#!/usr/bin/env python3
"""
A class representing a collection of GameData objects.
"""

import os

from collections.abc import Mapping
from modtools.gamedata_v2.gamedata import GameData
from modtools.prologue import TXT_PROLOGUE


class GameDataCollection:
    """A collection of GameData objects."""

    _game_data: list[GameData]

    def __init__(self):
        self._game_data = []

    def add(self, game_data: GameData) -> None:
        """Add GameData to the collection."""
        assert issubclass(game_data, GameData)
        self._game_data.append(game_data)

    def build(self, mod_dir: os.PathLike, folder: str) -> None:
        """Build the mod files corresponding to our game data."""
        file_data: Mapping[str, list[GameData]] = {}  # Filename -> [GameData]

        for game_data in self._game_data:
            file_data.setdefault(game_data.filename(), []).append(game_data)

        data_dir = os.path.join(mod_dir, "Public", folder, "Stats", "Generated", "Data")
        os.makedirs(data_dir, exist_ok=True)

        for filename, game_data in file_data.items():
            game_data.sort(key=lambda data: data.name)
            with open(os.path.join(data_dir, filename), "w") as f:
                f.write(TXT_PROLOGUE)
                f.write("\n".join(str(data) for data in game_data))
