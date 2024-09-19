#!/usr/bin/env python3
"""
A decorator for origin replacement.
"""

from collections.abc import Callable
from functools import cache
from modtools.lsx import Lsx
from modtools.lsx.children import LsxChildren
from modtools.lsx.game import SpellList
from modtools.replacers.replacer import Replacer
from typing import Iterable
from uuid import UUID


class DontIncludeSpellList(BaseException):
    """Raised to exclude a spell list from being updated."""
    pass


_SPELL_LISTS_LSX_PATH = "Shared.pak/Public/Shared/Lists/SpellLists.lsx"
_SPELL_LISTS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Lists/SpellLists.lsx"

type SpellListBuilder = Callable[[Replacer, SpellList], None]
type SpellListBuilderDict = dict[str, list[SpellListBuilder]]


def _key_by_comment(spell_list: SpellList) -> str:
    return (spell_list.Comment or "").lower()


def _key_by_uuid(spell_list: SpellList) -> str:
    return spell_list.UUID


@cache
def _load_spell_lists(replacer: Replacer) -> LsxChildren:
    spell_lists_lsx = Lsx.load(replacer.get_cache_path(_SPELL_LISTS_LSX_PATH))
    spell_lists_dev_lsx = Lsx.load(replacer.get_cache_path(_SPELL_LISTS_DEV_LSX_PATH))
    spell_lists_lsx.children.update(spell_lists_dev_lsx.children, key=_key_by_uuid)
    spell_lists_lsx.children.sort(key=_key_by_comment)
    return spell_lists_lsx.children


@cache
def _find_by_uuid(replacer: Replacer, uuid: UUID) -> SpellList:
    def by_uuid(spell_list: SpellList) -> bool:
        return spell_list.UUID == str(uuid)
    return _load_spell_lists(replacer).find(by_uuid)


def _make_builders(spell_list_builders: list[SpellListBuilder]) -> SpellListBuilderDict:
    """Make a SpellListBuilderDict from the decorated spell_list builders."""
    builders: SpellListBuilderDict = dict()

    for spell_list_builder in spell_list_builders:
        comment_or_uuids = getattr(spell_list_builder, "spell_lists")
        for comment_or_uuid in comment_or_uuids:
            builders_list = builders.setdefault(comment_or_uuid, [])
            builders_list.append(spell_list_builder)

    return builders


def _update_spell_lists(replacer: Replacer,
                        spell_lists: Iterable[SpellList],
                        builders: SpellListBuilderDict,
                        updated_spell_lists: set[SpellList]):
    """Update spell lists that match our builder names."""
    unused_spell_lists = set(builders.keys())

    for spell_list in spell_lists:
        if builder_fns := builders.get(spell_list.Comment) or builders.get(spell_list.UUID):
            was_updated = False
            for builder_fn in builder_fns:
                try:
                    builder_fn(replacer, spell_list)
                    was_updated = True
                except DontIncludeSpellList:  # Can still be updated by another builder_fn
                    pass
                if spell_list.Comment in unused_spell_lists:
                    unused_spell_lists.remove(spell_list.Comment)
                else:
                    unused_spell_lists.remove(spell_list.UUID)

            if was_updated:
                updated_spell_lists.add(spell_list)

    if len(unused_spell_lists) > 0:
        raise KeyError(f"Unmatched spell_list(s): {", ".join(sorted(unused_spell_lists))}")


def _spell_list_builder(replacer: Replacer, spell_list_builders: list[SpellListBuilder]) -> None:
    """Update existing spell lists."""
    builders = _make_builders(spell_list_builders)

    spell_lists = _load_spell_lists(replacer)
    updated_spell_lists: set[SpellList] = set()

    _update_spell_lists(replacer, spell_lists, builders, updated_spell_lists)

    # Save the updated origins
    for spell_list in sorted(updated_spell_lists, key=_key_by_comment):
        replacer.mod.add(spell_list)


def spell_list(comment_or_uuid: str) -> SpellListBuilder:
    """A decorator mapping a spell list to its builder function."""
    if isinstance(comment_or_uuid, UUID):
        comment_or_uuid = str(comment_or_uuid)

    def decorate(fn: SpellListBuilder) -> SpellListBuilder:
        setattr(fn, "builder", _spell_list_builder)
        spell_lists: list[str] = getattr(fn, "spell_lists", [])
        spell_lists.append(comment_or_uuid)
        setattr(fn, "spell_lists", spell_lists)
        return fn

    return decorate


# Cleric Spells


def cleric_cantrips(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("2f43a103-5bf1-4534-b14f-663decc0c525"))


def cleric_level_1_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("269d1a3b-eed8-4131-8901-a562238f5289"))


def cleric_level_2_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("2968a3e6-6c8a-4c2e-882a-ad295a2ad8ac"))


def cleric_level_3_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("21be0992-499f-4c7a-a77a-4430085e947a"))


def cleric_level_4_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("37e9b20b-5fd1-45c5-b1c5-159c42397c83"))


def cleric_level_5_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("b73aeea5-1ff9-4cac-b61d-b5aa6dfe31c2"))


def cleric_level_6_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("f8ba7b05-1237-4eaa-97fa-1d3623d5862b"))


# Druid Spells


def druid_cantrips(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("b8faf12f-ca42-45c0-84f8-6951b526182a"))


def druid_level_1_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("2cd54137-2fe5-4100-aad3-df64735a8145"))


def druid_level_2_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("92126d17-7f1a-41d2-ae6c-a8d254d2b135"))


def druid_level_3_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("3156daf5-9266-41d0-b52c-5bc559a98654"))


def druid_level_4_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("09c326c9-672c-4198-a4c0-6f07323bde27"))


def druid_level_5_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("ff711c12-b59f-4fde-b9ea-6e5c38ec8f23"))


def druid_level_6_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("6a4e2167-55f3-4ba8-900f-14666b293e93"))


# Druid Spells


def eldritch_knight_cantrips(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("6529c75a-d8cd-4ddb-a1b1-f55cb1e66d9f"))


def eldritch_knight_level_1_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("32aeba85-13bd-4a6f-8e06-cd4447b746d8"))


def eldritch_knight_level_2_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("4a86443c-6a21-4b8d-b1bf-55a99e021354"))


# Ranger Spells


def ranger_level_1_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("458be063-60d4-4548-ae7d-50117fa0226f"))


def ranger_level_2_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("e7cfb80a-f5c2-4304-8446-9b00ea6a9814"))


def ranger_level_3_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("9a60f649-7f82-4152-90b1-0499c5c9f3e2"))


# Warlock Spells


def warlock_cantrips(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("f5c4af9c-5d8d-4526-9057-94a4b243cd40"))


def warlock_level_1_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("4823a292-f584-4f7f-8434-6630c72e5411"))


def warlock_level_2_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("835aeca7-c64a-4aaa-a25c-143aa14a5cec"))


def warlock_level_3_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("5dec41aa-f16a-434e-b209-50c07e64e4ed"))


def warlock_level_4_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("7ad7dbd0-751b-4bcd-8034-53bcc7bfb19d"))


def warlock_level_5_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("deab57bf-4eec-4085-82f7-87335bce3f5d"))


# Wizard Spells


def wizard_cantrips(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("3cae2e56-9871-4cef-bba6-96845ea765fa"))


def wizard_level_1_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("11f331b0-e8b7-473b-9d1f-19e8e4178d7d"))


def wizard_level_2_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("80c6b070-c3a6-4864-84ca-e78626784eb4"))


def wizard_level_3_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("22755771-ca11-49f4-b772-13d8b8fecd93"))


def wizard_level_4_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("820b1220-0385-426d-ae15-458dc8a6f5c0"))


def wizard_level_5_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("f781a25e-d288-43b4-bf5d-3d8d98846687"))


def wizard_level_6_spells(replacer: Replacer) -> SpellList:
    return _find_by_uuid(replacer, UUID("bc917f22-7f71-4a25-9a77-7d2f91a96a65"))
