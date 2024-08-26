#!/usr/bin/env python3
"""
LSX definitions.
"""

from modtools.lsx.children import LsxChildren
from modtools.lsx.document import LsxDocument
from modtools.lsx.node import LsxNode
from modtools.lsx import Lsx
from modtools.lsx.type import LsxType


class TooltipUpcastDescription(LsxNode):
    _id_ = "TooltipUpcastDescriptions"

    Name: str = LsxType.FIXEDSTRING
    Text: tuple[str, int] | str = LsxType.TRANSLATEDSTRING
    UUID: str = LsxType.GUID

    def __init__(self,
                 *,
                 Name: str = None,
                 Text: tuple[str, int] | str = None,
                 UUID: str = None):
        super().__init__(
            Name=Name,
            Text=Text,
            UUID=UUID,
        )


class TooltipUpcastDescriptions(LsxDocument):
    path = "Public/{folder}/TooltipExtras/TooltipUpcastDescriptions.lsx"
    children: LsxChildren = (TooltipUpcastDescription,)


Lsx.register(TooltipUpcastDescriptions)
