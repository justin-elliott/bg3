#!/usr/bin/env python3
"""
A decorator for origin replacement.
"""

from collections.abc import Callable
from modtools.lsx import Lsx
from modtools.lsx.game import SpellList
from modtools.replacers.replacer import Replacer


type SpellListBuilder = Callable[[Replacer, SpellList], None]
type SpellListBuilderDict = dict[str, SpellListBuilder]


_SPELL_LISTS_LSX_PATH = "Shared.pak/Public/Shared/Lists/SpellLists.lsx"
_SPELL_LISTS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Lists/SpellLists.lsx"


def _by_comment(spell_list: SpellList) -> str:
    return spell_list.Comment


def _by_uuid(spell_list: SpellList) -> str:
    return spell_list.UUID


def _load_spell_lists(replacer: Replacer) -> list[SpellList]:
    """Load the game's SpellLists from the .pak cache."""
    spell_lists_lsx = Lsx.load(replacer.get_cache_path(_SPELL_LISTS_LSX_PATH))
    spell_lists_dev_lsx = Lsx.load(replacer.get_cache_path(_SPELL_LISTS_DEV_LSX_PATH))
    spell_lists_lsx.children.update(spell_lists_dev_lsx.children, key=_by_uuid)
    spell_lists_lsx.children.sort(key=_by_comment)
    return list(spell_lists_lsx.children)


def _make_builders(spell_list_builders: list[SpellListBuilder]) -> SpellListBuilderDict:
    """Make a SpellListBuilderDict from the decorated spell_list builders."""
    builders: SpellListBuilderDict = dict()

    for spell_list_builder in spell_list_builders:
        names = getattr(spell_list_builder, "spell_lists")
        for name in names:
            builders[name] = spell_list_builder

    return builders


def _update_spell_lists(replacer: Replacer,
                        spell_lists: list[SpellList],
                        builders: SpellListBuilderDict,
                        updated_spell_lists: set[SpellList]):
    """Update spell lists that match our builder names."""
    for spell_list in spell_lists:
        if builder_fn := builders.get(spell_list.UUID):
            builder_fn(replacer, spell_list)
            updated_spell_lists.add(spell_list)


def _spell_list_builder(replacer: Replacer, spell_list_builders: list[SpellListBuilder]) -> None:
    """Update existing spell lists."""
    builders = _make_builders(spell_list_builders)

    spell_lists = _load_spell_lists(replacer)
    updated_spell_lists: set[SpellList] = set()

    _update_spell_lists(replacer, spell_lists, builders, updated_spell_lists)

    # Save the updated origins
    for spell_list in sorted(updated_spell_lists, key=_by_comment):
        replacer.mod.add(spell_list)


def spell_list(uuid: str) -> SpellListBuilder:
    """A decorator mapping a spell list to its builder function."""
    def decorate(fn: SpellListBuilder) -> SpellListBuilder:
        setattr(fn, "builder", _spell_list_builder)
        spell_lists: list[str] = getattr(fn, "spell_lists", [])
        spell_lists.append(uuid)
        setattr(fn, "spell_lists", spell_lists)
        return fn

    return decorate
