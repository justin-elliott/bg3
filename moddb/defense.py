#!/usr/bin/env python3
"""
Defense-related functionality for Baldur's Gate 3 mods.
"""

from functools import cached_property
from modtools.lsx.game import CharacterAbility, SpellList
from modtools.gamedata import InterruptData, PassiveData, SpellData
from modtools.mod import Mod


class Defense:
    """Defense-related functionality for Baldur's Gate 3 mods."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize for the given Mod."""
        self._mod = mod

    @cached_property
    def _counterspell_display_name(self):
        """Get the localization handle for the Counterspell display name."""
        display_name = f"{self._mod.get_prefix()}_Counterspell_DisplayName"
        loca = self._mod.get_localization()
        loca[display_name] = {"en": "Counterspell"}
        return loca[display_name]

    @cached_property
    def _counterspell_description(self):
        """Get the localization handle for the Counterspell description."""
        description = f"{self._mod.get_prefix()}_Counterspell_Description"
        loca = self._mod.get_localization()
        loca[description] = {"en": """
            Try to stop a spell being cast.
            """}
        return loca[description]

    @cached_property
    def _warding_display_name(self):
        """Get the localization handle for the Warding display name."""
        display_name = f"{self._mod.get_prefix()}_Warding_DisplayName"
        loca = self._mod.get_localization()
        loca[display_name] = {"en": "Warding"}
        return loca[display_name]

    @cached_property
    def _warding_description(self):
        """Get the localization handle for the Warding description."""
        description = f"{self._mod.get_prefix()}_Warding_Description"
        loca = self._mod.get_localization()
        loca[description] = {"en": """
            A magical barrier protects you from harm, making you resistant to all forms of damage.
            Incoming damage is reduced by [1].
            """}
        return loca[description]

    def add_counterspell(self, *,
                         display_name_handle: str = None,
                         description_handle: str = None) -> None:
        """Add Counterspell, returning its name."""
        name = f"{self._mod.get_prefix()}_Counterspell"

        if not display_name_handle:
            display_name_handle = self._counterspell_display_name
        if not description_handle:
            description_handle = self._counterspell_description

        self._mod.add(SpellData(
            name,
            using="Target_Counterspell_6",
            SpellType="Target",
            DisplayName=display_name_handle,
            Description=description_handle,
            InterruptPrototype=f"{name}_Interrupt",
            UseCosts=["ReactionActionPoint:1"],
        ))

        self._mod.add(InterruptData(
            f"{name}_Interrupt",
            using="Interrupt_Counterspell_6",
            DisplayName=display_name_handle,
            Description=description_handle,
            Success=[
                "Counterspell()",
                f"UseSpell(OBSERVER_SOURCE,{name}_Success,true,true,true)",
            ],
            Cost=["ReactionActionPoint:1"],
        ))

        self._mod.add(SpellData(
            f"{name}_Success",
            using="Target_Counterspell_Success",
            SpellType="Target",
            InterruptPrototype=f"{name}_Interrupt",
            UseCosts=["ReactionActionPoint:1"],
        ))

        return name

    def add_counterspell_spell_list(self, *,
                         display_name_handle: str = None,
                         description_handle: str = None) -> None:
        """Add a spell list containing the Counterspell spell."""
        spell_list = str(self._mod.make_uuid("counterspell_spell_list"))
        self._mod.add(SpellList(
            Name="Counterspell spell list",
            Spells=[self.add_counterspell(display_name_handle=display_name_handle,
                                          description_handle=description_handle)],
            UUID=spell_list,
        ))
        return spell_list

    def add_unarmored_defense(self, ability: CharacterAbility, *, icon: str = "PassiveFeature_UnarmoredDefense") -> str:
        ability_name = ability.name.title()

        name = f"{self._mod.get_prefix()}_UnarmoredDefense_{ability_name}"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Unarmored Defense"}
        loca[f"{name}_Description"] = {"en": f"""
            Your body is as resilient as any armour.
            While not wearing armour, you add {"twice" if ability == CharacterAbility.DEXTERITY else ""}
            your {ability_name} <LSTag Tooltip="AbilityModifier">Modifier</LSTag>
            to your <LSTag Tooltip="ArmourClass">Armour Class</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon=icon,
            Properties=["Highlighted"],
            BoostContext=["OnEquip", "OnCreate"],
            BoostConditions=["not WearingArmor(context.Source) and not HasShieldEquipped(context.Source)"],
            Boosts=[f"ACOverrideFormula(10,true,Dexterity,{ability_name})"],
        ))

        return name

    def add_warding(self, *,
                    bonus: str = "ProficiencyBonus",
                    display_name_handle: str = None,
                    description_handle: str = None,
                    icon: str = "PassiveFeature_ArcaneWard") -> None:
        """Add the Warding passive, returning its name."""
        name = f"{self._mod.get_prefix()}_Warding"

        if not display_name_handle:
            display_name_handle = self._warding_display_name
        if not description_handle:
            description_handle = self._warding_description

        self._mod.add(PassiveData(
            name,
            DisplayName=display_name_handle,
            Description=description_handle,
            DescriptionParams=[f"RegainHitPoints(max(1,{bonus}))"],
            Icon=icon,
            Properties=["Highlighted"],
            Boosts=[f"DamageReduction(All,Flat,{bonus})"],
        ))

        return name
