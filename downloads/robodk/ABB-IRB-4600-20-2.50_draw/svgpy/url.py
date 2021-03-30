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


import os
import re
import sys
from collections.abc import MutableMapping
from urllib.parse import quote, quote_plus, unquote, urlencode, urlsplit

_SPECIAL_SCHEMES_PORT_NUMBERS = {
    'ftp:': '21',
    'file:': '',
    'gopher:': '70',
    'http:': '80',
    'https:': '443',
    'ws:': '80',
    'wss:': '443',
}

_RE_NUMERIC_CHARACTER_REFERENCE = re.compile(
    r'(?P<prefix>&#)([0-9]{4}|x[0-9a-f]{4})(?P<suffix>;)',
    re.IGNORECASE)


def quote_numeric_character_references(query, quote_via=None, safe=''):
    def _quote(_string):
        if quote_via is None:
            return _string
        else:
            return quote_via(_string, safe=safe)

    _query = ''
    pos = 0
    for it in _RE_NUMERIC_CHARACTER_REFERENCE.finditer(query):
        start, end = it.span()
        if start != pos:
            _query += _quote(query[pos:start])
        _query += '%26%23{}%3B'.format(query[start + 2:end - 1])
        pos = end
    else:
        if pos < len(query):
            _query += _quote(query[pos:])
    return _query


class Location(object):
    """Represents the [HTML] Location."""

    def __init__(self, browsing_context=None):
        """Constructs a Location object.

        Arguments:
            browsing_context (BrowsingContext, optional): A browsing context
                object that is associated with the document.
        """
        self._browsing_context = browsing_context
        self._url = URL('about:blank')

    def __repr__(self):
        return repr(self._url)

    @property
    def hash(self):
        """str: The URL's fragment (includes leading "#" if non-empty).
        If changed, the associated document navigates to the new page.
        """
        return self._url.hash

    @hash.setter
    def hash(self, fragment):
        self._url.hash = fragment
        self._navigate()

    @property
    def host(self):
        """str: The URL's host and port (if different from the default port
        for the scheme).
        If changed, the associated document navigates to the new page.
        """
        return self._url.host

    @host.setter
    def host(self, host):
        self._url.host = host
        self._navigate()

    @property
    def hostname(self):
        """str: The URL's host.
        If changed, the associated document navigates to the new page.
        """
        return self._url.hostname

    @hostname.setter
    def hostname(self, hostname):
        self._url.hostname = hostname
        self._navigate()

    @property
    def href(self):
        """str: The entire URL.
        If changed, the associated document navigates to the new page.
        """
        return self._url.href

    @href.setter
    def href(self, url):
        self._url.href = url
        self._navigate()

    @property
    def origin(self):
        """str: The URL's origin."""
        return self._url.origin

    @property
    def pathname(self):
        """str: The URL's path.
        If changed, the associated document navigates to the new page.
        """
        return self._url.pathname

    @pathname.setter
    def pathname(self, pathname):
        self._url.pathname = pathname
        self._navigate()

    @property
    def port(self):
        """str: The URL's port.
        If changed, the associated document navigates to the new page.
        """
        return self._url.port

    @port.setter
    def port(self, port):
        self._url.port = port
        self._navigate()

    @property
    def protocol(self):
        """str: The URL's scheme.
        If changed, the associated document navigates to the new page.
        """
        return self._url.protocol

    @protocol.setter
    def protocol(self, protocol):
        self._url.protocol = protocol
        self._navigate()

    @property
    def search(self):
        """str: The URL's query (includes leading "?" if non-empty).
        If changed, the associated document navigates to the new page.
        """
        return self._url.search

    @search.setter
    def search(self, search):
        self._url.search = search
        self._navigate()

    def _navigate(self):
        if self._browsing_context is not None:
            url = self._url
            if ((len(url.protocol) == 0 and len(url.host) == 0)
                    or url.protocol in ['blob:', 'data:']
                    or (url.protocol in ['about:', 'file:']
                        and len(url.pathname) == 0)):
                raise ValueError('Invalid URL: ' + repr(url.href))
            self._browsing_context.document.navigate(url)

    def assign(self, url):
        """Navigates to the given URL.

        Arguments:
            url (str): The URL of the page to navigate to.
        """
        self.href = url

    def reload(self):
        """Reloads the current page."""
        self._navigate()

    def tostring(self, exclude_fragment=False):
        """Serializes a Location object.

        Arguments:
            exclude_fragment (bool, optional): If exclude_fragment is True,
                removes fragment from the returned URL.
        Returns:
            str: The entire URL.
        """
        return self._url.tostring(exclude_fragment=exclude_fragment)


class URL(object):
    """Represents the [URL] URL."""

    def __init__(self, url, base=None):
        """Constructs an URL object.

        Arguments:
            url (str): An entire URL or a relative-URL.
            base (str, URL, optional): A base URL for a relative-URL.
        """
        self._protocol = ''
        self._username = ''
        self._password = ''
        self._hostname = ''
        self._host = ''
        self._port = ''
        self._pathname = ''
        self._search_params = URLSearchParams()
        self._hash = ''
        if base is None:
            parsed_base = None
        elif isinstance(base, str):
            if len(base) == 0:
                parsed_base = None
            else:
                parsed_base = URL(base)
        elif isinstance(base, URL):
            parsed_base = base
        else:
            raise TypeError('Expected str or URL, got ' + repr(type(base)))
        if (parsed_base is not None
                and parsed_base.protocol in ['about:', 'blob:', 'data:']):
            parsed_base = None
        done = False
        try:
            self._parse_url(url)
            done = True
        except ValueError:
            if parsed_base is None:
                raise
        if not done:
            if os.path.isabs(url):
                parsed_base.pathname = url
                parsed_base.search = ''
                parsed_base.hash = ''
            else:
                if parsed_base.protocol != 'file:':
                    pathname = os.path.join(
                        os.path.dirname(parsed_base.pathname),
                        url)
                else:  # 'file:'
                    parent_path = parsed_base.pathname
                    if sys.platform.startswith('win'):
                        parent_path = parent_path.lstrip('/')
                    if not os.path.isdir(parent_path):
                        parent_path = os.path.dirname(parent_path)
                    pathname = os.path.join(parent_path, url)
                pathname = pathname.replace('\\', '/')
                pr = urlsplit(pathname)
                parsed_base.pathname = pr.path
                parsed_base.search = pr.query
                parsed_base.hash = pr.fragment
            url = parsed_base.href
            self._parse_url(url)

    def __repr__(self):
        return repr({'href': self.tostring(),
                     'origin': self.origin,
                     'protocol': self._protocol,
                     'username': self._username,
                     'password': self._password,
                     'host': self._host,
                     'hostname': self._hostname,
                     'port': self._port,
                     'pathname': self._pathname,
                     'search': self._search_params,
                     'hash': self._hash,
                     })

    @property
    def hash(self):
        """str: The URL's fragment (includes leading "#" if non-empty)."""
        return '#' + self._hash if len(self._hash) > 0 else ''

    @hash.setter
    def hash(self, fragment):
        fragment = fragment.lstrip('#')
        # unsafe:
        # U+0020 (SP), U+0022 ("), U+003C (<), U+003E (>), and U+0060 (`)
        self._hash = quote(unquote(fragment),
                           safe='!#$%&\'()*+,-./:;=?@[\\]^_{|}~')

    @property
    def host(self):
        """str: The URL's host and port (if different from the default port
        for the scheme).
        """
        port = self.port
        if len(port) > 0:
            if _SPECIAL_SCHEMES_PORT_NUMBERS.get(self.protocol, '') == port:
                self._host = self._hostname
        return self._host

    @host.setter
    def host(self, host):
        self._parse_host(host)

    @property
    def hostname(self):
        """str: The URL's host."""
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        self._parse_host(hostname, hostname_state=True)

    @property
    def href(self):
        """str: The entire URL."""
        return self.tostring()

    @href.setter
    def href(self, url):
        self._parse_url(url)

    @property
    def origin(self):
        """str: The URL's origin."""
        protocol = self.protocol
        host = self.host
        if protocol == 'blob:':
            try:
                url = URL(self.pathname)
                origin = url.origin
            except ValueError:
                origin = 'null'
        elif protocol == 'file:':
            origin = 'null'
        elif (len(protocol) > 0
              and protocol in _SPECIAL_SCHEMES_PORT_NUMBERS
              and len(host) > 0):
            origin = '{}//{}'.format(protocol, host)
        else:
            origin = 'null'
        return origin

    @property
    def password(self):
        """str: The URL's password."""
        return self._password

    @password.setter
    def password(self, password):
        self._password = quote(unquote(password), safe='')

    @property
    def pathname(self):
        """str: The URL's path."""
        pathname = self._pathname
        if (self._protocol not in ['about:', 'blob:', 'data:']
                and not pathname.startswith('/')):
            pathname = '/' + pathname
        elif (self._protocol in ['about:', 'blob:', 'data:']
              and pathname.startswith('/')):
            pathname = pathname[1:]
        return pathname

    @pathname.setter
    def pathname(self, pathname):
        if len(pathname) == 0:
            self._pathname = ''
            return
        elif (len(self._protocol) > 0
                and self._protocol in _SPECIAL_SCHEMES_PORT_NUMBERS
                and '\\' in pathname):
            raise ValueError('Invalid pathname: ' + repr(pathname))
        if self._protocol not in ['blob:', 'data:']:
            pathname = unquote(pathname).replace('\\', '/')
            # U+0026 (&)
            # U+002F (/), U+003A (:), U+003B (;), U+003D (=), U+0040 (@),
            # U+005B ([), U+005C (\), U+005D (]), U+005F (_), U+007E (~)
            pathname = quote(pathname, safe='&/:;=@[]_~')
            sep = len(pathname) >= 2 and pathname.endswith('/')
            pathname = os.path.normpath(pathname).replace('\\', '/')
            if sep and not pathname.endswith('/'):
                pathname += '/'
        if (self._protocol not in ['about:', 'blob:', 'data:']
                and not pathname.startswith('/')):
            pathname = '/' + pathname
        self._pathname = pathname

    @property
    def port(self):
        """str: The URL's port."""
        return self._port

    @port.setter
    def port(self, port):
        if len(port) == 0:
            self._port = ''
            self._host = self._hostname
            return
        elif not port.isdigit() or int(port) > 2 ** 16 - 1:
            raise ValueError('Invalid port: ' + repr(port))
        self._port = port
        self._host = self._hostname
        if (len(port) > 0
                and len(self._host) > 0
                and _SPECIAL_SCHEMES_PORT_NUMBERS.get(
                    self._protocol, '') != port):
            self._host += ':' + port

    @property
    def protocol(self):
        """str: The URL's scheme."""
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        if len(protocol) > 0:
            protocol = protocol.rstrip(':').lower()
            if (not protocol[0].isalpha()
                    or (len(protocol) >= 2
                        and not all(ch.isalnum() or ch in '+-.'
                                    for ch in protocol[1:]))):
                raise ValueError('Invalid protocol: ' + repr(protocol))
            if not protocol.endswith(':'):
                protocol += ':'
        self._protocol = protocol

    @property
    def search(self):
        """str: The URL's query (includes leading "?" if non-empty)."""
        if len(self._search_params) == 0:
            return ''
        queries = list()
        # unsafe:
        # U+0020 (SP), U+0023 (#), U+0026 (&), and U+0027 (')
        safe = '!$%()*+,-./:;=?@[\\]^_`{|}~'
        # FIXME: implement URLSearchParams.sort().
        for key in sorted(self._search_params):
            value = self._search_params[key]
            key = quote_numeric_character_references(key,
                                                     quote_via=quote_plus,
                                                     safe=safe)
            value = quote_numeric_character_references(value,
                                                       quote_via=quote_plus,
                                                       safe=safe)
            query = '{}={}'.format(key, value)
            queries.append(query)
        return '?' + '&'.join(queries)

    @search.setter
    def search(self, query):
        query = query.lstrip('?')
        self._search_params.clear()
        if len(query) == 0:
            return
        pairs = query.split('&')
        for pair in pairs:
            kv = pair.split('=')
            if len(kv) < 2:
                kv.append('')
            key = kv[0].replace('+', ' ')
            value = kv[1].replace('+', ' ')
            self._search_params[key] = value

    @property
    def search_params(self):
        """URLSearchParams: The query's key and value pairs of the URL."""
        return self._search_params

    @property
    def username(self):
        """str: The URL's username."""
        return self._username

    @username.setter
    def username(self, username):
        self._username = quote(unquote(username), safe='')

    def _parse_host(self, host, hostname_state=False):
        if len(host) == 0:
            self._host = self._hostname = ''
            if not hostname_state:
                self._port = ''
            return
        elif any(ch in host for ch in '\t\n\r #%/?@\\'):
            # allow U+003A (:), U+005B ([), or U+005D (]).
            raise ValueError('Invalid hostname: ' + repr(host))
        host = host.lower().encode('idna').decode()
        colons = host.count(':')
        if colons > 1:
            # IPv6 address or IPv6 address with port
            if host.startswith('['):
                # IPv6 address or IPv6 address with port
                if ']' not in host:
                    raise ValueError('Invalid hostname: ' + repr(host))
                end = host.rfind(']') + 1
                self._host = self._hostname = host[:end]
            else:
                # IPv6 address
                end = -1
                self._host = self._hostname = '[{}]'.format(host)
        elif colons == 1:
            # ascii-domain with port or IPv4 address with port
            end = host.rfind(':')
            self._host = self._hostname = host[:end]
        else:
            # ascii-domain or IPv4 address
            end = -1
            self._host = self._hostname = host
        if not hostname_state:
            # host state
            if end < 0:
                self._port = ''
            else:
                self.port = host[end + 1:]
        else:
            # hostname state
            if end < 0:
                self.port = self._port
            else:
                port = host[end + 1:]
                if len(port) > 0:
                    self.port = port

    def _parse_url(self, url):
        pr = urlsplit(url)
        if ((len(pr.scheme) == 0 and len(pr.netloc) == 0)
                or (pr.scheme in ['about', 'blob', 'data']
                    and len(pr.path) == 0)):
            raise ValueError('Invalid URL: ' + repr(url))
        self.protocol = pr.scheme
        if len(pr.netloc) == 0:
            self._host = self._hostname = self._port = ''
        else:
            self._port = str(pr.port) if pr.port is not None else ''
            self.hostname = pr.hostname
        self.username = pr.username if pr.username is not None else ''
        self.password = pr.password if pr.password is not None else ''
        self.pathname = pr.path
        self.search = pr.query
        self.hash = pr.fragment

    def tostring(self, exclude_fragment=False):
        """Serializes an URL object.

        Arguments:
            exclude_fragment (bool, optional): If exclude_fragment is True,
                removes fragment from the returned URL.
        Returns:
            str: The entire URL.
        """
        parts = list()
        protocol = self.protocol
        host = self.host
        pathname = self.pathname
        if len(protocol) > 0:
            parts.append(protocol)
            if protocol not in ['about:', 'blob:', 'data:']:
                parts.append('//')
            if len(host) > 0 and protocol != 'file:':
                if len(self.username) > 0:
                    parts.append(self.username)
                    if len(self.password) > 0:
                        parts.append(':' + self.password)
                    parts.append('@')
                parts.append(host)
        parts.append(pathname)
        if len(host) > 0 or len(pathname) > 0:
            parts.append(self.search)
            if not exclude_fragment:
                parts.append(self.hash)
        return ''.join(parts)


class URLSearchParams(MutableMapping):
    """Represents the [URL] URLSearchParams."""

    def __init__(self, *args, **kwargs):
        self._data = dict()
        self.update(dict(*args, **kwargs))

    def __delitem__(self, key):
        del self._data[key]

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)

    def __setitem__(self, key, value):
        self._data[key] = value

    def tostring(self):
        """Serializes an URLSearchParams object.

        Returns:
            str: The URL's query (excludes leading "?" if non-empty).
        """
        if self.__len__() == 0:
            return ''
        # U+0020 (SP) -> U+002B (+)
        # safe:
        # U+002A (*), U+002D (-), U+002E (.), U+005F (_)
        queries = list()
        # FIXME: implement URLSearchParams.sort().
        for key in sorted(self._data):
            value = self.get(key)
            query = urlencode({key: value}, safe='*-._')
            queries.append(query)
        return '&'.join(queries)
