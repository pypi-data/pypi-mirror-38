import functools

try:
    from collections.abc import Mapping, Sequence
except ImportError:
    # Python 2
    from collections import Mapping, Sequence

import jref.error


__metaclass__ = type

TOKEN_SEPARATOR = '/'
ESCAPE_CHARACTER = '~'
ESCAPE_SEQUENCES = {
    '~0': '~',
    '~1': '/',
}


class PointerError(jref.error.Error):
    pass


class DashArrayIndexNotSupported(PointerError):
    MESSAGE = (
        'Referencing the nonexistent past-the-end element in array with \'-\' '
        'is not supported in this implementation of JSON Pointer: {0}')


class IndexOutOfRange(PointerError):
    MESSAGE = 'Array index \'{1}\' is out of range in JSON pointer: {0}'


class InvalidArrayIndex(PointerError):
    MESSAGE = 'Invalid array index, \'{1}\', in JSON pointer: {0}'


class MemberNotDefined(PointerError):
    MESSAGE = 'Member \'{1}\' not defined in object, in JSON pointer: {0}'


class UnescapedTilde(PointerError):
    MESSAGE = 'Unescaped tilde in JSON pointer: {0}'


class UnrecognizedEscapeSequence(PointerError):
    MESSAGE = 'Unrecognized escape sequence, \'~{1}\' in JSON pointer: {0}'


class UnreferenceableValue(PointerError):
    MESSAGE = (
        'Unable to dereference \'{1}\' from value of type \'{2}\', while '
        'processing JSON pointer: {0}')


def _inject_self(self, f):
    '''
    A function decorator that injects the 'self' argument in calls.
    
    The purpose of this decorator is to enable creation of class methods that
    can work seamlessly as static methods and instance methods. To that end,
    methods that are to be available as both static and instance methods should
    decorated and overridden at instance creation.
    '''
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(self, *args, **kwargs)
    return wrapper


class Pointer(str):
    '''
    Pointer implements the JSON Pointer specification, RFC 6901, it can be used
    to identify and retrieve values from a JSON-like document.

    _See also_, JSON Pointer, RFC 6901, https://tools.ietf.org/html/rfc6901
    '''
    def __new__(cls, *args, **kwargs):
        self = str.__new__(cls, *args, **kwargs)
        self.resolve_in = _inject_self(self, Pointer.resolve_in)
        self.tokenize = _inject_self(self, Pointer.tokenize)

        return self

    @staticmethod
    def _eval_lazy_value(value):
        try:
            if not callable(value.__lazy_eval__):
                return value
        except AttributeError:
            return value

        return Pointer._eval_lazy_value(value.__lazy_eval__())

    @staticmethod
    def resolve_in(self, document):
        value = document

        for token in Pointer.tokenize(self):
            value = Pointer._eval_lazy_value(value)

            if isinstance(value, Mapping):
                try:
                    value = value[token]
                except KeyError:
                    raise MemberNotDefined(self, token)
            elif isinstance(value, Sequence):
                try:
                    index = Pointer._token_to_array_index(self, token)
                    value = value[index]
                except IndexError:
                    raise IndexOutOfRange(self, index)
            else:
                raise UnreferenceableValue(self, token, type(value))

        return value

    @staticmethod
    def _split_escapes(self, token_start, token_end):
        start = 0

        while True:
            i = self.find(ESCAPE_CHARACTER, token_start, token_end)
            if i == -1:
                yield self[token_start:token_end]
                return

            try:
                self[i+1]
            except IndexError:
                raise UnescapedTilde(self)

            yield self[token_start:i]

            escape = self[i:i+2]
            try:
                yield ESCAPE_SEQUENCES[escape]
            except KeyError:
                raise UnrecognizedEscapeSequence(self, escape)

            token_start = i + 2

    @staticmethod
    def _token(self, token_start, token_end):
        return ''.join(Pointer._split_escapes(self, token_start, token_end))

    @staticmethod
    def _token_to_array_index(self, token):
        if token.isdigit():
            if (len(token) == 1
                    or not token.startswith('0')):
                return int(token)

        # The JSON Pointer specification defines '-' to represent the
        # (nonexistent) element after the last element in the array.
        if token == '-':
            raise DashArrayIndexNotSupported(self)

        raise InvalidArrayIndex(self, token)

    @staticmethod
    def tokenize(self):
        if not self:
            return

        start = 0

        # Root / is optional, but implied
        if self[0] == TOKEN_SEPARATOR:
            start = 1

        while True:
            i = self.find(TOKEN_SEPARATOR, start)
            if i == -1:
                yield Pointer._token(self, start, len(self))
                return

            yield Pointer._token(self, start, i)
            start = i + 1
