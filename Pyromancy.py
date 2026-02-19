#!/usr/bin/env python3
"""
Generates files for the "Pyromancy" mod.
"""

import os

from functools import cached_property
from moddb import Movement
from modtools.gamedata import PassiveData, Weapon
from modtools.lsx.game import CharacterClass, ClassDescription
from modtools.lsx.game import (
    Progression,
    SpellList,
    Tags,
)
from modtools.replacers import (
    class_description,
    progression,
    Replacer,
    tag,
)
from modtools.text import Script


class Pyromancy(Replacer):
    @cached_property
    def _pyromancy_display_name(self) -> str:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_DisplayName"] = {"en": "Pyromancy"}
        return loca[f"{self.mod.get_prefix()}_DisplayName"]

    @cached_property
    def _pyromancy_description(self) -> str:
        loca = self.mod.get_localization()
        loca[f"{self.mod.get_prefix()}_Description"] = {"en": """
            Flickering flames dance on your fingertips, a primal power yearning to be unleashed. You are not just a
            sorcerer, but a conduit, channeling the raw essence of fire into searing spells and devastating displays.
            """}
        return loca[f"{self.mod.get_prefix()}_Description"]

    @cached_property
    def _eternal_flame(self) -> str:
        """Add the Eternal Flame passive, returning its name."""
        name = self.make_name("EternalFlame")
        fire_spell_check = self.make_name("FireSpellCheck")

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = "Eternal Flame"
        loca[f"{name}_Description"] = """
            Your damaging fire spells do not cost a <LSTag Tooltip="SpellSlot">spell slot</LSTag> to cast.
            """

        self.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Gold",
            Properties=["Highlighted"],
            Boosts=[
                f"UnlockSpellVariant({fire_spell_check}(),ModifyTooltipDescription(),"
                    + "ModifyUseCosts(Replace,SpellSlot,0,-1,SpellSlot),"
                    + "ModifyUseCosts(Replace,WarlockSpellSlot,0,-1,WarlockSpellSlot),"
                    + "ModifyUseCosts(Replace,SpellSlotsGroup,0,-1,SpellSlotsGroup))",
            ],
        ))

        self.add(Script(f"""
            -- Check for a damaging fire spell.
            function {fire_spell_check}()
                return IsSpell() & SpellDamageTypeIs(DamageType.Fire) & (HasUseCosts('SpellSlot') | HasUseCosts('WarlockSpellSlot'))
            end
        """))

        return name

    @cached_property
    def _fire_walk(self) -> str:
        """Add the Fire Walk spell, returning its name."""
        return Movement(self.mod).add_fire_walk()

    @cached_property
    def _forged_in_flames(self) -> str:
        """Add the Forged in Flames passive, returning its name."""
        name = self.make_name("ForgedInFlames")

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Forged in Flames"}
        loca[f"{name}_Description"] = {"en": """
            You have <LSTag Tooltip="Resistant">Resistance</LSTag> to Fire damage, and cannot be
            <LSTag Type="Status" Tooltip="BURNING">Burned</LSTag>.
            """}

        self.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Red",
            Properties=["Highlighted"],
            Boosts=[
                "Resistance(Fire,Resistant)",
                "StatusImmunity(BURNING)",
                "StatusImmunity(WILD_MAGIC_BURNING)",
            ],
        ))

        return name

    @cached_property
    def _overheat(self) -> str:
        """Add the Overheat passive, returning its name."""
        name = f"{self._mod.get_prefix()}_Overheat"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Overheat"}
        loca[f"{name}_Description"] = {"en": """
            Your fire spells burn hotter, ignoring resistance, and dealing additional damage equal to your
            <LSTag Tooltip="Charisma">Charisma</LSTag> <LSTag Tooltip="AbilityModifier">Modifier</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Brass",
            Properties=["Highlighted"],
            Boosts=[
                "IgnoreResistance(Fire,Resistant)",
                "IF(SpellDamageTypeIs(DamageType.Fire)):DamageBonus(max(0,CharismaModifier))",
            ],
        ))

        return name

    @cached_property
    def _hellfire(self) -> str:
        """Add the Hellfire passive, returning its name."""
        name = f"{self._mod.get_prefix()}_Hellfire"

        loca = self._mod.get_localization()
        loca[f"{name}_DisplayName"] = {"en": "Hellfire"}
        loca[f"{name}_Description"] = {"en": """
            Your fire spells burn as hot as the hells, overcoming resistance and immunity, and dealing additional damage
            equal to your <LSTag Tooltip="Charisma">Charisma</LSTag> <LSTag Tooltip="AbilityModifier">Modifier</LSTag>.
            """}

        self._mod.add(PassiveData(
            name,
            DisplayName=loca[f"{name}_DisplayName"],
            Description=loca[f"{name}_Description"],
            Icon="PassiveFeature_DraconicAncestry_Brass",
            Properties=["Highlighted"],
            Boosts=[
                "IgnoreResistance(Fire,Immune)",
                "IgnoreResistance(Fire,Resistant)",
                "IF(SpellDamageTypeIs(DamageType.Fire)):DamageBonus(max(0,CharismaModifier))",
            ],
        ))

        return name

    def _upgrade_everburn_blade(self) -> None:
        """Upgrade the Everburn Blade."""
        self.add(Weapon(
            "MAG_Fire_AlwaysDippedInFire_Greatsword",
            using="MAG_Fire_AlwaysDippedInFire_Greatsword",
            Boosts=["AC(1)"],
            DefaultBoosts=[
                "HiddenDuringCinematic()",
                "WeaponEnchantment(2)",
                "WeaponProperty(Magical)",
            ],
            PassivesOnEquip=[
                "MAG_ArcaneEnchantment_Passive",
                "MAG_Legendary_Chromatic_Heat_Passive",
            ],
            Rarity="Legendary",
        ))
    
    @cached_property
    def _level_1_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_1_spelllist"))
        self.add(SpellList(
            Name="Spells gained at Pyromancy level 1",
            Spells=[
                "Projectile_FireBolt",
                "Target_Command_Container",
                "Zone_BurningHands",
                "Shout_HellishRebuke",
            ],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_3_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_3_spelllist"))
        self.add(SpellList(
            Name="Spells gained at Pyromancy level 3",
            Spells=["Projectile_ScorchingRay"],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_5_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_5_spelllist"))
        self.add(SpellList(
            Name="Spells gained at Pyromancy level 5",
            Spells=["Projectile_Fireball", self._fire_walk],
            UUID=spelllist,
        ))
        return spelllist

    @cached_property
    def _level_7_spell_list(self) -> str:
        spelllist = str(self.make_uuid("level_7_spelllist"))
        self.add(SpellList(
            Name="Spells gained at Pyromancy level 7",
            Spells=["Wall_WallOfFire"],
            UUID=spelllist,
        ))
        return spelllist

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Pyromancy",
                         description="A replacer for Wild Magic Sorcery.")
        self._upgrade_everburn_blade()

    @class_description(CharacterClass.SORCERER)
    def sorcerer_description(self, class_description: ClassDescription) -> None:
        class_description.BaseHp = 10
        class_description.HpPerLevel = 6

    @class_description(CharacterClass.SORCERER_WILDMAGIC)
    def sorcerer_pyromancy_description(self, class_description: ClassDescription) -> None:
        class_description.DisplayName = self._pyromancy_display_name
        class_description.Description = self._pyromancy_description

    @tag("885f8675-e400-4d53-924d-6204ff1d9558")
    def wild_magic_tag(self, tag: Tags.Tags) -> None:
        tag.DisplayName = self._pyromancy_display_name
        tag.DisplayDescription = self._pyromancy_description

    @progression(CharacterClass.SORCERER, 1)
    def level_1_sorcerer(self, progression: Progression) -> None:
        selectors = progression.Selectors or []
        selectors = [selector for selector in selectors if not selector.startswith("SelectSkills")]
        selectors.extend([
            "SelectSkills(f974ebd6-3725-4b90-bb5c-2b647d41615d,6)",
            "SelectSkillsExpertise(f974ebd6-3725-4b90-bb5c-2b647d41615d,2)",
        ])
        progression.Selectors = selectors

    @progression(CharacterClass.SORCERER_WILDMAGIC, 1)
    def level_1(self, progression: Progression) -> None:
        progression.Boosts = [
            "Proficiency(LightArmor)",
            "Proficiency(MediumArmor)",
            "Proficiency(Shields)",
            "Proficiency(SimpleWeapons)",
            "Proficiency(MartialWeapons)",
            "Proficiency(MusicalInstrument)",
        ]
        progression.PassivesAdded = [
            self._eternal_flame,
            self._forged_in_flames,
        ]
        progression.Selectors = [
            f"AddSpells({self._level_1_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 3)
    def level_3(self, progression: Progression) -> None:
        progression.PassivesAdded = ["MAG_Fire_ArcaneAcuityOnFireDamage_Hat_Passive"]
        progression.Selectors = [
            f"AddSpells({self._level_3_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 4)
    def level_4(self, progression: Progression) -> None:
        progression.PassivesAdded = ["SculptSpells"]
        progression.Selectors = None

    @progression(CharacterClass.SORCERER_WILDMAGIC, 5)
    def level_5(self, progression: Progression) -> None:
        progression.PassivesAdded = None
        progression.Selectors = [
            f"AddSpells({self._level_5_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 6)
    def level_6(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._overheat]
        progression.Selectors = None

    @progression(CharacterClass.SORCERER_WILDMAGIC, 7)
    def level_7(self, progression: Progression) -> None:
        progression.PassivesAdded = ["ImprovedCritical"]
        progression.Selectors = [
            f"AddSpells({self._level_7_spell_list},,,,AlwaysPrepared)"
        ]

    @progression(CharacterClass.SORCERER_WILDMAGIC, 11)
    def level_11(self, progression: Progression) -> None:
        progression.PassivesAdded = [self._hellfire]
        progression.PassivesRemoved = [self._overheat]
        progression.Selectors = None


def main():
    pyromancy = Pyromancy()
    pyromancy.build()


if __name__ == "__main__":
    main()
