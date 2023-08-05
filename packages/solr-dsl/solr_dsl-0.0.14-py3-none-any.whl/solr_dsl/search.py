from .cursor import Cursor


class Search():

    def __init__(self, solr, query="*:*", **kwargs):
        self.solr = solr
        self.query = query
        self.kwargs = kwargs
        print(kwargs)

    def scan(self):
        """Iterate over documents that match the search."""
        return Cursor(self.solr, self.query, **self.kwargs)
