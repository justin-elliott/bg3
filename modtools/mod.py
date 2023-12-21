#!/usr/bin/env python3
"""
The main mod definition for Baldur's Gate 3 mods.
"""

import os

import xml.etree.ElementTree as ElementTree

from .localization import Localization
from .modifiers import Modifiers
from .prologue import XML_PROLOGUE
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

    localization: Localization

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
        self.localization = Localization(mod_uuid)

    def _build_meta(self, mod_dir):
        """Build the meta.lsx underneath the given mod_dir."""
        major, minor, revision, build = self.__version
        version = (((major * 100) + minor) * 100 + revision) * 10_000 + build
        xml_element = ElementTree.fromstring(f"""
            <save>
                <version major="{major}" minor="{minor}" revision="{revision}" build="{build}"/>
                <region id="Config">
                    <node id="root">
                        <children>
                            <node id="Dependencies"/>
                            <node id="ModuleInfo">
                                <attribute id="Author" type="LSWString" value="{self.__author}"/>
                                <attribute id="CharacterCreationLevelName" type="FixedString" value=""/>
                                <attribute id="Description" type="LSWString" value="{self.__description}"/>
                                <attribute id="Folder" type="LSWString" value="{self.__folder}"/>
                                <attribute id="LobbyLevelName" type="FixedString" value=""/>
                                <attribute id="MD5" type="LSString" value=""/>
                                <attribute id="MainMenuBackgroundVideo" type="FixedString" value=""/>
                                <attribute id="MenuLevelName" type="FixedString" value=""/>
                                <attribute id="Name" type="FixedString" value="{self.__name}"/>
                                <attribute id="NumPlayers" type="uint8" value="4"/>
                                <attribute id="PhotoBooth" type="FixedString" value=""/>
                                <attribute id="StartupLevelName" type="FixedString" value=""/>
                                <attribute id="Tags" type="LSString" value=""/>
                                <attribute id="Type" type="FixedString" value="Add-on"/>
                                <attribute id="UUID" type="FixedString" value="{self.__uuid}"/>
                                <attribute id="Version" type="int64" value="{version}"/>
                                <children>
                                    <node id="PublishVersion">
                                        <attribute id="Version" type="int64" value="{version}"/>
                                    </node>
                                    <node id="Scripts"/>
                                    <node id="TargetModes">
                                        <children>
                                            <node id="Target">
                                                <attribute id="Object" type="FixedString" value="Story"/>
                                            </node>
                                        </children>
                                    </node>
                                </children>
                            </node>
                        </children>
                    </node>
                </region>
            </save>
            """)
        meta_dir = os.path.join(mod_dir, "Mods", self.__folder)
        os.makedirs(meta_dir, exist_ok=True)
        with open(os.path.join(meta_dir, "meta.lsx"), "wb") as f:
            f.write(XML_PROLOGUE)
            xml_document = ElementTree.ElementTree(xml_element)
            ElementTree.indent(xml_document, space=" "*4)
            xml_document.write(f, encoding="UTF-8", xml_declaration=False)

    def build(self):
        """Build the mod files underneath the __base_dir."""
        mod_dir = os.path.join(self.__base_dir, self.__folder)
        os.makedirs(mod_dir, exist_ok=True)
        self._build_meta(mod_dir)
        self.__modifiers.build(mod_dir, self.__folder)
        self.localization.build(mod_dir)
