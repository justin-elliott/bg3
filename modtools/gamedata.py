#!/usr/bin/env python3
"""
Management of BG3 game data files.
This makes use of LSLib: https://github.com/Norbyte/lslib
"""

import clr
import hashlib
import os
import requests
import shutil
import sys

from zipfile import ZipFile

EXPORT_TOOL_VERSION = "1.18.7"
BG3_DATA_DIR = R"C:\Program Files (x86)\Steam\steamapps\common\Baldurs Gate 3\Data"


class GameData:
    """Management of game data files."""

    cache_dir = os.path.join(os.path.dirname(__file__), ".cache")
    export_tool_dir = os.path.join(cache_dir, f"ExportTool-v{EXPORT_TOOL_VERSION}")
    gamedata_dir = os.path.join(cache_dir, "gamedata")

    @staticmethod
    def get_file_path(pak_name: str, relative_path: str) -> str:
        """Get the path of the named file, unpacking the .pak file into the cache if necessary.

        pak_name -- The name of the .pak file, without its extension.
        relative_path -- The path of the file within the .pak.
        """
        cached_pak_dir = GameData._get_cached_pak_dir(pak_name)
        return os.path.join(cached_pak_dir, relative_path)

    @staticmethod
    def _cache_export_tool() -> None:
        """Download the LSLib export tool into the cache, if it is not already present."""
        os.makedirs(GameData.cache_dir, exist_ok=True)

        cache_export_tool_zip = GameData.export_tool_dir + ".zip"
        export_tool_zip = os.path.basename(cache_export_tool_zip)

        if not os.path.exists(cache_export_tool_zip):
            export_tool = requests.get(
                f"https://github.com/Norbyte/lslib/releases/download/v{EXPORT_TOOL_VERSION}/{export_tool_zip}",
                stream=True)
            with open(cache_export_tool_zip, "wb") as export_tool_zip_file:
                for chunk in export_tool.iter_content(chunk_size=4096):
                    export_tool_zip_file.write(chunk)

        if not os.path.exists(GameData.export_tool_dir):
            with ZipFile(cache_export_tool_zip, "r") as cache_export_tool_zip:
                cache_export_tool_zip.extractall(path=GameData.cache_dir)

    @staticmethod
    def _get_cached_pak_dir(pak_name: str) -> str:
        """Get the path of a pak directory in the cache, unpacking it if necessary."""

        cached_pak_dir = os.path.join(GameData.gamedata_dir, pak_name)
        pak_filename = os.path.join(BG3_DATA_DIR, f"{pak_name}.pak")

        if os.path.exists(cached_pak_dir):
            with open(pak_filename, "rb") as pak_file, open(os.path.join(cached_pak_dir, ".sha256"), "r") as hash_file:
                digest = hashlib.file_digest(pak_file, "sha256")
                cached_hexdigest = hash_file.read()
                if digest.hexdigest() != cached_hexdigest:
                    shutil.rmtree(cached_pak_dir)

        if not os.path.exists(cached_pak_dir):
            os.makedirs(GameData.gamedata_dir, exist_ok=True)

            if GameData.export_tool_dir not in sys.path:
                sys.path.append(GameData.export_tool_dir)
            clr.AddReference("LSLib")
            from LSLib.LS import Packager

            packager = Packager()
            packager.UncompressPackage(pak_filename, cached_pak_dir)
            with open(pak_filename, "rb") as pak_file, open(os.path.join(cached_pak_dir, ".sha256"), "w") as hash_file:
                digest = hashlib.file_digest(pak_file, "sha256")
                hash_file.write(digest.hexdigest())

        return cached_pak_dir


GameData._cache_export_tool()
