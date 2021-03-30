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

from .base import SVGElement, SVGGraphicsElement, SVGPathDataSettings
from .core import CSSUtils, Font, SVGLength
from .dom import Element, Node
from .freetype import FreeType
from .geometry.matrix import DOMMatrix
from .geometry.rect import DOMRect
from .harfbuzz import HBBuffer, HBDirection, HBFeature, HBFTFont, HBLanguage, \
    HBScript
from .icu import UBiDi, UBreakIterator, ULocale
from .opentype import features_from_style, iso639_codes_from_language_tag
from .path import PathParser


class SVGTextContentElement(SVGGraphicsElement):
    """Represents the [SVG2] SVGTextContentElement."""

    _CHARS_ID = 0
    _CHARS_TEXT = 1
    _CHARS_STYLE = 2
    _CHARS_PATH_DATA = 3
    _CHARS_ADVANCE_LIST = 4
    _CHARS_BBOX = 5
    _CHARS_ELEMENT = 6

    def _get_chars_info(self):
        root = self.get_nearest_text_element()
        if root is None:
            return []

        chars_info = SVGTextContentElement._get_descendant_chars_info(
            root, first=True, is_display=True, is_render=True)
        return chars_info

    @staticmethod
    def _get_descendant_chars(element, style_map=None,
                              prev_text=None, first=False, **kwargs):
        """Returns the addressable characters.

        Arguments:
            element (SVGElement):
            style_map (dict, optional):
            prev_text (str, optional):
            first (bool, optional):
            **kwargs: See below.
        Keyword Arguments:
            is_display (bool, optional):
        Returns:
            list[list[int, str, dict, list[SVGPathSegment], list[float], DOMRect,
                SVGElement]]:
                Returns a list of seven numbers <hash value of an element>,
                <text for rendering>, <computed presentation properties>,
                <list of path segments>, <list of advance measure>,
                <bbox> and <element object>.
            str: previous text for rendering.
        """
        is_display = kwargs.get('is_display', False)
        chars_info = list()
        if not element.istext() or (is_display
                                    and not element.isdisplay()):
            return chars_info, prev_text

        if style_map is None:
            style_map = dict()
        key = hash(element)
        style = style_map.get(key)
        if style is None:
            style = element.get_computed_style()
            style_map[key] = copy.deepcopy(style)
        if element.text is not None:
            out_text = CSSUtils.normalize_text_content(
                element,
                element.text,
                style,
                prev_text,
                first)
            if len(out_text) > 0:
                path_data = []
                advance_list = []
                bbox = None
                chars_info.append(
                    [key, out_text, style, path_data, advance_list, bbox,
                     element])
                prev_text = out_text
                first = False

        for child in iter(element):
            if (child.node_type == Node.ELEMENT_NODE
                    and child.istext()
                    and (not is_display
                         or (is_display and child.isdisplay()))):
                child_chars_info, out_text = \
                    SVGTextContentElement._get_descendant_chars(
                        child, style_map, prev_text, first, **kwargs)
                if len(out_text) > 0:
                    chars_info += child_chars_info
                    prev_text = out_text
                    first = False
            if (child.local_name in SVGElement.TEXT_CONTENT_CHILD_ELEMENTS
                    and child.tail is not None):
                out_text = CSSUtils.normalize_text_content(
                    child,
                    child.tail,
                    style,
                    prev_text,
                    first)
                if len(out_text) > 0:
                    path_data = []
                    advance_list = []
                    bbox = None
                    chars_info.append(
                        [key, out_text, style, path_data, advance_list, bbox,
                         element])
                    prev_text = out_text
                    first = False
        return chars_info, prev_text

    @staticmethod
    def _get_descendant_chars_info(root, first=False, **kwargs):
        """Returns the addressable characters.

        Arguments:
            root (SVGElement):
            first (bool, optional):
            **kwargs: See below.
        Keyword Arguments:
            is_display (bool, optional):
            is_render (bool, optional):
        Returns:
            list[list[int, str, dict, list[SVGPathSegment], list[float],
                DOMRect, SVGElement]]:
                Returns a list of seven numbers <hash value of an element>,
                <text for rendering>, <computed presentation properties>,
                <list of path segments>, <list of advance measure>,
                <bbox> and <element object>.
        """
        chars_info, _ = SVGTextContentElement._get_descendant_chars(
            root, first=first, **kwargs)
        if len(chars_info) > 0:
            item = chars_info[-1]
            text = item[SVGTextContentElement._CHARS_TEXT].rstrip()
            item[SVGTextContentElement._CHARS_TEXT] = text

            is_render = kwargs.get('is_render', False)
            if is_render:
                style = chars_info[0][SVGTextContentElement._CHARS_STYLE]
                x_list = style['x']
                if x_list is None:
                    x = 0
                else:
                    x = x_list[0]
                y_list = style['y']
                if y_list is None:
                    y = 0
                else:
                    y = y_list[0]

                style_map = dict()
                for info in iter(chars_info):
                    key = info[SVGTextContentElement._CHARS_ID]
                    style = info[SVGTextContentElement._CHARS_STYLE]
                    style_map[key] = copy.deepcopy(style)

                for info in iter(chars_info):
                    path_data, advance_list, bbox, (x, y) = \
                        SVGTextContentElement._get_text_path_data(
                            info[SVGTextContentElement._CHARS_ELEMENT],
                            style_map,
                            info[SVGTextContentElement._CHARS_TEXT],
                            x, y)
                    info[SVGTextContentElement._CHARS_PATH_DATA] = path_data
                    info[SVGTextContentElement._CHARS_ADVANCE_LIST] = \
                        advance_list
                    info[SVGTextContentElement._CHARS_BBOX] = bbox

        return chars_info

    @staticmethod
    def _get_text_path_data(element, style_map, out_text, start_x, start_y):
        """Returns the addressable characters.

        Arguments:
            element (SVGElement):
            style_map (dict):
            out_text (str): A text for rendering.
            start_x (float):
            start_y (float):
        Returns:
            list[SVGPathSegment]:
            list[float]:
            DOMRect:
            tuple[float, float]:
        """

        def _get_inherited_attribute(_element, _style_map, _key,
                                     _default=None):
            while _element is not None:
                if (_element.node_type == Node.ELEMENT_NODE
                        and _element.istext()
                        and _element.isdisplay()):
                    _style = _style_map.get(hash(_element))
                    if _style is None:
                        _style = _element.get_computed_style()
                        _style_map[hash(_element)] = _style
                    _value = _style.get(_key)
                    if _value is not None:
                        return _value
                _element = _element.getparent()
            return _default

        # TODO: support line-breaking and word-breaking.
        x_list = _get_inherited_attribute(element, style_map, 'x', [])
        y_list = _get_inherited_attribute(element, style_map, 'y', [])
        dx_list = _get_inherited_attribute(element, style_map, 'dx', [])
        dy_list = _get_inherited_attribute(element, style_map, 'dy', [])
        rotate_list = _get_inherited_attribute(
            element, style_map, 'rotate', [])

        style = style_map.get(hash(element))  # computed style
        assert style is not None
        font = Font(element)
        face = font.face
        hb_font = HBFTFont.create(face)

        # alignment_baseline = style['alignment-baseline']
        # baseline_shift = style['baseline-shift']

        direction = style['direction']
        ltr = True if direction == 'ltr' else False

        # dominant_baseline = style['dominant-baseline']

        # font-feature-settings, font-kerning, font-variant-*
        hb_features = list()
        features = features_from_style(style)
        for feature in features:
            hb_features.append(HBFeature.fromstring(feature))

        font_synthesis = style['font-synthesis']
        force_embolden = True if (style['font-weight'] > Font.WEIGHT_NORMAL
                                  and 'weight' in font_synthesis
                                  and (face.style_flags
                                       & FreeType.FT_STYLE_FLAG_BOLD) == 0
                                  ) else False
        force_oblique = True if (style['font-style'] != 'normal'
                                 and 'style' in font_synthesis
                                 and (face.style_flags
                                      & FreeType.FT_STYLE_FLAG_ITALIC) == 0
                                 ) else False

        # glyph_orientation_vertical = style['glyph-orientation-vertical']
        # inline_size = style['inline-size']
        # letter_spacing = style['letter-spacing']
        # line_height = style['line-height']

        # text_anchor = style['text-anchor']
        # vpx, vpy, vpw, vph = element.get_viewport_size()

        # unicode_bidi = style['unicode-bidi']
        # word_spacing = style['word-spacing']

        writing_mode = style['writing-mode']
        horizontal = True if writing_mode in [
            'horizontal-tb', 'lr', 'lr-tb', 'rl', 'rl-tb'] else False
        sideways = True if writing_mode.startswith('sideways') else False

        buf = HBBuffer.create()
        buf.set_cluster_level(HBBuffer.CLUSTER_LEVEL_MONOTONE_CHARACTERS)
        if horizontal:
            if ltr:
                hb_direction = HBDirection(HBDirection.HB_DIRECTION_LTR)
            else:
                hb_direction = HBDirection(HBDirection.HB_DIRECTION_RTL)
        else:
            hb_direction = HBDirection(HBDirection.HB_DIRECTION_TTB)
        buf.set_direction(hb_direction)

        locale = None
        font_language_override = style['font-language-override']
        if font_language_override != 'normal':
            codes = iso639_codes_from_language_tag(font_language_override)
            if codes is not None:
                # FIXME: use correct language code.
                locale = ULocale(codes[0])
        else:
            xml_lang = style.get(Element.XML_LANG)
            if xml_lang is None:
                xml_lang = style.get('lang')
            if xml_lang is not None:
                locale = ULocale(xml_lang)
        if locale is None:
            locale = ULocale.get_default()
        hb_language = HBLanguage.fromstring(locale.get_language())
        buf.set_language(hb_language)
        script = locale.get_script()
        if script is not None and len(script) == 4:
            hb_script = HBScript.fromstring(script)
            buf.set_script(hb_script)
        else:
            hb_script = buf.get_script()

        current_x = start_x
        current_y = start_y
        rotate = 0
        matrix = DOMMatrix()
        path_data_list = list()
        advance_list = list()
        text_bbox = DOMRect()
        metrics = face.size.metrics
        glyph_width = metrics.x_ppem
        glyph_height = metrics.height / 64
        descender = metrics.descender / 64

        para = UBiDi()
        para.set_para(out_text,
                      UBiDi.UBIDI_DEFAULT_LTR if ltr
                      else UBiDi.UBIDI_DEFAULT_RTL)
        max_limit = para.get_processed_length()
        bi = UBreakIterator(UBreakIterator.UBRK_LINE, locale.locale)
        logical_start = 0
        while logical_start < max_limit:
            limit, para_level = para.get_logical_run(logical_start)
            para_level &= 1
            paragraph = out_text[logical_start:limit]
            bi.set_text(paragraph)
            if ((not ltr and para_level == UBiDi.UBIDI_LTR)
                    or (ltr and para_level == UBiDi.UBIDI_RTL)):
                iterable = reversed(bi)
            else:
                iterable = bi
            for line in iterable:
                buf.clear_contents()
                buf.set_language(hb_language)
                buf.set_script(hb_script)
                buf.add_utf8(line)
                buf.guess_segment_properties()
                buf.shape(hb_font, hb_features)
                infos = buf.get_glyph_infos()
                positions = buf.get_glyph_positions()
                if infos[0].cluster > infos[-1].cluster:
                    infos = list(reversed(infos))
                    positions = list(reversed(positions))

                # re-positioning
                if len(infos) != len(line):
                    clusters = [x.cluster for x in infos]
                    cluster_min = min(clusters)
                    cluster_max = max(clusters)
                    cluster_inc = max(
                        (cluster_max - cluster_min) // len(clusters), 1)
                    # try to find ligatures
                    last_cluster = None
                    for offset, cluster in enumerate(clusters):
                        if last_cluster is None:
                            pass
                        elif last_cluster == cluster:
                            pass  # decompose
                        elif last_cluster + cluster_inc == cluster:
                            pass  # do nothing
                        else:
                            # ligature
                            index = logical_start + offset
                            if index < len(x_list):
                                _ = x_list.pop(index)
                            if index < len(y_list):
                                _ = y_list.pop(index)
                            dx_length = len(dx_list)
                            if index < dx_length:
                                dx = dx_list.pop(index)
                                if index < dx_length - 1:
                                    dx_list[index] += dx
                            dy_length = len(dy_list)
                            if index < dy_length:
                                dy = dy_list.pop(index)
                                if index < dy_length - 1:
                                    dy_list[index] += dy
                            rotate_length = len(rotate_list)
                            if rotate_length > 1 and index < rotate_length:
                                _ = rotate_list.pop(index)
                        last_cluster = cluster

                # render line
                line_path_data = list()
                line_bbox = DOMRect()
                for info, position in zip(infos, positions):
                    if len(x_list) > 0:
                        x = x_list.pop(0)
                    else:
                        x = current_x
                    if len(y_list) > 0:
                        y = y_list.pop(0)
                    else:
                        y = current_y
                    if len(dx_list) > 0:
                        dx = dx_list.pop(0)
                    else:
                        dx = 0
                    if len(dy_list) > 0:
                        dy = dy_list.pop(0)
                    else:
                        dy = 0
                    rotate_length = len(rotate_list)
                    if rotate_length == 1:
                        rotate = rotate_list[0]
                    elif rotate_length > 1:
                        rotate = rotate_list.pop(0)

                    x_offset = position.x_offset / 64
                    y_offset = position.y_offset / 64
                    x += dx + x_offset
                    y += dy - y_offset
                    if horizontal:
                        advance = position.x_advance / 64
                        if para_level == UBiDi.UBIDI_RTL:
                            x -= advance
                        glyph_bbox = DOMRect(x,
                                             y - glyph_height - descender,
                                             advance,
                                             glyph_height)
                        x_advance = advance
                        y_advance = 0
                    else:
                        # TODO: fix bbox for vertical text.
                        advance = -position.y_advance / 64
                        if sideways:
                            glyph_bbox = DOMRect(x,
                                                 y,
                                                 glyph_width,
                                                 position.x_advance / 64)
                        else:
                            glyph_bbox = DOMRect(x,
                                                 y - advance + advance + y_offset,
                                                 glyph_width,
                                                 advance)
                        x_advance = 0
                        y_advance = advance
                    advance_list.append(advance)
                    if rotate != 0:
                        matrix.clear()
                        matrix.translate_self(x, y)
                        matrix.rotate_self(rot_z=rotate)
                        matrix.translate_self(-x, -y)
                        glyph_bbox.transform_self(matrix)

                    matrix.clear()
                    if rotate != 0:
                        matrix.rotate_self(rot_z=rotate)
                    matrix.translate_self(x, -y)

                    load_flags = FreeType.FT_LOAD_NO_BITMAP
                    if not horizontal:
                        load_flags |= FreeType.FT_LOAD_VERTICAL_LAYOUT
                    face.load_glyph(info.codepoint, load_flags)
                    glyph = face.glyph
                    if force_embolden:
                        glyph.embolden()
                    if force_oblique:
                        glyph.oblique()
                    path_data = PathParser.from_glyph(face, matrix)
                    if len(path_data) > 0:
                        line_path_data += path_data

                    if para_level == UBiDi.UBIDI_LTR:
                        x += x_advance - x_offset
                    y += y_advance + y_offset
                    line_bbox |= glyph_bbox
                    current_x = x
                    current_y = y
                if horizontal:
                    if ((not ltr and para_level == UBiDi.UBIDI_LTR)
                            or (ltr and para_level == UBiDi.UBIDI_RTL)):
                        k = -1 if not ltr else 1
                        width = line_bbox.width
                        line_bbox.translate_self(k * width, 0)
                        matrix.clear()
                        matrix.translate_self(k * width, 0)
                        line_path_data = PathParser.transform(line_path_data,
                                                              matrix)
                        if not ltr:
                            current_x = line_bbox.left
                        else:
                            current_x = line_bbox.right
                path_data_list += line_path_data
                text_bbox |= line_bbox

            logical_start = limit

        return path_data_list, advance_list, text_bbox, (current_x, current_y)

    def get_bbox(self, options=None, _depth=0):
        """Returns the bounding box of the current element.

        Arguments:
            options (SVGBoundingBoxOptions, optional): Reserved.
            _depth (int, optional): For internal use only.
        Returns:
            DOMRect: The bounding box of the current element.
        """
        bbox = DOMRect()
        chars_info = self._get_chars_info()
        if len(chars_info) == 0:
            return bbox

        for info in iter(chars_info):
            bbox |= info[SVGTextContentElement._CHARS_BBOX]

        return bbox

    def get_computed_geometry(self):
        geometry = dict()
        local_name = self.local_name

        # 'x' attribute
        # Value: [ [ <length> | <percentage> | <number> ]+ ]#
        # Initial: 0 <text>
        # Initial: (none) <tspan>
        default = '0' if local_name == 'text' else None
        _x = self.get('x', default)
        if _x is None:
            x = None
        else:
            x = [
                SVGLength(n,
                          context=self,
                          direction=SVGLength.DIRECTION_HORIZONTAL).value()
                for n in Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_x)
            ]
        geometry['x'] = x

        # 'y' attribute
        # Value: [ [ <length> | <percentage> | <number> ]+ ]#
        # Initial: 0 <text>
        # Initial: (none) <tspan>
        default = '0' if local_name == 'text' else None
        _y = self.get('y', default)
        if _y is None:
            y = None
        else:
            y = [
                SVGLength(n,
                          context=self,
                          direction=SVGLength.DIRECTION_VERTICAL).value()
                for n in Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_y)
            ]
        geometry['y'] = y

        # 'dx' attribute
        # Value: [ [ <length> | <percentage> | <number> ]+ ]#
        # Initial: (none)
        _dx = self.get('dx')
        if _dx is None:
            dx = None
        else:
            dx = [
                SVGLength(n,
                          context=self,
                          direction=SVGLength.DIRECTION_HORIZONTAL).value()
                for n in Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_dx)
            ]
        geometry['dx'] = dx

        # 'dy' attribute
        # Value: [ [ <length> | <percentage> | <number> ]+ ]#
        # Initial: (none)
        _dy = self.get('dy')
        if _dy is None:
            dy = None
        else:
            dy = [
                SVGLength(n,
                          context=self,
                          direction=SVGLength.DIRECTION_VERTICAL).value()
                for n in Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_dy)
            ]
        geometry['dy'] = dy

        # 'rotate' attribute
        # Value: [ <number>+ ]#
        # Initial: (none)
        _rotate = self.get('rotate')
        if _rotate is None:
            rotate = None
        else:
            rotate = [
                float(t) for t in
                Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_rotate)
            ]
        geometry['rotate'] = rotate

        return geometry

    def get_computed_text_length(self):
        return self.get_sub_string_length()

    def get_chars(self):
        """Returns the addressable characters available for rendering within
        the current element.

        Returns:
            str: The addressable characters or None.
        """
        root = self.get_nearest_text_element()
        if root is None:
            return None

        chars_info = SVGTextContentElement._get_descendant_chars_info(
            root, first=True, is_display=True)
        local_name = self.local_name
        if local_name == 'text':
            out = ''.join([x[SVGTextContentElement._CHARS_TEXT]
                           for x in chars_info])
            return out
        elif local_name in SVGElement.TEXT_CONTENT_CHILD_ELEMENTS:
            out = [x[SVGTextContentElement._CHARS_TEXT]
                   for x in chars_info
                   if x[SVGTextContentElement._CHARS_ID] == hash(self)]
            if len(out) == 0:
                return None
            return out[0]
        return None

    def get_nearest_text_element(self):
        element = self
        while element is not None:
            if element.local_name == 'text':
                return element
            element = element.getparent()
        return None

    def get_number_of_chars(self):
        """Returns the total number of addressable characters available for
        rendering within the current element.

        Returns:
            int: The total number of addressable characters.
        """
        chars = self.get_chars()
        if chars is None:
            return 0
        return len(chars)

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        path_data = list()
        chars_info = self._get_chars_info()
        if len(chars_info) == 0:
            return path_data

        for info in iter(chars_info):
            path_data += info[SVGTextContentElement._CHARS_PATH_DATA]

        if settings is not None:
            if not isinstance(settings, SVGPathDataSettings):
                raise TypeError('Expected SVGPathDataSettings, got {}'.format(
                    type(settings)))
            if settings.normalize:
                path_data = PathParser.normalize(path_data)
        return path_data

    def get_sub_string_length(self, char_num=0, nchars=-1):
        root = self.get_nearest_text_element()
        if root is None:
            return 0

        chars_info = SVGTextContentElement._get_descendant_chars_info(
            root, first=True, is_display=True, is_render=True)
        local_name = self.local_name
        advance_list = list()
        if local_name == 'text':
            for item in iter(chars_info):
                advance_list += item[SVGTextContentElement._CHARS_ADVANCE_LIST]
        elif local_name in SVGElement.TEXT_CONTENT_CHILD_ELEMENTS:
            out = [x[SVGTextContentElement._CHARS_ADVANCE_LIST]
                   for x in chars_info
                   if x[SVGTextContentElement._CHARS_ID] == hash(self)]
            if len(out) == 0:
                return 0
            advance_list = out[0]
        else:
            raise NotImplementedError

        if nchars == -1:
            last = len(advance_list)
        else:
            last = char_num + nchars
        return sum(advance_list[char_num:last])

    def get_total_length(self):
        """Returns the total length of the path.

        Returns:
            float: The total length of the path.
        """
        _ = self
        return 0


class SVGTextPositioningElement(SVGTextContentElement):
    """Represents the [SVG2] SVGTextPositioningElement."""
    pass
