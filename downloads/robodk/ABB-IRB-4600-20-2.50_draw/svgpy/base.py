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


from abc import abstractmethod

from .core import SVGLength
from .css.screen import Screen
from .dom import DOMStringMap, Element, ElementCSSInlineStyle
from .formatter import format_coordinate_pair_sequence, \
    to_coordinate_pair_sequence
from .geometry.matrix import DOMMatrix
from .geometry.rect import DOMRect
from .path import PathParser
from .transform import SVGTransformList
from .utils import QualifiedName


class HTMLOrSVGElement(Element):
    """Represents the [HTML] HTMLOrSVGElement."""

    def _init(self):
        super()._init()
        self._dataset = DOMStringMap(self, 'data-')

    @property
    def dataset(self):
        """DOMStringMap: A DOMStringMap object for the element's data-*
        attributes.

        Examples:
            >>> parser = SVGParser()
            >>> root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
            >>> root.dataset['foo'] = 'foo'
            >>> root.dataset['fooBar'] = 'foo-bar'
            >>> root.dataset
            {'foo': 'foo', 'fooBar': 'foo-bar'}
            >>> root.attributes
            {'data-foo': 'foo', 'data-foo-bar': 'foo-bar'}
            >>> root.tostring()
            b'<svg xmlns="http://www.w3.org/2000/svg" data-foo="foo" data-foo-bar="foo-bar"/>'
        """
        return self._dataset


class HTMLElement(ElementCSSInlineStyle, HTMLOrSVGElement):
    """Represents the [HTML] HTMLElement."""

    @property
    def lang(self):
        """str: The lang content attribute in no namespace."""
        return self.get('lang', '')

    @lang.setter
    def lang(self, value):
        self.set('lang', value)

    @property
    def title(self):
        """str: The title of the link, or the CSS style sheet set name."""
        return self.get('title', '')

    @title.setter
    def title(self, value):
        self.set('title', value)


class HTMLHyperlinkElementUtils(object):
    """Represents the [HTML] HTMLHyperlinkElementUtils."""
    # TODO: implement the HTMLHyperlinkElementUtils.
    pass


class HTMLMediaElement(HTMLElement):
    """Represents the [HTML] HTMLMediaElement."""
    pass


class SVGAnimatedPoints(Element):
    """Represents the [SVG2] SVGAnimatedPoints."""

    @property
    def points(self):
        """list[tuple[float, float]]: A list of coordinates pair.

        Examples:
            >>> parser = SVGParser()
            >>> polygon = parser.create_element_ns('http://www.w3.org/2000/svg', 'polygon')
            >>> polygon.set('points', '100,300 300,300 200,100')
            >>> polygon.points
            [(100.0, 300.0), (300.0, 300.0), (200.0, 100.0)]
            >>> polygon.points = [(100, 100), (300, 100), (200, 300)]
            >>> polygon.get('points')
            '100,100 300,100 200,300'
        """
        # 'points' property
        # Value: <points>
        # <points> = [ <number>+ ]#
        # Initial value: (none)
        points = self.get('points')
        if points is None:
            return []
        number_sequence = list()
        for it in PathParser.RE_NUMBER_SEQUENCE.finditer(points.strip()):
            number = it.group('number')
            number_sequence.append(float(number))
        if len(number_sequence) % 2 != 0:
            return []  # an odd number of coordinates
        return to_coordinate_pair_sequence(number_sequence)

    @points.setter
    def points(self, points):
        value = format_coordinate_pair_sequence(points)
        self.set('points', value)


class SVGBoundingBoxOptions(object):
    """Represents the [SVG2] SVGBoundingBoxOptions."""

    def __init__(self):
        self.fill = True
        self.stroke = False
        self.markers = False
        self.clipped = False


class SVGElement(ElementCSSInlineStyle, HTMLOrSVGElement):
    """Represents the [SVG2] SVGElement."""

    NEAREST_VIEWPORT = 0
    FARTHEST_VIEWPORT = 1

    @property
    def owner_svg_element(self):
        """SVGSVGElement: The nearest ancestor 'svg' element. If the current
        element is outer most 'svg' element, then returns None.
        """
        farthest = self.get_farthest_svg_element()
        if farthest is not None and hash(farthest) == hash(self):
            return None
        nearest = self.get_nearest_svg_element()
        return nearest

    @property
    def viewport_element(self):
        """SVGElement: The nearest ancestor element that establishes an SVG
        viewport. If the current element is outer most 'svg' element, then
        returns None.
        """
        farthest = self.get_farthest_svg_element()
        if farthest is not None and hash(farthest) == hash(self):
            return None
        nearest = self.get_nearest_viewport_element()
        return nearest

    def get_farthest_svg_element(self):
        """Returns the outermost 'svg' element.

        Returns:
            SVGSVGElement: The outermost 'svg' element.
        """
        root = None
        element = self
        while element is not None:
            if element.local_name == 'svg':
                root = element
            element = element.getparent()
        return root

    def get_farthest_viewport_element(self):
        root = None
        element = self
        while element is not None:
            if element.local_name in ('svg', 'symbol'):
                root = element
            element = element.getparent()
        return root

    def get_nearest_svg_element(self):
        element = self
        while element is not None:
            if element.local_name == 'svg':
                return element
            element = element.getparent()
        return None

    def get_nearest_viewport_element(self):
        element = self
        while element is not None:
            if element.local_name in ('svg', 'symbol'):
                return element
            element = element.getparent()
        return None

    def get_view_box(self, recursive=True):
        """Gets values of the 'viewBox' and 'preserveAspectRatio' attributes
        from nearest ancestor element that establishes an SVG viewport.

        Returns:
            tuple[SVGLength, SVGLength, SVGLength, SVGLength,
            SVGPreserveAspectRatio]: Returns a tuple of four numbers <min-x>,
            <min-y>, <width>, <height> and <preserveAspectRatio>.
        """
        element = self
        while element is not None:
            root = element.get_nearest_viewport_element()
            if root is None:
                return None
            assert isinstance(root, SVGFitToViewBox)
            view_box = root.view_box
            if view_box is not None:
                vbx, vby, vbw, vbh = view_box
                par = root.preserve_aspect_ratio
                return vbx, vby, vbw, vbh, par
            if not recursive:
                return None
            element = root.getparent()
        return None

    def get_viewport_size(self, recursive=True):
        """Gets the SVG viewport size from nearest ancestor element that
        establishes an SVG viewport.

        Returns:
            tuple[SVGLength, SVGLength, SVGLength, SVGLength]: Returns a tuple
            of four numbers <min-x>, <min-y>, <width>, and <height>.
        """
        # See https://svgwg.org/svg2-draft/coords.html#Units
        element = self
        roots = list()
        while element is not None:
            root = element.get_nearest_viewport_element()
            if root is None:
                break
            roots.insert(0, root)
            if not recursive:
                break
            element = root.getparent()

        win = (self.owner_document.default_view
               if self.owner_document is not None
               else None)
        if win is None:
            initial_viewport_width = Screen.DEFAULT_SCREEN_WIDTH
            initial_viewport_height = Screen.DEFAULT_SCREEN_HEIGHT
        else:
            initial_viewport_width = win.inner_width
            initial_viewport_height = win.inner_height
        parent_vpw = vpw = SVGLength(initial_viewport_width,
                                     direction=SVGLength.DIRECTION_HORIZONTAL)
        parent_vph = vph = SVGLength(initial_viewport_height,
                                     direction=SVGLength.DIRECTION_VERTICAL)
        for root in roots:
            _width = root.get('width', 'auto')
            if _width == 'auto':
                _width = '100%'
            if _width == 'inherit':
                vpw = parent_vpw
            else:
                vpw = SVGLength(_width,
                                context=root,
                                direction=SVGLength.DIRECTION_HORIZONTAL)
                unit = vpw.unit
                if unit in (SVGLength.TYPE_PERCENTAGE, SVGLength.TYPE_VW):
                    vpw = vpw.value(SVGLength.TYPE_PERCENTAGE) / 100 \
                          * parent_vpw
                elif unit == SVGLength.TYPE_VH:
                    vpw = vpw.value(SVGLength.TYPE_PERCENTAGE) / 100 \
                          * parent_vph
                elif unit == SVGLength.TYPE_VMAX:
                    vpw = max(parent_vpw, parent_vph)
                elif unit == SVGLength.TYPE_VMIN:
                    vpw = min(parent_vpw, parent_vph)
            parent_vpw = vpw

            _height = root.get('height', 'auto')
            if _height == 'auto':
                _height = '100%'
            if _height == 'inherit':
                vph = parent_vph
            else:
                vph = SVGLength(_height,
                                context=root,
                                direction=SVGLength.DIRECTION_VERTICAL)
                unit = vph.unit
                if unit in (SVGLength.TYPE_PERCENTAGE, SVGLength.TYPE_VH):
                    vph = vph.value(SVGLength.TYPE_PERCENTAGE) / 100 \
                          * parent_vph
                elif unit == SVGLength.TYPE_VW:
                    vph = vph.value(SVGLength.TYPE_PERCENTAGE) / 100 \
                          * parent_vpw
                elif unit == SVGLength.TYPE_VMAX:
                    vph = max(parent_vpw, parent_vph)
                elif unit == SVGLength.TYPE_VMIN:
                    vph = min(parent_vpw, parent_vph)
            parent_vph = vph
        if len(roots) == 0:
            vpx = SVGLength(0)
            vpy = SVGLength(0)
        else:
            root = roots[-1]
            vpx = SVGLength(root.get('x', '0'),
                            context=root,
                            direction=SVGLength.DIRECTION_HORIZONTAL)
            unit = vpx.unit
            if unit in (SVGLength.TYPE_PERCENTAGE, SVGLength.TYPE_VW):
                vpx = vpx.value(SVGLength.TYPE_PERCENTAGE) / 100 * vpw
            elif unit == SVGLength.TYPE_VH:
                vpx = vpx.value(SVGLength.TYPE_PERCENTAGE) / 100 * vph
            elif unit == SVGLength.TYPE_VMAX:
                vpx = max(vpw, vph)
            elif unit == SVGLength.TYPE_VMIN:
                vpx = min(vpw, vph)

            vpy = SVGLength(root.get('y', '0'),
                            context=root,
                            direction=SVGLength.DIRECTION_VERTICAL)
            unit = vpy.unit
            if unit in (SVGLength.TYPE_PERCENTAGE, SVGLength.TYPE_VH):
                vpy = vpy.value(SVGLength.TYPE_PERCENTAGE) / 100 * vph
            elif unit == SVGLength.TYPE_VW:
                vpy = vpy.value(SVGLength.TYPE_PERCENTAGE) / 100 * vpw
            elif unit == SVGLength.TYPE_VMAX:
                vpy = max(vpw, vph)
            elif unit == SVGLength.TYPE_VMIN:
                vpy = min(vpw, vph)

        # TODO: check a range: max-width, max-height, min-width and min-height.
        return vpx, vpy, vpw, vph


class SVGGraphicsElement(SVGElement):
    """Represents the [SVG2] SVGGraphicsElement."""

    @property
    def transform(self):
        """SVGTransformList: The computed value of the 'transform' property.
        """
        # 'transform' property
        # Value: none | <transform-list>
        # <transform-list> = <transform-function>+
        # Initial: none
        # Inherited: no
        transform = self.get('transform')
        if transform is None or transform == 'none':
            return None
        return SVGTransformList.parse(transform)

    @transform.setter
    def transform(self, transform):
        value = SVGTransformList.tostring(transform)
        self.set('transform', value)

    def _get_ctm(self, viewport_type):
        """Returns the current transformation matrix (CTM).

        Returns:
            DOMMatrix: The current transformation matrix (CTM).
        """
        roots = list()
        ctm = DOMMatrix()
        farthest = self.get_farthest_svg_element()
        if farthest is None:
            return ctm
        elif hash(farthest) == hash(self):
            roots.append(farthest)
        else:
            element = self
            while element is not None:
                root = element.get_nearest_viewport_element()
                if root is None or root in roots:
                    break
                roots.insert(0, root)
                if viewport_type == SVGElement.NEAREST_VIEWPORT:
                    if (self.local_name not in ('svg', 'symbol')
                            or len(roots) >= 2):
                        break
                element = root.getparent()
        if len(roots) == 0:
            return ctm

        if viewport_type == SVGElement.FARTHEST_VIEWPORT:
            scale = farthest.current_scale
            tx, ty = farthest.current_translate
            ctm *= DOMMatrix([scale, 0, 0, scale, tx, ty])
        for root in roots:
            vtm = root.get_viewport_transformation_matrix(recursive=False)
            ctm *= vtm

        transform_list = SVGTransformList()
        element = self
        while element is not None:
            if element.istransformable():
                transform = element.transform
                if transform is not None:
                    transform_list[0:0] = transform
            if element.local_name in ('svg', 'symbol'):
                break
            element = element.getparent()
        if len(transform_list) > 0:
            matrix = transform_list.matrix
            ctm *= matrix
        return ctm

    def get_bbox(self, options=None, _depth=0):
        """Returns the bounding box of the current element.

        Arguments:
            options (SVGBoundingBoxOptions, optional): Reserved.
            _depth (int, optional): For internal use only.
        Returns:
            DOMRect: The bounding box of the current element.
        """
        # TODO: implement SVGBoundingBoxOptions option.
        _depth += 1
        bbox = DOMRect()
        if self.local_name in ('defs', 'symbol'):
            return bbox  # not rendered directly
        if self.iscontainer():
            for child in iter(self):
                if isinstance(child, SVGGraphicsElement):
                    display = child.get('display', 'inline')
                    if display == 'none':
                        continue
                    bbox |= child.get_bbox(options, _depth)
            if _depth > 1:
                transform_list = self.transform  # type: SVGTransformList
                if transform_list is not None:
                    matrix = transform_list.matrix
                    bbox.transform_self(matrix)
        else:
            settings = SVGPathDataSettings()
            settings.normalize = True
            path_data = self.get_transformed_path_data(settings)
            if len(path_data) > 0:
                bbox = PathParser.get_bbox(path_data, options)
        return bbox

    def get_ctm(self):
        """Returns the current transformation matrix (CTM). The matrix that
        transforms the current element's coordinate system to its SVG
        viewport's coordinate system.

        Returns:
            DOMMatrix: The current transformation matrix (CTM).
        """
        ctm = self._get_ctm(SVGElement.NEAREST_VIEWPORT)
        return ctm

    def get_descendant_path_data(self, settings=None):
        path_data = list()
        for child in iter(self):
            if isinstance(child, SVGGraphicsElement):
                path_data += child.get_path_data(settings)
        return path_data

    @abstractmethod
    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        raise NotImplementedError

    def get_screen_ctm(self):
        """Returns the current transformation matrix (CTM). The matrix that
        transforms the current element's coordinate system to the coordinate
        system of the SVG viewport for the SVG document fragment.

        Returns:
            DOMMatrix: The current transformation matrix (CTM).
        """
        ctm = self._get_ctm(SVGElement.FARTHEST_VIEWPORT)
        return ctm

    def get_transformed_path_data(self, settings=None):
        path_data = self.get_path_data(settings)
        if len(path_data) == 0:
            return path_data
        if self.local_name == 'use':
            transform_list = self.instance_root.transform
            if transform_list is not None:
                matrix = transform_list.matrix
                path_data = PathParser.transform(path_data, matrix)
        transform_list = self.transform  # type: SVGTransformList
        if transform_list is not None:
            matrix = transform_list.matrix
            path_data = PathParser.transform(path_data, matrix)
        return path_data

    def get_viewport_transformation_matrix(self, recursive=True):
        """Returns the transformation matrix of an SVG viewport.

        Returns:
            DOMMatrix: The transformation matrix.
        """
        ctm = DOMMatrix()
        ex, ey, ew, eh = self.get_viewport_size(recursive)
        view_box = self.get_view_box(recursive)
        if view_box is None:
            if ex is not None and ey is not None:
                ctm.translate_self(ex.value(), ey.value())
            return ctm
        if ew is None or eh is None:
            return ctm
        vbx, vby, vbw, vbh, par = view_box
        align = par.align
        if align == SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_UNKNOWN:
            align = SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMIDYMID
        meet_or_slice = par.meet_or_slice
        if meet_or_slice == SVGPreserveAspectRatio.SVG_MEETORSLICE_UNKNOWN:
            meet_or_slice = SVGPreserveAspectRatio.SVG_MEETORSLICE_MEET
        sx = ew / vbw
        sy = eh / vbh
        if align != SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_NONE:
            if meet_or_slice == SVGPreserveAspectRatio.SVG_MEETORSLICE_MEET:
                if sx < sy:
                    sy = sx
                elif sx > sy:
                    sx = sy
            elif meet_or_slice == SVGPreserveAspectRatio.SVG_MEETORSLICE_SLICE:
                if sx > sy:
                    sy = sx
                elif sx < sy:
                    sx = sy
        tx = ex - vbx * sx
        ty = ey - vby * sy
        if align in (SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMIDYMIN,
                     SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMIDYMID,
                     SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMIDYMAX):
            # 'xMid'
            tx += (ew - vbw * sx) / 2
        if align in (SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMAXYMIN,
                     SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMAXYMID,
                     SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMAXYMAX):
            # 'xMax'
            tx += ew - vbw * sx
        if align in (SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMINYMID,
                     SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMIDYMID,
                     SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMAXYMID):
            # 'YMid'
            ty += (eh - vbh * sy) / 2
        if align in (SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMINYMAX,
                     SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMIDYMAX,
                     SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMAXYMAX):
            # 'YMax'
            ty += eh - vbh * sy
        ctm.translate_self(tx.value(), ty.value())
        ctm.scale_self(sx.value(tx.unit), sy.value(tx.unit))
        return ctm


class SVGFitToViewBox(Element):
    """Represents the [SVG2] SVGFitToViewBox."""

    @property
    def preserve_aspect_ratio(self):
        """SVGPreserveAspectRatio: The value of the 'preserveAspectRatio'
        attribute.
        """
        default = '{} {}'.format(
            SVGPreserveAspectRatio.ALIGN_XMIDYMID,
            SVGPreserveAspectRatio.MEETORSLICE_MEET)
        par = SVGPreserveAspectRatio(self.get('preserveAspectRatio', default))
        return par

    @property
    def view_box(self):
        """tuple[SVGLength, SVGLength, SVGLength, SVGLength]: The value of the
        'viewBox' attribute is a tuple of four numbers <min-x>, <min-y>,
        <width> and <height>.
        """
        # 'viewBox' attribute
        # Value: [<min-x>,? <min-y>,? <width>,? <height>]
        # <min-x>, <min-x>, <width>, <height> = <number>
        view_box = self.get('viewBox')
        if view_box is None:
            return None
        vb = Element.RE_DIGIT_SEQUENCE_SPLITTER.split(view_box)
        return (SVGLength(vb[0],
                          context=self,
                          direction=SVGLength.DIRECTION_HORIZONTAL),
                SVGLength(vb[1],
                          context=self,
                          direction=SVGLength.DIRECTION_VERTICAL),
                SVGLength(vb[2],
                          context=self,
                          direction=SVGLength.DIRECTION_HORIZONTAL),
                SVGLength(vb[3],
                          context=self,
                          direction=SVGLength.DIRECTION_VERTICAL))


class SVGGeometryElement(SVGGraphicsElement):
    """Represents the [SVG2] SVGGeometryElement."""

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        raise NotImplementedError  # implement in a subclass

    def get_point_at_length(self, distance):
        # TODO: implement SVGGeometryElement.getPointAtLength().
        pass

    def get_total_length(self):
        """Returns the total length of the path.

        Returns:
            float: The total length of the path.
        """
        path_data = self.get_path_data()
        if len(path_data) == 0:
            return 0
        return PathParser.get_total_length(path_data)


class SVGPathData(Element):
    """Represents the [SVG2] SVGPathData."""

    def set_path_data(self, path_data):
        if path_data is None or len(path_data) == 0:
            d = 'none'
        else:
            d = PathParser.tostring(path_data)
        self.set('d', d)


class SVGPathDataSettings(object):
    """Represents the [SVG2] SVGPathDataSettings."""

    def __init__(self):
        self.normalize = False


class SVGPreserveAspectRatio(object):
    """Represents the [SVG2] SVGPreserveAspectRatio."""

    SVG_PRESERVEASPECTRATIO_UNKNOWN = 0
    SVG_PRESERVEASPECTRATIO_NONE = 1
    SVG_PRESERVEASPECTRATIO_XMINYMIN = 2
    SVG_PRESERVEASPECTRATIO_XMIDYMIN = 3
    SVG_PRESERVEASPECTRATIO_XMAXYMIN = 4
    SVG_PRESERVEASPECTRATIO_XMINYMID = 5
    SVG_PRESERVEASPECTRATIO_XMIDYMID = 6  # default
    SVG_PRESERVEASPECTRATIO_XMAXYMID = 7
    SVG_PRESERVEASPECTRATIO_XMINYMAX = 8
    SVG_PRESERVEASPECTRATIO_XMIDYMAX = 9
    SVG_PRESERVEASPECTRATIO_XMAXYMAX = 10

    SVG_MEETORSLICE_UNKNOWN = 0
    SVG_MEETORSLICE_MEET = 1  # default
    SVG_MEETORSLICE_SLICE = 2

    ALIGN_NONE = 'none'
    ALIGN_XMINYMIN = 'xMinYMin'
    ALIGN_XMIDYMIN = 'xMidYMin'
    ALIGN_XMAXYMIN = 'xMaxYMin'
    ALIGN_XMINYMID = 'XMinYMid'
    ALIGN_XMIDYMID = 'xMidYMid'
    ALIGN_XMAXYMID = 'xMaxYMid'
    ALIGN_XMINYMAX = 'xMinYMax'
    ALIGN_XMIDYMAX = 'xMidYMax'
    ALIGN_XMAXYMAX = 'xMaxYMax'

    MEETORSLICE_MEET = 'meet'
    MEETORSLICE_SLICE = 'slice'

    _TYPE_ALIGN_MAP = {
        SVG_PRESERVEASPECTRATIO_NONE: ALIGN_NONE,
        SVG_PRESERVEASPECTRATIO_XMINYMIN: ALIGN_XMINYMIN,
        SVG_PRESERVEASPECTRATIO_XMIDYMIN: ALIGN_XMIDYMIN,
        SVG_PRESERVEASPECTRATIO_XMAXYMIN: ALIGN_XMAXYMIN,
        SVG_PRESERVEASPECTRATIO_XMINYMID: ALIGN_XMINYMID,
        SVG_PRESERVEASPECTRATIO_XMIDYMID: ALIGN_XMIDYMID,
        SVG_PRESERVEASPECTRATIO_XMAXYMID: ALIGN_XMAXYMID,
        SVG_PRESERVEASPECTRATIO_XMINYMAX: ALIGN_XMINYMAX,
        SVG_PRESERVEASPECTRATIO_XMIDYMAX: ALIGN_XMIDYMAX,
        SVG_PRESERVEASPECTRATIO_XMAXYMAX: ALIGN_XMAXYMAX,
    }

    _ALIGN_TYPE_MAP = dict((v, k) for k, v in _TYPE_ALIGN_MAP.items())

    _TYPE_MEETORSLICE_MAP = {
        SVG_MEETORSLICE_MEET: MEETORSLICE_MEET,
        SVG_MEETORSLICE_SLICE: MEETORSLICE_SLICE,
    }

    _MEETORSLICE_TYPE_MAP = dict(
        (v, k) for k, v in _TYPE_MEETORSLICE_MAP.items())

    def __init__(self, text=None):
        self._align = SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMIDYMID
        self._meet_or_slice = SVGPreserveAspectRatio.SVG_MEETORSLICE_MEET
        if text is not None:
            (self._align,
             self._meet_or_slice) = SVGPreserveAspectRatio.parse(text)

    def __eq__(self, other):
        if not isinstance(other, SVGPreserveAspectRatio):
            return NotImplemented
        return (self.align == other.align
                and self.meet_or_slice == other.meet_or_slice)

    def __repr__(self):
        return repr({
            'align': self.align,
            'meet_or_slice': self.meet_or_slice,
        })

    @property
    def align(self):
        """int: The numeric alignment type."""
        return self._align

    @align.setter
    def align(self, value):
        self._align = value

    @property
    def meet_or_slice(self):
        """int: The numeric meet-or-slice type."""
        return self._meet_or_slice

    @meet_or_slice.setter
    def meet_or_slice(self, value):
        self._meet_or_slice = value

    @staticmethod
    def parse(text):
        align = SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_XMIDYMID
        meet_or_slice = SVGPreserveAspectRatio.SVG_MEETORSLICE_MEET
        items = Element.RE_DIGIT_SEQUENCE_SPLITTER.split(text.strip())
        if len(items) > 0:
            align = SVGPreserveAspectRatio._ALIGN_TYPE_MAP.get(
                items[0],
                align)
            if len(items) > 1:
                meet_or_slice = SVGPreserveAspectRatio._MEETORSLICE_TYPE_MAP.get(
                    items[1],
                    meet_or_slice)
        return align, meet_or_slice

    def tostring(self):
        if self.align == SVGPreserveAspectRatio.SVG_PRESERVEASPECTRATIO_NONE:
            return SVGPreserveAspectRatio.ALIGN_NONE
        align = SVGPreserveAspectRatio._TYPE_ALIGN_MAP.get(
            self.align,
            SVGPreserveAspectRatio.ALIGN_XMIDYMID)
        meet_or_slice = SVGPreserveAspectRatio._TYPE_MEETORSLICE_MAP.get(
            self.meet_or_slice,
            SVGPreserveAspectRatio.MEETORSLICE_MEET)
        return ' '.join([align, meet_or_slice])


class SVGURIReference(Element):
    """Represents the [SVG2] SVGURIReference."""

    @property
    def href(self):
        href = self.get('href', '')
        if len(href) == 0:
            qname = QualifiedName(Element.XLINK_NAMESPACE_URI, 'href')
            href = self.get(qname.name, '')
        return href


class SVGGradientElement(SVGElement, SVGURIReference):
    """Represents the [SVG2] SVGGradientElement."""

    SVG_SPREADMETHOD_UNKNOWN = 0
    SVG_SPREADMETHOD_PAD = 1
    SVG_SPREADMETHOD_REFLECT = 2
    SVG_SPREADMETHOD_REPEAT = 3


class SVGZoomAndPan(Element):
    """Represents the [SVG2] SVGZoomAndPan."""

    SVG_ZOOMANDPAN_UNKNOWN = 0
    SVG_ZOOMANDPAN_DISABLE = 1  # default
    SVG_ZOOMANDPAN_MAGNIFY = 2

    ZOOMANDPAN_DISABLE = 'disable'
    ZOOMANDPAN_MAGNIFY = 'magnify'

    _TYPE_ZOOMANDPAN_MAP = {
        SVG_ZOOMANDPAN_DISABLE: ZOOMANDPAN_DISABLE,
        SVG_ZOOMANDPAN_MAGNIFY: ZOOMANDPAN_MAGNIFY,
    }

    _ZOOMANDPAN_TYPE_MAP = dict(
        (v, k) for k, v in _TYPE_ZOOMANDPAN_MAP.items())

    @property
    def zoom_and_pan(self):
        """int: The zoom and pan type."""
        value = self.get('zoomAndPan', SVGZoomAndPan.ZOOMANDPAN_DISABLE)
        zoom_and_pan = SVGZoomAndPan._ZOOMANDPAN_TYPE_MAP.get(
            value, SVGZoomAndPan.SVG_ZOOMANDPAN_UNKNOWN)
        return zoom_and_pan

    @zoom_and_pan.setter
    def zoom_and_pan(self, value):
        if value not in SVGZoomAndPan._TYPE_ZOOMANDPAN_MAP:
            return
        zoom_and_pan = SVGZoomAndPan._TYPE_ZOOMANDPAN_MAP[value]
        self.set('zoomAndPan', zoom_and_pan)
