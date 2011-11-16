import logging

from pyramid.traversal import find_resource
from pyramid.traversal import resource_path

from repoze.catalog.catalog import Catalog as Indexes
from repoze.catalog.document import DocumentMap

log = logging.getLogger(__name__)


class Catalog(object):

    def __init__(self, home, name, docid_attr='docid'):
        self.indexes = Indexes()
        self.home = home
        self.name = name
        self.docid_attr = docid_attr
        self.document_map = DocumentMap()

    def index_doc(self, doc):
        return self.indexes.index_doc(self._get_docid(doc), doc)

    def reindex_doc(self, doc):
        return self.indexes.reindex_doc(self._get_docid(doc), doc)

    def unindex_doc(self, doc_or_docid):
        if type(doc_or_docid) in (int, long):
            docid = doc_or_docid
        else:
            docid = getattr(doc_or_docid, self.docid_attr)
        return self.indexes.unindex_doc(docid)

    def query(self, queryobject, sort_index=None, limit=None, sort_type=None,
              reverse=False, names=None):
        count, docids = self.indexes.query(
            queryobject,
            sort_index=sort_index,
            limit=limit,
            sort_type=sort_type,
            reverse=reverse,
            names=names)
        return count, docids, self.resolver()

    def _get_docid(self, doc):
        docid_attr = self.docid_attr
        path = resource_path(doc)
        document_map = self.document_map
        docid = getattr(doc, docid_attr, None)
        if docid is None:
            docid = document_map.add(path)
            setattr(doc, docid_attr, docid)
        else:
            old_path = document_map.address_for_docid(docid)
            if old_path != path:
                document_map.remove_address(old_path)
                document_map.add(path, docid)
        return docid

    def resolver(self):
        root = self.home['content']
        document_map = self.document_map
        def resolve(docid):
            path = document_map.address_for_docid(docid)
            return find_resource(root, path)
        return resolve

    def add_index(self, name, index):
        """
        Add an index to an existing catalog.
        """
        log.info('Adding index: %s' % name)
        self.indexes[name] = index
        resolver = self.resolver()
        for docid in self.document_map.docid_to_address.keys():
            doc = resolver(docid)
            log.info('Calculating index for %s' % resource_path(doc))
            index.index_doc(docid, doc)
