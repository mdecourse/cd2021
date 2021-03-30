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
from collections.abc import KeysView, MutableMapping, MutableSequence

from lxml import cssselect, etree

from .core import CSSUtils, Font, SVGLength
from .css import CSSStyleDeclaration
from .exception import HierarchyRequestError, InUseAttributeError, \
    InvalidCharacterError, NotFoundError
from .style import get_css_rules, get_css_style, \
    get_css_style_sheet_from_element
from .utils import QualifiedName, get_elements_by_class_name, \
    get_elements_by_tag_name, get_elements_by_tag_name_ns, \
    is_ascii_whitespace, style_to_dict


_RE_DOM_STRING_MAP_INVALID_SYNTAX = re.compile(r'-[a-z]')

# https://www.w3.org/TR/xml/#NT-Name
_RE_XML_NAME = re.compile(
    r"^(:|[A-Z]|_|[a-z]|[\xc0-\xd6]|[\xd8-\xf6]"
    r"|[\u00f8-\u02ff]|[\u0370-\u037d]|[\u037f-\u1fff]|[\u200c-\u200d]"
    r"|[\u2070-\u218f]|[\u2c00-\u2fef]|[\u3001-\ud7ff]|[\uf900-\ufdcf]"
    r"|[\ufdf0-\ufffd]|[\U00010000-\U000effff])"
    r"(:|[A-Z]|_|[a-z]|[\xc0-\xd6]|[\xd8-\xf6]"
    r"|[\u00f8-\u02ff]|[\u0370-\u037d]|[\u037f-\u1fff]|[\u200c-\u200d]"
    r"|[\u2070-\u218f]|[\u2c00-\u2fef]|[\u3001-\ud7ff]|[\uf900-\ufdcf]"
    r"|[\ufdf0-\ufffd]|[\U00010000-\U000effff]"
    r"|-|\.|[0-9]|\xb7|[\u0300-\u036f]|[\u203f-\u2040])*$")


def node_append_data(node, data, tail=True):
    if tail:
        text = '' if node.tail is None else node.tail
        text += data
        node.tail = text
    else:
        text = '' if node.text is None else node.text
        text += data
        node.text = text


def node_insert_before(parent, node, child=None):
    """Inserts a node into a parent before a child.

    Arguments:
        parent (Node): A parent node.
        node (Node): A node to be inserted.
        child (Node, optional): A reference child node.
    Returns:
        Node: A node to be inserted.
    """
    parent.ensure_pre_insertion_validity(node, child)
    reference_child = child
    if reference_child is not None and reference_child == node:
        reference_child = node.getnext()
    if reference_child is None:
        parent.append(node)
    else:
        reference_child.addprevious(node)
    return node


def node_prepend_data(node, data, tail=True):
    if tail:
        text = '' if node.tail is None else node.tail
        text = data + text
        node.tail = text
    else:
        text = '' if node.text is None else node.text
        text = data + text
        node.text = text


class DOMStringMap(MutableMapping):
    """Represents the [HTML] DOMStringMap."""

    def __init__(self, owner_element, prefix):
        """Constructs a DOMStringMap object.

        Arguments:
            owner_element (Element): The element that is associated with the
                attribute.
            prefix (str): The prefix of the attribute name.
        """
        self._owner_element = owner_element
        self._prefix = prefix

    def __delitem__(self, key):
        name = self._convert_name(key)
        del self._owner_element.attributes[name]

    def __getitem__(self, key):
        name = self._convert_name(key)
        attr = self._owner_element.attributes[name]
        return attr.value

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def __repr__(self):
        return repr({key: value for key, value in self.items()})

    def __setitem__(self, key, value):
        if value is None or len(value) == 0:
            del self[key]
            return
        name = self._convert_name(key)
        if not self._validate_name(name):
            raise InvalidCharacterError("The string contains invalid "
                                        "characters: " + repr(name))
        self._owner_element.attributes[name] = value

    def _convert_key(self, name):
        _name = name[len(self._prefix):]
        length = len(_name)
        key = ''
        start = 0
        while start < length:
            end = _name.find('-', start)
            if end == -1:
                end = length
            if start == end:
                key += '-'
            else:
                part = _name[start:end]
                if start != 0:
                    part = part.capitalize()
                key += part
            start = end + 1
        return key

    def _convert_name(self, key):
        if _RE_DOM_STRING_MAP_INVALID_SYNTAX.search(key) is not None:
            raise ValueError('Invalid syntax: ' + repr(key))
        name = self._prefix
        for ch in key:
            if ch.isupper():
                name += '-'
            name += ch
        return name.lower()

    def _validate_name(self, name):
        _ = self
        matched = _RE_XML_NAME.fullmatch(name)
        if matched is not None:
            return True
        return False

    def keys(self):
        keys = [self._convert_key(name)
                for name in self._owner_element.attributes
                if name.startswith(self._prefix) and name.islower()]
        return KeysView(keys)


class DOMTokenList(MutableSequence):
    # FIXME: implement DOMTokenList.supports().
    """Represents the [DOM] DOMTokenList."""

    def __init__(self, owner_element, local_name):
        """Constructs a DOMTokenList object.

        Arguments:
            owner_element (Element): The element that is associated with the
                attribute.
            local_name (str): The local name of the attribute.
        """
        self._owner_element = owner_element
        self._local_name = local_name

    def __delitem__(self, index):
        tokens = list(self._tokens)
        del tokens[index]
        self._set_tokens(tokens)

    def __getitem__(self, index):
        return self._tokens[index]

    def __len__(self):
        return len(self._tokens)

    def __repr__(self):
        return repr(list(self._tokens))

    def __setitem__(self, index, value):
        if isinstance(value, str):
            if value in self._tokens:
                return
        elif isinstance(value, list):
            for token in list(value):
                if token in self._tokens:
                    value.remove(token)
            if len(value) == 0:
                return
        else:
            raise TypeError('Expected str or list[str], got {}'.format(
                type(value)))
        tokens = list(self._tokens)
        tokens[index] = value
        self._set_tokens(tokens)

    @property
    def _tokens(self):
        """tuple[str, ...]: The token set."""
        value = self._owner_element.get(self._local_name, '')
        tokens = tuple(value.split())
        return tokens

    @property
    def length(self):
        """int: The token set's size."""
        return len(self)

    @property
    def value(self):
        """str: The attribute's value."""
        return ' '.join(self._tokens)

    def _set_tokens(self, tokens):
        value = ' '.join(tokens).strip()
        if len(value) == 0:
            if self._local_name in self._owner_element.attrib:
                del self._owner_element.attrib[self._local_name]
        else:
            self._owner_element.set(self._local_name, value)

    def _validate_token(self, token):
        _ = self
        if len(token) == 0:
            raise ValueError('Unexpected empty string')
        elif is_ascii_whitespace(token):
            raise ValueError('Invalid token: ' + repr(token))
        return True

    def _validate_tokens(self, tokens):
        for token in tokens:
            self._validate_token(token)
        return True

    def add(self, *tokens):
        """Adds tokens to the end of this token set.

        Arguments:
            *tokens (str, ...): The tokens to be added.
        """
        self._validate_tokens(tokens)
        self.extend(tokens)

    def contains(self, token):
        """Returns True if this token set contains token `token`, and False
        otherwise.

        Arguments:
            token (str): The token.
        Returns:
            bool: Returns True if this token set contains token, and False
                otherwise.
        """
        return token in self._tokens

    def insert(self, index, token):
        """Inserts `token` at the given position `index` in this token set.

        Arguments:
            index (int): An index position of the token set.
            token (str): The token to be inserted.
        """
        self._validate_token(token)
        self[index:index] = [token]

    def item(self, index):
        """Returns the token at index position `index` in the token set.

        Arguments:
            index (int): An index position of the token set.
        Returns:
            str: The token.
        """
        return self[index]

    def remove(self, *tokens):
        """Removes tokens in this token set.

        Arguments:
            *tokens (str, ...): The tokens to be removed.
        """
        self._validate_tokens(tokens)
        for token in tokens:
            if token not in self._tokens:
                continue
            super().remove(token)

    def replace(self, token, new_token):
        """Replaces `token` with `new_token`.

        Arguments:
            token (str): The token to be replaced.
            new_token (str): The new token.
        Returns:
            bool: Returns True if `token` was replaced with `new_token`, and
                False otherwise.
        """
        self._validate_tokens([token, new_token])
        if token not in self._tokens or new_token in self._tokens:
            return False
        index = self._tokens.index(token)
        self[index] = new_token
        return True

    def toggle(self, token, force=None):
        """If `force` is not given, "toggles" `token`, removing it if it’s
        present and adding it if it’s not present. If `force` is True, adds
        token (same as add()). If `force` is False, removes token (same as
        remove()).

        Arguments:
            token (str): The token to be added or removed.
            force (bool, optional): The toggle flag.
        Returns:
            bool: Returns True if `token` is now present, and False otherwise.
        """
        if token in self._tokens:
            if force in (None, False):
                self.remove(token)
                return False
            return True
        elif force in (None, True):
            self.add(token)
            return True
        return False


class NamedNodeMap(MutableMapping):
    """Represents the [DOM] NamedNodeMap."""

    def __init__(self, owner_element):
        """Constructs a NamedNodeMap object.

        Arguments:
            owner_element (Element): An element that is associated with the
                attributes.
        """
        self._owner_element = owner_element
        self._attrib = owner_element.attrib  # type: dict
        self._attr_map = dict()
        for name in self._attrib:
            self._attr_map[name] = Attr(None,
                                        name,
                                        owner_element=owner_element)

    def __contains__(self, name):
        return name in self._attrib

    def __delitem__(self, name):
        """Removes an attribute with the specified `name`.

        Arguments:
            name (str, Attr): The qualified name of the attribute.
        """
        if isinstance(name, Attr):
            name = name.name
        attr = self._attr_map.pop(name, None)
        if attr is not None:
            attr.detach_element()
        del self._attrib[name]

    def __getitem__(self, name):
        """Gets an attribute with the specified `name`.

        Arguments:
            name (str, Attr): The qualified name of the attribute.
        Returns:
            Attr: An attribute object.
        """
        if isinstance(name, Attr):
            name = name.name
        if name not in self._attrib:
            attr = self._attr_map.pop(name, None)
            if attr is not None:
                attr.detach_element()
            raise KeyError(name)
        return self._set_default_named_item(name)

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self._attrib)

    def __repr__(self):
        return repr(self._attrib)

    def __setitem__(self, name, value):
        """Sets an attribute with the specified `name`.

        Arguments:
            name (str): The qualified name of the attribute.
            value (Attr, str, None): An attribute object or an attribute's
                value.
        """
        if value is None or isinstance(value, str):
            if value is None or len(value) == 0:
                if name in self._attrib:
                    del self[name]
                return
            self._attrib[name] = value
            self._set_default_named_item(name)
        elif isinstance(value, Attr):
            if name != value.name:
                raise ValueError("The attribute name '{}' did not match: "
                                 "{}".format(name, repr(value.name)))
            elif value.owner_element is not None:
                if value.owner_element != self._owner_element:
                    raise InUseAttributeError('The attribute is in use')
                return  # already exist
            elif value.value is None or len(value.value) == 0:
                if name in self._attrib:
                    del self[name]
                return
            old_attr = self._attr_map.get(name)
            if old_attr is not None:
                old_attr.detach_element()
            value.attach_element(self._owner_element)
            self._attr_map[name] = value  # replace or add it
        else:
            raise TypeError('Expected Attr or str, got ' + repr(type(value)))

    @property
    def length(self):
        """int: The attribute list's size."""
        return len(self)

    def _set_default_named_item(self, name):
        attr = self._attr_map.get(name)
        if attr is not None and name not in self._attrib:
            attr.detach_element()
            del self._attr_map[name]
            return None
        elif attr is None and name in self._attrib:
            self._attr_map[name] = attr = Attr(
                None,
                name,
                owner_element=self._owner_element)
        return attr

    def get_named_item(self, qualified_name):
        """Gets an attribute given the qualified name.

        Arguments:
            qualified_name (str): The qualified name of the attribute.
        Returns:
            Attr: An attribute object or None.
        """
        return self.get_named_item_ns(None, qualified_name)

    def get_named_item_ns(self, namespace, local_name):
        """Gets an attribute given the namespace URI and local name.

        Arguments:
            namespace (str, None): The namespace URI of the attribute.
            local_name (str): The local name of the attribute.
        Returns:
            Attr: An attribute object or None.
        """
        qname = QualifiedName(namespace, local_name)
        return self.get(qname.name)

    def item(self, index):
        """Returns the attribute list[`index`].

        Arguments:
            index (int): An index position of the attribute list.
        Returns:
            Attr: An attribute object or None.
        """
        keys = list(self.keys())
        try:
            name = keys[index]
            return self[name]
        except IndexError:
            return None

    def keys(self):
        return KeysView(self._attrib.keys())

    def remove_named_item(self, qualified_name):
        """Removes an attribute given the qualified name.

        Arguments:
            qualified_name (str): The qualified name of the attribute.
        Returns:
            Attr: An attribute object to be removed.
        """
        return self.remove_named_item_ns(None, qualified_name)

    def remove_named_item_ns(self, namespace, local_name):
        """Removes an attribute given the namespace URI and local name.

        Arguments:
            namespace (str, None): The namespace URI of the attribute.
            local_name (str): The local name of the attribute.
        Returns:
            Attr: An attribute object to be removed.
        """
        qname = QualifiedName(namespace, local_name)
        attr = self[qname.name]
        if attr is not None:
            del self[qname.name]
        return attr

    def set_named_item(self, attr):
        """Sets an attribute given `attr`.

        Arguments:
            attr (Attr): An attribute to be replaced or added.
        Returns:
            Attr: An attribute object to be removed or None.
        """
        return self.set_named_item_ns(attr)

    def set_named_item_ns(self, attr):
        """Sets an attribute given `attr`.
        Same as NamedNodeMap.set_named_item().

        Arguments:
            attr (Attr): An attribute to be replaced or added.
        Returns:
            Attr: An attribute object to be removed.
        """
        old = self.get(attr.name)
        self[attr.name] = attr
        return old


class Node(ABC):
    """Represents the [DOM] Node."""

    ELEMENT_NODE = 1
    ATTRIBUTE_NODE = 2
    PROCESSING_INSTRUCTION_NODE = 7
    COMMENT_NODE = 8
    DOCUMENT_NODE = 9

    def __init__(self):
        self._owner_document = None

    @property
    @abstractmethod
    def child_nodes(self):
        """list[Node]: The children of this node."""
        raise NotImplementedError

    @property
    def first_child(self):
        """Node: The first child node or None."""
        children = self.child_nodes
        return None if len(children) == 0 else children[0]

    @property
    def last_child(self):
        """Node: The last child node or None."""
        children = self.child_nodes
        return None if len(children) == 0 else children[-1]

    @property
    @abstractmethod
    def next_sibling(self):
        """Node: The first following sibling node or None."""
        raise NotImplementedError

    @property
    @abstractmethod
    def node_name(self):
        """str: A string appropriate for the type of node."""
        raise NotImplementedError

    @property
    @abstractmethod
    def node_type(self):
        """int: The type of node."""
        raise NotImplementedError

    @property
    @abstractmethod
    def node_value(self):
        """str: The value of node."""
        raise NotImplementedError

    @node_value.setter
    @abstractmethod
    def node_value(self, value):
        raise NotImplementedError

    @property
    def owner_document(self):
        """Document: An associated document."""
        if self.node_type == Node.DOCUMENT_NODE:
            return None
        current = self
        while True:
            if current._owner_document is not None:
                return current._owner_document
            parent = current.parent_node  # type: Node
            if parent is None:
                break
            current = parent
        return None

    @property
    def parent_element(self):
        """Element: A parent element."""
        parent = self.parent_node
        if parent is not None and parent.node_type == Node.ELEMENT_NODE:
            return parent
        return None

    @property
    @abstractmethod
    def parent_node(self):
        """Node: A parent node."""
        raise NotImplementedError

    @property
    @abstractmethod
    def previous_sibling(self):
        """Node: The first preceding sibling node or None."""
        raise NotImplementedError

    @property
    @abstractmethod
    def text_content(self):
        """str: The text content of node."""
        raise NotImplementedError

    @text_content.setter
    @abstractmethod
    def text_content(self, text):
        raise NotImplementedError

    @abstractmethod
    def append_child(self, node):
        """Adds a sub-node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        raise NotImplementedError

    def attach_document(self, document):
        """Attaches an associated document.

        Arguments:
            document (Document): A document that is associated with the node.
        Returns:
            bool: Returns True if successful; otherwise False.
        """
        if document is None:
            return False
        self._owner_document = document
        return True

    def detach_document(self):
        """Detaches an associated document.

        Returns:
            Document: A document to be detached.
        """
        owner_document = self._owner_document
        self._owner_document = None
        return owner_document

    def ensure_pre_insertion_validity(self, node, child=None):
        if self.node_type not in (Node.DOCUMENT_NODE, Node.ELEMENT_NODE):
            raise HierarchyRequestError(
                "This node type '{}' does not have children".format(
                    self.__class__.__name__))
        elif child is not None and child not in self:
            raise NotFoundError(
                "This node type '{}' is not a child of this node type "
                "'{}'".format(child.__class__.__name__,
                              self.__class__.__name__))
        elif node.node_type not in (Node.ELEMENT_NODE,
                                    Node.PROCESSING_INSTRUCTION_NODE,
                                    Node.COMMENT_NODE):
            raise HierarchyRequestError(
                "This node type '{}' cannot insert inside nodes of type "
                "'{}'".format(node.__class__.__name__,
                              self.__class__.__name__))
        return True

    def ensure_pre_remove_validity(self, child):
        if self.node_type not in (Node.DOCUMENT_NODE, Node.ELEMENT_NODE):
            raise HierarchyRequestError(
                "This node type '{}' does not have children".format(
                    self.__class__.__name__))
        elif child not in self:
            raise NotFoundError(
                "This node type '{}' is not a child of this node type "
                "'{}'".format(child.__class__.__name__,
                              self.__class__.__name__))
        return True

    @abstractmethod
    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        raise NotImplementedError

    def has_child_nodes(self):
        """Returns True if this node has children; otherwise returns False."""
        return len(self.child_nodes) > 0

    @abstractmethod
    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        raise NotImplementedError

    @abstractmethod
    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node): A reference child node.
        Returns:
            Node: A node to be removed.
        """
        raise NotImplementedError

    @abstractmethod
    def tostring(self, **kwargs):
        """Serializes a node to an encoded string representation of its XML
        tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        Returns:
            bytes: An XML document.
        """
        raise NotImplementedError


class NonDocumentTypeChildNode(ABC):
    """Represents the [DOM] NonDocumentTypeChildNode."""

    @property
    @abstractmethod
    def next_element_sibling(self):
        """Element: The first following sibling element or None."""
        raise NotImplementedError

    @property
    @abstractmethod
    def previous_element_sibling(self):
        """Element: The first preceding sibling element or None."""
        raise NotImplementedError


class NonElementParentNode(ABC):
    """Represents the [DOM] NonElementParentNode."""

    @abstractmethod
    def get_element_by_id(self, element_id, namespaces=None):
        """Finds the first matching sub-element, by id.

        Arguments:
            element_id (str): The id of the element.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            Element: The first matching sub-element. Returns None if there is
                no such element.
        """
        raise NotImplementedError


class ParentNode(ABC):
    """Represents the [DOM] ParentNode."""

    @property
    def child_element_count(self):
        """int: The number of the child elements."""
        return len(self.children)

    @property
    @abstractmethod
    def children(self):
        """list[Element]: A list of the child elements, in document order."""
        raise NotImplementedError

    @property
    def first_element_child(self):
        """Element: The first child element or None."""
        children = self.children
        return children[0] if len(children) > 0 else None

    @property
    def last_element_child(self):
        """Element: The last child element or None."""
        children = self.children
        return children[-1] if len(children) > 0 else None

    @abstractmethod
    def append(self, *nodes):
        """Inserts sub-nodes after the last child node.

        Arguments:
            *nodes (Node, str, ...): A list of nodes to be added.
        """
        raise NotImplementedError

    @abstractmethod
    def prepend(self, *nodes):
        """Inserts sub-nodes before the first child node.

        Arguments:
            *nodes (Node, str, ...): A list of nodes to be added.
        """
        raise NotImplementedError

    def query_selector(self, selectors):
        elements = self.query_selector_all(selectors)
        return elements[0] if len(elements) > 0 else None

    @abstractmethod
    def query_selector_all(self, selectors):
        raise NotImplementedError


class Attr(Node):
    """Represents the [DOM] Attr."""

    def __init__(self, namespace, qualified_name, value=None,
                 owner_element=None):
        """Constructs an Attr object.

        Arguments:
            namespace (str, None): The namespace URI.
            qualified_name (str): The qualified name of the attribute or the
                local part of the qualified name.
            value (str, optional): The attribute's value.
            owner_element (Element, optional): The element that is associated
                with the attribute.
        """
        super().__init__()
        if value is None and owner_element is None:
            raise ValueError("Expected 'value' or 'owner_element'")
        qname = QualifiedName(namespace, qualified_name)
        self._qualified_name = qname.name
        self._local_name = qname.local_name
        self._namespace_uri = qname.namespace_uri
        self._prefix = None
        self._value = value
        self._owner_element = owner_element
        if owner_element is not None:
            if value is not None:
                self.value = value
            if self._namespace_uri is not None:
                for prefix, namespace in owner_element.nsmap.items():
                    if namespace == self._namespace_uri:
                        self._prefix = prefix
                        break

    def __repr__(self):
        return repr({
            'name': self.name,
            'namespace_uri': self.namespace_uri,
            'local_name': self.local_name,
            'prefix': self.prefix,
            'value': self.value,
            'owner_element': self.owner_element,
        })

    @property
    def child_nodes(self):
        """list[Node]: The children of this node."""
        return []

    @property
    def local_name(self):
        """str: The local name of the attribute."""
        return self._local_name

    @property
    def name(self):
        """str: The qualified name of the attribute."""
        return self._qualified_name

    @property
    def namespace_uri(self):
        """str: The namespace URI of the attribute or None."""
        return self._namespace_uri

    @property
    def next_sibling(self):
        """Node: The first following sibling node or None."""
        return None

    @property
    def node_name(self):
        """str: The qualified name of the attribute.
        Same as Attr.name.
        """
        return self.name

    @property
    def node_type(self):
        """int: The type of node."""
        return Node.ATTRIBUTE_NODE

    @property
    def node_value(self):
        """str: The attribute's value."""
        value = self.value
        return value if value is not None else ''

    @node_value.setter
    def node_value(self, value):
        self.value = value

    @property
    def owner_element(self):
        """Element: The element that is associated with the attribute."""
        return self._owner_element

    @property
    def parent_node(self):
        """Node: A parent node."""
        return None

    @property
    def prefix(self):
        """str: The namespace prefix of the attribute or None."""
        return self._prefix

    @property
    def previous_sibling(self):
        """Node: The first preceding sibling node or None."""
        return None

    @property
    def text_content(self):
        """str: The attribute's value."""
        value = self.value
        return value if value is not None else ''

    @text_content.setter
    def text_content(self, value):
        self.value = value

    @property
    def value(self):
        """str: The attribute's value or None."""
        if self._owner_element is not None:
            return self._owner_element.get(self._qualified_name)
        return self._value

    @value.setter
    def value(self, value):
        if self._owner_element is not None:
            if value is None or len(value) == 0:
                if self._qualified_name in self._owner_element.attrib:
                    del self._owner_element.attrib[self._qualified_name]
                return
            self._owner_element.set(self._qualified_name, value)
        else:
            self._value = value

    def append_child(self, node):
        """Adds a node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        self.ensure_pre_insertion_validity(node)

    def attach_element(self, element):
        """Attaches an element to an attribute object.

        Arguments:
            element (Element): An element that is associated with the
                attribute.
        Returns:
            bool: Returns True if successful; otherwise False.
        """
        if element is None or self._owner_element is not None:
            return False
        new_value = self._value
        self._value = None
        self._owner_element = element
        if new_value is not None:
            self.value = new_value
        return True

    def detach_element(self):
        """Detaches an element from an attribute object.

        Returns:
            Node: An element to be detached.
        """
        if self._owner_element is None:
            return None
        self._value = self.value
        owner_element = self._owner_element
        self._owner_element = None
        return owner_element

    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        return self

    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        self.ensure_pre_insertion_validity(node, child)

    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        self.ensure_pre_remove_validity(child)

    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node): A reference child node.
        Returns:
            Node: A node to be removed.
        """
        self.ensure_pre_insertion_validity(node, child)
        self.ensure_pre_remove_validity(child)

    def tostring(self, **kwargs):
        """Serializes the attribute's value to a string.

        Arguments:
            **kwargs: Reserved.
        Returns:
            bytes: An attribute's value.
        """
        value = self.value
        if value is None:
            value = ''
        return value.encode()


class CharacterData(Node, NonDocumentTypeChildNode):
    """Represents the [DOM] CharacterData."""

    @property
    def child_nodes(self):
        """list[Node]: The children of this node."""
        return []

    @property
    @abstractmethod
    def data(self):
        """str: The value of node."""
        raise NotImplementedError

    @data.setter
    @abstractmethod
    def data(self, data):
        raise NotImplementedError

    @property
    def length(self):
        """int: A length of the data."""
        return len(self.data)


class Comment(etree.CommentBase, CharacterData):
    """Represents the [DOM] Comment."""

    def _init(self):
        Node.__init__(self)

    @property
    def data(self):
        """str: The value of node."""
        return self.text

    @data.setter
    def data(self, data):
        self.text = data

    @property
    def next_element_sibling(self):
        """Element: The first following sibling element or None."""
        nodes = self.itersiblings()
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def next_sibling(self):
        """Node: The first following sibling node or None."""
        return self.getnext()

    @property
    def node_name(self):
        """str: '#comment'."""
        return '#comment'

    @property
    def node_type(self):
        """int: The type of node."""
        return Node.COMMENT_NODE

    @property
    def node_value(self):
        """str: The value of node."""
        return self.data

    @node_value.setter
    def node_value(self, value):
        self.data = value

    @property
    def parent_node(self):
        """Node: A parent node."""
        return self.getparent()

    @property
    def previous_element_sibling(self):
        """Element: The first preceding sibling element or None."""
        nodes = self.itersiblings(preceding=True)
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def previous_sibling(self):
        """Node: The first preceding sibling node or None."""
        return self.getprevious()

    @property
    def text_content(self):
        """str: The text content of node."""
        return self.data

    @text_content.setter
    def text_content(self, text):
        self.data = text

    def addnext(self, node):
        """Reimplemented from lxml.etree.CommentBase.addnext().

        Adds the node as a following sibling directly after this node.
        """
        if node.node_type not in (Node.ELEMENT_NODE,
                                  Node.PROCESSING_INSTRUCTION_NODE,
                                  Node.COMMENT_NODE):
            raise HierarchyRequestError(
                "This node type '{}' cannot insert as a sibling node of type "
                "'{}'".format(node.__class__.__name__,
                              self.__class__.__name__))
        node.attach_document(self.owner_document)
        super().addnext(node)

    def addprevious(self, node):
        """Reimplemented from lxml.etree.CommentBase.addprevious().

        Adds the node as a preceding sibling directly before this node.
        """
        if node.node_type not in (Node.ELEMENT_NODE,
                                  Node.PROCESSING_INSTRUCTION_NODE,
                                  Node.COMMENT_NODE):
            raise HierarchyRequestError(
                "This node type '{}' cannot insert as a sibling node of type "
                "'{}'".format(node.__class__.__name__,
                              self.__class__.__name__))
        node.attach_document(self.owner_document)
        super().addprevious(node)

    def append(self, node):
        """Reimplemented from lxml.etree.CommentBase.append().

        Adds a sub-node to the end of this node.
        """
        self.ensure_pre_insertion_validity(node)

    def append_child(self, node):
        """Adds a node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        self.ensure_pre_insertion_validity(node)

    def extend(self, nodes):
        """Reimplemented from lxml.etree.CommentBase.extend().

        Extends the current children by the nodes in the iterable.
        """
        for node in nodes:
            self.ensure_pre_insertion_validity(node)

    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        root = self.getroottree().getroot()
        if root is None:
            root = self
        return root

    def insert(self, index, node):
        """Reimplemented from lxml.etree.CommentBase.insert().

        Inserts a sub-node at the given position in this node.
        """
        _ = index
        self.ensure_pre_insertion_validity(node)

    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        self.ensure_pre_insertion_validity(node, child)

    def remove(self, node):
        """Reimplemented from lxml.etree.CommentBase.remove().

        Removes a matching sub-node. Unlike the find methods, this method
        compares nodes based on identity, not on tag value or contents.
        """
        self.ensure_pre_remove_validity(node)

    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        self.ensure_pre_remove_validity(child)

    def replace(self, old_node, new_node):
        """Reimplemented from lxml.etree.CommentBase.replace().

        Replaces a sub-node with the node passed as second argument.
        """
        self.ensure_pre_insertion_validity(new_node, old_node)
        self.ensure_pre_remove_validity(old_node)

    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node): A reference child node.
        Returns:
            Node: A node to be removed.
        """
        self.ensure_pre_insertion_validity(node, child)
        self.ensure_pre_remove_validity(child)

    def tostring(self, **kwargs):
        """Serializes a comment to an encoded string representation of its
        XML tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        Returns:
            bytes: An XML document.
        """
        return etree.tostring(self, **kwargs)


class Element(etree.ElementBase, Node, ParentNode, NonDocumentTypeChildNode):
    """Represents the [DOM] Element."""

    SVG_NAMESPACE_URI = 'http://www.w3.org/2000/svg'
    XHTML_NAMESPACE_URI = 'http://www.w3.org/1999/xhtml'
    XLINK_NAMESPACE_URI = 'http://www.w3.org/1999/xlink'
    XML_NAMESPACE_URI = 'http://www.w3.org/XML/1998/namespace'

    XML_LANG = '{{{0}}}lang'.format(XML_NAMESPACE_URI)

    DESCRIPTIVE_ELEMENTS = ['desc', 'metadata', 'title']

    STRUCTURAL_ELEMENTS = ['defs', 'g', 'svg', 'symbol', 'use']

    STRUCTURALLY_EXTERNAL_ELEMENTS = \
        ['audio', 'foreignObject', 'iframe', 'image', 'script', 'use', 'video']

    CONTAINER_ELEMENTS = \
        ['a', 'clipPath', 'defs', 'g', 'marker', 'mask', 'pattern', 'svg',
         'switch', 'symbol', 'unknown']

    GRAPHICS_ELEMENTS = \
        ['audio', 'canvas', 'circle', 'ellipse', 'foreignObject', 'iframe',
         'image', 'line', 'mesh', 'path', 'polygon', 'polyline', 'rect',
         'text', 'textPath', 'tspan', 'video']

    GRAPHICS_REFERENCING_ELEMENTS = \
        ['audio', 'iframe', 'image', 'mesh', 'use', 'video']

    RENDERABLE_ELEMENTS = \
        ['a', 'audio', 'canvas', 'circle', 'ellipse', 'foreignObject', 'g',
         'iframe', 'image', 'line', 'mesh', 'path', 'polygon', 'polyline',
         'rect', 'svg', 'switch', 'text', 'textPath', 'tspan', 'unknown',
         'use', 'video']

    SHAPE_ELEMENTS = \
        ['circle', 'ellipse', 'line', 'mesh', 'path', 'polygon', 'polyline',
         'rect']

    TEXT_CONTENT_ELEMENTS = ['text', 'tspan']
    # TODO: add 'textPath' element to TEXT_CONTENT_ELEMENTS.

    TEXT_CONTENT_CHILD_ELEMENTS = ['textPath', 'tspan']

    TRANSFORMABLE_ELEMENTS = \
        ['a', 'defs', 'foreignObject', 'g', 'svg', 'switch',
         'use', ] + GRAPHICS_ELEMENTS
    # TODO: add 'clipPath' element to TRANSFORMABLE_ELEMENTS.

    RE_DIGIT_SEQUENCE_SPLITTER = re.compile(r'\s*,\s*|\s+')

    def _init(self):
        Node.__init__(self)
        self._attributes = NamedNodeMap(self)
        self._class_list = DOMTokenList(self, 'class')

    @property
    def attributes(self):
        """NamedNodeMap: A dictionary of an element attributes.

        Examples:
            >>> parser = SVGParser()
            >>> root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
            >>> root.attributes['viewBox'] = '0 0 600 400'
            >>> attr = parser.create_attribute_ns('http://www.w3.org/XML/1998/namespace', 'lang')
            >>> attr.value = 'ja'
            >>> root.attributes.set_named_item_ns(attr)
            >>> root.attributes
            {'viewBox': '0 0 600 400', '{http://www.w3.org/XML/1998/namespace}lang': 'ja'}
            >>> root.tostring()
            b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" xml:lang="ja"/>'
        """
        return self._attributes

    @property
    def child_nodes(self):
        """list[Node]: The children of this node."""
        return list(self)

    @property
    def children(self):
        """list[Element]: A list of the child elements, in document order."""
        children = self.child_nodes
        return [child for child in children
                if child.node_type == Node.ELEMENT_NODE]

    @property
    def class_list(self):
        """DOMTokenList: A list of classes."""
        return self._class_list

    @property
    def class_name(self):
        """str: Reflects the 'class' attribute."""
        return self.get('class', '')

    @class_name.setter
    def class_name(self, value):
        self.set('class', value)

    @property
    def id(self):
        """str: Reflects the 'id' attribute."""
        return self.get('id', '')

    @id.setter
    def id(self, value):
        self.set('id', value)

    @property
    def local_name(self):
        """str: The local part of the qualified name of an element."""
        return self.qname.localname

    @property
    def namespace_uri(self):
        return self.nsmap.get(self.prefix)

    @property
    def next_element_sibling(self):
        """Element: The first following sibling element or None."""
        nodes = self.itersiblings()
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def next_sibling(self):
        """Node: The first following sibling node or None."""
        return self.getnext()

    @property
    def node_name(self):
        """str: Same as Element.tag_name."""
        return self.tag_name

    @property
    def node_type(self):
        """int: The type of node."""
        return Node.ELEMENT_NODE

    @property
    def node_value(self):
        """str: The value of node."""
        return None

    @node_value.setter
    def node_value(self, value):
        pass  # do nothing

    @property
    def parent_node(self):
        """Node: A parent node."""
        return self.getparent()

    @property
    def previous_element_sibling(self):
        """Element: The first preceding sibling element or None."""
        nodes = self.itersiblings(preceding=True)
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def previous_sibling(self):
        """Node: The first preceding sibling node or None."""
        return self.getprevious()

    @property
    def qname(self):
        """lxml.etree.QName: The qualified XML name of an element."""
        qname = etree.QName(self)
        return qname

    @property
    def tag_name(self):
        """str: The qualified name of an element."""
        prefix = self.prefix
        local_name = self.local_name
        if prefix is not None:
            return prefix + ':' + local_name
        return local_name

    @property
    def text_content(self):
        """str: The text content of node."""
        # See https://dom.spec.whatwg.org/#dom-node-textcontent
        local_name = self.local_name
        if local_name in Element.DESCRIPTIVE_ELEMENTS:
            return self.text
        elif local_name in Element.TEXT_CONTENT_ELEMENTS:
            chars = Element._get_text_content(self)
            return ''.join(chars)
        return None

    @text_content.setter
    def text_content(self, text):
        for child in iter(self):
            self.remove(child)
        self.text = text

    @staticmethod
    def _get_text_content(element):
        # See https://dom.spec.whatwg.org/#dom-node-textcontent
        chars = list()
        if element.text is not None:
            chars.append(element.text)

        for child in iter(element):
            if child.node_type != Node.ELEMENT_NODE:
                continue
            local_name = child.local_name
            if local_name in Element.TEXT_CONTENT_ELEMENTS:
                contents = Element._get_text_content(child)
                chars.extend(contents)
                if (local_name in Element.TEXT_CONTENT_CHILD_ELEMENTS
                        and child.tail is not None):
                    chars.append(child.tail)
        return chars

    def addnext(self, node):
        """Reimplemented from lxml.etree.ElementBase.addnext().

        Adds the node as a following sibling directly after this node.
        """
        if node.node_type not in (Node.ELEMENT_NODE,
                                  Node.PROCESSING_INSTRUCTION_NODE,
                                  Node.COMMENT_NODE):
            raise HierarchyRequestError(
                "This node type '{}' cannot insert as a sibling node of type "
                "'{}'".format(node.__class__.__name__,
                              self.__class__.__name__))
        node.attach_document(self.owner_document)
        super().addnext(node)

    def addprevious(self, node):
        """Reimplemented from lxml.etree.ElementBase.addprevious().

        Adds the node as a preceding sibling directly before this node.
        """
        if node.node_type not in (Node.ELEMENT_NODE,
                                  Node.PROCESSING_INSTRUCTION_NODE,
                                  Node.COMMENT_NODE):
            raise HierarchyRequestError(
                "This node type '{}' cannot insert as a sibling node of type "
                "'{}'".format(node.__class__.__name__,
                              self.__class__.__name__))
        node.attach_document(self.owner_document)
        super().addprevious(node)

    def append(self, *nodes):
        """Inserts sub-nodes after the last child node.

        Arguments:
            *nodes (Node, str, ...): A list of nodes to be added.
        """
        data = ''
        target = self
        for node in nodes:
            if isinstance(node, str):
                data += node
                continue
            self.ensure_pre_insertion_validity(node)
            if len(data) > 0:
                tail = False if target == self else True
                node_append_data(target, data, tail)
                data = ''
            node.attach_document(self.owner_document)
            super().append(node)
            target = node

        if len(data) > 0:
            tail = False if target == self else True
            node_append_data(target, data, tail)

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
        if not super().attach_document(document):
            return False
        for child in self:
            child.attach_document(document)
        return True

    def create_sub_element(self, local_name, index=None, attrib=None,
                           nsmap=None, **_extra):
        """[DEPRECATED]
        Creates a sub-element instance, and adds to the end of this element.
        See also Element.create_sub_element_ns(), Document.create_element(),
        Document.create_element_ns(), SVGParser.create_element() and
        SVGParser.create_element_ns().

        Arguments:
            local_name (str): A local name of an element to be created.
            index (int, optional): If specified, inserts a sub-element at the
                given position in this element.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        """
        # TODO: remove Element.create_sub_element().
        element = self.makeelement(local_name,
                                   attrib=attrib,
                                   nsmap=nsmap,
                                   **_extra)
        if index is not None:
            self.insert(index, element)
        else:
            self.append(element)
        return element

    def create_sub_element_ns(self, namespace, local_name, index=None,
                              attrib=None, nsmap=None, **_extra):
        """[DEPRECATED]
        Creates a sub-element instance with the specified namespace URI,
        and adds to the end of this element.
        See also Element.create_sub_element(), Document.create_element(),
        Document.create_element_ns(), SVGParser.create_element() and
        SVGParser.create_element_ns().

        Arguments:
            namespace (str, None): The namespace URI to associated with
                the element.
            local_name (str): A local name of an element to be created.
            index (int, optional): If specified, inserts a sub-element at the
                given position in this element.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        Examples:
            >>> parser = SVGParser()
            >>> root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg', nsmap={'html': 'http://www.w3.org/1999/xhtml'})
            >>> video = root.create_sub_element_ns('http://www.w3.org/1999/xhtml', 'video')
            >>> print(root.tostring(pretty_print=True).decode())
            <svg xmlns:html="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/2000/svg">
              <html:video/>
            </svg>
        """
        # TODO: remove Element.create_sub_element_ns().
        qname = QualifiedName(namespace, local_name)
        element = self.create_sub_element(qname.name,
                                          index=index,
                                          attrib=attrib,
                                          nsmap=nsmap,
                                          **_extra)
        return element

    def detach_document(self):
        """Reimplemented from Node.detach_document().

        Detaches an associated document.

        Returns:
            Document: A document to be detached.
        """
        owner_document = super().detach_document()
        for child in self:
            child.detach_document()
        return owner_document

    def extend(self, nodes):
        """Reimplemented from lxml.etree.ElementBase.extend().

        Extends the current children by the nodes in the iterable.
        """
        owner_document = self.owner_document
        for node in nodes:
            self.ensure_pre_insertion_validity(node)
            node.attach_document(owner_document)
        super().extend(nodes)

    def get_attribute(self, qualified_name):
        """Returns an attribute's value with the specified name.

        Arguments:
            qualified_name (str): The qualified name of the attribute.
        Returns:
            str: The attribute's value or None.
        """
        return self.get_attribute_ns(None, qualified_name)

    def get_attribute_names(self):
        """Returns a list of attribute names in order.

        Returns:
            list[str]: A list of attribute names.
        """
        return sorted(self.attrib.keys())

    def get_attribute_node(self, qualified_name):
        """Returns an attribute given the qualified name.

        Arguments:
            qualified_name (str): The qualified name of the attribute.
        Returns:
            Attr: An attribute object or None.
        """
        return self.attributes.get_named_item(qualified_name)

    def get_attribute_node_ns(self, namespace, local_name):
        """Returns an attribute given the namespace URI and local name.

        Arguments:
            namespace (str, None): The namespace URI of the attribute.
            local_name (str): The local name of the attribute.
        Returns:
            Attr: An attribute object or None.
        """
        return self.attributes.get_named_item_ns(namespace, local_name)

    def get_attribute_ns(self, namespace, local_name):
        """Returns an attribute's value with the specified namespace and name.

        Arguments:
            namespace (str, None): The namespace URI.
            local_name (str): The local name of the attribute.
        Returns:
            str: The attribute's value or None.
        """
        qname = QualifiedName(namespace, local_name)
        return self.get(qname.name)

    def get_computed_geometry(self):
        return {}  # override with a subclass

    def get_computed_style(self):
        """Gets the presentation attributes from ancestor elements."""
        # TODO: implement Window.get_computed_style()
        style = self.get_inherited_style()

        # 'font-feature-settings' property
        style['font-feature-settings'] = CSSUtils.parse_font_feature_settings(
            style['font-feature-settings'])

        # 'font-size' property
        style['font-size'] = CSSUtils.compute_font_size(
            self,
            inherited_style=style)

        # 'font-size-adjust' property
        style['font-size-adjust'] = CSSUtils.compute_font_size_adjust(style)

        # 'font-synthesis' property
        # Value: none | [weight || style]
        items = style['font-synthesis'].split()
        items = [x for x in items if x in ['weight', 'style', 'none']]
        if 'none' in items and len(items) != 1:
            items = ['none']
        style['font-synthesis'] = items

        # 'font-weight' property
        style['font-weight'] = CSSUtils.compute_font_weight(
            self,
            inherited_style=style)

        # 'line-height' property
        style['line-height'] = CSSUtils.compute_line_height(self, style)

        # 'inline-size' property
        # Value: <length> | <percentage> | <number>
        # Initial: 0
        # Percentages: Refer to the width (for horizontal text) or height
        #  (for vertical text) of the current SVG viewport
        inline_size = style['inline-size']
        writing_mode = style['writing-mode']
        mode = SVGLength.DIRECTION_HORIZONTAL if writing_mode in [
            'horizontal-tb', 'lr', 'lr-tb', 'rl', 'rl-tb'
        ] else SVGLength.DIRECTION_VERTICAL
        style['inline-size'] = SVGLength(inline_size).value(direction=mode)

        # 'stroke-width' property
        # Value: <percentage> | <length>
        # Initial: 1
        # Percentages: refer to the size of the current SVG viewport
        stroke_width = style['stroke-width']
        style['stroke-width'] = SVGLength(
            stroke_width,
            context=self).value(direction=SVGLength.DIRECTION_UNSPECIFIED)

        # 'tab-size' property
        # Value: <percentage> | <length>
        # Initial: 8
        # See https://drafts.csswg.org/css-text-3/#tab-size-property
        tab_size = style['tab-size']
        style['tab-size'] = SVGLength(
            tab_size,
            context=self).value(direction=SVGLength.DIRECTION_UNSPECIFIED)

        # geometry properties
        geometry = self.get_computed_geometry()
        style.update(geometry)
        return style

    def get_inherited_style(self):
        def _update_font_prop(_value, _style, _inherited_style):
            _other = CSSUtils.parse_font(_value)
            for _key in _other:
                if _key not in _style:
                    _style[_key] = _other[_key]
                    if _key == 'font-variant':
                        _update_font_variant_prop(_other[_key],
                                                  _style,
                                                  _inherited_style)
            _inherited_style.pop('font-style', None)
            _inherited_style.pop('font-variant', None)
            _inherited_style.pop('font-weight', None)
            _inherited_style.pop('font-stretch', None)
            _inherited_style.pop('font-size', None)
            _inherited_style.pop('line-height', None)
            _inherited_style.pop('font-size-adjust', None)
            _inherited_style.pop('font-kerning', None)
            _inherited_style.pop('font-language-override', None)
            _inherited_style.pop('font-family', None)
            _inherited_style.pop('font', None)

        def _update_font_variant_prop(_value, _style, _inherited_style):
            _other = CSSUtils.parse_font_variant(_value)
            for _key in _other:
                if _key not in _style:
                    _style[_key] = _other[_key]
            _inherited_style.pop('font-variant-alternates', None)
            _inherited_style.pop('font-variant-caps', None)
            _inherited_style.pop('font-variant-east-asian', None)
            _inherited_style.pop('font-variant-ligatures', None)
            _inherited_style.pop('font-variant-numeric', None)
            _inherited_style.pop('font-variant-position', None)
            _inherited_style.pop('font-variant', None)

        # See https://svgwg.org/svg2-draft/propidx.html
        style = dict()
        non_inherited_props = \
            {'alignment-baseline': 'baseline',
             'baseline-shift': '0',
             'clip': 'auto',
             'clip-path': 'none',
             'display': 'inline',
             'dominant-baseline': 'auto',
             'filter': 'none',
             'flood-color': 'black',
             'flood-opacity': '1',
             'inline-size': '0',
             'lighting-color': 'white',
             'mask': 'no',
             'opacity': '1',
             'overflow': 'visible',
             'stop-color': 'black',
             'stop-opacity': '1',
             'text-decoration': 'none',
             'transform': 'none',
             'unicode-bidi': 'normal',
             'vector-effect': 'none',
             }
        for key in iter(non_inherited_props):
            style.setdefault(key,
                             self.get(key, non_inherited_props[key]))

        inherited_props = \
            {'clip-rule': 'nonzero',
             'color': 'black',  # depends on user agent
             'color-interpolation': 'sRGB',
             'color-rendering': 'auto',
             'cursor': 'auto',
             'direction': 'ltr',
             'fill': 'black',
             'fill-opacity': '1',
             'fill-rule': 'nonzero',
             'font': None,
             'font-family': None,
             'font-feature-settings': 'normal',
             'font-kerning': Font.CSS_DEFAULT_FONT_KERNING,
             'font-language-override': Font.CSS_DEFAULT_FONT_LANGUAGE_OVERRIDE,
             'font-size': Font.CSS_DEFAULT_FONT_SIZE,
             'font-size-adjust': Font.CSS_DEFAULT_FONT_SIZE_ADJUST,
             'font-stretch': Font.CSS_DEFAULT_FONT_STRETCH,
             'font-style': Font.CSS_DEFAULT_FONT_STYLE,
             'font-synthesis': 'weight style',
             'font-variant': Font.CSS_DEFAULT_FONT_VARIANT,
             'font-variant-alternates': ['normal'],
             'font-variant-caps': 'normal',
             'font-variant-east-asian': ['normal'],
             'font-variant-ligatures': ['normal'],
             'font-variant-numeric': ['normal'],
             'font-variant-position': 'normal',
             'font-weight': Font.CSS_DEFAULT_FONT_WEIGHT,
             # 'glyph-orientation-vertical': 'auto',  # deprecated
             'image-rendering': 'auto',
             'lang': None,
             'letter-spacing': 'normal',
             'line-height': Font.CSS_DEFAULT_LINE_HEIGHT,
             'marker': None,
             'marker-end': 'none',
             'marker-mid': 'none',
             'marker-start': 'none',
             'paint-order': 'normal',
             'pointer-events': 'visiblePainted',
             'shape-rendering': 'auto',
             'stroke': 'none',
             'stroke-dasharray': 'none',
             'stroke-dashoffset': '0',
             'stroke-linecap': 'butt',
             'stroke-linejoin': 'miter',
             'stroke-miterlimit': '4',
             'stroke-opacity': '1',
             'stroke-width': '1',
             'tab-size': '8',
             'text-anchor': 'start',
             'text-orientation': 'mixed',
             'text-rendering': 'auto',
             'visibility': 'visible',
             'white-space': 'normal',
             'word-spacing': 'normal',
             'writing-mode': 'horizontal-tb',
             Element.XML_LANG: None,
             }
        # 'color-interpolation-filters', 'font-feature-settings',
        # 'gradientTransform', 'glyph-orientation-horizontal',
        # 'isolation',
        # 'patternTransform',
        # 'solid-color', 'solid-opacity',
        # 'text-align', 'text-align-all', 'text-align-last',
        # 'text-decoration-color', 'text-decoration-line',
        # 'text-decoration-style', 'text-indent',
        # 'text-overflow',
        # 'transform', 'transform-box', 'transform-origin',
        # 'vertical-align',
        css_rules = get_css_rules(self)
        element = self
        while element is not None:
            css_style, css_style_important = get_css_style(element, css_rules)
            css_style.update(element.attrib)
            _style = css_style.pop('style', None)
            if _style is not None:
                css_style.update(style_to_dict(_style))
            css_style.update(css_style_important)
            for key in iter(list(inherited_props.keys())):
                value = css_style.get(key)
                if value is not None and value not in ['inherit']:
                    if key == 'font':
                        # 'font' shorthand property
                        style[key] = value
                        _update_font_prop(value, style, inherited_props)
                    elif key == 'font-family':
                        # 'font-family' property
                        style[key] = CSSUtils.parse_font_family(value)
                        del inherited_props[key]
                    elif key == 'font-variant':
                        # 'font-variant' shorthand property
                        style[key] = value
                        _update_font_variant_prop(value, style,
                                                  inherited_props)
                    elif key == 'marker':
                        # TODO: parse the 'marker' shorthand property.
                        raise NotImplementedError
                    else:
                        if key in ['font-variant-alternates',
                                   'font-variant-east-asian',
                                   'font-variant-ligatures',
                                   'font-variant-numeric']:
                            style[key] = value.split()
                        else:
                            style[key] = value
                        inherited_props.pop(key, None)
            # 'display' property
            display = css_style.get('display')
            if display is not None and display == 'none':
                style['display'] = 'none'
            element = element.getparent()

        for key, value in iter(inherited_props.items()):
            if value is not None:
                style[key] = value

        font_family = style.get('font-family')
        if font_family is None:
            style['font-family'] = CSSUtils.parse_font_family(
                Font.default_font_family)

        return style

    def get_elements_by_class_name(self, class_names, nsmap=None):
        """Finds all matching sub-elements, by class names.

        Arguments:
            class_names (str): A list of class names that are separated by
                whitespace.
            nsmap (dict, optional): The XPath prefixes in the path expression.
        Returns:
            list[Element]: A list of elements.
        """
        return get_elements_by_class_name(self,
                                          class_names,
                                          nsmap=nsmap)

    def get_elements_by_local_name(self, local_name, nsmap=None):
        """Finds all matching sub-elements, by the local name.

        Arguments:
            local_name (str): The local name.
            nsmap (dict, optional): The XPath prefixes in the path expression.
        Returns:
            list[Element]: A list of elements.
        """
        return self.xpath('.//*[local-name() = $local_name]',
                          namespaces=nsmap,
                          local_name=local_name)

    def get_elements_by_tag_name(self, qualified_name, nsmap=None):
        """Finds all matching sub-elements, by the qualified name.

        Arguments:
            qualified_name (str): The qualified name or '*'.
            nsmap (dict, optional): The XPath prefixes in the path expression.
        Returns:
            list[Element]: A list of elements.
        """
        return get_elements_by_tag_name(self,
                                        qualified_name,
                                        nsmap=nsmap)

    def get_elements_by_tag_name_ns(self, namespace, local_name, nsmap=None):
        """Finds all matching sub-elements, by the namespace URI and the local
        name.

        Arguments:
            namespace (str, None): The namespace URI, '*' or None.
            local_name (str): The local name or '*'.
            nsmap (dict, optional): The XPath prefixes in the path expression.
        Returns:
            list[Element]: A list of elements.
        """
        return get_elements_by_tag_name_ns(self,
                                           namespace,
                                           local_name,
                                           nsmap=nsmap)

    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        root = self.getroottree().getroot()
        if root is None:
            root = self
        return root

    def has_attribute(self, qualified_name):
        """Returns True if an attribute with the specified name exists;
        otherwise returns False.

        Arguments:
            qualified_name (str): The name of the attribute.
        Returns:
            bool: Returns True if the attribute exists, else False.
        """
        return self.has_attribute_ns(None, qualified_name)

    def has_attribute_ns(self, namespace, local_name):
        """Returns True if an attribute with the specified namespace and name
        exists; otherwise returns False.

        Arguments:
            namespace (str, None): The namespace URI.
            local_name (str): The local name of the attribute.
        Returns:
            bool: Returns True if the attribute exists, else False.
        """
        qname = QualifiedName(namespace, local_name)
        return qname.name in self.attrib

    def has_attributes(self):
        """Returns True if attribute list is not empty; otherwise returns
        False.
        """
        return len(self.attrib) > 0

    def insert(self, index, node):
        """Reimplemented from lxml.etree.ElementBase.insert().

        Inserts a sub-node at the given position in this node.
        """
        self.ensure_pre_insertion_validity(node)
        node.attach_document(self.owner_document)
        super().insert(index, node)

    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        node_insert_before(self, node, child)
        return node

    def iscontainer(self):
        """Returns True if this element is container element."""
        return self.local_name in Element.CONTAINER_ELEMENTS

    def isdisplay(self):
        style = self.get_inherited_style()
        return False if style['display'] == 'none' else True

    def isgraphics(self):
        """Returns True if this element is graphics element."""
        return self.local_name in Element.GRAPHICS_ELEMENTS

    def isrenderable(self):
        """Returns True if this element is renderable element."""
        return self.local_name in Element.RENDERABLE_ELEMENTS

    def isshape(self):
        """Returns True if this element is shape element."""
        return self.local_name in Element.SHAPE_ELEMENTS

    def istext(self):
        """Returns True if this element is text content element."""
        return self.local_name in Element.TEXT_CONTENT_ELEMENTS

    def istransformable(self):
        """Returns True if this element is transformable element."""
        return self.local_name in Element.TRANSFORMABLE_ELEMENTS

    def prepend(self, *nodes):
        """Inserts sub-nodes before the first child node.

        Arguments:
            *nodes (Node, str, ...): A list of nodes to be added.
        """
        first_child = self.first_child
        data = ''
        target = self
        text = '' if self.text is None else self.text
        if len(text) > 0:
            self.text = ''
        for node in nodes:
            if isinstance(node, str):
                data += node
                continue
            self.ensure_pre_insertion_validity(node)
            if len(data) > 0:
                tail = False if target == self else True
                node_prepend_data(target, data, tail)
                data = ''
            node.attach_document(self.owner_document)
            if first_child is None:
                super().append(node)
                first_child = node
            else:
                first_child.addprevious(node)
            target = node

        tail = False if target == self else True
        if len(data) > 0:
            node_prepend_data(target, data, tail)
        if len(text) > 0:
            node_append_data(target, text, tail)

    def query_selector_all(self, selectors):
        nsmap = self.nsmap.copy()
        uri = nsmap.pop(None, None)
        if uri is not None:
            nsmap['svg'] = uri
        sel = cssselect.CSSSelector(selectors, namespaces=nsmap)
        return sel(self)

    def remove(self, node=None):
        """Removes a matching sub-node. Unlike the find methods, this method
        compares nodes based on identity, not on tag value or contents.

        Arguments:
            node (Node, optional): A node to be removed.
        """
        if node is None:
            parent = self.getparent()
            if parent is not None:
                parent.remove(self)
            return
        self.ensure_pre_remove_validity(node)
        super().remove(node)

    def remove_attribute(self, qualified_name):
        """Removes an attribute with the specified name.

        Arguments:
            qualified_name (str): The qualified name of the attribute.
        """
        self.remove_attribute_ns(None, qualified_name)

    def remove_attribute_node(self, attr):
        """Removes an attribute given `attr`.

        Arguments:
            attr (Attr): An attribute to be removed.
        Returns:
            Attr: An attribute object to be removed.
        """
        attr = self.attributes.remove_named_item_ns(attr.namespace_uri,
                                                    attr.local_name)
        if attr is not None:
            attr.detach_element()
        return attr

    def remove_attribute_ns(self, namespace, local_name):
        """Removes an attribute with the specified namespace and name.

        Arguments:
            namespace (str, None): The namespace URI.
            local_name (str): The local name of the attribute.
        """
        try:
            attr = self.attributes.remove_named_item_ns(namespace, local_name)
            if attr is not None:
                attr.detach_element()
        except KeyError:
            pass

    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        self.remove(child)
        return child

    def replace(self, old_node, new_node):
        """Reimplemented from lxml.etree.ElementBase.replace().

        Replaces a sub-node with the node passed as second argument.
        """
        self.ensure_pre_insertion_validity(new_node, old_node)
        self.ensure_pre_remove_validity(old_node)
        new_node.attach_document(self.owner_document)
        super().replace(old_node, new_node)

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

    def set_attribute(self, qualified_name, value):
        """Sets an attribute with the specified name.

        Arguments:
            qualified_name (str): The qualified name of the attribute.
            value (str): The attribute's value.
        """
        self.set_attribute_ns(None, qualified_name, value)

    def set_attribute_node(self, attr):
        """Sets an attribute given `attr`.

        Arguments:
            attr (Attr): An attribute to be replaced or added.
        Returns:
            Attr: An attribute object to be removed or None.
        """
        return self.attributes.set_named_item(attr)

    def set_attribute_node_ns(self, attr):
        """Sets an attribute given `attr`.
        Same as Element.set_attribute_node().

        Arguments:
            attr (Attr): An attribute to be replaced or added.
        Returns:
            Attr: An attribute object to be removed or None.
        """
        return self.attributes.set_named_item_ns(attr)

    def set_attribute_ns(self, namespace, qualified_name, value):
        """Sets an attribute with the specified namespace and name.

        Arguments:
            namespace (str, None): The namespace URI.
            qualified_name (str): The qualified name of the attribute.
            value (str): The attribute's value.
        """
        qname = QualifiedName(namespace, qualified_name)
        self.attributes[qname.name] = value

    def toggle_attribute(self, qualified_name, force=None):
        """If `force` is not given, "toggles" `qualified_name`, removing it if
        it’s present and adding it if it’s not present. If `force` is True,
        adds attribute (same as set()). If `force` is False, removes attribute
        (same as remove_attribute()).

        Arguments:
            qualified_name (str): The qualified name of the attribute.
            force (bool, optional): The toggle flag.
        Returns:
            bool: Returns True if specified attribute is now present, and
                False otherwise.
        """
        if qualified_name in self.attrib:
            if force in (None, False):
                self.remove_attribute(qualified_name)
                return False
            return True
        elif force in (None, True):
            self.set(qualified_name, '')
            return True
        return False

    def tostring(self, **kwargs):
        """Serializes an element to an encoded string representation of its
        XML tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        Returns:
            bytes: An XML document.
        """
        return etree.tostring(self, **kwargs)


class ElementCSSInlineStyle(Element):
    """Represents the [cssom] ElementCSSInlineStyle."""

    def _init(self):
        super()._init()
        self._style = CSSStyleDeclaration(owner_node=self, inline_style=True)

    @property
    def style(self):
        """CSSStyleDeclaration: A CSS declaration block object.

        Examples:
            >>> parser = SVGParser()
            >>> g = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
            >>> g.attributes['style'] = 'fill: none; stroke: red;'
            >>> g.style['fill']
            'none'
            >>> g.style['stroke']
            'red'
            >>> g.style['stroke'] = 'blue'
            >>> g.style['stroke-width'] = '3'
            >>> g.attributes['style'].value
            'fill: none; stroke-width: 3; stroke: blue;'
        """
        return self._style


class LinkStyle(Element):
    """Represents the [cssom] LinkStyle."""

    @property
    def sheet(self):
        """StyleSheet: An associated CSS style sheet."""
        css_style_sheet = get_css_style_sheet_from_element(self)
        return css_style_sheet


class ProcessingInstruction(etree.PIBase, CharacterData):
    """Represents the [DOM] ProcessingInstruction."""

    def _init(self):
        Node.__init__(self)

    @property
    def data(self):
        """str: The value of node."""
        return self.text

    @data.setter
    def data(self, data):
        self.text = data

    @property
    def next_element_sibling(self):
        """Element: The first following sibling element or None."""
        nodes = self.itersiblings()
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def next_sibling(self):
        """Node: The first following sibling node or None."""
        return self.getnext()

    @property
    def node_name(self):
        """str: A string appropriate for the type of node."""
        return self.target

    @property
    def node_type(self):
        """int: The type of node."""
        return Node.PROCESSING_INSTRUCTION_NODE

    @property
    def node_value(self):
        """str: The value of node."""
        return self.data

    @node_value.setter
    def node_value(self, value):
        self.data = value

    @property
    def parent_node(self):
        """Node: A parent node."""
        return self.getparent()

    @property
    def previous_element_sibling(self):
        """Element: The first preceding sibling element or None."""
        nodes = self.itersiblings(preceding=True)
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def previous_sibling(self):
        """Node: The first preceding sibling node or None."""
        return self.getprevious()

    @property
    def text_content(self):
        """str: The text content of node."""
        return self.data

    @text_content.setter
    def text_content(self, text):
        self.data = text

    def addnext(self, node):
        """Reimplemented from lxml.etree.PIBase.addnext().

        Adds the node as a following sibling directly after this node.
        """
        if node.node_type not in (Node.ELEMENT_NODE,
                                  Node.PROCESSING_INSTRUCTION_NODE,
                                  Node.COMMENT_NODE):
            raise HierarchyRequestError(
                "This node type '{}' cannot insert as a sibling node of type "
                "'{}'".format(node.__class__.__name__,
                              self.__class__.__name__))
        node.attach_document(self.owner_document)
        super().addnext(node)

    def addprevious(self, node):
        """Reimplemented from lxml.etree.PIBase.addprevious().

        Adds the node as a preceding sibling directly before this node.
        """
        if node.node_type not in (Node.ELEMENT_NODE,
                                  Node.PROCESSING_INSTRUCTION_NODE,
                                  Node.COMMENT_NODE):
            raise HierarchyRequestError(
                "This node type '{}' cannot insert as a sibling node of type "
                "'{}'".format(node.__class__.__name__,
                              self.__class__.__name__))
        node.attach_document(self.owner_document)
        super().addprevious(node)

    def append(self, node):
        """Reimplemented from lxml.etree.PIBase.append().

        Adds a sub-node to the end of this node.
        """
        self.ensure_pre_insertion_validity(node)

    def append_child(self, node):
        """Adds a node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        self.ensure_pre_insertion_validity(node)

    def extend(self, nodes):
        """Reimplemented from lxml.etree.PIBase.extend().

        Extends the current children by the nodes in the iterable.
        """
        for node in nodes:
            self.ensure_pre_insertion_validity(node)

    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        root = self.getroottree().getroot()
        if root is None:
            root = self
        return root

    def insert(self, index, node):
        """Reimplemented from lxml.etree.PIBase.insert().

        Inserts a sub-node at the given position in this node.
        """
        _ = index
        self.ensure_pre_insertion_validity(node)

    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        self.ensure_pre_insertion_validity(node, child)

    def remove(self, node):
        """Reimplemented from lxml.etree.PIBase.remove().

        Removes a matching sub-node. Unlike the find methods, this method
        compares nodes based on identity, not on tag value or contents.
        """
        self.ensure_pre_remove_validity(node)

    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        self.ensure_pre_remove_validity(child)

    def replace(self, old_node, new_node):
        """Reimplemented from lxml.etree.PIBase.replace().

        Replaces a sub-node with the node passed as second argument.
        """
        self.ensure_pre_insertion_validity(new_node, old_node)
        self.ensure_pre_remove_validity(old_node)

    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node): A reference child node.
        Returns:
            Node: A node to be removed.
        """
        self.ensure_pre_insertion_validity(node, child)
        self.ensure_pre_remove_validity(child)

    def tostring(self, **kwargs):
        """Serializes a processing instruction to an encoded string
        representation of its XML tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        Returns:
            bytes: An XML document.
        """
        return etree.tostring(self, **kwargs)
