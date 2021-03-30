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


import os.path
import re
import subprocess
from collections.abc import Iterator, Reversible
from ctypes.util import find_library

from cffi import FFI

from ._ffi_api import dlopen

_lib_names = ['icuuc']
_icu_min_required_version = 4
ffi = FFI()
lib = dlopen(ffi, _lib_names)

_api = r"""
/*
 * ICU 60.2
 */
/* ---- umachine.h ---- */
typedef char16_t UChar;
typedef int8_t UBool;

/* ---- utypes.h ---- */
typedef enum UErrorCode {
    U_ZERO_ERROR = 0,
} UErrorCode;

const char *
u_errorName${modifier}(UErrorCode code);

/* ---- uloc.h ---- */
typedef enum {
  ULOC_ACTUAL_LOCALE    = 0,
  ULOC_VALID_LOCALE    = 1,
} ULocDataLocaleType;

const char*
uloc_getDefault${modifier}(void);

int32_t
uloc_getLanguage${modifier}(
    const char*    localeID,
    char* language,
    int32_t languageCapacity,
    UErrorCode* err);

/* ICU 2.8 */
int32_t
uloc_getScript${modifier}(
    const char*    localeID,
    char* script,
    int32_t scriptCapacity,
    UErrorCode* err);

/* ICU 54
UBool
uloc_isRightToLeft${modifier}(const char *locale);
*/

typedef enum {
  ULOC_LAYOUT_LTR   = 0,  /* left-to-right. */
} ULayoutType;

/* ICU 4.0 */
ULayoutType
uloc_getCharacterOrientation${modifier}(
    const char* localeId,
    UErrorCode *status);

/* ICU 4.0 */
ULayoutType
uloc_getLineOrientation${modifier}(
    const char* localeId,
    UErrorCode *status);

/* ---- ubrk.h ---- */
typedef struct UBreakIterator UBreakIterator;

typedef enum UBreakIteratorType {
    UBRK_CHARACTER = 0,
} UBreakIteratorType;

UBreakIterator *
ubrk_open${modifier}(
    UBreakIteratorType type,
    const char *locale,
    const UChar *text,
    int32_t textLength,
    UErrorCode *status);

void
ubrk_close${modifier}(UBreakIterator *bi);

void
ubrk_setText${modifier}(
    UBreakIterator* bi,
    const UChar*    text,
    int32_t         textLength,
    UErrorCode*     status);

int32_t
ubrk_current${modifier}(const UBreakIterator *bi);

int32_t
ubrk_next${modifier}(UBreakIterator *bi);

int32_t
ubrk_previous${modifier}(UBreakIterator *bi);

int32_t
ubrk_first${modifier}(UBreakIterator *bi);

int32_t
ubrk_last${modifier}(UBreakIterator *bi);

int32_t
ubrk_preceding${modifier}(
    UBreakIterator *bi,
    int32_t offset);

int32_t
ubrk_following${modifier}(
    UBreakIterator *bi,
    int32_t offset);

const char*
ubrk_getAvailable${modifier}(int32_t index);

int32_t
ubrk_countAvailable${modifier}(void);

UBool
ubrk_isBoundary${modifier}(UBreakIterator *bi, int32_t offset);

/* ICU 2.8 */
const char*
ubrk_getLocaleByType${modifier}(
    const UBreakIterator *bi,
    ULocDataLocaleType type,
    UErrorCode* status);

/* ---- ubidi.h ---- */
typedef uint8_t UBiDiLevel;

enum UBiDiDirection {
  UBIDI_LTR,
  UBIDI_RTL,
  UBIDI_MIXED,
  UBIDI_NEUTRAL
};
typedef enum UBiDiDirection UBiDiDirection;

typedef struct UBiDi UBiDi;

UBiDi *
ubidi_open${modifier}(void);

UBiDi *
ubidi_openSized${modifier}(
    int32_t maxLength,
    int32_t maxRunCount,
    UErrorCode *pErrorCode);

void
ubidi_close${modifier}(UBiDi *pBiDi);

void
ubidi_setInverse${modifier}(UBiDi *pBiDi, UBool isInverse);

UBool
ubidi_isInverse${modifier}(UBiDi *pBiDi);

typedef enum UBiDiReorderingMode {
    UBIDI_REORDER_DEFAULT = 0,
} UBiDiReorderingMode;

/* ICU 3.6 */
void
ubidi_setReorderingMode${modifier}(
    UBiDi *pBiDi, UBiDiReorderingMode reorderingMode);

/* ICU 3.6 */
UBiDiReorderingMode
ubidi_getReorderingMode${modifier}(UBiDi *pBiDi);

typedef enum UBiDiReorderingOption {
    UBIDI_OPTION_DEFAULT = 0,
} UBiDiReorderingOption;

void
ubidi_setReorderingOptions${modifier}(
    UBiDi *pBiDi, uint32_t reorderingOptions);

uint32_t
ubidi_getReorderingOptions${modifier}(UBiDi *pBiDi);

void
ubidi_setPara${modifier}(
    UBiDi *pBiDi, const UChar *text, int32_t length,
    UBiDiLevel paraLevel, UBiDiLevel *embeddingLevels,
    UErrorCode *pErrorCode);

void
ubidi_setLine${modifier}(
    const UBiDi *pParaBiDi,
    int32_t start, int32_t limit,
    UBiDi *pLineBiDi,
    UErrorCode *pErrorCode);

UBiDiDirection
ubidi_getDirection${modifier}(const UBiDi *pBiDi);

const UChar *
ubidi_getText${modifier}(const UBiDi *pBiDi);

int32_t
ubidi_getLength${modifier}(const UBiDi *pBiDi);

UBiDiLevel
ubidi_getParaLevel${modifier}(const UBiDi *pBiDi);

int32_t
ubidi_countParagraphs${modifier}(UBiDi *pBiDi);

void
ubidi_getLogicalRun${modifier}(
    const UBiDi *pBiDi, int32_t logicalPosition,
    int32_t *pLogicalLimit, UBiDiLevel *pLevel);

int32_t
ubidi_countRuns${modifier}(UBiDi *pBiDi, UErrorCode *pErrorCode);

UBiDiDirection
ubidi_getVisualRun${modifier}(
    UBiDi *pBiDi, int32_t runIndex,
    int32_t *pLogicalStart, int32_t *pLength);

int32_t
ubidi_getVisualIndex${modifier}(
    UBiDi *pBiDi, int32_t logicalIndex, UErrorCode *pErrorCode);

int32_t
ubidi_getLogicalIndex${modifier}(
    UBiDi *pBiDi, int32_t visualIndex, UErrorCode *pErrorCode);

void
ubidi_getLogicalMap${modifier}(
    UBiDi *pBiDi, int32_t *indexMap, UErrorCode *pErrorCode);

void
ubidi_getVisualMap${modifier}(
    UBiDi *pBiDi, int32_t *indexMap, UErrorCode *pErrorCode);

void
ubidi_reorderLogical${modifier}(
    const UBiDiLevel *levels, int32_t length, int32_t *indexMap);

void
ubidi_reorderVisual${modifier}(
    const UBiDiLevel *levels, int32_t length, int32_t *indexMap);

void
ubidi_invertMap${modifier}(
    const int32_t *srcMap, int32_t *destMap, int32_t length);

/* ICU 3.6 */
int32_t
ubidi_getProcessedLength${modifier}(const UBiDi *pBiDi);

/* ICU 3.6 */
int32_t
ubidi_getResultLength${modifier}(const UBiDi *pBiDi);

int32_t
ubidi_writeReordered${modifier}(
    UBiDi *pBiDi,
    UChar *dest, int32_t destSize,
    uint16_t options,
    UErrorCode *pErrorCode);

int32_t
ubidi_writeReverse${modifier}(
    const UChar *src, int32_t srcLength,
    UChar *dest, int32_t destSize,
    uint16_t options,
    UErrorCode *pErrorCode);

/* ---- ubiditransform.h ---- */
/* ICU 58 */

/* ---- ustring.h ---- */
int32_t
u_strlen${modifier}(const UChar *s);

char*
u_strToUTF8${modifier}(
    char *dest,
    int32_t destCapacity,
    int32_t *pDestLength,
    const UChar *src,
    int32_t srcLength,
    UErrorCode *pErrorCode);

UChar*
u_strFromUTF8${modifier}(
    UChar *dest,
    int32_t destCapacity,
    int32_t *pDestLength,
    const char *src,
    int32_t srcLength,
    UErrorCode *pErrorCode);

/* ---- uversion.h ---- */
typedef uint8_t UVersionInfo[4];

void
u_getVersion${modifier}(UVersionInfo versionArray);

/* ICU 2.4 */
void
u_versionToString${modifier}(
    const UVersionInfo versionArray,
    char* versionString);
"""


def _guess_version():
    # detect the version number from a library name
    re_ver_num = re.compile(r'\d+(\.\d+)*')
    for name in _lib_names:
        # Fedora 27: 'libicuuc.so.57'
        # WSL (Ubuntu): 'libicuuc.so.55'
        # MinGW64: 'C:\\Windows\\System32\\icuuc.dll'(?)
        # Windows: 'C:\\Windows\\System32\\icuuc.dll'
        path = find_library(name)
        if path is not None:
            filename = os.path.basename(path)
            for it in re_ver_num.finditer(filename):
                value = it.group(0)
                if float(value) > 0:
                    return value

    # try to find the non modified symbol
    global ffi
    ffi.cdef("""
    typedef uint8_t UVersionInfo[4];
    void u_getVersion(UVersionInfo versionArray);
    """)
    try:
        if getattr(lib, 'u_getVersion'):
            return ''
    except AttributeError:
        pass

    def _check_output(_args):
        try:
            _result = subprocess.run(_args,
                                     shell=False,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        except FileNotFoundError:
            return None
        if _result.returncode != 0:
            return None
        _output = _result.stdout.decode().strip()
        return _output

    # try to get the version number
    ver = _check_output(['pkg-config', '--modversion', 'icu-uc'])
    if ver is None:
        ver = _check_output(['icu-config', '--version'])
    return ver


version = _guess_version()
_modifier = ('_' + version.split('.')[0]
             if version is not None and len(version) > 0 else '')
ffi.cdef(_api.replace('${modifier}', _modifier), override=True)
del _api

# uversion.h
u_get_version = getattr(lib, 'u_getVersion' + _modifier)
u_version_to_string = getattr(lib, 'u_versionToString' + _modifier)

# utypes.h
_u_error_name = getattr(lib, 'u_errorName' + _modifier)

# ubidi.h
ubidi_close = getattr(lib, 'ubidi_close' + _modifier)
ubidi_count_paragraphs = getattr(lib, 'ubidi_countParagraphs' + _modifier)
ubidi_count_runs = getattr(lib, 'ubidi_countRuns' + _modifier)
ubidi_get_direction = getattr(lib, 'ubidi_getDirection' + _modifier)
ubidi_get_length = getattr(lib, 'ubidi_getLength' + _modifier)
ubidi_get_logical_index = getattr(lib, 'ubidi_getLogicalIndex' + _modifier)
ubidi_get_logical_map = getattr(lib, 'ubidi_getLogicalMap' + _modifier)
ubidi_get_logical_run = getattr(lib, 'ubidi_getLogicalRun' + _modifier)
ubidi_get_para_level = getattr(lib, 'ubidi_getParaLevel' + _modifier)
ubidi_get_processed_length = getattr(
    lib, 'ubidi_getProcessedLength' + _modifier)
ubidi_get_reordering_mode = getattr(lib, 'ubidi_getReorderingMode' + _modifier)
ubidi_get_reordering_options = getattr(
    lib, 'ubidi_getReorderingOptions' + _modifier)
ubidi_get_result_length = getattr(lib, 'ubidi_getResultLength' + _modifier)
ubidi_get_text = getattr(lib, 'ubidi_getText' + _modifier)
ubidi_get_visual_index = getattr(lib, 'ubidi_getVisualIndex' + _modifier)
ubidi_get_visual_map = getattr(lib, 'ubidi_getVisualMap' + _modifier)
ubidi_get_visual_run = getattr(lib, 'ubidi_getVisualRun' + _modifier)
ubidi_invert_map = getattr(lib, 'ubidi_invertMap' + _modifier)
ubidi_is_inverse = getattr(lib, 'ubidi_isInverse' + _modifier)
ubidi_open = getattr(lib, 'ubidi_open' + _modifier)
ubidi_open_sized = getattr(lib, 'ubidi_openSized' + _modifier)
ubidi_reorder_logical = getattr(lib, 'ubidi_reorderLogical' + _modifier)
ubidi_reorder_visual = getattr(lib, 'ubidi_reorderVisual' + _modifier)
ubidi_set_inverse = getattr(lib, 'ubidi_setInverse' + _modifier)
ubidi_set_line = getattr(lib, 'ubidi_setLine' + _modifier)
ubidi_set_para = getattr(lib, 'ubidi_setPara' + _modifier)
ubidi_set_reordering_mode = getattr(lib, 'ubidi_setReorderingMode' + _modifier)
ubidi_set_reordering_options = getattr(
    lib, 'ubidi_setReorderingOptions' + _modifier)
ubidi_write_reordered = getattr(lib, 'ubidi_writeReordered' + _modifier)
ubidi_write_reverse = getattr(lib, 'ubidi_writeReverse' + _modifier)

# ubrk.h
ubrk_close = getattr(lib, 'ubrk_close' + _modifier)
ubrk_count_available = getattr(lib, 'ubrk_countAvailable' + _modifier)
ubrk_current = getattr(lib, 'ubrk_current' + _modifier)
ubrk_first = getattr(lib, 'ubrk_first' + _modifier)
ubrk_following = getattr(lib, 'ubrk_following' + _modifier)
ubrk_get_available = getattr(lib, 'ubrk_getAvailable' + _modifier)
ubrk_get_locale_by_type = getattr(lib, 'ubrk_getLocaleByType' + _modifier)
ubrk_is_boundary = getattr(lib, 'ubrk_isBoundary' + _modifier)
ubrk_last = getattr(lib, 'ubrk_last' + _modifier)
ubrk_next = getattr(lib, 'ubrk_next' + _modifier)
ubrk_open = getattr(lib, 'ubrk_open' + _modifier)
ubrk_preceding = getattr(lib, 'ubrk_preceding' + _modifier)
ubrk_previous = getattr(lib, 'ubrk_previous' + _modifier)
ubrk_set_text = getattr(lib, 'ubrk_setText' + _modifier)

# uloc.h
uloc_get_character_orientation = getattr(
    lib, 'uloc_getCharacterOrientation' + _modifier)
uloc_get_default = getattr(lib, 'uloc_getDefault' + _modifier)
uloc_get_language = getattr(lib, 'uloc_getLanguage' + _modifier)
uloc_get_line_orientation = getattr(
    lib, 'uloc_getLineOrientation' + _modifier)
uloc_get_script = getattr(lib, 'uloc_getScript' + _modifier)

# ustring.h
u_str_to_utf8 = getattr(lib, 'u_strToUTF8' + _modifier)
u_str_from_utf8 = getattr(lib, 'u_strFromUTF8' + _modifier)
u_strlen = getattr(lib, 'u_strlen' + _modifier)


def get_version():
    vi = ffi.new('UVersionInfo')
    u_get_version(vi)
    # U_MAX_VERSION_STRING_LENGTH = 20
    version_string = ffi.new('char[20]')
    u_version_to_string(vi, version_string)
    return ffi.string(version_string).decode()


def u_error_name(status):
    error_name = _u_error_name(status)
    return ffi.string(error_name).decode()


def u_failure(status):
    return status > 0


def u_success(status):
    return status <= 0


class UBiDi(object):
    UBIDI_DEFAULT_LTR = 0xfe
    UBIDI_DEFAULT_RTL = 0xff

    UBIDI_MAP_NOWHERE = -1

    # UBiDiDirection
    UBIDI_LTR = 0
    UBIDI_RTL = 1
    UBIDI_MIXED = 2
    UBIDI_NEUTRAL = 3

    # UBiDiReorderingMode
    UBIDI_REORDER_DEFAULT = 0
    UBIDI_REORDER_NUMBERS_SPECIAL = 1
    UBIDI_REORDER_GROUP_NUMBERS_WITH_R = 2
    UBIDI_REORDER_RUNS_ONLY = 3
    UBIDI_REORDER_INVERSE_NUMBERS_AS_L = 4
    UBIDI_REORDER_INVERSE_LIKE_DIRECT = 5
    UBIDI_REORDER_INVERSE_FOR_NUMBERS_SPECIAL = 6

    # UBiDiReorderingOption
    UBIDI_OPTION_DEFAULT = 0,
    UBIDI_OPTION_INSERT_MARKS = 1

    # option flags for ubidi_writeReordered()
    UBIDI_KEEP_BASE_COMBINING = 1
    UBIDI_DO_MIRRORING = 2
    UBIDI_INSERT_LRM_FOR_NUMERIC = 4
    UBIDI_REMOVE_BIDI_CONTROLS = 8
    UBIDI_OUTPUT_REVERSE = 16

    def __init__(self):
        self._status = ffi.new('UErrorCode *')
        self._bidi = ffi.gc(ubidi_open(),
                            ubidi_close)
        self._source = None

    @property
    def status(self):
        return self._status[0]

    def count_paragraphs(self):
        return ubidi_count_paragraphs(self._bidi)

    def count_runs(self):
        self._status[0] = 0
        return ubidi_count_runs(self._bidi, self._status)

    def get_direction(self):
        return ubidi_get_direction(self._bidi)

    def get_length(self):
        return ubidi_get_length(self._bidi)

    def get_logical_index(self, visual_index):
        self._status[0] = 0
        return ubidi_get_logical_index(self._bidi, visual_index, self._status)

    def get_logical_run(self, logical_position):
        logical_limit = ffi.new('int32_t *')
        level = ffi.new('UBiDiLevel *')
        ubidi_get_logical_run(self._bidi,
                              logical_position,
                              logical_limit,
                              level)
        return logical_limit[0], level[0]

    def get_para_level(self):
        return ubidi_get_para_level(self._bidi)

    def get_processed_length(self):
        return ubidi_get_processed_length(self._bidi)

    def get_reordering_mode(self):
        return ubidi_get_reordering_mode(self._bidi)

    def get_reordering_options(self):
        return ubidi_get_reordering_options(self._bidi)

    def get_result_length(self):
        return ubidi_get_result_length(self._bidi)

    def get_text(self):
        buf = ubidi_get_text(self._bidi)
        return ffi.string(buf)

    def get_visual_index(self, logical_index):
        self._status[0] = 0
        return ubidi_get_visual_index(self._bidi, logical_index, self._status)

    def get_visual_run(self, run_index):
        logical_start = ffi.new('int32_t *')
        length = ffi.new('int32_t *')
        direction = ubidi_get_visual_run(self._bidi,
                                         run_index,
                                         logical_start,
                                         length)
        return logical_start[0], length[0], direction

    def set_para(self, text, para_level):
        self._status[0] = 0
        buf = ffi.new('UChar[]', text)
        buf_length = len(buf) - 1
        self._source = buf
        embedding_levels = ffi.NULL
        ubidi_set_para(self._bidi,
                       buf,
                       buf_length,
                       para_level,
                       embedding_levels,
                       self._status)

    def set_reordering_mode(self, reordering_mode):
        ubidi_set_reordering_mode(self._bidi, reordering_mode)

    def set_reordering_options(self, reordering_options):
        ubidi_set_reordering_options(self._bidi, reordering_options)

    def visual_iter(self):
        count = self.count_runs()
        for index in range(count):
            start, length, direction = self.get_visual_run(index)
            string = ffi.string(self._source[start:start + length])
            if direction == UBiDi.UBIDI_RTL:
                string = string[::-1]
            yield string

    def write_reordered(self, options=0):
        self._status[0] = 0
        if options == 0:
            dest_size = self.get_processed_length()
        else:
            dest_size = self.get_length()
            if options & UBiDi.UBIDI_INSERT_LRM_FOR_NUMERIC:
                dest_size += 2 * self.count_runs()
        dest = ffi.new('UChar[{}]'.format(dest_size))
        length = ubidi_write_reordered(self._bidi,
                                       dest,
                                       dest_size,
                                       options,
                                       self._status)
        if length == 0:
            output = None
        else:
            output = ffi.string(dest)
        return output, length


class UBreakIterator(Iterator, Reversible):
    UBRK_CHARACTER = 0
    UBRK_WORD = 1
    UBRK_LINE = 2
    UBRK_SENTENCE = 3

    UBRK_DONE = -1

    def __init__(self, break_type, locale, text=None):
        self._bi = None
        self._source = None
        self._status = ffi.new('UErrorCode *')
        where = ffi.new('char[]', locale.encode())
        if text is None:
            buf = ffi.NULL
            buf_length = 0
        else:
            buf = ffi.new('UChar[]', text)
            buf_length = len(buf) - 1
            self._source = buf
        self._bi = ffi.gc(
            ubrk_open(break_type, where, buf, buf_length, self._status),
            ubrk_close)

    def __iter__(self):
        self.first()
        return self

    def __next__(self):
        start = self.current()
        end = self.next()
        if end == UBreakIterator.UBRK_DONE:
            raise StopIteration
        assert start >= 0
        assert end > start
        assert end <= len(self._source) - 1
        segment = self._source[start:end]
        return ffi.string(segment)

    def __reversed__(self):
        items = list()
        for x in self:
            items.append(x)
        items.reverse()
        return items

    @property
    def status(self):
        return self._status[0]

    @staticmethod
    def count_available():
        return ubrk_count_available()

    def current(self):
        offset = ubrk_current(self._bi)
        return offset

    def first(self):
        offset = ubrk_first(self._bi)
        return offset

    @staticmethod
    def get_available(index):
        locale = ubrk_get_available(index)
        if locale == ffi.NULL:
            return None
        return ffi.string(locale).decode()

    def get_locale_by_type(self, locale_type):
        self._status[0] = 0
        locale = ubrk_get_locale_by_type(self._bi, locale_type, self._status)
        if locale == ffi.NULL:
            return None
        return ffi.string(locale).decode()

    def last(self):
        offset = ubrk_last(self._bi)
        return offset

    def next(self):
        offset = ubrk_next(self._bi)
        return offset

    def previous(self):
        offset = ubrk_previous(self._bi)
        return offset

    def set_text(self, text):
        buf = ffi.new('UChar[]', text)
        buf_length = len(buf) - 1
        self._source = buf
        self._status[0] = 0
        ubrk_set_text(self._bi, buf, buf_length, self._status)


class UErrorCode(object):
    U_USING_FALLBACK_WARNING = -128
    U_USING_DEFAULT_WARNING = -127
    U_ZERO_ERROR = 0


class ULocale(object):
    ULOC_LANG_CAPACITY = 12
    ULOC_SCRIPT_CAPACITY = 6

    ULOC_LAYOUT_LTR = 0  # left-to-right
    ULOC_LAYOUT_RTL = 1  # right-to-left
    ULOC_LAYOUT_TTB = 2  # top-to-bottom
    ULOC_LAYOUT_BTT = 3  # bottom-to-top
    ULOC_LAYOUT_UNKNOWN = 4

    ULOC_ACTUAL_LOCALE = 0
    ULOC_VALID_LOCALE = 1

    def __init__(self, locale):
        """Constructs a ULocale object.

        Arguments:
            locale (str): The ICU locale.
        """
        self.locale = locale
        self._status = ffi.new('UErrorCode *')

    @property
    def status(self):
        return self._status[0]

    def get_character_orientation(self):
        locale = ffi.new('char[]', self.locale.encode())
        self._status[0] = 0
        layout = uloc_get_character_orientation(locale, self._status)
        return layout

    @staticmethod
    def get_default():
        default = uloc_get_default()
        locale = ffi.string(default).decode()
        return ULocale(locale)

    def get_language(self):
        locale = ffi.new('char[]', self.locale.encode())
        language = ffi.new('char[{}]'.format(ULocale.ULOC_LANG_CAPACITY))
        self._status[0] = 0
        uloc_get_language(locale, language, len(language), self._status)
        if u_failure(self._status[0]):
            return None
        return ffi.string(language).decode()

    def get_line_orientation(self):
        locale = ffi.new('char[]', self.locale.encode())
        self._status[0] = 0
        layout = uloc_get_line_orientation(locale, self._status)
        return layout

    def get_script(self):
        locale = ffi.new('char[]', self.locale.encode())
        script = ffi.new('char[{}]'.format(ULocale.ULOC_SCRIPT_CAPACITY))
        self._status[0] = 0
        uloc_get_script(locale, script, len(script), self._status)
        if u_failure(self._status[0]):
            return None
        return ffi.string(script).decode()


version = get_version()
if float(version) < _icu_min_required_version:
    raise RuntimeError('Cannot find the ICU ' + str(_icu_min_required_version)
                       + '+ (found ' + version + ')')
