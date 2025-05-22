#!/usr/bin/env python3
"""
Generates files for the "ProgressionsReplacer" mod.
"""

import os

from modtools.lsx.game import (
    CharacterClass,
    CharacterSubclasses,
    Dependencies,
    Progression,
)
from modtools.replacers import (
    DontIncludeProgression,
    only_existing_progressions,
    progression,
    Replacer,
)


progression.include(
    "unlocklevelcurve_a2ffd0e4-c407-4p40.pak/Public/UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77/"
    + "Progressions/Progressions.lsx"
)


class ProgressionsReplacer(Replacer):
    def __init__(self):
        super().__init__(os.path.join(os.path.dirname(__file__), "Progressions"),
                         author="justin-elliott",
                         description="A class progressions replacer.")

        self.mod.add(Dependencies.ShortModuleDesc(
            Folder="UnlockLevelCurve_a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            MD5="f94d034502139cf8b65a1597554e7236",
            Name="UnlockLevelCurve",
            PublishHandle=4166963,
            UUID="a2ffd0e4-c407-8642-2611-c934ea0b0a77",
            Version64=72057594037927960,
        ))

    def make_name(self) -> str:
        """Generate a name for the Mod."""
        if len(self.args.feats) == 1:
            feat_level = next(level for level in self.args.feats)
            feat_levels = str(feat_level)
        else:
            feat_levels = "_".join(str(level) for level in sorted(self.args.feats))

        if len(feat_levels) > 0:
            feat_levels = f"F{feat_levels}-"

        if len(self.args.classes) == 0:
            class_names = "All"
        else:
            class_names = "-".join(class_name for class_name in self.args.classes)

        name = (f"Progressions-{class_names}-{feat_levels}S{self.args.spells}-W{self.args.warlock_spells}-"
                + f"A{self.args.actions}")
        if self.args.skills is not None:
            name += f"-K{self.args.skills}"
        if self.args.expertise is not None:
            name += f"-E{self.args.expertise}"
        return name

    @progression(CharacterSubclasses.ALL, range(1, 21))
    @only_existing_progressions
    def update_progression(self, _: Progression) -> None:
        """Ensure that we visit all relevant progressions. Updates themselves are handled by the Replacer."""
        raise DontIncludeProgression()


def main():
    progressions_replacer = ProgressionsReplacer()
    progressions_replacer.build()


if __name__ == "__main__":
    main()
