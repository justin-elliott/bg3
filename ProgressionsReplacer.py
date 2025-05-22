#!/usr/bin/env python3
"""
Generates files for the "ProgressionsReplacer" mod.
"""

import argparse
import os

from moddb import multiply_resources
from modtools.lsx.game import (
    ActionResource,
    BASE_CHARACTER_CLASSES,
    CharacterClass,
    CharacterSubclasses,
)
from modtools.lsx.game import Dependencies, Progression
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

    def _allow_improvement(self, progression: Progression) -> None:
        character_class = CharacterClass(progression.Name)
        if character_class not in self.args.classes:
            raise DontIncludeProgression()
        feats = (self.args.rogue_feats if character_class == CharacterClass.ROGUE
                else self.args.fighter_feats if character_class == CharacterClass.FIGHTER
                else self.args.other_feats)
        allow_improvement = progression.AllowImprovement
        progression.AllowImprovement = (progression.Level in feats) or None
        if allow_improvement == progression.AllowImprovement:
            raise DontIncludeProgression()

    @progression(BASE_CHARACTER_CLASSES, range(2, 21))
    @only_existing_progressions
    def allow_improvement_base(self, progression: Progression) -> None:
        self._allow_improvement(progression)

    @progression(CharacterSubclasses.ALL, range(1, 21))
    @only_existing_progressions
    def increase_resources(self, progression: Progression) -> None:
        if CharacterClass(progression.Name) not in self.args.classes:
            raise DontIncludeProgression()
        boosts = progression.Boosts
        multiply_resources(progression, [ActionResource.SPELL_SLOTS], self.args.spells)
        multiply_resources(progression, [ActionResource.WARLOCK_SPELL_SLOTS], self.args.warlock_spells)
        multiply_resources(progression, self.ACTION_RESOURCES, self.args.actions)
        if boosts == progression.Boosts:
            raise DontIncludeProgression()

    @progression(BASE_CHARACTER_CLASSES, 1, is_multiclass=False)
    def increase_skills(self, progression: Progression) -> None:
        if CharacterClass(progression.Name) not in self.args.classes:
            raise DontIncludeProgression()
        selectors = progression.Selectors
        if self.args.skills is not None:
            selectors = [selector for selector in (selectors or []) if not selector.startswith("SelectSkills(")]
            selectors.append(f"SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self.args.skills})")
        if self.args.expertise is not None:
            selectors = [selector for selector in selectors if not selector.startswith("SelectSkillsExpertise(")]
            selectors.append(f"SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,{self.args.expertise})")
        if progression.Selectors == selectors:
            raise DontIncludeProgression
        progression.Selectors = selectors


def class_list(s: str) -> set[str]:
    classes = frozenset([CharacterClass(cc) for cc in s.split(",")])
    if not classes.issubset(BASE_CHARACTER_CLASSES):
        raise "Invalid class names"
    return classes


def level_list(s: str) -> set[int]:
    levels = frozenset([int(level) for level in s.split(",")])
    if not levels.issubset(frozenset(range(1, 21))):
        raise "Invalid levels"
    return levels


def main():
    progressions_replacer = ProgressionsReplacer()
    progressions_replacer.build()


if __name__ == "__main__":
    main()
