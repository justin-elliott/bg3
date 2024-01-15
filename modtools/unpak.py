#!/usr/bin/env python3
"""
Management of BG3 .pak files.
This makes use of LSLib: https://github.com/Norbyte/lslib
"""

import clr
import hashlib
import os
import re
import requests
import shutil
import sys
import winreg

from collections.abc import Mapping
from dataclasses import dataclass
from zipfile import ZipFile

EXPORT_TOOL_VERSION = "1.18.7"


class Unpak:
    """Management of BG3 .pak files."""

    @dataclass
    class CachedPak:
        """Description of a cached, unpacked .pak file."""
        path: os.PathLike  # Path to the cached .pak directory
        hash: str          # SHA256 hex digest

    __installdir_regex = re.compile(R"""\s*"installdir"\s*"([^"]*)"\s*""")

    __cache_dir: os.PathLike
    __export_tool_dir: os.PathLike
    __unpak_dir: os.PathLike
    __cached_paks: Mapping[str, CachedPak]

    def __init__(self, cache_dir: os.PathLike | None):
        self.__cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), ".cache")
        self.__export_tool_dir = os.path.join(self.__cache_dir, f"ExportTool-v{EXPORT_TOOL_VERSION}")
        self.__unpak_dir = os.path.join(self.__cache_dir, "unpak")
        self.__cached_paks = {}
        self._cache_export_tool()

    def get(self, pak_name: str) -> CachedPak:
        """Retrieve the details for a .pak file, caching it if necessary."""
        pak_name = pak_name[0:-4] if pak_name.endswith(".pak") else pak_name
        if pak_name not in self.__cached_paks:
            cached_pak = self._get_cached_pak_dir(pak_name)
            self.__cached_paks[pak_name] = cached_pak
        return self.__cached_paks[pak_name]

    def _cache_export_tool(self) -> None:
        """Download the LSLib export tool into the cache, if it is not already present."""
        os.makedirs(self.__cache_dir, exist_ok=True)

        cache_export_tool_zip = self.__export_tool_dir + ".zip"
        export_tool_zip = os.path.basename(cache_export_tool_zip)

        if not os.path.exists(cache_export_tool_zip):
            export_tool = requests.get(
                f"https://github.com/Norbyte/lslib/releases/download/v{EXPORT_TOOL_VERSION}/{export_tool_zip}",
                stream=True)
            with open(cache_export_tool_zip, "wb") as export_tool_zip_file:
                for chunk in export_tool.iter_content(chunk_size=4096):
                    export_tool_zip_file.write(chunk)

        if not os.path.exists(self.__export_tool_dir):
            with ZipFile(cache_export_tool_zip, "r") as cache_export_tool_zip:
                cache_export_tool_zip.extractall(path=self.__cache_dir)

    def _get_cached_pak_dir(self, pak_name: str) -> CachedPak:
        """Get the path of a pak directory in the cache, unpacking it if necessary."""
        cached_pak_dir = os.path.join(self.__unpak_dir, pak_name)
        hash_filename = os.path.join(cached_pak_dir, ".sha256")
        pak_filename = os.path.join(self._get_bg3_data_dir(), f"{pak_name}.pak")
        hash = None

        if os.path.exists(cached_pak_dir):
            with open(pak_filename, "rb") as pak_file, open(hash_filename, "r") as hash_file:
                digest = hashlib.file_digest(pak_file, "sha256")
                hash = hash_file.read()
                if digest.hexdigest() != hash:
                    shutil.rmtree(cached_pak_dir)

        if not os.path.exists(cached_pak_dir):
            os.makedirs(self.__unpak_dir, exist_ok=True)

            if self.__export_tool_dir not in sys.path:
                sys.path.append(self.__export_tool_dir)
            clr.AddReference("LSLib")
            from LSLib.LS import Packager

            packager = Packager()
            packager.UncompressPackage(pak_filename, cached_pak_dir)
            with open(pak_filename, "rb") as pak_file, open(hash_filename, "w") as hash_file:
                hash = hashlib.file_digest(pak_file, "sha256").hexdigest()
                hash_file.write(hash)

        return Unpak.CachedPak(cached_pak_dir, hash)

    def _get_bg3_data_dir(self) -> os.PathLike:
        """Get the BG3 data directory."""
        try:
            hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, R"SOFTWARE\WOW6432Node\Valve\Steam")
            steam_install_path, _ = winreg.QueryValueEx(hkey, "InstallPath")
            steamapps_path = os.path.join(steam_install_path, "steamapps")
            manifest_path = self._get_bg3_dir_from_manifest(steamapps_path)
            if os.path.isabs(manifest_path):
                return os.path.join(manifest_path, "Data")
            return os.path.join(steamapps_path, "common", manifest_path, "Data")
        except (KeyError, OSError) as e:
            print(f"Unable to lookup the BG3 Data directory; falling back on default.\n{e}")
            return R"C:\Program Files (x86)\Steam\steamapps\common\Baldurs Gate 3\Data"

    def _get_bg3_dir_from_manifest(self, steamapps_path: os.PathLike) -> os.PathLike:
        """Given the steamapps_path, parse the BG3 manifest, and determine the game's install location."""
        with open(os.path.join(steamapps_path, "appmanifest_1086940.acf"), "r") as manifest_file:
            for line in manifest_file:
                if (match := self.__installdir_regex.match(line)):
                    return match[1]
        raise KeyError("Installdir not found in manifest")
