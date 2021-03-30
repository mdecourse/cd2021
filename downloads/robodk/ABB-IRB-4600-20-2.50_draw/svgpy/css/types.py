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


# TODO: add support for <transform-function> and <transform-list>.

import math
import re
from abc import abstractmethod
from collections import OrderedDict
from collections.abc import Iterable, Mapping, MutableMapping, MutableSequence
from decimal import Decimal
from enum import Enum

import tinycss2

from .props import PropertyDescriptor, PropertySyntax, \
    css_color_keyword_set, css_property_descriptor_map, css_wide_keyword_set
from ..formatter import format_number_sequence

_RE_REAL_NUMBER = re.compile(r'[+-]?[0-9]*\.?[0-9]+(e[+-]?[0-9]+)?',
                             re.IGNORECASE)

_RE_URL_FUNCTION = re.compile(r'^url\((?P<value>[^)]+)\)$')

_RE_VAR_FUNCTION = re.compile(r'(^|\s|\t|\*|/|\(|,)var\(')

list_valued_properties = [
    'animation', 'animation-delay', 'animation-direction',
    'animation-duration', 'animation-fill-mode', 'animation-iteration-count',
    'animation-name', 'animation-play-state', 'animation-timing-function',
    'background-attachment', 'background-clip', 'background-image',
    'background-origin', 'background-repeat', 'background-size',
    'font-family', 'mask', 'mask-clip', 'mask-composite', 'mask-image',
    'mask-mode', 'mask-origin', 'mask-position', 'mask-repeat', 'mask-size',
]
# FIXME: update a list of list-valued properties.
# https://github.com/w3c/css-houdini-drafts/issues/644

single_multi_valued_properties = [
    'd', 'font', 'font-family', 'font-feature-settings',
    'font-variation-settings', 'mask', 'mask-clip', 'mask-composite',
    'mask-image', 'mask-mode', 'mask-origin', 'mask-position', 'mask-repeat',
    'mask-size', 'shape-inside', 'stroke-dasharray',
]


class CSSMathOperator(Enum):
    """Represents the [css-typed-om] CSSMathOperator."""

    SUM = 'sum'
    PRODUCT = 'product'
    NEGATE = 'negate'
    INVERT = 'invert'
    MIN = 'min'
    MAX = 'max'
    CLAMP = 'clamp'


class CSSNumericBaseType(object):
    """Represents the [css-typed-om] CSSNumericBaseType."""

    LENGTH = 'length'
    ANGLE = 'angle'
    TIME = 'time'
    FREQUENCY = 'frequency'
    RESOLUTION = 'resolution'
    FLEX = 'flex'
    PERCENT = 'percent'


class CSSNumericType(CSSNumericBaseType, OrderedDict):
    """Represents the [css-typed-om] CSSNumericType."""

    PERCENT_HINT = 'percent_hint'

    def __repr__(self):
        return repr({key: value for key, value in self.items()})

    @property
    def angle(self):
        return self.get(CSSNumericType.ANGLE)

    @angle.setter
    def angle(self, power):
        self[CSSNumericType.ANGLE] = power

    @property
    def flex(self):
        return self.get(CSSNumericType.FLEX)

    @flex.setter
    def flex(self, power):
        self[CSSNumericType.FLEX] = power

    @property
    def frequency(self):
        return self.get(CSSNumericType.FREQUENCY)

    @frequency.setter
    def frequency(self, power):
        self[CSSNumericType.FREQUENCY] = power

    @property
    def length(self):
        return self.get(CSSNumericType.LENGTH)

    @length.setter
    def length(self, power):
        self[CSSNumericType.LENGTH] = power

    @property
    def percent(self):
        return self.get(CSSNumericType.PERCENT)

    @percent.setter
    def percent(self, power):
        self[CSSNumericType.PERCENT] = power

    @property
    def percent_hint(self):
        return self.get(CSSNumericType.PERCENT_HINT)

    @percent_hint.setter
    def percent_hint(self, power):
        self[CSSNumericType.PERCENT_HINT] = power

    @property
    def resolution(self):
        return self.get(CSSNumericType.RESOLUTION)

    @resolution.setter
    def resolution(self, power):
        self[CSSNumericType.RESOLUTION] = power

    @property
    def time(self):
        return self.get(CSSNumericType.TIME)

    @time.setter
    def time(self, power):
        self[CSSNumericType.TIME] = power

    @staticmethod
    def add_types(type1, type2):
        """Adds two types `type1` and `type2`.

        Arguments:
            type1 (CSSNumericType): The type object.
            type2 (CSSNumericType): The type object.
        Returns:
            CSSNumericType: A new type object or None.
        """
        type1 = type1.copy()
        type2 = type2.copy()
        percent_hint1 = type1.percent_hint
        percent_hint2 = type2.percent_hint
        if percent_hint1 is not None and percent_hint2 is not None:
            if percent_hint1 != percent_hint2:
                return None
        elif percent_hint1 is not None and percent_hint2 is None:
            CSSNumericType.apply_percent_hint(type2, percent_hint1)
        elif percent_hint1 is None and percent_hint2 is not None:
            CSSNumericType.apply_percent_hint(type1, percent_hint2)

        final_type = CSSNumericType()
        base_type_keys = {CSSNumericType.LENGTH, CSSNumericType.ANGLE,
                          CSSNumericType.TIME, CSSNumericType.FREQUENCY,
                          CSSNumericType.RESOLUTION, CSSNumericType.FLEX}
        keys1 = {key for key in set(type1) & base_type_keys
                 if type1[key] != 0}
        keys2 = {key for key in set(type2) & base_type_keys
                 if type2[key] != 0}
        if (all(key in type2 for key in keys1)
                and all(key in type1 for key in keys2)
                and all(type1[key] == type2[key]
                        for key in keys1 | keys2)):
            final_type.update(type1)
            for key in type2:
                if key not in final_type:
                    final_type[key] = type2[key]
            return final_type

        if (any([type1.percent, type2.percent])
                and (any([type1[key] for key in type1
                          if key != CSSNumericType.PERCENT])
                     or any([type2[key] for key in type2
                             if key != CSSNumericType.PERCENT]))):
            for key in base_type_keys:
                value1 = type1.get(key, 0)
                value2 = type2.get(key, 0)
                if any([value1, value2]) and value1 != value2:
                    CSSNumericType.apply_percent_hint(type1, key)
                    CSSNumericType.apply_percent_hint(type2, key)
                if type1.get(key, 0) != type2.get(key, 0):
                    return None
            final_type.update(type1)
            for key in set(type2) & base_type_keys:
                if key not in final_type and type2[key] != 0:
                    final_type[key] = type2[key]
            return final_type

        return None

    @staticmethod
    def apply_percent_hint(type_, hint):
        """Applies the percent hint `hint` to a `type_`.

        Arguments:
            type_ (CSSNumericType): A type object.
            hint (str): The percent hint.
        Returns:
            CSSNumericType: A type object.
        """
        if hint not in type_:
            type_[hint] = 0
        if CSSNumericType.PERCENT in type_:
            type_[hint] += type_[CSSNumericType.PERCENT]
            type_[CSSNumericType.PERCENT] = 0
        type_[CSSNumericType.PERCENT_HINT] = hint
        return type_

    @staticmethod
    def create_type(unit):
        """Creates a type from a string `unit`.

        Arguments:
            unit (str): The unit string.
        Returns:
            CSSNumericType: A new type object.
        """
        unit = unit.lower()
        result = CSSNumericType()
        if unit == UnitType.NUMBER:
            # "number"
            pass  # empty map
        elif unit == UnitType.PERCENT:
            # "percent"
            result.percent = 1
        elif unit in (UnitType.EM, UnitType.EX, UnitType.CH, UnitType.IC,
                      UnitType.REM, UnitType.LH, UnitType.RLH, UnitType.VW,
                      UnitType.VH, UnitType.VI, UnitType.VB, UnitType.VMIN,
                      UnitType.VMAX, UnitType.CM, UnitType.MM, UnitType.Q,
                      UnitType.IN, UnitType.PT, UnitType.PC, UnitType.PX):
            # <length>
            result.length = 1
        elif unit in (UnitType.DEG, UnitType.GRAD, UnitType.RAD,
                      UnitType.TURN):
            # <angle>
            result.angle = 1
        elif unit in (UnitType.S, UnitType.MS):
            # <time>
            result.time = 1
        elif unit in (UnitType.HZ, UnitType.KHZ):
            # <frequency>
            result.frequency = 1
        elif unit in (UnitType.DPI, UnitType.DPCM, UnitType.DPPX):
            # <resolution>
            result.resolution = 1
        elif unit == UnitType.FR:
            # <flex>
            result.flex = 1
        else:
            raise ValueError('Invalid unit: ' + repr(unit))
        return result

    @staticmethod
    def create_type_from_unit_map(unit_map):
        """Creates a type from a unit map `unit_map`.

        Arguments:
            unit_map (dict): The unit map.
        Returns:
            CSSNumericType: A new type object or None.
        """
        types = list()
        if len(unit_map) == 0:
            types.append(CSSNumericType())
        else:
            for unit, power in unit_map.items():
                type_ = CSSNumericType.create_type(unit)
                key = list(type_.keys())[0]
                type_[key] = power
                types.append(type_)
        type1 = types[0]
        for type2 in types[1:]:
            type1 = CSSNumericType.multiply_types(type1, type2)
            if type1 is None:
                return None
        return type1

    @staticmethod
    def multiply_types(type1, type2):
        """Multiplies two types `type1` and `type2`.

        Arguments:
            type1 (CSSNumericType): The type object.
            type2 (CSSNumericType): The type object.
        Returns:
            CSSNumericType: A new type object or None.
        """
        type1 = type1.copy()
        type2 = type2.copy()
        percent_hint1 = type1.percent_hint
        percent_hint2 = type2.percent_hint
        if percent_hint1 is not None and percent_hint2 is not None:
            if percent_hint1 != percent_hint2:
                return None
        elif percent_hint1 is not None and percent_hint2 is None:
            CSSNumericType.apply_percent_hint(type2, percent_hint1)
        elif percent_hint1 is None and percent_hint2 is not None:
            CSSNumericType.apply_percent_hint(type1, percent_hint2)

        final_type = CSSNumericType()
        final_type.update(type1)
        base_type_keys = {CSSNumericType.LENGTH, CSSNumericType.ANGLE,
                          CSSNumericType.TIME, CSSNumericType.FREQUENCY,
                          CSSNumericType.RESOLUTION, CSSNumericType.FLEX}
        for key in set(type2) & base_type_keys:
            power = type2[key]
            if key in final_type:
                final_type[key] += power
            else:
                final_type[key] = power
        return final_type

    @staticmethod
    def product_unit_maps(unit_map1, unit_map2):
        """Returns a product of two unit maps `unit_map1` and `unit_map2`.

        Arguments:
            unit_map1 (dict): The unit map.
            unit_map2 (dict): The unit map.
        Returns:
            dict: A new unit map.
        """
        result = unit_map1.copy()
        for unit, power in unit_map2.items():
            if unit in result:
                result[unit] += power
            else:
                result[unit] = power
        return result


class UnitType(object):
    UNKNOWN = None

    NUMBER = 'number'
    PERCENT = 'percent'

    # <length>
    EM = 'em'
    EX = 'ex'
    CH = 'ch'
    IC = 'ic'
    REM = 'rem'
    LH = 'lh'
    RLH = 'rlh'
    VW = 'vw'
    VH = 'vh'
    VI = 'vi'
    VB = 'vb'
    VMIN = 'vmin'
    VMAX = 'vmax'
    CM = 'cm'
    MM = 'mm'
    Q = 'q'
    IN = 'in'
    PT = 'pt'
    PC = 'pc'
    PX = 'px'

    # <angle>
    DEG = 'deg'
    GRAD = 'grad'
    RAD = 'rad'
    TURN = 'turn'

    # <time>
    S = 's'
    MS = 'ms'

    # <frequency>
    HZ = 'hz'
    KHZ = 'khz'

    # <resolution>
    DPI = 'dpi'
    DPCM = 'dpcm'
    DPPX = 'dppx'

    # <flex>
    FR = 'fr'

    @staticmethod
    def get_canonical_unit(unit):
        unit = unit.lower()
        if unit == UnitType.NUMBER:
            # "number"
            return UnitType.NUMBER
        elif unit in (UnitType.CM, UnitType.MM, UnitType.Q, UnitType.IN,
                      UnitType.PT, UnitType.PC, UnitType.PX):
            # <absolute length>
            return UnitType.PX
        elif unit in (UnitType.DEG, UnitType.GRAD, UnitType.RAD,
                      UnitType.TURN):
            # <angle>
            return UnitType.DEG
        elif unit in (UnitType.S, UnitType.MS):
            # <time>
            return UnitType.MS
        elif unit in (UnitType.HZ, UnitType.KHZ):
            # <frequency>
            return UnitType.HZ
        elif unit in (UnitType.DPI, UnitType.DPCM, UnitType.DPPX):
            # <resolution>
            return UnitType.DPPX
        return UnitType.UNKNOWN  # cannot convert

    @staticmethod
    def get_conversion_ratio(unit):
        unit = unit.lower()
        if unit == UnitType.CM:
            return Decimal(96) / Decimal(2.54)
        elif unit == UnitType.MM:
            return Decimal(96) / Decimal(2.54) / Decimal(10)
        elif unit == UnitType.Q:
            return Decimal(96) / Decimal(2.54) / Decimal(40)
        elif unit == UnitType.IN:
            return Decimal(96)
        elif unit == UnitType.PT:
            return Decimal(96) / Decimal(72)
        elif unit == UnitType.PC:
            return Decimal(96) / Decimal(6)
        elif unit == UnitType.GRAD:
            return Decimal(0.9)
        elif unit == UnitType.RAD:
            return Decimal(180) / Decimal(math.pi)
        elif unit == UnitType.TURN:
            return Decimal(360)
        elif unit == UnitType.S:
            return Decimal(1000)
        elif unit == UnitType.KHZ:
            return Decimal(1000)
        elif unit == UnitType.DPI:
            return Decimal(1) / Decimal(96)
        elif unit == UnitType.DPCM:
            return Decimal(1) / Decimal(96) * Decimal(2.54)
        return Decimal(1)


class CSSStyleValue(object):
    """Represents the base class of all CSS values accessible via the Typed OM
    API.
    """

    def __init__(self, value=None):
        self._associated_property = None
        self._value = value
        self._css_text = None

    @property
    def associated_property(self):
        return self._associated_property

    @property
    def css_text(self):
        return self._css_text

    @property
    def value(self):
        return self._value

    @staticmethod
    def _parse_css_style_value(property_name, css_text, context=None):
        if context is None:
            from ..window import window
            context = window.document

        if not property_name.startswith('--'):
            property_name = property_name.lower()

        if css_text.lower() in css_color_keyword_set | css_wide_keyword_set:
            css_text = css_text.lower()

        css_wide_keywords = 0
        reified_values = list()
        tokens = tinycss2.parse_component_value_list(css_text,
                                                     skip_comments=True)
        if (_RE_VAR_FUNCTION.search(css_text)
                or (property_name.startswith('--')
                    and property_name not in context.registered_property_set)):
            # unregistered custom property or
            # underlying value contains a var() reference
            value = CSSStyleValue._reify_component_values(tokens)
            reified_values.append(value)
        else:
            # registered custom property or
            # single property in CSS
            desc = css_property_descriptor_map.get(property_name)
            if desc is None:
                desc = PropertyDescriptor(
                    name=property_name,
                    syntax=PropertySyntax.ANY,
                    inherits=False)

            values = list()
            tokens = [token for token in tokens if token.type != 'whitespace']
            if property_name in single_multi_valued_properties:
                # single multi-valued properties
                syntax_set = list()
                for token in tokens:
                    if token.type == 'literal' and token.value == ',':
                        continue
                    text = tinycss2.serialize([token]).replace('/**/', '')
                    if text.lower() in css_wide_keyword_set:
                        css_wide_keywords += 1
                    supported, syntax = desc.support(token)
                    if not supported:
                        raise ValueError('Failed to parse as {}: {}'.format(
                            repr(property_name), repr(text)))
                    syntax_set.append(syntax)

                if len(syntax_set) == 1:
                    syntax = syntax_set[0]
                else:
                    syntax = None
                values.append([(css_text, syntax)])
            else:
                # single-valued or list-valued properties
                components = list()
                for token in tokens:
                    if token.type == 'literal' and token.value == ',':
                        values.append(components)
                        components = list()
                        continue
                    text = tinycss2.serialize([token]).replace('/**/', '')
                    if text.lower() in css_wide_keyword_set:
                        css_wide_keywords += 1
                    supported, syntax = desc.support(token)
                    if not supported:
                        raise ValueError('Failed to parse as {}: {}'.format(
                            repr(property_name), repr(text)))
                    if (syntax in (PropertySyntax.LENGTH,
                                   PropertySyntax.LENGTH_PERCENTAGE)
                            and _RE_REAL_NUMBER.fullmatch(text)):
                        # unit-less <dimension>
                        text += 'px'
                    components.append((text, syntax))

                if len(components) > 0:
                    values.append(components)

            for components in values:
                value = CSSStyleValue._reify_css_style_value(property_name,
                                                             components)
                reified_values.append(value)

        if css_wide_keywords > 0 and len(tokens) > 1:
            raise ValueError('Failed to parse as {}: {}'.format(
                repr(property_name), repr(css_text)))

        for value in reified_values:
            value._associated_property = property_name

        if len(reified_values) == 1:
            reified_values[0]._css_text = css_text

        return reified_values

    @staticmethod
    def _reify_component_values(tokens):
        members = list()
        single_string = ''
        for token in tokens:
            if token.type == 'function':
                if token.lower_name == 'var':
                    if len(single_string) > 0:
                        members.append(single_string)
                        single_string = ''
                    variable = ''
                    args = list(token.arguments)
                    while len(args) > 0:
                        arg = args.pop(0)
                        if arg.type == 'literal' and arg.value == ',':
                            break
                        variable += tinycss2.serialize([arg])
                    variable = variable.strip()
                    if len(args) == 0:
                        fallback = None
                    else:
                        fallback = CSSStyleValue._reify_component_values(args)
                    unparsed_value = CSSVariableReferenceValue(variable,
                                                               fallback)
                    members.append(unparsed_value)
                else:
                    single_string += token.name + '('
                    unparsed_value = CSSStyleValue._reify_component_values(
                        token.arguments)
                    if (len(unparsed_value) > 0
                            and isinstance(unparsed_value[0], str)):
                        single_string += unparsed_value.pop(0)
                    members.append(single_string)
                    single_string = ''
                    if (len(unparsed_value) > 0
                            and isinstance(unparsed_value[-1], str)):
                        single_string = unparsed_value.pop(-1)
                    members.extend(unparsed_value)
                    single_string += ')'
            else:
                single_string += tinycss2.serialize([token])

        if len(single_string) > 0:
            members.append(single_string)
        unparsed_value = CSSUnparsedValue(members)
        return unparsed_value

    @staticmethod
    def _reify_css_style_value(property_name, components):
        css_text = ' '.join([text for text, _ in components])
        if css_text.lower() in css_color_keyword_set | css_wide_keyword_set:
            css_text = css_text.lower()

        if css_text in css_wide_keyword_set:
            # CSS-wide keywords
            return CSSKeywordValue(css_text)
        elif property_name in (
                'alignment-baseline', 'all', 'animation-composition',
                'appearance', 'backface-visibility',
                'background-attachment', 'background-blend-mode',
                'background-clip', 'background-image-transform',
                'block-step-align', 'block-step-insert',
                'block-step-round', 'bookmark-state', 'border-boundary',
                'border-collapse', 'border-image-transform',
                'border-top-style', 'box-decoration-break', 'box-sizing',
                'caret-shape', 'clear', 'color-adjust',
                'color-interpolation', 'color-rendering', 'column-gap',
                'column-span', 'contain', 'content', 'continue',
                'copy-into', 'counter-increment', 'counter-reset',
                'counter-set', 'cue', 'cue-after', 'cue-before', 'cursor',
                'd', 'direction', 'display',
                'dominant-baseline', 'elevation', 'empty-cells', 'fill',
                'fill-break', 'fill-color', 'fill-image',
                'fill-origin', 'fill-position', 'fill-repeat',
                'fill-rule', 'fill-size', 'filter-margin-top',
                'filter-margin-right', 'filter-margin-bottom',
                'filter-margin-left', 'flex', 'flex-basis',
                'flex-direction', 'flex-flow', 'flex-grow', 'flex-shrink',
                'flex-wrap', 'float', 'font-optical-sizing',
                'font-presentation', 'font-style', 'list-style-position',
                'outline-offset', 'outline-style', 'overflow-anchor',
                'overflow-x', 'overflow-y', 'page', 'page-break-after',
                'page-break-before', 'page-break-inside', 'paint-order',
                'pause', 'pause-after', 'pause-before', 'perspective',
                'perspective-origin', 'pitch', 'pitch-range',
                'place-content', 'place-items', 'place-self',
                'play-during', 'pointer-events', 'position',
                'presentation-level', 'quotes', 'region-fragment',
                'resize', 'rotate', 'row-gap', 'ruby-align', 'ruby-merge',
                'ruby-position', 'scale', 'scroll-behavior',
                'scroll-margin', 'scroll-margin-block',
                'scroll-margin-block-end', 'scroll-margin-block-start',
                'scroll-margin-bottom', 'scroll-margin-inline',
                'scroll-margin-inline-end', 'scroll-margin-inline-start',
                'scroll-margin-left', 'scroll-margin-right',
                'scroll-margin-top', 'scroll-padding',
                'scroll-padding-block', 'scroll-padding-block-end',
                'scroll-padding-block-start', 'scroll-padding-bottom',
                'scroll-padding-inline', 'scroll-padding-inline-end',
                'scroll-padding-inline-start', 'scroll-padding-left',
                'scroll-padding-right', 'scroll-padding-top',
                'scroll-snap-align', 'scroll-snap-stop',
                'scroll-snap-type', 'scrollbar-3dlight-color',
                'scrollbar-arrow-color', 'scrollbar-base-color',
                'scrollbar-darkshadow-color', 'scrollbar-face-color',
                'scrollbar-gutter', 'scrollbar-highlight-color',
                'scrollbar-shadow-color', 'scrollbar-track-color',
                'shape-inside', 'shape-rendering', 'shape-subtract', 'size',
                'solid-color', 'solid-opacity', 'speak', 'speak-as',
                'speak-header', 'speak-numeral', 'speak-punctuation',
                'speech-rate', 'stop-color', 'stress',
                'stroke', 'stroke-align', 'stroke-break', 'stroke-color',
                'stroke-dash-corner', 'stroke-dash-justify',
                'stroke-dasharray', 'stroke-image',
                'stroke-linecap', 'stroke-linejoin',
                'stroke-origin', 'stroke-position',
                'stroke-repeat', 'stroke-size',
                'table-layout', 'text-align', 'text-anchor',
                'text-combine-upright', 'text-decoration',
                'text-decoration-color',
                'text-decoration-fill', 'text-decoration-line',
                'text-decoration-skip',
                'text-decoration-skip-ink', 'text-decoration-stroke',
                'text-emphasis-skip',
                'text-orientation', 'text-overflow',
                'text-rendering', 'text-size-adjust', 'text-transform',
                'visibility', 'voice-balance', 'voice-duration',
                'voice-family', 'voice-pitch', 'voice-range',
                'voice-rate', 'voice-stress', 'voice-volume', 'volume',
                'white-space'):
            # excludes:
            # 'cx', 'cy', 'fill-opacity', 'flood-opacity', 'r', 'rx', 'ry',
            # 'shape-margin', 'shape-padding', 'stop-opacity',
            # 'stroke-dashoffset', 'stroke-miterlimit', 'stroke-opacity',
            # 'stroke-width', 'text-decoration-width', 'text-indent'
            # includes:
            # 'text-decoration-color', 'text-decoration-line'
            return CSSKeywordValue(css_text)
        elif property_name in (
                'background', 'background-color', 'block-step',
                'bookmark-label', 'border', 'border-block',
                'border-block-color', 'border-block-end',
                'border-block-start', 'border-block-style',
                'border-block-width', 'border-bottom',
                'border-color', 'border-inline', 'border-inline-color',
                'border-inline-end', 'border-inline-end-color',
                'border-inline-end-style', 'border-inline-end-width',
                'border-inline-start', 'border-inline-start-color',
                'border-inline-start-style', 'border-inline-start-width',
                'border-inline-style', 'border-inline-width',
                'border-left', 'border-radius', 'border-right',
                'border-spacing', 'border-style', 'border-top',
                'border-width', 'float-defer', 'font', 'font-family',
                'font-variant', 'list-style-type', 'margin',
                'outline-width', 'overflow', 'overflow-x', 'overflow-y',
                'padding'):
            return CSSStyleValue(css_text)

        syntax_set = set([syntax for _, syntax in components])
        if len(syntax_set) != 1:
            if property_name in ('text-indent', 'vertical-align'):
                return CSSKeywordValue(css_text)
            return CSSStyleValue(css_text)

        syntax = list(syntax_set)[0]
        if syntax is None and property_name in ('height', 'width'):
            return CSSKeywordValue(css_text)
        elif syntax in (None, PropertySyntax.COLOR):
            # <color> or unknown
            return CSSStyleValue(css_text)
        elif syntax == PropertySyntax.CUSTOM_IDENT:
            # <custom-ident>
            return CSSKeywordValue(css_text)
        elif syntax == PropertySyntax.IMAGE:
            # <image>
            return CSSImageValue(css_text)
        elif syntax in (PropertySyntax.LENGTH, PropertySyntax.NUMBER,
                        PropertySyntax.PERCENTAGE,
                        PropertySyntax.LENGTH_PERCENTAGE,
                        PropertySyntax.INTEGER, PropertySyntax.ANGLE,
                        PropertySyntax.TIME, PropertySyntax.RESOLUTION):
            # numeric value or math functions
            return CSSNumericValue.parse(css_text)
        elif syntax == PropertySyntax.URL:
            # <url>
            return CSSURLImageValue(css_text)
        else:
            raise ValueError('Invalid syntax for property {}: {}'.format(
                repr(property_name), repr(css_text)))

    @staticmethod
    def parse(property_name, css_text, context=None):
        """Parses a CSS value.

        Arguments:
            property_name (str): The property name.
            css_text (str): The property's value to be parsed.
            context (Document, optional):
        Returns:
            CSSStyleValue:
        """
        values = CSSStyleValue._parse_css_style_value(property_name,
                                                      css_text,
                                                      context)
        return values[0] if len(values) > 0 else None

    @staticmethod
    def parse_all(property_name, css_text, context=None):
        """Parses a CSS value.

        Arguments:
            property_name (str): The property name.
            css_text (str): The property's value to be parsed.
            context (Document, optional):
        Returns:
            list[CSSStyleValue]: A list of CSS style value objects.
        """
        values = CSSStyleValue._parse_css_style_value(property_name,
                                                      css_text,
                                                      context)
        return values

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        return self._value if self._value is not None else ''


class CSSImageValue(CSSStyleValue):
    """Represents the [css-typed-om] CSSImageValue."""
    pass


class CSSKeywordValue(CSSStyleValue):
    """Represents the CSS keywords and other identifiers."""

    def __init__(self, value):
        """Constructs a CSSKeywordValue object.

        Arguments:
            value (str): The CSS keywords and other identifiers.
        """
        super().__init__()
        self.value = value

    @CSSStyleValue.value.setter
    def value(self, value):
        if value is None or len(value) == 0:
            raise ValueError('Expected non-empty string')
        self._value = value


class _MathExpression(object):

    def __init__(self, parent, operator, values):
        self._parent = parent
        self._operator = operator
        self._values = list(values)

    def __repr__(self):
        return repr({
            'operator': self._operator,
            'values': self._values
        })

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, operator):
        self._operator = operator

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def values(self):
        return self._values


class CSSNumericValue(CSSStyleValue):
    """Represents the base class of all numeric CSS values."""

    def __init__(self):
        super().__init__()

    @staticmethod
    def _parse_math_expression(css_text, token, root_node=None):
        function_name = token.lower_name
        if function_name == 'calc':
            operator = None
        elif function_name == 'clamp':
            operator = CSSMathOperator.CLAMP
        elif function_name == 'max':
            operator = CSSMathOperator.MAX
        elif function_name == 'min':
            operator = CSSMathOperator.MIN
        else:
            raise ValueError('Invalid math expression: ' + repr(token))

        args = [arg for arg in token.arguments if arg.type != 'whitespace']
        if len(args) == 0:
            raise ValueError('Invalid math expression: ' + repr(css_text))
        current_node = _MathExpression(root_node, operator, [])
        while len(args) > 0:
            arg = args.pop(0)
            operator = current_node.operator
            if arg.type == 'literal':
                literal = arg.value
                if (literal == ',' and operator in (CSSMathOperator.CLAMP,
                                                    CSSMathOperator.MAX,
                                                    CSSMathOperator.MIN)):
                    continue
                elif literal == '*':
                    if operator is None:
                        current_node.operator = CSSMathOperator.PRODUCT
                    elif operator != CSSMathOperator.PRODUCT:
                        previous_node = current_node
                        previous_value = previous_node.values.pop(-1)
                        current_node = _MathExpression(
                            previous_node,
                            CSSMathOperator.PRODUCT,
                            [previous_value])
                        previous_node.values.append(current_node)
                elif literal == '+':
                    if operator is None:
                        current_node.operator = CSSMathOperator.SUM
                    elif operator != CSSMathOperator.SUM:
                        while True:
                            parent_node = current_node.parent
                            if parent_node is None:
                                break
                            current_node = parent_node
                        previous_node = current_node
                        current_node = _MathExpression(
                            previous_node.parent,
                            CSSMathOperator.SUM,
                            [previous_node])
                        previous_node.parent = current_node
                elif literal == '/':
                    if len(args) == 0:
                        raise ValueError('Invalid math expression: '
                                         + repr(css_text))
                    next_token = args.pop(0)
                    next_value = CSSNumericValue._parse_numeric_value(
                        css_text, next_token, root_node=current_node)
                    next_node = _MathExpression(
                        current_node,
                        CSSMathOperator.INVERT,
                        [next_value])
                    if operator == CSSMathOperator.PRODUCT:
                        current_node.values.append(next_node)
                    else:
                        if len(current_node.values) == 1:
                            current_node.operator = CSSMathOperator.PRODUCT
                            current_node.values.append(next_node)
                        else:
                            previous_value = current_node.values.pop(-1)
                            node = _MathExpression(
                                current_node,
                                CSSMathOperator.PRODUCT,
                                [previous_value, next_node])
                            current_node.values.append(node)
                elif literal == '-':
                    # TODO: fix process of a "negate" node.
                    if len(args) == 0:
                        raise ValueError('Invalid math expression: '
                                         + repr(css_text))
                    next_token = args.pop(0)
                    next_value = CSSNumericValue._parse_numeric_value(
                        css_text, next_token, root_node=current_node)
                    next_node = _MathExpression(
                        current_node,
                        CSSMathOperator.NEGATE,
                        [next_value])
                    if operator == CSSMathOperator.SUM:
                        current_node.values.append(next_node)
                    else:
                        if len(current_node.values) == 1:
                            current_node.operator = CSSMathOperator.SUM
                            current_node.values.append(next_node)
                        else:
                            parent_node = current_node.parent
                            if parent_node is None:
                                parent_node = _MathExpression(
                                    None,
                                    CSSMathOperator.SUM,
                                    [current_node, next_node])
                                current_node.parent = parent_node
                                next_node.parent = parent_node
                                current_node = parent_node
                            else:
                                previous_value = parent_node.values.pop(-1)
                                node = _MathExpression(
                                    current_node,
                                    CSSMathOperator.SUM,
                                    [previous_value, next_node])
                                parent_node.values.append(node)
                else:
                    raise ValueError('Invalid math expression: ' + repr(arg))
            else:
                node = CSSNumericValue._parse_numeric_value(
                    css_text,
                    arg,
                    root_node=current_node)
                current_node.values.append(node)

        while True:
            parent_node = current_node.parent
            if (parent_node is None
                    or (root_node is not None
                        and parent_node is not None
                        and parent_node == root_node)):
                break
            current_node = parent_node
        return current_node

    @staticmethod
    def _parse_numeric_value(css_text, token, root_node=None):
        if token.type == 'number':
            # <number-token>
            return CSSUnitValue(token.value, UnitType.NUMBER)
        elif token.type == 'percentage':
            # <percentage-token>
            return CSSUnitValue(token.value, UnitType.PERCENT)
        elif token.type == 'dimension':
            # <dimension-token>
            return CSSUnitValue(token.value, token.unit)
        elif token.type == 'function':
            # 'math function'
            return CSSNumericValue._parse_math_expression(
                css_text,
                token,
                root_node=root_node)
        raise ValueError('Invalid math expression: ' + repr(token))

    @staticmethod
    def _reify_math_expression(node):
        if isinstance(node, CSSNumericValue):
            return node
        assert isinstance(node, _MathExpression)
        operator = node.operator
        if operator is None or operator == CSSMathOperator.SUM:
            expression = CSSMathSum
        elif operator == CSSMathOperator.CLAMP:
            expression = CSSMathClamp
        elif operator == CSSMathOperator.INVERT:
            expression = CSSMathInvert
        elif operator == CSSMathOperator.MAX:
            expression = CSSMathMax
        elif operator == CSSMathOperator.MIN:
            expression = CSSMathMin
        elif operator == CSSMathOperator.NEGATE:
            expression = CSSMathNegate
        elif operator == CSSMathOperator.PRODUCT:
            expression = CSSMathProduct
        else:
            raise ValueError('Invalid math expression: ' + repr(operator))
        args = list()
        for arg in node.values:
            args.append(CSSNumericValue._reify_math_expression(arg))
        return expression(*args)

    def add(self, *values):
        values = CSSNumericValue.rectify_values(values)
        if isinstance(self, CSSMathSum):
            values = self.values + values
        else:
            values = [self] + values
        if all(isinstance(item, CSSUnitValue) for item in values):
            unit = values[0].unit
            if all(unit == item.unit for item in values[1:]):
                sum_value = sum([item.value for item in values])
                return CSSUnitValue(sum_value, unit)
        return CSSMathSum(*values)

    @abstractmethod
    def create_sum_value(self):
        raise NotImplementedError

    def div(self, *values):
        # TODO: implement CSSNumericValue.div().
        pass

    def equals(self, *values):
        values = CSSNumericValue.rectify_values(values)
        for item in values:
            if (isinstance(self, CSSUnitValue)
                    and isinstance(item, CSSUnitValue)):
                if self.unit != item.unit or self.value != item.value:
                    return False
            elif ((isinstance(self, CSSMathSum)
                   and isinstance(item, CSSMathSum))
                  or (isinstance(self, CSSMathProduct)
                      and isinstance(item, CSSMathProduct))
                  or (isinstance(self, CSSMathMin)
                      and isinstance(item, CSSMathMin))
                  or (isinstance(self, CSSMathMax)
                      and isinstance(item, CSSMathMax))):
                if len(self.values) != len(item.values):
                    return False
                for value1, value2 in zip(self.values, item.values):
                    if not value1.equals(value2):
                        return False
            else:
                return False
        return True

    def max(self, *values):
        # TODO: implement CSSNumericValue.max().
        pass

    def min(self, *values):
        # TODO: implement CSSNumericValue.min().
        pass

    def mul(self, *values):
        # TODO: implement CSSNumericValue.mul().
        pass

    def negate(self):
        # TODO: implement CSSNumericValue.negate().
        pass

    @staticmethod
    def parse(css_text, unused=None, unused2=None):
        """Parses a string `css_text` into a CSSNumericValue object, and
        returns it.

        Arguments:
            css_text (str): A string to be parsed.
            unused (optional): Reserved.
            unused2 (optional): Reserved.
        Returns:
            CSSNumericValue: A CSSNumericValue object.
        """
        token = tinycss2.parse_one_component_value(css_text,
                                                   skip_comments=True)
        node = CSSNumericValue._parse_numeric_value(css_text, token)
        value = CSSNumericValue._reify_math_expression(node)
        value._css_text = css_text
        return value

    @staticmethod
    def rectify_values(values):
        rectified = list()
        for item in values:
            if isinstance(item, (int, float)):
                rectified.append(CSSUnitValue(item, UnitType.NUMBER))
            elif isinstance(item, CSSNumericValue):
                rectified.append(item)
            else:
                raise TypeError('Expected int, float or CSSNumericValue, got '
                                + repr(type(item)))
        return rectified

    def sub(self, *values):
        # TODO: implement CSSNumericValue.sub().
        pass

    def to(self, unit):
        _ = CSSNumericType.create_type(unit)
        sum_value = self.create_sum_value()
        if sum_value is None or len(sum_value) != 1:
            raise ValueError('Cannot convert to ' + repr(unit))
        value, unit_map = sum_value[0]
        units = [unit for unit, power in unit_map.items() if power != 0]
        unit_map_length = len(units)
        if unit_map_length == 0:
            item = CSSUnitValue(value, UnitType.NUMBER)
        elif unit_map_length > 1:
            raise ValueError('Incompatible types')
        else:
            item = CSSUnitValue(value, units[0])
        if item.unit == unit.lower():
            return item
        return item.to(unit)

    def to_sum(self, *units):
        for unit in units:
            _ = CSSNumericType.create_type(unit)
        sum_value = self.create_sum_value()
        values = list()
        for item in sum_value:
            values.append(CSSUnitValue.create_from_sum_value_item(item))
        if len(units) == 0:
            values = sorted(values, key=lambda x: x.unit)
            return CSSMathSum(*values)
        result = list()
        for unit in units:
            temp = CSSUnitValue(0, unit)
            for value in list(values):
                canonical_unit1 = UnitType.get_canonical_unit(value.unit)
                canonical_unit2 = UnitType.get_canonical_unit(unit)
                if (value.unit == unit
                        or (canonical_unit1 is not None
                            and canonical_unit2 is not None
                            and canonical_unit1 == canonical_unit2)):
                    temp.value += value.to(unit).value
                    values.remove(value)
                    break
            result.append(temp)
        if len(values) > 0:
            raise ValueError('Cannot convert to '
                             + repr([x.unit for x in values]))
        return CSSMathSum(*result)

    @abstractmethod
    def type(self):
        raise NotImplementedError


class CSSMathValue(CSSNumericValue):
    """Represents the [css-typed-om] CSSMathValue."""

    @property
    @abstractmethod
    def operator(self):
        raise NotImplementedError


class CSSMathClamp(CSSMathValue):
    """Represents the [css-typed-om] CSSMathClamp."""

    def __init__(self, min_, val, max_):
        super().__init__()
        self._min = CSSNumericValue.rectify_values([min_])[0]
        self._val = CSSNumericValue.rectify_values([val])[0]
        self._max = CSSNumericValue.rectify_values([max_])[0]
        type1 = self._min.type()
        for item in [self._val, self._max]:
            type2 = item.type()
            type1 = CSSNumericType.add_types(type1, type2)
            if type1 is None:
                raise ValueError('Incompatible types')
        self._type = type1

    @property
    def max(self):
        return self._max

    @property
    def min(self):
        return self._min

    @property
    def operator(self):
        return CSSMathOperator.CLAMP

    @property
    def val(self):
        return self._val

    def create_sum_value(self):
        return None

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        args = list()
        args.append(self._min.tostring(**kwargs))
        args.append(self._val.tostring(**kwargs))
        args.append(self._max.tostring(**kwargs))
        s = 'clamp({})'.format(', '.join(args))
        return s

    def type(self):
        return self._type


class CSSMathInvert(CSSMathValue):
    """Represents the [css-typed-om] CSSMathInvert."""

    def __init__(self, arg):
        super().__init__()
        values = CSSNumericValue.rectify_values([arg])
        self._value = values[0]
        self._type = self._value.type()
        for key in list(self._type):
            self._type[key] *= -1

    @property
    def operator(self):
        return CSSMathOperator.INVERT

    def create_sum_value(self):
        values = self._value.create_sum_value()
        if values is None or len(values) > 1:
            return None
        for i in range(len(values)):
            value, unit_map = values[i]
            if value != 0:
                value = 1 / value
            for key in list(unit_map):
                unit_map[key] *= -1
            values[i] = value, unit_map
        return values

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        nested = kwargs.get('nested', False)
        paren_less = kwargs.get('paren_less', False)
        if not paren_less:
            s = '(' if nested else 'calc('
        else:
            s = ''
        s += '1 / ' + self._value.tostring(**kwargs)
        if not paren_less:
            s += ')'
        return s

    def type(self):
        return self._type


class CSSMathMax(CSSMathValue):
    """Represents the [css-typed-om] CSSMathMax."""

    def __init__(self, *args):
        super().__init__()
        if len(args) == 0:
            raise ValueError('Expected one or more arguments')
        self._values = CSSNumericValue.rectify_values(args)
        type1 = self._values[0].type()
        for item in self._values[1:]:
            type2 = item.type()
            type1 = CSSNumericType.add_types(type1, type2)
            if type1 is None:
                raise ValueError('Incompatible types')
        self._type = type1

    @property
    def operator(self):
        return CSSMathOperator.MAX

    @property
    def values(self):
        return self._values

    def create_sum_value(self):
        args = list()
        for item in self._values:
            new_values = item.create_sum_value()
            if new_values is None or len(new_values) > 1:
                return None
            args.append(new_values[0])
        value1, unit_map1 = args[0]
        values = list([value1])
        for value2, unit_map2 in args[1:]:
            if unit_map1 != unit_map2:
                return None
            values.append(value2)
        return [(max(values), unit_map1)]

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        kwargs['nested'] = True
        kwargs['paren_less'] = True
        args = list()
        for arg in self._values:
            args.append(arg.tostring(**kwargs))
        s = 'max({})'.format(', '.join(args))
        return s

    def type(self):
        return self._type


class CSSMathMin(CSSMathValue):
    """Represents the [css-typed-om] CSSMathMin."""

    def __init__(self, *args):
        super().__init__()
        if len(args) == 0:
            raise ValueError('Expected one or more arguments')
        self._values = CSSNumericValue.rectify_values(args)
        type1 = self._values[0].type()
        for item in self._values[1:]:
            type2 = item.type()
            type1 = CSSNumericType.add_types(type1, type2)
            if type1 is None:
                raise ValueError('Incompatible types')
        self._type = type1

    @property
    def operator(self):
        return CSSMathOperator.MIN

    @property
    def values(self):
        return self._values

    def create_sum_value(self):
        args = list()
        for item in self._values:
            new_values = item.create_sum_value()
            if new_values is None or len(new_values) > 1:
                return None
            args.append(new_values[0])
        value1, unit_map1 = args[0]
        values = list([value1])
        for value2, unit_map2 in args[1:]:
            if unit_map1 != unit_map2:
                return None
            values.append(value2)
        return [(min(values), unit_map1)]

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        kwargs['nested'] = True
        kwargs['paren_less'] = True
        args = list()
        for arg in self._values:
            args.append(arg.tostring(**kwargs))
        s = 'min({})'.format(', '.join(args))
        return s

    def type(self):
        return self._type


class CSSMathNegate(CSSMathValue):
    """Represents the [css-typed-om] CSSMathNegate."""

    def __init__(self, arg):
        super().__init__()
        values = CSSNumericValue.rectify_values([arg])
        self._value = values[0]
        self._type = self._value.type()

    @property
    def operator(self):
        return CSSMathOperator.NEGATE

    def create_sum_value(self):
        values = self._value.create_sum_value()
        if values is None:
            return None
        for i in range(len(values)):
            value, unit_map = values[i]
            values[i] = -value, unit_map
        return values

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        nested = kwargs.get('nested', False)
        paren_less = kwargs.get('paren_less', False)
        if not paren_less:
            s = '(' if nested else 'calc('
        else:
            s = ''
        s += '-'
        s += self._value.tostring(**kwargs)
        if not paren_less:
            s += ')'
        return s

    def type(self):
        return self._type


class CSSMathProduct(CSSMathValue):
    """Represents the [css-typed-om] CSSMathProduct."""

    def __init__(self, *args):
        super().__init__()
        if len(args) == 0:
            raise ValueError('Expected one or more arguments')
        self._values = CSSNumericValue.rectify_values(args)
        type1 = self._values[0].type()
        for item in self._values[1:]:
            type2 = item.type()
            type1 = CSSNumericType.multiply_types(type1, type2)
            if type1 is None:
                raise ValueError('Incompatible types')
        self._type = type1

    @property
    def operator(self):
        return CSSMathOperator.PRODUCT

    @property
    def values(self):
        return self._values

    def create_sum_value(self):
        values = list([(1, {})])
        for item in self._values:
            new_values = item.create_sum_value()
            if new_values is None:
                return None
            temp = list()
            for value1, unit_map1 in values:
                for value2, unit_map2 in new_values:
                    unit_map = CSSNumericType.product_unit_maps(
                        unit_map1, unit_map2)
                    for key in list(unit_map):
                        if unit_map[key] == 0:
                            del unit_map[key]
                    temp.append((value1 * value2, unit_map))
            values = temp
        return values

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        nested = kwargs.get('nested', False)
        paren_less = kwargs.get('paren_less', False)
        if not paren_less:
            s = '(' if nested else 'calc('
        else:
            s = ''
        kwargs2 = kwargs.copy()
        kwargs2['nested'] = True
        s += self._values[0].tostring(**kwargs2)
        for arg in self._values[1:]:
            if isinstance(arg, CSSMathInvert):
                s += ' / '
                arg = arg.value
            else:
                s += ' * '
            s += arg.tostring(**kwargs2)
        if not paren_less:
            s += ')'
        return s

    def type(self):
        return self._type


class CSSMathSum(CSSMathValue):
    """Represents the [css-typed-om] CSSMathSum."""

    def __init__(self, *args):
        super().__init__()
        if len(args) == 0:
            raise ValueError('Expected one or more arguments')
        self._values = CSSNumericValue.rectify_values(args)
        type1 = self._values[0].type()
        for item in self._values[1:]:
            type2 = item.type()
            type1 = CSSNumericType.add_types(type1, type2)
            if type1 is None:
                raise ValueError('Incompatible types')
        self._type = type1

    @property
    def operator(self):
        return CSSMathOperator.SUM

    @property
    def values(self):
        return self._values

    def create_sum_value(self):
        values = list()
        for item in self._values:
            value = item.create_sum_value()
            if value is None:
                return None
            for sub_value, sub_unit_map in value:
                sub_unit_map_keys = sorted(sub_unit_map.keys())
                found = [i for i, (value, unit_map) in enumerate(values)
                         if sorted(unit_map.keys()) == sub_unit_map_keys]
                if len(found) == 0:
                    values.append([sub_value, sub_unit_map])
                else:
                    index = found[0]
                    values[index][0] += sub_value

        _, unit_map = values[0]
        type1 = CSSNumericType.create_type_from_unit_map(unit_map)
        if type1 is None:
            return None
        for _, unit_map in values[1:]:
            type2 = CSSNumericType.create_type_from_unit_map(unit_map)
            if type2 is None:
                return None
            type1 = CSSNumericType.multiply_types(type1, type2)
            if type1 is None:
                return None
        return [(value, unit_map) for value, unit_map in values]

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        nested = kwargs.get('nested', False)
        paren_less = kwargs.get('paren_less', False)
        if not paren_less:
            s = '(' if nested else 'calc('
        else:
            s = ''
        kwargs2 = kwargs.copy()
        kwargs2['nested'] = True
        s += self._values[0].tostring(**kwargs2)
        for arg in self._values[1:]:
            if isinstance(arg, CSSMathNegate):
                s += ' - '
                arg = arg.value
            else:
                s += ' + '
            s += arg.tostring(**kwargs2)
        if not paren_less:
            s += ')'
        return s

    def type(self):
        return self._type


class CSSUnitValue(CSSNumericValue):
    """Represents the numeric values."""

    rel_tol = 1e-09
    abs_tol = 0.0

    def __init__(self, value, unit):
        """Constructs a CSSUnitValue object.

        Arguments:
            value (float): The value.
            unit (str): The unit string.
        """
        super().__init__()
        self._unit = unit.lower()
        self._type = CSSNumericType.create_type(self._unit)
        self._value = Decimal(value)

    def __eq__(self, other):
        other = self.normalize(other)
        if other is None:
            return NotImplemented
        return math.isclose(self._value,
                            other._value,
                            rel_tol=CSSUnitValue.rel_tol,
                            abs_tol=CSSUnitValue.abs_tol)

    def __ge__(self, other):
        other = self.normalize(other)
        if other is None:
            return NotImplemented
        if math.isclose(self._value,
                        other._value,
                        rel_tol=CSSUnitValue.rel_tol,
                        abs_tol=CSSUnitValue.abs_tol):
            return True
        return self._value >= other._value

    def __gt__(self, other):
        other = self.normalize(other)
        if other is None:
            return NotImplemented
        if math.isclose(self._value,
                        other._value,
                        rel_tol=CSSUnitValue.rel_tol,
                        abs_tol=CSSUnitValue.abs_tol):
            return False
        return self._value > other._value

    def __le__(self, other):
        other = self.normalize(other)
        if other is None:
            return NotImplemented
        if math.isclose(self._value,
                        other._value,
                        rel_tol=CSSUnitValue.rel_tol,
                        abs_tol=CSSUnitValue.abs_tol):
            return True
        return self._value <= other._value

    def __lt__(self, other):
        other = self.normalize(other)
        if other is None:
            return NotImplemented
        if math.isclose(self._value,
                        other._value,
                        rel_tol=CSSUnitValue.rel_tol,
                        abs_tol=CSSUnitValue.abs_tol):
            return False
        return self._value < other._value

    def __repr__(self):
        return repr({
            'value': self.value,
            'unit': self.unit,
        })

    @property
    def unit(self):
        """str: The unit string."""
        return self._unit

    @property
    def value(self):
        """float: The value."""
        return float(self._value)

    @value.setter
    def value(self, value):
        self._value = Decimal(value)

    @staticmethod
    def create_from_sum_value_item(item):
        value, unit_map = item
        unit_map_length = len(unit_map)
        if unit_map_length == 0:
            return CSSUnitValue(value, UnitType.NUMBER)
        units = [unit for unit, power in unit_map.items() if power == 1]
        if unit_map_length > 1 or len(units) != 1:
            raise ValueError('Cannot convert to CSSUnitValue')
        return CSSUnitValue(value, units[0])

    def create_sum_value(self):
        unit = self._unit
        value = self._value
        canonical_unit = UnitType.get_canonical_unit(unit)
        if canonical_unit is not None and canonical_unit != unit:
            conversion_ratio = UnitType.get_conversion_ratio(unit)
            unit = canonical_unit
            value *= conversion_ratio
        unit_map = dict()
        if unit != UnitType.NUMBER:
            unit_map[unit] = 1
        return [(value, unit_map)]

    def normalize(self, value):
        if isinstance(value, (int, float)):
            value = CSSUnitValue(value, UnitType.NUMBER)
        if not isinstance(value, CSSUnitValue):
            return None
        if self._unit != value._unit:
            value = value.to(self._unit)
        return value

    def to(self, unit):
        unit = unit.lower()
        old_unit = self._unit
        old_value = self._value
        if old_unit == unit:
            return CSSUnitValue(old_value, old_unit)
        canonical_unit1 = UnitType.get_canonical_unit(old_unit)
        canonical_unit2 = UnitType.get_canonical_unit(unit)
        if (canonical_unit1 is None
                or canonical_unit2 is None
                or canonical_unit1 != canonical_unit2):
            raise ValueError('Cannot convert to ' + repr(unit))
        conversion_ratio = (UnitType.get_conversion_ratio(old_unit)
                            / UnitType.get_conversion_ratio(unit))
        return CSSUnitValue(old_value * conversion_ratio, unit)

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        s = format_number_sequence([self._value])[0]
        if self._unit == UnitType.NUMBER:
            return s
        elif self._unit == UnitType.PERCENT:
            return s + '%'
        return s + self._unit

    def type(self):
        return self._type


class CSSUnparsedValue(CSSStyleValue, MutableSequence, Iterable):
    """Represents the property values that reference custom properties."""

    def __init__(self, members=None):
        """Constructs a CSSUnparsedValue object.

        Arguments:
            members (list[str, CSSVariableReferenceValue], optional):
                A list of string or CSSVariableReferenceValue objects.
        """
        super().__init__()
        self._tokens = list()
        if members is not None:
            self.extend(members)

    def __delitem__(self, index):
        del self._tokens[index]

    def __getitem__(self, index):
        return self._tokens[index]

    def __iter__(self):
        return iter(self._tokens)

    def __len__(self):
        return len(self._tokens)

    def __setitem__(self, index, value):
        if isinstance(index, int):
            values = [value]
        else:  # elif isinstance(index, slice):
            values = value
        for item in values:
            if not isinstance(item, (str, CSSVariableReferenceValue)):
                raise TypeError("Expected str or CSSVariableReferenceValue,"
                                " got " + repr(type(item)))

        if isinstance(index, int):
            self._tokens.insert(index, value)
        else:
            self._tokens[index] = value

    @property
    def length(self):
        """int: The number of str and CSSVariableReferenceValue objects."""
        return len(self)

    def insert(self, index, value):
        self[index] = value

    def tostring(self, **kwargs):
        if self._css_text is not None:
            return self._css_text
        s = list()
        for token in self._tokens:
            if isinstance(token, CSSVariableReferenceValue):
                token = token.tostring(**kwargs)
            print(repr(token))
            s.append(token)
        return ''.join(s)


class CSSURLImageValue(CSSImageValue):
    """Represents the [css-typed-om] CSSURLImageValue."""

    def __init__(self, value):
        super().__init__()
        matched = _RE_URL_FUNCTION.fullmatch(value)
        if matched:
            value = matched.group('value')
        if value[0] == '"' and value[-1] == '"':
            value = value.strip('"')
        self._value = value

    def tostring(self, **kwargs):
        # FIXME: add support for <url-modifier>.
        # <url> = url( <string> <url-modifier>* )
        # <url-modifier> = <ident> | <function>
        if self._css_text is not None:
            return self._css_text
        s = 'url("{}")'.format(self._value)
        return s


class CSSVariableReferenceValue(object):
    """Represents the [css-typed-om] CSSVariableReferenceValue."""

    def __init__(self, variable, fallback=None):
        """Constructs a CSSVariableReferenceValue object.

        Arguments:
            variable (str): The custom property name.
            fallback (CSSUnparsedValue, optional):
        """
        self._variable = variable
        self._fallback = fallback

    @property
    def fallback(self):
        """CSSUnparsedValue:"""
        return self._fallback

    @property
    def variable(self):
        """str: The custom property name."""
        return self._variable

    @variable.setter
    def variable(self, value):
        self._variable = value

    def tostring(self, **kwargs):
        s = 'var(' + self._variable
        if self._fallback is not None:
            s += ','
            if isinstance(self._fallback, str):
                s += self._fallback
            else:
                s += self._fallback.tostring(**kwargs)
        s += ')'
        return s


class StylePropertyMapReadOnly(Mapping):
    """Represents the [css-typed-om] StylePropertyMapReadOnly."""

    def __init__(self, declaration):
        """Constructs a StylePropertyMapReadOnly object.

        Arguments:
            declaration (CSSStyleDeclaration): A CSS declarations.
        """
        self._declarations = declaration  # type: dict

    def __getitem__(self, property_name):
        return self.get_all(property_name)

    def __iter__(self):
        return iter(self._declarations)

    def __len__(self):
        return len(self._declarations)

    def __repr__(self):
        return repr(self._declarations)

    @property
    def size(self):
        return len(self)

    def get(self, property_name):
        values = self.get_all(property_name)
        return values[0] if len(values) > 0 else None

    def get_all(self, property_name):
        if not property_name.startswith('--'):
            property_name = property_name.lower()

        props = self._declarations
        if property_name not in props:
            return []

        css_text = props[property_name]
        values = CSSStyleValue.parse_all(property_name, css_text)
        return values

    def has(self, property_name):
        if not property_name.startswith('--'):
            property_name = property_name.lower()

        props = self._declarations
        return property_name in props

    def keys(self):
        return self._declarations.keys()


class StylePropertyMap(StylePropertyMapReadOnly, MutableMapping):
    """Represents the [css-typed-om] StylePropertyMap."""

    def __delitem__(self, property_name):
        self.delete(property_name)

    def __setitem__(self, property_name, value):
        self.set(property_name, value)

    def append(self, property_name, *values):
        # TODO: implement StylePropertyMap.append().
        pass

    def delete(self, property_name):
        if not property_name.startswith('--'):
            property_name = property_name.lower()

        props = self._declarations
        if property_name in props:
            del props[property_name]

    def set(self, property_name, *values):
        if not property_name.startswith('--'):
            property_name = property_name.lower()

        var_references = 0
        for item in values:
            if isinstance(item, str):
                continue
            elif not isinstance(item, CSSStyleValue):
                raise TypeError('Expected str or CSSStyleValue, got '
                                + repr(type(item)))
            if isinstance(item, (CSSUnparsedValue,
                                 CSSVariableReferenceValue)):
                var_references += 1
            associated_property = item.associated_property
            if (associated_property is not None
                    and property_name != associated_property):
                raise ValueError('Property name did not match: '
                                 + repr((property_name, associated_property)))

        if len(values) > 1 and var_references > 0:
            raise TypeError('Invalid type for property: '
                            + repr(property_name))

        props = self._declarations
        if property_name in props:
            del props[property_name]

        values_to_set = list()
        for value in values:
            # TODO: create an underlying value.
            if isinstance(value, str):
                values_to_set.append(value)
            else:
                values_to_set.append(value.tostring())

        delimiter = ', ' if property_name in list_valued_properties else ' '
        props[property_name] = delimiter.join(values_to_set)
