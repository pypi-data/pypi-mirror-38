from .cursor import Cursor


class Search():

    def __init__(self, solr, query="*:*"):
        self.solr = solr
        self.query = query

    def scan(self):
        """Iterate over documents that match the search."""
        return Cursor(self.solr, self.query)
