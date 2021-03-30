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


import re
from abc import ABC, abstractmethod
from collections import OrderedDict
from collections.abc import MutableMapping, MutableSequence
from logging import getLogger
from urllib.error import URLError

import tinycss2

from .longhands import Longhand
from .props import PropertyDescriptor, PropertySyntax, \
    css_color_keyword_set, css_property_descriptor_map, css_wide_keyword_set
from .screen import Screen, ScreenOrientation
from .shorthands import Shorthand, font_sub_property_list
from .types import CSSKeywordValue, CSSImageValue, CSSMathClamp, \
    CSSMathInvert, CSSMathMax, CSSMathMin, CSSMathNegate, CSSMathOperator, \
    CSSMathProduct, CSSMathSum, CSSMathValue, CSSNumericBaseType, \
    CSSNumericType, CSSNumericValue, CSSStyleValue, CSSURLImageValue, \
    CSSUnitValue, CSSUnparsedValue, CSSVariableReferenceValue, \
    StylePropertyMap, StylePropertyMapReadOnly, UnitType
from ..exception import NoModificationAllowedError
from ..utils import CaseInsensitiveMapping, dict_to_style, get_content_type, \
    load, normalize_url, style_to_dict

_RE_COLLAPSIBLE_WHITESPACE = re.compile(r'(\x20){2,}')


def normalize_text(text):
    out_text = text.strip().replace(
        '\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
    out_text = _RE_COLLAPSIBLE_WHITESPACE.sub(' ', out_text)
    return out_text


class _StyleAttribute(object):

    def __init__(self, declarations, owner_node):
        self._declarations = declarations  # type: OrderedDict
        self._owner_node = owner_node
        attr = owner_node.attributes.get_named_item_ns(None, 'style')
        style = '' if attr is None else attr.value
        self._style_map = style_to_dict(style)

    def _remove(self, property_name, force=False):
        style_map = self._style_map
        updated = False
        if property_name in style_map:
            updated = True
            del style_map[property_name]

        if Shorthand.is_shorthand(property_name):
            # shorthand
            # remove shorthand's sub-properties
            longhand_names = Shorthand.longhands(property_name)
            for longhand_name in longhand_names:
                if longhand_name in style_map:
                    updated = True
                    del style_map[longhand_name]

        if force:
            return updated

        if (Shorthand.is_shorthand(property_name)
                or Longhand.is_longhand(property_name)):
            # shorthand or shorthand's sub-property
            # try to set the shorthand
            declarations = self._declarations
            shorthand_names = Longhand.shorthands(property_name)
            for shorthand_name in shorthand_names:
                _updated = self._set_shorthand(shorthand_name)
                if _updated:
                    updated = True
                else:
                    if shorthand_name in style_map:
                        updated = True
                        del style_map[shorthand_name]
                    longhand_names = Shorthand.longhands(shorthand_name)
                    for longhand_name in longhand_names:
                        if longhand_name in declarations:
                            updated = True
                            longhand_value = declarations[longhand_name][0]
                            style_map[longhand_name] = longhand_value

        return updated

    def _set(self, property_name, value, append=True, restore=False):
        style_map = self._style_map
        if not append and property_name not in style_map:
            return False
        if restore:
            if property_name not in self._declarations:
                return False
            value = self._declarations[property_name][0]
        updated = False
        if Longhand.is_longhand(property_name):
            # longhand => shorthand
            # e.g.: 'font-variant-caps: small-caps'
            # => 'font: small-caps' or 'font-variant: small-caps'
            shorthand_names = Longhand.shorthands(property_name)
            for shorthand_name in shorthand_names:
                _updated = self._set_shorthand(shorthand_name)
                if _updated:
                    updated = True
                    for sub_shorthand_name in (set(shorthand_names)
                                               - {shorthand_name}):
                        if sub_shorthand_name in style_map:
                            del style_map[sub_shorthand_name]
                    break
                else:
                    # shorthand => longhand
                    updated |= self._set_longhand_from_shorthand(
                        shorthand_name)
        elif Shorthand.is_shorthand(property_name):
            # shorthand
            updated = self._set_shorthand(property_name)
            if not updated:
                # shorthand => longhand
                updated = self._set_longhand_from_shorthand(property_name)

        if not updated and len(value) > 0:
            updated = True
            style_map[property_name] = value
        return updated

    def _set_longhand_from_shorthand(self, shorthand_name):
        style_map = self._style_map
        declarations = self._declarations
        updated = False
        if shorthand_name in style_map:
            updated = True
            del style_map[shorthand_name]
        longhand_names = Shorthand.longhands(shorthand_name)
        for longhand_name in longhand_names:
            if longhand_name in declarations:
                updated = True
                longhand_value = declarations[longhand_name][0]
                style_map[longhand_name] = longhand_value
            elif Shorthand.is_shorthand(longhand_name):
                _updated = self._set_shorthand(longhand_name)
                if _updated:
                    updated = True
                    continue
                updated |= self._set_longhand_from_shorthand(longhand_name)

        return updated

    def _set_shorthand(self, property_name):
        style_map = self._style_map
        updated = False
        shorthand = Shorthand(self._declarations)
        result = shorthand.get_property_value(property_name)
        if len(result) > 0:
            updated = True
            style_map[property_name] = result
            longhand_names = Shorthand.longhands(property_name)
            for longhand_name in longhand_names:
                if longhand_name in style_map:
                    del style_map[longhand_name]

        return updated

    def _update_style(self):
        attributes = self._owner_node.attributes
        if len(self._style_map) == 0:
            if 'style' in attributes:
                del attributes['style']
            return
        style = dict_to_style(self._style_map)
        attributes['style'] = style

    def update(self, property_name, value):
        updated = False
        if len(value) == 0:
            updated = self._remove(property_name)
            if property_name == 'font':
                for sub_property_name in font_sub_property_list:
                    updated |= self._set(sub_property_name, '', restore=True)
            elif property_name in font_sub_property_list:
                updated |= self._set_shorthand('font')
            elif property_name == 'mask-border':
                updated |= self._set_shorthand('mask')
        else:
            if property_name in font_sub_property_list and value != 'initial':
                updated |= self._set_longhand_from_shorthand('font')
            elif property_name == 'mask':
                updated |= self._remove('mask-border', force=True)
            elif property_name == 'mask-border' and value != 'initial':
                updated |= self._set_longhand_from_shorthand('mask')
            updated |= self._set(property_name, value)
            if updated and 'font' in self._style_map:
                for sub_property_name in font_sub_property_list:
                    # updated |= self._set(sub_property_name,
                    #                      'initial',
                    #                      append=False)
                    updated |= self._remove(sub_property_name, force=True)

        if updated:
            self._update_style()


class CSS(object):
    """The CSS-related functions."""
    # TODO: implement CSS.supports(conditionText).

    @staticmethod
    def ch(value):
        """Same as CSSUnitValue(`value`, 'ch').

        Arguments:
            value (float): The value in 'ch' unit, which relative to the
                advance measure of the “0” (ZERO, U+0030) glyph in the
                element’s font.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.CH)

    @staticmethod
    def cm(value):
        """Same as CSSUnitValue(`value`, 'cm').

        Arguments:
            value (float): The value in centimeters.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.CM)

    @staticmethod
    def deg(value):
        """Same as CSSUnitValue(`value`, 'deg').

        Arguments:
            value (float): The value in degrees.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.DEG)

    @staticmethod
    def dpcm(value):
        """Same as CSSUnitValue(`value`, 'dpcm').

        Arguments:
            value (float): The value in dots per centimeter.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.DPCM)

    @staticmethod
    def dpi(value):
        """Same as CSSUnitValue(`value`, 'dpi').

        Arguments:
            value (float): The value in dots per inch.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.DPI)

    @staticmethod
    def dppx(value):
        """Same as CSSUnitValue(`value`, 'dppx').

        Arguments:
            value (float): The value in dots per 'px' unit.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.DPPX)

    @staticmethod
    def em(value):
        """Same as CSSUnitValue(`value`, 'em').

        Arguments:
            value (float): The value in 'em' unit, which relative to the font
                size of the element.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.EM)

    @staticmethod
    def escape(ident):
        s = ''
        for i, ch in enumerate(ident):
            if ch == '\0':
                ch = '\ufffd'
            elif (('\u0001' <= ch <= '\u001f' or ch == '\u007f')
                  or (i == 0 and '0' <= ch <= '9')
                  or (i == 1 and '0' <= ch <= '9' and ident[0] == '-')):
                # escape a character as code point
                ch = '\\{:x} '.format(ord(ch))
            elif i == 0 and ch == '-' and len(ident) == 1:
                # escape a character
                ch = '\\' + ch
            elif (ch >= '\u0080'
                  or ch in ('-', '_')
                  or '0' <= ch <= '9'
                  or 'A' <= ch <= 'Z'
                  or 'a' <= ch <= 'z'):
                pass
            else:
                # escape a character
                ch = '\\' + ch
            s += ch
        return s

    @staticmethod
    def ex(value):
        """Same as CSSUnitValue(`value`, 'ex').

        Arguments:
            value (float): The value in 'ex' unit, which relative to the
                x-height of the element’s font.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.EX)

    @staticmethod
    def fr(value):
        """Same as CSSUnitValue(`value`, 'fr').

        Arguments:
            value (float): The value in flexible length, which represents
                a fraction of the leftover space in the grid container.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.FR)

    @staticmethod
    def grad(value):
        """Same as CSSUnitValue(`value`, 'grad').

        Arguments:
            value (float): The value in gradians.
                There are 400 gradians in a full circle.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.GRAD)

    @staticmethod
    def hz(value):
        """Same as CSSUnitValue(`value`, 'Hz').

        Arguments:
            value (float): The value in hertz.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.HZ)

    @staticmethod
    def ic(value):
        """Same as CSSUnitValue(`value`, 'ic').

        Arguments:
            value (float): The value in 'ic' unit, which relative to the
                advance measure of the “水” (CJK water ideograph, U+6C34)
                glyph in the element’s font.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.IC)

    @staticmethod
    def in_(value):
        """Same as CSSUnitValue(`value`, 'in').

        Arguments:
            value (float): The value in inches.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.IN)

    @staticmethod
    def khz(value):
        """Same as CSSUnitValue(`value`, 'kHz').

        Arguments:
            value (float): The value in kilohertz.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.KHZ)

    @staticmethod
    def lh(value):
        """Same as CSSUnitValue(`value`, 'lh').

        Arguments:
            value (float): The value in 'lh' unit, which relative to the
                line height of the element’s font.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.LH)

    @staticmethod
    def mm(value):
        """Same as CSSUnitValue(`value`, 'mm').

        Arguments:
            value (float): The value in millimeters.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.MM)

    @staticmethod
    def ms(value):
        """Same as CSSUnitValue(`value`, 'ms').

        Arguments:
            value (float): The value in milliseconds.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.MS)

    @staticmethod
    def number(value):
        """Same as CSSUnitValue(`value`, 'number').

        Arguments:
            value (float): The real numbers.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.NUMBER)

    @staticmethod
    def percent(value):
        """Same as CSSUnitValue(`value`, 'percent').

        Arguments:
            value (float): The percentage values.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.PERCENT)

    @staticmethod
    def pc(value):
        """Same as CSSUnitValue(`value`, 'pc').

        Arguments:
            value (float): The value in picas.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.PC)

    @staticmethod
    def pt(value):
        """Same as CSSUnitValue(`value`, 'pt').

        Arguments:
            value (float): The value in points.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.PT)

    @staticmethod
    def px(value):
        """Same as CSSUnitValue(`value`, 'px').

        Arguments:
            value (float): The value in pixels.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.PX)

    @staticmethod
    def q(value):
        """Same as CSSUnitValue(`value`, 'Q').

        Arguments:
            value (float): The value in quarter-millimeters.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.Q)

    @staticmethod
    def rad(value):
        """Same as CSSUnitValue(`value`, 'rad').

        Arguments:
            value (float): The value in radians.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.RAD)

    @staticmethod
    def register_property(descriptor, context=None):
        if not descriptor.name.startswith('--'):
            raise ValueError('Invalid custom property name: '
                             + repr(descriptor.name))
        if context is None:
            from ..window import window
            context = window.document
        property_set = context.registered_property_set
        if descriptor.name in property_set:
            raise ValueError('Custom property {} already exists'.format(
                repr(descriptor.name)))
        property_set[descriptor.name] = descriptor

    @staticmethod
    def rem(value):
        """Same as CSSUnitValue(`value`, 'rem').

        Arguments:
            value (float): The value in 'rem' unit, which relative to the font
                size of the root element.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.REM)

    @staticmethod
    def rlh(value):
        """Same as CSSUnitValue(`value`, 'rlh').

        Arguments:
            value (float): The value in 'rlh' unit, which relative to the
                line height of the root element’s font.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.RLH)

    @staticmethod
    def s(value):
        """Same as CSSUnitValue(`value`, 's').

        Arguments:
            value (float): The value in seconds.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.S)

    @staticmethod
    def supports(property_name, value):
        desc = css_property_descriptor_map.get(property_name.lower())
        if desc is None:
            return False
        return desc.supports(value)

    @staticmethod
    def turn(value):
        """Same as CSSUnitValue(`value`, 'turn').

        Arguments:
            value (float): The value in turns.
                There is 1 turn in a full circle.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.TURN)

    @staticmethod
    def vb(value):
        """Same as CSSUnitValue(`value`, 'vb').

        Arguments:
            value (float): The value in 'vb' unit, which equal to 1% of the
                size of the initial containing block in the direction of the
                root element’s block axis.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.VB)

    @staticmethod
    def vh(value):
        """Same as CSSUnitValue(`value`, 'vh').

        Arguments:
            value (float): The value in 'vh' unit, which equal to 1% of the
                height of the initial containing block.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.VH)

    @staticmethod
    def vi(value):
        """Same as CSSUnitValue(`value`, 'vi').

        Arguments:
            value (float): The value in 'vi' unit, which equal to 1% of the
                size of the initial containing block in the direction of the
                root element’s inline axis.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.VI)

    @staticmethod
    def vmax(value):
        """Same as CSSUnitValue(`value`, 'vmax').

        Arguments:
            value (float): The value in 'vmax' unit, which equal to the
                larger of 'vw' or 'vh'.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.VMAX)

    @staticmethod
    def vmin(value):
        """Same as CSSUnitValue(`value`, 'vmin').

        Arguments:
            value (float): The value in 'vmin' unit, which equal to the
                smaller of 'vw' or 'vh'.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.VMIN)

    @staticmethod
    def vw(value):
        """Same as CSSUnitValue(`value`, 'vw').

        Arguments:
            value (float): The value in 'vw' unit, which equal to 1% of the
                width of the initial containing block.
        Returns:
            CSSUnitValue: A new CSSUnitValue object.
        """
        return CSSUnitValue(value, UnitType.VW)


class CSSRule(object):
    """Represents an abstract, base CSS style rule."""

    UNKNOWN_RULE = 0
    STYLE_RULE = 1
    CHARSET_RULE = 2  # historical
    IMPORT_RULE = 3
    MEDIA_RULE = 4
    FONT_FACE_RULE = 5
    PAGE_RULE = 6
    MARGIN_RULE = 9
    NAMESPACE_RULE = 10
    SUPPORTS_RULE = 12
    FONT_FEATURE_VALUES_RULE = 14

    def __init__(self, rule, rule_type, parent_style_sheet=None,
                 parent_rule=None):
        """Constructs a CSSRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            rule_type (int): The CSS rule type.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        self._type = rule_type
        self._parent_style_sheet = parent_style_sheet
        self._parent_rule = parent_rule
        self._css_text = None
        if rule is not None:
            self._css_text = normalize_text(rule.serialize())

    @property
    def css_text(self):
        """str: A serialization of the CSS rule."""
        # TODO: implement CSSRule.cssText.
        return self._css_text

    @property
    def parent_rule(self):
        """CSSRule: The parent CSS rule."""
        return self._parent_rule

    @property
    def parent_style_sheet(self):
        """CSSStyleSheet: The parent CSS style sheet."""
        return self._parent_style_sheet

    @property
    def type(self):
        """int: The CSS rule type."""
        return self._type


class CSSGroupingRule(CSSRule):
    """Represents an at-rule that contains other rules nested inside itself.
    """

    def __init__(self, rule, rule_type, parent_style_sheet=None,
                 parent_rule=None):
        """Constructs a CSSGroupingRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            rule_type (int): The CSS rule type.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         rule_type,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._css_rules = list()

    @property
    def css_rules(self):
        """list[CSSRule]: A list of the child CSS rules."""
        return self._css_rules

    def delete_rule(self, index):
        """Removes a CSS rule from a list of the child CSS rules at index.

        Arguments:
            index (int): An index position of the child CSS rules to be
                removed.
        """
        del self._css_rules[index]

    def insert_rule(self, rule, index):
        """Inserts a CSS rule into a list of the child CSS rules at index.

        Arguments:
            rule (str): A CSS rule.
            index (int): An index position of the child CSS rules to be
                inserted.
        Returns:
            int: An index position of the child CSS rules.
        """
        css_rules = CSSParser.fromstring(
            rule,
            parent_style_sheet=self.parent_style_sheet,
            parent_rule=self)
        self._css_rules[index:index] = css_rules
        return index


class CSSConditionRule(CSSGroupingRule, ABC):
    """Represents all the 'conditional' at-rules, which consist of a condition
    and a statement block.
    """

    def __init__(self, rule, rule_type, parent_style_sheet=None,
                 parent_rule=None):
        """Constructs a CSSConditionRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            rule_type (int): The CSS rule type.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         rule_type,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)

    @property
    @abstractmethod
    def condition_text(self):
        """str: The condition of the rule."""
        raise NotImplementedError


class MediaList(MutableSequence):
    """Represents a collection of media queries."""

    def __init__(self):
        self._items = list()

    def __delitem__(self, index):
        del self._items[index]

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return repr(self._items)

    def __setitem__(self, index, item):
        self._items[index] = item

    @property
    def length(self):
        """int: The number of media queries."""
        return len(self)

    @property
    def media_text(self):
        """str: A serialization of the collection of media queries."""
        # FIXME: implement serialize-a-media-query-list.
        # https://drafts.csswg.org/cssom/#serialize-a-media-query-list
        return ', '.join(self._items).lower()

    @media_text.setter
    def media_text(self, value):
        media_text = normalize_text(value)
        if len(media_text) == 0:
            self.clear()
            return
        m = MediaList._parse_media_query_list(value)
        self._items = m

    @staticmethod
    def _parse_media_query(medium):
        m = MediaList._parse_media_query_list(medium)
        return m[0] if len(m) == 1 else None

    @staticmethod
    def _parse_media_query_list(medium):
        m = [x.strip() for x in medium.split(',')]
        return m

    def append(self, medium):
        """Adds the media query to the collection of media queries.
        Same as append_medium().

        Arguments:
            medium (str): The media query to be added.
        """
        self.append_medium(medium)

    def append_medium(self, medium):
        """Adds the media query to the collection of media queries.

        Arguments:
            medium (str): The media query to be added.
        """
        m = MediaList._parse_media_query(medium)
        if m is None or m in self:
            return
        index = len(self)
        self.insert(index, m)

    def delete_medium(self, medium):
        """Removes the media query in the collection of media queries.

        Arguments:
            medium (str): The media query to be removed.
        """
        m = MediaList._parse_media_query(medium)
        if m is None:
            return
        index = self.index(m)
        del self[index]

    def insert(self, index, medium):
        """Inserts the media query into the collection of media queries at
        index.

        Arguments:
            index (int): An index position of the collection of media queries.
            medium (str): The media query to be added.
        """
        self[index:index] = [medium.strip()]

    def item(self, index):
        """Returns a serialization of the media query in the collection of
        media queries given by index.

        Arguments:
            index (int): An index position of the collection of media queries.
        Returns:
            str: The media query.
        """
        return self[index]


class StyleSheet(object):
    """Represents an abstract, base style sheet."""

    def __init__(self, type_=None, href=None, owner_node=None,
                 parent_style_sheet=None, title=None, media=None,
                 disabled=False):
        """Constructs a StyleSheet object.

        Arguments:
            type_ (str, optional): The type of the style sheet.
            href (str, optional): The location of the style sheet.
            owner_node (Element, optional): The owner node of the style sheet.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            title (str, optional): The title of the style sheet.
            media (str, optional): The media queries of the style sheet.
            disabled (bool, optional): The disabled flag of the style sheet.
        """
        self._type = type_ if type_ is not None else 'text/css'
        self._media = MediaList()
        if media is not None:
            self._media.media_text = media
        self._href = href
        self._owner_node = owner_node
        self._parent_style_sheet = parent_style_sheet
        self._title = title
        self._disabled = disabled

    @property
    def disabled(self):
        """bool: The disabled flag of the style sheet."""
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = value

    @property
    def href(self):
        """str: The location of the style sheet."""
        return self._href

    @property
    def media(self):
        """MediaList: The media queries of the style sheet."""
        return self._media

    @property
    def owner_node(self):
        """Element: The owner node of the style sheet."""
        return self._owner_node

    @property
    def parent_style_sheet(self):
        """CSSStyleSheet: The parent CSS style sheet."""
        return self._parent_style_sheet

    @property
    def title(self):
        """str: The title of the style sheet."""
        return self._title

    @property
    def type(self):
        """str: The type of the style sheet."""
        return self._type


class CSSFontFaceRule(CSSRule):
    """Represents the '@font-face' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSFontFaceRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.FONT_FACE_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._style = CSSStyleDeclaration(rule, parent_rule=self)

    def __repr__(self):
        return repr({
            type(self).__name__: {
                type(self._style).__name__: self._style,
            }
        })

    @property
    def style(self):
        """CSSStyleDeclaration: A CSS declaration block associated with the
        at-rule.
        """
        return self._style


class CSSFontFeatureValuesRule(CSSRule):
    """Represents the '@font-feature-values' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSFontFeatureValuesRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.FONT_FEATURE_VALUES_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._font_family = normalize_text(tinycss2.serialize(rule.prelude))
        self._annotation = CaseInsensitiveMapping()
        self._character_variant = CaseInsensitiveMapping()
        self._ornaments = CaseInsensitiveMapping()
        self._styleset = CaseInsensitiveMapping()
        self._stylistic = CaseInsensitiveMapping()
        self._swash = CaseInsensitiveMapping()
        self._parse_content(rule.content)

    def __repr__(self):
        return repr({
            type(self).__name__: {
                'font_family': self._font_family,
                'annotation': self._annotation,
                'character_variant': self._character_variant,
                'ornaments': self._ornaments,
                'styleset': self._styleset,
                'stylistic': self._stylistic,
                'swash': self._swash,
            }
        })

    def _parse_content(self, content):
        nodes = tinycss2.parse_rule_list(content,
                                         skip_comments=True,
                                         skip_whitespace=True)
        for node in nodes:
            if node.type == 'at-rule':
                # tinycss2.parse_one_component_value() returns ParseError
                feature_type = node.lower_at_keyword
                name = None
                feature_values = None
                for token in node.content:
                    if token.type == 'ident':
                        name = token.value
                    elif token.type == 'literal' and token.value == ':':
                        if name is not None:
                            feature_values = list()
                    elif token.type == 'number' and token.is_integer:
                        if feature_values is not None and token.int_value >= 0:
                            feature_values.append(token.int_value)
                    elif token.type == 'literal' and token.value == ';':
                        if (name is not None
                                and feature_values is not None
                                and len(feature_values) > 0):
                            if feature_type == 'annotation':
                                self._annotation[name] = feature_values
                            elif feature_type == 'character-variant':
                                self._character_variant[name] = feature_values
                            elif feature_type == 'ornaments':
                                self._ornaments[name] = feature_values
                            elif feature_type == 'styleset':
                                self._styleset[name] = feature_values
                            elif feature_type == 'stylistic':
                                self._stylistic[name] = feature_values
                            elif feature_type == 'swash':
                                self._swash[name] = feature_values
                        name = None
                        feature_values = None

    @property
    def font_family(self):
        """str: The list of one or more font families."""
        return self._font_family

    @property
    def annotation(self):
        """CaseInsensitiveMapping: The '@annotation' feature values."""
        return self._annotation

    @property
    def character_variant(self):
        """CaseInsensitiveMapping: The '@character-variant' feature values.
        """
        return self._character_variant

    @property
    def ornaments(self):
        """CaseInsensitiveMapping: The '@ornaments' feature values."""
        return self._ornaments

    @property
    def styleset(self):
        """CaseInsensitiveMapping: The '@styleset' feature values."""
        return self._styleset

    @property
    def stylistic(self):
        """CaseInsensitiveMapping: The '@stylistic' feature values."""
        return self._stylistic

    @property
    def swash(self):
        """CaseInsensitiveMapping: The '@swash' feature values."""
        return self._swash


class CSSImportRule(CSSRule):
    """Represents the '@import' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSImportRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.IMPORT_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._href = None
        self._media = MediaList()
        self._style_sheet = None
        self._parse_prelude(rule.prelude)

    def __repr__(self):
        return repr({
            type(self).__name__: {
                'href': self._href,
                'media': self._media,
                'style_sheet': self._style_sheet,
            }
        })

    def _parse_prelude(self, prelude):
        if self.parent_style_sheet is not None:
            owner_node = self.parent_style_sheet.owner_node
            base_url = self.parent_style_sheet.href
            if base_url is None and owner_node is not None:
                doc = owner_node.owner_document
                if doc is not None:
                    base_url = doc.location.href
        else:
            owner_node = None
            base_url = None
        mediums = list()
        for token in prelude:
            if self._href is None:
                if token.type in ('string', 'url'):
                    url = normalize_url(token.value, base_url)
                    self._href = url.href
            else:
                mediums.append(token)
        if len(mediums) > 0:
            self._media.media_text = tinycss2.serialize(mediums)
        if self._href is None:
            self._style_sheet = CSSStyleSheet(owner_node=owner_node,
                                              media=self._media.media_text,
                                              owner_rule=self)
        else:
            self._style_sheet = CSSParser.parse(self._href,
                                                owner_node=owner_node,
                                                parent_rule=self)

    @property
    def href(self):
        """str: The location of the style sheet."""
        return self._href

    @property
    def media(self):
        """MediaList: The media queries of the style sheet."""
        return self._media

    @property
    def style_sheet(self):
        """CSSStyleSheet: The associated CSS style sheet."""
        return self._style_sheet


class CSSMediaRule(CSSConditionRule):
    """Represents the '@media' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSMediaRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.MEDIA_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._media = MediaList()
        self._media.media_text = tinycss2.serialize(rule.prelude)
        rules = tinycss2.parse_rule_list(rule.content,
                                         skip_comments=True,
                                         skip_whitespace=True)
        css_rules = CSSParser.parse_rules(
            rules,
            parent_style_sheet=parent_style_sheet,
            parent_rule=self)
        self.css_rules.extend(css_rules)

    def __repr__(self):
        return repr({
            type(self).__name__: {
                'media': self._media,
                'css_rules': self._css_rules,
            }
        })

    @property
    def condition_text(self):
        """str: A serialization of the collection of media queries.
        Same as media.media_text.
        """
        return self._media.media_text

    @condition_text.setter
    def condition_text(self, value):
        self._media.media_text = value

    @property
    def media(self):
        """MediaList: The media queries of the style sheet."""
        return self._media


class CSSNamespaceRule(CSSRule):
    """Represents the '@namespace' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSNamespaceRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.NAMESPACE_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._namespace_uri = None
        self._prefix = ''
        self._parse_prelude(rule.prelude)

    def __repr__(self):
        return repr({
            type(self).__name__: {
                'namespace_uri': self._namespace_uri,
                'prefix': self._prefix,
            }
        })

    def _parse_prelude(self, prelude):
        for token in prelude:
            if token.type == 'url':
                self._namespace_uri = token.value
            elif token.type == 'ident':
                self._prefix = token.value

    @property
    def namespace_uri(self):
        """str: The namespace of the '@namespace' at-rule."""
        return self._namespace_uri

    @property
    def prefix(self):
        """str: The prefix of the '@namespace' at-rule."""
        return self._prefix


class CSSStyleDeclaration(MutableMapping):
    """Represents a CSS declaration block."""

    def __init__(self, rule=None, parent_rule=None, owner_node=None,
                 inline_style=False):
        """Constructs a CSSStyleDeclaration object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_rule (CSSRule, optional): The parent CSS rule.
            owner_node (Element, optional): The owner node of the inline style
                properties.
            inline_style (bool, optional): Enables the inline CSS styles.
        """
        self._parent_rule = parent_rule
        self._css_text = None
        self._property_map = OrderedDict()
        self._owner_node = owner_node
        self._inline_style = inline_style
        self._readonly = False
        if rule is not None:
            self._css_text = normalize_text(tinycss2.serialize(rule.content))
            self._parse_content(rule.content)

    def __contains__(self, property_name):
        if not property_name.startswith('--'):
            property_name = property_name.lower()
        return property_name in self._declarations()

    def __delitem__(self, property_name):
        self.remove_property(property_name)

    def __getitem__(self, property_name):
        return self.get_property_value(property_name)

    def __iter__(self):
        return iter(self._declarations())

    def __len__(self):
        return len(self._declarations())

    def __repr__(self):
        return repr(self._declarations())

    def __setitem__(self, property_name, value):
        """Sets a CSS declaration property with a value in the declarations.

        Arguments:
            property_name (str): A property name of a CSS declaration.
            value (str, None): A CSS value of the declarations.
        """
        self.set_property(property_name, value)

    @property
    def css_text(self):
        """str: A serialization of the CSS rule."""
        # TODO: implement CSSStyleDeclaration.cssText.
        return self._css_text

    @property
    def length(self):
        """int: The number of CSS declarations in the declarations."""
        return len(self)

    @property
    def parent_rule(self):
        """CSSRule: The parent CSS rule."""
        return self._parent_rule

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, readonly):
        self._readonly = readonly

    def _declarations(self):
        if self._readonly:
            return self._property_map.copy()
        elif self._owner_node is None or not self._inline_style:
            return self._property_map

        # 'style' attribute => CSS declarations
        attr = self._owner_node.attributes.get_named_item_ns(None, 'style')
        style = '' if attr is None else attr.value
        property_map = style_to_dict(style)
        declarations = self._property_map
        for property_name in declarations:
            if Longhand.is_longhand(property_name):
                shorthand_names = Longhand.shorthands(property_name)
                for shorthand_name in shorthand_names:
                    if shorthand_name in property_map:
                        shorthand = Shorthand(declarations)
                        result = shorthand.get_property_value(shorthand_name)
                        if result == property_map[shorthand_name]:
                            del property_map[shorthand_name]
                            break
            elif (property_name in property_map
                  and declarations[property_name][0]
                  == property_map[property_name]):
                del property_map[property_name]

        for property_name, value in property_map.items():
            needs_update = False
            priority = ''
            if Shorthand.is_shorthand(property_name):
                shorthand = Shorthand(declarations)
                result = shorthand.get_property_value(property_name)
                if result != value:
                    needs_update = True
                    priority = shorthand.get_property_priority(property_name)
            else:
                if property_name not in declarations:
                    needs_update = True
                elif value != declarations[property_name][0]:
                    needs_update = True
                    priority = declarations[property_name][1]
            if needs_update:
                self._set_property_internal(declarations,
                                            property_name,
                                            value,
                                            priority)

        return declarations

    def _parse_content(self, content):
        nodes = tinycss2.parse_declaration_list(content,
                                                skip_comments=True,
                                                skip_whitespace=True)
        for node in nodes:
            if node.type == 'declaration':
                property_name = node.name
                value = tinycss2.serialize(node.value)
                priority = 'important' if node.important else ''
                self.set_property(property_name, value, priority)

    def _set_css_declaration(self, declarations, property_name,
                             component_list, priority):
        _ = self
        value = tinycss2.serialize(component_list).strip()
        if len(value) == 0:
            return False
        if value.lower() in css_color_keyword_set | css_wide_keyword_set:
            value = value.lower()
        if property_name in declarations:
            declarations.move_to_end(property_name)
        declarations[property_name] = value, priority
        return True

    def _set_property_internal(self, declarations, property_name, value,
                               priority):
        component_list = tinycss2.parse_component_value_list(
            value,
            skip_comments=True)
        if len(component_list) == 0:
            return False, ''
        result = ''
        if Shorthand.is_shorthand(property_name):
            shorthand = Shorthand(declarations)
            updated = shorthand.set_css_declaration(property_name,
                                                    component_list,
                                                    priority)
            if updated:
                result = shorthand.get_property_value(property_name)
        else:
            updated = self._set_css_declaration(declarations,
                                                property_name,
                                                component_list,
                                                priority)
            if updated:
                result = declarations[property_name][0]
        return updated, result

    def _update_style_attribute(self, declarations, property_name, value):
        if self._owner_node is None:
            return
        style = _StyleAttribute(declarations, self._owner_node)
        style.update(property_name, value)

    def get_property_priority(self, property_name):
        """Returns the important flag of the first exact match of name in the
        declarations.

        Arguments:
            property_name (str): A property name of a CSS declaration.
        Returns:
            str: The important flag of the declarations.
        """
        declarations = self._declarations()
        if not property_name.startswith('--'):
            property_name = property_name.lower()
            if Shorthand.is_shorthand(property_name):
                shorthand = Shorthand(declarations)
                priority = shorthand.get_property_priority(property_name)
                return priority
        if property_name not in declarations:
            return ''
        priority = declarations[property_name][1]
        return priority

    def get_property_value(self, property_name):
        """Returns a CSS value of the first exact match of name in the
        declarations.

        Arguments:
            property_name (str): A property name of a CSS declaration.
        Returns:
            str: A CSS value of the declarations.
        """
        declarations = self._declarations()
        if not property_name.startswith('--'):
            property_name = property_name.lower()
            if Shorthand.is_shorthand(property_name):
                shorthand = Shorthand(declarations)
                value = shorthand.get_property_value(property_name)
                return value
        if property_name not in declarations:
            return ''
        value = declarations[property_name][0]
        return value

    def item(self, index):
        property_name = list(self.keys())[index]
        return property_name

    def items(self):
        return self._declarations().items()

    def keys(self):
        return self._declarations().keys()

    def remove_property(self, property_name):
        """Removes a CSS declaration property of the first exact match of name
        in the declarations.

        Arguments:
            property_name (str): A property name of a CSS declaration.
        """
        if self._readonly:
            raise NoModificationAllowedError('The object can not be modified')
        if not property_name.startswith('--'):
            property_name = property_name.lower()
        value = self.get_property_value(property_name)
        removed = False
        declarations = self._declarations()
        if Shorthand.is_shorthand(property_name):
            shorthand = Shorthand(declarations)
            removed = shorthand.remove_property(property_name)
        elif property_name in declarations:
            del declarations[property_name]
            removed = True
        if removed and self._inline_style:
            self._update_style_attribute(declarations, property_name, '')
        return value

    def set_property(self, property_name, value, priority=None):
        """Sets a CSS declaration property with a value and an important flag
        in the declarations.

        Arguments:
            property_name (str): A property name of a CSS declaration.
            value (str): A CSS value of the declarations.
            priority (str, optional): An important flag of the
                declarations.
        """
        if self._readonly:
            raise NoModificationAllowedError('The object can not be modified')
        value = normalize_text(value)
        if len(value) == 0:
            self.remove_property(property_name)
            return

        if not property_name.startswith('--'):
            property_name = property_name.lower()
        if priority is None:
            priority = self.get_property_priority(property_name)
        else:
            priority = priority.lower()
        if priority not in ('', 'important'):
            return
        declarations = self._declarations()
        updated, result = self._set_property_internal(declarations,
                                                      property_name,
                                                      value,
                                                      priority)
        if updated and self._inline_style:
            self._update_style_attribute(declarations, property_name, result)

    def values(self):
        return self._declarations().values()


class CSSStyleRule(CSSRule):
    """Represents a style rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSStyleRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.STYLE_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._selector_text = normalize_text(tinycss2.serialize(rule.prelude))
        self._style = CSSStyleDeclaration(rule, parent_rule=self)

    def __repr__(self):
        return repr({
            type(self).__name__: {
                'selector_text': self._selector_text,
                'style': self._style,
            }
        })

    @property
    def selector_text(self):
        """str: The associated group of selectors."""
        return self._selector_text

    @property
    def style(self):
        """CSSStyleDeclaration: A CSS declaration block associated with the
        at-rule.
        """
        return self._style


class CSSStyleSheet(StyleSheet):
    """Represents a CSS style sheet."""

    def __init__(self, owner_rule=None, **extra):
        """Constructs a CSSStyleSheet object.

        Arguments:
            owner_rule (CSSRule, optional): The owner CSS rule.
            **extra: See StyleSheet.__init__().
        """
        super().__init__(**extra)
        self._owner_rule = owner_rule
        self._css_rules = list()

    def __repr__(self):
        return repr({
            type(self).__name__: {
                'href': self._href,
                'media': self._media,
                'title': self._title,
                'css_rules': self._css_rules,
            }
        })

    @property
    def owner_rule(self):
        """CSSRule: The owner CSS rule."""
        return self._owner_rule

    @property
    def css_rules(self):
        """list[CSSRule]: A list of the child CSS rules."""
        return self._css_rules

    def delete_rule(self, index):
        """Removes a CSS rule from a list of the child CSS rules at index.

        Arguments:
            index (int): An index position of the child CSS rules to be
                removed.
        """
        del self._css_rules[index]

    def insert_rule(self, rule, index=0):
        """Inserts a CSS rule into a list of the child CSS rules at index.

        Arguments:
            rule (str): A CSS rule.
            index (int, optional): An index position of the child CSS rules to
            be inserted.
        Returns:
            int: An index position of the child CSS rules.
        """
        css_rules = CSSParser.fromstring(
            rule,
            parent_style_sheet=self,
            parent_rule=self._owner_rule)
        self._css_rules[index:index] = css_rules
        return index


class CSSParser(object):
    @classmethod
    def fromstring(cls, stylesheet, parent_style_sheet=None,
                   parent_rule=None):
        """Parses the CSS style sheet or fragment from a string.

        Arguments:
            stylesheet (str): The CSS style sheet to be parsed.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        Returns:
            list[CSSRule]: A list of CSS rules.
       """
        try:
            rules = tinycss2.parse_stylesheet(
                stylesheet,
                skip_comments=True,
                skip_whitespace=True)
            css_rules = CSSParser.parse_rules(
                rules,
                parent_style_sheet=parent_style_sheet,
                parent_rule=parent_rule)
            return css_rules
        except URLError as exp:
            logger = getLogger('{}.{}'.format(__name__, cls.__name__))
            logger.info('failed to parse: ' + repr(exp))
            return []

    @classmethod
    def parse(cls, url, owner_node=None, parent_style_sheet=None,
              parent_rule=None, encoding=None):
        """Parses the CSS style sheet.

        Arguments:
            url (str): The location of the style sheet.
            owner_node (Element, optional): The owner node of the style sheet.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
            encoding (str, optional): An advisory character encoding for the
                referenced style sheet.
        Returns:
            CSSStyleSheet: A new CSSStyleSheet object.
        """
        extra = dict({
            'type_': None,
            'href': None,
            'owner_node': owner_node,
            'parent_style_sheet': parent_style_sheet,
            'title': None,
            'media': None,
        })
        if owner_node is not None:
            extra.update({
                'type_': owner_node.get('type'),
                'href': owner_node.get('href'),
                'title': owner_node.get('title'),
                'media': owner_node.get('media'),
            })
        css_style_sheet = CSSStyleSheet(owner_rule=parent_rule, **extra)
        logger = getLogger('{}.{}'.format(__name__, cls.__name__))
        try:
            logger.debug('urlopen \'{}\''.format(url))
            data, headers = load(url)
            if encoding is None:
                content_type = get_content_type(headers)
                if content_type is None:
                    encoding = 'utf-8'
                else:
                    encoding = content_type.get('charset', 'utf-8')
            rules, encoding = tinycss2.parse_stylesheet_bytes(
                css_bytes=data,
                protocol_encoding=encoding,
                skip_comments=True,
                skip_whitespace=True)
            css_rules = CSSParser.parse_rules(
                rules,
                parent_style_sheet=css_style_sheet,
                parent_rule=parent_rule)
            css_style_sheet.css_rules.extend(css_rules)
        except URLError as exp:
            logger.info(
                'failed to parse: \'{}\': {}'.format(url, repr(exp)))
        return css_style_sheet

    @staticmethod
    def parse_rules(rules, parent_style_sheet=None, parent_rule=None):
        css_rules = list()
        for rule in rules:
            if rule.type == 'at-rule':
                if rule.lower_at_keyword == 'font-face':
                    # @font-face at-rule
                    css_rule = CSSFontFaceRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
                elif rule.lower_at_keyword == 'font-feature-values':
                    # @font-feature-values at-rule
                    css_rule = CSSFontFeatureValuesRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
                elif rule.lower_at_keyword == 'import':
                    # @import at-rule
                    css_rule = CSSImportRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
                elif rule.lower_at_keyword == 'media':
                    # @media at-rule
                    css_rule = CSSMediaRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
                elif rule.lower_at_keyword == 'namespace':
                    # @namespace at-rule
                    css_rule = CSSNamespaceRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
            elif rule.type == 'qualified-rule':
                css_rule = CSSStyleRule(
                    rule,
                    parent_style_sheet=parent_style_sheet,
                    parent_rule=parent_rule)
                css_rules.append(css_rule)
        return css_rules
