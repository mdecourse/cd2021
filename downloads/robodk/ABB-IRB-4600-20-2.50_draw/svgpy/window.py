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


from abc import ABC, abstractmethod
from collections.abc import Collection
from fractions import Fraction
from io import StringIO
from logging import getLogger

from lxml import etree

from .core import SVGLength
from .css import mediaquery as mq
from .css.screen import Screen
from .dom import Element, Node, NonElementParentNode, ParentNode, \
    node_insert_before
from .exception import HierarchyRequestError
from .style import get_css_style_sheets
from .url import Location
from .utils import get_content_type, get_element_by_id, \
    get_elements_by_class_name, get_elements_by_tag_name, \
    get_elements_by_tag_name_ns, load, normalize_url


class BrowsingContext(object):
    """A browsing context object that is associated with the document."""

    def __init__(self, document, window_=None):
        """Constructs a browsing context object.

        Arguments:
            document (Document, None): The current document associated with
                the active window.
            window_ (Window, optional): The active window that is associated
                with the current document.
        """
        self._document = document
        if window_ is None:
            global window
            window_ = window
        self._window = window_

    @property
    def document(self):
        """Document: The current document associated with the active window.
        """
        return (self._document if self._document is not None
                else self._window.document)

    @property
    def window(self):
        """Window: The active window that is associated with the current
        document.
        """
        return self._window


class Document(Node, NonElementParentNode, ParentNode, Collection):
    """Represents the [DOM] Document."""

    def __init__(self, content_type=None, default_view=None,
                 document_element=None, implementation=None):
        """Constructs a Document object.

        Arguments:
            content_type (str, optional): The MIME type of the document.
            default_view (Window, optional): The active window that is
                associated with the document.
            document_element (Element, optional): A root element of the
                document.
            implementation (SVGDOMImplementation, optional):
                A DOM implementation object that is associated with the
                document.
        """
        super().__init__()
        self._browsing_context = BrowsingContext(self, default_view)
        self._content_type = (content_type if content_type is not None
                              else 'application/xml')
        self._document_element = None
        if document_element is not None:
            self.append(document_element)
        self._implementation = implementation
        if default_view is not None:
            self._location = default_view.location
        else:
            self._location = Location(self._browsing_context)
        self._registered_property_set = dict()

    def __contains__(self, node):
        return node in self.child_nodes

    def __iter__(self):
        children = self.child_nodes
        return iter(children)

    def __len__(self):
        return len(self.child_nodes)

    @property
    def child_nodes(self):
        """list[Node]: The children of this node."""
        root = self._document_element
        if root is None:
            return []
        children = list(root.itersiblings(preceding=True))
        children.reverse()
        children += [root]
        children += list(root.itersiblings())
        return children

    @property
    def children(self):
        """list[Element]: A list of the child elements, in document order."""
        children = self.child_nodes
        return [child for child in children
                if child.node_type == Node.ELEMENT_NODE]

    @property
    def content_type(self):
        """str: The MIME type of the current document."""
        return self._content_type

    @property
    def default_view(self):
        """Window: The active window that is associated with the current
        document.
        """
        return self._browsing_context.window

    @property
    def document_element(self):
        """Element: A root element of the current document."""
        return self._document_element

    @property
    def document_uri(self):
        """str: The entire URL of the current document."""
        return self._location.href

    @property
    def implementation(self):
        """DOMImplementation: The DOM implementation object that is associated
        with the current document.
        """
        return self._implementation

    @property
    def location(self):
        """Location: The Location object that is associated with the current
        document.
        If changed, the associated document navigates to the new page.
        """
        return self._location

    @location.setter
    def location(self, src):
        url = normalize_url(src, self._location.href)
        self._location.href = url.tostring()

    @property
    def next_sibling(self):
        """Node: The first following sibling node or None."""
        return None

    @property
    def node_name(self):
        """str: '#document'."""
        return '#document'

    @property
    def node_type(self):
        """int: The type of node."""
        return Node.DOCUMENT_NODE

    @property
    def node_value(self):
        """str: The value of node."""
        return None

    @node_value.setter
    def node_value(self, value):
        pass  # do nothing

    @property
    def origin(self):
        """str: The URL's origin of the current document."""
        return self._location.origin

    @property
    def parent_node(self):
        """Node: A parent node."""
        return None

    @property
    def previous_sibling(self):
        """Node: The first preceding sibling node or None."""
        return None

    @property
    def registered_property_set(self):
        """dict: A set of records that describe registered custom properties.
        """
        return self._registered_property_set

    @property
    def style_sheets(self):
        """list[StyleSheet]: A list of the document CSS style sheets."""
        root = self._document_element
        return get_css_style_sheets(root) if root is not None else []

    @property
    def text_content(self):
        """str: The text content of node."""
        return None

    @text_content.setter
    def text_content(self, text):
        pass  # do nothing

    @property
    def url(self):
        """str: The entire URL of the current document."""
        return self._location.href

    def append(self, *nodes):
        """Inserts sub-nodes after the last child node.

        Arguments:
            *nodes (Node, str, ...): A list of nodes to be added.
        """
        root = self._document_element
        last_child = None
        for node in nodes:
            if isinstance(node, str):
                raise HierarchyRequestError(
                    "This node type '{}' cannot insert inside nodes of type "
                    "'{}'".format('#text',
                                  self.__class__.__name__))
            self.ensure_pre_insertion_validity(node)
            if root is None:
                if not isinstance(node, Element):
                    raise HierarchyRequestError(
                        "The Element node must be insert first")
                node.attach_document(self)
                root = self._document_element = node
            elif node == root:
                continue  # do nothing
            else:
                if last_child is None:
                    last_child = self.last_child
                last_child.addnext(node)
                last_child = node

    def append_child(self, node):
        """Adds a sub-node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        self.append(node)
        return node

    def attach_document(self, document):
        """Reimplemented from Node.attach_document().

        Attaches an associated document.

        Arguments:
            document (Document): A document that is associated with the node.
        Returns:
            bool: Returns True if successful; otherwise False.
        """
        _ = document
        return False

    def create_attribute(self, local_name):
        """Creates a new attribute instance, and returns it.
        See also SVGParser.create_attribute().

        Arguments:
            local_name (str): A local name of an attribute to be created.
        Returns:
            Attr: A new attribute.
        """
        if self._implementation is None:
            raise ValueError('No DOMImplementation found')
        parser = self._implementation.parser
        attr = parser.create_attribute(local_name)
        attr.attach_document(self)
        return attr

    def create_attribute_ns(self, namespace, qualified_name):
        """Creates a new attribute instance with the specified namespace URI
        and qualified name, and returns it.
        See also SVGParser.create_attribute_ns().

        Arguments:
            namespace (str, None): The namespace URI to associated with
                the element.
            qualified_name (str): A qualified name of an attribute to be
                created.
        Returns:
            Attr: A new attribute.
        """
        if self._implementation is None:
            raise ValueError('No DOMImplementation found')
        parser = self._implementation.parser
        attr = parser.create_attribute_ns(namespace, qualified_name)
        attr.attach_document(self)
        return attr

    def create_comment(self, data):
        """Creates a new comment instance, and returns it.
        See also SVGParser.create_comment().

        Arguments:
            data (str): A string of the comment.
        Returns:
            Comment: A new comment.
        """
        if self._implementation is None:
            raise ValueError('No DOMImplementation found')
        parser = self._implementation.parser
        comment = parser.create_comment(data)
        comment.attach_document(self)
        return comment

    def create_element(self, local_name, attrib=None, nsmap=None, **_extra):
        """Creates a new element instance, and returns it.
        See also SVGParser.create_element().

        Arguments:
            local_name (str): A local name of an element to be created.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        """
        if self._implementation is None:
            raise ValueError('No DOMImplementation found')
        parser = self._implementation.parser
        element = parser.create_element(local_name,
                                        attrib=attrib,
                                        nsmap=nsmap,
                                        **_extra)
        element.attach_document(self)
        return element

    def create_element_ns(self, namespace, qualified_name, attrib=None,
                          nsmap=None, **_extra):
        """Creates a new element instance with the specified namespace URI
        and qualified name, and returns it.
        See also SVGParser.create_element_ns().

        Arguments:
            namespace (str, None): The namespace URI to associated with
                the element.
            qualified_name (str): A qualified name of an element to be created.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        """
        if self._implementation is None:
            raise ValueError('No DOMImplementation found')
        parser = self._implementation.parser
        element = parser.create_element_ns(namespace,
                                           qualified_name,
                                           attrib=attrib,
                                           nsmap=nsmap,
                                           **_extra)
        element.attach_document(self)
        return element

    def create_processing_instruction(self, target, data=None):
        """Creates a new processing instruction, and returns it.

        Arguments:
            target (str): The target of this processing instruction.
            data (str, optional): The content of this processing instruction.
        Returns:
            ProcessingInstruction: A new processing instruction.
        """
        if self._implementation is None:
            raise ValueError('No DOMImplementation found')
        parser = self._implementation.parser
        pi = parser.create_processing_instruction(target, data)
        pi.attach_document(self)
        return pi

    def detach_document(self):
        """Reimplemented from Node.detach_document().

        Detaches an associated document.

        Returns:
            Document: A document to be detached.
        """
        return None

    def extend(self, nodes):
        """Extends the current children by the nodes in the iterable.
        """
        if isinstance(nodes, (list, tuple)):
            self.append(*nodes)
            return
        for node in nodes:
            self.append(node)

    def get_element_by_id(self, element_id, nsmap=None):
        """Finds the first matching sub-element, by id.

        Arguments:
            element_id (str): The id of the element.
            nsmap (dict, optional): The XPath prefixes in the path expression.
        Returns:
            Element: The first matching sub-element. Returns None if there is
                no such element.
        """
        root = self._document_element
        if root is None:
            return None
        return get_element_by_id(root, element_id, nsmap=nsmap)

    def get_elements_by_class_name(self, class_names, nsmap=None):
        """Finds all matching sub-elements, by class names.

        Arguments:
            class_names (str): A list of class names that are separated by
                whitespace.
            nsmap (dict, optional): The XPath prefixes in the path expression.
        Returns:
            list[Element]: A list of elements.
        """
        root = self._document_element
        if root is None:
            return []
        return get_elements_by_class_name(root,
                                          class_names,
                                          nsmap=nsmap,
                                          include_self=True)

    def get_elements_by_tag_name(self, qualified_name, nsmap=None):
        """Finds all matching sub-elements, by the qualified name.

        Arguments:
            qualified_name (str): The qualified name or '*'.
            nsmap (dict, optional): The XPath prefixes in the path expression.
        Returns:
            list[Element]: A list of elements.
        """
        root = self._document_element
        if root is None:
            return []
        return get_elements_by_tag_name(root,
                                        qualified_name,
                                        nsmap=nsmap,
                                        include_self=True)

    def get_elements_by_tag_name_ns(self, namespace, local_name,
                                    nsmap=None):
        """Finds all matching sub-elements, by the namespace URI and the local
        name.

        Arguments:
            namespace (str, None): The namespace URI, '*' or None.
            local_name (str): The local name or '*'.
            nsmap (dict, optional): The XPath prefixes in the path expression.
        Returns:
            list[Element]: A list of elements.
        """
        root = self._document_element
        if root is None:
            return []
        return get_elements_by_tag_name_ns(root,
                                           namespace,
                                           local_name,
                                           nsmap=nsmap,
                                           include_self=True)

    def get_root_node(self):
        """Returns a root node of the current document that contains this node.

        Returns:
            Node: A root node.
        """
        return self

    def insert(self, index, node):
        """Inserts a sub-node at the given position in this node.

        Arguments:
            index (int): An index position of the child nodes.
            node (Node): A node to be inserted.
        """
        root = self._document_element
        if root is None:
            self.append(node)
        elif node == root:
            pass  # do nothing
        else:
            children = self.child_nodes
            children[index].addprevious(node)

    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        self.ensure_pre_insertion_validity(node, child)
        node_insert_before(self, node, child)
        return node

    def iter(self, tag=None, *tags):
        """Iterates over all nodes in the subtree in document order
        (depth first pre-order).
        See also lxml.etree._Element.iter().
        """
        nodes = list()
        for node in self.child_nodes:
            children = node.iter(tag=tag, *tags)
            for child in children:
                nodes.append(child)
        return iter(nodes)

    def navigate(self, url):
        """Replaces the current document in-place.
        See also Document.location.

        Arguments:
            url (URL): The entire URL.
        Returns:
            Document: Returns itself.
        """
        resource = url.href
        logger = getLogger('{}.{}'.format(__name__, self.__class__.__name__))
        logger.debug('navigate to \'{}\''.format(resource))
        root = self._document_element
        if root is not None:
            self.remove(root)
        if url.protocol != 'about:':
            root = self._implementation.parse(resource)
            self.append(root)
        return self

    def prepend(self, *nodes):
        """Inserts sub-nodes before the first child node.

        Arguments:
            *nodes (Node, str, ...): A list of nodes to be added.
        """
        root = self._document_element
        first_child = None
        for node in nodes:
            if isinstance(node, str):
                raise HierarchyRequestError(
                    "This node type '{}' cannot insert inside nodes of type "
                    "'{}'".format('#text',
                                  self.__class__.__name__))
            self.ensure_pre_insertion_validity(node)
            if root is None:
                self.append(node)
                root = node
            elif node == root:
                continue  # do nothing
            else:
                if first_child is None:
                    first_child = self.first_child
                first_child.addprevious(node)

    def query_selector_all(self, selectors):
        root = self._document_element
        return root.query_selector_all(selectors) if root is not None else []

    def remove(self, node):
        """Removes a child node from this node.

        Arguments:
            node (Node): A node to be removed.
        """
        self.ensure_pre_remove_validity(node)
        root = self._document_element
        if node == root:
            self._document_element = None
            return
        root.append(node)  # move
        root.remove(node)

    def remove_child(self, node):
        """Removes a child node from this node.

        Arguments:
            node (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        self.remove(node)
        return node

    def replace(self, old_node, new_node):
        """Replaces a sub-node with the node passed as second argument.

        Arguments:
            old_node (Node): A reference child node.
            new_node (Node): A node to be replaced.
        """
        self.ensure_pre_insertion_validity(new_node, old_node)
        self.ensure_pre_remove_validity(old_node)
        root = self._document_element
        if old_node == root:
            self.remove(old_node)
            self.append(new_node)
            return
        children = self.child_nodes
        pos = children.index(old_node)
        children[pos].addprevious(new_node)
        self.remove(old_node)

    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node): A reference child node.
        Returns:
            Node: A node to be removed.
        """
        self.replace(child, node)
        return child

    def tostring(self, **kwargs):
        """Serializes a document to an encoded string representation of its
        XML tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        Returns:
            bytes: An XML document.
        """
        root = self._document_element
        if root is None:
            return b''
        return etree.tostring(root.getroottree(), **kwargs)


class DOMImplementation(ABC):
    """Represents the [DOM] DOMImplementation."""

    @abstractmethod
    def create_document(self, namespace, qualified_name=None, doctype=None,
                        nsmap=None, **extra):
        """Creates a new XML document instance, and returns it.

        Arguments:
            namespace (str, None): The namespace URI to associated with the
                element.
            qualified_name (str, optional): A qualified name of an element to
                be created.
            doctype (DocumentType, optional): A Document Type of the document.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **extra: Reserved.
        Returns:
            XMLDocument: A new XML document.
        """
        raise NotImplementedError


def _mql_compare(left, right, user_data):
    left_value = SVGLength(left, context=user_data)
    right_value = SVGLength(right, context=user_data)
    if left_value == right_value:
        return 0
    cmp = 1 if left_value > right_value else -1
    return cmp


class MediaQueryList(object):
    """Represents the [cssom-view] MediaQueryList."""

    def __init__(self, browsing_context, query):
        """Constructs a MediaQueryList object.

        Arguments:
            browsing_context (BrowsingContext): A browsing context object that
                is associated with the document.
            query (str): The media query list to be parsed.
        """
        self._browsing_context = browsing_context
        self._query = query
        self._tree = mq.parse(self._query)

    @property
    def matches(self):
        """bool: The matches state of the associated media query list."""
        doc = self._browsing_context.document
        win = self._browsing_context.window
        context = doc.document_element
        if context is not None:
            _, _, vpw, vph = context.get_viewport_size()
            width = vpw.value()
            height = vph.value()
        else:
            width = win.inner_width
            height = win.inner_height
        aspect_ratio = Fraction(int(width), int(height))
        screen = win.screen
        device_aspect_ratio = Fraction(int(screen.width), int(screen.height))
        conditions = {
            'media': screen.media,
            'width': '{}px'.format(width),
            'height': '{}px'.format(height),
            'aspect-ratio': '{}'.format(aspect_ratio),
            'orientation': screen.orientation.type,
            'resolution': '{}dppx'.format(win.device_pixel_ratio),
            'scan': screen.scan,
            'grid': 0,
            'update': screen.update,
            'overflow-block': 'none',
            'overflow-inline': 'none',
            'color': screen.color_depth,
            'color-index': 1 << screen.color_depth,
            'monochrome': screen.monochrome,
            'color-gamut': screen.color_gamut,
            # deprecated media features
            'device-width': '{}px'.format(screen.width),
            'device-height': '{}px'.format(screen.height),
            'device-aspect-ratio': '{}'.format(device_aspect_ratio),
        }
        matches, _ = mq.match(self._tree, conditions, _mql_compare,
                              user_data=context)
        return matches

    @property
    def media(self):
        """str: The serialized form of the associated media query list."""
        # TODO: serialize a media query list.
        return self._query


class SVGDOMImplementation(DOMImplementation):

    def __init__(self, parser=None, **kwargs):
        """Constructs an SVGDOMImplementation object.

        Arguments:
            parser (SVGParser, optional): An SVG parser object.
            **kwargs: See SVGParser.__init__().
        """
        if parser is None:
            from .element import SVGParser
            parser = SVGParser(**kwargs)
        self._parser = parser

    @property
    def parser(self):
        """SVGParser: An SVG parser object."""
        return self._parser

    def create_document(self, namespace, qualified_name=None, doctype=None,
                        nsmap=None, **extra):
        """Creates a new XML document instance, and returns it.

        Arguments:
            namespace (str, None): The namespace URI to associated with the
                element.
            qualified_name (str, optional): A qualified name of an element to
                be created.
            doctype (DocumentType, optional): A Document Type of the document.
                Sets to None.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **extra: See Document.__init__().
        Returns:
            XMLDocument: A new XML document.
        """
        _ = doctype
        if namespace == Element.SVG_NAMESPACE_URI:
            content_type = 'image/svg+xml'
        elif namespace == Element.XHTML_NAMESPACE_URI:
            content_type = 'application/xhtml+xml'
        else:
            content_type = 'application/xml'
        doc = XMLDocument(content_type=content_type,
                          implementation=self,
                          **extra)
        if qualified_name is not None and len(qualified_name) > 0:
            root = doc.create_element_ns(namespace,
                                         qualified_name,
                                         nsmap=nsmap)
            doc.append(root)
        return doc

    def create_svg_document(self, nsmap=None):
        """Creates a new SVG document instance, and returns it.

        Arguments:
            nsmap (dict, optional): A map of a namespace prefix to the URI.
        Returns:
            XMLDocument: A new SVG document.
        """
        doc = self.create_document(Element.SVG_NAMESPACE_URI,
                                   'svg',
                                   nsmap=nsmap)
        return doc

    def parse(self, source):
        """Parses an SVG document, and returns the root element of it.

        Arguments:
            source (str, file): An URL or a file-like object of an SVG
                document.
        Returns:
            Element: A root element of the document.
        """
        if isinstance(source, str):
            data, headers = load(source)
            content_type = get_content_type(headers)
            if content_type is None:
                charset = 'utf-8'
            else:
                charset = content_type.get('charset', 'utf-8')
            data = StringIO(data.decode(charset))
        else:
            data = source
        tree = self._parser.parse(data)
        return tree.getroot()


class Window(object):
    """Represents the [HTML] Window."""

    def __init__(self, implementation):
        """Constructs a Window object.

        Arguments:
            implementation (DOMImplementation): A DOMImplementation object.
        """
        self._browsing_context = BrowsingContext(None, self)
        self._location = Location(self._browsing_context)
        self._implementation = implementation
        self._document = self._implementation.create_document(
            Element.SVG_NAMESPACE_URI,
            'svg',
            default_view=self)
        self._screen = Screen()
        self._inner_width = self._screen.width
        self._inner_height = self._screen.height
        self._page_zoom_scale = 1.

    @property
    def device_pixel_ratio(self):
        """float: The result of dividing CSS pixel size by device pixel size
        of the output device.
        """
        return self._screen.device_pixel_ratio * self.page_zoom_scale

    @property
    def document(self):
        """Document: The current document associated with the current window.
        """
        return self._document

    @property
    def inner_height(self):
        """int: The viewport height."""
        return self._inner_height

    @inner_height.setter
    def inner_height(self, height):
        self._inner_height = int(height)

    @property
    def inner_width(self):
        """int: The viewport width."""
        return self._inner_width

    @inner_width.setter
    def inner_width(self, width):
        self._inner_width = int(width)

    @property
    def location(self):
        """Location: The location object that is associated with the current
        document.
        If changed, the associated document navigates to the new page.
        """
        return self._location

    @location.setter
    def location(self, src):
        url = normalize_url(src, self._document.document_uri)
        self._location.href = url.tostring()

    @property
    def page_zoom_scale(self):
        """float: The current zoom scale of the current window."""
        return self._page_zoom_scale

    @page_zoom_scale.setter
    def page_zoom_scale(self, scale):
        self._page_zoom_scale = float(scale)

    @property
    def screen(self):
        """Screen: The Screen object that is associated with the current
        window.
        """
        return self._screen

    def match_media(self, query):
        """Returns a new MediaQueryList object, with the context object’s
        associated Document, with parsed media query list as its associated
        media query list.

        Arguments:
            query (str): The media query list to be parsed.
        Returns:
            MediaQueryList: A new MediaQueryList object.
        """
        mql = MediaQueryList(self._browsing_context, query)
        return mql


class XMLDocument(Document):
    """Represents the [DOM] XMLDocument."""
    pass


window = Window(SVGDOMImplementation())
