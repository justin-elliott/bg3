#!/usr/bin/env python3
"""
Localization for Baldur's Gate 3 mods.
"""

import hashlib
import os
import re

from modtools.prologue import XML_PROLOGUE
from uuid import UUID

import xml.etree.ElementTree as ElementTree

_double_newline = re.compile("[ \t]*\n[ \t]*\n[ \t]*")
_whitespace_run = re.compile("\\s{2,}")
_whitespace_around_br = re.compile("\\s*<br>\\s*")


def _strip_whitespace(s):
    return _whitespace_around_br.sub("<br>", _whitespace_run.sub(" ", _double_newline.sub("<br><br>", s.strip())))


class Translation:
    """A single entry in the localization dictionary."""

    handle: str

    __translations: {str, str}

    def __init__(self, handle: str, translations: {str: str}) -> None:
        self.handle = handle
        self.__translations = {short_lang_name: _strip_whitespace(text)
                               for short_lang_name, text in translations.items()}

    def add_content(self, content_list: ElementTree.Element, short_lang_name: str) -> None:
        content = ElementTree.SubElement(content_list, "content", contentuid=self.handle, version="1")
        content.text = self.__translations[short_lang_name]


class Localization:
    """Localization dictionaries."""

    __mod_uuid: UUID
    __languages: {str, str}
    __translations: {str, Translation}

    def __init__(self, mod_uuid: UUID):
        self.__mod_uuid = mod_uuid
        self.__languages = {}
        self.__translations = {}

    def add_language(self, short_lang_name: str, full_lang_name: str) -> None:
        """Add a language by its short and full names."""
        self.__languages[short_lang_name] = full_lang_name

    def __getitem__(self, key: str) -> str:
        """Get the translation handle for a given key."""
        return self.__translations[key].handle

    def __setitem__(self, key: str, translations: {str: str}) -> None:
        """Add a translation for the given key."""
        m = hashlib.sha256()
        m.update(self.__mod_uuid.bytes)
        m.update(bytes(key, "UTF-8"))
        handle = f"h{str(UUID(m.hexdigest()[0:32])).replace("-", "g")}"

        for short_lang_name in translations.keys():
            if short_lang_name not in self.__languages:
                raise KeyError(f"Unknown short language name for '{key}': '{short_lang_name}'")

        for short_lang_name in self.__languages.keys():
            if short_lang_name not in translations:
                raise KeyError(f"Missing translation for '{key}': '{short_lang_name}'")

        self.__translations[key] = Translation(handle, translations)

    def build(self, mod_dir: str) -> None:
        """Build the localization files in the given mod_dir."""
        for short_lang_name, full_lang_name in self.__languages.items():
            content_list = ElementTree.Element("contentList")
            for _, translation in self.__translations.items():
                translation.add_content(content_list, short_lang_name)
            language_dir = os.path.join(mod_dir, "Localization", full_lang_name)
            os.makedirs(language_dir, exist_ok=True)
            with open(os.path.join(language_dir, f"{full_lang_name}.loca.xml"), "wb") as f:
                f.write(XML_PROLOGUE)
                xml_document = ElementTree.ElementTree(content_list)
                ElementTree.indent(xml_document, space=" "*4)
                xml_document.write(f, encoding="UTF-8", xml_declaration=False)
