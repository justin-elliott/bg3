#!/usr/bin/env python3
"""
Representation of .lsx types.
"""

from modtools.lsx.attributes import LsxAttribute, LsxBool, LsxList, LsxNumber, LsxString, LsxTranslation


class LsxType:
    """Attribute types as found in the .lsx 'type' XML attribute."""

    NONE = LsxString("None")
    UINT8 = LsxNumber("uint8")
    INT16 = LsxNumber("int16")
    UINT16 = LsxNumber("uint16")
    INT32 = LsxNumber("int32")
    UINT32 = LsxNumber("uint32")
    FLOAT = LsxNumber("float")
    DOUBLE = LsxNumber("double")
    IVEC2 = LsxString("ivec2")
    IVEC3 = LsxString("ivec3")
    IVEC4 = LsxString("ivec4")
    FVEC2 = LsxString("fvec2")
    FVEC3 = LsxString("fvec3")
    FVEC4 = LsxString("fvec4")
    MAT2X2 = LsxString("mat2x2")
    MAT3X3 = LsxString("mat3x3")
    MAT3X4 = LsxString("mat3x4")
    MAT4X3 = LsxString("mat4x3")
    MAT4X4 = LsxString("mat4x4")
    BOOL = LsxBool("bool")
    STRING = LsxString("string")
    PATH = LsxString("path")
    FIXEDSTRING = LsxString("FixedString")
    LSSTRING = LsxList("LSString")
    LSSTRING_VALUE = LsxString("LSString")  # A pseudo-type representing a single string value
    LSSTRING_COMMA = LsxList("LSString", ",")  # A pseudo-type representing comma-separated lists such as PassiveLists.
    UINT64 = LsxNumber("uint64")
    SCRATCHBUFFER = LsxString("ScratchBuffer")
    OLD_INT64 = LsxNumber("old_int64")
    INT8 = LsxNumber("int8")
    TRANSLATEDSTRING = LsxTranslation("TranslatedString")
    WSTRING = LsxString("WString")
    LSWSTRING = LsxList("LSWString")
    GUID = LsxString("guid")
    INT64 = LsxNumber("int64")
    TRANSLATEDFSSTRING = LsxString("TranslatedFSString")

    # Mapping of .lsx 'type' attribute names to LsxType names.
    BY_NAME: dict[str, str] = {}


LsxType.BY_NAME = {
    value._type_name: name for name, value in LsxType.__dict__.items()
    if isinstance(value, LsxAttribute)
    and name not in ("LSSTRING_VALUE", "LSSTRING_COMMA")  # Omit pseudo-types
}
