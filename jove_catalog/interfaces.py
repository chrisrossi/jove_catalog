import abc


class CatalogDescriptor(object):
    """
    Descriptor to be passed to catalog service by application with information
    on how to provide the catalog service for that application.

    + `name` Optional, the name of the catalog. If multiple catalogs are
      running in a single application, they will need to be disambiguated by
      name. Default is `None`.

    + `docid_attr` Document ids are assigned by the catalog and attached
      to content objects. This method returns the name of the attribute to
      use to store docids on content objects. If using multiple catalogs in
      a single application, the catalogs will need to use different
      attribute names. Default is `'docid'`.
    """
    __metaclass__ = abc.ABCMeta

    name = None
    docid_attr = 'docid'

    @abc.abstractmethod
    def indexes(self):
        """
        Returns a dict mapping name to index. See `repoze.catalog` for more
        information on indexes.
        """
