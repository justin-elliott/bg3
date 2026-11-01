#!/usr/bin/env python3

from modtools.gamedata import SpellData
from modtools.lsx.game import Dependencies
from modtools.replacers import Mod

import os


class VampirePatches(Mod):
    def __init__(self, **kwds: str):
        super().__init__(os.path.join(os.path.dirname(__file__)),
                         author="justin-elliott",
                         name="VampirePatches",
                         description="Patches for the Symphony of a Vampire - Vampirism Overhaul mod.",
                         **kwds)

        self.add(Dependencies.ShortModuleDesc(
            Folder="vampiric_tree_75d2d721-1e37-d98f-9e4e-dc330c33ee10",
            MD5="38d556d7af0d378ffe57fd4b14c3f036",
            Name="Symphony of a Vampire - Vampirism Overhaul",
            PublishHandle=6339986,
            UUID="75d2d721-1e37-d98f-9e4e-dc330c33ee10",
            Version64=36310271995674683,
        ))

        self._patch_shadow_leap()

    def _patch_shadow_leap(self) -> None:
        """Make Shadow Leap less situational in use."""
        self.add(SpellData(
            "Target_VT_ShadowLeap",
            using="Target_VT_ShadowLeap",
            SpellType="Target",
            RequirementConditions=[],
            RequirementEvents=[],
            TargetConditions=["CanStand('') and not Character() and not Self()"],
        ))


if __name__ == "__main__":
    vampire_patches = VampirePatches()
    vampire_patches.build()