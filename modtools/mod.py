#!/usr/bin/env python3
"""
The main mod definition for Baldur's Gate 3 mods.
"""

import hashlib
import os
import re
import shutil
import textwrap
import time

from modtools.gamedata import GameData, GameDataCollection
from modtools.unpak import Unpak
from modtools.localization import Localization
from modtools.lsx import Lsx
from modtools.lsx.game import Dependencies, ModuleInfo
from modtools.lsx.node import LsxNode
from modtools.prologue import LUA_PROLOGUE, TXT_PROLOGUE
from typing import Tuple
from uuid import UUID


class Mod:
    """Baldur's Gate 3 mod definition."""

    _author: str
    _base_dir: str
    _name: str
    _description: str
    _folder: str
    _uuid: UUID
    _version: Tuple[int, int, int, int]

    _unpak: Unpak

    _localization: Localization

    _game_data: GameDataCollection
    _lsx: Lsx

    _equipment: list[str]
    _scripts: list[str]
    _treasure_table: list[str]
    _xp_data: dict[int, int]

    def __init__(self,
                 base_dir: str,
                 *,
                 author: str,
                 name: str,
                 mod_uuid: UUID = None,
                 description: str = "",
                 folder: str = None,
                 version: Tuple[int, int, int, int] = (4, 1, 1, 1),
                 cache_dir: os.PathLike | None = None):
        """Define a mod.

        base_dir -- the base directory of the mod
        author -- the mod's author
        name -- the name of the mod (not localized)
        mod_uuid -- the UUID of the mod
        description -- an optional description for the mod (not localized)
        folder -- folder for the mod (defaults to the mod's name)
        version -- version of the mod (major, minor, revision, build)
        """
        self._author = author
        self._base_dir = base_dir
        self._name = name
        self._description = description
        self._folder = folder or name
        self._version = version

        if mod_uuid:
            self._uuid = mod_uuid
        else:
            m = hashlib.sha256()
            m.update(bytes(f"BG3:{author}:{name}", "UTF-8"))
            self._uuid = UUID(bytes=m.digest()[0:16])

        self._unpak = Unpak(cache_dir)

        self._localization = Localization(self._uuid)
        self._localization.add_language("en", "English")

        self._game_data = GameDataCollection()
        self._lsx = Lsx()

        self._equipment = None
        self._scripts = None
        self._treasure_table = None
        self._xp_data = None

    def make_uuid(self, key: str) -> UUID:
        m = hashlib.sha256()
        m.update(self._uuid.bytes)
        m.update(bytes(key, "UTF-8"))
        return UUID(bytes=m.digest()[0:16])

    def get_author(self) -> str:
        return self._author

    def get_base_dir(self) -> str:
        return self._base_dir

    def get_name(self) -> str:
        return self._name

    def get_prefix(self) -> str:
        """Get the module name with all non-alphanumeric, non-underscore characters removed."""
        return re.sub(r"\W+", "", self._name)

    def get_description(self) -> str:
        return self._description

    def get_folder(self) -> str:
        return self._folder

    def get_uuid(self) -> UUID:
        return self._uuid

    def get_version(self) -> tuple[int, int, int, int]:
        return self._version

    def get_localization(self) -> Localization:
        return self._localization

    def get_cache_path(self, lsx_path: os.PathLike) -> os.PathLike:
        """Get the path of a file in the unpak cache."""
        return self._unpak.get_path(lsx_path)

    def add(self, item: any) -> None:
        """Add a datum to the GameData collection."""
        if isinstance(item, GameData):
            self._game_data.add(item)
        elif isinstance(item, LsxNode):
            self._lsx.children.append(item)
        else:
            raise TypeError("add: Invalid data type")

    def add_equipment(self, text: str) -> None:
        self._equipment = self._equipment or []
        self._equipment.append(textwrap.dedent(text))

    def add_script(self, text: str) -> None:
        self._scripts = self._scripts or []
        text = textwrap.dedent(text)
        if text not in self._scripts:
            self._scripts.append(text)

    def add_treasure_table(self, text: str) -> None:
        self._treasure_table = self._treasure_table or []
        self._treasure_table.append(textwrap.dedent(text))

    def set_xp_data(self, xp_data: dict[int, int]) -> None:
        self._xp_data = xp_data

    def _add_meta(self) -> None:
        """Add the meta definition."""
        build_version = str(time.time_ns())

        self.add(Dependencies())
        self.add(ModuleInfo(
            Author=self._author,
            CharacterCreationLevelName="",
            Description=self._description,
            Folder=self._folder,
            LobbyLevelName="",
            MD5="",
            MainMenuBackgroundVideo="",
            MenuLevelName="",
            Name=self._name,
            NumPlayers="4",
            PhotoBooth="",
            StartupLevelName="",
            Tags="",
            Type="Add-on",
            UUID=self._uuid,
            Version64=build_version,
            children=[
                ModuleInfo.PublishVersion(
                    Version64=build_version,
                ),
                ModuleInfo.Scripts(),
                ModuleInfo.TargetModes(
                    children=[
                        ModuleInfo.TargetModes.Target(
                            Object="Story",
                        ),
                    ],
                ),
            ],
        ))

    def _build_equipment(self, public_dir: str) -> None:
        if self._equipment:
            equipment_dir = os.path.join(public_dir, "Stats", "Generated")
            os.makedirs(equipment_dir, exist_ok=True)
            with open(os.path.join(equipment_dir, "Equipment.txt"), "w") as f:
                f.write(TXT_PROLOGUE)
                f.write("\n".join(self._equipment))

    def _build_scripts(self, mod_dir: str) -> None:
        if self._scripts:
            scripts_dir = os.path.join(mod_dir, "Scripts", "thoth", "helpers")
            os.makedirs(scripts_dir, exist_ok=True)
            with open(os.path.join(scripts_dir, "Scripts.khn"), "w") as f:
                f.write(LUA_PROLOGUE)
                f.write("\n".join(self._scripts))

    def _build_treasure_table(self, public_dir: str) -> None:
        if self._treasure_table:
            treasure_table_dir = os.path.join(public_dir, "Stats", "Generated")
            os.makedirs(treasure_table_dir, exist_ok=True)
            with open(os.path.join(treasure_table_dir, "TreasureTable.txt"), "w") as f:
                f.write(TXT_PROLOGUE)
                f.write("\n".join(self._treasure_table))

    def _build_xp_data(self, public_dir: str) -> None:
        if self._xp_data:
            xp_data_dir = os.path.join(public_dir, "Stats", "Generated", "Data")
            os.makedirs(xp_data_dir, exist_ok=True)
            with open(os.path.join(xp_data_dir, "XPData.txt"), "w") as f:
                f.write(TXT_PROLOGUE)
                f.write("".join(f"""key "Level{level}","{xp}"\n\n""" for level, xp in self._xp_data.items()))
                f.write(f"""key "MaxXPLevel","{len(self._xp_data)}"\n""")

    def build(self) -> None:
        """Build the mod files underneath the _base_dir."""
        mod_dir = os.path.join(self._base_dir, self._folder)
        if os.path.exists(mod_dir):
            shutil.rmtree(mod_dir)
        os.makedirs(mod_dir, exist_ok=True)
        self._add_meta()
        self._game_data.build(mod_dir, self._folder)
        self._lsx.save(mod_dir, version=self._version, folder=self._folder)
        self._localization.build(mod_dir)
        public_dir = os.path.join(mod_dir, "Public", self._folder)
        self._build_equipment(public_dir)
        self._build_scripts(mod_dir)
        self._build_treasure_table(public_dir)
        self._build_xp_data(public_dir)
