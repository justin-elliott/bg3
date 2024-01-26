#!/usr/bin/env python3
"""
Meta definitions.
"""

from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class Dependencies(LsxNode):
    pass


class ModuleInfo(LsxNode):
    class PublishVersion(LsxNode):
        Version64: int = LsxType.INT64

    class Scripts(LsxNode):
        pass

    class TargetModes(LsxNode):
        class Target(LsxNode):
            Object: str = LsxType.FIXEDSTRING

        children = (Target,)

    Author: str = LsxType.LSSTRING_VALUE
    CharacterCreationLevelName: str = LsxType.FIXEDSTRING
    Description: str = LsxType.LSSTRING_VALUE
    Folder: str = LsxType.LSSTRING_VALUE
    LobbyLevelName: str = LsxType.FIXEDSTRING
    MD5: str = LsxType.LSSTRING_VALUE
    MainMenuBackgroundVideo: str = LsxType.FIXEDSTRING
    MenuLevelName: str = LsxType.FIXEDSTRING
    Name: str = LsxType.LSSTRING_VALUE
    NumPlayers: int = LsxType.UINT8
    PhotoBooth: str = LsxType.FIXEDSTRING
    StartupLevelName: str = LsxType.FIXEDSTRING
    Tags: str = LsxType.LSSTRING_VALUE
    Type: str = LsxType.FIXEDSTRING
    UUID: str = LsxType.FIXEDSTRING
    Version64: int = LsxType.INT64
    children = (PublishVersion, Scripts, TargetModes)


class Config(LsxDocument):
    path = "Mods/{folder}/meta.lsx"
    children = (Dependencies, ModuleInfo)


Lsx.register(Config)
