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

import tinycss2

from .props import css_property_descriptor_map, css_wide_keyword_set, \
    PropertySyntax

_RE_CSS_VERSION = re.compile(r'-css[0-9]$')


def create_component_list(value):
    component_list = tinycss2.parse_component_value_list(
        value,
        skip_comments=True)
    return component_list


def get_longhand_list(shorthand_name):
    longhand_list = list()
    for property_name in Shorthand.longhands(shorthand_name):
        if Shorthand.is_shorthand(property_name):
            longhand_list.extend(get_longhand_list(property_name))
        else:
            longhand_list.append(property_name)

    return longhand_list


class Shorthand(object):

    def __init__(self, declarations):
        self._declarations = declarations  # {property: (value, priority)}

    def _shorthand(self, property_name):
        shorthand = _shorthand_property_class_map[property_name]
        return shorthand(self._declarations)

    def get_property_priority(self, property_name):
        declarations = self._declarations
        priorities = list()
        for longhand_name in Shorthand.longhands(property_name):
            if Shorthand.is_shorthand(longhand_name):
                priority = self.get_property_priority(longhand_name)
            else:
                if longhand_name not in declarations:
                    continue
                priority = declarations[longhand_name][1]
            priorities.append(priority)

        if (len(priorities) == 0
                or (len(priorities) > 1
                    and not all(priorities[0] == x for x in priorities[1:]))):
            return ''
        return priorities[0]

    def get_property_value(self, property_name):
        declarations = self._declarations
        property_map = OrderedDict()
        priorities = list()
        for longhand_name in Shorthand.longhands(property_name):
            if Shorthand.is_shorthand(longhand_name):
                value = self.get_property_value(longhand_name)
                priority = self.get_property_priority(longhand_name)
            else:
                if longhand_name not in declarations:
                    continue
                desc = css_property_descriptor_map[longhand_name]
                value, priority = declarations[longhand_name]
                if len(value) == 0 or not desc.supports(value):
                    return ''
            property_map[longhand_name] = value
            priorities.append(priority)

        if (len(priorities) == 0
                or (len(priorities) > 1
                    and not all(priorities[0] == x for x in priorities[1:]))):
            return ''

        shorthand = self._shorthand(property_name)
        value = shorthand.tostring(property_map)
        return value

    @staticmethod
    def is_shorthand(property_name):
        if property_name.startswith('--'):
            return False
        property_name = property_name.lower()
        return property_name in shorthand_property_map

    @staticmethod
    def longhands(property_name, remove_version=True):
        property_name = property_name.lower()
        longhand_names = shorthand_property_map.get(property_name, ())
        if not remove_version or len(longhand_names) == 0:
            return longhand_names
        return tuple(_RE_CSS_VERSION.sub('', x) for x in longhand_names)

    def remove_property(self, property_name):
        declarations = self._declarations
        removed = False
        for longhand_name in Shorthand.longhands(property_name):
            if Shorthand.is_shorthand(longhand_name):
                if self.remove_property(longhand_name):
                    removed = True
            else:
                if longhand_name not in declarations:
                    continue
                del declarations[longhand_name]
                removed = True

        return removed

    def set_css_declaration(self, property_name, component_list, priority):
        property_name = property_name.lower()
        if property_name not in shorthand_property_map:
            return False

        shorthand = self._shorthand(property_name)
        updated = shorthand.set_css_declaration(component_list, priority)
        return updated


class ShorthandProperty(ABC):

    def __init__(self, declarations):
        self._declarations = declarations  # type: OrderedDict

    @staticmethod
    def _parse_component_list(property_name, component_list, components_map,
                              css_wide_keywords):
        desc = css_property_descriptor_map[property_name]
        found_solidus = False
        target = None
        for component in list(component_list):
            if component.type == 'whitespace':
                if target is not None:
                    target.append(component)
                    component_list.remove(component)
                continue
            elif (component.type == 'ident'
                  and component.lower_value in css_wide_keyword_set):
                css_wide_keywords.append(component.lower_value)
                component_list.remove(component)
                continue
            elif component == ',':
                if '#' not in desc.syntax and ',' not in desc.syntax:
                    if property_name in components_map:
                        del components_map[property_name]
                    break
                elif target is not None:
                    target.append(component)
                    component_list.remove(component)
                continue
            elif component == '/':
                if (property_name not in _with_solidus_properties
                        and '/' not in desc.syntax):
                    if target is not None and len(target) > 0:
                        break
                    continue
                elif found_solidus:
                    break
                else:
                    found_solidus = True
                    target = components_map.setdefault(property_name, list())
                    if '/' in desc.syntax:
                        target.append(component)
                    component_list.remove(component)
                    continue
            elif (property_name in _with_solidus_properties
                  and not found_solidus):
                continue

            supported, syntax = desc.support(component)
            if supported:
                target = components_map.setdefault(property_name, list())
                target.append(component)
                component_list.remove(component)
                if (property_name == 'mask-border-slice'
                        and syntax == PropertySyntax.CUSTOM_IDENT):
                    # <mask-border-slice> = <number-percentage>{1,4} fill?
                    break
            elif found_solidus or (target is not None and len(target) > 0):
                break

        if (property_name in components_map
                and len(components_map[property_name]) == 0):
            del components_map[property_name]
        return components_map, css_wide_keywords

    @staticmethod
    def _parse_css_declaration(property_name, component_list,
                               set_initial_value=True):
        components_map = OrderedDict()
        css_wide_keywords = list()
        longhand_names = shorthand_property_map[property_name]
        for longhand_name in longhand_names:
            ShorthandProperty._parse_component_list(longhand_name,
                                                    component_list,
                                                    components_map,
                                                    css_wide_keywords)

        if len(css_wide_keywords) > 0:
            components_map.clear()
        if len(css_wide_keywords) == 1 and set_initial_value:
            initial_value = create_component_list(css_wide_keywords[0])
            for longhand_name in longhand_names:
                components_map[longhand_name] = initial_value.copy()
        elif set_initial_value:
            for longhand_name in longhand_names:
                if longhand_name not in components_map:
                    desc = css_property_descriptor_map[longhand_name]
                    components_map[longhand_name] = create_component_list(
                        desc.initial_value)

        return components_map, css_wide_keywords

    def _set_css_declaration_map(self, components_map, priority):
        declarations = self._declarations
        updated = False
        for property_name, component_list in components_map.items():
            value = tinycss2.serialize(component_list).strip()
            updated = True
            if property_name in declarations:
                declarations.move_to_end(property_name)
            declarations[property_name] = value, priority

        return updated

    @abstractmethod
    def set_css_declaration(self, component_list, priority):
        raise NotImplementedError

    @abstractmethod
    def tostring(self, property_map):
        raise NotImplementedError


class FontShorthand(ShorthandProperty):

    def set_css_declaration(self, component_list, priority):
        components_map, _ = ShorthandProperty._parse_css_declaration(
            'font',
            component_list)

        font_variant_components = components_map.pop('font-variant-css2')
        shorthand = FontVariantShorthand(self._declarations)
        shorthand.set_css_declaration(font_variant_components, priority)

        font_stretch_components = components_map.pop('font-stretch-css3')
        components_map['font-stretch'] = font_stretch_components

        updated = self._set_css_declaration_map(components_map, priority)
        return updated

    def tostring(self, property_map):
        declarations = self._declarations
        keys = list(declarations.keys())
        max_index_of_font = -1
        min_index_of_font = -1
        longhand_names = get_longhand_list('font')
        for property_name in longhand_names:
            if property_name not in keys:
                return ''
            index = keys.index(property_name)
            max_index_of_font = max(max_index_of_font, index)
            if min_index_of_font < 0:
                min_index_of_font = index
            else:
                min_index_of_font = min(min_index_of_font, index)

        for property_name in font_sub_property_list:
            if property_name not in keys:
                continue
            index = keys.index(property_name)
            if (min_index_of_font < index < max_index_of_font
                    or (max_index_of_font < index
                        and declarations[property_name][0] != 'initial')):
                return ''

        font_style = property_map.get('font-style')
        font_variant = property_map.get('font-variant')
        font_weight = property_map.get('font-weight')
        font_stretch = property_map.get('font-stretch')
        font_size = property_map.get('font-size')
        line_height = property_map.get('line-height')
        font_family = property_map.get('font-family')
        values = (
            font_style,
            font_variant,
            font_weight,
            font_stretch,
            font_size,
            line_height,
            font_family,
        )
        if any(x is None or len(x) == 0 for x in values):
            return ''
        elif any(x in css_wide_keyword_set for x in values):
            if (all(x in css_wide_keyword_set for x in values)
                    and all(x == values[0] for x in values[1:])):
                return values[0]
            else:
                return ''

        desc = css_property_descriptor_map['font-variant-css2']
        if not desc.supports(font_variant):
            return ''

        desc = css_property_descriptor_map['font-stretch-css3']
        if not desc.supports(font_stretch):
            return ''

        if line_height != 'normal':
            property_map = property_map.copy()
            property_map['font-size'] = '{}/{}'.format(font_size, line_height)
            del property_map['line-height']

        values = list()
        for property_name, value in property_map.items():
            desc = css_property_descriptor_map[property_name]
            if property_name == 'font-family' or value != desc.initial_value:
                values.append(value)

        s = ' '.join(values)
        return s


class FontSynthesisShorthand(ShorthandProperty):

    def set_css_declaration(self, component_list, priority):
        components_map = OrderedDict()
        values = [tinycss2.serialize([x]) for x in component_list
                  if x.type != 'whitespace']
        font_synthesis_weight = None
        font_synthesis_style = None
        if len(values) == 1:
            if values[0] == 'none':
                font_synthesis_weight = 'none'
                font_synthesis_style = 'none'
            elif values[0] == 'weight':
                font_synthesis_weight = 'auto'
                font_synthesis_style = 'none'
            elif values[0] == 'style':
                font_synthesis_weight = 'none'
                font_synthesis_style = 'auto'
            elif values[0].lower() in css_wide_keyword_set:
                value = values[0].lower()
                font_synthesis_weight = font_synthesis_style = value
        elif len(values) == 2 and 'weight' in values and 'style' in values:
            font_synthesis_weight = 'auto'
            font_synthesis_style = 'auto'

        if font_synthesis_weight is None:
            desc = css_property_descriptor_map['font-synthesis-weight']
            font_synthesis_weight = desc.initial_value
        if font_synthesis_style is None:
            desc = css_property_descriptor_map['font-synthesis-style']
            font_synthesis_style = desc.initial_value

        components_map['font-synthesis-weight'] = \
            create_component_list(font_synthesis_weight)
        components_map['font-synthesis-style'] = \
            create_component_list(font_synthesis_style)

        updated = self._set_css_declaration_map(components_map, priority)
        return updated

    def tostring(self, property_map):
        _ = self
        font_synthesis_weight = property_map.get('font-synthesis-weight')
        font_synthesis_style = property_map.get('font-synthesis-style')
        if font_synthesis_weight is None or font_synthesis_style is None:
            return ''
        elif (font_synthesis_weight == 'none'
              and font_synthesis_style == 'none'):
            return 'none'
        elif (font_synthesis_weight == 'auto'
              and font_synthesis_style == 'none'):
            return 'weight'
        elif (font_synthesis_weight == 'none'
              and font_synthesis_style == 'auto'):
            return 'style'
        elif (font_synthesis_weight == 'auto'
              and font_synthesis_style == 'auto'):
            return 'weight style'
        elif (font_synthesis_weight == font_synthesis_style
              and font_synthesis_weight in css_wide_keyword_set):
            return font_synthesis_weight
        return ''


class FontVariantShorthand(ShorthandProperty):

    def set_css_declaration(self, component_list, priority):
        value = tinycss2.serialize(component_list).strip()
        if value in ('normal', 'none'):
            components_map = OrderedDict()
            for longhand_name in shorthand_property_map['font-variant']:
                if (longhand_name == 'font-variant-ligatures'
                        and value == 'none'):
                    initial_value = 'none'
                else:
                    desc = css_property_descriptor_map[longhand_name]
                    initial_value = desc.initial_value
                components_map[longhand_name] = create_component_list(
                    initial_value)
        else:
            components_map, _ = ShorthandProperty._parse_css_declaration(
                'font-variant',
                component_list)

        updated = self._set_css_declaration_map(components_map, priority)
        return updated

    def tostring(self, property_map):
        _ = self
        font_variant_ligatures = property_map.get('font-variant-ligatures')
        font_variant_caps = property_map.get('font-variant-caps')
        font_variant_alternates = property_map.get('font-variant-alternates')
        font_variant_numeric = property_map.get('font-variant-numeric')
        font_variant_east_asian = property_map.get('font-variant-east-asian')
        font_variant_position = property_map.get('font-variant-position')
        values = (
            font_variant_ligatures,
            font_variant_caps,
            font_variant_alternates,
            font_variant_numeric,
            font_variant_east_asian,
            font_variant_position,
        )
        if any(x is None for x in values):
            return ''
        elif all(x == 'normal' for x in values):
            return 'normal'
        elif font_variant_ligatures == 'none':
            if all(x == 'normal' for x in (font_variant_caps,
                                           font_variant_alternates,
                                           font_variant_numeric,
                                           font_variant_east_asian,
                                           font_variant_position)):
                return 'none'
            else:
                return ''
        elif any(x in css_wide_keyword_set for x in values):
            if (all(x in css_wide_keyword_set for x in values)
                    and all(x == values[0] for x in values[1:])):
                return values[0]
            else:
                return ''

        s = ' '.join(x for x in values if x != 'normal')
        return s


class MaskBorderShorthand(ShorthandProperty):

    def set_css_declaration(self, component_list, priority):
        components_map = OrderedDict()
        css_wide_keywords = list()

        ShorthandProperty._parse_component_list(
            'mask-border-source',
            component_list,
            components_map,
            css_wide_keywords)

        ShorthandProperty._parse_component_list(
            'mask-border-slice',
            component_list,
            components_map,
            css_wide_keywords)

        if 'mask-border-slice' in components_map:
            ShorthandProperty._parse_component_list(
                'mask-border-width',
                component_list,
                components_map,
                css_wide_keywords)

        if 'mask-border-width' in components_map:
            ShorthandProperty._parse_component_list(
                'mask-border-outset',
                component_list,
                components_map,
                css_wide_keywords)

        ShorthandProperty._parse_component_list(
            'mask-border-repeat',
            component_list,
            components_map,
            css_wide_keywords)

        ShorthandProperty._parse_component_list(
            'mask-border-mode',
            component_list,
            components_map,
            css_wide_keywords)

        if len(css_wide_keywords) > 1:
            return False
        elif len(css_wide_keywords) == 1:
            components_map.clear()
            initial_value = create_component_list(css_wide_keywords[0])
        else:
            initial_value = create_component_list('initial')

        for property_name in shorthand_property_map['mask-border']:
            if property_name not in components_map:
                components_map[property_name] = initial_value.copy()

        updated = self._set_css_declaration_map(components_map, priority)
        return updated

    def tostring(self, property_map):
        keys = list(self._declarations.keys())
        max_index_of_mask_border = -1
        min_index_of_mask_border = -1
        for property_name in shorthand_property_map['mask-border']:
            if property_name not in keys:
                return ''
            index = keys.index(property_name)
            max_index_of_mask_border = max(max_index_of_mask_border, index)
            if min_index_of_mask_border < 0:
                min_index_of_mask_border = index
            else:
                min_index_of_mask_border = min(min_index_of_mask_border, index)

        # in the order of 'mask-border', 'mask'
        for property_name in shorthand_property_map['mask']:
            if property_name not in keys:
                continue
            index = keys.index(property_name)
            if (min_index_of_mask_border < index < max_index_of_mask_border
                    or max_index_of_mask_border < index):
                return ''

        mask_border_source = property_map.get('mask-border-source')
        mask_border_slice = property_map.get('mask-border-slice')
        mask_border_width = property_map.get('mask-border-width')
        mask_border_outset = property_map.get('mask-border-outset')
        mask_border_repeat = property_map.get('mask-border-repeat')
        mask_border_mode = property_map.get('mask-border-mode')
        values = (
            mask_border_source,
            mask_border_slice,
            mask_border_width,
            mask_border_outset,
            mask_border_repeat,
            mask_border_mode,
        )

        if any(x is None for x in values):
            return ''
        elif (all(x in css_wide_keyword_set for x in values)
              and all(x == values[0] for x in values[1:])):
            return values[0]
        elif any(x in css_wide_keyword_set - {'initial'} for x in values):
            return ''
        elif ((mask_border_slice == 'initial'
               and mask_border_width != 'initial')
              or ((mask_border_slice == 'initial'
                   or mask_border_width == 'initial')
                  and mask_border_outset != 'initial')):
            # <mask-border-slice> [ / <mask-border-width>?
            #  [ / <mask-border-outset> ]? ]?
            return ''

        values = list()
        for property_name in shorthand_property_map['mask-border']:
            value = property_map[property_name]
            if value == 'initial':
                continue
            elif (property_name == 'mask-border-width'
                  or property_name == 'mask-border-outset'):
                # <mask-border-slice> [ / <mask-border-width>?
                #  [ / <mask-border-outset> ]? ]?
                values.extend(['/', value])
            else:
                values.append(value)

        s = ' '.join(values)
        return s


class MaskShorthand(ShorthandProperty):

    def set_css_declaration(self, component_list, priority):
        components_map, css_wide_keywords = \
            ShorthandProperty._parse_css_declaration(
                'mask',
                component_list,
                set_initial_value=False)

        mask_origin = components_map.get('mask-origin')
        if mask_origin:
            geometry_box = [x for x in mask_origin if x.type != 'whitespace']
            mask_clip = components_map.get('mask-clip')
            if len(geometry_box) == 1 and mask_clip is None:
                components_map['mask-clip'] = [geometry_box[0]]
            elif len(geometry_box) == 2 and mask_clip is None:
                components_map['mask-origin'] = [geometry_box[0]]
                components_map['mask-clip'] = [geometry_box[1]]
            elif len(geometry_box) >= 2:
                del components_map['mask-origin']

        if len(css_wide_keywords) > 1:
            return False
        elif len(css_wide_keywords) == 1:
            components_map.clear()
            initial_value = create_component_list(css_wide_keywords[0])
        else:
            initial_value = create_component_list('initial')

        for property_name in shorthand_property_map['mask']:
            if property_name not in components_map:
                components_map[property_name] = initial_value.copy()

        updated = self._set_css_declaration_map(components_map, priority)
        return updated

    def tostring(self, property_map):
        declarations = self._declarations
        keys = list(declarations.keys())
        max_index_of_mask = -1
        min_index_of_mask = -1
        for property_name in shorthand_property_map['mask']:
            if property_name not in keys:
                return ''
            index = keys.index(property_name)
            max_index_of_mask = max(max_index_of_mask, index)
            if min_index_of_mask < 0:
                min_index_of_mask = index
            else:
                min_index_of_mask = min(min_index_of_mask, index)

        # in the order of 'mask', 'mask-border'
        for property_name in shorthand_property_map['mask-border']:
            if property_name not in keys:
                continue
            index = keys.index(property_name)
            if (min_index_of_mask < index < max_index_of_mask
                    or (max_index_of_mask < index
                        and declarations[property_name][0] != 'initial')):
                return ''

        mask_image = property_map.get('mask-image')
        mask_position = property_map.get('mask-position')
        mask_size = property_map.get('mask-size')
        mask_repeat = property_map.get('mask-repeat')
        mask_origin = property_map.get('mask-origin')
        mask_clip = property_map.get('mask-clip')
        mask_composite = property_map.get('mask-composite')
        mask_mode = property_map.get('mask-mode')
        values = (
            mask_image,
            mask_position,
            mask_size,
            mask_repeat,
            mask_origin,
            mask_clip,
            mask_composite,
            mask_mode,
        )

        if any(x is None for x in values):
            return ''
        elif any(x in css_wide_keyword_set for x in values):
            if (all(x in css_wide_keyword_set for x in values)
                    and all(x == values[0] for x in values[1:])):
                return values[0]
            elif any(x in css_wide_keyword_set - {'initial'} for x in values):
                return ''
        if mask_position == 'initial' and mask_size != 'initial':
            # <position> [ / <bg-size> ]?
            return ''

        values = list()
        for property_name in shorthand_property_map['mask']:
            value = property_map[property_name]
            if value == 'initial':
                continue
            elif property_name == 'mask-clip' and mask_origin == mask_clip:
                continue
            elif property_name == 'mask-size':
                # <position> [ / <bg-size> ]?
                values.extend(['/', value])
            else:
                values.append(value)

        s = ' '.join(values)
        return s


class OverflowShorthand(ShorthandProperty):

    def set_css_declaration(self, component_list, priority):
        components_map = OrderedDict()
        css_wide_keywords = list()

        ShorthandProperty._parse_component_list(
            'overflow-x',
            component_list,
            components_map,
            css_wide_keywords)

        if len(css_wide_keywords) > 1:
            return False
        elif len(css_wide_keywords) == 1:
            components_map.clear()
            initial_value = create_component_list(css_wide_keywords[0])
            for property_name in shorthand_property_map['overflow']:
                components_map[property_name] = initial_value.copy()
        else:
            temp = [x for x in components_map['overflow-x']
                    if x.type != 'whitespace']
            if not (1 <= len(temp) <= 2):
                return False
            components_map['overflow-x'] = [temp[0]]
            components_map['overflow-y'] = [temp[0] if len(temp) == 1
                                            else temp[1]]

        updated = self._set_css_declaration_map(components_map, priority)
        return updated

    def tostring(self, property_map):
        _ = self
        overflow_x = property_map.get('overflow-x')
        if overflow_x is None:
            return ''

        overflow_y = property_map.get('overflow-y')
        if overflow_y is None:
            return ''
        elif overflow_x == overflow_y:
            return overflow_x
        elif (overflow_x in css_wide_keyword_set
              or overflow_y in css_wide_keyword_set):
            return ''

        s = ' '.join([overflow_x, overflow_y])
        return s


class TextDecorationShorthand(ShorthandProperty):

    def set_css_declaration(self, component_list, priority):
        components_map, css_wide_keywords = \
            ShorthandProperty._parse_css_declaration(
                'text-decoration',
                component_list,
                set_initial_value=False)

        if len(css_wide_keywords) > 1:
            return False
        elif len(css_wide_keywords) == 1:
            components_map.clear()
            initial_value = create_component_list(css_wide_keywords[0])
        else:
            initial_value = create_component_list('initial')

        for property_name in shorthand_property_map['text-decoration']:
            if property_name not in components_map:
                components_map[property_name] = initial_value.copy()

        updated = self._set_css_declaration_map(components_map, priority)
        return updated

    def tostring(self, property_map):
        _ = self
        text_decoration_line = property_map.get('text-decoration-line')
        text_decoration_style = property_map.get('text-decoration-style')
        text_decoration_color = property_map.get('text-decoration-color')
        values = (
            text_decoration_line,
            text_decoration_style,
            text_decoration_color,
        )
        if any(x is None for x in values):
            return ''
        elif (all(x in css_wide_keyword_set for x in values)
              and all(x == values[0] for x in values[1:])):
            return values[0]
        elif any(x in css_wide_keyword_set - {'initial'} for x in values):
            return ''

        s = ' '.join(x for x in values if x != 'initial')
        return s


class WhiteSpaceShorthand(ShorthandProperty):

    def set_css_declaration(self, component_list, priority):
        value = tinycss2.serialize(component_list).strip()
        if value == 'normal':
            text_space_collapse = 'collapse'
            text_wrap = 'wrap'
            text_space_trim = 'none'
        elif value == 'pre':
            text_space_collapse = 'preserve'
            text_wrap = 'nowrap'
            text_space_trim = 'none'
        elif value == 'nowrap':
            text_space_collapse = 'collapse'
            text_wrap = 'nowrap'
            text_space_trim = 'none'
        elif value == 'pre-wrap':
            text_space_collapse = 'preserve'
            text_wrap = 'wrap'
            text_space_trim = 'none'
        elif value == 'pre-line':
            text_space_collapse = 'preserve-breaks'
            text_wrap = 'wrap'
            text_space_trim = 'none'
        elif value.lower() in css_wide_keyword_set:
            text_space_collapse = text_wrap = text_space_trim = value.lower()
        else:
            desc = css_property_descriptor_map['text-space-collapse']
            text_space_collapse = desc.initial_value
            desc = css_property_descriptor_map['text-wrap']
            text_wrap = desc.initial_value
            desc = css_property_descriptor_map['text-space-trim']
            text_space_trim = desc.initial_value

        components_map = OrderedDict()
        components_map['text-space-collapse'] = \
            create_component_list(text_space_collapse)

        components_map['text-wrap'] = \
            create_component_list(text_wrap)

        components_map['text-space-trim'] = \
            create_component_list(text_space_trim)

        updated = self._set_css_declaration_map(components_map, priority)
        return updated

    def tostring(self, property_map):
        _ = self
        text_space_collapse = property_map.get('text-space-collapse')
        text_wrap = property_map.get('text-wrap')
        text_space_trim = property_map.get('text-space-trim')
        values = text_space_collapse, text_wrap, text_space_trim
        if any(x is None for x in values):
            return ''
        elif (text_space_collapse == 'collapse'
              and text_wrap == 'wrap'
              and text_space_trim == 'none'):
            return 'normal'
        elif (text_space_collapse == 'preserve'
              and text_wrap == 'nowrap'
              and text_space_trim == 'none'):
            return 'pre'
        elif (text_space_collapse == 'collapse'
              and text_wrap == 'nowrap'
              and text_space_trim == 'none'):
            return 'nowrap'
        elif (text_space_collapse == 'preserve'
              and text_wrap == 'wrap'
              and text_space_trim == 'none'):
            return 'pre-wrap'
        elif (text_space_collapse == 'preserve-breaks'
              and text_wrap == 'wrap'
              and text_space_trim == 'none'):
            return 'pre-line'
        elif (all(x in css_wide_keyword_set for x in values)
              and all(x == values[0] for x in values[1:])):
            return values[0]
        return ''


_shorthand_property_class_map = {
    'font': FontShorthand,
    'font-synthesis': FontSynthesisShorthand,
    'font-variant': FontVariantShorthand,
    'mask': MaskShorthand,
    'mask-border': MaskBorderShorthand,
    'overflow': OverflowShorthand,
    'text-decoration': TextDecorationShorthand,
    'white-space': WhiteSpaceShorthand,
}

_with_solidus_properties = (
    # 'font': <font-size> [ / <line-height> ]?
    'line-height',
    # 'mask-border': <mask-border-slice> [ / <mask-border-width>?
    'mask-border-width',
    # 'mask-border': <mask-border-width>? [ / <mask-border-outset> ]?
    'mask-border-outset',
)

font_sub_property_list = (
    'font-size-adjust',
    'font-kerning',
    'font-feature-settings',
    'font-language-override',
    'font-min-size',
    'font-max-size',
    'font-optical-sizing',
    'font-variation-settings',
    'font-palette',
)

shorthand_property_map = {
    'font': (
        'font-style',
        'font-variant-css2',
        'font-weight',
        'font-stretch-css3',
        'font-size',
        'line-height',
        'font-family',
    ),
    'font-synthesis': (
        'font-synthesis-weight',
        'font-synthesis-style',
    ),
    'font-variant': (
        'font-variant-ligatures',
        'font-variant-caps',
        'font-variant-alternates',
        'font-variant-numeric',
        'font-variant-east-asian',
        'font-variant-position',
    ),
    'mask': (
        'mask-image',
        'mask-position',
        'mask-size',
        'mask-repeat',
        'mask-origin',
        'mask-clip',
        'mask-composite',
        'mask-mode',
    ),
    'mask-border': (
        'mask-border-source',
        'mask-border-slice',
        'mask-border-width',
        'mask-border-outset',
        'mask-border-repeat',
        'mask-border-mode',
    ),
    'overflow': (
        'overflow-x',
        'overflow-y',
    ),
    'text-decoration': (
        'text-decoration-line',
        'text-decoration-style',
        'text-decoration-color',
    ),
    'white-space': (
        'text-space-collapse',
        'text-wrap',
        'text-space-trim',
    ),
}
