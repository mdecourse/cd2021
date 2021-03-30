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


import copy
import math

import numpy as np

from ._ffi_api import dlopen, ffi
from .geometry.rect import DOMRect

lib = dlopen(ffi, ['freetype'])


def matrix2d(a, b, c, d):
    return np.array([[float(a), float(c)],
                     [float(b), float(d)]])


def ft_tag(c1, c2, c3, c4):
    return (ord(c1) << 24) | (ord(c2) << 16) | (ord(c3) << 8) | ord(c4)


def ft_tag_to_string(tag):
    string = chr(tag >> 24)
    string += chr((tag >> 16) & 0xff)
    string += chr((tag >> 8) & 0xff)
    string += chr(tag & 0xff)
    return string


class FTBitmap(object):
    """Represents the 'FT_Bitmap' data type."""

    def __init__(self, ft_bitmap):
        self._bitmap = ft_bitmap

    def __repr__(self):
        return (
            "('rows': {}, 'width': {}, 'pitch': {},"
            " 'num_grays': {}, 'pixel_mode': {})".format(
                self.rows, self.width, self.pitch,
                self.num_grays, self.pixel_mode))

    @property
    def buffer(self):
        # FIXME: FT_Bitmap.buffer should be aligned on 32-bit boundaries
        length = self.pitch * self.rows
        buf = ffi.unpack(self._bitmap.buffer, length)
        return buf

    @property
    def num_grays(self):
        return self._bitmap.num_grays

    @property
    def palette(self):
        """Not used currently."""
        raise NotImplementedError  # void*

    @property
    def palette_mode(self):
        """Not used currently."""
        # return self._bitmap.palette_mode
        raise NotImplementedError

    @property
    def pitch(self):
        return self._bitmap.pitch

    @property
    def pixel_mode(self):
        return self._bitmap.pixel_mode

    @property
    def rows(self):
        return self._bitmap.rows

    @property
    def width(self):
        return self._bitmap.width


class FTBitmapSize(object):
    """Represents the 'FT_Bitmap_Size' data type."""

    def __init__(self, ft_bitmap_size):
        self._bitmap_size = ft_bitmap_size

    def __repr__(self):
        return (
            "('height': {}, 'width': {}, 'size': {},"
            " 'x_ppem': {}, 'y_ppem': {})".format(
                self.height, self.width, self.size,
                self.x_ppem, self.y_ppem))

    @property
    def height(self):
        return self._bitmap_size.height

    @property
    def size(self):
        return self._bitmap_size.size

    @property
    def width(self):
        return self._bitmap_size.width

    @property
    def x_ppem(self):
        return self._bitmap_size.x_ppem

    @property
    def y_ppem(self):
        return self._bitmap_size.y_ppem


class FTCharMap(object):
    """Represents the 'FT_CharMap' data type."""

    def __init__(self, ft_charmap):
        self._charmap = ft_charmap

    def __repr__(self):
        return "('encoding': {}, 'encoding_id': {}, 'platform_id': {})".format(
            self.encoding,
            self.encoding_id,
            self.platform_id)

    @property
    def encoding(self):
        return self._charmap.encoding

    @property
    def encoding_id(self):
        return self._charmap.encoding_id

    @property
    def ft_charmap(self):
        return self._charmap

    @property
    def platform_id(self):
        return self._charmap.platform_id

    def get_charmap_index(self):
        index = lib.FT_Get_Charmap_Index(self._charmap)
        return index


class FTFace(object):
    """Represents the 'FT_Face' data type."""

    def __init__(self, ft_face, reference=False, _memory_base=None):
        self._face = ft_face
        self._memory_base = _memory_base  # keep a reference
        if reference:
            self.reference_face()

    def __del__(self):
        lib.FT_Done_Face(self._face)

    @property
    def ascender(self):
        return self._face.ascender

    @property
    def available_sizes(self):
        bitmap_sizes = list()
        for n in range(0, self.num_fixed_sizes):
            bitmap_sizes.append(FTBitmapSize(self._face.available_sizes[n]))
        return bitmap_sizes

    @property
    def bbox(self):
        bbox = self._face.bbox
        rect = DOMRect(bbox.xMin,
                       bbox.yMin,
                       bbox.xMax - bbox.xMin,
                       bbox.yMax - bbox.yMin)
        return rect

    @property
    def charmap(self):
        charmap = FTCharMap(self._face.charmap)
        return charmap

    @property
    def charmaps(self):
        charmaps = list()
        for n in range(0, self.num_charmaps):
            charmaps.append(FTCharMap(self._face.charmaps[n]))
        return charmaps

    @property
    def descender(self):
        return self._face.descender

    @property
    def face_index(self):
        return self._face.face_index

    @property
    def face_flags(self):
        return self._face.face_flags

    @property
    def family_name(self):
        family_name = ffi.string(self._face.family_name).decode()
        return family_name

    @property
    def ft_face(self):
        return self._face

    @property
    def glyph(self):
        glyph = FTGlyphSlot(self._face.glyph)
        return glyph

    @property
    def height(self):
        return self._face.height

    @property
    def max_advance_height(self):
        return self._face.max_advance_height

    @property
    def max_advance_width(self):
        return self._face.max_advance_width

    @property
    def num_charmaps(self):
        return self._face.num_charmaps

    @property
    def num_faces(self):
        return self._face.num_faces

    @property
    def num_fixed_sizes(self):
        return self._face.num_fixed_sizes

    @property
    def num_glyphs(self):
        return self._face.num_glyphs

    @property
    def size(self):
        size = FTSize(self._face.size)
        return size

    @property
    def style_flags(self):
        return self._face.style_flags

    @property
    def style_name(self):
        style_name = ffi.string(self._face.style_name).decode()
        return style_name

    @property
    def underline_position(self):
        return self._face.underline_position

    @property
    def underline_thickness(self):
        return self._face.underline_thickness

    @property
    def units_per_em(self):
        return self._face.units_per_EM

    def get_advance(self, glyph_index, load_flags):
        advance = ffi.new('FT_Fixed *')
        error = lib.FT_Get_Advance(self._face,
                                   glyph_index,
                                   load_flags,
                                   advance)
        if error:
            raise RuntimeError('FT_Get_Advance() failed: ' + hex(error))
        return advance[0]

    def get_char_index(self, char_code):
        if isinstance(char_code, str):
            char_code = ord(char_code)
        glyph_index = lib.FT_Get_Char_Index(self._face, char_code)
        return glyph_index

    def get_kerning(self, left_glyph, right_glyph, kern_mode=0):
        kerning = ffi.new('FT_Vector *')
        error = lib.FT_Get_Kerning(self._face,
                                   left_glyph,
                                   right_glyph,
                                   kern_mode,
                                   kerning)
        if error:
            raise RuntimeError('FT_Get_Kerning() failed: ' + hex(error))
        return kerning.x, kerning.y

    def has_color(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_COLOR) > 0

    def has_fixed_sizes(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_FIXED_SIZES) > 0

    def has_glyph_names(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_GLYPH_NAMES) > 0

    def has_horizontal(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_HORIZONTAL) > 0

    def has_kerning(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_KERNING) > 0

    def has_multiple_masters(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_MULTIPLE_MASTERS) > 0

    def has_vertical(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_VERTICAL) > 0

    def is_cid_keyed(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_CID_KEYED) > 0

    def is_fixed_width(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_FIXED_WIDTH) > 0

    def is_scalable(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_SCALABLE) > 0

    def is_sfnt(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_SFNT) > 0

    def is_tricky(self):
        return (self.face_flags & FreeType.FT_FACE_FLAG_TRICKY) > 0

    def load_char(self, char_code, load_flags=0):
        if isinstance(char_code, str):
            char_code = ord(char_code)
        error = lib.FT_Load_Char(self._face, char_code, load_flags)
        if error:
            raise RuntimeError('FT_Load_Char() failed: ' + hex(error))

    def load_glyph(self, glyph_index, load_flags=0):
        error = lib.FT_Load_Glyph(self._face, glyph_index, load_flags)
        if error:
            raise RuntimeError('FT_Load_Glyph() failed: ' + hex(error))

    @staticmethod
    def new_face(filename, index=0):
        face = ffi.new('FT_Face *')
        error = lib.FT_New_Face(FreeType.library.ft_library,
                                filename.encode(),
                                index,
                                face)
        if error:
            raise RuntimeError('FT_New_Face() failed: ' + hex(error))
        return FTFace(face[0])

    @staticmethod
    def new_memory_face(file_base, file_size=0, face_index=0):
        memory_base = ffi.new('FT_Byte[]', file_base)
        if file_size <= 0:
            file_size = len(file_base)
        face = ffi.new('FT_Face *')
        error = lib.FT_New_Memory_Face(FreeType.library.ft_library,
                                       memory_base,
                                       file_size,
                                       face_index,
                                       face)
        if error:
            raise RuntimeError('FT_New_Memory_Face() failed: ' + hex(error))
        return FTFace(face[0], _memory_base=memory_base)

    def reference_face(self):
        error = lib.FT_Reference_Face(self._face)
        if error:
            raise RuntimeError('FT_Reference_Face() failed: ' + hex(error))

    def request_size(self, size_request_type, width, height,
                     hori_resolution=0, vert_resolution=0):
        size_request = ffi.new('FT_Size_Request')
        size_request.type = size_request_type
        size_request.width = width
        size_request.height = height
        size_request.horiResolution = hori_resolution
        size_request.vertResolution = vert_resolution
        error = lib.FT_Request_Size(self._face, size_request)
        if error:
            raise RuntimeError('FT_Request_Size() failed: ' + hex(error))

    def select_charmap(self, encoding):
        error = lib.FT_Select_Charmap(self._face, encoding)
        if error:
            raise RuntimeError('FT_Select_Charmap() failed: ' + hex(error))

    def select_size(self, strike_index):
        error = lib.FT_Select_Size(self._face, strike_index)
        if error:
            raise RuntimeError('FT_Select_Size() failed: ' + hex(error))

    def set_char_size(self, char_width, char_height,
                      horz_resolution=0, vert_resolution=0):
        error = lib.FT_Set_Char_Size(self._face,
                                     char_width,
                                     char_height,
                                     horz_resolution,
                                     vert_resolution)
        if error:
            raise RuntimeError('FT_Set_Char_Size() failed: ' + hex(error))

    def set_charmap(self, charmap):
        error = lib.FT_Set_Charmap(self._face,
                                   charmap.ft_charmap)
        if error:
            raise RuntimeError('FT_Set_Charmap() failed: ' + hex(error))

    def set_pixel_sizes(self, pixel_width, pixel_height):
        error = lib.FT_Set_Pixel_Sizes(self._face,
                                       pixel_width,
                                       pixel_height)
        if error:
            raise RuntimeError('FT_Set_Pixel_Sizes() failed: ' + hex(error))


class FTGlyphMetrics(object):
    """Represents the 'FT_Glyph_Metrics' data type."""

    def __init__(self, ft_glyph_metrics):
        self._metrics = ft_glyph_metrics

    def __repr__(self):
        return (
            "('width': {}, 'height': {},"
            " 'hori_bearing_x': {}, 'hori_bearing_y': {},"
            " 'hori_advance': {},"
            " 'vert_bearing_x': {}, 'vert_bearing_y': {},"
            " 'vert_advance': {})".format(
                self.width, self.height,
                self.hori_bearing_x, self.hori_bearing_y, self.hori_advance,
                self.vert_bearing_x, self.vert_bearing_y, self.vert_advance))

    @property
    def height(self):
        return self._metrics.height

    @property
    def hori_advance(self):
        return self._metrics.horiAdvance

    @property
    def hori_bearing_x(self):
        return self._metrics.horiBearingX

    @property
    def hori_bearing_y(self):
        return self._metrics.horiBearingY

    @property
    def vert_advance(self):
        return self._metrics.vertAdvance

    @property
    def vert_bearing_x(self):
        return self._metrics.vertBearingX

    @property
    def vert_bearing_y(self):
        return self._metrics.vertBearingY

    @property
    def width(self):
        return self._metrics.width


class FTGlyphSlot(object):
    """Represents the 'FT_GlyphSlot' data type."""

    def __init__(self, ft_glyph_slot):
        self._slot = ft_glyph_slot

    def __repr__(self):
        return (
            "('metrics': {},"
            " 'linear_hori_advance': {}, 'linear_vert_advance': {},"
            " 'advance': {}, 'format': {}, 'bitmap': {},"
            " 'bitmap_left': {}, 'bitmap_top': {}, 'outline': {},"
            " 'lsb_delta': {}, 'rsb_delta': {})".format(
                repr(self.metrics),
                self.linear_hori_advance, self.linear_vert_advance,
                self.advance, self.format,
                repr(self.bitmap), self.bitmap_left, self.bitmap_top,
                self.outline, self.lsb_delta, self.rsb_delta))

    @property
    def advance(self):
        advance = self._slot.advance
        return advance.x, advance.y

    @property
    def bitmap(self):
        bitmap = FTBitmap(self._slot.bitmap)
        return bitmap

    @property
    def bitmap_left(self):
        return self._slot.bitmap_left

    @property
    def bitmap_top(self):
        return self._slot.bitmap_top

    @property
    def format(self):
        return self._slot.format

    @property
    def linear_hori_advance(self):
        return self._slot.linearHoriAdvance

    @property
    def linear_vert_advance(self):
        return self._slot.linearVertAdvance

    @property
    def lsb_delta(self):
        return self._slot.lsb_delta

    @property
    def metrics(self):
        metrics = FTGlyphMetrics(self._slot.metrics)
        return metrics

    @property
    def outline(self):
        outline = FTOutline(self._slot.outline)
        return outline

    @property
    def rsb_delta(self):
        return self._slot.rsb_delta

    def embolden(self):
        """[EXPERIMENTAL]"""
        lib.FT_GlyphSlot_Embolden(self._slot)

    def oblique(self):
        """[EXPERIMENTAL]"""
        lib.FT_GlyphSlot_Oblique(self._slot)

    def render_glyph(self, render_mode):
        error = lib.FT_Render_Glyph(self._slot, render_mode)
        if error:
            raise RuntimeError('FT_Render_Glyph() failed: ' + hex(error))


class FTLibrary(object):
    def __init__(self):
        self._library = None
        library = ffi.new('FT_Library *')
        error = lib.FT_Init_FreeType(library)
        if error:
            raise RuntimeError(
                'Cannot initialize a FreeType library object: ' + hex(error))
        self._library = library[0]

        major = ffi.new('FT_Int *')
        minor = ffi.new('FT_Int *')
        patch = ffi.new('FT_Int *')
        lib.FT_Library_Version(self._library, major, minor, patch)
        self._version = major[0], minor[0], patch[0]

    def __del__(self):
        if self._library is not None:
            lib.FT_Done_FreeType(self._library)

    @property
    def ft_library(self):
        return self._library

    @property
    def version(self):
        return self._version


class FreeType(object):
    # freetype/freetype.h
    FT_SIZE_REQUEST_TYPE_NOMINAL = 0
    FT_SIZE_REQUEST_TYPE_REAL_DIM = 1
    FT_SIZE_REQUEST_TYPE_BBOX = 2
    FT_SIZE_REQUEST_TYPE_CELL = 3
    FT_SIZE_REQUEST_TYPE_SCALES = 4
    FT_SIZE_REQUEST_TYPE_MAX = 5

    FT_ENCODING_NONE = 0
    FT_ENCODING_MS_SYMBOL = 1937337698
    FT_ENCODING_UNICODE = 1970170211
    FT_ENCODING_SJIS = 1936353651
    FT_ENCODING_PRC = 1734484000
    FT_ENCODING_BIG5 = 1651074869
    FT_ENCODING_WANSUNG = 2002873971
    FT_ENCODING_JOHAB = 1785686113
    FT_ENCODING_ADOBE_STANDARD = 1094995778
    FT_ENCODING_ADOBE_EXPERT = 1094992453
    FT_ENCODING_ADOBE_CUSTOM = 1094992451
    FT_ENCODING_ADOBE_LATIN_1 = 1818326065
    FT_ENCODING_OLD_LATIN_2 = 1818326066
    FT_ENCODING_APPLE_ROMAN = 1634889070

    FT_RENDER_MODE_NORMAL = 0
    FT_RENDER_MODE_LIGHT = 1
    FT_RENDER_MODE_MONO = 2
    FT_RENDER_MODE_LCD = 3
    FT_RENDER_MODE_LCD_V = 4
    FT_RENDER_MODE_MAX = 5

    FT_LOAD_DEFAULT = 0
    FT_LOAD_NO_SCALE = 1 << 0
    FT_LOAD_NO_HINTING = 1 << 1
    FT_LOAD_RENDER = 1 << 2
    FT_LOAD_NO_BITMAP = 1 << 3
    FT_LOAD_VERTICAL_LAYOUT = 1 << 4
    FT_LOAD_FORCE_AUTOHINT = 1 << 5
    FT_LOAD_CROP_BITMAP = 1 << 6
    FT_LOAD_PEDANTIC = 1 << 7
    FT_LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH = 1 << 9
    FT_LOAD_NO_RECURSE = 1 << 10
    FT_LOAD_IGNORE_TRANSFORM = 1 << 11
    FT_LOAD_MONOCHROME = 1 << 12
    FT_LOAD_LINEAR_DESIGN = 1 << 13
    FT_LOAD_NO_AUTOHINT = 1 << 15
    FT_LOAD_COLOR = 1 << 20
    FT_LOAD_COMPUTE_METRICS = 1 << 21
    FT_LOAD_BITMAP_METRICS_ONLY = 1 << 22

    FT_LOAD_TARGET_NORMAL = (FT_RENDER_MODE_NORMAL & 15) << 16
    FT_LOAD_TARGET_LIGHT = (FT_RENDER_MODE_LIGHT & 15) << 16
    FT_LOAD_TARGET_MONO = (FT_RENDER_MODE_MONO & 15) << 16
    FT_LOAD_TARGET_LCD = (FT_RENDER_MODE_LCD & 15) << 16
    FT_LOAD_TARGET_LCD_V = (FT_RENDER_MODE_LCD_V & 15) << 16

    FT_KERNING_DEFAULT = 0
    FT_KERNING_UNFITTED = 1
    FT_KERNING_UNSCALED = 2

    FT_FACE_FLAG_SCALABLE = 1 << 0
    FT_FACE_FLAG_FIXED_SIZES = 1 << 1
    FT_FACE_FLAG_FIXED_WIDTH = 1 << 2
    FT_FACE_FLAG_SFNT = 1 << 3
    FT_FACE_FLAG_HORIZONTAL = 1 << 4
    FT_FACE_FLAG_VERTICAL = 1 << 5
    FT_FACE_FLAG_KERNING = 1 << 6
    FT_FACE_FLAG_FAST_GLYPHS = 1 << 7
    FT_FACE_FLAG_MULTIPLE_MASTERS = 1 << 8
    FT_FACE_FLAG_GLYPH_NAMES = 1 << 9
    FT_FACE_FLAG_EXTERNAL_STREAM = 1 << 10
    FT_FACE_FLAG_HINTER = 1 << 11
    FT_FACE_FLAG_CID_KEYED = 1 << 12
    FT_FACE_FLAG_TRICKY = 1 << 13
    FT_FACE_FLAG_COLOR = 1 << 14

    FT_STYLE_FLAG_ITALIC = 1 << 0
    FT_STYLE_FLAG_BOLD = 1 << 1

    # freetype/ftimage.h
    FT_PIXEL_MODE_NONE = 0
    FT_PIXEL_MODE_MONO = 1
    FT_PIXEL_MODE_GRAY = 2
    FT_PIXEL_MODE_GRAY2 = 3
    FT_PIXEL_MODE_GRAY4 = 4
    FT_PIXEL_MODE_LCD = 5
    FT_PIXEL_MODE_LCD_V = 6
    FT_PIXEL_MODE_BGRA = 7
    FT_PIXEL_MODE_MAX = 8

    # (ord(x1) << 24) | (ord(x2) << 16) | (ord(x3) << 8) | ord(x4)
    FT_GLYPH_FORMAT_NONE = 0
    FT_GLYPH_FORMAT_COMPOSITE = 1668246896  # 0x636f6d70
    FT_GLYPH_FORMAT_BITMAP = 1651078259  # 0x62697473
    FT_GLYPH_FORMAT_OUTLINE = 1869968492  # 0x6f75746c
    FT_GLYPH_FORMAT_PLOTTER = 1886154612  # 0x706c6f74

    FT_OUTLINE_NONE = 0x0
    FT_OUTLINE_OWNER = 0x1
    FT_OUTLINE_EVEN_ODD_FILL = 0x2
    FT_OUTLINE_REVERSE_FILL = 0x4
    FT_OUTLINE_IGNORE_DROPOUTS = 0x8
    FT_OUTLINE_SMART_DROPOUTS = 0x10
    FT_OUTLINE_INCLUDE_STUBS = 0x20
    FT_OUTLINE_HIGH_PRECISION = 0x100
    FT_OUTLINE_SINGLE_PASS = 0x200

    # freetype/ftoutln.h
    FT_ORIENTATION_TRUETYPE = 0
    FT_ORIENTATION_POSTSCRIPT = 1
    FT_ORIENTATION_FILL_RIGHT = FT_ORIENTATION_TRUETYPE
    FT_ORIENTATION_FILL_LEFT = FT_ORIENTATION_POSTSCRIPT
    FT_ORIENTATION_NONE = 2

    # freetype/ttnameid.h
    TT_PLATFORM_APPLE_UNICODE = 0
    TT_PLATFORM_MACINTOSH = 1
    TT_PLATFORM_MICROSOFT = 3
    TT_PLATFORM_CUSTOM = 4
    TT_PLATFORM_ADOBE = 7  # artificial

    TT_APPLE_ID_DEFAULT = 0  # Unicode 1.0
    TT_APPLE_ID_UNICODE_1_1 = 1  # specify Hangul at U+34xx
    TT_APPLE_ID_UNICODE_2_0 = 3  # or later
    TT_APPLE_ID_UNICODE_32 = 4  # 2.0 or later, full repertoire
    TT_APPLE_ID_VARIANT_SELECTOR = 5  # variation selector data
    TT_APPLE_ID_FULL_UNICODE = 6  # used with type 13 cmaps

    TT_MS_ID_SYMBOL_CS = 0
    TT_MS_ID_UNICODE_CS = 1
    TT_MS_ID_SJIS = 2
    TT_MS_ID_PRC = 3
    TT_MS_ID_BIG_5 = 4
    TT_MS_ID_WANSUNG = 5
    TT_MS_ID_JOHAB = 6
    TT_MS_ID_UCS_4 = 10

    library = FTLibrary()


class FTOutline(object):
    """Represents the 'FT_Outline' data type."""

    def __init__(self, ft_outline):
        self._outline = ft_outline

    def __repr__(self):
        return (
            "('n_contours': {}, 'n_points': {}, 'flags': {})".format(
                self.n_contours, self.n_points, self.flags))

    @property
    def contours(self):
        contours = list()
        for n in range(0, self.n_contours):
            contours.append(self._outline.contours[n])
        return contours

    @property
    def flags(self):
        return self._outline.flags

    @property
    def n_contours(self):
        return self._outline.n_contours

    @property
    def n_points(self):
        return self._outline.n_points

    @property
    def points(self):
        points = list()
        for n in range(0, self.n_points):
            point = self._outline.points[n]
            points.append((point.x, point.y))
        return points

    @property
    def tags(self):
        tags = ffi.string(self._outline.tags)
        return list(tags)

    def decompose(self, move_to_func, line_to_func, conic_to_func,
                  cubic_to_func, shift=0, delta=0, user=None):
        @ffi.callback('int(FT_Vector *, void *)')
        def _move_to(to, _):
            move_to_func(to.x, to.y, user)
            return 0

        @ffi.callback('int(FT_Vector *, void *)')
        def _line_to(to, _):
            line_to_func(to.x, to.y, user)
            return 0

        @ffi.callback('int(FT_Vector *, FT_Vector *, void *)')
        def _conic_to(control, to, _):
            conic_to_func(control.x, control.y, to.x, to.y, user)
            return 0

        @ffi.callback('int(FT_Vector *, FT_Vector *, FT_Vector *, void *)')
        def _cubic_to(control1, control2, to, _):
            cubic_to_func(control1.x, control1.y,
                          control2.x, control2.y,
                          to.x, to.y,
                          user)
            return 0

        outline_funcs = ffi.new('FT_Outline_Funcs *')
        outline_funcs.move_to = _move_to
        outline_funcs.line_to = _line_to
        outline_funcs.conic_to = _conic_to
        outline_funcs.cubic_to = _cubic_to
        outline_funcs.shift = shift
        outline_funcs.delta = delta
        error = lib.FT_Outline_Decompose(ffi.addressof(self._outline),
                                         outline_funcs,
                                         ffi.NULL)
        if error:
            raise RuntimeError('FT_Outline_Decompose() failed: ' + hex(error))

    def get_bbox(self):
        bbox = ffi.new('FT_BBox *')
        error = lib.FT_Outline_Get_BBox(ffi.addressof(self._outline), bbox)
        if error:
            raise RuntimeError('FT_Outline_Get_BBox() failed: ' + hex(error))
        rect = DOMRect(bbox.xMin,
                       bbox.yMin,
                       bbox.xMax - bbox.xMin,
                       bbox.yMax - bbox.yMin)
        return rect

    def get_cbox(self):
        bbox = ffi.new('FT_BBox *')
        error = lib.FT_Outline_Get_CBox(ffi.addressof(self._outline), bbox)
        if error:
            raise RuntimeError('FT_Outline_Get_CBox() failed: ' + hex(error))
        rect = DOMRect(bbox.xMin,
                       bbox.yMin,
                       bbox.xMax - bbox.xMin,
                       bbox.yMax - bbox.yMin)
        return rect

    def get_orientation(self):
        orientation = lib.FT_Outline_Get_Orientation(
            ffi.addressof(self._outline))
        return orientation

    def reverse(self):
        error = lib.FT_Outline_Reverse(ffi.addressof(self._outline))
        if error:
            raise RuntimeError('FT_Outline_Reverse() failed: ' + hex(error))

    def translate(self, x_offset, y_offset):
        lib.FT_Outline_Translate(ffi.addressof(self._outline),
                                 x_offset,
                                 y_offset)

    def transform(self, matrix):
        lib.FT_Outline_Transform(ffi.addressof(self._outline),
                                 matrix.ft_matrix)


class FTSize(object):
    """Represents the 'FT_Size' data type."""

    def __init__(self, ft_size):
        self._size = ft_size

    def __repr__(self):
        return "('metrics': {})".format(repr(self.metrics))

    @property
    def metrics(self):
        metrics = FTSizeMetrics(self._size.metrics)
        return metrics


class FTSizeMetrics(object):
    """Represents the 'FT_Size_Metrics' data type."""

    def __init__(self, ft_size_metrics):
        self._metrics = ft_size_metrics

    def __repr__(self):
        return (
            "('x_ppem': {}, 'y_ppem': {},"
            " 'x_scale': {}, 'y_scale': {},"
            " 'ascender': {}, 'descender': {},"
            " 'height': {}, 'max_advance': {})".format(
                self.x_ppem, self.y_ppem, self.x_scale, self.y_scale,
                self.ascender, self.descender, self.height, self.max_advance))

    @property
    def ascender(self):
        return self._metrics.ascender

    @property
    def descender(self):
        return self._metrics.descender

    @property
    def height(self):
        return self._metrics.height

    @property
    def max_advance(self):
        return self._metrics.max_advance

    @property
    def x_ppem(self):
        return self._metrics.x_ppem

    @property
    def x_scale(self):
        return self._metrics.x_scale

    @property
    def y_ppem(self):
        return self._metrics.y_ppem

    @property
    def y_scale(self):
        return self._metrics.y_scale


class FTMatrix(object):
    """Represents a 2x2 matrix."""

    def __init__(self, ft_matrix=None):
        """Constructs a FTMatrix object.

        Arguments:
            ft_matrix (cdata, optional): A pointer of C type
                <cdata 'FT_Matrix *'>.
        """
        if ft_matrix is None:
            xx = 1.0
            xy = 0
            yx = 0
            yy = 1.0
        else:
            xx = ft_matrix.xx / 0x10000
            xy = ft_matrix.xy / 0x10000
            yx = ft_matrix.yx / 0x10000
            yy = ft_matrix.yy / 0x10000
        self._matrix = matrix2d(xx, yx, xy, yy)

    def __eq__(self, other):
        if not isinstance(other, FTMatrix):
            return NotImplemented
        return (self._matrix == other._matrix).all()

    def __imul__(self, other):
        if not isinstance(other, FTMatrix):
            return NotImplemented
        self.multiply_self(other)
        return self

    def __mul__(self, other):
        if not isinstance(other, FTMatrix):
            return NotImplemented
        m = copy.deepcopy(self)
        m.multiply_self(other)
        return m

    def __repr__(self):
        return '<{}.{} object at {} {}>'.format(
            type(self).__module__, type(self).__name__, hex(id(self)),
            self._matrix.tolist())

    @property
    def a(self):
        """float: The a component of the matrix.
        Equivalent to FTMatrix.xx.
        """
        return self._matrix[0, 0]

    @a.setter
    def a(self, value):
        self._matrix[0, 0] = float(value)

    @property
    def b(self):
        """float: The b component of the matrix.
        Equivalent to FTMatrix.yx.
        """
        return self._matrix[0, 1]

    @b.setter
    def b(self, value):
        self._matrix[0, 1] = float(value)

    @property
    def c(self):
        """float: The c component of the matrix.
        Equivalent to FTMatrix.xy.
        """
        return self._matrix[1, 0]

    @c.setter
    def c(self, value):
        self._matrix[1, 0] = float(value)

    @property
    def d(self):
        """float: The d component of the matrix.
        Equivalent to FTMatrix.yy.
        """
        return self._matrix[1, 1]

    @d.setter
    def d(self, value):
        self._matrix[1, 1] = float(value)

    @property
    def ft_matrix(self):
        """cdata: The current matrix."""
        matrix = ffi.new('FT_Matrix *')
        matrix.xx = int(self._matrix[0, 0] * 0x10000)
        matrix.xy = int(self._matrix[0, 1] * 0x10000)
        matrix.yx = int(self._matrix[1, 0] * 0x10000)
        matrix.yy = int(self._matrix[1, 1] * 0x10000)
        return matrix

    @property
    def matrix(self):
        """numpy.array: The current matrix."""
        return self._matrix

    @property
    def xx(self):
        """float: The xx component of the matrix.
        Equivalent to FTMatrix.a.
        """
        return self._matrix[0, 0]

    @xx.setter
    def xx(self, value):
        self._matrix[0, 0] = float(value)

    @property
    def xy(self):
        """float: The xy component of the matrix.
        Equivalent to FTMatrix.c.
        """
        return self._matrix[0, 1]

    @xy.setter
    def xy(self, value):
        self._matrix[0, 1] = float(value)

    @property
    def yx(self):
        """float: The yx component of the matrix.
        Equivalent to FTMatrix.b.
        """
        return self._matrix[1, 0]

    @yx.setter
    def yx(self, value):
        self._matrix[1, 0] = float(value)

    @property
    def yy(self):
        """float: The yy component of the matrix.
        Equivalent to FTMatrix.d.
        """
        return self._matrix[1, 1]

    @yy.setter
    def yy(self, value):
        self._matrix[1, 1] = float(value)

    def clear(self):
        """Sets the matrix [1 0 0 1].

        Returns:
            FTMatrix: Returns itself.
        """
        self._matrix = matrix2d(1, 0, 0, 1)
        return self

    def flip_x(self):
        """Post-multiplies the transformation [-1 0 0 1] on the current matrix
        and returns the resulting matrix.
        The current matrix is not modified.

        Returns:
            FTMatrix: The resulting matrix.
        """
        m = copy.deepcopy(self)
        b = matrix2d(-1, 0, 0, 1)
        m._matrix = np.dot(m._matrix, b)
        return m

    def flip_y(self):
        """Post-multiplies the transformation [1 0 0 -1] on the current matrix
        and returns the resulting matrix.
        The current matrix is not modified.

        Returns:
            FTMatrix: The resulting matrix.
        """
        m = copy.deepcopy(self)
        b = matrix2d(1, 0, 0, -1)
        m._matrix = np.dot(m._matrix, b)
        return m

    @staticmethod
    def from_float_array(values):
        """Creates a new FTMatrix object from a list of elements of the
        matrix, and returns it.

        Arguments:
            values (list[float, ...]): A list of elements of the matrix.
        Returns:
            FTMatrix: A new FTMatrix object.
        """
        m = FTMatrix()
        a, c, b, d = values
        m._matrix = matrix2d(a, b, c, d)
        return m

    def inverse(self):
        """Returns the inverse matrix.
        The current matrix is not modified.

        Returns:
            FTMatrix: The resulting matrix.
        """
        m = copy.deepcopy(self)
        m.invert_self()
        return m

    def invert_self(self):
        """Inverts the current matrix.

        Returns:
            FTMatrix: Returns itself.
        """
        self._matrix = np.linalg.inv(self._matrix)
        return self

    def multiply(self, other):
        """Post-multiplies the other matrix on the current matrix and returns
        the resulting matrix.
        The current matrix is not modified.

        Arguments:
            other (FTMatrix): A matrix to be multiplied.
        Returns:
            FTMatrix: The resulting matrix.
        """
        m = self * other
        return m

    def multiply_self(self, other):
        """Post-multiplies the other matrix on the current matrix.

        Arguments:
            other (FTMatrix): A matrix to be multiplied.
        Returns:
            FTMatrix: Returns itself.
        """
        self._matrix = np.dot(self._matrix, other._matrix)
        return self

    def rotate(self, angle):
        """Post-multiplies a rotation transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            angle (float): The rotation angle in degrees.
        Returns:
            FTMatrix: The resulting matrix.
        """
        m = copy.deepcopy(self)
        m.rotate_self(angle)
        return m

    def rotate_self(self, angle):
        """Post-multiplies a rotation transformation on the current matrix.

        Arguments:
            angle (float): The rotation angle in degrees.
        Returns:
            FTMatrix: Returns itself.
        """
        cos_a = math.cos(math.radians(angle))
        sin_a = math.sin(math.radians(angle))
        b = matrix2d(cos_a, -sin_a, sin_a, cos_a)
        self._matrix = np.dot(self._matrix, b)
        return self

    def scale(self, scale_x, scale_y=None):
        """Post-multiplies a non-uniform scale transformation on the current
        matrix and returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            scale_x (float): The scale amount in X.
            scale_y (float, optional): The scale amount in Y.
        Returns:
            FTMatrix: The resulting matrix.
        """
        m = copy.deepcopy(self)
        m.scale_self(scale_x, scale_y)
        return m

    def scale_self(self, scale_x, scale_y=None):
        """Post-multiplies a non-uniform scale transformation on the current
        matrix.

        Arguments:
            scale_x (float): The scale amount in X.
            scale_y (float, optional): The scale amount in Y.
        Returns:
            FTMatrix: Returns itself.
        """
        if scale_y is None:
            scale_y = scale_x
        b = matrix2d(scale_x, 0, 0, scale_y)
        self._matrix = np.dot(self._matrix, b)
        return self

    def skew_x(self, angle):
        """Post-multiplies a skewX transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            FTMatrix: The resulting matrix.
        """
        m = copy.deepcopy(self)
        m.skew_x_self(angle)
        return m

    def skew_x_self(self, angle):
        """Post-multiplies a skewX transformation on the current matrix.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            FTMatrix: Returns itself.
        """
        b = matrix2d(1, 0, -math.tan(math.radians(angle)), 1)
        self._matrix = np.dot(self._matrix, b)
        return self

    def skew_y(self, angle):
        """Post-multiplies a skewY transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            FTMatrix: The resulting matrix.
        """
        m = copy.deepcopy(self)
        m.skew_y_self(angle)
        return m

    def skew_y_self(self, angle):
        """Post-multiplies a skewY transformation on the current matrix.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            FTMatrix: Returns itself.
        """
        b = matrix2d(1, -math.tan(math.radians(angle)), 0, 1)
        self._matrix = np.dot(self._matrix, b)
        return self

    def to_float_array(self):
        return [self.a, self.b, self.c, self.d]

    def tolist(self):
        return self.to_float_array()
