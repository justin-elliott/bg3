#!/usr/bin/env python3
"""
Management of BG3 .pak files.
This makes use of LSLib: https://github.com/Norbyte/lslib
"""

import clr
import os
import re
import requests
import sys
import winreg

from collections.abc import Mapping
from pathlib import PurePath
from zipfile import ZipFile

EXPORT_TOOL_VERSION = "1.18.7"


class Unpak:
    """Management of BG3 .pak files."""

    _INSTALLDIR_REGEX = re.compile(R"""\s*"installdir"\s*"([^"]*)"\s*""")

    _cache_dir: os.PathLike
    _export_tool_dir: os.PathLike
    _unpak_dir: os.PathLike
    _cached_files: Mapping[tuple[str, str], os.PathLike]

    def __init__(self, cache_dir: os.PathLike | None = None):
        self._cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), ".cache")
        self._export_tool_dir = os.path.join(self._cache_dir, f"ExportTool-v{EXPORT_TOOL_VERSION}")
        self._unpak_dir = os.path.join(self._cache_dir, "unpak")
        self._cached_files = {}
        self._cache_export_tool()

    def get_path(self, pak_path: str) -> os.PathLike:
        """Retrieve the details for a .pak file, caching it if necessary."""
        pak_name, _, relative_path = str(PurePath(pak_path).as_posix()).partition("/")
        pak_name = pak_name[0:-4] if pak_name.endswith(".pak") else pak_name
        file_key = (pak_name, relative_path)
        if file_path := self._cached_files.get(file_key):
            return file_path

        file_path = self._cache_file(pak_name, relative_path)
        self._cached_files[file_key] = file_path
        return file_path

    def _cache_export_tool(self) -> None:
        """Download the LSLib export tool into the cache, if it is not already present."""
        os.makedirs(self._cache_dir, exist_ok=True)

        cache_export_tool_zip = self._export_tool_dir + ".zip"
        export_tool_zip = os.path.basename(cache_export_tool_zip)

        if not os.path.exists(cache_export_tool_zip):
            export_tool = requests.get(
                f"https://github.com/Norbyte/lslib/releases/download/v{EXPORT_TOOL_VERSION}/{export_tool_zip}",
                stream=True)
            with open(cache_export_tool_zip, "wb") as export_tool_zip_file:
                for chunk in export_tool.iter_content(chunk_size=4096):
                    export_tool_zip_file.write(chunk)

        if not os.path.exists(self._export_tool_dir):
            with ZipFile(cache_export_tool_zip, "r") as cache_export_tool_zip:
                cache_export_tool_zip.extractall(path=self._cache_dir)

    def _cache_file(self, pak_name: str, relative_path: str) -> os.PathLike:
        """Get the path of a pak directory in the cache, unpacking it if necessary."""
        cached_pak_dir = os.path.join(self._unpak_dir, pak_name)
        cached_file_path = os.path.join(cached_pak_dir, relative_path)
        pak_filename = os.path.join(self._get_bg3_data_dir(), f"{pak_name}.pak")

        # If there is a cached file, and it is still current, return its path
        pak_stat_result = os.stat(pak_filename)
        try:
            file_stat_result = os.stat(cached_file_path)
            if file_stat_result.st_mtime >= pak_stat_result.st_mtime:
                return cached_file_path
            os.remove(cached_file_path)  # The file is stale
        except FileNotFoundError:
            pass

        if not os.path.exists(cached_file_path):
            os.makedirs(self._unpak_dir, exist_ok=True)

            if self._export_tool_dir not in sys.path:
                sys.path.append(self._export_tool_dir)
            clr.AddReference("LSLib")
            from LSLib.LS import (
                AbstractFileInfo,
                Packager,
                ResourceConversionParameters,
                ResourceLoadParameters,
                ResourceUtils
            )
            from LSLib.LS.Enums import Game, ResourceFormat
            from System import Func

            # Filter for the file of interest
            filter_path = relative_path[0:-4] if relative_path.endswith(".lsf.lsx") else relative_path
            destination_path = os.path.join(cached_pak_dir, filter_path)

            def filter(file_info: AbstractFileInfo) -> bool:
                return file_info.Name == filter_path

            # Extract the file
            packager = Packager()
            packager.UncompressPackage(pak_filename, cached_pak_dir, Func[AbstractFileInfo, bool](filter))

            # Ensure that the file was extracted
            os.stat(destination_path)

            # Convert .lsf -> .lsf.lsx
            if destination_path.endswith(".lsf"):
                resource_utils = ResourceUtils()
                resource = resource_utils.LoadResource(destination_path,
                                                       ResourceFormat.LSF,
                                                       ResourceLoadParameters.FromGameVersion(Game.BaldursGate3))
                resource_utils.SaveResource(resource,
                                            cached_file_path,
                                            ResourceFormat.LSX,
                                            ResourceConversionParameters.FromGameVersion(Game.BaldursGate3))
                os.remove(destination_path)

        return cached_file_path

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
                if (match := self._INSTALLDIR_REGEX.match(line)):
                    return match[1]
        raise KeyError("Installdir not found in manifest")
