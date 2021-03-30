# Copyright (C) 2018 Tetsuya Miura <miute.dev@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import array

from ._ffi_api import dlopen, ffi
from .freetype import FTFace

lib = dlopen(ffi, ['harfbuzz', 'libharfbuzz-0'])


def hb_shape(font, buffer, features=None):
    if features is None:
        features_length = 0
        hb_features = ffi.NULL
    else:
        features_length = len(features)
        hb_features = ffi.new('hb_feature_t[]',
                              [x.hb_feature[0] for x in features])
    lib.hb_shape(font.hb_font, buffer.hb_buffer, hb_features, features_length)


def hb_tag(c1, c2, c3, c4):
    return (ord(c1) << 24) | (ord(c2) << 16) | (ord(c3) << 8) | ord(c4)


def hb_version():
    major = ffi.new('unsigned int *')
    minor = ffi.new('unsigned int *')
    patch = ffi.new('unsigned int *')
    lib.hb_version(major, minor, patch)
    return major[0], minor[0], patch[0]


class HarfBuzz(object):
    version = hb_version()


class HBDirection(object):
    """Represents the 'hb_direction_t' data type."""

    HB_DIRECTION_INVALID = 0
    HB_DIRECTION_LTR = 4
    HB_DIRECTION_RTL = 5
    HB_DIRECTION_TTB = 6
    HB_DIRECTION_BTT = 7

    def __init__(self, hb_direction):
        self.direction = hb_direction

    def is_backward(self):
        return (self.direction & ~2) == 5

    def is_forward(self):
        return (self.direction & ~2) == 4

    def is_horizontal(self):
        return (self.direction & ~1) == 4

    def is_valid(self):
        return (self.direction & ~3) == 4

    def is_vertical(self):
        return (self.direction & ~1) == 6

    @staticmethod
    def fromstring(value):
        # 'ltr', 'rtl', 'ttb', 'btt'
        string = ffi.new('char[]', value.encode())
        direction = lib.hb_direction_from_string(string, -1)
        return HBDirection(direction)

    def reverse(self):
        direction = self.direction ^ 1
        return HBDirection(direction)

    def tostring(self):
        string = lib.hb_direction_to_string(self.direction)
        return ffi.string(string).decode()


class HBFace(object):
    """Represents the 'hb_face_t' data type."""

    def __init__(self, hb_face, reference=False):
        """Constructs a HBFace object.

        Arguments:
            hb_face (cdata): A pointer of C type <cdata 'hb_face_t *'>.
        """
        self._face = hb_face
        if reference:
            self.reference()

    def __del__(self):
        lib.hb_face_destroy(self._face)

    @property
    def hb_face(self):
        return self._face

    @staticmethod
    def create(blob, index=0):
        """Creates a HBFace object from a HBBlob object.

        Arguments:
            blob (HBBlob): A HBBlob object.
        Returns:
            HBFace: A new HBFace object.
        """
        face = lib.hb_face_create(blob.hb_blob, index)
        return HBFace(face)

    def get_glyph_count(self):
        glyph_count = lib.hb_face_get_glyph_count(self._face)
        return glyph_count

    def get_index(self):
        index = lib.hb_face_get_index(self._face)
        return index

    def get_upem(self):
        upem = lib.hb_face_get_upem(self._face)
        return upem

    def reference(self):
        lib.hb_face_reference(self._face)

    def reference_blob(self):
        lib.hb_face_reference_blob(self._face)

    def set_glyph_count(self, glyph_count):
        lib.hb_face_set_glyph_count(self._face, glyph_count)

    def set_index(self, index):
        lib.hb_face_set_index(self._face, index)

    def set_upem(self, upem):
        lib.hb_face_set_upem(self._face, upem)


class HBFTFace(HBFace):

    @staticmethod
    def create(face):
        """Creates a HBFTFace object from a FTFace object.

        Arguments:
            face (FTFace): A FTFace object.
        Returns:
            HBFTFace: A new HBFTFace object.
        """
        hb_face = lib.hb_ft_face_create(face.ft_face, ffi.NULL)
        return HBFTFace(hb_face)


class HBFeature(object):
    """Represents the 'hb_feature_t' data type."""

    def __init__(self, hb_feature):
        """Constructs a HBFeature object.

        Arguments:
            hb_feature (cdata): A pointer of C type <cdata 'hb_feature_t'>.
        """
        self._feature = hb_feature

    def __repr__(self):
        return (
            "('tag': {}, 'value': {}, 'start': {}, 'end': {})".format(
                self.tag, self.value, self.start, self.end))

    @property
    def end(self):
        return self._feature.end

    @end.setter
    def end(self, value):
        self._feature.end = value

    @property
    def hb_feature(self):
        return self._feature

    @property
    def start(self):
        return self._feature.start

    @start.setter
    def start(self, value):
        self._feature.start = value

    @property
    def tag(self):
        return self._feature.tag

    @tag.setter
    def tag(self, value):
        self._feature.tag = value

    @property
    def value(self):
        return self._feature.value

    @value.setter
    def value(self, value):
        self._feature.value = value

    @staticmethod
    def fromstring(string):
        feature = ffi.new('hb_feature_t *')
        result = lib.hb_feature_from_string(string.encode(),
                                            len(string),
                                            feature)
        if result == 0:
            return None
        return HBFeature(feature)

    def tostring(self):
        buf = ffi.new('char[128]')
        lib.hb_feature_to_string(self._feature,
                                 buf,
                                 len(buf))
        string = ffi.string(buf)
        return string.decode()


class HBFont(object):
    """Represents the 'hb_font_t' data type."""

    def __init__(self, hb_font, reference=False):
        """Constructs a HBFont object.

        Arguments:
            hb_font (cdata): A pointer of C type <cdata 'hb_font_t *'>.
        """
        self._font = hb_font
        if reference:
            self.reference()

    def __del__(self):
        lib.hb_font_destroy(self._font)

    @property
    def hb_font(self):
        """cdata: A pointer of C type <cdata 'hb_font_t *'>."""
        return self._font

    @staticmethod
    def create(face):
        """Creates a HBFont object from a HBFace object.

        Arguments:
            face (HBFace): A HBFace object.
        Returns:
            HBFont: A new HBFont object.
        """
        font = lib.hb_font_create(face.hb_face)
        return HBFont(font)

    def get_face(self):
        face = lib.hb_font_get_face(self._font)
        return HBFace(face)

    def get_glyph(self, unicode, variation_selector=0):
        glyph = ffi.new('hb_codepoint_t *')
        result = lib.hb_font_get_glyph(self._font,
                                       unicode,
                                       variation_selector,
                                       glyph)
        if result == 0:
            # raise RuntimeError('hb_font_get_glyph() failed.')
            return 0
        return glyph[0]

    def get_glyph_h_advance(self, glyph):
        position = lib.hb_font_get_glyph_h_advance(self.hb_font, glyph)
        return position

    def get_glyph_v_advance(self, glyph):
        position = lib.hb_font_get_glyph_v_advance(self.hb_font, glyph)
        return position

    def get_ppem(self):
        x_ppem = ffi.new('unsigned int *')
        y_ppem = ffi.new('unsigned int *')
        lib.hb_font_get_ppem(self._font, x_ppem, y_ppem)
        return x_ppem[0], y_ppem[0]

    def get_ptem(self):
        ptem = lib.hb_font_get_ptem(self._font)
        return ptem

    def get_scale(self):
        x_scale = ffi.new('int *')
        y_scale = ffi.new('int *')
        lib.hb_font_get_scale(self._font, x_scale, y_scale)
        return x_scale[0], y_scale[0]

    def reference(self):
        lib.hb_font_reference(self._font)

    def set_scale(self, x_scale, y_scale):
        lib.hb_font_set_scale(self._font, x_scale, y_scale)

    def set_face(self, face):
        lib.hb_font_set_face(self._font, face.hb_face)


class HBFTFont(HBFont):

    @staticmethod
    def create(face):
        """Creates a HBFTFont object from a FTFace object.

        Arguments:
            face (FTFace): A FTFace object.
        Returns:
            HBFTFont: A new HBFTFont object.
        """
        hb_font = lib.hb_ft_font_create(face.ft_face, ffi.NULL)
        return HBFTFont(hb_font)

    def get_face(self):
        face = lib.hb_ft_font_get_face(self._font)
        return FTFace(face, reference=True)

    def get_load_flags(self):
        load_flags = lib.hb_ft_font_get_load_flags(self._font)
        return load_flags

    def set_load_flags(self, load_flags):
        lib.hb_ft_font_set_load_flags(self._font, load_flags)


class HBLanguage(object):
    """Represents the 'hb_language_t' data type."""

    def __init__(self, language):
        self.language = language

    @staticmethod
    def fromstring(value):
        """Converts value representing an ISO 639 language code to the
        corresponding HBLanguage object.

        Arguments:
            value (str): An ISO 639 language code.
        Returns:
            HBLanguage: A new HBLanguage object.
        """
        string = ffi.new('char[]', value.encode())
        language = lib.hb_language_from_string(string, -1)
        return HBLanguage(language)

    @staticmethod
    def get_default():
        language = lib.hb_language_get_default()
        return HBLanguage(language)

    def tostring(self):
        string = lib.hb_language_to_string(self.language)
        return ffi.string(string).decode()


class HBOTFont(HBFont):

    @staticmethod
    def set_funcs(font):
        lib.hb_ot_font_set_funcs(font.hb_font)


class HBBlob(object):
    """Represents the 'hb_blob_t' data type."""

    HB_MEMORY_MODE_DUPLICATE = 1
    HB_MEMORY_MODE_READONLY = 2
    HB_MEMORY_MODE_WRITABLE = 3
    HB_MEMORY_MODE_READONLY_MAY_MAKE_WRITABLE = 4

    def __init__(self, hb_blob, reference=False):
        """Constructs a HBBlob object.

        Arguments:
            hb_blob (cdata): A pointer of C type <cdata 'hb_blob_t *'>.
        """
        self._blob = hb_blob
        if reference:
            self.reference()

    def __del__(self):
        lib.hb_blob_destroy(self._blob)

    @property
    def hb_blob(self):
        return self._blob

    @staticmethod
    def create(data, length=-1, mode=2):
        # bytes
        if length < 0:
            length = len(data)
        blob = lib.hb_blob_create(data,
                                  length,
                                  mode,
                                  ffi.NULL,
                                  ffi.NULL)
        return HBBlob(blob)

    def get_data(self):
        length = ffi.new('unsigned int *')
        data = lib.hb_blob_get_data(self._blob, length)
        buf = ffi.unpack(data, length[0])
        return buf

    def get_length(self):
        length = lib.hb_blob_get_length(self._blob)
        return length

    def reference(self):
        lib.hb_blob_reference(self._blob)


class HBBuffer(object):
    """Represents the 'hb_buffer_t' data type."""

    # CONTENT_TYPE_INVALID = 0
    # CONTENT_TYPE_UNICODE = 1
    # CONTENT_TYPE_GLYPHS = 2

    CLUSTER_LEVEL_MONOTONE_GRAPHEMES = 0
    CLUSTER_LEVEL_MONOTONE_CHARACTERS = 1
    CLUSTER_LEVEL_CHARACTERS = 2
    CLUSTER_LEVEL_DEFAULT = CLUSTER_LEVEL_MONOTONE_GRAPHEMES

    def __init__(self, hb_buffer, reference=False):
        """Constructs a HBBuffer object.

        Arguments:
            hb_buffer (cdata): A pointer of C type <cdata 'hb_buffer_t *'>.
        """
        self._buffer = hb_buffer
        if reference:
            self.reference()

    def __del__(self):
        lib.hb_buffer_destroy(self._buffer)

    @property
    def hb_buffer(self):
        """cdata: A pointer of C type <cdata 'hb_buffer_t *'>."""
        return self._buffer

    def add_utf16(self, text):
        arr = array.array('H', text.encode('utf-16'))
        buf = ffi.new('uint16_t[]', arr.tolist())
        lib.hb_buffer_add_utf16(self._buffer, buf, len(buf), 0, -1)

    def add_utf32(self, text):
        arr = array.array('I', text.encode('utf-32'))
        buf = ffi.new('uint32_t[]', arr.tolist())
        lib.hb_buffer_add_utf32(self._buffer, buf, len(buf), 0, -1)

    def add_utf8(self, text):
        buf = ffi.new('char[]', text.encode('utf-8'))
        lib.hb_buffer_add_utf8(self._buffer, buf, -1, 0, -1)

    @staticmethod
    def create():
        buffer = lib.hb_buffer_create()
        return HBBuffer(buffer)

    def clear_contents(self):
        lib.hb_buffer_clear_contents(self._buffer)

    def get_cluster_level(self):
        return lib.hb_buffer_get_cluster_level(self._buffer)

    def get_direction(self):
        direction = lib.hb_buffer_get_direction(self._buffer)
        return HBDirection(direction)

    def get_glyph_infos(self):
        length = ffi.new('unsigned int *')
        hb_glyph_infos = lib.hb_buffer_get_glyph_infos(self._buffer, length)
        infos = list()
        for i in range(0, length[0]):
            infos.append(HBGlyphInfo(hb_glyph_infos[i]))
        return infos

    def get_glyph_positions(self):
        length = ffi.new('unsigned int *')
        hb_glyph_positions = lib.hb_buffer_get_glyph_positions(
            self._buffer, length)
        positions = list()
        for i in range(0, length[0]):
            positions.append(HBGlyphPosition(hb_glyph_positions[i]))
        return positions

    def get_language(self):
        language = lib.hb_buffer_get_language(self._buffer)
        return HBLanguage(language)

    def get_length(self):
        length = lib.hb_buffer_get_length(self._buffer)
        return length

    def get_script(self):
        script = lib.hb_buffer_get_script(self._buffer)
        return HBScript(script)

    def guess_segment_properties(self):
        lib.hb_buffer_guess_segment_properties(self._buffer)

    def reset(self):
        lib.hb_buffer_reset(self._buffer)

    def reference(self):
        lib.hb_buffer_reference(self._buffer)

    def reverse(self):
        lib.hb_buffer_reverse(self._buffer)

    def reverse_clusters(self):
        lib.hb_buffer_reverse_clusters(self._buffer)

    def reverse_range(self, start, end):
        lib.hb_buffer_reverse_range(self._buffer, start, end)

    def set_cluster_level(self, cluster_level):
        lib.hb_buffer_set_cluster_level(self._buffer, cluster_level)

    def set_direction(self, direction):
        lib.hb_buffer_set_direction(self._buffer, direction.direction)

    def set_language(self, language):
        lib.hb_buffer_set_language(self._buffer, language.language)

    def set_script(self, script):
        lib.hb_buffer_set_script(self._buffer, script.script)

    def shape(self, font, features=None):
        hb_shape(font, self, features)


class HBGlyphInfo(object):
    def __init__(self, hb_glyph_info):
        self.codepoint = hb_glyph_info.codepoint
        self.mask = hb_glyph_info.mask
        self.cluster = hb_glyph_info.cluster

    def __repr__(self):
        return "('codepoint': {}, 'mask': {}, 'cluster': {})".format(
            hex(self.codepoint), self.mask, self.cluster)


class HBGlyphPosition(object):
    def __init__(self, hb_glyph_position):
        self.x_advance = hb_glyph_position.x_advance
        self.y_advance = hb_glyph_position.y_advance
        self.x_offset = hb_glyph_position.x_offset
        self.y_offset = hb_glyph_position.y_offset

    def __repr__(self):
        return (
            "('x_advance': {}, 'y_advance': {}"
            ", 'x_offset': {}, 'y_offset': {})".format(
                self.x_advance, self.y_advance,
                self.x_offset, self.y_offset))


class HBScript(object):
    """Represents the 'hb_script_t' data type.
    See also http://unicode.org/iso15924/.
    """

    HB_SCRIPT_COMMON = 1517910393  # 'Zyyy'
    HB_SCRIPT_INHERITED = 1516858984  # 'Zinh'
    HB_SCRIPT_UNKNOWN = 1517976186  # 'Zzzz'
    HB_SCRIPT_INVALID = 0

    def __init__(self, hb_script):
        self.script = hb_script

    @staticmethod
    def from_iso15924_tag(tag):
        # hb_tag_t to hb_script_t
        script = lib.hb_script_from_iso15924_tag(tag)
        return HBScript(script)

    @staticmethod
    def fromstring(value):
        """Converts value representing an ISO 15924 script code to the
        corresponding HBScript object.

        Arguments:
            value (str): An ISO 15924 script code.
        Returns:
            HBScript: A new HBScript object.
        """
        string = ffi.new('char[]', value.encode())
        script = lib.hb_script_from_string(string, -1)
        return HBScript(script)

    def get_horizontal_direction(self):
        direction = lib.hb_script_get_horizontal_direction(self.script)
        return HBDirection(direction)

    def to_iso15924_string(self):
        tag = self.to_iso15924_tag()
        string = ffi.new('char[4]')
        lib.hb_tag_to_string(tag, string)
        return ffi.string(string).decode()

    def to_iso15924_tag(self):
        tag = lib.hb_script_to_iso15924_tag(self.script)
        return tag
