import mock
from pyramid import testing
import unittest2


class DummyHome(dict):

    def __init__(self):
        super(DummyHome, self).__init__()
        self['content'] = root = testing.DummyResource()
        root['foo'] = testing.DummyResource(docid=100)
        root['bar'] = testing.DummyResource(docid=101)


class DummyCatalog(object):

    def __init__(self):
        self.index_doc_called = []
        self.reindex_doc_called = []
        self.unindex_doc_called = []
        self.query_called = []
        self.indexes_added = []

    def index_doc(self, docid, doc):
        self.index_doc_called.append((docid, doc))

    def reindex_doc(self, docid, doc):
        self.reindex_doc_called.append((docid, doc))

    def unindex_doc(self, docid):
        self.unindex_doc_called.append(docid)

    def query(self, queryobject, sort_index, limit, sort_type, reverse, names):
        self.query_called.append((queryobject, sort_index, limit, sort_type,
                                  reverse, names))
        return 2, [100, 101]

    def __setitem__(self, name, index):
        self.indexes_added.append((name, index))


class TestCatalog(unittest2.TestCase):

    def setUp(self):
        self.home = DummyHome()

    def make_one(self):
        from jove_catalog.catalog import Catalog
        return Catalog(self.home, 'name', 'thedocid')

    @mock.patch('jove_catalog.catalog.Indexes', DummyCatalog)
    def test_index_doc(self):
        doc = testing.DummyResource()
        catalog = self.make_one()
        catalog.index_doc(doc)
        self.assertEqual(catalog.indexes.index_doc_called,
                         [(doc.thedocid, doc)])

    @mock.patch('jove_catalog.catalog.Indexes', DummyCatalog)
    def test_reindex_doc(self):
        doc = testing.DummyResource(thedocid=5)
        catalog = self.make_one()
        catalog.reindex_doc(doc)
        self.assertEqual(catalog.indexes.reindex_doc_called, [(5, doc)])

    @mock.patch('jove_catalog.catalog.Indexes', DummyCatalog)
    def test_unindex_doc(self):
        doc = testing.DummyResource(thedocid=5)
        catalog = self.make_one()
        catalog.unindex_doc(doc)
        self.assertEqual(catalog.indexes.unindex_doc_called, [5])

    @mock.patch('jove_catalog.catalog.Indexes', DummyCatalog)
    def test_unindex_docid(self):
        catalog = self.make_one()
        catalog.unindex_doc(6)
        self.assertEqual(catalog.indexes.unindex_doc_called, [6])

    @mock.patch('jove_catalog.catalog.Indexes', DummyCatalog)
    def test_query(self):
        catalog = self.make_one()
        catalog.document_map.add('/foo', 100)
        catalog.document_map.add('/bar', 101)
        count, docids, resolver = catalog.query(
            'queryobject', 'sort_index', 'limit', 'sort_type', 'reverse',
            'names')
        self.assertEqual(count, 2)
        self.assertEqual(docids, [100, 101])
        root = self.home['content']
        self.assertEqual(map(resolver, docids), [root['foo'], root['bar']])
        self.assertEqual(catalog.indexes.query_called, [('queryobject',
            'sort_index', 'limit', 'sort_type', 'reverse', 'names')])

    @mock.patch('jove_catalog.catalog.Indexes', DummyCatalog)
    def test_add_index(self):
        catalog = self.make_one()
        catalog.document_map.add('/foo', 100)
        catalog.document_map.add('/bar', 101)
        index = mock.Mock()
        catalog.add_index('color', index)
        self.assertEqual(catalog.indexes.indexes_added, [('color', index)])
        root = self.home['content']
        self.assertEqual(index.method_calls, [
            ('index_doc', (100, root['foo']), {}),
            ('index_doc', (101, root['bar']), {})])

