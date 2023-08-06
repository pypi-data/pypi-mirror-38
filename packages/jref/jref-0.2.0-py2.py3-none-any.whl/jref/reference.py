import functools

try:
    from collections.abc import Mapping, Sequence, Set
except ImportError:
    # Python 2
    from collections import Mapping, Sequence, Set

import jref.error
import jref.pointer
import jref.scalar
import jref.util


__metaclass__ = type

MAXIMUM_REFERENCE_RECURSION_DEPTH = 50


try:
    # Python 2
    dict.iteritems
    def _map_items(mapping):
        return mapping.iteritems()
except AttributeError:
    # Python 3
    def _map_items(mapping):
        return mapping.items()


def convert_to(ctor):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return ctor(f(*args, **kwargs))
        return wrapper
    return decorator


class ReferenceError(jref.error.Error):
    pass


class CircularReference(ReferenceError):
    MESSAGE = (
        'Circular reference detected while trying to expand {0}. Expansion of '
        '{1} references itself, possibly indirectly.')


class MaximumRecursionDepth(ReferenceError):
    MESSAGE = (
        'Maximum recursion depth exceeded while trying to expand {0}. Giving '
        'up expansion of {1}.')


class Reference(jref.util.EqualityComparableMixin):
    '''A reference identifies a specific portion of a document.'''
    def __init__(self, ctx, pointer):
        self.context = ctx
        self.pointer = pointer

    def __hash__(self):
        return hash((self.base_uri, self.pointer))

    def __str__(self):
        if not self.pointer:
            return self.base_uri
        return '{}#{}'.format(self.base_uri, self.pointer)

    def __repr__(self):
        return 'Reference({})'.format(self)

    def __lazy_eval__(self):
        return self.value

    @property
    def base_uri(self):
        return self.context.base_uri

    @property
    def document(self):
        return self.context.load_document()

    def expand(self):
        try:
            return _ReferenceExpander().expand(self)

        # Limit user-facing tracebacks
        except jref.error.Error as e:
            raise e.__class__(*e.args)

    @property
    def value(self):
        return jref.pointer.Pointer.resolve_in(self.pointer, self.document)


class _ReferenceExpander:
    def __init__(self):
        self.reference_stack = []

    @convert_to(dict)
    def _expand_mapping(self, mapping):
        for k, v in _map_items(mapping):
            yield self.expand(k), self.expand(v)

    @convert_to(list)
    def _expand_sequence(self, sequence):
        for v in sequence:
            yield self.expand(v)

    @convert_to(set)
    def _expand_set(self, set_):
        for v in set_:
            yield self.expand(v)

    def _expand_reference(self, ref):
        if ref in self.reference_stack:
            raise CircularReference(self.reference_stack[0], ref)

        if len(self.reference_stack) == MAXIMUM_REFERENCE_RECURSION_DEPTH:
            raise MaximumRecursionDepth(self.reference_stack[0], ref)

        self.reference_stack.append(ref)

        value = self.expand(ref.value)

        # Instances of this class are meant to be short-lived. In the face of
        # exceptions, reference_stack is cleared in one go when the instance is
        # reclaimed.
        last = self.reference_stack.pop()
        assert last is ref

        return value

    def expand(self, value):
        if jref.scalar.is_scalar(value):
            return value

        if isinstance(value, Mapping):
            return self._expand_mapping(value)

        if isinstance(value, Sequence):
            return self._expand_sequence(value)

        if isinstance(value, Set):
            return self._expand_set(value)

        if isinstance(value, Reference):
            return self._expand_reference(value)

        return value
