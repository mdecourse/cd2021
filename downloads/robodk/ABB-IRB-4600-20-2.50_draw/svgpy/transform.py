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
import re
from collections.abc import MutableSequence

from .formatter import format_number_sequence
from .geometry.matrix import DOMMatrix, DOMMatrixReadOnly


_RE_TRANSFORM_LIST = re.compile(
    r"(?P<transform>(?P<name>matrix|translate|scale|rotate|skewX|skewY)"
    r"\s*\((?P<values>[^)]+)\))($|\s+|\s*,\s*)")

_RE_NUMBER_SEQUENCE = re.compile(
    r"(?P<number>[+-]?"
    r"((\d+(\.\d*)?([Ee][+-]?\d+)?)|(\d*\.\d+([Ee][+-]?\d+)?)))"
    r"(\s*,\s*|\s+)?")


class SVGTransform(object):
    """Represents the transform function values."""

    SVG_TRANSFORM_UNKNOWN = 0
    SVG_TRANSFORM_MATRIX = 1
    SVG_TRANSFORM_TRANSLATE = 2
    SVG_TRANSFORM_SCALE = 3
    SVG_TRANSFORM_ROTATE = 4
    SVG_TRANSFORM_SKEWX = 5
    SVG_TRANSFORM_SKEWY = 6

    def __init__(self, transform_type=None, *values):
        """Constructs an SVGTransform object.

        Arguments:
            transform_type (int, optional): The type of transform function.
            *values: The values of transform function.
        Examples:
            >>> t = SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, 100, -200)
            >>> t.tostring()
            'translate(100, -200)'
            >>> t.matrix.tolist()
            [1.0, 0.0, 0.0, 1.0, 100.0, -200.0]
        """
        self._transform_type = SVGTransform.SVG_TRANSFORM_UNKNOWN
        self._values = None
        self._angle = 0
        if transform_type is not None:
            self.set(transform_type, *values)

    def __repr__(self):
        return '<{}.{} object at {} {{{}, {}}}>'.format(
            type(self).__module__, type(self).__name__, hex(id(self)),
            self._transform_type, repr(self._values))

    @property
    def angle(self):
        """float: A current angle of a rotate(), skewX() or skewY() function,
        in degrees.
        """
        return self._angle

    @property
    def matrix(self):
        """DOMMatrix: The current matrix or None."""
        if (self._transform_type == SVGTransform.SVG_TRANSFORM_UNKNOWN
                or self._values is None):
            return None
        elif self._transform_type == SVGTransform.SVG_TRANSFORM_MATRIX:
            matrix = DOMMatrix.from_float_array(self._values)
            return matrix
        matrix = DOMMatrix()
        if self._transform_type == SVGTransform.SVG_TRANSFORM_ROTATE:
            angle, cx, cy = self._values
            if cx != 0 or cy != 0:
                matrix.translate_self(cx, cy)
            matrix.rotate_self(rot_z=angle)
            if cx != 0 or cy != 0:
                matrix.translate_self(-cx, -cy)
        elif self._transform_type == SVGTransform.SVG_TRANSFORM_SCALE:
            matrix.scale_self(*self._values)
        elif self._transform_type == SVGTransform.SVG_TRANSFORM_SKEWX:
            matrix.skew_x_self(*self._values)
        elif self._transform_type == SVGTransform.SVG_TRANSFORM_SKEWY:
            matrix.skew_y_self(*self._values)
        elif self._transform_type == SVGTransform.SVG_TRANSFORM_TRANSLATE:
            matrix.translate_self(*self._values)
        else:
            raise NotImplementedError('Unknown transform type: {}'.format(
                self._transform_type))
        return matrix

    @property
    def type(self):
        """int: The type of the transform function."""
        return self._transform_type

    @property
    def values(self):
        """tuple[float, ...]: The values of the transform function."""
        return self._values

    def _set_matrix(self, a, b, c, d, e, f):
        """Sets the transform function value is matrix(a b c d e f).

        Arguments:
            a (float): The a component of the matrix.
            b (float): The b component of the matrix.
            c (float): The c component of the matrix.
            d (float): The d component of the matrix.
            e (float): The e component of the matrix.
            f (float): The f component of the matrix.
        """
        self._transform_type = SVGTransform.SVG_TRANSFORM_MATRIX
        self._values = a, b, c, d, e, f
        self._angle = 0

    @staticmethod
    def from_matrix(matrix):
        """Creates a new SVGTransform initialized with the DOMMatrixReadOnly
        matrix.

        Arguments:
            matrix (DOMMatrixReadOnly): A 2d matrix object.
        Returns:
            SVGTransform: A new SVGTransform object.
        """
        transform = SVGTransform()
        transform.set_matrix(matrix)
        return transform

    def set(self, transform_type, *values):
        if transform_type == SVGTransform.SVG_TRANSFORM_MATRIX:
            self._set_matrix(*values)
        elif transform_type == SVGTransform.SVG_TRANSFORM_ROTATE:
            self.set_rotate(*values)
        elif transform_type == SVGTransform.SVG_TRANSFORM_SCALE:
            self.set_scale(*values)
        elif transform_type == SVGTransform.SVG_TRANSFORM_SKEWX:
            self.set_skew_x(*values)
        elif transform_type == SVGTransform.SVG_TRANSFORM_SKEWY:
            self.set_skew_y(*values)
        elif transform_type == SVGTransform.SVG_TRANSFORM_TRANSLATE:
            self.set_translate(*values)
        elif transform_type == SVGTransform.SVG_TRANSFORM_UNKNOWN:
            self.set_unknown()
        else:
            raise ValueError('Unknown transform type: {}'.format(
                repr(transform_type)))

    def set_matrix(self, matrix):
        """Sets the transform function value is matrix(a, b, c, d, e, f).

        Arguments:
            matrix (DOMMatrixReadOnly): The 2d matrix object.
        """
        if not matrix.is2d:
            raise ValueError('Expected a 2d matrix')
        values = matrix.tolist()
        self._set_matrix(*values)

    def set_rotate(self, angle, cx=0, cy=0):
        """Sets the transform function value is rotate(angle, cx, cy).

        Arguments:
            angle (float): The rotation angle in degrees.
            cx (float): The x-coordinate of center of rotation.
            cy (float): The y-coordinate of center of rotation.
        """
        self._transform_type = SVGTransform.SVG_TRANSFORM_ROTATE
        self._values = angle, cx, cy
        self._angle = angle

    def set_scale(self, sx, sy=None):
        """Sets the transform function value is scale(sx, sy).

        Arguments:
            sx (float): The scale amount in X.
            sy (float): The scale amount in Y.
        """
        if sy is None:
            sy = sx
        self._transform_type = SVGTransform.SVG_TRANSFORM_SCALE
        self._values = sx, sy
        self._angle = 0

    def set_skew_x(self, angle):
        """Sets the transform function value is skewX(angle).

        Arguments:
            angle (float): The skew angle in degrees.
        """
        self._transform_type = SVGTransform.SVG_TRANSFORM_SKEWX
        self._values = (angle,)
        self._angle = angle

    def set_skew_y(self, angle):
        """Sets the transform function value is skewY(angle).

        Arguments:
            angle (float): The skew angle in degrees.
        """
        self._transform_type = SVGTransform.SVG_TRANSFORM_SKEWY
        self._values = (angle,)
        self._angle = angle

    def set_translate(self, tx, ty=0):
        """Sets the transform function value is translate(tx, ty).

        Arguments:
            tx (float): The translation amount in X.
            ty (float): The translation amount in Y.
        """
        self._transform_type = SVGTransform.SVG_TRANSFORM_TRANSLATE
        self._values = tx, ty
        self._angle = 0

    def set_unknown(self):
        self._transform_type = SVGTransform.SVG_TRANSFORM_UNKNOWN
        self._values = None
        self._angle = 0

    def tostring(self, delimiter=None):
        function_name = _FUNCTION_NAME_MAP.get(self._transform_type)
        if function_name is None or self._values is None:
            return ''
        number_sequence = format_number_sequence(self._values)
        if self._transform_type == SVGTransform.SVG_TRANSFORM_ROTATE:
            # "rotate(a 0 0)" -> "rotate(a)"
            if number_sequence[1] == '0' and number_sequence[2] == '0':
                del number_sequence[1:]
        elif self._transform_type == SVGTransform.SVG_TRANSFORM_SCALE:
            # "scale(a a)" -> "scale(a)"
            if number_sequence[0] == number_sequence[1]:
                del number_sequence[1]
        elif self._transform_type == SVGTransform.SVG_TRANSFORM_TRANSLATE:
            # "translate(a 0)" -> "translate(a)"
            if number_sequence[1] == '0':
                del number_sequence[1]
        if delimiter is None or len(delimiter) == 0:
            delimiter = ', '
        return '{0}({1})'.format(function_name,
                                 delimiter.join(number_sequence))


class SVGTransformList(MutableSequence):
    """Represents a list of SVGTransform objects.

    Examples:
        >>> t = SVGTransformList()
        >>> t.append(SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, 9))
        >>> t.append(SVGTransform(SVGTransform.SVG_TRANSFORM_SCALE, 0.33))
        >>> len(t)
        2
        >>> t.tostring()
        'rotate(9) scale(0.33)'
        >>> t.matrix.tostring()
        'matrix(0.325937, 0.051623, -0.051623, 0.325937, 0, 0)'
        >>> t.consolidate()
        >>> len(t)
        1
        >>> t.tostring()
        'matrix(0.325937, 0.051623, -0.051623, 0.325937, 0, 0)'
    """

    def __init__(self, iterable=None):
        """Constructs the transform list.

        Arguments:
            iterable (list[SVGTransform], str, optional): The
                transform list.
        Examples:
            >>> t = SVGTransformList()
            >>> len(t)
            0
            >>> t = SVGTransformList('rotate(9) scale(0.33)')
            >>> len(t)
            2
            >>> t
            ['rotate(9)', 'scale(0.33)']
        """
        self._items = list()
        if iterable is not None:
            if isinstance(iterable, str):
                self.extend(SVGTransformList.parse(iterable))
            else:
                self.extend(iterable)

    def __add__(self, other):
        if not isinstance(other, (SVGTransformList, list, tuple)):
            return NotImplemented
        t = copy.deepcopy(self)
        t.extend(other)
        return t

    def __delitem__(self, index):
        del self._items[index]

    def __getitem__(self, index):
        return self._items[index]

    def __iadd__(self, other):
        if not isinstance(other, (SVGTransformList, list, tuple)):
            return NotImplemented
        self.extend(other)
        return self

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return '[{}]'.format(
            ', '.join(['\'{}\''.format(x.tostring()) for x in self]))

    def __setitem__(self, index, item):
        if isinstance(index, slice):
            if not isinstance(item, (SVGTransformList, list, tuple)):
                raise TypeError('Expected iterable, got {}'.format(
                    type(item)))
            for it in item:
                if not isinstance(it, SVGTransform):
                    raise TypeError('Expected SVGTransform, got {}'.format(
                        type(it)))
        elif not isinstance(item, SVGTransform):
            raise TypeError('Expected SVGTransform, got {}'.format(
                type(item)))
        self._items[index] = item

    @property
    def length(self):
        """int: The number of SVGTransform objects.
        Same as SVGTransformList.number_of_items.
        """
        return self.__len__()

    @property
    def matrix(self):
        """DOMMatrix: The current matrix or None.
        This is a read-only attribute.
        """
        if len(self) == 0:
            return None
        matrix = DOMMatrix()
        for transform in iter(self):
            if not isinstance(transform, SVGTransform):
                raise TypeError('Expected SVGTransform, got {}'.format(
                    type(transform)))
            matrix *= transform.matrix
        return matrix

    @property
    def number_of_items(self):
        """int: The number of SVGTransform objects.
        Same as SVGTransformList.length.
        """
        return self.__len__()

    @property
    def transform(self):
        """SVGTransform: A new SVGTransform object or None."""
        matrix = self.matrix
        if matrix is None:
            return None
        transform = SVGTransform.from_matrix(matrix)
        return transform

    def append(self, item):
        """Adds the SVGTransform object to the end of the transform list.
        Same as SVGTransformList.append_item().

        Arguments:
            item (SVGTransform): The SVGTransform object to be added.
        """
        if not isinstance(item, SVGTransform):
            raise TypeError('Expected SVGTransform, got {}'.format(
                type(item)))
        self._items.append(item)

    def append_item(self, item):
        """Adds the SVGTransform object to the end of the transform list.
        Same as SVGTransformList.append().

        Arguments:
            item (SVGTransform): The SVGTransform object to be added.
        Returns:
            SVGTransform: The SVGTransform object to be added.
        """
        self.append(item)
        return item

    def consolidate(self):
        """Converts the transform list into an equivalent transformation
        using a single transform function and returns it.

        Returns:
            SVGTransform: An SVGTransform object or None.
        """
        if self.__len__() == 0:
            return None
        transform = self.transform
        if transform is None:
            return None
        self.clear()
        self.append(transform)
        return transform

    @staticmethod
    def create_svg_transform_from_matrix(matrix):
        """Creates a new SVGTransform initialized with the DOMMatrixReadOnly
        matrix.

        Arguments:
            matrix (DOMMatrixReadOnly): A 2d matrix object.
        Returns:
            SVGTransform: A new SVGTransform object.
        """
        transform = SVGTransform.from_matrix(matrix)
        return transform

    def get_item(self, index):
        """Gets the SVGTransform object from the transform list at the
        specified position and returns it.

        Arguments:
            index (int): An index position of the transform list.
        Returns:
            SVGTransform: The SVGTransform object.
        """
        return self.__getitem__(index)

    def initialize(self, item):
        """Clears the transform list and adds a single SVGTransform object.

        Arguments:
            item (SVGTransform): The SVGTransform object to be added.
        Returns:
            SVGTransform: The SVGTransform object to be added.
        """
        self.clear()
        self.append(item)
        return item

    def insert(self, index, item):
        """Inserts the SVGTransform object into the transform list at the
        specified position.
        Same as SVGTransformList.insert_item_before().

        Arguments:
            index (int): An index position of the transform list.
            item (SVGTransform): The SVGTransform object to be added.
        """
        if not isinstance(item, SVGTransform):
            raise TypeError('Expected SVGTransform, got {}'.format(
                type(item)))
        self._items.insert(index, item)

    def insert_item_before(self, item, index):
        """Inserts the SVGTransform object into the transform list at the
        specified position.
        Same as SVGTransformList.insert().

        Arguments:
            item (SVGTransform): The SVGTransform object to be added.
            index (int): An index position of the transform list.
        Returns:
            SVGTransform: The SVGTransform object to be added.
        """
        self.insert(index, item)
        return item

    @staticmethod
    def parse(text):
        """Parses a text into a list of SVGTransform objects and returns it.

        Arguments:
            text (str): A text to be parsed.
        Returns:
            SVGTransformList[SVGTransform, ...]: A list of SVGTransform
                objects.
        Examples:
            >>> t = SVGTransformList.parse('translate(50 30) rotate(30)')
            >>> len(t)
            2
            >>> for x in iter(t):
            ...     print(x.tostring())
            ...
            translate(50, 30)
            rotate(30)
        """
        transform_list = SVGTransformList()
        for it in _RE_TRANSFORM_LIST.finditer(text.strip()):
            function_name = it.group('name').strip()
            number_sequence = list()
            for it2 in _RE_NUMBER_SEQUENCE.finditer(
                    it.group('values').strip()):
                number_sequence.append(float(it2.group('number')))
            transform_type = _TRANSFORM_TYPE_MAP.get(
                function_name,
                SVGTransform.SVG_TRANSFORM_UNKNOWN)
            transform_list.append(SVGTransform(transform_type,
                                               *number_sequence))
        return transform_list

    def remove_item(self, index):
        """Removes the SVGTransform object from the transform list.

        Arguments:
            index (int): An index position of the transform list.
        Returns:
            SVGTransform: The SVGTransform object to be removed.
        """
        item = self.__getitem__(index)
        self.__delitem__(index)
        return item

    def replace_item(self, item, index):
        """Replaces an existing SVGTransform object in the transform list with
        the new SVGTransform object.

        Arguments:
            item (SVGTransform): The SVGTransform object to be replaced.
            index (int): An index position of the transform list.
        Returns:
            SVGTransform: The SVGTransform object to be replaced.
        """
        self.__setitem__(index, item)
        return item

    def tostring(self, delimiter=None):
        items = list()
        for transform in iter(self):
            if not isinstance(transform, SVGTransform):
                raise TypeError('Expected SVGTransform, got {}'.format(
                    type(transform)))
            items.append(transform.tostring(delimiter=delimiter))
        return ' '.join(items)


_FUNCTION_NAME_MAP = {
    SVGTransform.SVG_TRANSFORM_MATRIX: 'matrix',
    SVGTransform.SVG_TRANSFORM_TRANSLATE: 'translate',
    SVGTransform.SVG_TRANSFORM_SCALE: 'scale',
    SVGTransform.SVG_TRANSFORM_ROTATE: 'rotate',
    SVGTransform.SVG_TRANSFORM_SKEWX: 'skewX',
    SVGTransform.SVG_TRANSFORM_SKEWY: 'skewY',
}

_TRANSFORM_TYPE_MAP = dict((v, k) for k, v in _FUNCTION_NAME_MAP.items())
