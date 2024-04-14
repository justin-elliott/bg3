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
    def unlock_origins(self, origin: Origin) -> None:
        origin.BackgroundUUID = None
        origin.LockClass = None
        origin.LockRace = None

    def __init__(self):
        super().__init__(os.path.dirname(__file__),
                         author="justin-elliott",
                         name="UnlockOrigins",
                         description="Unlocks background, class, and race for origin characters.")


def main():
    unlock_origins = UnlockOrigins()
    unlock_origins.build()


if __name__ == "__main__":
    main()
