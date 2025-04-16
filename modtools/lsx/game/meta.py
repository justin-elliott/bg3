#!/usr/bin/env python3
"""
Meta definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class Dependencies(LsxNode):
    class ShortModuleDesc(LsxNode):
        Folder: str = LsxType.LSSTRING_VALUE
        MD5: str = LsxType.LSSTRING_VALUE
        Name: str = LsxType.LSSTRING_VALUE
        PublishHandle: int = LsxType.UINT64
        UUID: str = LsxType.FIXEDSTRING
        Version64: int = LsxType.INT64

        def __init__(self,
                     *,
                     Folder: str = None,
                     MD5: str = None,
                     Name: str = None,
                     PublishHandle: int = None,
                     UUID: str = None,
                     Version64: int = None):
            super().__init__(
                Folder=Folder,
                MD5=MD5,
                Name=Name,
                PublishHandle=PublishHandle,
                UUID=UUID,
                Version64=Version64,
            )

    children: LsxChildren = (ShortModuleDesc,)

    def __init__(self,
                 *,
                 children: LsxChildren = None):
        super().__init__(
            children=children,
        )


class ModuleInfo(LsxNode):
    class PublishVersion(LsxNode):
        Version64: int = LsxType.INT64

        def __init__(self,
                     *,
                     Version64: int = None):
            super().__init__(
                Version64=Version64,
            )

    class Scripts(LsxNode):
        pass

    class TargetModes(LsxNode):
        class Target(LsxNode):
            Object: str = LsxType.FIXEDSTRING

            def __init__(self,
                         *,
                         Object: str = None):
                super().__init__(
                    Object=Object,
                )

        children: LsxChildren = (Target,)

        def __init__(self,
                     *,
                     children: LsxChildren = None):
            super().__init__(
                children=children,
            )

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
    children: LsxChildren = (PublishVersion, Scripts, TargetModes)

    def __init__(self,
                 *,
                 Author: str = None,
                 CharacterCreationLevelName: str = None,
                 Description: str = None,
                 Folder: str = None,
                 LobbyLevelName: str = None,
                 MD5: str = None,
                 MainMenuBackgroundVideo: str = None,
                 MenuLevelName: str = None,
                 Name: str = None,
                 NumPlayers: int = None,
                 PhotoBooth: str = None,
                 StartupLevelName: str = None,
                 Tags: str = None,
                 Type: str = None,
                 UUID: str = None,
                 Version64: int = None,
                 children: LsxChildren = None):
        super().__init__(
            Author=Author,
            CharacterCreationLevelName=CharacterCreationLevelName,
            Description=Description,
            Folder=Folder,
            LobbyLevelName=LobbyLevelName,
            MD5=MD5,
            MainMenuBackgroundVideo=MainMenuBackgroundVideo,
            MenuLevelName=MenuLevelName,
            Name=Name,
            NumPlayers=NumPlayers,
            PhotoBooth=PhotoBooth,
            StartupLevelName=StartupLevelName,
            Tags=Tags,
            Type=Type,
            UUID=UUID,
            Version64=Version64,
            children=children,
        )


class Config(LsxDocument):
    path = "Mods/{folder}/meta.lsx"
    children: LsxChildren = (Dependencies, ModuleInfo)


Lsx.register(Config)
