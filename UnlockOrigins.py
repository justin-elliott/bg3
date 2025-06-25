#!/usr/bin/env python3
"""
Generates files for the "UnlockOrigins" mod.
"""

import os

from modtools.lsx.game import Origin
from modtools.replacers import (
    origin,
    Replacer,
)


class UnlockOrigins(Replacer):
    @origin("Astarion")
    @origin("Gale")
    @origin("Karlach")
    @origin("Laezel")
    @origin("Shadowheart")
    @origin("Wyll")
    def unlock_class(self, origin: Origin) -> None:
        origin.LockClass = False

    @origin("Astarion")
    @origin("Gale")
    @origin("Karlach")
    @origin("Laezel")
    @origin("Shadowheart")
    @origin("Wyll")
    def unlock_background(self, origin: Origin) -> None:
        self.mod.add(Origin(
            AppearanceLocked=origin.AppearanceLocked,
            AvailableInCharacterCreation=origin.AvailableInCharacterCreation,
            BackgroundUUID=None,
            BodyShape=origin.BodyShape,
            BodyType=origin.BodyType,
            ClassEquipmentOverride=origin.ClassEquipmentOverride,
            ClassUUID=origin.ClassUUID,
            CloseUpA=origin.CloseUpA,
            CloseUpB=origin.CloseUpB,
            DefaultsTemplate=origin.DefaultsTemplate,
            Description=origin.Description,
            DisplayName=origin.DisplayName,
            ExcludesOriginUUID=origin.ExcludesOriginUUID,
            GlobalTemplate=origin.GlobalTemplate,
            GodUUID=origin.GodUUID,
            IntroDialogUUID=origin.IntroDialogUUID,
            LockBody=origin.LockBody,
            LockClass=False,
            LockRace=origin.LockRace,
            Name=origin.Name,
            Passives=origin.Passives,
            RaceUUID=origin.RaceUUID,
            SubClassUUID=origin.SubClassUUID,
            SubRaceUUID=origin.SubRaceUUID,
            UUID=self.make_uuid(origin.Name),
            Unique=origin.Unique,
            VoiceTableUUID=origin.VoiceTableUUID,
            children=origin.children,
        ))

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="UnlockOrigins",
                         description="Unlocks background and class for origin characters.")


def main():
    unlock_origins = UnlockOrigins()
    unlock_origins.build()


if __name__ == "__main__":
    main()
