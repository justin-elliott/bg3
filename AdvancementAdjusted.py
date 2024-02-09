#!/usr/bin/env python3
"""
Generates files for the "Daisy" mod.
"""

import os

from modtools.mod import Mod

advancement = Mod(os.path.dirname(__file__),
                  author="justin-elliott",
                  name="AdvancementAdjusted",
                  description="Adjusts the experience needed to advance in levels.")

# The default advancement table for Baldur's Gate 3
default_advancement = {
    1: 300,
    2: 600,
    3: 1800,
    4: 3800,
    5: 6500,
    6: 8000,
    7: 9000,
    8: 12000,
    9: 14000,
    10: 20000,
    11: 24000,
    12: 30000,
}

double_advancement = {
    level: xp // 2 for level, xp in default_advancement.items()
}

advancement.set_xp_data(double_advancement)
advancement.build()
