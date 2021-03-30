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


class DOMRectReadOnly(object):
    """Represents the [geometry] DOMRectReadOnly."""

    def __init__(self, x=None, y=None, width=0, height=0):
        """Constructs a DOMRectReadOnly object.

        Arguments:
            x (float, optional): The absolute x-coordinate of the rectangle's
                left edge.
            y (float, optional): The absolute y-coordinate of the rectangle's
                top edge.
            width (float, optional): The width of the rectangle.
            height (float, optional): The height of the rectangle.
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def __and__(self, other):
        if not isinstance(other, DOMRectReadOnly):
            return NotImplemented
        rect = DOMRect(**self.tojson())
        rect.intersect_self(other)
        return rect

    def __eq__(self, other):
        if not isinstance(other, DOMRectReadOnly):
            return NotImplemented
        elif (self.x == other.x
              and self.y == other.y
              and self.width == other.width
              and self.height == other.height):
            return True
        return False

    def __iand__(self, other):
        return None

    def __ior__(self, other):
        return None

    def __or__(self, other):
        if not isinstance(other, DOMRectReadOnly):
            return NotImplemented
        rect = DOMRect(**self.tojson())
        rect.unite_self(other.x, other.y, other.width, other.height)
        return rect

    def __repr__(self):
        return (
            "<{}.{} object at {}"
            " ('x': {}, 'y': {}, 'width': {:g}, 'height': {:g})>".format(
                type(self).__module__, type(self).__name__, hex(id(self)),
                '{:g}'.format(self._x) if isinstance(
                    self._x, (float, int)) else self._x,
                '{:g}'.format(self._y) if isinstance(
                    self._y, (float, int)) else self._y,
                self._width, self._height))

    @property
    def bottom(self):
        """float: The y-coordinate of the rectangle's bottom edge."""
        if self._y is None:
            return None
        return self._y + self._height

    @property
    def height(self):
        """float: The height of the rectangle."""
        return self._height

    @property
    def left(self):
        """float: The x-coordinate of the rectangle's left edge.
        Equivalent to DOMRectReadOnly.x.
        """
        return self._x

    @property
    def right(self):
        """float: The x-coordinate of the rectangle's right edge."""
        if self._x is None:
            return None
        return self._x + self._width

    @property
    def top(self):
        """float: The y-coordinate of the rectangle's top edge.
        Equivalent to DOMRectReadOnly.y.
        """
        return self._y

    @property
    def width(self):
        """float: The width of the rectangle."""
        return self._width

    @property
    def x(self):
        """float: The x-coordinate of the rectangle's left edge.
        Equivalent to DOMRectReadOnly.left.
        """
        return self._x

    @property
    def y(self):
        """float: The y-coordinate of the rectangle's top edge.
        Equivalent to DOMRectReadOnly.top.
        """
        return self._y

    def adjust(self, dx1, dy1, dx2, dy2):
        """Adds dx1, dy1, dx2 and dy2 respectively to the existing coordinates
        of the rectangle.
        The current rectangle is not modified.

        Arguments:
            dx1 (float): The amount to inflate this Rectangle's left edge.
            dy1 (float): The amount to inflate this Rectangle's top edge.
            dx2 (float): The amount to inflate this Rectangle's right edge.
            dy2 (float): The amount to inflate this Rectangle's bottom edge.
        Returns:
            DOMRect: The resulting rectangle.
        """
        rect = DOMRect(**self.tojson())
        rect.adjust_self(dx1, dy1, dx2, dy2)
        return rect

    def contains(self, x, y, width=0, height=0):
        """Returns True if the given point (x, y) or rectangle is inside or on
        the edge of the rectangle; otherwise returns False.
        """
        if not self.isvalid():
            return False
        if width <= 0 or height <= 0:
            if self.left <= x <= self.right and self.top <= y <= self.bottom:
                return True
            return False
        right = x + width
        bottom = y + height
        if (self.left <= x <= self.right
                and self.left <= right <= self.right
                and self.top <= y <= self.bottom
                and self.top <= bottom <= self.bottom):
            return True
        return False

    @staticmethod
    def from_rect(other):
        """Creates a new DOMRectReadOnly object from a dictionary other,
        and returns it.

        Arguments:
            other (dict): See DOMRectReadOnly.__init__().
        Returns:
            DOMRectReadOnly: A new DOMRectReadOnly object.
        """
        rect = DOMRectReadOnly(**other)
        return rect

    def get_coords(self):
        """Returns the position of the rectangle's top-left corner and
        bottom-right corner.

        Returns:
            float: The x-coordinate of the rectangle's left edge.
            float: The y-coordinate of the rectangle's top edge.
            float: The x-coordinate of the rectangle's right edge.
            float: The y-coordinate of the rectangle's bottom edge.
        """
        return self.left, self.top, self.right, self.bottom

    def get_rect(self):
        """Returns the position of the rectangle's top-left corner, width,
        and height.

        Returns:
            float: The x-coordinate of the rectangle's left edge.
            float: The y-coordinate of the rectangle's top edge.
            float: The width of the rectangle.
            float: The height of the rectangle.
        """
        return self.left, self.top, self.width, self.height

    def get_size(self):
        """Returns the size of the rectangle.

        Returns:
            float: The width of the rectangle.
            float: The height of the rectangle.
        """
        return self.width, self.height

    def intersect(self, other):
        """Returns the intersection of this rectangle and the given rectangle.
        The current rectangle is not modified.

        Arguments:
            other (DOMRectReadOnly): A rectangle to be intersected.
        Returns:
            DOMRect: The resulting rectangle.
        """
        rect = DOMRect(**self.tojson())
        rect.intersect_self(other)
        return rect

    def isempty(self):
        """Returns True if the rectangle is empty, otherwise returns False.

        An empty rectangle has a width<=0 or height<=0.
        """
        return (self._x is None
                or self._y is None
                or self._width <= 0
                or self._height <= 0)

    def isvalid(self):
        """Returns True if the rectangle is valid, otherwise returns False.

        A valid rectangle has a width>0 and height>0.
        """
        return (self._x is not None
                and self._y is not None
                and self._width > 0
                and self._height > 0)

    def normalize(self):
        """Returns a normalized rectangle.
        The current rectangle is not modified.

        Returns:
            DOMRect: The resulting rectangle.
        """
        x1, y1, x2, y2 = self.get_coords()
        width, height = self.get_size()
        if width is not None and width < 0:
            x1, x2 = x2, x1
            width = x2 - x1
        if height is not None and height < 0:
            y1, y2 = y2, y1
            height = y2 - y1
        return DOMRect(x1, y1, width, height)

    def tojson(self):
        serialized = {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
        }
        return serialized

    def transform(self, matrix):
        """Returns a copy of the rectangle that is post-multiplied the matrix
        transformation on the current rectangle.

        Arguments:
            matrix (DOMMatrix): A matrix to be multiplied.
        Returns:
            DOMRect: The resulting rectangle.
        """
        rect = DOMRect(**self.tojson())
        rect.transform_self(matrix)
        return rect

    def translate(self, dx, dy):
        """Returns a copy of the rectangle that is translated dx along the
        x-axis and dy along the y-axis, relative to the current position.

        Arguments:
            dx (float): The amount to translate this Rectangle's left edge.
            dy (float): The amount to translate this Rectangle's top edge.
        Returns:
            DOMRect: The resulting rectangle.
        """
        rect = DOMRect(**self.tojson())
        rect.translate_self(dx, dy)
        return rect

    def transpose(self):
        """Returns a copy of the rectangle that has its width and height
        exchanged.

        Returns:
            DOMRect: The resulting rectangle.
        """
        rect = DOMRect(**self.tojson())
        rect.transpose_self()
        return rect

    def unite(self, x, y, width=0, height=0):
        """Returns the bounding rectangle of this rectangle and the given
        rectangle.
        The current rectangle is not modified.

        Arguments:
            x (float): The absolute x-coordinate of the rectangle's left edge.
            y (float): The absolute y-coordinate of the rectangle's top edge.
            width (float, optional): The width of the rectangle.
            height (float, optional): The height of the rectangle.
        Returns:
            DOMRect: The resulting rectangle.
        """
        rect = DOMRect(**self.tojson())
        rect.unite_self(x, y, width, height)
        return rect


class DOMRect(DOMRectReadOnly):
    """Represents the [geometry] DOMRect."""

    def __init__(self, x=None, y=None, width=0, height=0):
        """Constructs a DOMRect object.

        Arguments:
            x (float, optional): The absolute x-coordinate of the rectangle's
                left edge.
            y (float, optional): The absolute y-coordinate of the rectangle's
                top edge.
            width (float, optional): The width of the rectangle.
            height (float, optional): The height of the rectangle.
        """
        super(DOMRect, self).__init__(x, y, width, height)

    def __iand__(self, other):
        if not isinstance(other, DOMRect):
            return NotImplemented
        self.intersect_self(other)
        return self

    def __ior__(self, other):
        if not isinstance(other, DOMRect):
            return NotImplemented
        self.unite_self(other.x, other.y, other.width, other.height)
        return self

    @DOMRectReadOnly.height.setter
    def height(self, height):
        self._height = height

    @DOMRectReadOnly.width.setter
    def width(self, width):
        self._width = width

    @DOMRectReadOnly.x.setter
    def x(self, x):
        self._x = x

    @DOMRectReadOnly.y.setter
    def y(self, y):
        self._y = y

    def adjust_self(self, dx1, dy1, dx2, dy2):
        """Adds dx1, dy1, dx2 and dy2 respectively to the existing coordinates
        of the rectangle.

        Arguments:
            dx1 (float): The amount to inflate this Rectangle's left edge.
            dy1 (float): The amount to inflate this Rectangle's top edge.
            dx2 (float): The amount to inflate this Rectangle's right edge.
            dy2 (float): The amount to inflate this Rectangle's bottom edge.
        Returns:
            DOMRect: Returns itself.
        """
        if not self.isvalid():
            return self
        x1, y1, x2, y2 = self.get_coords()
        x1 += dx1
        y1 += dy1
        x2 += dx2
        y2 += dy2
        self.set_coords(x1, y1, x2, y2)
        return self

    @staticmethod
    def from_rect(other):
        """Creates a new DOMRect object from a dictionary other, and returns
        it.

        Arguments:
            other (dict): See DOMRect.__init__().
        Returns:
            DOMRect: A new DOMRect object.
        """
        rect = DOMRect(**other)
        return rect

    def intersect_self(self, other):
        """Computes the intersection of this rectangle and the given rectangle.

        Arguments:
            other (DOMRectReadOnly): A rectangle to be intersected.
        Returns:
            DOMRect: Returns itself.
        """
        if not isinstance(other, DOMRectReadOnly):
            raise TypeError('Expected DOMRectReadOnly, got {}'.format(
                type(other)))
        elif not self.isvalid() or not other.isvalid():
            return self
        elif other.contains(self.x, self.y, self.width, self.height):
            return self

        x1, y1, x2, y2 = self.get_coords()

        # left-edge
        if (self.left < other.left < self.right
                and ((other.top < self.top and self.bottom < other.bottom)
                     or self.top <= other.top < self.bottom
                     or self.top < other.bottom <= self.bottom)):
            x1 = other.left

        # top-edge
        if (self.top < other.top < self.bottom
                and ((other.left < self.left and self.right < other.right)
                     or self.left <= other.left < self.right
                     or self.left < other.right <= self.right)):
            y1 = other.top

        # right-edge
        if (self.left < other.right < self.right
                and ((other.top < self.top and self.bottom < other.bottom)
                     or self.top <= other.top < self.bottom
                     or self.top < other.bottom <= self.bottom)):
            x2 = other.right

        # bottom-edge
        if (self.top < other.bottom < self.bottom
                and ((other.left < self.left and self.right < other.right)
                     or self.left <= other.left < self.right
                     or self.left < other.right <= self.right)):
            y2 = other.bottom

        self.set_coords(x1, y1, x2, y2)
        return self

    def move_to(self, x, y):
        """Sets the top-left corner of the rectangle to the given position
        (x, y).

        Arguments:
            x (float): The x-coordinate of the rectangle's left edge to be
                moved.
            y (float): The y-coordinate of the rectangle's top edge to be
                moved.
        Returns:
            DOMRect: Returns itself.
        """
        self._x = x
        self._y = y
        return self

    def set_coords(self, x1, y1, x2, y2):
        """Sets the bounds of this rectangle to the specified x1, y1, x2
        and y2.

        Arguments:
            x1 (float): The x-coordinate of the rectangle's left edge.
            y1 (float): The y-coordinate of the rectangle's top edge.
            x2 (float): The x-coordinate of the rectangle's right edge.
            y2 (float): The y-coordinate of the rectangle's bottom edge.
        Returns:
            DOMRect: Returns itself.
        """
        self._x = x1
        self._y = y1
        self._width = x2 - x1
        self._height = y2 - y1
        return self

    def set_rect(self, x, y, width, height):
        """Sets the bounds of this rectangle to the specified x, y, width
        and height.

        Arguments:
            x (float): The absolute x-coordinate of the rectangle's left edge.
            y (float): The absolute y-coordinate of the rectangle's top edge.
            width (float): The width of the rectangle.
            height (float): The height of the rectangle.
        Returns:
            DOMRect: Returns itself.
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        return self

    def set_size(self, width, height):
        """Sets the size of this rectangle to the specified width and height.

        Arguments:
            width (float): The width of the rectangle.
            height (float): The height of the rectangle.
        Returns:
            DOMRect: Returns itself.
        """
        self._width = width
        self._height = height
        return self

    def transform_self(self, matrix):
        """Post-multiplies the matrix transformation on the current rectangle
        and returns the resulting rectangle.

        Arguments:
            matrix (DOMMatrix): A matrix to be multiplied.
        Returns:
            DOMRect: Returns itself.
        """
        if not self.isvalid():
            return self
        # clockwise
        x1, y1, x3, y3 = self.get_coords()
        x2 = x3
        y2 = y1
        x4 = x1
        y4 = y3
        x1, y1 = matrix.transform_point(x1, y1)
        x2, y2 = matrix.transform_point(x2, y2)
        x3, y3 = matrix.transform_point(x3, y3)
        x4, y4 = matrix.transform_point(x4, y4)
        x1 = min(x1, x2, x3, x4)
        y1 = min(y1, y2, y3, y4)
        x3 = max(x1, x2, x3, x4)
        y3 = max(y1, y2, y3, y4)
        self.set_coords(x1, y1, x3, y3)
        return self

    def translate_self(self, dx, dy):
        """Moves the rectangle dx along the x-axis and dy along the y-axis,
        relative to the current position.

        Arguments:
            dx (float): The amount to translate this Rectangle's left edge.
            dy (float): The amount to translate this Rectangle's top edge.
        Returns:
            DOMRect: Returns itself.
        """
        self._x += dx
        self._y += dy
        return self

    def transpose_self(self):
        """Swaps width with height.

        Returns:
            DOMRect: Returns itself.
        """
        self._width, self._height = self._height, self._width
        return self

    def unite_self(self, x, y, width=0, height=0):
        """Computes the bounding rectangle of this rectangle and the given
        rectangle.

        Arguments:
            x (float): The absolute x-coordinate of the rectangle's left edge.
            y (float): The absolute y-coordinate of the rectangle's top edge.
            width (float, optional): The width of the rectangle.
            height (float, optional): The height of the rectangle.
        Returns:
            DOMRect: Returns itself.
        """
        if x is None or y is None:
            return self
        elif self.contains(x, y, width, height):
            return self

        x1, y1, x2, y2 = self.get_coords()

        if x1 is None or x < x1:
            x1 = x
        elif x > x2:
            x2 = x

        if y1 is None or y < y1:
            y1 = y
        elif y > y2:
            y2 = y

        if width > 0 and height > 0:
            right = x + width
            bottom = y + height
            if x2 is None or right > x2:
                x2 = right
            if y2 is None or bottom > y2:
                y2 = bottom

        if x2 is not None and y2 is not None:
            self.set_coords(x1, y1, x2, y2)
        else:
            self._x = x1
            self._y = y1
        return self
