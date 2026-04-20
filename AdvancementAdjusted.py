#!/usr/bin/env python3
"""
Generates files for the "Daisy" mod.
"""

import os

from modtools.mod import Mod
from modtools.text import XPData


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
    # 13: 20000,
    # 14: 25000,
    # 15: 30000,
    # 16: 30000,
    # 17: 40000,
    # 18: 40000,
    # 19: 50000,
    # 20: 55000,
}

def multiply_advancement(factor: float) -> dict[int, int]:
    return {key: max(1, int(value * factor)) for key, value in default_advancement.items()}


advancement.add(XPData(multiply_advancement(0.75)))
advancement.build()
