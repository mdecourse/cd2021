# Copyright (C) 2017 Tetsuya Miura <miute.dev@gmail.com>
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
import html
import math
import re
import shlex
import unicodedata
from decimal import Decimal, InvalidOperation

import numpy as np

from .css.screen import Screen
from .fontconfig import FontConfig
from .formatter import format_number_sequence
from .freetype import FreeType, FTFace


class CSSUtils(object):
    _ABSOLUTE_FONT_SIZE_MAP = {
        # <absolute-size> keyword: (row, scale size factor)
        'xx-small': (0, 3 / 5),
        'x-small': (1, 3 / 4),
        'small': (2, 8 / 9),
        'medium': (3, 1),
        'large': (4, 6 / 5),
        'x-large': (5, 3 / 2),
        'xx-large': (6, 2 / 1),
    }
    """dict: The scale size factor for the absolute font size."""

    _QUIRKS_FONT_SIZE_TABLE = [
        [9, 9, 9, 9, 11, 14, 18, 28],
        [9, 9, 9, 10, 11, 14, 18, 31],  # (10px) fixed
        [9, 9, 9, 11, 13, 17, 22, 34],
        [9, 9, 10, 12, 14, 18, 24, 37],  # (12px)
        [9, 9, 10, 13, 16, 20, 26, 40],  # fixed font default (13px)
        [9, 9, 11, 14, 17, 21, 28, 42],
        [9, 10, 12, 15, 17, 23, 30, 45],
        [9, 10, 13, 16, 18, 24, 32, 48],  # proportional font default (16px)
    ]

    _STRICT_FONT_SIZE_TABLE = [
        [9, 9, 9, 9, 11, 14, 18, 27],
        [9, 9, 9, 10, 12, 15, 20, 30],
        [9, 9, 10, 11, 13, 17, 22, 33],
        [9, 9, 10, 12, 14, 18, 24, 36],
        [9, 10, 12, 13, 16, 20, 26, 39],
        [9, 10, 12, 14, 17, 21, 28, 42],
        [9, 10, 13, 15, 18, 23, 30, 45],
        [9, 10, 13, 16, 18, 24, 32, 48],  # proportional font default (16px)
    ]
    # See https://dom.spec.whatwg.org/#concept-document-mode
    """list: The table of the font size for the absolute font size."""

    _FONT_SIZE_TABLE_MAX = 16
    _FONT_SIZE_TABLE_MIN = 9
    _MINIMUM_FONT_SIZE = 10

    _FONT_WEIGHT_MAP = {
        'normal': 400,
        'bold': 700,
    }

    _INHERITED_WEIGHT_LIST = [100, 200, 300, 400, 500, 600, 700, 800, 900]
    _BOLDER_WEIGHT_LIST = [400, 400, 400, 700, 700, 900, 900, 900, 900]
    _LIGHTER_WEIGHT_LIST = [100, 100, 100, 100, 100, 400, 400, 700, 700]

    _RE_COLLAPSIBLE_WHITESPACE = re.compile(r'(\x20){2,}', re.MULTILINE)
    _RE_SEGMENT_BREAKS = re.compile(r'(\r\n|\r|\n)+', re.MULTILINE)
    _RE_PRECEDING_TAB_WHITESPACE = re.compile(r'^(\x20|\t)+', re.MULTILINE)
    _RE_FOLLOWING_TAB_WHITESPACE = re.compile(r'(\x20|\t)+$', re.MULTILINE)

    @staticmethod
    def compute_font_size(element, inherited_size=None, inherited_style=None):
        if inherited_style is None:
            inherited_style = element.get_inherited_style()

        # 'font-size' property
        # Value: <absolute-size> | <relative-size> | <length> | <percentage>
        # Initial: medium
        # Inherited: yes
        # Percentages: refer to parent element's font size
        font_size = inherited_style['font-size']
        if font_size in CSSUtils._ABSOLUTE_FONT_SIZE_MAP:
            # <absolute-size>
            # Value: xx-small | x-small | small | medium | large | x-large
            #  | xx-large
            column, scale_factor = CSSUtils._ABSOLUTE_FONT_SIZE_MAP[
                font_size]
            medium_size = Font.default_font_size
            if CSSUtils._FONT_SIZE_TABLE_MIN <= medium_size \
                    <= CSSUtils._FONT_SIZE_TABLE_MAX:
                row = int(medium_size - CSSUtils._FONT_SIZE_TABLE_MIN)
                px = CSSUtils._QUIRKS_FONT_SIZE_TABLE[row][column]
            else:
                px = scale_factor * medium_size
        elif font_size in ['larger', 'smaller']:
            # <relative-size>
            # Value: larger | smaller
            if inherited_size is None:
                inherited_size = Font.default_font_size
            parent_sequence = list()
            parent = element.getparent()
            while parent is not None:
                parent_sequence.insert(0, parent)
                parent = parent.getparent()
            for parent in iter(parent_sequence):
                value = parent.get('font-size')
                if value is None:
                    continue
                elif value in ['larger', 'smaller']:
                    scale_factor = 1.2 if font_size == 'larger' else 1 / 1.2
                    inherited_size *= scale_factor
                else:
                    inherited_size = CSSUtils.compute_font_size(
                        parent,
                        inherited_size,
                        {'font-size': value})
            px = inherited_size
        else:
            # <length> or <percentage>
            # See https://drafts.csswg.org/css-values-3/#lengths
            fs = SVGLength(font_size, context=element)
            px = fs.value()

        if px < CSSUtils._MINIMUM_FONT_SIZE:
            px = CSSUtils._MINIMUM_FONT_SIZE
        return float(px)

    @staticmethod
    def compute_font_size_adjust(style):
        # 'font-size-adjust' property
        # Value: 'none' | <number>
        # Initial: none
        # Inherited: yes
        # Percentages: N/A
        font_size_adjust = style['font-size-adjust']
        if font_size_adjust != 'none':
            font_size_adjust = SVGLength(font_size_adjust).value()
        return font_size_adjust

    @staticmethod
    def compute_font_weight(element,
                            inherited_weight=None, inherited_style=None):
        if inherited_style is None:
            inherited_style = element.get_inherited_style()

        # 'font-weight' property
        # Value: normal | bold | bolder | lighter
        #  | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900
        # Initial: normal
        # Inherited: yes
        # Percentages: N/A
        font_weight = inherited_style['font-weight']
        if font_weight in ['bolder', 'lighter']:
            # <relative-weight>
            # Value: bolder | lighter
            if inherited_weight is None:
                inherited_weight = Font.default_font_weight
            parent_sequence = list()
            parent = element.getparent()
            while parent is not None:
                parent_sequence.insert(0, parent)
                parent = parent.getparent()
            for parent in iter(parent_sequence):
                value = parent.get('font-weight')
                if value is None:
                    continue
                elif value in ['bolder', 'lighter']:
                    xp = CSSUtils._INHERITED_WEIGHT_LIST
                    fp = CSSUtils._BOLDER_WEIGHT_LIST if value == 'bolder' \
                        else CSSUtils._LIGHTER_WEIGHT_LIST
                    inherited_weight = np.interp(inherited_weight, xp, fp)
                else:
                    inherited_weight = CSSUtils.compute_font_weight(
                        parent,
                        inherited_weight,
                        {'font-weight': value})
            weight = inherited_weight
        else:
            # <absolute-weight>
            weight = CSSUtils._FONT_WEIGHT_MAP.get(font_weight, font_weight)

        return int(weight)

    @staticmethod
    def compute_line_height(element, computed_style=None):
        if computed_style is None:
            computed_style = element.get_computed_style()

        # 'line-height' property
        # Value: normal | <number> | <length> | <percentage> | inherit
        # Initial: normal
        # Inherited: yes
        # Percentages: refer to the font size of the element itself
        value = computed_style['line-height']
        font_size = computed_style['font-size']
        if value == 'normal':
            line_height = 1.2 * font_size
        else:
            h = SVGLength(value, context=element)
            if h.unit == SVGLength.TYPE_PERCENTAGE:
                # <percentage>
                line_height = (h.value(SVGLength.TYPE_PERCENTAGE) / 100
                               * font_size)
            else:
                # <length> or <number>
                line_height = h.value()
        return line_height

    @staticmethod
    def get_value(element, key, default=None):
        context = element
        while context is not None:
            value = context.get(key, default)
            if value == 'auto' and key in ['width', 'height']:
                # See https://drafts.csswg.org/css2/visudet.html#the-width-property
                local_name = context.local_name
                if local_name == 'svg':
                    return '100%', context
                elif local_name == 'image':
                    # TODO: compute width/height for 'image' element.
                    raise NotImplementedError
                else:
                    return '0', context
            elif value is not None and value != 'inherit':
                return value, context
            context = context.getparent()
        return None, element

    @staticmethod
    def normalize_text_content(element, text, style, prev_text=None,
                               first=False, tail=False):
        """Apply white-space processing to a text."""
        _ = element  # reserved

        def _is_hangul(ch):
            return (('\uAC00' <= ch <= '\uD7AF')
                    or ('\u1100' <= ch <= '\u11FF')
                    or ('\u3130' <= ch <= '\u318F')
                    or ('\uA960' <= ch <= '\uA97F')
                    or ('\uD7B0' <= ch <= '\uD7FF'))

        def _transform_segment_break(_text, _style):
            # See https://drafts.csswg.org/css-text-3/#line-break-transform
            _white_space = _style['white-space']
            if _white_space in ['pre', 'pre-wrap', 'pre-line']:
                _out_text = _text.replace('\r\n', '\n').replace('\r', '\n')
                return _out_text

            # white-space: normal | nowrap
            _break_positions = list()
            for _it in CSSUtils._RE_SEGMENT_BREAKS.finditer(_text):
                _break_positions.append(_it.span(0))
            if len(_break_positions) == 0:
                return _text

            _out_text = ''
            _last = 0
            _max_length = len(_text)
            for _start, _end in _break_positions:
                _out_text += _text[_last:_start]
                if ((_start > 0 and _text[_start - 1] == '\u200B')
                        or (_end < _max_length
                            and _text[_end] == '\u200B')):
                    pass  # remove segment breaks
                elif (_start > 0 and _end < _max_length
                      and unicodedata.east_asian_width(
                            _text[_start - 1]) in 'FWH'
                      and not _is_hangul(_text[_start - 1])
                      and unicodedata.east_asian_width(
                            _text[_end]) in 'FWH'
                      and not _is_hangul(_text[_end])):
                    pass  # remove segment breaks
                else:
                    _out_text += ' '  # convert to a space (U+0020)
                _last = _end
            else:
                _out_text += _text[_last:]
            return _out_text

        # 'white-space' property
        # Value: normal | pre | nowrap | pre-wrap | pre-line
        # Initial: normal
        # Inherited: yes
        # Percentages: N/A
        white_space = style['white-space']
        out_text = html.unescape(text)

        # FIXME: fix white-space processing.
        if white_space in ['normal', 'nowrap', 'pre-line']:
            out_text = CSSUtils._RE_PRECEDING_TAB_WHITESPACE.sub(
                '', out_text)
            out_text = CSSUtils._RE_FOLLOWING_TAB_WHITESPACE.sub(
                '', out_text)
            out_text = _transform_segment_break(out_text, style)
            out_text = out_text.replace('\t', ' ')
            out_text = CSSUtils._RE_COLLAPSIBLE_WHITESPACE.sub(
                ' ', out_text)
        if white_space in ['pre', 'pre-wrap']:
            out_text = _transform_segment_break(out_text, style)

        if prev_text is not None:
            if prev_text.endswith(' ') and out_text.startswith(' '):
                out_text = out_text.lstrip()
            elif not prev_text.endswith(' ') and not out_text.startswith(' '):
                out_text = ' ' + out_text
        if first:
            out_text = out_text.lstrip(' ')
        # if len(element) == 0:
        if tail:
            out_text = out_text.rstrip(' ')

        return out_text

    @staticmethod
    def parse_font(value):
        """Parses a value of the shorthand 'font' property.

        Arguments:
            value (str):
        Returns:
            dict:
        """
        # 'font' property
        # Value: [ [ <font-style> || <font-variant-css21>
        #  || <font-weight> || <font-stretch> ]? <font-size>
        #  [ / <line-height> ]? <font-family> ]
        #  | caption | icon | menu | message-box | small-caption | status-bar
        items = shlex.split(value)
        if len(items) == 0:
            return {}
        for item in iter(items):
            # system font
            if item in ['caption', 'icon', 'menu', 'message-box',
                        'small-caption', 'status-bar']:
                return {}

        style = dict({
            'font-family': [],
            'font-kerning': Font.CSS_DEFAULT_FONT_KERNING,
            'font-language-override': Font.CSS_DEFAULT_FONT_LANGUAGE_OVERRIDE,
            'font-size': Font.CSS_DEFAULT_FONT_SIZE,
            'font-size-adjust': Font.CSS_DEFAULT_FONT_SIZE_ADJUST,
            'font-stretch': Font.CSS_DEFAULT_FONT_STRETCH,
            'font-style': Font.CSS_DEFAULT_FONT_STYLE,
            'font-variant': Font.CSS_DEFAULT_FONT_VARIANT,
            'font-weight': Font.CSS_DEFAULT_FONT_WEIGHT,
            'line-height': Font.CSS_DEFAULT_LINE_HEIGHT,
        })

        # 'font-family' property
        font_family = list([items.pop()])
        delimiter = False
        while len(items) > 0:
            item = items[-1]
            if item == ',':
                # 'a_,_b' -> ['a', ',', 'b']
                delimiter = True
            elif delimiter or item.endswith(','):
                font_family.insert(0, item)
                delimiter = False
            else:
                break
            items.pop()
        style['font-family'] = CSSUtils.parse_font_family(font_family)

        # 'font-size' and 'line-height' properties
        try:
            item = items.pop()
        except IndexError:
            return {}
        if item.find('/') != -1:
            # 'font-size' [/ 'line-height']
            parts = item.split('/')
            style['font-size'] = parts[0]
            style['line-height'] = parts[1]
        else:
            style['font-size'] = item

        while len(items) > 0:
            item = items.pop(0)
            if item == 'normal':
                pass
            elif item in ['italic', 'oblique']:
                # 'font-style' property
                style['font-style'] = item
            elif item in ['small-caps']:
                # 'font-variant-css21' property
                style['font-variant'] = item
            elif item in ['bold', 'bolder', 'lighter', '100', '200', '300',
                          '400', '500', '600', '700', '800', '900']:
                # 'font-weight' property
                style['font-weight'] = item
            elif item in ['ultra-condensed', 'extra-condensed',
                          'condensed', 'semi-condensed', 'semi-expanded',
                          'expanded', 'extra-expanded', 'ultra-expanded']:
                # 'font-stretch' property
                style['font-stretch'] = item
            else:
                break

        return style

    @staticmethod
    def parse_font_family(value):
        """Parses a value of the 'font-family' property.

        Arguments:
            value (str, list[str]):
        Returns:
            list[str]:
        """
        # 'font-family' property
        # Value: [[ <family-name> | <generic-family> ]
        #  [, [ <family-name>| <generic-family>] ]* ] | inherit
        # Initial: depends on user agent
        # Inherited: yes
        # Percentages: N/A
        if isinstance(value, list):
            items = value
        elif isinstance(value, str):
            if '"' in value or '\'' in value:
                items = shlex.split(value)
            else:
                items = [value]
        else:
            raise TypeError('Expected str or list, got {}'.format(
                type(value)))
        font_family = list()
        for item in iter(items):
            for name in iter(item.split(',')):
                name = name.strip()
                if len(name) > 0:
                    font_family.append(name)
        return font_family

    @staticmethod
    def parse_font_feature_settings(value):
        # 'font-feature-settings' property
        # Value: normal | <feature-tag-value>#
        # <feature-tag-value> = <string> [ <integer> | on | off ]?
        # Initial: normal
        features = dict()
        if value == 'normal':
            return features
        tags = value.split(',')
        for tag_value in tags:
            items = tag_value.split()
            tag = items[0]
            if tag[0] == tag[-1] and tag[0] in '"\'':
                tag = tag[1:-1]
            if len(tag) != 4:
                continue  # invalid tag
            invalid_tag = False
            for ch in tag:
                if not (0x20 <= ord(ch) <= 0x7e):
                    invalid_tag = True
                    break
            if invalid_tag:
                continue
            if len(items) >= 2:
                if items[1].isdigit():
                    sw = int(items[1])
                elif items[1] == 'on':
                    sw = 1
                elif items[1] == 'off':
                    sw = 0
                else:
                    continue  # invalid value
            else:
                sw = 1
            features[tag] = sw

        return features

    @staticmethod
    def parse_font_variant(value):
        """Parses a value of the shorthand 'font-variant' property.

        Arguments:
            value (str):
        Returns:
            dict:
        """
        # 'font-variant' property
        # Value: normal | none
        #  | [ <common-lig-values> || <discretionary-lig-values>
        #  || <historical-lig-values> || <contextual-alt-values>
        #  || stylistic(<feature-value-name>) || historical-forms
        #  || styleset(<feature-value-name> #)
        #  || character-variant(<feature-value-name> #)
        #  || swash(<feature-value-name>) || ornaments(<feature-value-name>)
        #  || annotation(<feature-value-name>)
        #  || [ small-caps | all-small-caps | petite-caps | all-petite-caps
        #  | unicase | titling-caps ]
        #  || <numeric-figure-values> || <numeric-spacing-values>
        #  || <numeric-fraction-values> || ordinal || slashed-zero
        #  || <east-asian-variant-values> || <east-asian-width-values>
        #  || ruby || [ sub | super ] ]
        style = dict({
            'font-variant-alternates': None,
            'font-variant-caps': 'normal',
            'font-variant-east-asian': None,
            'font-variant-ligatures': None,
            'font-variant-numeric': None,
            'font-variant-position': 'normal',
        })
        if value == 'normal':
            style['font-variant-alternates'] = ['normal']
            style['font-variant-east-asian'] = ['normal']
            style['font-variant-ligatures'] = ['normal']
            style['font-variant-numeric'] = ['normal']
            return style
        elif value == 'none':
            style['font-variant-alternates'] = ['normal']
            style['font-variant-east-asian'] = ['normal']
            style['font-variant-ligatures'] = ['none']
            style['font-variant-numeric'] = ['normal']
            return style

        font_variant_alternates = list()
        font_variant_east_asian = list()
        font_variant_ligatures = list()
        font_variant_numeric = list()
        items = value.split()
        while len(items) > 0:
            item = items.pop(0)
            if item in ['common-ligatures', 'no-common-ligatures',
                        'discretionary-ligatures',
                        'no-discretionary-ligatures',
                        'historical-ligatures', 'no-historical-ligatures',
                        'contextual', 'no-contextual']:
                font_variant_ligatures.append(item)
            elif (item in ['historical-forms']
                  or item.startswith('stylistic(')
                  or item.startswith('styleset(')
                  or item.startswith('character-variant(')
                  or item.startswith('swash(')
                  or item.startswith('ornaments(')
                  or item.startswith('annotation(')):
                font_variant_alternates.append(item)
            elif item in ['small-caps', 'all-small-caps', 'petite-caps',
                          'all-petite-caps', 'unicase', 'titling-caps']:
                style['font-variant-caps'] = item
            elif item in ['jis78', 'jis83', 'jis90', 'jis04', 'simplified',
                          'traditional',
                          'full-width', 'proportional-width', 'ruby']:
                font_variant_east_asian.append(item)
            elif item in ['lining-nums', 'oldstyle-nums',
                          'proportional-nums', 'tabular-nums',
                          'diagonal-fractions', 'stacked-fractions',
                          'ordinal', 'slashed-zero']:
                font_variant_numeric.append(item)
            elif item in ['sub', 'super']:
                style['font-variant-position'] = item

        if len(font_variant_alternates) == 0:
            font_variant_alternates.append('normal')
        style['font-variant-alternates'] = font_variant_alternates

        if len(font_variant_east_asian) == 0:
            font_variant_east_asian.append('normal')
        style['font-variant-east-asian'] = font_variant_east_asian

        if len(font_variant_ligatures) == 0:
            font_variant_ligatures.append('normal')
        style['font-variant-ligatures'] = font_variant_ligatures

        if len(font_variant_numeric) == 0:
            font_variant_numeric.append('normal')
        style['font-variant-numeric'] = font_variant_numeric

        return style


class Font(object):
    CSS_DEFAULT_FONT_KERNING = 'auto'
    CSS_DEFAULT_FONT_LANGUAGE_OVERRIDE = 'normal'
    CSS_DEFAULT_FONT_SIZE = 'medium'
    CSS_DEFAULT_FONT_SIZE_ADJUST = 'none'
    CSS_DEFAULT_FONT_STRETCH = 'normal'
    CSS_DEFAULT_FONT_STYLE = 'normal'
    CSS_DEFAULT_FONT_VARIANT = 'normal'
    CSS_DEFAULT_FONT_WEIGHT = 'normal'
    CSS_DEFAULT_LINE_HEIGHT = 'normal'

    WEIGHT_THIN = 100
    WEIGHT_EXTRA_LIGHT = 200
    WEIGHT_ULTRA_LIGHT = 200
    WEIGHT_LIGHT = 300
    WEIGHT_NORMAL = 400
    WEIGHT_MEDIUM = 500
    WEIGHT_DEMI_BOLD = 600
    WEIGHT_SEMI_BOLD = 600
    WEIGHT_BOLD = 700
    WEIGHT_EXTRA_BOLD = 800
    WEIGHT_ULTRA_BOLD = 800
    WEIGHT_BLACK = 900
    WEIGHT_HEAVY = 900

    default_font_family = 'sans-serif'
    default_font_size = 16
    default_font_weight = WEIGHT_NORMAL
    generic_font_family = [
        'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace',
    ]

    def __init__(self, context):
        """Constructs a Font object.

        Arguments:
            context (Element): An Element object.
        """
        self._context = context
        self._style = context.get_computed_style()
        self._face = FontManager.get_face(self._style,
                                          context.owner_document,
                                          context.text)

    def __eq__(self, other):
        if not isinstance(other, Font):
            return NotImplemented
        style = self._style
        other_style = other._style
        return (style['font-family'] == other_style['font-family']
                and style['font-size'] == other_style['font-size']
                and style['font-size-adjust'] == other_style[
                    'font-size-adjust']
                and style['font-stretch'] == other_style['font-stretch']
                and style['font-style'] == other_style['font-style']
                and style['font-weight'] == other_style['font-weight'])

    def __repr__(self):
        return (
            "('family': '{}', 'ascent': {}, 'descent': {},"
            " 'cap_height': {}, 'ch_width': {}, 'height': {},"
            " 'ic_width': {}, 'line_height': {}, 'x_height': {})".format(
                self.family, self.ascent, self.descent,
                self.cap_height, self.ch_advance, self.height,
                self.ic_advance, self.line_height, self.x_height))

    @property
    def ascent(self):
        return self._face.ascender / 64

    @property
    def attributes(self):
        return self._style

    @property
    def cap_height(self):
        for ch in 'Hh':
            index = self._face.get_char_index(ch)
            if index != 0:
                self._face.load_char(ch, FreeType.FT_LOAD_NO_BITMAP)
                return self._face.glyph.metrics.vert_advance / 64
        return self._face.size.height / 64

    @property
    def ch_advance(self):
        """float: An advance measure of the '0' (ZERO, U+0030)."""
        self._face.load_char('\u0030', FreeType.FT_LOAD_NO_BITMAP)
        writing_mode = self._style['writing-mode']
        if writing_mode in ['horizontal-tb', 'lr', 'lr-tb', 'rl', 'rl-tb']:
            # horizontal
            return self._face.glyph.metrics.hori_advance / 64
        else:
            # vertical
            text_orientation = self._style['text-orientation']
            if text_orientation in ['upright']:
                return 0  # 1em
            return self._face.glyph.metrics.vert_advance / 64

    @property
    def context(self):
        return self._context

    @property
    def descent(self):
        return self._face.descender / 64

    @property
    def face(self):
        """freetype.FTFace: A FreeType FTFace object."""
        return self._face

    @property
    def family(self):
        return self._face.family_name

    @property
    def height(self):
        return self._face.size.metrics.y_ppem

    @property
    def ic_advance(self):
        """float: An advance measure of the '水' (CJK water ideograph, U+6C34).
        """
        index = self._face.get_char_index('\u6c34')
        if index == 0:
            return 0  # 1em
        self._face.load_glyph(index, FreeType.FT_LOAD_NO_BITMAP)
        writing_mode = self._style['writing-mode']
        if writing_mode in ['horizontal-tb', 'lr', 'lr-tb', 'rl', 'rl-tb']:
            # horizontal
            return self._face.glyph.metrics.hori_advance / 64
        else:
            # vertical
            text_orientation = self._style['text-orientation']
            if text_orientation in ['upright']:
                return 0  # 1em
            return self._face.glyph.metrics.vert_advance / 64

    @property
    def line_height(self):
        return self._face.size.metrics.height / 64

    @property
    def x_height(self):
        self._face.load_char('x', FreeType.FT_LOAD_NO_BITMAP)
        return self._face.glyph.metrics.height / 64

    def set_point_size(self, width, height, hori_resolution=0,
                       vert_resolution=0):
        self._face.request_size(FreeType.FT_SIZE_REQUEST_TYPE_NOMINAL,
                                width, height,
                                hori_resolution, vert_resolution)


class FontManager(object):
    @staticmethod
    def __debug_print(matched):
        # for style in matched:
        #     print(style)
        # print('----')
        pass

    @staticmethod
    def _find_face(style, text=None):
        font_family_names = list()
        for font_family_name in iter(style['font-family']):
            name = FontManager.match(font_family_name)
            if name is not None and name not in font_family_names:
                font_family_names.append(name)
        font_stretch = style['font-stretch']
        fc_width = FontConfig.FC_WIDTH_MAP.get(font_stretch)
        font_style = style['font-style']
        font_weight = style['font-weight']
        font_size = style['font-size']
        # font_size_adjust = style['font-size-adjust']

        for font_family_name in iter(font_family_names):
            # narrow down by font family name
            matched = FontManager.list(font_family_name)
            if len(matched) == 0:
                continue
            FontManager.__debug_print(matched)

            # narrow down by 'font-stretch' property (fontconfig width)
            # font-stretch : normal | ultra-condensed
            #  | extra-condensed | condensed | semi-condensed | semi-expanded
            #  | expanded | extra-expanded | ultra-expanded
            group = [x for x in iter(matched) if
                     fc_width == x[FontConfig.FC_WIDTH]]
            if len(group) == 0 and fc_width is not None:
                # narrow down by nearest font width
                fc_width_table = set(
                    [x[FontConfig.FC_WIDTH] for x in iter(matched)])
                if (font_stretch == 'normal'
                        or font_stretch.endswith('condensed')):
                    # 'normal' or '*condensed'
                    fc_width_table = sorted(fc_width_table)
                elif font_stretch.endswith('expanded'):
                    # '*expanded'
                    fc_width_table = sorted(fc_width_table, reverse=True)
                index = np.abs(
                    np.asarray(fc_width_table) - fc_width).argmin()
                group = [x for x in iter(matched) if
                         fc_width_table[index] == x[FontConfig.FC_WIDTH]]
            if len(group) == 0:
                continue
            else:
                matched = group
                FontManager.__debug_print(matched)

            # narrow down by 'font-style' property (fontconfig slant)
            # font-style: normal | italic | oblique
            if font_style == 'italic':
                order = ['italic', 'oblique', 'normal']
            elif font_style == 'oblique':
                order = ['oblique', 'italic', 'normal']
            else:
                order = ['normal', 'oblique', 'italic']
            for include_style in iter(order):
                fc_slant = FontConfig.FC_SLANT_MAP.get(include_style)
                group = [x for x in iter(matched) if
                         fc_slant == x[FontConfig.FC_SLANT]]
                if len(group) > 0:
                    matched = group
                    break
            FontManager.__debug_print(matched)

            # narrow down by 'font-weight' property
            # font-weight : normal | bold | bolder | lighter
            #  | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900
            group = [x for x in iter(matched) if
                     font_weight == x[FontConfig.FC_WEIGHT]]
            if len(group) == 0:
                # FIXME: narrow down by nearest font weight.
                fc_weight_table = set(
                    [x[FontConfig.FC_WEIGHT] for x in iter(matched)])
                if font_weight < Font.WEIGHT_NORMAL:  # <400
                    fc_weight_table = sorted(fc_weight_table, reverse=True)
                else:  # >=400
                    fc_weight_table = sorted(fc_weight_table)
                index = np.abs(
                    np.asarray(fc_weight_table) - font_weight).argmin()
                group = [x for x in iter(matched) if
                         fc_weight_table[index] == x[
                             FontConfig.FC_WEIGHT]]
            if len(group) == 0:
                continue
            else:
                matched = group
            FontManager.__debug_print(matched)

            # narrow down by 'font-size' property (fontconfig pixelsize)
            group = [x for x in iter(matched) if
                     font_size == x[FontConfig.FC_PIXEL_SIZE]]
            if len(group) == 0:
                pixel_size_table = sorted(set(
                    [x[FontConfig.FC_PIXEL_SIZE] for x in iter(matched)]
                ))
                index = np.abs(
                    np.asarray(pixel_size_table) - font_size).argmin()
                group = [x for x in iter(matched) if
                         pixel_size_table[index] == x[
                             FontConfig.FC_PIXEL_SIZE]]
            if len(group) == 0:
                continue
            else:
                matched = group
            if len(matched) > 1:
                # FIXME: narrow down to a single font face.
                # (e.g. 'Courier' / Windows)
                matched = sorted(matched,
                                 key=lambda x: x[FontConfig.FC_FILE])
            FontManager.__debug_print(matched)

            # check the glyph
            for fc in iter(matched):
                face = FTFace.new_face(fc[FontConfig.FC_FILE],
                                       fc[FontConfig.FC_INDEX])
                glyph_not_found = False
                if text is not None:
                    for ch in iter(text):
                        if ch in ['\t', '\r', '\n', '\x20']:
                            continue
                        index = face.get_char_index(ch)
                        if index == 0:
                            glyph_not_found = True
                            break
                        # for encoding in [FreeType.FT_ENCODING_MS_SYMBOL,
                        #                  FreeType.FT_ENCODING_ADOBE_CUSTOM,
                        #                  FreeType.FT_ENCODING_UNICODE]:
                        #     index = face.get_char_index(ch)
                        #     if index == 0:
                        #         face.select_charmap(encoding)
                        #     else:
                        #         if face.charmap.encoding \
                        #                 != FreeType.FT_ENCODING_UNICODE:
                        #             face.select_charmap(
                        #                 FreeType.FT_ENCODING_UNICODE)
                        #         break
                        # else:
                        #     glyph_not_found = True
                        # if glyph_not_found:
                        #     break
                if not glyph_not_found:
                    return face

        # fallback font
        filename = FontConfig.match(Font.default_font_family, '%{file}')[0]
        face = FTFace.new_face(filename)
        return face

    @staticmethod
    def get_face(style, owner_document, text=None):
        face = FontManager._find_face(style, text)
        face.select_charmap(FreeType.FT_ENCODING_UNICODE)
        pixel_size = style['font-size']
        point_size = int(SVGLength(pixel_size).value(SVGLength.TYPE_PT) * 64)
        if (owner_document is not None
                and owner_document.default_view is not None):
            screen = owner_document.default_view.screen
            horizontal_resolution = screen.horizontal_resolution
            vertical_resolution = screen.vertical_resolution
        else:
            horizontal_resolution = Screen.DEFAULT_HORIZONTAL_RESOLUTION
            vertical_resolution = Screen.DEFAULT_VERTICAL_RESOLUTION
        face.request_size(FreeType.FT_SIZE_REQUEST_TYPE_NOMINAL,
                          0,
                          point_size,
                          horizontal_resolution,
                          vertical_resolution)
        return face

    @staticmethod
    def list(family):
        fc_elements = [FontConfig.FC_FAMILY, FontConfig.FC_FILE,
                       FontConfig.FC_FONT_FORMAT, FontConfig.FC_INDEX,
                       FontConfig.FC_PIXEL_SIZE, FontConfig.FC_SLANT,
                       FontConfig.FC_WEIGHT, FontConfig.FC_WIDTH]
        fc_format = '\t'.join(['%{{{}}}'.format(x) for x in fc_elements])
        matched = FontConfig.list(family, fc_elements, fc_format)
        style_sequence = list()
        for line in iter(matched):
            items = line.split('\t')
            style = dict()
            style[FontConfig.FC_FAMILY] = items[0]
            style[FontConfig.FC_FILE] = items[1]
            style[FontConfig.FC_FONT_FORMAT] = items[2]
            style[FontConfig.FC_INDEX] = int(items[3])
            pixel_size = float(items[4]) if len(items[4]) > 0 else 0
            style[FontConfig.FC_PIXEL_SIZE] = pixel_size
            style[FontConfig.FC_SLANT] = int(items[5])
            style[FontConfig.FC_WEIGHT] = FontConfig.weight_to_open_type(
                int(items[6]))
            style[FontConfig.FC_WIDTH] = int(items[7])
            style_sequence.append(style)
        return style_sequence

    @staticmethod
    def match(family):
        matched = FontConfig.match(family, '%{family[0]}')
        if len(matched) == 0:
            return None
        return matched[0]


class SVGLength(object):
    TYPE_NUMBER = ''  # pixel
    TYPE_PERCENTAGE = '%'
    TYPE_EMS = 'em'
    TYPE_EXS = 'ex'
    TYPE_PX = 'px'
    TYPE_CM = 'cm'
    TYPE_MM = 'mm'
    TYPE_IN = 'in'
    TYPE_PT = 'pt'
    TYPE_PC = 'pc'
    TYPE_Q = 'q'
    TYPE_CAPS = 'cap'
    TYPE_CHS = 'ch'
    TYPE_ICS = 'ic'
    TYPE_REMS = 'rem'
    TYPE_VW = 'vw'
    TYPE_VH = 'vh'
    TYPE_VMIN = 'vmin'
    TYPE_VMAX = 'vmax'
    TYPE_DPI = 'dpi'
    TYPE_DPCM = 'dpcm'
    TYPE_DPPX = 'dppx'

    SUPPORTED_UNITS = (
        TYPE_PERCENTAGE,
        TYPE_EMS, TYPE_EXS, TYPE_CAPS, TYPE_CHS, TYPE_ICS, TYPE_REMS,
        TYPE_VW, TYPE_VH, TYPE_VMIN, TYPE_VMAX,
        TYPE_CM, TYPE_MM, TYPE_Q, TYPE_IN, TYPE_PT, TYPE_PC, TYPE_PX,
        TYPE_DPI, TYPE_DPCM, TYPE_DPPX,
    )

    DIRECTION_UNSPECIFIED = 0
    DIRECTION_HORIZONTAL = 1
    DIRECTION_VERTICAL = 2

    RE_LENGTH = re.compile(
        r"(?P<number>[+-]?"
        r"((\d+(\.\d*)?([Ee][+-]?\d+)?)|(\d*\.\d+([Ee][+-]?\d+)?)))"
        r"(?P<unit>%|[a-z]+)?",
        re.IGNORECASE
    )

    rel_tol = 1e-9

    abs_tol = 1e-9

    # 1in = 2.54cm = 96px
    # 1cm = 1in/2.54 = 96px/2.54
    # 1mm = 1cm/10
    # 1Q = 1cm/40
    # 1pt = 1in/72
    # 1pc = 1in/6
    _TO_PIXEL_SIZE_MAP = {
        TYPE_PX: 1.0,
        TYPE_IN: Decimal(96),
        TYPE_CM: Decimal(96) / Decimal(2.54),
        TYPE_MM: Decimal(96) / Decimal(25.4),
        TYPE_Q: Decimal(96) / Decimal(2.54) / Decimal(40),
        TYPE_PT: Decimal(96) / Decimal(72),
        TYPE_PC: Decimal(96) / Decimal(6),
    }

    def __init__(self, value=None, unit=None, context=None, direction=None):
        """Constructs a SVGLength object.

        Arguments:
            value (str, float, optional): A number or a number with unit.
            unit (str, optional): The unit string.
            context (SVGElement, optional): The referencing element.
            direction (int, optional): The direction of this length value.
        Examples:
            >>> n = SVGLength()
            >>> n.tostring(), n.value(), n.unit
            ('0', 0, None)
            >>> n = SVGLength(math.pi)
            >>> n.tostring(), n.value(), n.unit
            ('3.141593', 3.141592653589793, None)
            >>> n = SVGLength('1.0in')
            >>> n.tostring(), n.value(), n.unit
            ('1in', 96.0, 'in')
            >>> n.tostring(SVGLength.TYPE_MM), n.value(SVGLength.TYPE_MM)
            ('25.4mm', 25.4)
            >>> n = SVGLength('18.0pt')
            >>> n.tostring(), n.value(), n.unit
            ('18pt', 24.0, 'pt')  # 18(pt) * 4 / 3 = 24(px)
            >>> n /= 2
            >>> n.tostring(), n.value(), n.unit
            ('9pt', 12.0, 'pt')
        """
        self._context = context
        self._direction = direction
        if value is not None and unit is not None:
            self.new_value(value, unit)
        else:
            self._number, self._unit = SVGLength.parse(value)

    def __abs__(self):
        x = copy.deepcopy(self)
        x._number = abs(x._number)
        return x

    def __add__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        x = copy.deepcopy(self)
        if x._unit is None and other.unit is not None:
            x.convert(other.unit)
        x._number += Decimal(other.value(x._unit))
        return x

    def __eq__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        return math.isclose(self._number, o,
                            rel_tol=SVGLength.rel_tol,
                            abs_tol=SVGLength.abs_tol)

    def __ge__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        if math.isclose(self._number, o,
                        rel_tol=SVGLength.rel_tol, abs_tol=SVGLength.abs_tol):
            return True
        return self._number >= o

    def __gt__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        if math.isclose(self._number, o,
                        rel_tol=SVGLength.rel_tol, abs_tol=SVGLength.abs_tol):
            return False
        return self._number > o

    def __iadd__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        if self._unit is None and other.unit is not None:
            self.convert(other.unit)
        self._number += Decimal(other.value(self._unit))
        return self

    def __imul__(self, other):
        if isinstance(other, SVGLength):
            if self._unit is None and other.unit is not None:
                self.convert(other.unit)
            self._number *= Decimal(other.value(self._unit))
        elif isinstance(other, (int, float)):
            self._number *= Decimal(other)
        else:
            return NotImplemented
        return self

    def __isub__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        if self._unit is None and other.unit is not None:
            self.convert(other.unit)
        self._number -= Decimal(other.value(self._unit))
        return self

    def __itruediv__(self, other):
        if isinstance(other, SVGLength):
            if self._unit is None and other.unit is not None:
                self.convert(other.unit)
            self._number /= Decimal(other.value(self._unit))
        elif isinstance(other, (int, float)):
            self._number /= Decimal(other)
        else:
            return NotImplemented
        return self

    def __le__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        if math.isclose(self._number, o,
                        rel_tol=SVGLength.rel_tol, abs_tol=SVGLength.abs_tol):
            return True
        return self._number <= o

    def __lt__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        if math.isclose(self._number, o,
                        rel_tol=SVGLength.rel_tol, abs_tol=SVGLength.abs_tol):
            return False
        return self._number < o

    def __mul__(self, other):
        x = copy.deepcopy(self)
        if isinstance(other, SVGLength):
            if x._unit is None and other.unit is not None:
                x.convert(other.unit)
            x._number *= Decimal(other.value(x._unit))
        elif isinstance(other, (int, float)):
            x._number *= Decimal(other)
        else:
            return NotImplemented
        return x

    def __neg__(self):
        x = copy.deepcopy(self)
        x._number = -x._number
        return x

    def __pos__(self):
        x = copy.deepcopy(self)
        return x

    def __pow__(self, power, modulo=None):
        x = copy.deepcopy(self)
        x._number = pow(x._number, power, modulo)
        return x

    def __repr__(self):
        return '<{}.{} object at {} ({:g} {})>'.format(
            type(self).__module__, type(self).__name__, hex(id(self)),
            self._number, self._unit)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return '{:g}{}'.format(self._number,
                               self._unit if self._unit is not None else '')

    def __sub__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        x = copy.deepcopy(self)
        if x._unit is None and other.unit is not None:
            x.convert(other.unit)
        x._number -= Decimal(other.value(x._unit))
        return x

    def __truediv__(self, other):
        x = copy.deepcopy(self)
        if isinstance(other, SVGLength):
            if x._unit is None and other.unit is not None:
                x.convert(other.unit)
            x._number /= Decimal(other.value(x._unit))
        elif isinstance(other, (int, float)):
            x._number /= Decimal(other)
        else:
            return NotImplemented
        return x

    @property
    def context(self):
        return self._context

    @property
    def unit(self):
        """str: The unit string."""
        return self._unit if self._unit != SVGLength.TYPE_NUMBER else None

    @staticmethod
    def _normalize(number, unit):
        if unit is not None:
            unit = unit.lower()
            if unit not in SVGLength.SUPPORTED_UNITS:
                raise ValueError('Unknown unit: ' + repr(unit))
        try:
            return Decimal(number).normalize(), unit
        except InvalidOperation:
            return Decimal(0), unit

    def convert(self, unit):
        """Resets the stored unit.

        Arguments:
            unit (str): The unit string.
        """
        if unit == self._unit:
            return
        self._number = Decimal(self.value(unit))
        self._unit = unit

    def isabsolute(self):
        return self._unit in [
            None, SVGLength.TYPE_CM, SVGLength.TYPE_MM, SVGLength.TYPE_Q,
            SVGLength.TYPE_IN, SVGLength.TYPE_PT, SVGLength.TYPE_PC,
            SVGLength.TYPE_PX, SVGLength.TYPE_NUMBER,
        ]

    def isrelative(self):
        return self._unit in [
            SVGLength.TYPE_EMS, SVGLength.TYPE_EXS, SVGLength.TYPE_CHS,
            SVGLength.TYPE_ICS, SVGLength.TYPE_REMS,
            SVGLength.TYPE_PERCENTAGE,
            SVGLength.TYPE_VW, SVGLength.TYPE_VH,
            SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX,
        ]

    def isresolution(self):
        return self._unit in [
            SVGLength.TYPE_DPI, SVGLength.TYPE_DPCM, SVGLength.TYPE_DPPX,
        ]

    def new_value(self, number, unit):
        """Resets the value as a number with the unit.

        Arguments:
            number (float): The new value.
            unit (str): The unit string.
        """
        self._number = Decimal(number)
        self._unit = unit

    @staticmethod
    def parse(text):
        if text is None:
            return Decimal(0), None
        elif isinstance(text, str):
            match = SVGLength.RE_LENGTH.match(text.strip())
            if match is None:
                raise ValueError('Expected number, got \'{}\''.format(text))
            number = match.group('number')
            unit = match.group('unit')
        else:
            number = text
            unit = None
        return SVGLength._normalize(number, unit)

    def tostring(self, unit=None, direction=None):
        """Returns a string with the unit, formatted according to the specified
        precision.

        Arguments:
            unit (str, optional): The unit string.
            direction (int, optional): The direction of this length value.
        Returns:
            str: The value in specified unit.
        Examples:
            >>> n = SVGLength('10cm')
            >>> n.tostring()
            '10cm'
            >>> n.tostring(SVGLength.TYPE_MM)
            '100mm'
            >>> from svgpy import formatter
            >>> formatter.precision
            6  # default precision for a floating point value
            >>> n /= 3
            >>> n.tostring()
            '3.333333cm'
            >>> formatter.precision = 3
            >>> n.tostring()
            '3.333cm'
        """
        if unit is None:
            unit = self._unit
        number = self.value(unit, direction=direction)
        value = format_number_sequence([number])[0]
        return '{0}{1}'.format(value, unit if unit is not None else '')

    def value(self, unit=None, direction=None):
        """Returns the value in specified unit, or in pixels if the unit is
        None or SVGLength.TYPE_NUMBER.

        Arguments:
            unit (str, optional): The unit string.
            direction (int, optional): The direction of this length value.
        Returns:
            float: The value in specified unit.
        Examples:
            >>> n = SVGLength('1in')
            >>> n.value(SVGLength.TYPE_IN)
            1.0  # 1.0(in)
            >>> n.value(SVGLength.TYPE_CM)
            2.54  # 2.54(cm)
            >>> n.value(SVGLength.TYPE_PX)
            96.0  # 96.0(px)
        """
        # See https://drafts.csswg.org/css-values/#lengths
        if unit == self._unit:
            return float(self._number)
        if direction is None:
            direction = self._direction
        if ((self._unit in [SVGLength.TYPE_DPI, SVGLength.TYPE_DPCM,
                            SVGLength.TYPE_DPPX]
             and unit not in [SVGLength.TYPE_DPI, SVGLength.TYPE_DPCM,
                              SVGLength.TYPE_DPPX])
                or (self._unit not in [SVGLength.TYPE_DPI, SVGLength.TYPE_DPCM,
                                       SVGLength.TYPE_DPPX]
                    and unit in [SVGLength.TYPE_DPI, SVGLength.TYPE_DPCM,
                                 SVGLength.TYPE_DPPX])):
            raise ValueError('Cannot convert: ' + repr(self._unit) + ' to '
                             + repr(unit))
        element_font_size = None
        root_font_size = None
        vw = None
        vh = None
        vmin = None
        vmax = None
        font = None
        if self._unit == SVGLength.TYPE_REMS or unit == SVGLength.TYPE_REMS:
            # <font-relative lengths>: rem
            if self._context is None:
                root_font_size = Decimal(Font.default_font_size)
            else:
                root = self._context.getroottree().getroot()
                root_font_size = Decimal(CSSUtils.compute_font_size(root))

        if (self._unit in [SVGLength.TYPE_EMS, SVGLength.TYPE_PERCENTAGE,
                           SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                           SVGLength.TYPE_CHS,
                           SVGLength.TYPE_ICS]
                or unit in [SVGLength.TYPE_EMS, SVGLength.TYPE_PERCENTAGE,
                            SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                            SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]):
            # <font-relative lengths>: em
            # <font-percentage lengths>: %
            # falls back for 'ex' | 'cap' | 'ch' | 'ic' units
            if self._context is None:
                element_font_size = Decimal(Font.default_font_size)
            else:
                context = self._context.getparent()
                if context is None:
                    element_font_size = Decimal(Font.default_font_size)
                else:
                    element_font_size = Decimal(
                        CSSUtils.compute_font_size(context))

        if (self._unit in [SVGLength.TYPE_VW, SVGLength.TYPE_VH,
                           SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX,
                           SVGLength.TYPE_PERCENTAGE]
                or unit in [SVGLength.TYPE_VW, SVGLength.TYPE_VH,
                            SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX,
                            SVGLength.TYPE_PERCENTAGE]):
            # <viewport-percentage lengths>: % | vw | vh | vmin | vmax
            if self._context is None:
                vw = 100
                vh = 100
            else:
                view_box = self._context.get_view_box()
                if view_box is not None:
                    _, _, vbw, vbh, _ = view_box
                    vw = vbw.value()
                    vh = vbh.value()
                else:
                    _, _, vpw, vph = self._context.get_viewport_size()
                    vw = vpw.value()
                    vh = vph.value()
            vmin = min(vw, vh)
            vmax = max(vw, vh)

        if (self._unit in [SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                           SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]
                or unit in [SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                            SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]):
            # <font-relative lengths>: ex | cap | ch | ic
            if self._context is not None:
                font = Font(self._context)

        # convert to pixels
        if self._unit in [None, SVGLength.TYPE_NUMBER, SVGLength.TYPE_PX]:
            # pixels
            px = self._number
        elif self._unit == SVGLength.TYPE_REMS:
            # <font-relative lengths> 'rem' unit to pixels
            px = self._number * root_font_size
        elif self._unit in [SVGLength.TYPE_EMS]:
            # <font-relative lengths> 'em' unit to pixels
            px = self._number * element_font_size
        elif self._unit in [SVGLength.TYPE_PERCENTAGE]:
            # <viewport-percentage lengths> | <font-percentage lengths>:
            # percentage units to pixels
            if direction == SVGLength.DIRECTION_HORIZONTAL:
                px = self._number * Decimal(vw) / 100
            elif direction == SVGLength.DIRECTION_VERTICAL:
                px = self._number * Decimal(vh) / 100
            elif direction == SVGLength.DIRECTION_UNSPECIFIED:
                k = math.sqrt(vw ** 2 + vh ** 2) / math.sqrt(2)
                px = self._number * Decimal(k) / 100
            else:
                px = self._number * element_font_size / 100
        elif self._unit in [SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                            SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]:
            # <font-relative lengths> 'ex' | 'cap' | 'ch' | 'ic'
            #  units to pixels
            if font is None:
                px = self._number * element_font_size / 2
            else:
                if self._unit == SVGLength.TYPE_EXS:
                    k = font.x_height
                elif self._unit == SVGLength.TYPE_CAPS:
                    k = font.cap_height
                elif self._unit == SVGLength.TYPE_CHS:
                    k = font.ch_advance
                else:  # self._unit == SVGLength.TYPE_ICS:
                    k = font.ic_advance
                val = Decimal(k)
                if val == 0:
                    val = element_font_size
                px = self._number * val
        elif self._unit in [SVGLength.TYPE_VW, SVGLength.TYPE_VH,
                            SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX]:
            # <viewport-percentage lengths> 'vw' | 'vh' | 'vmin' | 'vmax' units
            # to pixels
            if self._unit == SVGLength.TYPE_VW:
                k = vw
            elif self._unit == SVGLength.TYPE_VH:
                k = vh
            elif self._unit == SVGLength.TYPE_VMIN:
                k = vmin
            else:  # self._unit == SVGLength.TYPE_VMAX:
                k = vmax
            px = self._number * Decimal(k) / 100
        elif self._unit in [SVGLength.TYPE_DPI, SVGLength.TYPE_DPCM,
                            SVGLength.TYPE_DPPX]:
            # <resolution lengths> units to 'dppx'
            if self._unit == SVGLength.TYPE_DPI:
                px = self._number / Decimal(96)
            elif self._unit == SVGLength.TYPE_DPCM:
                px = self._number / Decimal(96) * Decimal(2.54)
            else:  # self._unit == SVGLength.TYPE_DPPX
                px = self._number
        else:
            # <absolute lengths> units to pixels
            k = SVGLength._TO_PIXEL_SIZE_MAP.get(self._unit)
            if k is None:
                raise NotImplementedError('Unknown unit: ' + repr(self._unit))
            px = self._number * k

        # convert to specified units
        if unit in [None, SVGLength.TYPE_NUMBER, SVGLength.TYPE_PX]:
            # to pixels
            return float(px)
        elif unit == SVGLength.TYPE_REMS:
            # to 'rem' unit
            px /= root_font_size
            return float(px)
        elif unit in [SVGLength.TYPE_EMS]:
            # to <font-relative lengths> 'em' unit
            px /= element_font_size
            return float(px)
        elif unit in [SVGLength.TYPE_PERCENTAGE]:
            # to <viewport-percentage lengths> | <font-percentage lengths>
            if direction == SVGLength.DIRECTION_HORIZONTAL:
                px /= Decimal(vw)
            elif direction == SVGLength.DIRECTION_VERTICAL:
                px /= Decimal(vh)
            elif direction == SVGLength.DIRECTION_UNSPECIFIED:
                k = math.sqrt(vw ** 2 + vh ** 2) / math.sqrt(2)
                px /= Decimal(k)
            else:
                px /= element_font_size
            return float(px * 100)
        elif unit in [SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                      SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]:
            # to <font-relative lengths> 'ex' | 'cap' | 'ch' | 'ic' units
            if font is None:
                px /= element_font_size / 2
            else:
                pt = int(px / SVGLength._TO_PIXEL_SIZE_MAP[SVGLength.TYPE_PT]
                         * 64)
                horizontal_resolution = Screen.DEFAULT_HORIZONTAL_RESOLUTION
                vertical_resolution = Screen.DEFAULT_VERTICAL_RESOLUTION
                if self._context is not None:
                    doc = self._context.owner_document
                    if doc is not None and doc.default_view is not None:
                        screen = doc.default_view.screen
                        horizontal_resolution = screen.horizontal_resolution
                        vertical_resolution = screen.vertical_resolution
                font.set_point_size(0,
                                    pt,
                                    horizontal_resolution,
                                    vertical_resolution)
                if unit == SVGLength.TYPE_EXS:
                    k = font.x_height
                elif unit == SVGLength.TYPE_CAPS:
                    k = font.cap_height
                elif unit == SVGLength.TYPE_CHS:
                    k = font.ch_advance
                else:  # unit == SVGLength.TYPE_ICS:
                    k = font.ic_advance
                val = Decimal(k)
                if val == 0:
                    val = element_font_size
                px /= val
            return float(px)
        elif unit in [SVGLength.TYPE_VW, SVGLength.TYPE_VH,
                      SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX]:
            # to <viewport-percentage lengths>
            # 'vw' | 'vh' | 'vmin' | 'vmax' units
            if unit == SVGLength.TYPE_VW:
                k = vw
            elif unit == SVGLength.TYPE_VH:
                k = vh
            elif unit == SVGLength.TYPE_VMIN:
                k = vmin
            else:  # unit == SVGLength.TYPE_VMAX:
                k = vmax
            return float(px / Decimal(k) * 100)
        elif unit in [SVGLength.TYPE_DPI, SVGLength.TYPE_DPCM,
                      SVGLength.TYPE_DPPX]:
            # 'dppx' to <resolution lengths> 'dpi' | 'dpcm'
            if unit == SVGLength.TYPE_DPI:
                px *= Decimal(96)
            elif unit == SVGLength.TYPE_DPCM:
                px *= Decimal(96) / Decimal(2.54)
            return float(px)

        # to <absolute lengths> units
        k = SVGLength._TO_PIXEL_SIZE_MAP.get(unit)
        if k is None:
            raise NotImplementedError('Unknown unit: ' + repr(unit))
        return float(px / k)
