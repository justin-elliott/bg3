#!/usr/bin/env python3
"""
Parser for the ValueLists.txt file.
"""

import argparse
import os
import re

from collections.abc import Mapping
from modtools.prologue import PYTHON_PROLOGUE
from modtools.unpak import Unpak
from pathlib import PurePath


PROLOGUE = f'''\
{PYTHON_PROLOGUE}
import modtools.gamedata.valuelists as VL

from modtools.gamedata.gamedata import GameData
'''

MODIFIERS_PATH = "Shared.pak/Public/Shared/Stats/Generated/Structure/Modifiers.txt"


class GameDataParser:
    """Parse the Modifiers.txt file."""
    _MODIFIER_REGEX = re.compile("""\\s*modifier\\s+type\\s*"([^"]+)"\\s*""")
    _MEMBER_REGEX = re.compile("""\\s*modifier\\s*"([^"]+)"\\s*,\\s*"([^"]+)"\\s*""")

    _MODIFIER_TO_FILENAME = {
        "Character": "Character.txt",
        "Armor": "Armor.txt",
        "ObjectData": "Object.txt",
        "Weapon": "Weapon.txt",
        "SpellData": "Spell_{self.SpellType[0]}.txt",
        "StatusData": "Status_{self.StatusType[0]}.txt",
        "PassiveData": "Passive.txt",
        "InterruptData": "Interrupt.txt",
        "CriticalHitTypeData": "CriticalHitTypes.txt",
    }

    _STDOUT = 1

    _modifiers_path: os.PathLike

    def __init__(self, unpak: Unpak):
        pak_name, _, relative_path = str(PurePath(MODIFIERS_PATH).as_posix()).partition("/")
        cached_pak = unpak.get(pak_name)
        self._modifiers_path = os.path.join(cached_pak.path, relative_path)

    def parse(self, output: str | None):
        if output:
            output_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "modtools", output))
            os.makedirs(output_path, exist_ok=True)
        else:
            output_path = None

        modifiers: Mapping[str, Mapping[str, str]] = {}
        modifier: str = None
        members: Mapping[str, str] = {}

        with open(self._modifiers_path, "r") as modifiers_file:
            for line in modifiers_file:
                if match := self._MODIFIER_REGEX.match(line):
                    if modifier:
                        modifiers[modifier] = members
                    modifier = match[1]
                    members = {}
                    if modifier == "Object":
                        modifier = "ObjectData"
                        members = {"_id_": "Object"}
                elif match := self._MEMBER_REGEX.match(line):
                    members[match[1].replace(" ", "_")] = match[2].replace(" ", "")
                elif line.strip():
                    raise RuntimeError(f"Unknown line in Modifiers.txt: {line}")

        if modifier is not None:
            modifiers[modifier] = members

        for modifier in modifiers.keys():
            modifier_file = os.path.join(output_path, modifier.lower() + ".py") if output_path is not None else None
            with (open(modifier_file, "w") if modifier_file is not None else os.fdopen(self._STDOUT, "w")) as f:
                f.write(PROLOGUE)
                f.write("\n\n")
                f.write(f"class {modifier}(GameData):\n")
                members = modifiers[modifier]
                if "_id_" in members:
                    f.write(f"    _id_ = \"{members["_id_"]}\"\n")
                for member, member_type in sorted(members.items()):
                    if member != "_id_":
                        f.write(f"    {member}: VL.{member_type} = VL.{member_type}\n")
                f.write("\n")
                filename = self._MODIFIER_TO_FILENAME[modifier]
                f.write("    def filename(self) -> str:\n")
                f.write(f"""        return {"f" if "{" in filename else ""}"{filename}"\n""")


def main():
    parser = argparse.ArgumentParser(description="Generate GameData definitions from the Modifiers.txt file.")
    parser.add_argument("-o", "--output", type=str, default=None, help="Name of the output directory.")
    args = parser.parse_args()

    unpak = Unpak(cache_dir=None)
    parser = GameDataParser(unpak)
    parser.parse(args.output)


if __name__ == "__main__":
    main()
