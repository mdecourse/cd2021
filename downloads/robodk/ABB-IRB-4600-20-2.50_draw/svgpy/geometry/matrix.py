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


import math

import numpy as np

from ..formatter import format_number_sequence


def _same_value_zero(x, y):
    if x is None and y is None:
        return True
    elif x is None or y is None:
        return False
    elif not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return False  # SameValueNonNumber(x, y)
    return x == y


def matrix2d(a, b, c, d, e, f):
    """Returns a 2d (4x4) matrix.

    Arguments:
        a (float): The a component of the matrix.
        b (float): The b component of the matrix.
        c (float): The c component of the matrix.
        d (float): The d component of the matrix.
        e (float): The e component of the matrix.
        f (float): The f component of the matrix.
    Returns:
        numpy.array: A 4x4 matrix object.
    """
    return np.array([[float(a), float(c), float(0), float(e)],
                     [float(b), float(d), float(0), float(f)],
                     [float(0), float(0), float(1), float(0)],
                     [float(0), float(0), float(0), float(1)]])


def matrix3d(m11, m12, m13, m14,
             m21, m22, m23, m24,
             m31, m32, m33, m34,
             m41, m42, m43, m44):
    """Returns a 3d (4x4) matrix.

    Arguments:
        m11 (float): The m11 component of the matrix.
        m12 (float): The m12 component of the matrix.
        m13 (float): The m13 component of the matrix.
        m14 (float): The m14 component of the matrix.
        m21 (float): The m21 component of the matrix.
        m22 (float): The m22 component of the matrix.
        m23 (float): The m23 component of the matrix.
        m24 (float): The m24 component of the matrix.
        m31 (float): The m31 component of the matrix.
        m32 (float): The m32 component of the matrix.
        m33 (float): The m33 component of the matrix.
        m34 (float): The m34 component of the matrix.
        m41 (float): The m41 component of the matrix.
        m42 (float): The m42 component of the matrix.
        m43 (float): The m43 component of the matrix.
        m44 (float): The m44 component of the matrix.
    Returns:
        numpy.array: A 4x4 matrix object.
    """
    return np.array([[float(m11), float(m21), float(m31), float(m41)],
                     [float(m12), float(m22), float(m32), float(m42)],
                     [float(m13), float(m23), float(m33), float(m43)],
                     [float(m14), float(m24), float(m34), float(m44)]])


class DOMMatrixReadOnly(object):
    """Represents the [geometry] DOMMatrixReadOnly."""

    def __init__(self, values=None, **init):
        """Constructs a DOMMatrixReadOnly object.

        Arguments:
            values (list[float], optional): A list of elements of the matrix.
            **init (optional): See below.
        Keyword Arguments:
            a (float): The a component of a 2d matrix.
            b (float): The b component of a 2d matrix.
            c (float): The c component of a 2d matrix.
            d (float): The d component of a 2d matrix.
            e (float): The e component of a 2d matrix.
            f (float): The f component of a 2d matrix.
            is2d (bool): A 2d matrix flag.
            m11 (float): The m11 component of a 4x4 matrix.
            m12 (float): The m12 component of a 4x4 matrix.
            m13 (float): The m13 component of a 4x4 matrix.
            m14 (float): The m14 component of a 4x4 matrix.
            m21 (float): The m21 component of a 4x4 matrix.
            m22 (float): The m22 component of a 4x4 matrix.
            m23 (float): The m23 component of a 4x4 matrix.
            m24 (float): The m24 component of a 4x4 matrix.
            m31 (float): The m31 component of a 4x4 matrix.
            m32 (float): The m32 component of a 4x4 matrix.
            m33 (float): The m33 component of a 4x4 matrix.
            m34 (float): The m34 component of a 4x4 matrix.
            m41 (float): The m41 component of a 4x4 matrix.
            m42 (float): The m42 component of a 4x4 matrix.
            m43 (float): The m43 component of a 4x4 matrix.
            m44 (float): The m44 component of a 4x4 matrix.
        Examples:
            >>> m = DOMMatrixReadOnly()
            >>> m.tolist()
            [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
            >>> m = DOMMatrixReadOnly([11, 12, 21, 22, 41, 42])
            >>> m.tolist()
            [11.0, 12.0, 21.0, 22.0, 41.0, 42.0]
            >>> m = DOMMatrixReadOnly(m41=100, m42=-200, is2d=False)
            >>> m.tolist()
            [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 100.0, -200.0, 0.0, 1.0]
        """
        self._matrix = None
        self._is2d = None
        if values is not None:
            self._init_from_array(values)
        else:
            self._init_from_matrix(**init)

    def __eq__(self, other):
        if not isinstance(other, DOMMatrixReadOnly):
            return NotImplemented
        return (self._matrix == other.matrix).all()

    def __imul__(self, other):
        return None

    def __mul__(self, other):
        if not isinstance(other, DOMMatrixReadOnly):
            return NotImplemented
        m = DOMMatrix(self.tolist())
        m.multiply_self(other)
        return m

    def __repr__(self):
        return '<{}.{} object at {} {}>'.format(
            type(self).__module__, type(self).__name__, hex(id(self)),
            self._matrix.tolist())

    @property
    def a(self):
        """float: The a component of the matrix."""
        return self._matrix[0, 0]

    @property
    def b(self):
        """float: The b component of the matrix."""
        return self._matrix[1, 0]

    @property
    def c(self):
        """float: The c component of the matrix."""
        return self._matrix[0, 1]

    @property
    def d(self):
        """float: The d component of the matrix."""
        return self._matrix[1, 1]

    @property
    def e(self):
        """float: The e component of the matrix."""
        return self._matrix[0, 3]

    @property
    def f(self):
        """float: The f component of the matrix."""
        return self._matrix[1, 3]

    @property
    def is2d(self):
        """bool: The 2d matrix flag."""
        return self._is2d

    @property
    def isidentity(self):
        return (self.m11 == 1
                and self.m22 == 1
                and self.m33 == 1
                and self.m44 == 1
                and self.m12 == 0
                and self.m13 == 0
                and self.m14 == 0
                and self.m21 == 0
                and self.m23 == 0
                and self.m24 == 0
                and self.m31 == 0
                and self.m32 == 0
                and self.m34 == 0
                and self.m41 == 0
                and self.m42 == 0
                and self.m43 == 0)

    @property
    def m11(self):
        """float: The m11 component of the matrix."""
        return self._matrix[0, 0]

    @property
    def m12(self):
        """float: The m12 component of the matrix."""
        return self._matrix[1, 0]

    @property
    def m13(self):
        """float: The m13 component of the matrix."""
        return self._matrix[2, 0]

    @property
    def m14(self):
        """float: The m14 component of the matrix."""
        return self._matrix[3, 0]

    @property
    def m21(self):
        """float: The m21 component of the matrix."""
        return self._matrix[0, 1]

    @property
    def m22(self):
        """float: The m22 component of the matrix."""
        return self._matrix[1, 1]

    @property
    def m23(self):
        """float: The m23 component of the matrix."""
        return self._matrix[2, 1]

    @property
    def m24(self):
        """float: The m24 component of the matrix."""
        return self._matrix[3, 1]

    @property
    def m31(self):
        """float: The m31 component of the matrix."""
        return self._matrix[0, 2]

    @property
    def m32(self):
        """float: The m32 component of the matrix."""
        return self._matrix[1, 2]

    @property
    def m33(self):
        """float: The m33 component of the matrix."""
        return self._matrix[2, 2]

    @property
    def m34(self):
        """float: The m34 component of the matrix."""
        return self._matrix[3, 2]

    @property
    def m41(self):
        """float: The m41 component of the matrix."""
        return self._matrix[0, 3]

    @property
    def m42(self):
        """float: The m42 component of the matrix."""
        return self._matrix[1, 3]

    @property
    def m43(self):
        """float: The m43 component of the matrix."""
        return self._matrix[2, 3]

    @property
    def m44(self):
        return self._matrix[3, 3]

    @property
    def matrix(self):
        """numpy.array: The current matrix."""
        return self._matrix

    def _init_from_array(self, values):
        if len(values) == 6:
            self._matrix = matrix2d(*values)
            self._is2d = True
        elif len(values) == 16:
            self._matrix = matrix3d(*values)
            self._is2d = False
        else:
            raise TypeError("'values' required 6 elements for a 2d matrix"
                            " or 16 elements for a 3d matrix")

    def _init_from_matrix(self, **init):
        if len(init) == 0:
            self._matrix = matrix2d(1, 0, 0, 1, 0, 0)
            self._is2d = True
            return
        a = init.pop('a', None)
        m11 = init.pop('m11', None)
        if a is not None and m11 is not None and not _same_value_zero(a, m11):
            raise ValueError("a and m11 are both present,"
                             " but they are not the same")
        b = init.pop('b', None)
        m12 = init.pop('m12', None)
        if b is not None and m12 is not None and not _same_value_zero(b, m12):
            raise ValueError("b and m12 are both present,"
                             " but they are not the same")
        c = init.pop('c', None)
        m21 = init.pop('m21', None)
        if c is not None and m21 is not None and not _same_value_zero(c, m21):
            raise ValueError("c and m21 are both present,"
                             " but they are not the same")
        d = init.pop('d', None)
        m22 = init.pop('m22', None)
        if d is not None and m22 is not None and not _same_value_zero(d, m22):
            raise ValueError("d and m22 are both present,"
                             " but they are not the same")
        e = init.pop('e', None)
        m41 = init.pop('m41', None)
        if e is not None and m41 is not None and not _same_value_zero(e, m41):
            raise ValueError("e and m41 are both present,"
                             " but they are not the same")
        f = init.pop('f', None)
        m42 = init.pop('m42', None)
        if f is not None and m42 is not None and not _same_value_zero(f, m42):
            raise ValueError("f and m42 are both present,"
                             " but they are not the same")
        if m11 is None:
            m11 = a if a is not None else 1
        if m12 is None:
            m12 = b if b is not None else 0
        if m21 is None:
            m21 = c if c is not None else 0
        if m22 is None:
            m22 = d if d is not None else 1
        if m41 is None:
            m41 = e if e is not None else 0
        if m42 is None:
            m42 = f if f is not None else 0
        is2d = init.pop('is2d', None)
        m13 = init.pop('m13', None)
        m14 = init.pop('m14', None)
        m23 = init.pop('m23', None)
        m24 = init.pop('m24', None)
        m31 = init.pop('m31', None)
        m32 = init.pop('m32', None)
        m33 = init.pop('m33', None)
        m34 = init.pop('m34', None)
        m43 = init.pop('m43', None)
        m44 = init.pop('m44', None)
        if len(init) > 0:
            raise TypeError('Invalid keyword argument(s): '
                            + repr(list(init.keys())).strip('[]'))
        if is2d is None:
            if ((m13 is not None and m13 != 0)
                    or (m14 is not None and m14 != 0)
                    or (m23 is not None and m23 != 0)
                    or (m24 is not None and m24 != 0)
                    or (m31 is not None and m31 != 0)
                    or (m32 is not None and m32 != 0)
                    or (m33 is not None and m33 != 1)
                    or (m34 is not None and m34 != 0)
                    or (m43 is not None and m43 != 0)
                    or (m44 is not None and m44 != 1)):
                is2d = False
        elif is2d:
            if ((m13 is not None and m13 != 0)
                    or (m14 is not None and m14 != 0)
                    or (m23 is not None and m23 != 0)
                    or (m24 is not None and m24 != 0)
                    or (m31 is not None and m31 != 0)
                    or (m32 is not None and m32 != 0)
                    or (m33 is not None and m33 != 1)
                    or (m34 is not None and m34 != 0)
                    or (m43 is not None and m43 != 0)
                    or (m44 is not None and m44 != 1)):
                raise ValueError('Invalid keyword argument(s) for a 2d matrix')
        if is2d is None or is2d:
            self._matrix = matrix2d(m11, m12, m21, m22, m41, m42)
            self._is2d = True
        else:
            if m13 is None:
                m13 = 0
            if m14 is None:
                m14 = 0
            if m23 is None:
                m23 = 0
            if m24 is None:
                m24 = 0
            if m31 is None:
                m31 = 0
            if m32 is None:
                m32 = 0
            if m33 is None:
                m33 = 1
            if m34 is None:
                m34 = 0
            if m43 is None:
                m43 = 0
            if m44 is None:
                m44 = 1
            self._matrix = matrix3d(m11, m12, m13, m14,
                                    m21, m22, m23, m24,
                                    m31, m32, m33, m34,
                                    m41, m42, m43, m44)
            self._is2d = False

    def flip_x(self):
        """Post-multiplies the transformation [-1 0 0 1 0 0] on the current
        matrix and returns the resulting matrix.
        The current matrix is not modified.

        Returns:
            DOMMatrix: The resulting matrix.
        """
        m = self * DOMMatrix([-1, 0, 0, 1, 0, 0])
        return m

    def flip_y(self):
        """Post-multiplies the transformation [1 0 0 -1 0 0] on the current
        matrix.
        The current matrix is not modified.

        Returns:
            DOMMatrix: The resulting matrix.
        """
        m = self * DOMMatrix([1, 0, 0, -1, 0, 0])
        return m

    @staticmethod
    def from_float_array(values):
        """Creates a new DOMMatrixReadOnly object from a list of elements of
        the matrix, and returns it.

        Arguments:
            values (list[float]): A list of elements of the matrix.
        Returns:
            DOMMatrixReadOnly: A new DOMMatrixReadOnly object.
        """
        matrix = DOMMatrixReadOnly(values)
        return matrix

    @staticmethod
    def from_matrix(other):
        """Creates a new DOMMatrixReadOnly object from a dictionary other,
        and returns it.

        Arguments:
            other (dict): See DOMMatrixReadOnly.__init__().
        Returns:
            DOMMatrixReadOnly: A new DOMMatrixReadOnly object.
        """
        matrix = DOMMatrixReadOnly(**other)
        return matrix

    def get_angle(self, degrees=True):
        """Returns the rotation angle.

        Arguments:
            degrees (bool, optional): If degrees is True, returns angle in
                degrees; otherwise returns angle in radians.
        Returns:
            float: The rotation angle is in the range of >-180 to <=180 in
                degrees.
        """
        rot_z = math.atan2(self.m12, self.m11)
        if degrees:
            rot_z = math.degrees(rot_z)
        if self._is2d:
            return rot_z
        rot_y = math.atan2(-self.m13,
                           math.sqrt(self.m23 ** 2 + self.m33 ** 2))
        rot_x = math.atan2(self.m23, self.m33)
        if degrees:
            rot_y = math.degrees(rot_y)
            rot_x = math.degrees(rot_x)
        return rot_x, rot_y, rot_z

    def get_scale(self):
        """Returns the scale amounts.

        Returns:
             tuple[float, ...]: The scale amounts.
        """
        m11 = self.m11
        m12 = self.m12
        m13 = self.m13
        m21 = self.m21
        m22 = self.m22
        m23 = self.m23
        sx = math.sqrt(m11 ** 2 + m12 ** 2 + m13 ** 2)
        sy = math.sqrt(m21 ** 2 + m22 ** 2 + m23 ** 2)
        if self._is2d:
            return sx, sy
        m31 = self.m31
        m32 = self.m32
        m33 = self.m33
        sz = math.sqrt(m31 ** 2 + m32 ** 2 + m33 ** 2)
        return sx, sy, sz

    def get_translate(self):
        """Returns the translation amounts.

        Returns:
             tuple[float, ...]: The translation amounts.
        """
        tx = self.m41
        ty = self.m42
        if self._is2d:
            return tx, ty
        tz = self.m43
        return tx, ty, tz

    def inverse(self):
        """Returns the inverse matrix.
        The current matrix is not modified.

        Returns:
            DOMMatrix: The resulting matrix.
        """
        m = DOMMatrix(self.tolist())
        m.invert_self()
        return m

    def multiply(self, other):
        """Post-multiplies the other matrix on the current matrix and returns
        the resulting matrix.
        The current matrix is not modified.

        Arguments:
            other (DOMMatrixReadOnly): A matrix to be multiplied.
        Returns:
            DOMMatrix: The resulting matrix.
        """
        m = self * other
        return m

    def rotate(self, rot_x=0, rot_y=0, rot_z=0):
        """Post-multiplies a rotation transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            rot_x (float, optional): The x-axis rotation angle in degrees.
            rot_y (float, optional): The y-axis rotation angle in degrees.
            rot_z (float, optional): The z-axis rotation angle in degrees.
        Returns:
            DOMMatrix: The resulting matrix.
        """
        m = DOMMatrix(self.tolist())
        m.rotate_self(rot_x, rot_y, rot_z)
        return m

    def rotate_axis_angle(self, x=0, y=0, z=0, angle=0):
        m = DOMMatrix(self.tolist())
        m.rotate_axis_angle_self(x, y, z, angle)
        return m

    def rotate_from_vector(self, x=0, y=0):
        m = DOMMatrix(self.tolist())
        m.rotate_from_vector_self(x, y)
        return m

    def scale(self, scale_x=1, scale_y=None, scale_z=1,
              origin_x=0, origin_y=0, origin_z=0):
        """Post-multiplies a non-uniform scale transformation on the current
        matrix and returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            scale_x (float, optional): The scale amount in X.
            scale_y (float, optional): The scale amount in Y.
            scale_z (float, optional): The scale amount in Z.
            origin_x (float, optional): The translation amount in X.
            origin_y (float, optional): The translation amount in Y.
            origin_z (float, optional): The translation amount in Z.
        Returns:
            DOMMatrix: The resulting matrix.
        """
        m = DOMMatrix(self.tolist())
        m.scale_self(scale_x, scale_y, scale_z, origin_x, origin_y, origin_z)
        return m

    def scale3d(self, scale=1, origin_x=0, origin_y=0, origin_z=0):
        m = DOMMatrix(self.tolist())
        m.scale3d_self(scale, origin_x, origin_y, origin_z)
        return m

    def skew_x(self, angle):
        """Post-multiplies a skewX transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            DOMMatrix: The resulting matrix.
        """
        m = DOMMatrix(self.tolist())
        m.skew_x_self(angle)
        return m

    def skew_y(self, angle):
        """Post-multiplies a skewY transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            DOMMatrix: The resulting matrix.
        """
        m = DOMMatrix(self.tolist())
        m.skew_y_self(angle)
        return m

    def to_float_array(self):
        return [self.m11, self.m12, self.m13, self.m14,
                self.m21, self.m22, self.m23, self.m24,
                self.m31, self.m32, self.m33, self.m34,
                self.m41, self.m42, self.m43, self.m44]

    def tojson(self):
        if self._is2d:
            serialized = {
                'm11': self.m11,
                'm12': self.m12,
                'm21': self.m21,
                'm22': self.m22,
                'm41': self.m41,
                'm42': self.m42,
                'is2d': True,
            }
        else:
            serialized = {
                'm11': self.m11,
                'm12': self.m12,
                'm13': self.m13,
                'm14': self.m14,
                'm21': self.m21,
                'm22': self.m22,
                'm23': self.m23,
                'm24': self.m24,
                'm31': self.m31,
                'm32': self.m32,
                'm33': self.m33,
                'm34': self.m34,
                'm41': self.m41,
                'm42': self.m42,
                'm43': self.m43,
                'm44': self.m44,
                'is2d': False,
            }
        return serialized

    def tolist(self):
        if self._is2d:
            return [self.a, self.b, self.c, self.d, self.e, self.f]
        else:
            return self.to_float_array()

    def tostring(self, delimiter=None):
        if self._is2d:
            name = 'matrix'
        else:
            name = 'matrix3d'
        elements = self.tolist()
        number_sequence = format_number_sequence(elements)
        if delimiter is None or len(delimiter) == 0:
            delimiter = ', '
        return '{}({})'.format(name, delimiter.join(number_sequence))

    def transform_point(self, x, y, z=0, w=1):
        """Post-multiplies the transformation [x y z w] and returns the
        resulting point.

        Arguments:
            x (float): The x-coordinate to transform.
            y (float): The y-coordinate to transform.
            z (float, optional): The z-coordinate to transform.
            w (float, optional): The w-coordinate to transform.
        Returns:
             tuple[float, ...]: The resulting coordinates.
        """
        pt = np.array([[float(x)], [float(y)], [float(z)], [float(w)]])
        pt = np.dot(self._matrix, pt)
        if self._is2d and z == 0 and w == 1:
            return pt.item(0), pt.item(1)
        return pt.item(0), pt.item(1), pt.item(2), pt.item(3)

    def translate(self, tx=0, ty=0, tz=0):
        """Post-multiplies a translation transformation on the current matrix
        and returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            tx (float, optional): The translation amount in X.
            ty (float, optional): The translation amount in Y.
            tz (float, optional): The translation amount in Z.
        Returns:
            DOMMatrix: The resulting matrix.
        """
        m = DOMMatrix(self.tolist())
        m.translate_self(tx, ty, tz)
        return m


class DOMMatrix(DOMMatrixReadOnly):
    # TODO: implement DOMMatrix.setMatrixValue().
    """Represents the [geometry] DOMMatrix."""

    def __init__(self, values=None, **init):
        """Constructs a DOMMatrix object.

        Arguments:
            values (list[float], optional): A list of elements of the matrix.
            **init (optional): See below.
        Keyword Arguments:
            a (float): The a component of a 2d matrix.
            b (float): The b component of a 2d matrix.
            c (float): The c component of a 2d matrix.
            d (float): The d component of a 2d matrix.
            e (float): The e component of a 2d matrix.
            f (float): The f component of a 2d matrix.
            is2d (bool): A 2d matrix flag.
            m11 (float): The m11 component of a 4x4 matrix.
            m12 (float): The m12 component of a 4x4 matrix.
            m13 (float): The m13 component of a 4x4 matrix.
            m14 (float): The m14 component of a 4x4 matrix.
            m21 (float): The m21 component of a 4x4 matrix.
            m22 (float): The m22 component of a 4x4 matrix.
            m23 (float): The m23 component of a 4x4 matrix.
            m24 (float): The m24 component of a 4x4 matrix.
            m31 (float): The m31 component of a 4x4 matrix.
            m32 (float): The m32 component of a 4x4 matrix.
            m33 (float): The m33 component of a 4x4 matrix.
            m34 (float): The m34 component of a 4x4 matrix.
            m41 (float): The m41 component of a 4x4 matrix.
            m42 (float): The m42 component of a 4x4 matrix.
            m43 (float): The m43 component of a 4x4 matrix.
            m44 (float): The m44 component of a 4x4 matrix.
        """
        super().__init__(values, **init)

    def __imul__(self, other):
        if not isinstance(other, DOMMatrixReadOnly):
            return NotImplemented
        self.multiply_self(other)
        return self

    def __repr__(self):
        return '<{}.{} object at {} {}>'.format(
            type(self).__module__, type(self).__name__, hex(id(self)),
            self._matrix.tolist())

    @DOMMatrixReadOnly.a.setter
    def a(self, value):
        self._matrix[0, 0] = float(value)

    @DOMMatrixReadOnly.b.setter
    def b(self, value):
        self._matrix[1, 0] = float(value)

    @DOMMatrixReadOnly.c.setter
    def c(self, value):
        self._matrix[0, 1] = float(value)

    @DOMMatrixReadOnly.d.setter
    def d(self, value):
        self._matrix[1, 1] = float(value)

    @DOMMatrixReadOnly.e.setter
    def e(self, value):
        self._matrix[0, 3] = float(value)

    @DOMMatrixReadOnly.f.setter
    def f(self, value):
        self._matrix[1, 3] = float(value)

    @DOMMatrixReadOnly.m11.setter
    def m11(self, value):
        self._matrix[0, 0] = float(value)

    @DOMMatrixReadOnly.m12.setter
    def m12(self, value):
        self._matrix[1, 0] = float(value)

    @DOMMatrixReadOnly.m13.setter
    def m13(self, value):
        self._matrix[2, 0] = float(value)
        if value:
            self._is2d = False

    @DOMMatrixReadOnly.m14.setter
    def m14(self, value):
        self._matrix[3, 0] = float(value)
        if value:
            self._is2d = False

    @DOMMatrixReadOnly.m21.setter
    def m21(self, value):
        self._matrix[0, 1] = float(value)

    @DOMMatrixReadOnly.m22.setter
    def m22(self, value):
        self._matrix[1, 1] = float(value)

    @DOMMatrixReadOnly.m23.setter
    def m23(self, value):
        self._matrix[2, 1] = float(value)
        if value:
            self._is2d = False

    @DOMMatrixReadOnly.m24.setter
    def m24(self, value):
        self._matrix[3, 1] = float(value)
        if value:
            self._is2d = False

    @DOMMatrixReadOnly.m31.setter
    def m31(self, value):
        self._matrix[0, 2] = float(value)
        if value:
            self._is2d = False

    @DOMMatrixReadOnly.m32.setter
    def m32(self, value):
        self._matrix[1, 2] = float(value)
        if value:
            self._is2d = False

    @DOMMatrixReadOnly.m33.setter
    def m33(self, value):
        self._matrix[2, 2] = float(value)
        if value != 1:
            self._is2d = False

    @DOMMatrixReadOnly.m34.setter
    def m34(self, value):
        self._matrix[3, 2] = float(value)
        if value:
            self._is2d = False

    @DOMMatrixReadOnly.m41.setter
    def m41(self, value):
        self._matrix[0, 3] = float(value)

    @DOMMatrixReadOnly.m42.setter
    def m42(self, value):
        self._matrix[1, 3] = float(value)

    @DOMMatrixReadOnly.m43.setter
    def m43(self, value):
        self._matrix[2, 3] = float(value)
        if value:
            self._is2d = False

    @DOMMatrixReadOnly.m44.setter
    def m44(self, value):
        self._matrix[3, 3] = float(value)
        if value != 1:
            self._is2d = False

    def clear(self, is2d=None):
        """Sets the matrix [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1].

        Arguments:
            is2d (bool, optional): The 2d matrix flag.
        Returns:
            DOMMatrix: Returns itself.
        """
        _is2d = self._is2d if is2d is None else is2d
        self._init_from_array([1, 0, 0, 0,
                               0, 1, 0, 0,
                               0, 0, 1, 0,
                               0, 0, 0, 1])
        self._is2d = _is2d
        return self

    @staticmethod
    def from_float_array(values):
        """Creates a new DOMMatrix object from a list of elements of the
        matrix, and returns it.

        Arguments:
            values (list[float]): A list of elements of the matrix.
        Returns:
            DOMMatrix: A new DOMMatrix object.
        """
        matrix = DOMMatrix(values)
        return matrix

    @staticmethod
    def from_matrix(other):
        """Creates a new DOMMatrix object from a dictionary other, and
        returns it.

        Arguments:
            other (dict): See DOMMatrixReadOnly.__init__().
        Returns:
            DOMMatrix: A new DOMMatrix object.
        """
        matrix = DOMMatrix(**other)
        return matrix

    def invert_self(self):
        """Inverts the current matrix.

        Returns:
            DOMMatrix: Returns itself.
        """
        self._matrix = np.linalg.inv(self._matrix)
        return self

    def multiply_self(self, other):
        """Post-multiplies the other matrix on the current matrix.

        Arguments:
            other (DOMMatrixReadOnly): A matrix to be multiplied.
        Returns:
            DOMMatrix: Returns itself.
        """
        self._matrix = np.dot(self._matrix, other._matrix)
        if not other._is2d:
            self._is2d = False
        return self

    def rotate_axis_angle_self(self, x=0, y=0, z=0, angle=0):
        length = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        if length == 0:
            return self
        elif length != 1:
            x /= length
            y /= length
            z /= length

        t = math.radians(angle)
        sin = math.sin(t)
        cos = math.cos(t)
        if x == 0 and y == 0 and z == 1:
            # [0, 0, 1, rot_z]
            r = matrix3d(cos, sin, 0, 0,
                         -sin, cos, 0, 0,
                         0, 0, 1, 0,
                         0, 0, 0, 1)
        elif x == 0 and y == 1 and z == 0:
            # [0, 1, 0, rot_y]
            r = matrix3d(cos, 0, -sin, 0,
                         0, 1, 0, 0,
                         sin, 0, cos, 0,
                         0, 0, 0, 1)
        elif x == 1 and y == 0 and z == 0:
            # [1, 0, 0, rot_x]
            r = matrix3d(1, 0, 0, 0,
                         0, cos, sin, 0,
                         0, -sin, cos, 0,
                         0, 0, 0, 1)
        else:
            m11 = cos + x ** 2 * (1 - cos)
            m12 = y * x * (1 - cos) + z * sin
            m13 = z * x * (1 - cos) - y * sin
            m14 = 0
            m21 = x * y * (1 - cos) - z * sin
            m22 = cos + y * y * (1 - cos)
            m23 = z * y * (1 - cos) + x * sin
            m24 = 0
            m31 = x * z * (1 - cos) + y * sin
            m32 = y * z * (1 - cos) - x * sin
            m33 = cos + z * z * (1 - cos)
            m34 = 0
            m41 = 0
            m42 = 0
            m43 = 0
            m44 = 1
            r = matrix3d(m11, m12, m13, m14,
                         m21, m22, m23, m24,
                         m31, m32, m33, m34,
                         m41, m42, m43, m44)
        self._matrix = np.dot(self._matrix, r)
        if x != 0 or y != 0:
            self._is2d = False
        return self

    def rotate_from_vector_self(self, x=0, y=0):
        rot_z = math.degrees(math.atan2(y, x))
        return self.rotate_self(rot_z=rot_z)

    def rotate_self(self, rot_x=0, rot_y=0, rot_z=0):
        """Post-multiplies a rotation transformation on the current matrix.

        Arguments:
            rot_x (float, optional): The x-axis rotation angle in degrees.
            rot_y (float, optional): The y-axis rotation angle in degrees.
            rot_z (float, optional): The z-axis rotation angle in degrees.
        Returns:
            DOMMatrix: Returns itself.
        """
        if rot_z != 0:
            self.rotate_axis_angle_self(0, 0, 1, rot_z)

        if rot_y != 0:
            self.rotate_axis_angle_self(0, 1, 0, rot_y)
            self._is2d = False

        if rot_x != 0:
            self.rotate_axis_angle_self(1, 0, 0, rot_x)
            self._is2d = False

        return self

    def scale_self(self, scale_x=1, scale_y=None, scale_z=1,
                   origin_x=0, origin_y=0, origin_z=0):
        """Post-multiplies a non-uniform scale transformation on the current
        matrix.

        Arguments:
            scale_x (float, optional): The scale amount in X.
            scale_y (float, optional): The scale amount in Y.
            scale_z (float, optional): The scale amount in Z.
            origin_x (float, optional): The translation amount in X.
            origin_y (float, optional): The translation amount in Y.
            origin_z (float, optional): The translation amount in Z.
      Returns:
            DOMMatrix: Returns itself.
        """
        if scale_y is None:
            scale_y = scale_x
        if scale_x == 1 and scale_y == 1 and scale_z == 1:
            return self
        if origin_x != 0 or origin_y != 0 or origin_z != 0:
            self.translate_self(origin_x, origin_y, origin_z)
        m = matrix3d(scale_x, 0, 0, 0,
                     0, scale_y, 0, 0,
                     0, 0, scale_z, 0,
                     0, 0, 0, 1)
        self._matrix = np.dot(self._matrix, m)
        if scale_z != 1 or origin_z != 0:
            self._is2d = False
        if origin_x != 0 or origin_y != 0 or origin_z != 0:
            self.translate_self(-origin_x, -origin_y, -origin_z)
        return self

    def scale3d_self(self, scale=1, origin_x=0, origin_y=0, origin_z=0):
        return self.scale_self(scale, scale, scale,
                               origin_x, origin_y, origin_z)

    def skew_x_self(self, angle):
        """Post-multiplies a skewX transformation on the current matrix.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            DOMMatrix: Returns itself.
        """
        m = matrix2d(1, 0, math.tan(math.radians(angle)), 1, 0, 0)
        self._matrix = np.dot(self._matrix, m)
        return self

    def skew_y_self(self, angle):
        """Post-multiplies a skewY transformation on the current matrix.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            DOMMatrix: Returns itself.
        """
        m = matrix2d(1, math.tan(math.radians(angle)), 0, 1, 0, 0)
        self._matrix = np.dot(self._matrix, m)
        return self

    def translate_self(self, tx=0, ty=0, tz=0):
        """Post-multiplies a translation transformation on the current
        matrix.

        Arguments:
            tx (float, optional): The translation amount in X.
            ty (float, optional): The translation amount in Y.
            tz (float, optional): The translation amount in Z.
        Returns:
            DOMMatrix: Returns itself.
        """
        if tx == 0 and ty == 0 and tz == 0:
            return self
        m = matrix3d(1, 0, 0, 0,
                     0, 1, 0, 0,
                     0, 0, 1, 0,
                     tx, ty, tz, 1)
        self._matrix = np.dot(self._matrix, m)
        if tz != 0:
            self._is2d = False
        return self
