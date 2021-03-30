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

_API = r"""
/*
 * FreeType 2.8.1
 */
typedef int32_t  FT_Int32;

/* ---- freetype/fttypes.h ---- */
typedef unsigned char  FT_Byte;
typedef char  FT_String;
typedef signed short  FT_Short;
typedef unsigned short  FT_UShort;
typedef signed int  FT_Int;
typedef unsigned int  FT_UInt;
typedef signed long  FT_Long;
typedef unsigned long  FT_ULong;
typedef signed long  FT_F26Dot6;
typedef signed long  FT_Fixed;
typedef int  FT_Error;

typedef struct  FT_Matrix_
{
  FT_Fixed  xx, xy;
  FT_Fixed  yx, yy;
} FT_Matrix;

typedef void  (*FT_Generic_Finalizer)(void*  object);

typedef struct  FT_Generic_
{
  void*                 data;
  FT_Generic_Finalizer  finalizer;
} FT_Generic;

typedef struct FT_ListNodeRec_*  FT_ListNode;

typedef struct  FT_ListRec_
{
  FT_ListNode  head;
  FT_ListNode  tail;
} FT_ListRec;

/* ---- freetype/ftsystem.h ---- */
typedef struct FT_MemoryRec_*  FT_Memory;
typedef struct FT_StreamRec_*  FT_Stream;

/* ---- freetype/ftimage.h ---- */
typedef signed long  FT_Pos;

typedef struct  FT_Vector_
{
  FT_Pos  x;
  FT_Pos  y;
} FT_Vector;

typedef struct  FT_BBox_
{
  FT_Pos  xMin, yMin;
  FT_Pos  xMax, yMax;
} FT_BBox;

typedef struct  FT_Bitmap_
{
  unsigned int    rows;
  unsigned int    width;
  int             pitch;
  unsigned char*  buffer;
  unsigned short  num_grays;
  unsigned char   pixel_mode;
  unsigned char   palette_mode;
  void*           palette;
} FT_Bitmap;

typedef struct  FT_Outline_
{
  short       n_contours;      /* number of contours in glyph        */
  short       n_points;        /* number of points in the glyph      */
  FT_Vector*  points;          /* the outline's points               */
  char*       tags;            /* the points flags                   */
  short*      contours;        /* the contour end points             */
  int         flags;           /* outline masks                      */
} FT_Outline;

typedef int
(*FT_Outline_MoveToFunc)( const FT_Vector*  to,
                          void*             user );
typedef int
(*FT_Outline_LineToFunc)( const FT_Vector*  to,
                          void*             user );
typedef int
(*FT_Outline_ConicToFunc)( const FT_Vector*  control,
                           const FT_Vector*  to,
                           void*             user );
typedef int
(*FT_Outline_CubicToFunc)( const FT_Vector*  control1,
                           const FT_Vector*  control2,
                           const FT_Vector*  to,
                           void*             user );

typedef struct  FT_Outline_Funcs_
{
  FT_Outline_MoveToFunc   move_to;
  FT_Outline_LineToFunc   line_to;
  FT_Outline_ConicToFunc  conic_to;
  FT_Outline_CubicToFunc  cubic_to;
  int                     shift;
  FT_Pos                  delta;
} FT_Outline_Funcs;

typedef enum  FT_Glyph_Format_
{
  FT_GLYPH_FORMAT_NONE = 0,
  /* ... */
} FT_Glyph_Format;

/* ---- freetype/freetype.h ---- */
typedef struct  FT_Glyph_Metrics_
{
  FT_Pos  width;
  FT_Pos  height;
  FT_Pos  horiBearingX;
  FT_Pos  horiBearingY;
  FT_Pos  horiAdvance;
  FT_Pos  vertBearingX;
  FT_Pos  vertBearingY;
  FT_Pos  vertAdvance;
} FT_Glyph_Metrics;

typedef struct  FT_Bitmap_Size_
{
  FT_Short  height;
  FT_Short  width;
  FT_Pos    size;
  FT_Pos    x_ppem;
  FT_Pos    y_ppem;
} FT_Bitmap_Size;

typedef ...  *FT_Library;
/* typedef struct FT_ModuleRec_*  FT_Module; */
typedef struct FT_DriverRec_*  FT_Driver;
typedef struct FT_RendererRec_*  FT_Renderer;
typedef struct FT_FaceRec_*  FT_Face;
typedef struct FT_SizeRec_*  FT_Size;
typedef struct FT_GlyphSlotRec_*  FT_GlyphSlot;
typedef struct FT_CharMapRec_*  FT_CharMap;

typedef enum  FT_Encoding_
{
  FT_ENCODING_NONE = 0,
  /* ... */
} FT_Encoding;

typedef struct  FT_CharMapRec_
{
  FT_Face      face;
  FT_Encoding  encoding;
  FT_UShort    platform_id;
  FT_UShort    encoding_id;
} FT_CharMapRec;

typedef struct FT_Face_InternalRec_*  FT_Face_Internal;

typedef struct  FT_FaceRec_
{
  FT_Long           num_faces;
  FT_Long           face_index;
  FT_Long           face_flags;
  FT_Long           style_flags;
  FT_Long           num_glyphs;
  FT_String*        family_name;
  FT_String*        style_name;
  FT_Int            num_fixed_sizes;
  FT_Bitmap_Size*   available_sizes;
  FT_Int            num_charmaps;
  FT_CharMap*       charmaps;
  FT_Generic        generic;
  /*# The following member variables (down to `underline_thickness') */
  /*# are only relevant to scalable outlines; cf. @FT_Bitmap_Size    */
  /*# for bitmap fonts.                                              */
  FT_BBox           bbox;
  FT_UShort         units_per_EM;
  FT_Short          ascender;
  FT_Short          descender;
  FT_Short          height;
  FT_Short          max_advance_width;
  FT_Short          max_advance_height;
  FT_Short          underline_position;
  FT_Short          underline_thickness;
  FT_GlyphSlot      glyph;
  FT_Size           size;
  FT_CharMap        charmap;
  /*@private begin */
  FT_Driver         driver;
  FT_Memory         memory;
  FT_Stream         stream;
  FT_ListRec        sizes_list;
  FT_Generic        autohint;   /* face-specific auto-hinter data */
  void*             extensions; /* unused                         */
  FT_Face_Internal  internal;
  /*@private end */
} FT_FaceRec;

typedef struct FT_Size_InternalRec_*  FT_Size_Internal;

typedef struct  FT_Size_Metrics_
{
  FT_UShort  x_ppem;      /* horizontal pixels per EM               */
  FT_UShort  y_ppem;      /* vertical pixels per EM                 */
  FT_Fixed   x_scale;     /* scaling values used to convert font    */
  FT_Fixed   y_scale;     /* units to 26.6 fractional pixels        */
  FT_Pos     ascender;    /* ascender in 26.6 frac. pixels          */
  FT_Pos     descender;   /* descender in 26.6 frac. pixels         */
  FT_Pos     height;      /* text height in 26.6 frac. pixels       */
  FT_Pos     max_advance; /* max horizontal advance, in 26.6 pixels */
} FT_Size_Metrics;

typedef struct  FT_SizeRec_
{
  FT_Face           face;      /* parent face object              */
  FT_Generic        generic;   /* generic pointer for client uses */
  FT_Size_Metrics   metrics;   /* size metrics                    */
  FT_Size_Internal  internal;
} FT_SizeRec;

typedef struct FT_SubGlyphRec_*  FT_SubGlyph;
typedef struct FT_Slot_InternalRec_*  FT_Slot_Internal;

typedef struct  FT_GlyphSlotRec_
{
  FT_Library        library;
  FT_Face           face;
  FT_GlyphSlot      next;
  FT_UInt           reserved;       /* retained for binary compatibility */
  FT_Generic        generic;
  FT_Glyph_Metrics  metrics;
  FT_Fixed          linearHoriAdvance;
  FT_Fixed          linearVertAdvance;
  FT_Vector         advance;
  FT_Glyph_Format   format;
  FT_Bitmap         bitmap;
  FT_Int            bitmap_left;
  FT_Int            bitmap_top;
  FT_Outline        outline;
  FT_UInt           num_subglyphs;
  FT_SubGlyph       subglyphs;
  void*             control_data;
  long              control_len;
  FT_Pos            lsb_delta;
  FT_Pos            rsb_delta;
  void*             other;
  FT_Slot_Internal  internal;
} FT_GlyphSlotRec;

typedef enum  FT_Size_Request_Type_
{
  FT_SIZE_REQUEST_TYPE_NOMINAL,
  /* ... */
} FT_Size_Request_Type;

typedef struct  FT_Size_RequestRec_
{
  FT_Size_Request_Type  type;
  FT_Long               width;
  FT_Long               height;
  FT_UInt               horiResolution;
  FT_UInt               vertResolution;
} FT_Size_RequestRec;

typedef struct FT_Size_RequestRec_  *FT_Size_Request;

typedef enum  FT_Render_Mode_
{
  FT_RENDER_MODE_NORMAL = 0,
  /* ... */
} FT_Render_Mode;

/* ---- freetype/ftoutln.h ---- */
typedef enum  FT_Orientation_
{
  FT_ORIENTATION_TRUETYPE   = 0,
  /* ... */
} FT_Orientation;

/* ---- Base Interface ---- */
void
FT_Library_Version( FT_Library   library,
                    FT_Int      *amajor,
                    FT_Int      *aminor,
                    FT_Int      *apatch );

FT_Error
FT_Init_FreeType( FT_Library  *alibrary );

FT_Error
FT_Done_FreeType( FT_Library  library );

FT_Error
FT_New_Face( FT_Library   library,
             const char*  filepathname,
             FT_Long      face_index,
             FT_Face     *aface );

FT_Error
FT_New_Memory_Face( FT_Library      library,
                    const FT_Byte*  file_base,
                    FT_Long         file_size,
                    FT_Long         face_index,
                    FT_Face        *aface );

FT_Error
FT_Reference_Face( FT_Face  face );

FT_Error
FT_Done_Face( FT_Face  face );

FT_Error
FT_Set_Char_Size( FT_Face     face,
                  FT_F26Dot6  char_width,
                  FT_F26Dot6  char_height,
                  FT_UInt     horz_resolution,
                  FT_UInt     vert_resolution );

FT_Error
FT_Set_Pixel_Sizes( FT_Face  face,
                    FT_UInt  pixel_width,
                    FT_UInt  pixel_height );

FT_Error
FT_Request_Size( FT_Face          face,
                 FT_Size_Request  req );

FT_Error
FT_Select_Size( FT_Face  face,
                FT_Int   strike_index );

void
FT_Set_Transform( FT_Face     face,
                  FT_Matrix*  matrix,
                  FT_Vector*  delta );

FT_Error
FT_Load_Glyph( FT_Face   face,
               FT_UInt   glyph_index,
               FT_Int32  load_flags );

FT_UInt
FT_Get_Char_Index( FT_Face   face,
                   FT_ULong  charcode );

FT_Error
FT_Load_Char( FT_Face   face,
              FT_ULong  char_code,
              FT_Int32  load_flags );

FT_Error
FT_Render_Glyph( FT_GlyphSlot    slot,
                 FT_Render_Mode  render_mode );

FT_Error
FT_Get_Kerning( FT_Face     face,
                FT_UInt     left_glyph,
                FT_UInt     right_glyph,
                FT_UInt     kern_mode,
                FT_Vector  *akerning );

FT_Error
FT_Select_Charmap( FT_Face      face,
                   FT_Encoding  encoding );

FT_Error
FT_Set_Charmap( FT_Face     face,
                FT_CharMap  charmap );

FT_Int
FT_Get_Charmap_Index( FT_CharMap  charmap );

/* ---- Outline Processing ---- */
void
FT_Outline_Translate( const FT_Outline*  outline,
                      FT_Pos             xOffset,
                      FT_Pos             yOffset );

void
FT_Outline_Transform( const FT_Outline*  outline,
                      const FT_Matrix*   matrix );

FT_Error
FT_Outline_Embolden( FT_Outline*  outline,
                     FT_Pos       strength );

FT_Error
FT_Outline_EmboldenXY( FT_Outline*  outline,
                       FT_Pos       xstrength,
                       FT_Pos       ystrength );

void
FT_Outline_Reverse( FT_Outline*  outline );

FT_Error
FT_Outline_Check( FT_Outline*  outline );

void
FT_Outline_Get_CBox( const FT_Outline*  outline,
                     FT_BBox           *acbox );

FT_Error
FT_Outline_Get_BBox( FT_Outline*  outline,
                     FT_BBox     *abbox );

FT_Error
FT_Outline_Get_Bitmap( FT_Library        library,
                       FT_Outline*       outline,
                       const FT_Bitmap  *abitmap );

FT_Error
FT_Outline_Decompose( FT_Outline*              outline,
                      const FT_Outline_Funcs*  func_interface,
                      void*                    user );

FT_Orientation
FT_Outline_Get_Orientation( FT_Outline*  outline );

/* ---- freetype/ftadvanc.h ---- */
FT_Error
FT_Get_Advance( FT_Face    face,
                FT_UInt    gindex,
                FT_Int32   load_flags,
                FT_Fixed  *padvance );

/* ---- freetype/fysynth.h ---- */
void
FT_GlyphSlot_Embolden( FT_GlyphSlot  slot );

void
FT_GlyphSlot_Oblique( FT_GlyphSlot  slot );

/* ---- freetype/ftmodapi.h ---- */
FT_Error
FT_Property_Set( FT_Library        library,
                 const FT_String*  module_name,
                 const FT_String*  property_name,
                 const void*       value );

FT_Error
FT_Property_Get( FT_Library        library,
                 const FT_String*  module_name,
                 const FT_String*  property_name,
                 void*             value );

/*
 * HarfBuzz 1.7.4
 */
/* ---- hb-common.h ---- */
typedef int hb_bool_t;
typedef uint32_t hb_codepoint_t;
typedef int32_t hb_position_t;
typedef uint32_t hb_mask_t;
typedef union _hb_var_int_t {
  uint32_t u32;
  int32_t i32;
  uint16_t u16[2];
  int16_t i16[2];
  uint8_t u8[4];
  int8_t i8[4];
} hb_var_int_t;
typedef uint32_t hb_tag_t;

/* len=-1 means str is NUL-terminated. */
hb_tag_t
hb_tag_from_string (const char *str, int len);

/* buf should have 4 bytes. */
void
hb_tag_to_string (hb_tag_t tag, char *buf);

#define HB_TAG_NONE  0
// #define HB_TAG_MAX HB_TAG(0xff,0xff,0xff,0xff)
#define HB_TAG_MAX  0xffffffff
// #define HB_TAG_MAX_SIGNED HB_TAG(0x7f,0xff,0xff,0xff)
#define HB_TAG_MAX_SIGNED  0x7fffffff

typedef enum {
  HB_DIRECTION_INVALID = 0,
  HB_DIRECTION_LTR = 4,
  HB_DIRECTION_RTL,
  HB_DIRECTION_TTB,
  HB_DIRECTION_BTT
} hb_direction_t;

hb_direction_t
hb_direction_from_string (const char *str, int len);

const char *
hb_direction_to_string (hb_direction_t direction);

typedef const struct hb_language_impl_t *hb_language_t;

hb_language_t
hb_language_from_string (const char *str, int len);

const char *
hb_language_to_string (hb_language_t language);

hb_language_t
hb_language_get_default (void);

typedef enum
{
  /*1.1*/ HB_SCRIPT_COMMON			= 0x5a797979, // HB_TAG('Z','y','y','y'),
  /*1.1*/ HB_SCRIPT_INHERITED			= 0x5a696e68, // HB_TAG('Z','i','n','h'),
  /*5.0*/ HB_SCRIPT_UNKNOWN			= 0x5a7a7a7a, // HB_TAG('Z','z','z','z'),
  /* ... */

  /* No script set. */
  HB_SCRIPT_INVALID				= HB_TAG_NONE,

  /* Dummy values to ensure any hb_tag_t value can be passed/stored as hb_script_t
   * without risking undefined behavior.  Include both a signed and unsigned max,
   * since technically enums are int, and indeed, hb_script_t ends up being signed.
   * See this thread for technicalities:
   *
   *   http://lists.freedesktop.org/archives/harfbuzz/2014-March/004150.html
   */
  _HB_SCRIPT_MAX_VALUE				= HB_TAG_MAX, /*< skip >*/
  _HB_SCRIPT_MAX_VALUE_SIGNED			= HB_TAG_MAX_SIGNED /*< skip >*/
} hb_script_t;

hb_script_t
hb_script_from_iso15924_tag (hb_tag_t tag);

hb_script_t
hb_script_from_string (const char *str, int len);

hb_tag_t
hb_script_to_iso15924_tag (hb_script_t script);

hb_direction_t
hb_script_get_horizontal_direction (hb_script_t script);

typedef void (*hb_destroy_func_t) (void *user_data);

typedef struct hb_feature_t {
  hb_tag_t      tag;
  uint32_t      value;
  unsigned int  start;
  unsigned int  end;
} hb_feature_t;

hb_bool_t
hb_feature_from_string (const char *str, int len,
                        hb_feature_t *feature);

void
hb_feature_to_string (hb_feature_t *feature,
                      char *buf, unsigned int size);

typedef struct hb_variation_t {
  hb_tag_t tag;
  float    value;
} hb_variation_t;

/* ---- hb-unicode.h ---- */

/* ---- hb-blob.h ---- */
typedef enum {
  HB_MEMORY_MODE_DUPLICATE,
  HB_MEMORY_MODE_READONLY,
  HB_MEMORY_MODE_WRITABLE,
  HB_MEMORY_MODE_READONLY_MAY_MAKE_WRITABLE
} hb_memory_mode_t;

typedef struct hb_blob_t hb_blob_t;

hb_blob_t *
hb_blob_create (const char        *data,
                unsigned int       length,
                hb_memory_mode_t   mode,
                void              *user_data,
                hb_destroy_func_t  destroy);

hb_blob_t *
hb_blob_reference (hb_blob_t *blob);

void
hb_blob_destroy (hb_blob_t *blob);

unsigned int
hb_blob_get_length (hb_blob_t *blob);

const char *
hb_blob_get_data (hb_blob_t *blob, unsigned int *length);

/* ---- hb-face.h ---- */
typedef struct hb_face_t hb_face_t;

hb_face_t *
hb_face_create (hb_blob_t    *blob,
                unsigned int  index);

hb_face_t *
hb_face_reference (hb_face_t *face);

void
hb_face_destroy (hb_face_t *face);

hb_blob_t *
hb_face_reference_blob (hb_face_t *face);

void
hb_face_set_index (hb_face_t *face,
                   unsigned int index);

unsigned int
hb_face_get_index (hb_face_t *face);

void
hb_face_set_upem (hb_face_t *face,
                  unsigned int upem);

unsigned int
hb_face_get_upem (hb_face_t *face);

void
hb_face_set_glyph_count (hb_face_t    *face,
                         unsigned int  glyph_count);

unsigned int
hb_face_get_glyph_count (hb_face_t *face);

/* ---- hb-font.h ---- */
typedef struct hb_font_t hb_font_t;
typedef struct hb_font_funcs_t hb_font_funcs_t;

hb_font_funcs_t *
hb_font_funcs_create (void);

typedef struct hb_font_extents_t
{
  hb_position_t ascender; /* typographic ascender. */
  hb_position_t descender; /* typographic descender. */
  hb_position_t line_gap; /* suggested line spacing gap. */
  /*< private >*/
  hb_position_t reserved9;
  hb_position_t reserved8;
  hb_position_t reserved7;
  hb_position_t reserved6;
  hb_position_t reserved5;
  hb_position_t reserved4;
  hb_position_t reserved3;
  hb_position_t reserved2;
  hb_position_t reserved1;
} hb_font_extents_t;

typedef struct hb_glyph_extents_t
{
  hb_position_t x_bearing; /* left side of glyph from origin. */
  hb_position_t y_bearing; /* top side of glyph from origin. */
  hb_position_t width; /* distance from left to right side. */
  hb_position_t height; /* distance from top to bottom side. */
} hb_glyph_extents_t;

hb_bool_t
hb_font_get_h_extents (hb_font_t *font,
                       hb_font_extents_t *extents);

hb_bool_t
hb_font_get_v_extents (hb_font_t *font,
                       hb_font_extents_t *extents);

hb_bool_t
hb_font_get_nominal_glyph (hb_font_t *font,
                           hb_codepoint_t unicode,
                           hb_codepoint_t *glyph);

hb_bool_t
hb_font_get_variation_glyph (hb_font_t *font,
                             hb_codepoint_t unicode, hb_codepoint_t variation_selector,
                             hb_codepoint_t *glyph);

hb_position_t
hb_font_get_glyph_h_advance (hb_font_t *font,
                             hb_codepoint_t glyph);

hb_position_t
hb_font_get_glyph_v_advance (hb_font_t *font,
                             hb_codepoint_t glyph);

hb_bool_t
hb_font_get_glyph_h_origin (hb_font_t *font,
                            hb_codepoint_t glyph,
                            hb_position_t *x, hb_position_t *y);

hb_bool_t
hb_font_get_glyph_v_origin (hb_font_t *font,
                            hb_codepoint_t glyph,
                            hb_position_t *x, hb_position_t *y);

hb_position_t
hb_font_get_glyph_h_kerning (hb_font_t *font,
                             hb_codepoint_t left_glyph,
                             hb_codepoint_t right_glyph);

hb_position_t
hb_font_get_glyph_v_kerning (hb_font_t *font,
                             hb_codepoint_t top_glyph,
                             hb_codepoint_t bottom_glyph);

hb_bool_t
hb_font_get_glyph_extents (hb_font_t *font,
                           hb_codepoint_t glyph,
                           hb_glyph_extents_t *extents);

hb_bool_t
hb_font_get_glyph (hb_font_t *font,
                   hb_codepoint_t unicode, hb_codepoint_t variation_selector,
                   hb_codepoint_t *glyph);

void
hb_font_get_extents_for_direction (hb_font_t *font,
                                   hb_direction_t direction,
                                   hb_font_extents_t *extents);

void
hb_font_get_glyph_advance_for_direction (hb_font_t *font,
                                         hb_codepoint_t glyph,
                                         hb_direction_t direction,
                                         hb_position_t *x, hb_position_t *y);

void
hb_font_get_glyph_origin_for_direction (hb_font_t *font,
                                        hb_codepoint_t glyph,
                                        hb_direction_t direction,
                                        hb_position_t *x, hb_position_t *y);

void
hb_font_get_glyph_kerning_for_direction (hb_font_t *font,
                                         hb_codepoint_t first_glyph, hb_codepoint_t second_glyph,
                                         hb_direction_t direction,
                                         hb_position_t *x, hb_position_t *y);

hb_bool_t
hb_font_get_glyph_extents_for_origin (hb_font_t *font,
                                      hb_codepoint_t glyph,
                                      hb_direction_t direction,
                                      hb_glyph_extents_t *extents);

hb_font_t *
hb_font_create (hb_face_t *face);

hb_font_t *
hb_font_reference (hb_font_t *font);

void
hb_font_destroy (hb_font_t *font);

void
hb_font_set_face (hb_font_t *font,
                  hb_face_t *face);

hb_face_t *
hb_font_get_face (hb_font_t *font);

void
hb_font_set_scale (hb_font_t *font,
                   int x_scale,
                   int y_scale);

void
hb_font_get_scale (hb_font_t *font,
                   int *x_scale,
                   int *y_scale);

void
hb_font_set_ppem (hb_font_t *font,
                  unsigned int x_ppem,
                  unsigned int y_ppem);

void
hb_font_get_ppem (hb_font_t *font,
                  unsigned int *x_ppem,
                  unsigned int *y_ppem);

void
hb_font_set_ptem (hb_font_t *font, float ptem);

float
hb_font_get_ptem (hb_font_t *font);

void
hb_font_set_variations (hb_font_t *font,
                        const hb_variation_t *variations,
                        unsigned int variations_length);

/* ---- hb-ft.h ---- */
hb_face_t *
hb_ft_face_create (FT_Face ft_face,
                   hb_destroy_func_t destroy);

hb_font_t *
hb_ft_font_create (FT_Face ft_face,
                   hb_destroy_func_t destroy);

FT_Face
hb_ft_font_get_face (hb_font_t *font);

void
hb_ft_font_set_load_flags (hb_font_t *font, int load_flags);

int
hb_ft_font_get_load_flags (hb_font_t *font);

/* ---- hb-buffer.h ---- */
typedef struct hb_glyph_info_t {
  hb_codepoint_t codepoint;
  hb_mask_t      mask; /* Holds hb_glyph_flags_t after hb_shape(), plus other things. */
  uint32_t       cluster;
  /*< private >*/
  hb_var_int_t   var1;
  hb_var_int_t   var2;
} hb_glyph_info_t;

typedef struct hb_glyph_position_t {
  hb_position_t  x_advance;
  hb_position_t  y_advance;
  hb_position_t  x_offset;
  hb_position_t  y_offset;
  /*< private >*/
  hb_var_int_t   var;
} hb_glyph_position_t;

typedef struct hb_segment_properties_t {
  hb_direction_t  direction;
  hb_script_t     script;
  hb_language_t   language;
  /*< private >*/
  void           *reserved1;
  void           *reserved2;
} hb_segment_properties_t;

typedef enum {
  HB_BUFFER_CONTENT_TYPE_INVALID = 0,
  HB_BUFFER_CONTENT_TYPE_UNICODE,
  HB_BUFFER_CONTENT_TYPE_GLYPHS
} hb_buffer_content_type_t;

typedef struct hb_buffer_t hb_buffer_t;

hb_buffer_t *
hb_buffer_create (void);

hb_buffer_t *
hb_buffer_reference (hb_buffer_t *buffer);

void
hb_buffer_destroy (hb_buffer_t *buffer);

void
hb_buffer_set_direction (hb_buffer_t    *buffer,
                         hb_direction_t  direction);

hb_direction_t
hb_buffer_get_direction (hb_buffer_t *buffer);

void
hb_buffer_set_script (hb_buffer_t *buffer,
                      hb_script_t  script);

hb_script_t
hb_buffer_get_script (hb_buffer_t *buffer);

void
hb_buffer_set_language (hb_buffer_t   *buffer,
                        hb_language_t  language);

hb_language_t
hb_buffer_get_language (hb_buffer_t *buffer);

void
hb_buffer_guess_segment_properties (hb_buffer_t *buffer);

typedef enum {
  HB_BUFFER_CLUSTER_LEVEL_MONOTONE_GRAPHEMES	= 0,
  HB_BUFFER_CLUSTER_LEVEL_MONOTONE_CHARACTERS	= 1,
  HB_BUFFER_CLUSTER_LEVEL_CHARACTERS		= 2,
  HB_BUFFER_CLUSTER_LEVEL_DEFAULT = HB_BUFFER_CLUSTER_LEVEL_MONOTONE_GRAPHEMES
} hb_buffer_cluster_level_t;

void
hb_buffer_set_cluster_level (hb_buffer_t               *buffer,
                             hb_buffer_cluster_level_t  cluster_level);

hb_buffer_cluster_level_t
hb_buffer_get_cluster_level (hb_buffer_t *buffer);

void
hb_buffer_reset (hb_buffer_t *buffer);

void
hb_buffer_clear_contents (hb_buffer_t *buffer);

void
hb_buffer_reverse (hb_buffer_t *buffer);

void
hb_buffer_reverse_range (hb_buffer_t *buffer,
                         unsigned int start,
                         unsigned int end);

void
hb_buffer_reverse_clusters (hb_buffer_t *buffer);

void
hb_buffer_add_utf8 (hb_buffer_t  *buffer,
                    const char   *text,
                    int           text_length,
                    unsigned int  item_offset,
                    int item_length);

void
hb_buffer_add_utf16 (hb_buffer_t    *buffer,
                     const uint16_t *text,
                     int             text_length,
                     unsigned int    item_offset,
                     int             item_length);

void
hb_buffer_add_utf32 (hb_buffer_t    *buffer,
                     const uint32_t *text,
                     int             text_length,
                     unsigned int    item_offset,
                     int             item_length);

void
hb_buffer_append (hb_buffer_t *buffer,
                  hb_buffer_t *source,
                  unsigned int start,
                  unsigned int end);

hb_bool_t
hb_buffer_set_length (hb_buffer_t  *buffer,
                      unsigned int  length);

unsigned int
hb_buffer_get_length (hb_buffer_t *buffer);

hb_glyph_info_t *
hb_buffer_get_glyph_infos (hb_buffer_t  *buffer,
                           unsigned int *length);

hb_glyph_position_t *
hb_buffer_get_glyph_positions (hb_buffer_t  *buffer,
                               unsigned int *length);

void
hb_buffer_normalize_glyphs (hb_buffer_t *buffer);

/* ---- hb-shape.h ---- */
void
hb_shape (hb_font_t           *font,
          hb_buffer_t         *buffer,
          const hb_feature_t  *features,
          unsigned int         num_features);

/* ---- hb-ot-font.h ---- */
void
hb_ot_font_set_funcs (hb_font_t *font);

/* ---- hb-version.h ---- */
void
hb_version (unsigned int *major,
            unsigned int *minor,
            unsigned int *micro);
"""

ffi = FFI()
ffi.cdef(_API)
del _API


def dlopen(_ffi, names):
    lib = None
    for name in iter(names):
        try:
            lib = _ffi.dlopen(name)
            break
        except OSError:
            pass
    if lib is None:
        raise OSError('Cannot open shared object file: ' + repr(names))
    return lib
