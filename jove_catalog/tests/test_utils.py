from pyramid import testing
import unittest2


class TestUtils(unittest2.TestCase):

    def test_find_catalog(self):
        from jove_catalog.utils import find_catalog
        home = {
            'content': testing.DummyResource(),
            'jove_catalog': {None: 'thecatalog'},
        }
        root = home['content']
        root.__home__ = home
        self.assertEqual(find_catalog(root), 'thecatalog')
