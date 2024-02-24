#!/usr/bin/env python3
"""
A decorator for tags replacement.
"""

from collections.abc import Callable
from modtools.lsx import Lsx
from modtools.lsx.game import Tags
from modtools.replacers.replacer import Replacer
from uuid import UUID


type TagBuilder = Callable[[Replacer, Tags.Tags], None]
type TagBuilderDict = dict[str, Tags.Tags]


_TAGS_PATH = "Shared.pak/Public/Shared/Tags"
_TAGS_DEV_PATH = "Shared.pak/Public/SharedDev/Tags"


def _load_tags(replacer: Replacer, uuids: list[str]) -> list[Tags.Tags]:
    """Load the game's Tags from the .pak cache."""
    tags: list[Tags.Tags] = []

    for uuid in uuids:
        try:
            tag_path = replacer.get_cache_path(f"{_TAGS_PATH}/{uuid}.lsf.lsx")
        except FileNotFoundError:
            tag_path = replacer.get_cache_path(f"{_TAGS_DEV_PATH}/{uuid}.lsf.lsx")

        tags_document: Tags = Lsx.load(tag_path)
        for child in tags_document.children:
            tags.append(child)

    return tags


def _make_builders(tag_builders: list[TagBuilder]) -> TagBuilderDict:
    """Make a TagBuilderDict from the decorated tag builders."""
    builders: TagBuilderDict = dict()

    for tag_builder in tag_builders:
        tags: list[str] = getattr(tag_builder, "tags")
        for tag in tags:
            builders[tag] = tag_builder

    return builders


def _update_tags(replacer: Replacer,
                 tags: list[Tags.Tags],
                 builders: TagBuilderDict):
    """Update tags that match our builder classes."""
    unused_builders = set(builders.keys())

    for tag in tags:
        if builder_fn := builders.get(tag.UUID):
            builder_fn(replacer, tag)
            unused_builders.remove(tag.UUID)

    if len(unused_builders) > 0:
        raise KeyError(f"Unmatched tag(s): {", ".join(sorted(unused_builders))}")


def _tag_builder(replacer: Replacer, tag_builders: list[TagBuilder]) -> None:
    """Update existing class descriptions."""
    builders = _make_builders(tag_builders)
    tags = _load_tags(replacer, builders.keys())

    _update_tags(replacer, tags, builders)

    # Save the updated tags
    for tag in tags:
        replacer.mod.add(tag)


def tag(uuid: str | UUID) -> TagBuilder:
    """A decorator mapping UUIDs to their tag builder function."""
    uuid = str(uuid)

    def decorate(fn: TagBuilder) -> TagBuilder:
        setattr(fn, "builder", _tag_builder)
        tags: list[str] = getattr(fn, "tags", [])
        tags.append(uuid)
        setattr(fn, "tags", tags)
        return fn

    return decorate
