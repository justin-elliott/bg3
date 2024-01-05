#!/usr/bin/env python3
"""
The main mod definition for Baldur's Gate 3 mods.
"""

import hashlib
import os
import shutil
import time

from .entity import Entities, Entity
from .gamedata import GameData
from .localization import Localization
from .lsx import Lsx
from .modifiers import Modifiers
from .prologue import TXT_PROLOGUE
from .valuelists import ValueLists
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

    __gamedata: GameData
    __modifiers: Modifiers
    __valuelists: ValueLists

    __localization: Localization

    __entities: Entities

    __character_creation_presets: Lsx
    __feat_descriptions: Lsx
    __feats: Lsx
    __level_maps: Lsx
    __passive_lists: Lsx
    __progressions: Lsx
    __progression_descriptions: Lsx
    __races: Lsx
    __root_templates: Lsx
    __spell_lists: Lsx
    __tags: Lsx

    __treasure_table: [str]

    def __init__(self, base_dir: str, author: str, name: str, mod_uuid: UUID, description: str = "", folder: str = None,
                 version: (int, int, int, int) = (4, 1, 1, 1), cache_dir: os.PathLike | None = None):
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

        self.__gamedata = GameData(cache_dir)
        self.__modifiers = Modifiers(self.__gamedata)
        self.__valuelists = ValueLists(self.__gamedata)

        self.__localization = Localization(mod_uuid)

        self.__entities = Entities(self.__modifiers, self.__valuelists)

        self.__character_creation_presets = None
        self.__feat_descriptions = None
        self.__feats = None
        self.__level_maps = None
        self.__passive_lists = None
        self.__progressions = None
        self.__progression_descriptions = None
        self.__races = None
        self.__root_templates = None
        self.__spell_lists = None
        self.__tags = None

        self.__treasure_table = None

    def make_uuid(self, key: str) -> UUID:
        m = hashlib.sha256()
        m.update(self.__uuid.bytes)
        m.update(bytes(key, "UTF-8"))
        return UUID(m.hexdigest()[0:32])

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

    def add(self, data: any) -> None:
        """Add an entity to the Entities collection."""
        if isinstance(data, Entity):
            self.__entities.add(data)
        else:
            raise TypeError("add: Invalid data type")

    def add_character_creation_presets(self, nodes: [Lsx.Node]) -> None:
        if not self.__character_creation_presets:
            self.__character_creation_presets = Lsx(self.__version, "CharacterCreationPresets", "root")
        self.__character_creation_presets.add_children(nodes)

    def add_feat_descriptions(self, nodes: [Lsx.Node]) -> None:
        if not self.__feat_descriptions:
            self.__feat_descriptions = Lsx(self.__version, "FeatDescriptions", "root")
        self.__feat_descriptions.add_children(nodes)

    def add_feats(self, nodes: [Lsx.Node]) -> None:
        if not self.__feats:
            self.__feats = Lsx(self.__version, "Feats", "root")
        self.__feats.add_children(nodes)

    def add_level_maps(self, nodes: [Lsx.Node]) -> None:
        if not self.__level_maps:
            self.__level_maps = Lsx(self.__version, "LevelMapValues", "root")
        self.__level_maps.add_children(nodes)

    def add_passive_lists(self, nodes: [Lsx.Node]) -> None:
        if not self.__passive_lists:
            self.__passive_lists = Lsx(self.__version, "PassiveLists", "root")
        self.__passive_lists.add_children(nodes)

    def add_progressions(self, nodes: [Lsx.Node]) -> None:
        if not self.__progressions:
            self.__progressions = Lsx(self.__version, "Progressions", "root")
        self.__progressions.add_children(nodes)

    def add_progression_descriptions(self, nodes: [Lsx.Node]) -> None:
        if not self.__progression_descriptions:
            self.__progression_descriptions = Lsx(self.__version, "ProgressionDescriptions", "root")
        self.__progression_descriptions.add_children(nodes)

    def add_races(self, nodes: [Lsx.Node]) -> None:
        if not self.__races:
            self.__races = Lsx(self.__version, "Races", "root")
        self.__races.add_children(nodes)

    def add_root_templates(self, nodes: [Lsx.Node]) -> None:
        if not self.__root_templates:
            self.__root_templates = Lsx(self.__version, "Templates", "Templates")
        self.__root_templates.add_children(nodes)

    def add_spell_lists(self, nodes: [Lsx.Node]) -> None:
        if not self.__spell_lists:
            self.__spell_lists = Lsx(self.__version, "SpellLists", "root")
        self.__spell_lists.add_children(nodes)

    def add_tags(self, nodes: [Lsx.Node]) -> None:
        if not self.__tags:
            self.__tags = []
        self.__tags.extend(nodes)

    def add_treasure_table(self, text: str) -> None:
        self.__treasure_table = self.__treasure_table or []
        self.__treasure_table.append(text)

    def _build_meta(self, mod_dir: str) -> None:
        """Build the meta.lsx underneath the given mod_dir."""
        build_version = str(time.time_ns())

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
                    Lsx.Attribute("Version64", "int64", value=build_version),
                ],
                children=[
                    Lsx.Node("PublishVersion", [
                        Lsx.Attribute("Version64", "int64", value=build_version)
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

    def _build_character_creation_presets(self, public_dir: str) -> None:
        if self.__character_creation_presets:
            self.__character_creation_presets.build(os.path.join(public_dir, "CharacterCreationPresets",
                                                                 "CharacterCreationPresets.lsx"))

    def _build_feat_descriptions(self, public_dir: str) -> None:
        if self.__feat_descriptions:
            self.__feat_descriptions.build(os.path.join(public_dir, "Feats", "FeatDescriptions.lsx"))

    def _build_feats(self, public_dir: str) -> None:
        if self.__feats:
            self.__feats.build(os.path.join(public_dir, "Feats", "Feats.lsx"))

    def _build_level_maps(self, public_dir: str) -> None:
        if self.__level_maps:
            self.__level_maps.build(os.path.join(public_dir, "Levelmaps", "LevelMapValues.lsx"))

    def _build_progressions(self, public_dir: str) -> None:
        if self.__progressions:
            self.__progressions.build(os.path.join(public_dir, "Progressions", "Progressions.lsx"))

    def _build_passive_lists(self, public_dir: str) -> None:
        if self.__passive_lists:
            self.__passive_lists.build(os.path.join(public_dir, "Lists", "PassiveLists.lsx"))

    def _build_progression_descriptions(self, public_dir: str) -> None:
        if self.__progression_descriptions:
            self.__progression_descriptions.build(
                os.path.join(public_dir, "Progressions", "ProgressionDescriptions.lsx"))

    def _build_races(self, public_dir: str) -> None:
        if self.__races:
            self.__races.build(os.path.join(public_dir, "Races", "Races.lsx"))

    def _build_root_templates(self, public_dir: str) -> None:
        if self.__root_templates:
            self.__root_templates.build(os.path.join(public_dir, "RootTemplates", "_merged.lsx"))

    def _build_spell_lists(self, public_dir: str) -> None:
        if self.__spell_lists:
            self.__spell_lists.build(os.path.join(public_dir, "Lists", "SpellLists.lsx"))

    def _build_tags(self, public_dir: str) -> None:
        if self.__tags:
            for tag in self.__tags:
                lsx = Lsx(self.__version, "Tags")
                lsx.set_root(tag)
                tag_uuid = next(attr.get_value() for attr in tag.get_attributes() if attr.get_id() == "UUID")
                tag_file = f"{tag_uuid}.lsx"
                lsx.build(os.path.join(public_dir, "Tags", tag_file))

    def _build_treasure_table(self, public_dir: str) -> None:
        if self.__treasure_table:
            treasure_table_dir = os.path.join(public_dir, "Stats", "Generated")
            os.makedirs(treasure_table_dir, exist_ok=True)
            with open(os.path.join(treasure_table_dir, "TreasureTable.txt"), "w") as f:
                f.write(TXT_PROLOGUE)
                f.write("\n".join(self.__treasure_table))

    def build(self) -> None:
        """Build the mod files underneath the __base_dir."""
        mod_dir = os.path.join(self.__base_dir, self.__folder)
        if os.path.exists(mod_dir):
            shutil.rmtree(mod_dir)
        os.makedirs(mod_dir, exist_ok=True)
        self._build_meta(mod_dir)
        self.__entities.build(mod_dir, self.__folder)
        self.__localization.build(mod_dir)
        public_dir = os.path.join(mod_dir, "Public", self.__folder)
        self._build_character_creation_presets(public_dir)
        self._build_feat_descriptions(public_dir)
        self._build_feats(public_dir)
        self._build_level_maps(public_dir)
        self._build_passive_lists(public_dir)
        self._build_progressions(public_dir)
        self._build_progression_descriptions(public_dir)
        self._build_races(public_dir)
        self._build_root_templates(public_dir)
        self._build_spell_lists(public_dir)
        self._build_tags(public_dir)
        self._build_treasure_table(public_dir)
