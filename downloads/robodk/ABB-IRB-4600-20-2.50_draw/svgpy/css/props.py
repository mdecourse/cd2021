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

import tinycss2.color3

_RE_FUNCTION = re.compile(r'<(?P<name>(--|-|[a-z_])[a-z0-9_\-]*)\([^)]*\)>',
                          re.IGNORECASE)

_RE_HEX_COLOR = re.compile(
    r'[0-9a-f]{8}|[0-9a-f]{6}|[0-9a-f]{4}|[0-9a-f]{3}',
    re.IGNORECASE)

_RE_SYNTAX_COMBINATOR = re.compile(r' |\|{1,2}|&&|\[|\]')

_RE_SYNTAX_MULTIPLIERS = re.compile(
    r'(\*|\+|\?|#|!)?(\{[0-9]+(,([0-9]+)?)?\}|(\*|\+|\?|#|!))?$')

css_color_keyword_set = {
    'currentcolor', 'transparent',
}

css_wide_keyword_set = {
    'default', 'inherit', 'initial', 'revert', 'unset',
}


class PropertySyntax(object):
    LENGTH = '<length>'
    NUMBER = '<number>'
    PERCENTAGE = '<percentage>'
    LENGTH_PERCENTAGE = '<length-percentage>'
    COLOR = '<color>'
    IMAGE = '<image>'
    URL = '<url>'
    INTEGER = '<integer>'
    ANGLE = '<angle>'
    TIME = '<time>'
    RESOLUTION = '<resolution>'
    TRANSFORM_FUNCTION = '<transform-function>'
    CUSTOM_IDENT = '<custom-ident>'
    TRANSFORM_LIST = '<transform-list>'

    ANY = '*'
    STRING = '<string>'


class PropertyDescriptor(object):

    def __init__(self, name, inherits, syntax=PropertySyntax.ANY,
                 initial_value=None):
        self._name = name
        self._inherits = inherits
        self._syntax = syntax
        self._initial_value = initial_value
        components = (set(_RE_SYNTAX_COMBINATOR.split(syntax))
                      - {'', '*', '+', '?', '#', '!'})
        components = {x for x in components
                      if _RE_SYNTAX_MULTIPLIERS.fullmatch(x) is None}
        if syntax == PropertySyntax.ANY:
            self._syntax_components = {
                PropertySyntax.ANY: True,
            }
        else:
            self._syntax_components = {
                PropertySyntax.LENGTH: any(
                    x for x in components
                    if x.startswith(PropertySyntax.LENGTH)),
                PropertySyntax.NUMBER: any(
                    x for x in components
                    if x.startswith(PropertySyntax.NUMBER)),
                PropertySyntax.PERCENTAGE: any(
                    x for x in components
                    if x.startswith(PropertySyntax.PERCENTAGE)),
                PropertySyntax.LENGTH_PERCENTAGE: any(
                    x for x in components
                    if x.startswith(PropertySyntax.LENGTH_PERCENTAGE)),
                PropertySyntax.COLOR: any(
                    x for x in components
                    if x.startswith(PropertySyntax.COLOR)),
                PropertySyntax.IMAGE: any(
                    x for x in components
                    if x.startswith(PropertySyntax.IMAGE)),
                PropertySyntax.URL: any(
                    x for x in components
                    if x.startswith(PropertySyntax.URL)),
                PropertySyntax.INTEGER: any(
                    x for x in components
                    if x.startswith(PropertySyntax.INTEGER)),
                PropertySyntax.ANGLE: any(
                    x for x in components
                    if x.startswith(PropertySyntax.ANGLE)),
                PropertySyntax.TIME: any(
                    x for x in components
                    if x.startswith(PropertySyntax.TIME)),
                PropertySyntax.RESOLUTION: any(
                    x for x in components
                    if x.startswith(PropertySyntax.RESOLUTION)),
                PropertySyntax.TRANSFORM_FUNCTION: any(
                    x for x in components
                    if x.startswith(PropertySyntax.TRANSFORM_FUNCTION)),
                PropertySyntax.CUSTOM_IDENT: any(
                    x for x in components
                    if x.startswith(PropertySyntax.CUSTOM_IDENT)),
                PropertySyntax.TRANSFORM_LIST: any(
                    x for x in components
                    if x.startswith(PropertySyntax.TRANSFORM_LIST)),
                PropertySyntax.ANY: False,
                PropertySyntax.STRING: any(
                    x for x in components
                    if x.startswith(PropertySyntax.STRING)),
            }
        functions = list(['var'])
        components = {_RE_SYNTAX_MULTIPLIERS.sub('', x) for x in components}
        for item in components:
            matched = _RE_FUNCTION.fullmatch(item)
            if matched:
                functions.append(matched.group('name').lower())
        self._functions = set(functions)
        components = {x for x in components
                      if (x[0] != '<' and x[-1] != '>'
                          and x.lower() not in (css_color_keyword_set
                                                | css_wide_keyword_set))}
        self._identifiers = components

    @property
    def identifiers(self):
        return self._identifiers

    @property
    def inherits(self):
        return self._inherits

    @property
    def initial_value(self):
        return self._initial_value

    @property
    def name(self):
        return self._name

    @property
    def syntax(self):
        return self._syntax

    def support(self, token):
        if token.type == 'dimension':
            # <dimension-token>
            unit = token.lower_unit

            # <angle> type
            if unit in ('deg', 'grad', 'rad', 'turn'):
                if (self._syntax_components[PropertySyntax.ANY]
                        or self._syntax_components[PropertySyntax.ANGLE]):
                    return True, PropertySyntax.ANGLE

            # <time> type
            elif unit in ('s', 'ms'):
                if (self._syntax_components[PropertySyntax.ANY]
                        or self._syntax_components[PropertySyntax.TIME]):
                    return True, PropertySyntax.TIME

            # <resolution> type
            elif unit in ('dpi', 'dpcm', 'dppx'):
                if (self._syntax_components[PropertySyntax.ANY]
                        or self._syntax_components[PropertySyntax.RESOLUTION]):
                    return True, PropertySyntax.RESOLUTION

            # <length-percentage> or <length> type
            elif unit in ('em', 'ex', 'cap', 'ch', 'ic', 'rem', 'lh', 'rlh',
                          'vw', 'vh', 'vi', 'vb', 'vmin', 'vmax',
                          'cm', 'mm', 'q', 'in', 'pt', 'pc', 'px',
                          'deg', 'grad', 'rad', 'turn',
                          's', 'ms',
                          'hz', 'khz',
                          'dpi', 'dpcm', 'dppx',
                          'fr'):
                # <length> type
                if (self._syntax_components[PropertySyntax.ANY]
                        or self._syntax_components[PropertySyntax.LENGTH]):
                    return True, PropertySyntax.LENGTH

                # <length-percentage> type
                elif self._syntax_components[PropertySyntax.LENGTH_PERCENTAGE]:
                    return True, PropertySyntax.LENGTH_PERCENTAGE

            return False, None
        elif token.type == 'function':
            # <function-token>
            function_name = token.lower_name

            # <color> type
            if function_name in ('rgb', 'rgba', 'hsl', 'hsla', 'hwb', 'gray',
                                 'device-cmyk'):
                if (self._syntax_components[PropertySyntax.ANY]
                        or self._syntax_components[PropertySyntax.COLOR]):
                    return True, PropertySyntax.COLOR

            # <image> type
            elif function_name in ('cross-fade', 'image', 'image-set',
                                   'conic-gradient', 'linear-gradient',
                                   'radial-gradient',
                                   'repeating-conic-gradient',
                                   'repeating-linear-gradient',
                                   'repeating-radial-gradient'):
                if (self._syntax_components[PropertySyntax.ANY]
                        or self._syntax_components[PropertySyntax.IMAGE]):
                    return True, PropertySyntax.IMAGE

            # math functions
            elif function_name in ('calc', 'min', 'max', 'clamp'):
                if (self._syntax_components[PropertySyntax.ANY]
                        or self._syntax_components[
                            PropertySyntax.LENGTH_PERCENTAGE]):
                    return True, PropertySyntax.LENGTH_PERCENTAGE

            # <transform-function> or <transform-list> type
            elif function_name in ('matrix',
                                   'translate', 'translatex', 'translatey',
                                   'scale', 'scalex', 'scaley',
                                   'rotate',
                                   'skew', 'skewx', 'skewy'):
                if (self._syntax_components[PropertySyntax.ANY]
                        or self._syntax_components[
                            PropertySyntax.TRANSFORM_FUNCTION]):
                    return True, PropertySyntax.TRANSFORM_FUNCTION
                elif self._syntax_components[PropertySyntax.TRANSFORM_LIST]:
                    return True, PropertySyntax.TRANSFORM_LIST

            # any supported functions
            elif function_name in self._functions:
                return True, None

            return False, None
        elif token.type == 'hash':
            # <hash-token>
            value = token.value

            # <color> type (<hex-color>)
            if (self._syntax_components[PropertySyntax.ANY]
                    or self._syntax_components[PropertySyntax.COLOR]):
                if _RE_HEX_COLOR.fullmatch(value) is not None:
                    return True, PropertySyntax.COLOR

            return False, None
        elif token.type in ('ident', 'string'):
            # <ident-token> or <string-token>
            value = token.value

            # CSS-wide keywords
            if value.lower() in css_wide_keyword_set:
                return True, None

            # <custom-ident> type
            if value in self._identifiers:
                return True, PropertySyntax.CUSTOM_IDENT

            # <color> type (<named-color> or 'currentcolor')
            if (self._syntax_components[PropertySyntax.ANY]
                    or self._syntax_components[PropertySyntax.COLOR]):
                if value.lower() == 'currentcolor':
                    return True, PropertySyntax.CUSTOM_IDENT

                color = tinycss2.color3.parse_color(value)
                if color is not None:
                    return True, PropertySyntax.COLOR

            # <custom-ident> type
            if (self._syntax_components[PropertySyntax.ANY]
                    or self._syntax_components[PropertySyntax.CUSTOM_IDENT]
                    or self._syntax_components[PropertySyntax.STRING]):
                return True, PropertySyntax.CUSTOM_IDENT

            return False, None
        elif token.type == 'literal':
            if (token.value in self._identifiers
                    or self._syntax_components[PropertySyntax.ANY]
                    or self._syntax_components[PropertySyntax.CUSTOM_IDENT]):
                return True, PropertySyntax.CUSTOM_IDENT

            return False, None
        elif token.type == 'number':
            # <numeric-token>
            # <integer> type
            if (token.is_integer
                    and (self._syntax_components[PropertySyntax.ANY]
                         or self._syntax_components[PropertySyntax.INTEGER])):
                return True, PropertySyntax.INTEGER

            # <number> type
            if (self._syntax_components[PropertySyntax.ANY]
                    or self._syntax_components[PropertySyntax.NUMBER]):
                return True, PropertySyntax.NUMBER

            # unit-less <dimension>
            elif self._syntax_components[PropertySyntax.LENGTH]:
                return True, PropertySyntax.LENGTH
            elif self._syntax_components[PropertySyntax.LENGTH_PERCENTAGE]:
                return True, PropertySyntax.LENGTH_PERCENTAGE

            # <custom-ident> type
            elif (self._syntax_components[PropertySyntax.CUSTOM_IDENT]
                  or self._syntax_components[PropertySyntax.STRING]):
                return True, PropertySyntax.CUSTOM_IDENT

            return False, None
        elif token.type == 'percentage':
            # <percentage-token>
            # <percentage> type
            if (self._syntax_components[PropertySyntax.ANY]
                    or self._syntax_components[PropertySyntax.PERCENTAGE]):
                return True, PropertySyntax.PERCENTAGE

            # <length-percentage> type
            elif self._syntax_components[PropertySyntax.LENGTH_PERCENTAGE]:
                return True, PropertySyntax.LENGTH_PERCENTAGE

            return False, None
        elif token.type == 'url':
            # <url-token>
            # <url> type
            if (self._syntax_components[PropertySyntax.ANY]
                    or self._syntax_components[PropertySyntax.URL]):
                return True, PropertySyntax.URL

            # <image> type
            elif self._syntax_components[PropertySyntax.IMAGE]:
                return True, PropertySyntax.IMAGE

            return False, None
        elif token.type == 'error':
            raise ValueError('Cannot parse for property: ' + repr(token))
        raise NotImplementedError(token)

    def supports(self, css_text):
        tokens = tinycss2.parse_component_value_list(css_text,
                                                     skip_comments=True)
        tokens = [token for token in tokens if token.type != 'whitespace']
        css_wide_keywords = 0
        for token in tokens:
            if token.type == 'literal' and token.value == ',':
                if '#' in self._syntax or token.value in self._identifiers:
                    continue
                else:
                    return False
            text = tinycss2.serialize([token]).replace('/**/', '')
            if text.lower() in css_wide_keyword_set:
                css_wide_keywords += 1
                continue
            supported, _ = self.support(token)
            if not supported:
                return False

        if css_wide_keywords > 0 and len(tokens) > 1:
            return False
        return True


_property_descriptors = [
    PropertyDescriptor(
        name='alignment-baseline',  # [css-inline-3]
        syntax="baseline | text-bottom | alphabetic | ideographic | middle"
               " | central | mathematical | text-top | bottom | center | top",
        initial_value='baseline',
        inherits=False,
    ),
    PropertyDescriptor(
        name='baseline-shift',  # [css-inline-3]
        syntax='<length-percentage> | sub | super',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='clip-path',  # [css-masking-1]
        syntax="<url>"
               " | [ [ <inset()> | <circle()> | <ellipse()> | <polygon()> ]"
               " || [ [ [ border-box | padding-box | content-box ]"
               " | margin-box ] | fill-box | stroke-box | view-box ] ]"
               " | none",
        # = <clip-source> | [ <basic-shape> || <geometry-box> ] | none
        #
        # <clip-source> = <url>
        #
        # <basic-shape> = 'inset()', 'circle()', 'ellipse()' or 'polygon()'
        # // [css-shapes-2]
        #
        # <geometry-box> = <shape-box> | fill-box | stroke-box | view-box
        #
        # <shape-box> = <box> | margin-box
        # // [css-shapes-1]
        #
        # <box> = border-box | padding-box | content-box
        # // [css-backgrounds-3]
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='clip-rule',  # [css-masking-1]
        syntax='nonzero | evenodd',
        initial_value='nonzero',
        inherits=True,
    ),
    PropertyDescriptor(
        name='color',  # [css-color-4]
        syntax='<color>',
        initial_value='black',  # UA-defined
        inherits=True,
    ),
    PropertyDescriptor(
        name='color-interpolation',
        syntax='auto | sRGB | linearRGB',
        initial_value='sRGB',
        inherits=True,
    ),
    PropertyDescriptor(
        name='color-interpolation-filters',  # [filter-effects-1]
        syntax='auto | sRGB | linearRGB',
        initial_value='linearRGB',
        inherits=True,
    ),
    PropertyDescriptor(
        name='color-rendering',
        syntax='auto | optimizeSpeed | optimizeQuality',
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='cursor',  # [css-ui-4]
        syntax="[ [ <url> [ <number> <number> ]? , ]*"
               " [ auto | default | none"
               " | context-menu | help | pointer | progress | wait | cell"
               " | crosshair | text | vertical-text | alias | copy | move"
               " | no-drop | not-allowed | grab | grabbing | e-resize"
               " | n-resize | ne-resize | nw-resize | s-resize | se-resize"
               " | sw-resize | w-resize | ew-resize | ns-resize | nesw-resize"
               " | nwse-resize | col-resize | row-resize | all-scroll"
               " | zoom-in | zoom-out ] ]",
        # = [ [ <url> [ <x> <y> ]? , ]*
        #  [ auto | default | none |
        #  context-menu | help | pointer | progress | wait |
        #  cell | crosshair | text | vertical-text |
        #  alias | copy | move | no-drop | not-allowed | grab | grabbing |
        #  e-resize | n-resize | ne-resize | nw-resize | s-resize | se-resize
        #  | sw-resize | w-resize | ew-resize | ns-resize | nesw-resize
        #  | nwse-resize | col-resize | row-resize | all-scroll
        #  | zoom-in | zoom-out
        #  ] ]
        #
        # <x> = <number>
        #
        # <y> = <number>
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='cx',
        syntax='<length-percentage>',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='cy',
        syntax='<length-percentage>',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='d',
        syntax='none | <string>',
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='direction',  # [css-writing-modes-4]
        syntax='ltr | rtl',
        initial_value='ltr',
        inherits=True,
    ),
    PropertyDescriptor(
        name='display',  # [CSS22]
        syntax="inline | block | list-item | inline-block | table"
               " | inline-table | table-row-group | table-header-group"
               " | table-footer-group | table-row | table-column-group"
               " | table-column | table-cell | table-caption | none",
        initial_value='inline',
        inherits=False,
    ),
    PropertyDescriptor(
        name='dominant-baseline',  # [css-inline-3]
        syntax="auto | text-bottom | alphabetic | ideographic | middle"
               " | central | mathematical | hanging | text-top",
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='fill',  # [fill-stroke-3]
        syntax="none | <color> | <url> [ none | <color> ]? | context-fill"
               " | context-stroke",
        # <paint> = none | <color> | <url> [ none | <color> ]? | context-fill
        #  | context-stroke
        # // [SVG2]
        #
        # = <background> = <bg-layer># , <final-bg-layer>
        # // [css-backgrounds-3]
        #
        # <bg-layer> = <bg-image> || <bg-position> [ / <bg-size> ]?
        #  || <repeat-style> || <attachment> || <box> || <box>
        #
        # <final-bg-layer> =  <background-color>
        #  || <bg-image>
        #  || <bg-position> [ / <bg-size> ]?
        #  || <repeat-style> || <attachment> || <box> || <box>
        initial_value='black',
        inherits=True,
    ),
    PropertyDescriptor(
        name='fill-opacity',
        syntax='<number> | <percentage>',
        # = <alpha-value> = <number> | <percentage>
        initial_value='1',
        inherits=True,
    ),
    PropertyDescriptor(
        name='fill-rule',  # [fill-stroke-3]
        syntax='nonzero | evenodd',
        initial_value='nonzero',
        inherits=True,
    ),
    PropertyDescriptor(
        name='filter',  # [filter-effects-1]
        syntax='none'
               ' | [ [ <blur()> | <brightness()> | <contrast()>'
               ' | <drop-shadow()> | <grayscale()> | <hue-rotate()>'
               ' | <invert()> | <opacity()> | <sepia()> | <saturate()> ]'
               ' | <url> ]+',
        # = none | <filter-value-list>
        #
        # <filter-value-list> = [ <filter-function> | <url> ]+
        #
        # <filter-function> = <blur()> | <brightness()> | <contrast()>
        #  | <drop-shadow()> | <grayscale()> | <hue-rotate()> | <invert()>
        #  | <opacity()> | <sepia()> | <saturate()>
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='flood-color',  # [filter-effects-1]
        syntax='<color>',
        initial_value='black',
        inherits=False,
    ),
    PropertyDescriptor(
        name='flood-opacity',  # [filter-effects-1]
        syntax='<number> | <percentage>',
        # = <alpha-value> = <number> | <percentage>
        initial_value='1',
        inherits=False,
    ),
    PropertyDescriptor(
        name='font',  # [css-fonts-4]
        syntax="[ [ [ normal | italic | oblique <angle>? ]"
               " || [ normal | small-caps ]"
               " || [ [ normal | bold | <number> ] | bolder | lighter ]"
               " || [ normal | ultra-condensed | extra-condensed | condensed"
               " | semi-condensed | semi-expanded | expanded"
               " | extra-expanded | ultra-expanded ] ]?"
               " [ [ xx-small | x-small | small | medium | large | x-large"
               " | xx-large ] | [ larger | smaller ] | <length-percentage> ]"
               " [ / [ normal | <number> || <length-percentage> ] ]?"
               " [ [ <string> | [ serif | sans-serif | cursive | fantasy"
               " | monospace | system-ui | emoji | math | fangsong ] ]# ] ]"
               " | caption | icon | menu | message-box | small-caption"
               " | status-bar",
        # = [ [ <font-style> || <font-variant-css2> || <font-weight>
        #  || <font-stretch-css3> ]? <font-size> [ / <line-height> ]?
        #  <font-family> ] | caption | icon | menu | message-box
        #  | small-caption | status-bar
        #
        # <font-style> = normal | italic | oblique <angle>?
        #
        # <font-variant-css2>= [normal | small-caps]
        #
        # <font-weight> = <font-weight-absolute> | bolder | lighter
        #
        # <font-weight-absolute> = [normal | bold | <number>]
        #
        # <font-stretch-css3>= [normal | ultra-condensed | extra-condensed
        #  | condensed | semi-condensed | semi-expanded | expanded
        #  | extra-expanded | ultra-expanded]
        #
        # <font-size> = <absolute-size> | <relative-size>
        #  | <length-percentage>
        #
        # <absolute-size> = [ xx-small | x-small | small | medium | large
        #  | x-large | xx-large ]
        #
        # <relative-size> = [ larger | smaller ]
        #
        # <line-height> = normal | <number> || <length-percentage>
        #
        # <font-family> = [ <family-name> | <generic-family> ]#
        #
        # <generic-family> = serif | sans-serif | cursive | fantasy
        #  | monospace | system-ui | emoji | math | fangsong
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-family',  # [css-fonts-4]
        syntax="[ <string> | [ serif | sans-serif | cursive | fantasy"
               " | monospace | system-ui | emoji | math | fangsong ] ]#",
        # = [ <family-name> | <generic-family> ]#
        #
        # <generic-family> = serif | sans-serif | cursive | fantasy
        #  | monospace | system-ui | emoji | math | fangsong
        initial_value='sans-serif',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-feature-settings',  # [css-fonts-3]
        syntax='normal | [ <string> [ <integer> | on | off ]? ]#',
        # = normal | <feature-tag-value>#
        #
        # <feature-tag-value> = <string> [ <integer> | on | off ]?
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-kerning',  # [css-fonts-3]
        syntax='auto | normal | none',
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-language-override',  # [css-fonts-4]
        syntax='normal | <string>',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-max-size',  # [css-fonts-4]
        syntax="[ xx-small | x-small | small | medium | large | x-large"
               " | xx-large ]"
               " | [ larger | smaller ]"
               " | <length-percentage>"
               " | infinity ",
        # = <absolute-size> | <relative-size> | <length-percentage>
        #
        # <absolute-size> = [ xx-small | x-small | small | medium | large
        #  | x-large | xx-large ]
        #
        # <relative-size> = [ larger | smaller ]
        initial_value='infinity',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-min-size',  # [css-fonts-4]
        syntax="[ xx-small | x-small | small | medium | large | x-large"
               " | xx-large ]"
               " | [ larger | smaller ]"
               " | <length-percentage>",
        # = <absolute-size> | <relative-size> | <length-percentage>
        #
        # <absolute-size> = [ xx-small | x-small | small | medium | large
        #  | x-large | xx-large ]
        #
        # <relative-size> = [ larger | smaller ]
        initial_value='0',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-optical-sizing',  # [css-fonts-4]
        syntax='auto | none',
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-palette',  # [css-fonts-4]
        syntax='normal | light | dark | <custom-ident>',
        # Value: normal | light | dark | <palette-identifier>
        #
        # <palette-identifier> = defined by using the '@font-palette-values'
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-size',  # [css-fonts-4]
        syntax="[ xx-small | x-small | small | medium | large | x-large"
               " | xx-large ]"
               " | [ larger | smaller ]"
               " | <length-percentage>",
        # = <absolute-size> | <relative-size> | <length-percentage>
        #
        # <absolute-size> = [ xx-small | x-small | small | medium | large
        #  | x-large | xx-large ]
        #
        # <relative-size> = [ larger | smaller ]
        initial_value='medium',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-size-adjust',  # [css-fonts-4]
        syntax='none | <number>',
        initial_value='none',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-stretch',  # [css-fonts-4]
        syntax="normal | <percentage> | ultra-condensed | extra-condensed"
               " | condensed | semi-condensed | semi-expanded | expanded"
               " | extra-expanded | ultra-expanded",
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-stretch-css3',  # for the 'font' property
        syntax="normal | ultra-condensed | extra-condensed | condensed"
               " | semi-condensed | semi-expanded | expanded | extra-expanded"
               " | ultra-expanded",
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-style',  # [css-fonts-4]
        syntax='normal | italic | oblique <angle>?',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-synthesis',  # [css-fonts-4]
        syntax='none | [ weight || style || small-caps ]',
        initial_value='weight style small-caps',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-synthesis-small-caps',  # [css-fonts-4]
        syntax='auto | none',
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-synthesis-style',  # [css-fonts-4]
        syntax='auto | none',
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-synthesis-weight',  # [css-fonts-4]
        syntax='auto | none',
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variant',  # [css-fonts-3]
        syntax="normal | none"
               " | ["
               " [ common-ligatures | no-common-ligatures ]"
               " || [ discretionary-ligatures | no-discretionary-ligatures ]"
               " || [ historical-ligatures | no-historical-ligatures ]"
               " || [ contextual | no-contextual ]"
               " || [ small-caps | all-small-caps | petite-caps"
               " | all-petite-caps | unicase | titling-caps ]"
               " || [ <stylistic(<feature-value-name>)> || historical-forms"
               " || <styleset(<feature-value-name>#)>"
               " || <character-variant(<feature-value-name>#)>"
               " || <swash(<feature-value-name>)>"
               " || <ornaments(<feature-value-name>)>"
               " || <annotation(<feature-value-name>)> ]"
               " || [ lining-nums | oldstyle-nums ]"
               " || [ proportional-nums | tabular-nums ]"
               " || [ diagonal-fractions | stacked-fractions ]"
               " || ordinal || slashed-zero"
               " || [ jis78 | jis83 | jis90 | jis04 | simplified"
               " | traditional ]"
               " || [ full-width | proportional-width ]"
               " || ruby"
               " || [ sub | super ]"
               " ]",
        # = normal | none
        #  | [ <common-lig-values>
        #  || <discretionary-lig-values>
        #  || <historical-lig-values>
        #  || <contextual-alt-values>
        #  || [ small-caps | all-small-caps | petite-caps | all-petite-caps
        #  | unicase | titling-caps ]
        #  || <numeric-figure-values>
        #  || <numeric-spacing-values>
        #  || <numeric-fraction-values>
        #  || ordinal || slashed-zero
        #  || <east-asian-variant-values>
        #  || <east-asian-width-values>
        #  || ruby || [ sub | super ] ]
        #
        # <common-lig-values> = [ common-ligatures | no-common-ligatures ]
        #
        # <discretionary-lig-values> = [ discretionary-ligatures
        #  | no-discretionary-ligatures ]
        #
        # <historical-lig-values> = [ historical-ligatures
        #  | no-historical-ligatures ]
        #
        # <contextual-alt-values> = [ contextual | no-contextual ]
        #
        # <numeric-figure-values> = [ lining-nums | oldstyle-nums ]
        #
        # <numeric-spacing-values> = [ proportional-nums | tabular-nums ]
        #
        # <numeric-fraction-values> = [ diagonal-fractions
        #  | stacked-fractions ]
        #
        # <east-asian-variant-values> = [ jis78 | jis83 | jis90 | jis04
        #  | simplified | traditional ]
        #
        # <east-asian-width-values> = [ full-width | proportional-width ]
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variant-alternates',  # [css-fonts-4]
        syntax="normal"
               " | [ <stylistic(<feature-value-name>)>"
               " || historical-forms"
               " || <styleset(<feature-value-name>#)>"
               " || <character-variant(<feature-value-name>#)>"
               " || <swash(<feature-value-name>)>"
               " || <ornaments(<feature-value-name>)>"
               " || <annotation(<feature-value-name>)> ]",
        # = normal
        #  | [ stylistic(<feature-value-name>)
        #  || historical-forms
        #  || styleset(<feature-value-name>#)
        #  || character-variant(<feature-value-name>#)
        #  || swash(<feature-value-name>)
        #  || ornaments(<feature-value-name>)
        #  || annotation(<feature-value-name>) ]
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variant-caps',  # [css-fonts-3]
        syntax="normal | small-caps | all-small-caps | petite-caps"
               " | all-petite-caps | unicase | titling-caps",
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variant-css2',  # for the 'font' property
        syntax='normal | small-caps',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variant-east-asian',  # [css-fonts-3]
        syntax="normal | ["
               " [ jis78 | jis83 | jis90 | jis04 | simplified | traditional ]"
               " || [ full-width | proportional-width ]"
               " || ruby ]",
        # = normal
        #  | [ <east-asian-variant-values>
        #  || <east-asian-width-values>
        #  || ruby ]
        #
        # <east-asian-variant-values> = [ jis78 | jis83 | jis90 | jis04
        #  | simplified | traditional ]
        #
        # <east-asian-width-values> = [ full-width | proportional-width ]
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variant-emoji',  # [css-fonts-4]
        syntax='auto | text | emoji | unicode',
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variant-ligatures',  # [css-fonts-3]
        syntax="normal | none"
               " | [ [ common-ligatures | no-common-ligatures ]"
               " || [ discretionary-ligatures | no-discretionary-ligatures ]"
               " || [ historical-ligatures | no-historical-ligatures ]"
               " || [ contextual | no-contextual ] ]",
        # = normal | none
        #  | [ <common-lig-values>
        #  || <discretionary-lig-values>
        #  || <historical-lig-values>
        #  || <contextual-alt-values> ]
        #
        # <common-lig-values> = [ common-ligatures | no-common-ligatures ]
        #
        # <discretionary-lig-values> = [ discretionary-ligatures
        #  | no-discretionary-ligatures ]
        #
        # <historical-lig-values> = [ historical-ligatures
        #  | no-historical-ligatures ]
        #
        # <contextual-alt-values> = [ contextual | no-contextual ]
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variant-numeric',  # [css-fonts-3]
        syntax="normal"
               " | [ [ lining-nums | oldstyle-nums ]"
               " || [ proportional-nums | tabular-nums ]"
               " || [ diagonal-fractions | stacked-fractions ]"
               " || ordinal || slashed-zero ]",
        # = normal
        #  | [ <numeric-figure-values>
        #  || <numeric-spacing-values>
        #  || <numeric-fraction-values>
        #  || ordinal || slashed-zero ]
        #
        # <numeric-figure-values> = [ lining-nums | oldstyle-nums ]
        #
        # <numeric-spacing-values> = [ proportional-nums | tabular-nums ]
        #
        # <numeric-fraction-values> = [ diagonal-fractions
        #  | stacked-fractions ]
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variant-position',  # [css-fonts-3]
        syntax='normal | sub | super',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-variation-settings',  # [css-fonts-4]
        syntax='normal | [ <string> <number> ] #',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='font-weight',  # [css-fonts-4]
        syntax='[ normal | bold | <number> ] | bolder | lighter',
        # = <font-weight-absolute> | bolder | lighter
        #
        # <font-weight-absolute> = [ normal | bold | <number> ]
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='glyph-orientation-vertical',  # [SVG11]
        syntax='auto | <angle>',  # '0deg' or '90deg'
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='height',  # [css-sizing-3]
        syntax="auto | <length-percentage> | min-content | max-content"
               " | <fit-content(<length-percentage>)>",
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='image-rendering',  # [SVG2]
        syntax='auto | optimizeQuality | optimizeSpeed',
        # https://svgwg.org/svg2-draft/painting.html#ImageRenderingProperty
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='inline-size',  # [css-logical-1]
        syntax='<length-percentage> | auto',
        # = <width> = <length> | <percentage> | auto
        # // [css-logical-1]
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='inline-sizing',  # [css-inline-3]
        syntax='normal | stretch',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='isolation',  # [compositing-1]
        syntax='auto | isolate',
        # = <isolation-mode> = auto | isolate
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='letter-spacing',  # [css-text-3]
        syntax='normal | <length>',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='line-height',  # [css-inline-3]
        syntax='normal | <number> || <length-percentage>',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='line-sizing',  # [css-inline-3]
        syntax="quirks-behavior | current-behavior | better-behavior"
               " | box-model-behavior | absolute-behavior",
        initial_value='current-behavior',
        inherits=True,
    ),
    PropertyDescriptor(
        name='lighting-color',  # [filter-effects-1]
        syntax='<color>',
        initial_value='white',
        inherits=False,
    ),
    PropertyDescriptor(
        name='marker',
        syntax='none | <url>',
        # = none | <marker-ref>
        #
        # <marker-ref> = <url>
        initial_value='none',
        inherits=True,
    ),
    PropertyDescriptor(
        name='marker-end',
        syntax='none | <url>',
        # = none | <marker-ref>
        #
        # <marker-ref> = <url>
        initial_value='none',
        inherits=True,
    ),
    PropertyDescriptor(
        name='marker-mid',
        syntax='none | <url>',
        # = none | <marker-ref>
        #
        # <marker-ref> = <url>
        initial_value='none',
        inherits=True,
    ),
    PropertyDescriptor(
        name='marker-start',
        syntax='none | <url>',
        # = none | <marker-ref>
        #
        # <marker-ref> = <url>
        initial_value='none',
        inherits=True,
    ),
    PropertyDescriptor(
        name='mask',  # [css-masking-1]
        syntax="[ [ none | <image> | <url> ]"
               " || [ [ left | center | right | top | bottom"
               " | <length-percentage> ]"
               " |"
               " [ left | center | right | <length-percentage> ]"
               " [ top | center | bottom | <length-percentage> ]"
               " |"
               " [ center | [ left | right ] <length-percentage>? ] &&"
               " [ center | [ top | bottom ] <length-percentage>? ]"
               " ]"
               " [ / ["
               " [ <length-percentage> | auto ]{1,2} | cover | contain ] ]?"
               " || [ repeat-x | repeat-y | [ repeat | space | round"
               " | no-repeat ]{1,2} ]"
               " || [ [ [ [ border-box | padding-box | content-box ]"
               " | margin-box ] | fill-box | stroke-box | view-box ]"
               " | no-clip ]"
               " || [ [ [ [ [ border-box | padding-box | content-box ]"
               " | margin-box ] | fill-box | stroke-box | view-box ]"
               " | no-clip ] | no-clip ]"
               " || [ add | subtract | intersect | exclude ]"
               " || [ alpha | luminance | match-source ] ]#",
        # = <mask-layer>#
        #
        # <mask-layer> =
        #  <mask-reference>
        #  || <position> [ / <bg-size> ]?
        #  || <repeat-style>
        #  || <geometry-box>
        #  || [ <geometry-box> | no-clip ]
        #  || <compositing-operator>
        #  || <masking-mode>
        #
        # <mask-reference> = none | <image> | <mask-source>
        #
        # <mask-source> = <url>
        initial_value='border-box',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-border',  # [css-masking-1]
        syntax="[ none | <image> ]"
               " || [ [ <number> | <percentage> ]{1,4} fill? ]"
               " [ / [ [ <length-percentage> | <number> | auto ]{1,4} ]?"
               " [ / [ <length> | <number> ]{1,4}"
               " ]? ]?"
               " || [ stretch | repeat | round | space ]{1,2}"
               " || [ luminance | alpha ]",
        # = <mask-border-source>
        #  || <mask-border-slice>
        #  [ / <mask-border-width>?
        #  [ / <mask-border-outset>
        #  ]? ]?
        #  || <mask-border-repeat>
        #  || <mask-border-mode>
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-border-mode',  # [css-masking-1]
        syntax='luminance | alpha',
        initial_value='alpha',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-border-outset',  # [css-masking-1]
        syntax='[ <length> | <number> ]{1,4}',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-border-repeat',  # [css-masking-1]
        syntax='[ stretch | repeat | round | space ]{1,2}',
        initial_value='stretch',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-border-slice',  # [css-masking-1]
        syntax='[ <number> | <percentage> ]{1,4} fill?',
        # = <number-percentage>{1,4} fill?
        #
        # <number-percentage> = [ <number> | <percentage> ]
        # // [css-values-3]
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-border-source',  # [css-masking-1]
        syntax='none | <image>',
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-border-width',  # [css-masking-1]
        syntax='[ <length-percentage> | <number> | auto ]{1,4}',
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-clip',  # [css-masking-1]
        syntax="[ [ [ [ border-box | padding-box | content-box ]"
               " | margin-box ] | fill-box | stroke-box | view-box ]"
               " | no-clip ]#",
        # = [ <geometry-box> | no-clip ]#
        #
        # <geometry-box> = <shape-box> | fill-box | stroke-box | view-box
        #
        # <shape-box> = <box> | margin-box
        # // [css-shapes-1]
        #
        # <box> = border-box | padding-box | content-box
        # // [css-backgrounds-3]
        initial_value='border-box',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-composite',  # [css-masking-1]
        syntax="[ add | subtract | intersect | exclude ]#",
        # = <compositing-operator>#
        #
        # <compositing-operator> = add | subtract | intersect | exclude
        initial_value='add',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-image',  # [css-masking-1]
        syntax='[ none | <image> | <url> ]#',
        # = <mask-reference>#
        #
        # <mask-reference> = none | <image> | <mask-source>
        #
        # <mask-source> = <url>
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-mode',  # [css-masking-1]
        syntax='[ alpha | luminance | match-source ]#',
        # = <masking-mode>#
        #
        # <masking-mode> = alpha | luminance | match-source
        initial_value='match-source',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-origin',  # [css-masking-1]
        syntax="[ [ [ border-box | padding-box | content-box ] | margin-box ]"
               " | fill-box | stroke-box | view-box ]#",
        # = <geometry-box>#
        #
        # <geometry-box> = <shape-box> | fill-box | stroke-box | view-box
        #
        # <shape-box> = <box> | margin-box
        # // [css-shapes-1]
        #
        # <box> = border-box | padding-box | content-box
        # // [css-backgrounds-3]
        initial_value='border-box',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-position',  # [css-masking-1]
        syntax="[ [ left | center | right | top | bottom"
               " | <length-percentage> ]"
               " |"
               " [ left | center | right | <length-percentage> ]"
               " [ top | center | bottom | <length-percentage> ]"
               " |"
               " [ center | [ left | right ] <length-percentage>? ] &&"
               " [ center | [ top | bottom ] <length-percentage>? ]"
               "]#",
        # = <position>#
        #
        # <bg-position> = [ [ left | center | right | top | bottom
        #  | <length-percentage> ]
        # |
        #   [ left | center | right | <length-percentage> ]
        #   [ top | center | bottom | <length-percentage> ]
        # |
        #   [ center | [ left | right ] <length-percentage>? ] &&
        #   [ center | [ top | bottom ] <length-percentage>? ]
        # ]
        # // [css-backgrounds-3]
        initial_value='0% 0%',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-repeat',  # [css-masking-1]
        syntax="[ repeat-x | repeat-y | [ repeat | space | round"
               " | no-repeat ]{1,2} ]#",
        # = <repeat-style>#
        #
        # <repeat-style> = repeat-x | repeat-y | [repeat | space | round
        #  | no-repeat]{1,2}
        # // [css-backgrounds-3]
        initial_value='repeat',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-size',  # [css-masking-1]
        syntax='[ [ <length-percentage> | auto ]{1,2} | cover | contain ]#',
        # = <bg-size>#
        #
        # <bg-size> = [ <length-percentage> | auto ]{1,2} | cover | contain
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='mask-type',  # [css-masking-1]
        syntax='luminance | alpha',
        initial_value='luminance',
        inherits=False,
    ),
    PropertyDescriptor(
        name='max-height',  # [css-sizing-3]
        syntax="none | <length-percentage> | min-content | max-content"
               " | <fit-content(<length-percentage>)>",
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='max-width',  # [css-sizing-3]
        syntax="none | <length-percentage> | min-content | max-content"
               " | <fit-content(<length-percentage>)>",
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='min-height',  # [css-sizing-3]
        syntax="auto | <length-percentage> | min-content | max-content"
               " | <fit-content(<length-percentage>)>",
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='min-width',  # [css-sizing-3]
        syntax="auto | <length-percentage> | min-content | max-content"
               " | <fit-content(<length-percentage>)>",
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='opacity',  # [css-color-4]
        syntax='<number> | <percentage>',
        # = <alpha-value> = <number> | <percentage>
        initial_value='1',
        inherits=False,
    ),
    PropertyDescriptor(
        name='overflow',  # [css-overflow-3]
        syntax='[ visible | hidden | clip | scroll | auto ]{1,2}',
        initial_value='visible',
        inherits=False,
    ),
    PropertyDescriptor(
        name='overflow-x',  # [css-overflow-3]
        syntax='visible | hidden | clip | scroll | auto',
        initial_value='visible',
        inherits=False,
    ),
    PropertyDescriptor(
        name='overflow-y',  # [css-overflow-3]
        syntax='visible | hidden | clip | scroll | auto',
        initial_value='visible',
        inherits=False,
    ),
    PropertyDescriptor(
        name='paint-order',
        syntax='normal | [ fill || stroke || markers ]',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='pointer-events',
        syntax="auto | bounding-box | visiblePainted | visibleFill"
               " | visibleStroke | visible | painted | fill | stroke | all"
               " | none",
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='r',
        syntax='<length-percentage>',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='rx',
        syntax='<length-percentage> | auto',
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='ry',
        syntax='<length-percentage> | auto',
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='shape-image-threshold',  # [css-shapes-1]
        syntax='<number>',
        initial_value='0.0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='shape-inside',  # [css-shapes-2]
        syntax="auto"
               " | [ [ <inset()> | <circle()> | <ellipse()> | <polygon()> ]"
               " | <url> ]+",
        # = auto | [ <basic-shape> | <uri> ]+
        # // [SVG2]
        #
        # <basic-shape> = 'inset()', 'circle()', 'ellipse()' or 'polygon()'
        # // [css-shapes-2]
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='shape-margin',  # [css-shapes-1]
        syntax='<length-percentage>',
        # = <length> | <percentage>
        # // [css-shapes-1]
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='shape-padding',  # [css-shapes-2]
        syntax='<length>',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='shape-rendering',
        syntax='auto | optimizeSpeed | crispEdges | geometricPrecision',
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='shape-subtract',  # [SVG2]
        syntax="none"
               " | [ [ <inset()> | <circle()> | <ellipse()> | <polygon()> ]"
               " | <url> ]+",
        # = none | [ <basic-shape> | <uri> ]+
        # // [SVG2]
        #
        # <basic-shape> = 'inset()', 'circle()', 'ellipse()' or 'polygon()'
        # // [css-shapes-2]
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='stop-color',
        syntax='currentColor | <color> <icc-color()>',
        # = currentColor | <color> <icccolor>
        #
        # <icccolor> = "icc-color(" name (comma-wsp number)+ ")"
        initial_value='black',
        inherits=False,
    ),
    PropertyDescriptor(
        name='stop-opacity',
        syntax='<number> | <percentage>',
        # <alpha-value> = <number> | <percentage>
        initial_value='1',
        inherits=False,
    ),
    PropertyDescriptor(
        name='stroke',
        syntax="none | <color> | <url> [none | <color>]? | context-fill"
               " | context-stroke",
        # <paint> = none | <color> | <url> [none | <color>]? | context-fill
        #  | context-stroke
        initial_value='none',
        inherits=True,
    ),
    PropertyDescriptor(
        name='stroke-dasharray',
        syntax='none | [ <length-percentage> | <number> ]#*',
        # = none | <dasharray>
        #
        # <dasharray> = [ <length-percentage> | <number> ]#*
        initial_value='none',
        inherits=True,
    ),
    PropertyDescriptor(
        name='stroke-dashoffset',
        syntax='<length-percentage>',
        initial_value='0',
        inherits=True,
    ),
    PropertyDescriptor(
        name='stroke-linecap',
        syntax='butt | round | square',
        initial_value='butt',
        inherits=True,
    ),
    PropertyDescriptor(
        name='stroke-linejoin',
        syntax='miter | miter-clip | round | bevel | arcs',
        initial_value='miter',
        inherits=True,
    ),
    PropertyDescriptor(
        name='stroke-miterlimit',
        syntax='<number>',
        initial_value='4',
        inherits=True,
    ),
    PropertyDescriptor(
        name='stroke-opacity',
        syntax='<number> | <percentage>',
        # <alpha-value> = <number> | <percentage>
        initial_value='1',
        inherits=True,
    ),
    PropertyDescriptor(
        name='stroke-width',
        syntax='<length-percentage>',
        initial_value='1',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-align',  # [css-text-4]
        syntax="[ start | end | left | right | center | justify"
               " | match-parent | justify-all ] || <string>",
        initial_value='start',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-align-all',  # [css-text-3]
        syntax='start | end | left | right | center | justify | match-parent',
        initial_value='start',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-align-last',  # [css-text-3]
        syntax="auto | start | end | left | right | center | justify"
               " | match-parent",
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-anchor',  # [SVG2]
        syntax='start | middle | end',
        initial_value='start',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-decoration',  # [css-text-decor-3]
        syntax="[ none | [ underline || overline || line-through || blink ]"
               " | spelling-error | grammar-error ]"
               " || [ solid | double | dotted | dashed | wavy ]"
               " || <color>",
        # = <text-decoration-line>
        #  || <text-decoration-style>
        #  || <text-decoration-color>
        inherits=False,
    ),
    PropertyDescriptor(
        name='text-decoration-color',  # [css-text-decor-3]
        syntax='<color>',
        initial_value='currentcolor',
        inherits=False,
    ),
    PropertyDescriptor(
        name='text-decoration-fill',  # [SVG2]
        syntax="none | <color> | <url> [ none | <color> ]? | context-fill"
               " | context-stroke",
        # = <paint> = none | <color> | <url> [ none | <color> ]?
        #  | context-fill | context-stroke
        inherits=False,
    ),
    PropertyDescriptor(
        name='text-decoration-line',  # [css-text-decor-4]
        syntax="none | [ underline || overline || line-through || blink ]"
               " | spelling-error | grammar-error",
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='text-decoration-stroke',  # [SVG2]
        syntax="none | <color> | <url> [ none | <color> ]? | context-fill"
               " | context-stroke",
        # = <paint> = none | <color> | <url> [ none | <color> ]?
        #  | context-fill | context-stroke
        inherits=False,
    ),
    PropertyDescriptor(
        name='text-decoration-style',  # [css-text-decor-3]
        syntax='solid | double | dotted | dashed | wavy',
        initial_value='solid',
        inherits=False,
    ),
    PropertyDescriptor(
        name='text-decoration-width',  # [css-text-decor-3]
        syntax='auto | from-font | <length>',
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='text-indent',  # [css-text-3]
        syntax='[ <length-percentage> ] && hanging? && each-line?',
        initial_value='0',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-orientation',  # [css-writing-modes-4]
        syntax='mixed | upright | sideways',
        initial_value='mixed',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-overflow',  # [css-overflow-4]
        syntax='[ clip | ellipsis | <string> | fade | <fade()> ]{1,2}',
        # <fade()> = fade( <length> | <percentage> )
        initial_value='clip',
        inherits=False,
    ),
    PropertyDescriptor(
        name='text-rendering',
        syntax="auto | optimizeSpeed | optimizeLegibility"
               " | geometricPrecision",
        initial_value='auto',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-space-collapse',  # [css-text-4]
        syntax="collapse | discard | preserve | preserve-breaks"
               " | preserve-spaces",
        initial_value='collapse',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-space-trim',  # [css-text-4]
        syntax='none | trim-inner || discard-before || discard-after',
        initial_value='none',
        inherits=True,
    ),
    PropertyDescriptor(
        name='text-wrap',  # [css-text-4]
        syntax='wrap | nowrap | balance',
        initial_value='wrap',
        inherits=True,
    ),
    # PropertyDescriptor(
    #     name='transform',  # [css-transforms-1]
    #     syntax='none | <transform-function>+',
    #     # = none | <transform-list>
    #     #
    #     # <transform-list> = <transform-function>+
    #     #
    #     # <transform-function> = <matrix()> | <translate()> | <translateX()>
    #     #  | <translateY()> | <scale()> | <scaleX()> | <scaleY()> | <rotate()>
    #     #  | <skew()> | <skewX()> | <skewY()>
    #     initial_value='none',
    #     inherits=False,
    # ),
    # PropertyDescriptor(
    #     name='transform-box',  # [css-transforms-1]
    #     syntax='content-box | border-box | fill-box | stroke-box | view-box',
    #     initial_value='view-box',
    #     inherits=False,
    # ),
    # PropertyDescriptor(
    #     name='transform-origin',  # [css-transforms-1]
    #     syntax="[ left | center | right | top | bottom | <length-percentage> ]"
    #            " |"
    #            " [ left | center | right | <length-percentage> ]"
    #            " [ top | center | bottom | <length-percentage> ] <length>?"
    #            " |"
    #            " [[ center | left | right ] && [ center | top | bottom ]]"
    #            " <length>?",
    #     initial_value='50% 50%',
    #     inherits=False,
    # ),
    PropertyDescriptor(
        name='unicode-bidi',  # [css-writing-modes]
        syntax="normal | embed | isolate | bidi-override | isolate-override"
               " | plaintext",
        initial_value='normal',
        inherits=False,
    ),
    PropertyDescriptor(
        name='vector-effect',  # [SVG2]
        syntax="none | [ non-scaling-stroke | non-scaling-size | non-rotation"
               " | fixed-position ]+ [ viewport | screen ]?",
        initial_value='none',
        inherits=False,
    ),
    PropertyDescriptor(
        name='vertical-align',  # [css-inline-3]
        syntax="[ <length-percentage> | sub | super ]"
               " || [ baseline | text-bottom | alphabetic | ideographic"
               " | middle | central | mathematical | text-top | bottom"
               " | center | top ]",
        # = <baseline-shift> || <alignment-baseline>
        #
        # <baseline-shift> = <length-percentage> | sub | super
        #
        # <alignment-baseline> = baseline | text-bottom | alphabetic
        #  | ideographic | middle | central | mathematical | text-top
        #  | bottom | center | top
        initial_value='baseline',
        inherits=False,
    ),
    PropertyDescriptor(
        name='visibility',  # [CSS22]
        syntax='visible | hidden | collapse',
        initial_value='visible',
        inherits=True,
    ),
    PropertyDescriptor(
        name='white-space',  # [css-text-4]
        syntax='normal | pre | nowrap | pre-wrap | pre-line',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='width',  # [css-sizing-3]
        syntax="auto | <length-percentage> | min-content | max-content"
               " | <fit-content(<length-percentage>)>",
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='will-change',  # [css-will-change-1]
        syntax='auto | [ scroll-position | contents | <custom-ident> ]#',
        # = auto | <animateable-feature>#
        #
        # <animateable-feature> = scroll-position | contents | <custom-ident>
        initial_value='auto',
        inherits=False,
    ),
    PropertyDescriptor(
        name='word-spacing',  # [css-text-3]
        syntax='normal | <length-percentage>',
        initial_value='normal',
        inherits=True,
    ),
    PropertyDescriptor(
        name='writing-mode',  # [css-writing-modes-4] and [SVG11]
        syntax="horizontal-tb | vertical-rl | vertical-lr"
               " | sideways-rl | sideways-lr"
               " | lr | lr-tb | rl | rl-tb | tb | tb-rl",
        initial_value='horizontal-tb',
        inherits=True,
    ),
    PropertyDescriptor(
        name='x',
        syntax='<length-percentage>',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='x1',
        syntax='<length-percentage> | <number>',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='x2',
        syntax='<length-percentage> | <number>',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='y',
        syntax='<length-percentage>',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='y1',
        syntax='<length-percentage> | <number>',
        initial_value='0',
        inherits=False,
    ),
    PropertyDescriptor(
        name='y2',
        syntax='<length-percentage> | <number>',
        initial_value='0',
        inherits=False,
    ),
]

css_property_descriptor_map = dict((x.name, x) for x in _property_descriptors)
del _property_descriptors
