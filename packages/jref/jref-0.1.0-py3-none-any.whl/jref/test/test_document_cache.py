import unittest

from jref.util import DocumentCacheMixin
from jref.uri import LocalPath, RemoteURI


__metaclass__ = type


class TestBaseContext:
    def __init__(self, base_uri, doc):
        self.base_uri = base_uri
        self._test_document = doc

    def load_document(self):
        return self._test_document


class TestContext(DocumentCacheMixin, TestBaseContext):
    pass


class TestDocumentCacheMixin(unittest.TestCase):
    def test_it_calls_super_to_load_document(self):
        sentinel = object()
        tc = TestContext(self.id(), sentinel)

        self.assertIs(tc.load_document(), sentinel)

    def test_it_caches_a_loaded_document(self):
        sentinel = object()
        tc = TestContext(self.id(), sentinel)

        self.assertIs(tc.load_document(), sentinel)

        tc._test_document = object()
        self.assertIs(tc.load_document(), sentinel)

    def test_once_cached_documents_persist_across_context_instances(self):
        sentinel1 = object()
        sentinel2 = object()

        tc1 = TestContext(self.id(), sentinel1)
        tc2 = TestContext(self.id(), sentinel2)

        doc1 = tc1.load_document()
        doc2 = tc2.load_document()

        self.assertIsNot(tc1, tc2)
        self.assertIsNot(sentinel1, sentinel2)

        self.assertIs(doc1, sentinel1)
        self.assertIs(doc1, doc2)

    def test_document_cache_is_keyed_on_base_uri_of_context(self):
        sentinel = object()
        tc = TestContext(self.id(), sentinel)

        doc1 = tc.load_document()

        tc._test_document = object()
        doc2 = tc.load_document()

        tc.base_uri = self.id() + '/2'
        doc3 = tc.load_document()

        self.assertIs(doc1, sentinel)
        self.assertIs(doc2, sentinel)
        self.assertIsNot(doc3, sentinel)

    def test_context_may_add_attribute_to_cache_key(self):
        test_attr = '_test_cache_attribute'

        sentinel = object()
        tc = TestContext(self.id(), sentinel)

        tc.DOCUMENT_CACHE_ATTRIBUTE = test_attr
        setattr(tc, test_attr, 'before')

        doc1 = tc.load_document()

        tc._test_document = object()
        doc2 = tc.load_document()

        setattr(tc, test_attr, 'after')
        doc3 = tc.load_document()

        self.assertIs(doc1, sentinel)
        self.assertIs(doc2, sentinel)
        self.assertIsNot(doc3, sentinel)

    def test_document_cache_is_keyed_on_type_of_base_uri(self):
        local = LocalPath(self.id())
        remote = RemoteURI(self.id())

        self.assertEqual(local, remote)
        self.assertNotEqual(type(local), type(remote))

        sentinel = object()
        tc = TestContext(local, sentinel)

        doc1 = tc.load_document()

        tc._test_document = object()
        doc2 = tc.load_document()

        tc.base_uri = remote
        doc3 = tc.load_document()

        self.assertIs(doc1, sentinel)
        self.assertIs(doc2, sentinel)
        self.assertIsNot(doc3, sentinel)


if __name__ == '__main__':
    unittest.main()
