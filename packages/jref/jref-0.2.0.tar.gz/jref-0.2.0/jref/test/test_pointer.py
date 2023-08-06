import unittest

import jref.pointer as error

from jref.pointer import Pointer


class TestPointer(unittest.TestCase):
    def setUp(self):
        self.sentinel = object()

    def check_pointer_is_sentinel(self, pointer, document):
        self.check_pointer_equal(document, pointer, self.sentinel)

    def check_pointer_equal(self, document, pointer, value):
        self.assertEqual(Pointer.resolve_in(pointer, document), value)

        # test that starting slash in non-empty pointer is optional
        if (len(pointer) > 1
                and pointer[0] == '/'):
            self.assertEqual(Pointer.resolve_in(pointer[1:], document), value)

    def test_pointer_resolve_in_can_be_called_as_an_instance_method(self):
        self.assertEqual(
            Pointer('key').resolve_in({'key': self.sentinel}), self.sentinel)
        self.assertEqual(
            Pointer('key').resolve_in(document={'key': self.sentinel}),
            self.sentinel)

    def test_pointer_resolve_in_can_be_called_as_a_static_method(self):
        self.assertEqual(
            Pointer.resolve_in('key', {'key': self.sentinel}), self.sentinel)
        self.assertEqual(
            Pointer.resolve_in('key', document={'key': self.sentinel}),
            self.sentinel)

    def test_an_empty_pointer_resolves_to_the_document(self):
        self.check_pointer_is_sentinel('', document=self.sentinel)

    def test_empty_root_resolves_to_empty_key(self):
        self.check_pointer_is_sentinel('/', document={'': self.sentinel})

    def test_it_can_access_a_map_item_by_key(self):
        doc = { 'key': self.sentinel }
        self.check_pointer_is_sentinel('/key', doc)

    def test_it_can_access_nested_map_items_by_key(self):
        doc = { 'nested': { 'key': self.sentinel } }
        self.check_pointer_is_sentinel('/nested/key', doc)

    def test_it_can_access_array_element_by_index(self):
        doc = [ 1, 2, self.sentinel, 4, 5 ]
        self.check_pointer_is_sentinel('/2', doc)

    def test_it_handles_complex_nesting(self):
        doc1 = {
            'a': [
                1, 2, {
                    'c': [ 3, 4 ],
                    'd': 5,
                },
            ],
            'b': {
                'f': [ 6, 7, 8 ],
            },
        }
        self.check_pointer_equal(doc1, '/a/0',      1)
        self.check_pointer_equal(doc1, '/a/1',      2)
        self.check_pointer_equal(doc1, '/a/2/c/0',  3)
        self.check_pointer_equal(doc1, '/a/2/c/1',  4)
        self.check_pointer_equal(doc1, '/a/2/d',    5)
        self.check_pointer_equal(doc1, '/b/f/0',    6)
        self.check_pointer_equal(doc1, '/b/f/1',    7)
        self.check_pointer_equal(doc1, '/b/f/2',    8)

        doc2 = [
            1, 2, {
                'a': 3,
                'b': {
                    'c': 4,
                    'd': [ 5 ],
                },
            },
        ]
        self.check_pointer_equal(doc2, '/0',        1)
        self.check_pointer_equal(doc2, '/1',        2)
        self.check_pointer_equal(doc2, '/2/a',      3)
        self.check_pointer_equal(doc2, '/2/b/c',    4)
        self.check_pointer_equal(doc2, '/2/b/d/0',  5)

    def test_it_supports_numerical_keys(self):
        self.check_pointer_is_sentinel('/0', document={'0': self.sentinel})
        self.check_pointer_is_sentinel('/1', document={'1': self.sentinel})
        self.check_pointer_is_sentinel('/999', document={'999': self.sentinel})

    def test_it_supports_dash_as_a_map_key(self):
        self.check_pointer_is_sentinel('/-', document={'-': self.sentinel})

    def test_it_raises_an_error_for_dash_as_an_array_index(self):
        with self.assertRaises(error.DashArrayIndexNotSupported):
            Pointer.resolve_in('/-', document=[])

        with self.assertRaises(error.DashArrayIndexNotSupported):
            Pointer.resolve_in('-', document=[])

    def test_it_raises_an_error_for_array_index_out_of_range(self):
        with self.assertRaises(error.IndexOutOfRange):
            Pointer.resolve_in('/5', document=[])

        with self.assertRaises(error.IndexOutOfRange):
            Pointer.resolve_in('5', document=[])

    def test_it_raises_an_error_for_non_numeric_array_index(self):
        with self.assertRaises(error.InvalidArrayIndex):
            Pointer.resolve_in('/key', document=[])

        with self.assertRaises(error.InvalidArrayIndex):
            Pointer.resolve_in('key', document=[])

    def test_it_raises_an_error_if_key_not_in_document(self):
        with self.assertRaises(error.MemberNotDefined):
            Pointer.resolve_in('/key', document={})

        with self.assertRaises(error.MemberNotDefined):
            Pointer.resolve_in('key', document={})

    def test_it_recognizes_tilde_escapes(self):
        doc = {
            'a~b': 1,
            'ab~': 2,
            '~ab': 3,
            'a/b': 4,
            'ab/': 5,
            '/ab': 6,
            '~/~': 7,
            '/~/': 8,
            '~0':  9,
            '~1': 10,
        }
        self.check_pointer_equal(doc, '/a~0b',      1)
        self.check_pointer_equal(doc, '/ab~0',      2)
        self.check_pointer_equal(doc, '/~0ab',      3)
        self.check_pointer_equal(doc, '/a~1b',      4)
        self.check_pointer_equal(doc, '/ab~1',      5)
        self.check_pointer_equal(doc, '/~1ab',      6)
        self.check_pointer_equal(doc, '/~0~1~0',    7)
        self.check_pointer_equal(doc, '/~1~0~1',    8)
        self.check_pointer_equal(doc, '/~00',       9)
        self.check_pointer_equal(doc, '/~01',       10)

    def test_it_raises_an_error_on_unrecognized_escape_sequences(self):
        with self.assertRaises(error.UnrecognizedEscapeSequence):
            Pointer.resolve_in('/~2', document={})

        with self.assertRaises(error.UnrecognizedEscapeSequence):
            Pointer.resolve_in('~2', document={})

    def test_it_raises_an_error_on_unescaped_tilde(self):
        with self.assertRaises(error.UnescapedTilde):
            Pointer.resolve_in('/~', document={})

        with self.assertRaises(error.UnescapedTilde):
            Pointer.resolve_in('~', document={})

    def test_it_raises_an_error_if_unable_to_resolve_token(self):
        with self.assertRaises(error.UnreferenceableValue):
            Pointer.resolve_in('/key', document=object())

        with self.assertRaises(error.UnreferenceableValue):
            Pointer.resolve_in('key', document=object())

    def test_it_offers_support_for_lazy_loaded_values(self):
        class LazyValue:
            def __lazy_eval__(self):
                return {'a': 1, 'b': 2, 'c': 3}

        value = LazyValue()
        self.assertEqual(Pointer.resolve_in('/a', value), 1)
        self.assertEqual(Pointer.resolve_in('/b', value), 2)
        self.assertEqual(Pointer.resolve_in('/c', value), 3)

    def test_it_offers_support_for_recursive_lazy_loaded_values(self):
        class LazyValue:
            def __lazy_eval__(self):
                return {'a': 1, 'b': 2, 'c': 3}

        class EvenLazierValue:
            def __lazy_eval__(self):
                return LazyValue()

        value = EvenLazierValue()
        self.assertEqual(Pointer.resolve_in('/a', value), 1)
        self.assertEqual(Pointer.resolve_in('/b', value), 2)
        self.assertEqual(Pointer.resolve_in('/c', value), 3)
