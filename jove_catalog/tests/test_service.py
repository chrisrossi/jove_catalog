import unittest2


class TestCatalogService(unittest2.TestCase):

    def make_one(self):
        from jove_catalog.service import CatalogService
        return CatalogService(TestCatalogDescriptor())

    def test_prebootstrap(self):
        home = {}
        service = self.make_one()
        service.prebootstrap(home, None)
        indexes = home['jove_catalog']['thename'].indexes
        self.assertEqual(indexes['foo'], 'one')
        self.assertEqual(indexes['bar'], 'two')


class TestCatalogDescriptor(object):
    name = 'thename'
    docid_attr = 'thedocid'

    def indexes(self):
        return {'foo': DummyIndex('one'), 'bar': DummyIndex('two')}


class DummyIndex(str):
    from repoze.catalog.interfaces import ICatalogIndex
    from zope.interface import implements
    implements(ICatalogIndex)
