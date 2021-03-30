# Copyright (C) 2019 Tetsuya Miura <miute.dev@gmail.com>
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


class DOMException(Exception):
    """Represents the [WebIDL] DOMException."""

    INDEX_SIZE_ERR = 1  # deprecated
    DOMSTRING_SIZE_ERR = 2  # deprecated
    HIERARCHY_REQUEST_ERR = 3
    WRONG_DOCUMENT_ERR = 4
    INVALID_CHARACTER_ERR = 5
    NO_DATA_ALLOWED_ERR = 6  # deprecated
    NO_MODIFICATION_ALLOWED_ERR = 7
    NOT_FOUND_ERR = 8
    NOT_SUPPORTED_ERR = 9
    INUSE_ATTRIBUTE_ERR = 10
    INVALID_STATE_ERR = 11
    SYNTAX_ERR = 12
    INVALID_MODIFICATION_ERR = 13
    NAMESPACE_ERR = 14
    INVALID_ACCESS_ERR = 15  # deprecated
    VALIDATION_ERR = 16  # deprecated
    TYPE_MISMATCH_ERR = 17  # deprecated
    SECURITY_ERR = 18
    NETWORK_ERR = 19
    ABORT_ERR = 20
    URL_MISMATCH_ERR = 21
    QUOTA_EXCEEDED_ERR = 22
    TIMEOUT_ERR = 23
    INVALID_NODE_TYPE_ERR = 24
    DATA_CLONE_ERR = 25

    def __init__(self, *args, **kwargs):
        message = kwargs.pop('message', '')
        name = kwargs.pop('name', 'Error')
        if len(kwargs) > 0:
            raise TypeError('Invalid keyword argument(s): '
                            + repr(list(kwargs.keys())).strip('[]'))

        if len(message) == 0 and len(args) > 0:
            t = [x if isinstance(x, str) else str(x) for x in args]
            message = ' '.join(t)
        self._message = message
        if len(args) == 0 and len(message) > 0:
            args = (message,)
        super().__init__(*args)
        if self.__class__ is not DOMException:
            name = self.__class__.__name__
        self._name = name
        self._code = _error_names_map.get(name, 0)

    def __repr__(self):
        s = "{}(message='{}', name='{}')".format(
            self.__class__.__name__,
            self._message,
            self._name,
        )
        return s

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    @property
    def name(self):
        return self._name


class AbortError(DOMException):
    pass


class ConstraintError(DOMException):
    pass


class DataCloneError(DOMException):
    pass


class DataError(DOMException):
    pass


class EncodingError(DOMException):
    pass


class HierarchyRequestError(DOMException):
    pass


class InUseAttributeError(DOMException):
    pass


class InvalidCharacterError(DOMException):
    pass


class InvalidModificationError(DOMException):
    pass


class InvalidNodeTypeError(DOMException):
    pass


class InvalidStateError(DOMException):
    pass


class NamespaceError(DOMException):
    pass


class NetworkError(DOMException):
    pass


class NoModificationAllowedError(DOMException):
    pass


class NotAllowedError(DOMException):
    pass


class NotFoundError(DOMException):
    pass


class NotReadableError(DOMException):
    pass


class NotSupportedError(DOMException):
    pass


class OperationError(DOMException):
    pass


class QuotaExceededError(DOMException):
    pass


class ReadOnlyError(DOMException):
    pass


class SecurityError(DOMException):
    pass


class TransactionInactiveError(DOMException):
    pass


class UnknownError(DOMException):
    pass


class URLMismatchError(DOMException):
    pass


class VersionError(DOMException):
    pass


class WrongDocumentError(DOMException):
    pass


_error_names_map = {
    'HierarchyRequestError': DOMException.HIERARCHY_REQUEST_ERR,
    'WrongDocumentError': DOMException.WRONG_DOCUMENT_ERR,
    'InvalidCharacterError': DOMException.INVALID_CHARACTER_ERR,
    'NoModificationAllowedError': DOMException.NO_MODIFICATION_ALLOWED_ERR,
    'NotFoundError': DOMException.NOT_FOUND_ERR,
    'NotSupportedError': DOMException.NOT_SUPPORTED_ERR,
    'InUseAttributeError': DOMException.INUSE_ATTRIBUTE_ERR,
    'InvalidStateError': DOMException.INVALID_STATE_ERR,
    'SyntaxError': DOMException.SYNTAX_ERR,
    'InvalidModificationError': DOMException.INVALID_MODIFICATION_ERR,
    'NamespaceError': DOMException.NAMESPACE_ERR,
    'SecurityError': DOMException.SECURITY_ERR,
    'NetworkError': DOMException.NETWORK_ERR,
    'AbortError': DOMException.ABORT_ERR,
    'URLMismatchError': DOMException.URL_MISMATCH_ERR,
    'QuotaExceededError': DOMException.QUOTA_EXCEEDED_ERR,
    'TimeoutError': DOMException.TIMEOUT_ERR,
    'InvalidNodeTypeError': DOMException.INVALID_NODE_TYPE_ERR,
    'DataCloneError': DOMException.DATA_CLONE_ERR,
}
