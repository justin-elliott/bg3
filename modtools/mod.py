#!/usr/bin/env python3
"""
The main mod definition for Baldur's Gate 3 mods.
"""

import os

from .localization import Localization
from .lsx import Lsx
from .modifiers import Modifiers
from uuid import UUID


class Mod:
    """Baldur's Gate 3 mod definition."""

    __author: str
    __base_dir: str
    __name: str
    __description: str
    __folder: str
    __uuid: UUID
    __version: (int, int, int, int)

    __modifiers: Modifiers
    __localization: Localization

    def __init__(self, base_dir: str, author: str, name: str, mod_uuid: UUID, description: str = "", folder: str = None,
                 version: (int, int, int, int) = (4, 0, 0, 1)):
        """Define a mod.

        base_dir -- the base directory of the mod
        author -- the mod's author
        name -- the name of the mod (not localized)
        mod_uuid -- the UUID of the mod
        description -- an optional description for the mod (not localized)
        folder -- folder for the mod (defaults to the mod's name)
        version -- version of the mod (major, minor, revision, build)
        """
        self.__author = author
        self.__base_dir = base_dir
        self.__name = name
        self.__description = description
        self.__folder = folder or name
        self.__uuid = mod_uuid
        self.__version = version
        self.__modifiers = Modifiers(self)
        self.__localization = Localization(mod_uuid)

    def get_author(self) -> str:
        return self.__author

    def get_base_dir(self) -> str:
        return self.__base_dir

    def get_name(self) -> str:
        return self.__name

    def get_description(self) -> str:
        return self.__description

    def get_folder(self) -> str:
        return self.__folder

    def get_uuid(self) -> UUID:
        return self.__uuid

    def get_version(self) -> (int, int, int, int):
        return self.__version

    def get_modifiers(self) -> Modifiers:
        return self.__modifiers

    def get_localization(self) -> Localization:
        return self.__localization

    def _build_meta(self, mod_dir: str):
        """Build the meta.lsx underneath the given mod_dir."""
        major, minor, revision, build = self.__version
        version_str = str((((major * 100) + minor) * 100 + revision) * 10_000 + build)

        lsx = Lsx(self.__version, "Config", "root")
        lsx.add_children([
            Lsx.Node("Dependencies"),
            Lsx.Node("ModuleInfo", attributes=[
                    Lsx.Attribute("Author", "LSWString", value=self.__author),
                    Lsx.Attribute("CharacterCreationLevelName", "FixedString", value=""),
                    Lsx.Attribute("Description", "LSWString", value=self.__description),
                    Lsx.Attribute("Folder", "LSWString", value=self.__folder),
                    Lsx.Attribute("LobbyLevelName", "FixedString", value=""),
                    Lsx.Attribute("MD5", "LSString", value=""),
                    Lsx.Attribute("MainMenuBackgroundVideo", "FixedString", value=""),
                    Lsx.Attribute("MenuLevelName", "FixedString", value=""),
                    Lsx.Attribute("Name", "FixedString", value=self.__name),
                    Lsx.Attribute("NumPlayers", "uint8", value="4"),
                    Lsx.Attribute("PhotoBooth", "FixedString", value=""),
                    Lsx.Attribute("StartupLevelName", "FixedString", value=""),
                    Lsx.Attribute("Tags", "LSString", value=""),
                    Lsx.Attribute("Type", "FixedString", value="Add-on"),
                    Lsx.Attribute("UUID", "FixedString", value=str(self.__uuid)),
                    Lsx.Attribute("Version", "int64", value=version_str),
                ],
                children=[
                    Lsx.Node("PublishVersion", [
                        Lsx.Attribute("Version", "int64", value=version_str)
                    ]),
                    Lsx.Node("Scripts"),
                    Lsx.Node("TargetModes", children=[
                        Lsx.Node("Target", [
                            Lsx.Attribute("Object", "FixedString", value="Story")
                        ])
                    ]),
                ])
        ])
        lsx.build(os.path.join(mod_dir, "Mods", self.__folder, "meta.lsx"))

    def build(self):
        """Build the mod files underneath the __base_dir."""
        mod_dir = os.path.join(self.__base_dir, self.__folder)
        os.makedirs(mod_dir, exist_ok=True)
        self._build_meta(mod_dir)
        self.__modifiers.build(mod_dir, self.__folder)
        self.__localization.build(mod_dir)
