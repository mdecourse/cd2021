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


from logging import getLogger

from lxml import cssselect, etree

from .css import CSSParser, CSSRule, CSSStyleSheet
from .utils import normalize_url


_SVG_UA_CSS_STYLESHEET = '''
@namespace url(http://www.w3.org/2000/svg);
@namespace xml url(http://www.w3.org/XML/1998/namespace);

svg|svg:not(:root), svg|hatch, svg|image, svg|marker, svg|pattern, svg|symbol,
svg:not(:root), hatch, image, marker, pattern, symbol { overflow: hidden; }

*:not(svg|svg),
*:not(svg|foreignObject) > svg|svg,
*:not(svg),
*:not(foreignObject) > svg {
  transform-origin: 0 0;
}

*[xml|space=preserve] {
  text-space-collapse: preserve-spaces;
}

svg|defs,
svg|clipPath, svg|mask, svg|marker,
svg|desc, svg|title, svg|metadata,
svg|pattern, svg|hatch,
svg|linearGradient, svg|radialGradient, svg|meshGradient,
svg|script, svg|style,
svg|symbol,
defs,
clipPath, mask, marker,
desc, title, metadata,
pattern, hatch,
linearGradient, radialGradient, meshGradient,
script, style,
symbol {
  display: none !important;
}
:host(svg|use) > svg|symbol,
:host(use) > symbol {
  display: inline !important;
}

/* [fill-stroke-3] */
/* svg:svg:root, *|*:not(svg|*) > svg:svg */
svg|svg:root, 
svg:root {
  fill-color: black;
}

svg|svg, svg {
  fill-origin: content-box;
}
'''

# _OPENTYPE_UA_CSS_STYLESHEET = '''
# @namespace svg url(http://www.w3.org/2000/svg);
#
# svg|text, svg|foreignObject {
#   display: none !important;
# }
# '''

logger = getLogger(__name__)


def flatten_css_rules(element, css_rules):
    doc = element.owner_document
    win = doc.default_view if doc is not None else None
    flattened = list()
    for css_rule in css_rules:
        if css_rule.type == CSSRule.IMPORT_RULE:
            # '@import' at-rule
            media = css_rule.media.media_text
            if media not in ['', 'all']:
                if win is None:
                    logger.debug('no active window: {}'.format(element))
                    continue
                mql = win.match_media(media)
                if not mql.matches:
                    logger.debug('media not matched: media={}'.format(
                        repr(media)))
                    continue
            flattened.extend(
                flatten_css_rules(element, css_rule.style_sheet.css_rules))
        elif css_rule.type == CSSRule.MEDIA_RULE:
            # '@media' at-rule
            media = css_rule.media.media_text
            if media not in ['', 'all']:
                if win is None:
                    logger.debug('no active window: {}'.format(element))
                    continue
                mql = win.match_media(media)
                if not mql.matches:
                    logger.debug('media not matched: media={}'.format(
                        repr(media)))
                    continue
            flattened.extend(
                flatten_css_rules(element, css_rule.css_rules))
        else:
            flattened.append(css_rule)
    return flattened


def get_css_rules(element):
    css_rules = list()
    style_sheets = get_css_style_sheets(element)
    for css_style_sheet in style_sheets:
        css_rules.extend(css_style_sheet.css_rules)
    flattened = flatten_css_rules(element, css_rules)
    return flattened


def get_css_style_sheets(element):
    style_sheets = list()

    # user-agent style sheet
    css_style_sheet = CSSStyleSheet()
    css_style_sheet.insert_rule(_SVG_UA_CSS_STYLESHEET)
    style_sheets.append(css_style_sheet)

    root = element.getroottree().getroot()

    # xml-stylesheet
    style_sheets.extend(get_css_style_sheets_from_xml_stylesheet(root))

    # linked into or embedded stylesheet
    style_sheets.extend(get_css_style_sheets_from_svg_document(root))

    return style_sheets


def get_css_style_sheet_from_element(element, doc=None):
    local_name = element.local_name
    if local_name not in ['link', 'style']:
        raise ValueError(
            'Expected <link> or <style> element, got <{}>'.format(local_name))
    if doc is None:
        doc = element.owner_document
    if doc is not None:
        win = doc.default_view
        base_url = doc.document_uri
    else:
        win = None
        base_url = None

    if local_name == 'link':
        rel_list = element.rel_list
        as_ = element.as_
        if ('alternate' in rel_list
                or ('stylesheet' not in rel_list
                    and not ('preload' in rel_list and as_ == 'style'))
                or ('preload' in rel_list and as_ != 'style')):
            logger.debug('not a style sheet: {} rel={} as={}'.format(
                element, repr(rel_list), repr(as_)))
            return None  # TODO: support alternative style sheet.
        href = element.href
        if href is None or href[0] == '#':
            logger.debug('invalid URL: {} href={}'.format(
                element, repr(href)))
            return None
        media = element.media
        if media not in ['', 'all']:
            if win is None:
                logger.debug('no active window: {}'.format(element))
                return None
            mql = win.match_media(media)
            if not mql.matches:
                logger.debug('media not matched: {} media={}'.format(
                    element, repr(media)))
                return None
        url = normalize_url(href, base_url)
        css_style_sheet = CSSParser.parse(url.href,
                                          owner_node=element)
        return css_style_sheet
    else:  # 'style'
        if element.type != 'text/css' or element.text is None:
            logger.debug(
                'not a style sheet: {} type={} size={}'.format(
                    element,
                    repr(element.type),
                    0 if element.text is None else len(element.text)))
            return None
        media = element.media
        if media not in ['', 'all']:
            if win is None:
                logger.debug('no active window: {}'.format(element))
                return None
            mql = win.match_media(media)
            if not mql.matches:
                logger.debug('media not matched: {} media={}'.format(
                    element, repr(media)))
                return None
        css_style_sheet = CSSStyleSheet(type_=element.type,
                                        owner_node=element,
                                        title=element.title,
                                        media=element.media)
        css_rules = CSSParser.fromstring(element.text,
                                         parent_style_sheet=css_style_sheet)
        css_style_sheet.css_rules.extend(css_rules)
        return css_style_sheet


def get_css_style_sheets_from_svg_document(root):
    style_sheets = list()
    doc = root.owner_document
    for element in root.iter(tag=('{*}link', '{*}style')):
        # FIXME: iterated node's owner_document returns None.
        css_style_sheet = get_css_style_sheet_from_element(element, doc)
        if css_style_sheet is None:
            continue
        style_sheets.append(css_style_sheet)
    return style_sheets


def get_css_style_sheets_from_xml_stylesheet(root):
    style_sheets = list()
    doc = root.owner_document
    if doc is not None:
        win = doc.default_view
        base_url = doc.document_uri
    else:
        win = None
        base_url = None

    # 'lxml.etree.SiblingsIterator' object is not reversible
    siblings = root.itersiblings(preceding=True)
    elements = [it for it in siblings]
    elements.reverse()
    for element in elements:
        if not isinstance(element, etree.PIBase):
            continue
        elif element.target != 'xml-stylesheet':
            continue
        href = element.get('href')
        if (href is None
                or href[0] == '#'
                or element.get('alternate', '') == 'yes'):
            logger.debug('not a style sheet: {}'.format(element))
            continue  # TODO: support alternative style sheet.
        media = element.get('media', '')
        if media not in ['', 'all']:
            if win is None:
                logger.debug('no active window: {}'.format(root))
                continue
            mql = win.match_media(media)
            if not mql.matches:
                logger.debug('media not matched: media={}'.format(
                    repr(media)))
                continue
        encoding = element.get('charset')
        url = normalize_url(href, base_url)
        css_style_sheet = CSSParser.parse(url.href,
                                          owner_node=element,
                                          encoding=encoding)
        style_sheets.append(css_style_sheet)
    return style_sheets


def get_css_style(element, css_rules):
    style = dict()
    style_important = dict()
    namespaces = element.nsmap.copy()
    uri = namespaces.pop(None, None)
    if uri is not None:
        namespaces['svg'] = uri
    for css_rule in css_rules:
        if css_rule.type == CSSRule.STYLE_RULE:
            try:
                selector = cssselect.CSSSelector(css_rule.selector_text,
                                                 namespaces=namespaces)
                matched = selector(element)
                if len(matched) > 0 and element in matched:
                    for key, (value, priority) in css_rule.style.items():
                        style[key] = value
                        if priority == 'important':
                            style_important[key] = value
            except cssselect.ExpressionError as exp:
                logger.info('ExpressionError: {}: \'{}\''.format(
                    exp,
                    css_rule.selector_text))
            except cssselect.SelectorSyntaxError as exp:
                logger.info('SelectorSyntaxError: {}: \'{}\''.format(
                    exp,
                    css_rule.selector_text))
        elif css_rule.type == CSSRule.FONT_FACE_RULE:
            # TODO: support CSS @font-face at-rule.
            pass
        elif css_rule.type == CSSRule.FONT_FEATURE_VALUES_RULE:
            # TODO: support CSS @font-feature-values at-rule.
            pass
        elif css_rule.type == CSSRule.NAMESPACE_RULE:
            if len(css_rule.namespace_uri) > 0:
                prefix = css_rule.prefix
                if len(prefix) == 0:
                    prefix = 'svg'
                namespaces[prefix] = css_rule.namespace_uri
    return style, style_important
