#!/usr/bin/env python3
"""
Generates files for the "Demigod" mod.
"""

import os

from functools import cached_property
from modtools.gamedata import PassiveData
from modtools.lsx.game import Origin
from modtools.mod import Mod


class Demigod(Mod):
    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="Demigod",
                         description="Adds the Demigod Origin.")
        self.add_origin()

    @cached_property
    def divine_heritage(self) -> str:
        name = f"{self.get_prefix()}_DivineHeritage"
        display_name = f"{name}_DisplayName"
        description = f"{name}_Description"

        ability_bonus = 4
        initiative_bonus = 3
        movement_bonus = 4.5
        jump_bonus = 2
        carry_bonus = 4

        loca = self.get_localization()
        loca[display_name] = {"en": "Divine Heritage"}
        loca[description] = {"en": """
            Your abilities are increased by [1].
            Your <LSTag Tooltip="MovementSpeed">movement speed</LSTag> is increased by [2], your
            <LSTag Type="Spell" Tooltip="Projectile_Jump">Jump</LSTag> distance is increased by [3]%,
            and your carrying capacity is increased by [4]%.
            You gain a +[5] bonus to Initiative, and can't be
            <LSTag Type="Status" Tooltip="SURPRISED">Surprised</LSTag>.
            """}

        self.add(PassiveData(
            name,
            DisplayName=loca[display_name],
            Description=loca[description],
            DescriptionParams=[
                ability_bonus,
                f"Distance({movement_bonus})",
                (jump_bonus - 1) * 100,
                (carry_bonus - 1) * 100,
                initiative_bonus
            ],
            Icon="Action_SightOfTheSeelie_BestialCommunion_Wildshape",
            Properties=["Highlighted", "ForceShowInCC"],
            BoostContext=["OnEquip", "OnCreate"],
            Boosts=[
                f"Ability(Strength,{ability_bonus})",
                f"Ability(Dexterity,{ability_bonus})",
                f"Ability(Constitution,{ability_bonus})",
                f"Ability(Intelligence,{ability_bonus})",
                f"Ability(Wisdom,{ability_bonus})",
                f"Ability(Charisma,{ability_bonus})",
                f"ActionResource(Movement,{movement_bonus},0)",
                f"JumpMaxDistanceMultiplier({jump_bonus})",
                f"CarryCapacityMultiplier({carry_bonus})",
                f"Initiative({initiative_bonus})",
                "StatusImmunity(SURPRISED)",
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
                "HumanMilitia",
                "SuperiorDarkvision",
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
