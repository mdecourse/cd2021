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


from cffi import FFI

from ._ffi_api import dlopen

_API = r"""
/*
 * Fontconfig 2.12.6
 */
typedef int fc_atomic_int_t;  // src/fcatomic.h
typedef struct _FcRef { fc_atomic_int_t count; } FcRef;  // src/fcatomic.h

// fontconfig/fontconfig.h
typedef unsigned char   FcChar8;
typedef unsigned short  FcChar16;
typedef unsigned int    FcChar32;
typedef int             FcBool;

typedef enum _FcResult {
    FcResultMatch, FcResultNoMatch, FcResultTypeMismatch, FcResultNoId,
    FcResultOutOfMemory
} FcResult;

struct _FcPattern {
    int             num;
    int             size;
    intptr_t        elts_offset;
    FcRef           ref;
};  // src/fcint.h
typedef struct _FcPattern   FcPattern;

typedef struct _FcFontSet {
    int             nfont;
    int             sfont;
    FcPattern       **fonts;
} FcFontSet;

typedef struct _FcObjectSet {
    int             nobject;
    int             sobject;
    const char      **objects;
} FcObjectSet;

typedef enum _FcMatchKind {
    FcMatchPattern, FcMatchFont, FcMatchScan
} FcMatchKind;

// typedef struct _FcConfig    FcConfig;  // -> void

struct _FcStrSet {
    FcRef           ref;        /* reference count */
    int             num;
    int             size;
    FcChar8         **strs;
    unsigned int    control;    /* control bits for set behavior */
};  // src/fcint.h
typedef struct _FcStrSet    FcStrSet;

struct _FcStrList {
    FcStrSet        *set;
    int             n;
};  // src/fcint.h
typedef struct _FcStrList   FcStrList;

void FcConfigDestroy(void *config);
FcStrList * FcConfigGetConfigFiles(void *config);
FcBool FcConfigSubstitute(void *config, void *p, FcMatchKind kind);

void FcDefaultSubstitute(void *pattern);

void FcFini(void);

FcFontSet * FcFontList(void *config, FcPattern *p, FcObjectSet *os);
FcPattern * FcFontMatch(void *config, FcPattern *p, FcResult *result);
FcBool FcFontSetAdd(FcFontSet *s, FcPattern *font);
FcFontSet * FcFontSetCreate(void);
void FcFontSetDestroy(FcFontSet *s);

int FcGetVersion(void);
void * FcInitLoadConfigAndFonts(void);
void * FcNameParse(const FcChar8 *name);

FcObjectSet * FcObjectSetBuild(const char *first, ...);
FcObjectSet * FcObjectSetCreate(void);
void FcObjectSetDestroy(FcObjectSet *os);

FcPattern * FcPatternCreate(void);
void FcPatternDestroy(void *p);
FcPattern * FcPatternFilter(FcPattern *p, const FcObjectSet *);
FcChar8 * FcPatternFormat(FcPattern *pat, const FcChar8 *format);

void FcStrFree(FcChar8 *s);

void FcStrListDone(FcStrList *list);
void FcStrListFirst(FcStrList *list);
FcChar8 * FcStrListNext(FcStrList *list);

int FcWeightFromOpenType(int ot_weight);
int FcWeightToOpenType(int fc_weight);
"""

ffi = FFI()
ffi.cdef(_API)
del _API

lib = dlopen(ffi, ['fontconfig', 'libfontconfig-1'])


class FontConfig(object):
    # See https://www.freedesktop.org/software/fontconfig/fontconfig-user.html

    # Font properties
    # from fontconfig/fontconfig/fontconfig.h
    FC_FAMILY = 'family'
    FC_STYLE = 'style'
    FC_SLANT = 'slant'
    FC_WEIGHT = 'weight'
    FC_SIZE = 'size'
    FC_ASPECT = 'aspect'
    FC_PIXEL_SIZE = 'pixelsize'
    FC_SPACING = 'spacing'
    FC_FOUNDRY = 'foundry'
    FC_ANTIALIAS = 'antialias'
    FC_HINTING = 'hinting'
    FC_HINT_STYLE = 'hintstyle'
    FC_VERTICAL_LAYOUT = 'verticallayout'
    FC_AUTOHINT = 'autohint'
    FC_WIDTH = 'width'
    FC_FILE = 'file'
    FC_INDEX = 'index'
    FC_OUTLINE = 'outline'
    FC_SCALABLE = 'scalable'
    FC_SYMBOL = 'symbol'
    FC_LANG = 'lang'
    FC_FONT_FORMAT = 'fontformat'

    FC_WEIGHT_EXTRA_BLACK = 215

    # CSS 'font-style' name to font-config FC_SLANT value
    # from fontconfig/fontconfig/fontconfig.h
    FC_SLANT_MAP = {
        'normal': 0,
        'italic': 100,
        'oblique': 110,
    }

    # CSS 'font-stretch' name to font-config FC_WIDTH value
    # from fontconfig/fontconfig/fontconfig.h
    FC_WIDTH_MAP = {
        'ultra-condensed': 50,
        'extra-condensed': 63,
        'condensed': 75,
        'semi-condensed': 87,
        'normal': 100,
        'semi-expanded': 113,
        'expanded': 125,
        'extra-expanded': 150,
        'ultra-expanded': 200,
    }

    # font-config FC_WEIGHT value to CSS 'font-weight' value
    # from fontconfig/fontconfig/fontconfig.h
    FC_WEIGHT_MAP = {
        0: 100,  # thin
        40: 200,  # extra light/ultra light
        50: 300,  # light
        55: 350,  # demi light/semi light
        75: 380,  # book
        80: 400,  # regular/normal
        100: 500,  # medium
        180: 600,  # demi bold/semi bold
        200: 700,  # bold
        205: 800,  # extra bold/ultra bold
        210: 900,  # black/heavy
        215: 1000,  # extra black/ultra black
    }

    version = lib.FcGetVersion()

    @staticmethod
    def get_config_files():
        cdata = ffi.gc(lib.FcConfigGetConfigFiles(ffi.NULL),
                       lib.FcStrListDone)
        files = list()
        while True:
            item = lib.FcStrListNext(cdata)
            if item == ffi.NULL:
                break
            files.append(ffi.string(item).decode())
        return files

    @staticmethod
    def list(fc_pattern=None, fc_elements=None, fc_format=None):
        # See https://www.freedesktop.org/software/fontconfig/fontconfig-devel/fcpatternformat.html
        if fc_pattern is None:
            pat = ffi.gc(lib.FcPatternCreate(),
                         lib.FcPatternDestroy)
        else:
            pat = ffi.gc(lib.FcNameParse(fc_pattern.encode()),
                         lib.FcPatternDestroy)
        if fc_elements is None:
            fc_elements = [FontConfig.FC_FAMILY, FontConfig.FC_STYLE,
                           FontConfig.FC_FILE]
        elements = [ffi.new('char[]', x.encode()) for x in
                    iter(fc_elements)] + [ffi.NULL]
        if fc_format is None:
            fc_format = '%{=fclist}'
        fmt = fc_format.encode()
        os = ffi.gc(lib.FcObjectSetBuild(*elements),
                    lib.FcObjectSetDestroy)
        fs = ffi.gc(lib.FcFontList(ffi.NULL, pat, os),
                    lib.FcFontSetDestroy)
        font_sequence = list()
        for i in range(0, fs.nfont):
            patfmt = ffi.gc(lib.FcPatternFormat(fs.fonts[i], fmt),
                            lib.FcStrFree)
            data = ffi.string(patfmt)
            if len(data) > 0:
                font_sequence.append(data.decode())
        return font_sequence

    @staticmethod
    def match(fc_pattern, fc_format=None):
        if fc_format is None:
            fc_format = '%{=fcmatch}'
        fmt = fc_format.encode()
        pat = ffi.gc(lib.FcNameParse(fc_pattern.encode()),
                     lib.FcPatternDestroy)
        lib.FcConfigSubstitute(ffi.NULL, pat, lib.FcMatchPattern)
        lib.FcDefaultSubstitute(pat)
        fs = ffi.gc(lib.FcFontSetCreate(),
                    lib.FcFontSetDestroy)
        result = ffi.new('FcResult *')
        match = ffi.gc(lib.FcFontMatch(ffi.NULL, pat, result),
                       lib.FcPatternDestroy)
        lib.FcFontSetAdd(fs, match)
        font_sequence = list()
        for i in range(0, fs.nfont):
            font = ffi.gc(lib.FcPatternFilter(fs.fonts[i], ffi.NULL),
                          lib.FcPatternDestroy)
            patfmt = ffi.gc(lib.FcPatternFormat(font, fmt),
                            lib.FcStrFree)
            font_sequence.append(ffi.string(patfmt).decode())
        return font_sequence

    @staticmethod
    def weight_from_open_type(ot_weight):
        return lib.FcWeightFromOpenType(ot_weight)

    @staticmethod
    def weight_to_open_type(fc_weight):
        return lib.FcWeightToOpenType(fc_weight)
