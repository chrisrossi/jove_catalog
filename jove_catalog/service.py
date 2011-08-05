from persistent.mapping import PersistentMapping
from jove.interfaces import LocalService
from jove_catalog.catalog import Catalog

FOLDER_NAME = 'jove_catalog'


class CatalogService(LocalService):
    """
    Provides search for an application via `repoze.catalog`.
    """
    def __init__(self, descriptor):
        self.descriptor = descriptor

    def bootstrap(self, home, site):
        folder = home.get(FOLDER_NAME)
        if folder is None:
            home[FOLDER_NAME] = folder = PersistentMapping()
        descriptor = self.descriptor
        name = descriptor.name
        catalog = folder.get(name)
        if catalog is None:
            catalog = Catalog(home, name, descriptor.docid_attr)
            folder[name] = catalog
            indexes = catalog.indexes
            for name, index in descriptor.indexes().items():
                indexes[name] = index
