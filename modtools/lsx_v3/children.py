#!/usr/bin/env python3
"""
Representation of a collection of .lsx child nodes.
"""

from collections.abc import Iterable
from modtools.lsx_v3.node import LsxNode

import modtools.lsx_v3.detail as detail


class LsxChildren(detail.LsxChildren[LsxNode]):
    """A specialization of the LsxChildren generic class for LsxNode."""

    def __init__(self, children: Iterable[LsxNode] = [], *, types: Iterable[LsxNode] = (LsxNode,)):
        """Initialize the collection, optionally setting the children and allowed child types."""
        super().__init__(children, types=types)
