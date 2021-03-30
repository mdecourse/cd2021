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


import pprint
import re
from fractions import Fraction
from logging import getLogger

MEDIA_TYPES = [
    'all', 'print', 'screen', 'speech',
    # deprecated media types
    'tty', 'tv', 'projection', 'handheld', 'braille', 'embossed', 'aural',
]  # case-insensitive

DISCRETE_FEATURES = [
    'orientation', 'scan', 'grid', 'update', 'overflow-block',
    'overflow-inline', 'color-gamut', 'pointer', 'hover', 'any-pointer',
    'any-hover',
]

# See https://drafts.csswg.org/mediaqueries-4/#mq-syntax
_RE_MEDIA_QUERY = re.compile(
    r"(?P<media_not>not\s+\(.+\))"
    r"|(?P<media_in_parens>\(.+\))"
    r"|(?P<media_query>(not\s+|only\s+)?[^ \n\t]+(\s+and\s+(\(.+\))+)?)",
    re.IGNORECASE | re.MULTILINE)

_RE_MEDIA_IN_PARENS = re.compile(
    r"(?P<mf_plain>\(\s*\S+\s*:\s*\S+\s*\))"
    r"|(?P<mf_boolean>\(\s*\S+\s*\))"
    r"|(?P<mf_range>\(\s*[^<> ]+\s*[<>]=?\s*[^<>) ]+\s*"
    r"([<>]=?\s*[^<>) ]+\s*)?\))"
    r"|(?P<media_not>not\s+\(.+\))"
    r"|(?P<media_in_parens>\(.+\))"
    r"|(\s+(?P<op>(and|or))\s+)",
    re.IGNORECASE | re.MULTILINE)

_RE_MF_PLAIN = re.compile(
    r'(\(\s*(?P<mf_name>\S+)\s*:\s*(?P<mf_value>\S+)\s*\))',
    re.MULTILINE)

_RE_MF_RANGE = re.compile(
    r"(\(\s*(?P<left>[^<> ]+)\s*(?P<op>[<>]=?)\s*(?P<right>[^<>) ]+)\s*"
    r"((?P<op2>[<>]=?)\s*(?P<right2>[^<>) ]+)\s*)?\))",
    re.MULTILINE)

_RE_WHITESPACE = re.compile(r'\s+', re.MULTILINE)

_RE_NUMBER = re.compile(
    r'(^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+)?)',
    re.MULTILINE)

MQ_EXPR = 'expr'
MQ_EXPR_COMPARE = 'Compare'
MQ_EXPR_NAME = 'Name'
MQ_EXPR_NUM = 'Num'
MQ_EXPR_BOOL_OP = 'BoolOp'
MQ_EXPR_UNARY_OP = 'UnaryOp'
MQ_OP = 'op'
MQ_OPS = 'ops'
MQ_OPERAND = 'operand'
MQ_COMPARATORS = 'comparators'
MQ_VALUES = 'values'
MQ_ID = 'id'
MQ_LEFT = 'left'
MQ_NUM = 'n'

logger = getLogger(__name__)


def parse(query):
    node_list = list()
    media_query_list = query.strip().lower().split(',')
    for media_query in media_query_list:
        media_query = media_query.strip()
        if len(media_query) == 0:
            continue
        node = dict()
        _parse_media_query(media_query, node)
        node_list.append(node)
    return node_list


def dump(node_list, **kwargs):
    pprint.pprint(node_list, **kwargs)


def match(node_list, conditions, compare_func, user_data=None):
    logger.debug('id={}: start'.format(hex(id(node_list))))
    matched_media = None
    for node in node_list:
        logger.debug('id={}: node={}'.format(hex(id(node_list)), repr(node)))
        result, media = _match_node(node, conditions, compare_func,
                                    user_data=user_data)
        if result and media and matched_media is None:
            matched_media = media
        if result:
            logger.debug('id={}: matched media={}'.format(
                hex(id(node_list)), repr(matched_media)))
            return True, matched_media
    logger.debug('id={}: unmatched'.format(hex(id(node_list))))
    return False, matched_media


def _match_node(node, conditions, compare_func, not_op=False, user_data=None):
    expr = node[MQ_EXPR]
    op = node.get(MQ_OP, 'or')
    if expr == MQ_EXPR_UNARY_OP:
        # <media-not>
        child = node[MQ_OPERAND]
        result, media = _match_node(child, conditions, compare_func,
                                    not_op=True, user_data=user_data)
        return not result, media
    assert expr == MQ_EXPR_BOOL_OP
    ops = node.get(MQ_OPS, [])
    if len(ops) > 0 and ops.count('and') > 0 and ops.count('or') > 0:
        return False, None
    result = True
    matched_media = None
    children = node[MQ_VALUES]
    for child in children:
        expr = child[MQ_EXPR]
        if expr == MQ_EXPR_NAME:
            # <media-type> | <mf-boolean>
            result, media = _eval_expr_name(child, conditions)
            if result and media and matched_media is None:
                matched_media = media
        elif expr == MQ_EXPR_COMPARE:
            # <mf-plain> | <mf-range>
            result, media = _eval_expr_compare(child, conditions, compare_func,
                                               user_data)
            if result and media and matched_media is None:
                matched_media = media
        elif expr == MQ_EXPR_UNARY_OP:
            # <media-not>
            result, media = _match_node(child, conditions, compare_func,
                                        not_op=True, user_data=user_data)
            if result and media and matched_media is None:
                matched_media = media
        else:
            raise NotImplementedError('Unexpected value: ' + repr(expr))
        if ((op == 'and' and (not not_op) and not result)
                or (op == 'and' and not_op and result)
                or (op == 'or' and (not not_op) and result)
                or (op == 'or' and not_op and not result)):
            # (False) and (...)
            # not ((...) and (...)) -> (True) or (...)
            # (True) or (...)
            # not ((...) or (...)) -> (False) and (...)
            break
    return result, matched_media


def _eval_expr_compare(node, conditions, compare_func, user_data=None):
    # <mf-range>
    left = node[MQ_LEFT]
    left_expr = left[MQ_EXPR]
    name = None
    if left_expr == MQ_EXPR_NUM:
        left_value = left[MQ_NUM]
    else:
        name = left[MQ_ID]
        left_value = conditions.get(name)
        if left_value is None:
            logger.debug('feature \'{}\': missing value'.format(name))
            return False, None
    for right, op in zip(node[MQ_COMPARATORS], node[MQ_OPS]):
        right_expr = right[MQ_EXPR]
        if right_expr == MQ_EXPR_NUM:
            right_value = right[MQ_NUM]
        else:
            name = right[MQ_ID]
            right_value = conditions.get(name)
            if right_value is None:
                return False, None
        if ((left_expr == MQ_EXPR_NAME or right_expr == MQ_EXPR_NAME)
                and name != 'grid'
                and name in DISCRETE_FEATURES):
            # value type: discrete
            # e.g.: '(orientation: portrait)' -> '(orientation == portrait)'
            # FIXME: '(min-grid: 1)' to invalidate.
            if name == 'orientation':
                if '-' in left_value and '-' not in right_value:
                    left_value = left_value.split('-')[0]
                elif '-' not in left_value and '-' in right_value:
                    right_value = right_value.split('-')[0]
            if op[-1] != '=' or left_value != right_value:
                result = False
            else:
                result = True
            logger.debug('feature \'{}\': {} {} {}: result={}'.format(
                name, repr(left_value), op, repr(right_value), result))
            if not result:
                return False, None
        elif ((left_expr == MQ_EXPR_NAME or right_expr == MQ_EXPR_NAME)
              and name == 'aspect-ratio'):
            # value: <ratio>
            # e.g.: '(aspect-ratio: 16/9)' -> '(aspect-ratio == 16/9)'
            left_ratio = Fraction(left_value)
            right_ratio = Fraction(right_value)
            if op[-1] == '=' and left_ratio == right_ratio:
                logger.debug('feature \'{}\': {} {} {}: result={}'.format(
                    name, repr(left_ratio), op, repr(right_ratio), True))
            else:
                cmp = left_ratio > right_ratio
                logger.debug('feature \'{}\': {} {} {}: result={}'.format(
                    name, repr(left_ratio), op, repr(right_ratio), cmp))
                if (op[0] == '>' and not cmp) or (op[0] == '<' and cmp):
                    return False, None
        else:
            # value: <length> | <resolution> | <mq-boolean> | <integer>
            # e.g.: '(1 < color-index < 255)' ->
            # '(1 < color-index)' and '(color-index < 255)'
            try:
                cmp = compare_func(left_value, right_value, user_data)
                logger.debug('feature \'{}\': {} {} {}: result={}'.format(
                    name, repr(left_value), op, repr(right_value), cmp))
            except ValueError as exp:
                logger.debug('feature \'{}\': {} {} {}: exception={}'.format(
                    name, repr(left_value), op, repr(right_value), repr(exp)))
                return False, None
            if ((cmp == 0 and op[-1] == '=')
                    or (cmp > 0 and op[0] == '>')
                    or (cmp < 0 and op[0] == '<')):
                pass  # ok
            else:
                return False, None
        left_expr = right_expr
        left_value = right_value
    return True, None


def _eval_expr_name(node, conditions):
    result = False
    matched_media = None
    name = node[MQ_ID]
    if name in MEDIA_TYPES:
        # <media-type>
        if name == 'all' or conditions.get('media', '') == name:
            result = True
            matched_media = name
        logger.debug('media \'{}\': result={}'.format(name, result))
    else:
        # <mf-boolean>
        if name in DISCRETE_FEATURES:
            if name in ['orientation', 'scan', 'color-gamut']:
                result = name in conditions
            elif name == 'grid':
                result = int(conditions.get(name, 0)) == 1  # 0 or 1
            else:
                result = conditions.get(name, 'none') != 'none'
        elif name in ['color', 'color-index', 'monochrome']:
            result = conditions.get(name, 0) > 0
        else:
            result = name in conditions
        logger.debug('feature \'{}\': {}: result={}'.format(
            name, repr(conditions.get(name)), result))
    return result, matched_media


def _parse_media_query(query, parent):
    for it in _RE_MEDIA_QUERY.finditer(query):
        # <media-not>
        media_not = it.group('media_not')
        if media_not:
            _parse_media_not(media_not, parent)

        # <media-in-parens>
        media_in_parens = it.group('media_in_parens')
        if media_in_parens:
            _parse_media_in_parens(media_in_parens, parent)

        # <media-query>
        media_query = it.group('media_query')
        if media_query:
            start = 0
            for it_media_query in _RE_WHITESPACE.finditer(media_query):
                limit, end = it_media_query.span()
                segment = media_query[start:limit]
                if segment == 'only':
                    pass  # skip
                elif segment == 'not':
                    node = dict({
                        MQ_EXPR: MQ_EXPR_BOOL_OP,
                        MQ_VALUES: [],
                    })
                    parent[MQ_EXPR] = MQ_EXPR_UNARY_OP
                    parent[MQ_OP] = segment
                    parent[MQ_OPERAND] = node
                elif segment in ['and', 'or']:
                    expr = parent.get(MQ_EXPR)
                    if expr is None:
                        # invalid grammar: treat as media type
                        # e.g.: 'or and (color)'
                        _parse_media_type(segment, parent)
                    else:
                        if expr == MQ_EXPR_UNARY_OP:
                            node = parent[MQ_OPERAND]
                            ops = node.setdefault(MQ_OPS, [])
                            ops.append(segment)
                        else:
                            node = parent
                        op = node.get(MQ_OP)
                        if op is None:
                            node[MQ_OP] = segment
                else:
                    if not segment.startswith('('):
                        # <media-type>
                        _parse_media_type(segment, parent)
                    else:
                        # <media-condition-without-or>
                        remain = media_query[start:]
                        _parse_media_query(remain, parent)
                        break
                start = end
            else:
                remain = media_query[start:]
                if media_query[start] == '(':
                    # <media-query>
                    _parse_media_query(remain, parent)
                else:
                    # <media-type>
                    _parse_media_type(remain, parent)
            break
    return parent


def _parse_media_type(query, parent):
    # <media-type>
    node = dict({
        MQ_EXPR: MQ_EXPR_NAME,
        MQ_ID: query,
    })
    expr = parent.setdefault(MQ_EXPR, MQ_EXPR_BOOL_OP)
    if expr == MQ_EXPR_UNARY_OP:
        operand = parent[MQ_OPERAND]
        values = operand[MQ_VALUES]
    else:
        values = parent.setdefault(MQ_VALUES, [])
    values.append(node)
    return parent


def _parse_media_not(query, parent):
    node = dict({
        MQ_EXPR: MQ_EXPR_BOOL_OP,
        MQ_VALUES: [],
    })
    parent[MQ_EXPR] = MQ_EXPR_UNARY_OP
    parent[MQ_OP] = 'not'
    parent[MQ_OPERAND] = node
    matched = _RE_WHITESPACE.search(query)
    remain = query[matched.end(0):]
    _parse_media_query(remain, parent)
    return parent


def _parse_media_in_parens(query, parent):
    expr = parent.setdefault(MQ_EXPR, MQ_EXPR_BOOL_OP)
    if expr == MQ_EXPR_UNARY_OP:
        node = parent[MQ_OPERAND]
    else:
        node = parent
    node.setdefault(MQ_OPS, [])
    for it in _RE_MEDIA_IN_PARENS.finditer(query):
        # <mf-plain>
        mf_plain = it.group('mf_plain')
        if mf_plain:
            _parse_mf_plain(mf_plain, parent)

        # <mf-boolean>
        mf_boolean = it.group('mf_boolean')
        if mf_boolean:
            _parse_mf_boolean(mf_boolean, parent)

        # <mf-range>
        mf_range = it.group('mf_range')
        if mf_range:
            _parse_mf_range(mf_range, parent)

        # <media-not>
        media_not = it.group('media_not')
        if media_not:
            _parse_media_not(media_not, parent)

        # and | or
        op = it.group('op')
        if op:
            if node.get(MQ_OP) is None:
                node[MQ_OP] = op
            node[MQ_OPS].append(op)
    return parent


def _parse_mf_boolean(query, parent):
    # e.g.: '(color)'
    expr = parent.setdefault(MQ_EXPR, MQ_EXPR_BOOL_OP)
    if expr == MQ_EXPR_UNARY_OP:
        operand = parent[MQ_OPERAND]
        values = operand[MQ_VALUES]
    else:
        values = parent.setdefault(MQ_VALUES, [])
    node = dict({
        MQ_EXPR: MQ_EXPR_NAME,
        MQ_ID: query.strip('()'),
    })
    values.append(node)
    return node


def _parse_mf_plain(query, parent):
    # e.g.: '(min-height: 600px)'
    expr = parent.setdefault(MQ_EXPR, MQ_EXPR_BOOL_OP)
    if expr == MQ_EXPR_UNARY_OP:
        operand = parent[MQ_OPERAND]
        values = operand[MQ_VALUES]
    else:
        values = parent.setdefault(MQ_VALUES, [])
    node = dict({
        MQ_EXPR: MQ_EXPR_COMPARE,
        MQ_OPS: [],
        MQ_COMPARATORS: [],
    })
    values.append(node)
    matched = _RE_MF_PLAIN.match(query)
    mf_name = matched.group('mf_name')
    mf_value = matched.group('mf_value')
    if ((mf_name.startswith('max-') or mf_name.startswith('min-'))
            and mf_name[4:] in DISCRETE_FEATURES):
        op = '=='
    else:
        if mf_name.startswith('max-'):
            op = '<='
            mf_name = mf_name[4:]
        elif mf_name.startswith('min-'):
            op = '>='
            mf_name = mf_name[4:]
        else:
            op = '=='
    node[MQ_OPS].append(op)
    node[MQ_LEFT] = dict({
        MQ_EXPR: MQ_EXPR_NAME,
        MQ_ID: mf_name,
    })
    node[MQ_COMPARATORS].append(dict({
        MQ_EXPR: MQ_EXPR_NUM,
        MQ_NUM: mf_value,
    }))
    return node


def _parse_mf_range(query, parent):
    # e.g.: '(height >= 600px)', '(400px <= width <= 700px)'
    expr = parent.setdefault(MQ_EXPR, MQ_EXPR_BOOL_OP)
    if expr == MQ_EXPR_UNARY_OP:
        operand = parent[MQ_OPERAND]
        values = operand[MQ_VALUES]
    else:
        values = parent.setdefault(MQ_VALUES, [])
    node = dict({
        MQ_EXPR: MQ_EXPR_COMPARE,
        MQ_OPS: [],
        MQ_COMPARATORS: [],
    })
    values.append(node)
    matched = _RE_MF_RANGE.match(query)
    left_value = matched.group('left')
    right_value = matched.group('right')
    op = matched.group('op')
    node[MQ_OPS].append(op)
    if _RE_NUMBER.match(left_value):
        left = dict({
            MQ_EXPR: MQ_EXPR_NUM,
            MQ_NUM: left_value,
        })
    else:
        left = dict({
            MQ_EXPR: MQ_EXPR_NAME,
            MQ_ID: left_value,
        })
    if _RE_NUMBER.match(right_value):
        right = dict({
            MQ_EXPR: MQ_EXPR_NUM,
            MQ_NUM: right_value,
        })
    else:
        right = dict({
            MQ_EXPR: MQ_EXPR_NAME,
            MQ_ID: right_value,
        })
    node[MQ_LEFT] = left
    node[MQ_COMPARATORS].append(right)

    right_value = matched.group('right2')
    if right_value:
        op = matched.group('op2')
        node[MQ_OPS].append(op)
        if _RE_NUMBER.match(right_value):
            right = dict({
                MQ_EXPR: MQ_EXPR_NUM,
                MQ_NUM: right_value,
            })
        else:
            right = dict({
                MQ_EXPR: MQ_EXPR_NAME,
                MQ_ID: right_value,
            })
        node[MQ_COMPARATORS].append(right)
    return node
