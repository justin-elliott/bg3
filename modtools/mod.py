#!/usr/bin/env python3
"""
The main mod definition for Baldur's Gate 3 mods.
"""

import hashlib
import os
import re
import shutil
import time

from modtools.gamedata import GameData, GameDatum
from modtools.unpak import Unpak
from modtools.localization import Localization
from modtools.lsx_v1 import Lsx
from modtools.lsx.types import LsxCollection, Node
from modtools.modifiers import Modifiers
from modtools.prologue import LUA_PROLOGUE, TXT_PROLOGUE
from modtools.valuelists import ValueLists
from uuid import UUID


class Mod:
    """Baldur's Gate 3 mod definition."""

    _author: str
    _base_dir: str
    _name: str
    _description: str
    _folder: str
    _uuid: UUID
    _version: (int, int, int, int)

    _unpak: Unpak
    _modifiers: Modifiers
    _valuelists: ValueLists

    _localization: Localization

    _gamedata: GameData
    _lsx_collection: LsxCollection

    _character_creation_presets: Lsx
    _class_descriptions: Lsx
    _feat_descriptions: Lsx
    _feats: Lsx
    _level_maps: Lsx
    _passive_lists: Lsx
    _progressions: Lsx
    _progression_descriptions: Lsx
    _races: Lsx
    _root_templates: Lsx
    _spell_lists: Lsx
    _tags: Lsx

    _scripts: [str]
    _treasure_table: [str]

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
        self._author = author
        self._base_dir = base_dir
        self._name = name
        self._description = description
        self._folder = folder or name
        self._uuid = mod_uuid
        self._version = version

        self._unpak = Unpak(cache_dir)
        self._modifiers = Modifiers(self._unpak)
        self._valuelists = ValueLists(self._unpak)

        self._localization = Localization(mod_uuid)
        self._localization.add_language("en", "English")

        self._gamedata = GameData(self._modifiers, self._valuelists)
        self._lsx_collection = LsxCollection()

        self._character_creation_presets = None
        self._class_descriptions = None
        self._feat_descriptions = None
        self._feats = None
        self._level_maps = None
        self._passive_lists = None
        self._progressions = None
        self._progression_descriptions = None
        self._races = None
        self._root_templates = None
        self._spell_lists = None
        self._tags = None

        self._scripts = None
        self._treasure_table = None

    def make_uuid(self, key: str) -> UUID:
        m = hashlib.sha256()
        m.update(self._uuid.bytes)
        m.update(bytes(key, "UTF-8"))
        return UUID(m.hexdigest()[0:32])

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

    def get_version(self) -> (int, int, int, int):
        return self._version

    def get_modifiers(self) -> Modifiers:
        return self._modifiers

    def get_localization(self) -> Localization:
        return self._localization

    def add(self, item: any) -> None:
        """Add a datum to the GameData collection."""
        if isinstance(item, GameDatum):
            self._gamedata.add(item)
        elif isinstance(item, Node):
            self._lsx_collection.add(item)
        else:
            raise TypeError("add: Invalid data type")

    def add_character_creation_presets(self, nodes: [Lsx.Node]) -> None:
        if not self._character_creation_presets:
            self._character_creation_presets = Lsx(self._version, "CharacterCreationPresets", "root")
        self._character_creation_presets.add_children(nodes)

    def add_class_descriptions(self, nodes: [Lsx.Node]) -> None:
        if not self._class_descriptions:
            self._class_descriptions = Lsx(self._version, "ClassDescriptions", "root")
        self._class_descriptions.add_children(nodes)

    def add_feat_descriptions(self, nodes: [Lsx.Node]) -> None:
        if not self._feat_descriptions:
            self._feat_descriptions = Lsx(self._version, "FeatDescriptions", "root")
        self._feat_descriptions.add_children(nodes)

    def add_feats(self, nodes: [Lsx.Node]) -> None:
        if not self._feats:
            self._feats = Lsx(self._version, "Feats", "root")
        self._feats.add_children(nodes)

    def add_level_maps(self, nodes: [Lsx.Node]) -> None:
        if not self._level_maps:
            self._level_maps = Lsx(self._version, "LevelMapValues", "root")
        self._level_maps.add_children(nodes)

    def add_passive_lists(self, nodes: [Lsx.Node]) -> None:
        if not self._passive_lists:
            self._passive_lists = Lsx(self._version, "PassiveLists", "root")
        self._passive_lists.add_children(nodes)

    def add_progressions(self, nodes: [Lsx.Node]) -> None:
        if not self._progressions:
            self._progressions = Lsx(self._version, "Progressions", "root")
        self._progressions.add_children(nodes)

    def add_progression_descriptions(self, nodes: [Lsx.Node]) -> None:
        if not self._progression_descriptions:
            self._progression_descriptions = Lsx(self._version, "ProgressionDescriptions", "root")
        self._progression_descriptions.add_children(nodes)

    def add_races(self, nodes: [Lsx.Node]) -> None:
        if not self._races:
            self._races = Lsx(self._version, "Races", "root")
        self._races.add_children(nodes)

    def add_root_templates(self, nodes: [Lsx.Node]) -> None:
        if not self._root_templates:
            self._root_templates = Lsx(self._version, "Templates", "Templates")
        self._root_templates.add_children(nodes)

    def add_spell_lists(self, nodes: [Lsx.Node]) -> None:
        if not self._spell_lists:
            self._spell_lists = Lsx(self._version, "SpellLists", "root")
        self._spell_lists.add_children(nodes)

    def add_tags(self, nodes: [Lsx.Node]) -> None:
        if not self._tags:
            self._tags = []
        self._tags.extend(nodes)

    def add_script(self, text: str) -> None:
        self._scripts = self._scripts or []
        if text not in self._scripts:
            self._scripts.append(text)

    def add_treasure_table(self, text: str) -> None:
        self._treasure_table = self._treasure_table or []
        self._treasure_table.append(text)

    def _build_meta(self, mod_dir: str) -> None:
        """Build the meta.lsx underneath the given mod_dir."""
        build_version = str(time.time_ns())

        lsx = Lsx(self._version, "Config", "root")
        lsx.add_children([
            Lsx.Node("Dependencies"),
            Lsx.Node("ModuleInfo", attributes=[
                    Lsx.Attribute("Author", "LSWString", value=self._author),
                    Lsx.Attribute("CharacterCreationLevelName", "FixedString", value=""),
                    Lsx.Attribute("Description", "LSWString", value=self._description),
                    Lsx.Attribute("Folder", "LSWString", value=self._folder),
                    Lsx.Attribute("LobbyLevelName", "FixedString", value=""),
                    Lsx.Attribute("MD5", "LSString", value=""),
                    Lsx.Attribute("MainMenuBackgroundVideo", "FixedString", value=""),
                    Lsx.Attribute("MenuLevelName", "FixedString", value=""),
                    Lsx.Attribute("Name", "FixedString", value=self._name),
                    Lsx.Attribute("NumPlayers", "uint8", value="4"),
                    Lsx.Attribute("PhotoBooth", "FixedString", value=""),
                    Lsx.Attribute("StartupLevelName", "FixedString", value=""),
                    Lsx.Attribute("Tags", "LSString", value=""),
                    Lsx.Attribute("Type", "FixedString", value="Add-on"),
                    Lsx.Attribute("UUID", "FixedString", value=str(self._uuid)),
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
        lsx.build(os.path.join(mod_dir, "Mods", self._folder, "meta.lsx"))

    def _build_character_creation_presets(self, public_dir: str) -> None:
        if self._character_creation_presets:
            self._character_creation_presets.build(os.path.join(public_dir, "CharacterCreationPresets",
                                                                 "CharacterCreationPresets.lsx"))

    def _build_class_descriptions(self, public_dir: str) -> None:
        if self._class_descriptions:
            self._class_descriptions.build(os.path.join(public_dir, "ClassDescriptions", "ClassDescriptions.lsx"))

    def _build_feat_descriptions(self, public_dir: str) -> None:
        if self._feat_descriptions:
            self._feat_descriptions.build(os.path.join(public_dir, "Feats", "FeatDescriptions.lsx"))

    def _build_feats(self, public_dir: str) -> None:
        if self._feats:
            self._feats.build(os.path.join(public_dir, "Feats", "Feats.lsx"))

    def _build_level_maps(self, public_dir: str) -> None:
        if self._level_maps:
            self._level_maps.build(os.path.join(public_dir, "Levelmaps", "LevelMapValues.lsx"))

    def _build_progressions(self, public_dir: str) -> None:
        if self._progressions:
            self._progressions.build(os.path.join(public_dir, "Progressions", "Progressions.lsx"))

    def _build_passive_lists(self, public_dir: str) -> None:
        if self._passive_lists:
            self._passive_lists.build(os.path.join(public_dir, "Lists", "PassiveLists.lsx"))

    def _build_progression_descriptions(self, public_dir: str) -> None:
        if self._progression_descriptions:
            self._progression_descriptions.build(
                os.path.join(public_dir, "Progressions", "ProgressionDescriptions.lsx"))

    def _build_races(self, public_dir: str) -> None:
        if self._races:
            self._races.build(os.path.join(public_dir, "Races", "Races.lsx"))

    def _build_root_templates(self, public_dir: str) -> None:
        if self._root_templates:
            self._root_templates.build(os.path.join(public_dir, "RootTemplates", "_merged.lsx"))

    def _build_spell_lists(self, public_dir: str) -> None:
        if self._spell_lists:
            self._spell_lists.build(os.path.join(public_dir, "Lists", "SpellLists.lsx"))

    def _build_tags(self, public_dir: str) -> None:
        if self._tags:
            for tag in self._tags:
                lsx = Lsx(self._version, "Tags")
                lsx.set_root(tag)
                tag_uuid = next(attr.get_value() for attr in tag.get_attributes() if attr.get_id() == "UUID")
                tag_file = f"{tag_uuid}.lsx"
                lsx.build(os.path.join(public_dir, "Tags", tag_file))

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

    def build(self) -> None:
        """Build the mod files underneath the _base_dir."""
        mod_dir = os.path.join(self._base_dir, self._folder)
        if os.path.exists(mod_dir):
            shutil.rmtree(mod_dir)
        os.makedirs(mod_dir, exist_ok=True)
        self._build_meta(mod_dir)
        self._gamedata.build(mod_dir, self._folder)
        self._lsx_collection.save(mod_dir, self._version)
        self._localization.build(mod_dir)
        public_dir = os.path.join(mod_dir, "Public", self._folder)
        self._build_character_creation_presets(public_dir)
        self._build_class_descriptions(public_dir)
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
        self._build_scripts(mod_dir)
        self._build_treasure_table(public_dir)
