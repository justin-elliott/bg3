#!/usr/bin/env python3
"""
Text-based Baldur's Gate 3 mod files.
"""

import os

from abc import ABC, abstractmethod
from modtools.prologue import LUA_PROLOGUE, TXT_PROLOGUE
from textwrap import dedent


class Text(ABC):
    text: str

    def __init__(self, text: str):
        self.text = dedent(text).strip()

    @property
    @abstractmethod
    def path(self) -> str:
        """The path to the file that should contain this text."""
        pass

    @property
    def prologue(self) -> str:
        return TXT_PROLOGUE


class TextCollection:
    _entries: list[Text]

    def __init__(self):
        self._entries = []

    def add(self, entry: Text) -> None:
        assert isinstance(entry, Text), f"{type(entry).__name__} is not a subclass of Text"
        self._entries.append(entry)

    def save(self, mod_path: os.PathLike, **kwds: str) -> None:
        """Save each entry to the appropriate file."""
        file_mappings: dict[str, list[Text]] = {}

        for entry in self._entries:
            path = os.path.join(mod_path, entry.path.format(**kwds))
            file_mappings.setdefault(path, []).append(entry)

        for filename, entries in file_mappings.items():
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(entries[0].prologue)
                f.write("\n\n".join(entry.text for entry in entries))
                f.write("\n")


class Equipment(Text):
    @property
    def path(self) -> str:
        return "Public/{folder}/Stats/Generated/Equipment.txt"


class Script(Text):
    @property
    def path(self) -> str:
        return "Scripts/thoth/helpers/Scripts.khn"

    @property
    def prologue(self) -> str:
        return LUA_PROLOGUE


class TreasureTable(Text):
    @property
    def path(self) -> str:
        return "Public/{folder}/Stats/Generated/TreasureTable.txt"


class XPData(Text):
    def __init__(self, xp_data: dict[int, int]):
        text = ("".join(f"""key "Level{level}","{xp}"\n\n""" for level, xp in xp_data.items())
                + f"""key "MaxXPLevel","{len(xp_data)}"\n""")
        super.__init__(text)

    @property
    def path(self) -> str:
        return "Public/{folder}/Stats/Generated/Data/XPData.txt"
