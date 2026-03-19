#!/usr/bin/env python3
"""
Maneuver-related functionality for Baldur's Gate 3 mods.
"""

from functools import cached_property
from moddb.scripts import is_battle_master_maneuver
from modtools.gamedata import InterruptData, PassiveData, SpellData
from modtools.mod import Mod


class Maneuvers:
    """Maneuver-related functionality for Baldur's Gate 3 mods."""
    _mod: Mod

    def __init__(self, mod: Mod):
        """Initialize for the given Mod."""
        self._mod = mod
        
        self._update_precision_attack()
        self._update_sweeping_attack()

    def _update_precision_attack(self) -> None:
        passive_name = "PrecisionAttack"
        interrupt_name = self._mod.make_name("Interrupt_PrecisionAttack")

        self._mod.loca[f"{passive_name}_DisplayName"] = "Precision Attack"

        self._mod.add(PassiveData(
            passive_name,
            DisplayName=self._mod.loca[f"{passive_name}_DisplayName"],
            Description=self._mod.loca(f"{passive_name}_Description", """
                On a miss, you can spend a <LSTag Type="ActionResource" Tooltip="SuperiorityDie">Superiority Die</LSTag>
                to add it to the result of the <LSTag Tooltip="AttackRoll">Attack Roll</LSTag>, possibly making it hit.
            """),
            Icon="Action_PrecisionAttack",
            Boosts=[f"UnlockInterrupt({interrupt_name})"],
        ))

        self._mod.add(is_battle_master_maneuver)
        self._mod.add(InterruptData(
            interrupt_name,
            DisplayName=self._mod.loca[f"{passive_name}_DisplayName"],
            Description=self._mod.loca(f"{interrupt_name}_Description", """
                Add a <LSTag Type="ActionResource" Tooltip="SuperiorityDie">Superiority Die</LSTag> to
                your <LSTag Tooltip="AttackRoll">Attack Roll</LSTag>.
            """),
            Icon="Action_PrecisionAttack",
            InterruptContext="OnPostRoll",
            InterruptContextScope="Self",
            Container="YesNoDecision",
            Conditions=[
                "Self(context.Source,context.Observer)"
                + " and not Dead(context.Observer)"
                + " and HasInterruptedAttack()"
                + " and not AnyEntityIsItem()"
                + " and (not IsBattleMasterManeuver()"
                +       " or HasActionResource('SuperiorityDie',2,0,false,false,context.Source))"
                + " and ((not CharacterLevelGreaterThan(9) and IsFlatValueInterruptInteresting(8,context.Source))"
                +       " or (CharacterLevelGreaterThan(9) and IsFlatValueInterruptInteresting(10,context.Source)))",
            ],
            Properties=["AdjustRoll(OBSERVER_OBSERVER,LevelMapValue(SuperiorityDie))"],
            Cost="SuperiorityDie:1",
            InterruptDefaultValue=["Ask", "Enabled"],
            EnableCondition=[
                "not HasStatus('SG_Polymorph')"
                + " or HasAnyStatus({"
                +       "'SG_Disguise',"
                +       "'WILDSHAPE_STARRY_ARCHER_PLAYER',"
                +       "'WILDSHAPE_STARRY_CHALICE_PLAYER',"
                +       "'WILDSHAPE_STARRY_DRAGON_PLAYER'"
                +       "})",
            ],
            EnableContext=["OnStatusApplied", "OnStatusRemoved"],
        ))

    def _update_sweeping_attack(self) -> None:
        passive_name = "SweepingAttack"
        spell_name = "Zone_SweepingAttack"

        self._mod.add(PassiveData(
            passive_name,
            using=passive_name,
            Description=self._mod.loca(f"{passive_name}_Description", """
                Swing your weapon in a rapid, sweeping arc to attack multiple enemies at once.
            """),
        ))

        self._mod.add(SpellData(
            spell_name,
            using=spell_name,
            SpellType="Zone",
            SpellProperties=[
                "GROUND:DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "GROUND:ExecuteWeaponFunctors(MainHand)",
                "IF(not Player(context.Source)):ApplyStatus(SELF,AI_HELPER_EXTRAATTACK,100,1)",
            ],
            SpellSuccess=[
                "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)",
                "ExecuteWeaponFunctors(MainHand)",
            ],
            TooltipDamageList=["DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType)"],
        ))
    
    @cached_property
    def relentless(self) -> str:
        name = self._mod.make_name("Relentless")
        self._mod.loca[f"{name}_DisplayName"] = "Relentless"
        self._mod.loca[f"{name}_Description"] = """
            At the start of your turn, you regain one
            <LSTag Type="ActionResource" Tooltip="SuperiorityDie">Superiority Die</LSTag>.
        """
        self._mod.add(PassiveData(
            name,
            DisplayName=self._mod.loca[f"{name}_DisplayName"],
            Description=self._mod.loca[f"{name}_Description"],
            Icon="Action_BolsteringMagic_Boost",
            Conditions=["Combat()"],
            Properties=["Highlighted", "ForceShowInCC"],
            StatsFunctorContext=["OnTurn"],
            StatsFunctors=["RestoreResource(SuperiorityDie,1,0)"],
        ))
        return name
