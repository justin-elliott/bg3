#!/usr/bin/env python3
"""
Baldur's Gate 3 spell lists.
"""

from functools import cached_property
from modtools.lsx import Lsx
from modtools.mod import Mod
from modtools.lsx.game import SpellList, SpellLists
from uuid import UUID


class GameSpellLists:
    _SPELL_LISTS_LSX_PATH = "Shared.pak/Public/Shared/Lists/SpellLists.lsx"
    _SPELL_LISTS_DEV_LSX_PATH = "Shared.pak/Public/SharedDev/Lists/SpellLists.lsx"

    _mod: Mod

    def __init__(self, mod: Mod):
        self._mod = mod

    @cached_property
    def spell_lists(self) -> SpellLists:
        spell_lists_lsx = Lsx.load(self._mod.get_cache_path(self._SPELL_LISTS_LSX_PATH))
        spell_lists_dev_lsx = Lsx.load(self._mod.get_cache_path(self._SPELL_LISTS_DEV_LSX_PATH))
        spell_lists_lsx.children.update(spell_lists_dev_lsx.children, key=self._key_by_uuid)
        spell_lists_lsx.children.sort(key=self._key_by_comment)
        return spell_lists_lsx

    @staticmethod
    def _key_by_comment(spell_list: SpellList) -> str:
        return spell_list.Comment.lower()

    @staticmethod
    def _key_by_uuid(spell_list: SpellList) -> str:
        return spell_list.UUID

    def _find_by_uuid(self, uuid: UUID) -> SpellList:
        def by_uuid(node: SpellList) -> bool:
            return node.UUID == uuid
        return self.spell_lists.children.find(by_uuid)

    # Cleric Spells

    @cached_property
    def cleric_cantrips(self) -> SpellList:
        return self._find_by_uuid(UUID("2f43a103-5bf1-4534-b14f-663decc0c525"))

    @cached_property
    def cleric_level_1_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("269d1a3b-eed8-4131-8901-a562238f5289"))

    @cached_property
    def cleric_level_2_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("2968a3e6-6c8a-4c2e-882a-ad295a2ad8ac"))

    @cached_property
    def cleric_level_3_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("21be0992-499f-4c7a-a77a-4430085e947a"))

    @cached_property
    def cleric_level_4_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("37e9b20b-5fd1-45c5-b1c5-159c42397c83"))

    @cached_property
    def cleric_level_5_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("b73aeea5-1ff9-4cac-b61d-b5aa6dfe31c2"))

    @cached_property
    def cleric_level_6_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("f8ba7b05-1237-4eaa-97fa-1d3623d5862b"))

    # Druid Spells

    @cached_property
    def druid_cantrips(self) -> SpellList:
        return self._find_by_uuid(UUID("b8faf12f-ca42-45c0-84f8-6951b526182a"))

    @cached_property
    def druid_level_1_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("2cd54137-2fe5-4100-aad3-df64735a8145"))

    @cached_property
    def druid_level_2_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("92126d17-7f1a-41d2-ae6c-a8d254d2b135"))

    @cached_property
    def druid_level_3_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("3156daf5-9266-41d0-b52c-5bc559a98654"))

    @cached_property
    def druid_level_4_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("09c326c9-672c-4198-a4c0-6f07323bde27"))

    @cached_property
    def druid_level_5_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("ff711c12-b59f-4fde-b9ea-6e5c38ec8f23"))

    @cached_property
    def druid_level_6_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("6a4e2167-55f3-4ba8-900f-14666b293e93"))

    # Warlock Spells

    @cached_property
    def warlock_cantrips(self) -> SpellList:
        return self._find_by_uuid(UUID("f5c4af9c-5d8d-4526-9057-94a4b243cd40"))

    @cached_property
    def warlock_level_1_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("4823a292-f584-4f7f-8434-6630c72e5411"))

    @cached_property
    def warlock_level_2_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("835aeca7-c64a-4aaa-a25c-143aa14a5cec"))

    @cached_property
    def warlock_level_3_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("5dec41aa-f16a-434e-b209-50c07e64e4ed"))

    @cached_property
    def warlock_level_4_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("7ad7dbd0-751b-4bcd-8034-53bcc7bfb19d"))

    @cached_property
    def warlock_level_5_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("deab57bf-4eec-4085-82f7-87335bce3f5d"))

    # Wizard Spells

    @cached_property
    def wizard_cantrips(self) -> SpellList:
        return self._find_by_uuid(UUID("3cae2e56-9871-4cef-bba6-96845ea765fa"))

    @cached_property
    def wizard_level_1_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("11f331b0-e8b7-473b-9d1f-19e8e4178d7d"))

    @cached_property
    def wizard_level_2_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("80c6b070-c3a6-4864-84ca-e78626784eb4"))

    @cached_property
    def wizard_level_3_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("22755771-ca11-49f4-b772-13d8b8fecd93"))

    @cached_property
    def wizard_level_4_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("820b1220-0385-426d-ae15-458dc8a6f5c0"))

    @cached_property
    def wizard_level_5_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("f781a25e-d288-43b4-bf5d-3d8d98846687"))

    @cached_property
    def wizard_level_6_spells(self) -> SpellList:
        return self._find_by_uuid(UUID("bc917f22-7f71-4a25-9a77-7d2f91a96a65"))
