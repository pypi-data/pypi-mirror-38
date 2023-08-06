import unittest

import jref.reference as error

from jref.reference import Reference
from jref.pointer import Pointer


__metaclass__ = type


class TestContext:
    def __init__(self, base_uri, doc=None):
        self.base_uri = base_uri
        self._test_document = doc

    def load_document(self):
        return self._test_document


class TestReference(unittest.TestCase):
    def test_its_string_representation_is_context_uri_and_pointer_as_fragment(self):
        uri = self.id()
        pointer = '/non/empty/pointer'

        ctx = TestContext(uri)
        ref = Reference(ctx, pointer)

        self.assertEqual(str(ref), '{}#{}'.format(uri, pointer))

    def test_absent_a_pointer_its_string_representation_is_the_context_uri(self):
        ctx = TestContext(self.id())
        ref = Reference(ctx, '')

        self.assertEqual(str(ref), ctx.base_uri)

    def test_its_value_property_performs_shallow_resolution(self):
        ctx = TestContext(self.id())

        sentinel = object()
        value_ref = Reference(ctx, '/value')
        indirect_value_ref = Reference(ctx, '/value-reference')

        ctx._test_document = {
            'value': sentinel,
            'value-reference': value_ref,
        }

        self.assertIs(value_ref.value, sentinel)
        self.assertIs(indirect_value_ref.value, value_ref)

    def test_its_expand_method_performs_deep_resolution(self):
        ctx = TestContext(self.id())

        sentinel = object()
        value_ref = Reference(ctx, '/value')
        indirect_value_ref = Reference(ctx, '/value-reference')

        ctx._test_document = {
            'value': sentinel,
            'value-reference': value_ref,
        }

        self.assertIs(value_ref.expand(), sentinel)
        self.assertIs(indirect_value_ref.expand(), sentinel)

    def test_expand_method_expands_references_in_a_map(self):
        ctx = TestContext(self.id())
        ctx._test_document = {
            'key1': Reference(ctx, '/values/0'),
            'key2': Reference(ctx, '/values/2'),
            'key3': Reference(ctx, '/values/4'),
            'values': [ 1, 2, 3, 4, 5 ],
        }

        doc_ref = Reference(ctx, '')
        value = doc_ref.expand()

        self.assertIsInstance(value, dict)
        self.assertEqual(value['key1'], 1)
        self.assertEqual(value['key2'], 3)
        self.assertEqual(value['key3'], 5)

    def test_expand_method_expands_references_in_a_sequence(self):
        ctx = TestContext(self.id())
        ctx._test_document = [
            1, 2, 3, 4, 5,
            Reference(ctx, '/0'),
            Reference(ctx, '/2'),
            Reference(ctx, '/4'),
        ]

        doc_ref = Reference(ctx, '')
        value = doc_ref.expand()

        self.assertIsInstance(value, list)
        self.assertEqual(value, [1, 2, 3, 4, 5, 1, 3, 5])

    def test_expand_method_expands_references_in_sets(self):
        ctx = TestContext(self.id())
        ctx._test_document = {
            'values': [ 1, 2, 3, 4, 5 ],
            'set': {
                Reference(ctx, '/values/0'),
                Reference(ctx, '/values/2'),
                Reference(ctx, '/values/4'),
            },
        }

        doc_ref = Reference(ctx, '/set')
        value = doc_ref.expand()

        self.assertIsInstance(value, set)
        self.assertEqual(value, {1, 3, 5})

    def test_its_expand_method_raises_an_error_on_self_references(self):
        ctx = TestContext(self.id())
        ctx._test_document = {
            'self-reference': Reference(ctx, '/self-reference'),
        }

        with self.assertRaises(error.CircularReference):
            Reference(ctx, '/self-reference').expand()

    def test_its_expand_method_raises_an_error_on_reference_cycles(self):
        ctx = TestContext(self.id())
        ctx._test_document = {
            'reference-cycle': Reference(ctx, '/reference-cycle-loop'),
            'reference-cycle-loop': Reference(ctx, '/reference-cycle'),
        }

        with self.assertRaises(error.CircularReference):
            Reference(ctx, '/reference-cycle').expand()

    def test_its_expand_method_limits_recursion_depth(self):
        class InfiniteReferenceRecursion(dict):
            def __getitem__(self, key):
                reference, _, index = key.rpartition('-')
                if index.isdigit():
                    index = int(index) + 1
                else:
                    reference = key
                    index = '1'

                return Reference(ctx, '/{}-{}'.format(reference, index))

        ctx = TestContext(self.id())
        ctx._test_document = InfiniteReferenceRecursion()

        with self.assertRaises(error.MaximumRecursionDepth):
            Reference(ctx, '/infinite-recursion').expand()

    def test_it_can_be_used_as_a_document_to_resolve_a_pointer_in(self):
        ctx = TestContext(self.id(), {'a': 1, 'b': 2, 'c': 3})
        ref = Reference(ctx, '')

        self.assertEqual(Pointer.resolve_in('/a', ref), 1)
        self.assertEqual(Pointer.resolve_in('/b', ref), 2)
        self.assertEqual(Pointer.resolve_in('/c', ref), 3)


if __name__ == '__main__':
    unittest.main()
