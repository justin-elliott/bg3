#!/usr/bin/env python3
"""
Generates files for the "Demigod" mod.
"""

import os

from functools import cached_property
from moddb import Bolster
from modtools.gamedata import PassiveData
from modtools.lsx.game import Origin
from modtools.mod import Mod


class Demigod(Mod):
    INITIATIVE_BONUS = 5
    MOVEMENT_BONUS = 4.5
    JUMP_BONUS = 2
    CARRY_BONUS = 5

    _bolster: str

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Demigod",
                         description="Adds the Demigod Origin.")
        self._bolster = Bolster(self).add_bolster()
        self.add_origin()

    @cached_property
    def divine_heritage(self) -> str:
        name = f"{self.get_prefix()}_DivineHeritage"
        display_name = f"{name}_DisplayName"
        description = f"{name}_Description"

        loca = self.get_localization()
        loca[display_name] = {"en": "Divine Heritage"}
        loca[description] = {"en": """
            Your <LSTag Tooltip="MovementSpeed">movement speed</LSTag> is increased by [1], your
            <LSTag Type="Spell" Tooltip="Projectile_Jump">Jump</LSTag> distance is increased by [2]%,
            and your carrying capacity is increased by [3]%. You are immune to critical hits, gain a +[4] bonus to
            Initiative, and can't be <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>.
            You are <LSTag Tooltip="ProficiencyBonus">Proficient</LSTag> in all
            <LSTag Tooltip="Dexterity">Dexterity</LSTag> and <LSTag Tooltip="Charisma">Charisma</LSTag> skills, and have
            proficiency in Constitution and Dexterity <LSTag Tooltip="SavingThrow">Saving Throws</LSTag>.
            """}

        self.add(PassiveData(
            name,
            DisplayName=loca[display_name],
            Description=loca[description],
            DescriptionParams=[
                f"Distance({self.MOVEMENT_BONUS})",
                (self.JUMP_BONUS - 1) * 100,
                (self.CARRY_BONUS - 1) * 100,
                self.INITIATIVE_BONUS
            ],
            Icon="Action_SightOfTheSeelie_BestialCommunion_Wildshape",
            Properties=["Highlighted"],
            Boosts=[
                f"UnlockSpell({self._bolster})",
                f"ActionResource(Movement,{self.MOVEMENT_BONUS},0)",
                f"JumpMaxDistanceMultiplier({self.JUMP_BONUS})",
                f"CarryCapacityMultiplier({self.CARRY_BONUS})",
                f"Initiative({self.INITIATIVE_BONUS})",
                "CriticalHit(AttackTarget,Success,Never)",
                "StatusImmunity(SURPRISED)",
                "ProficiencyBonus(SavingThrow,Constitution)",
                "ProficiencyBonus(SavingThrow,Dexterity)",
                "ProficiencyBonus(Skill,Acrobatics)",
                "ProficiencyBonus(Skill,SleightOfHand)",
                "ProficiencyBonus(Skill,Stealth)",
                "Proficiency(MusicalInstrument)",
                "ProficiencyBonus(Skill,Deception)",
                "ProficiencyBonus(Skill,Intimidation)",
                "ProficiencyBonus(Skill,Performance)",
                "ProficiencyBonus(Skill,Persuasion)",
            ],
        ))
        return name

    def add_origin(self):
        loca = self.get_localization()
        loca["Demigod_DisplayName"] = {"en": "Demigod"}
        loca["Demigod_Description"] = {"en": """
            You are descended from a divine being, granting you superior abilities.
            """}

        demigod_uuid = self.make_uuid("Demigod Origin")
        self.add(Origin(
            AppearanceLocked=False,
            AvailableInCharacterCreation=1,
            BodyShape=2,
            BodyType=2,
            DisplayName=loca["Demigod_DisplayName"],
            Description=loca["Demigod_Description"],
            Name="Demigod",
            Passives=[
                "DeathSavingThrows",
                "DevilsSight",
                self.divine_heritage,
            ],
            UUID=demigod_uuid,
            VoiceTableUUID="5ee56242-d07c-482e-9260-24529d1473a3",
            children=[
                Origin.AppearanceTags(Object="730e82f3-c067-44a4-985b-0dfe079d4fea"),
                Origin.ReallyTags(Object="264a6880-9a51-429c-a9fc-97f8952baf90"),
            ],
        ))


def main():
    demigod = Demigod()
    demigod.build()


if __name__ == "__main__":
    main()
