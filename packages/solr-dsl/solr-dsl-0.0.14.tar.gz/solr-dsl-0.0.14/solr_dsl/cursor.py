import six

BATCH_SIZE = 100
SORT = "date desc, id asc"


class Cursor(six.Iterator):

    def __init__(self, solr, query, **kwargs):
        self.solr = solr
        self.query = query
        self.mark = "*"
        self.batch = []
        self.kwargs = kwargs

    def __iter__(self):
        return self

    def __next__(self):
        if self.batch:
            return self.batch.pop(0)
        else:
            self.pull()
            return self.__next__()

    def pull(self):
        results = self.select()
        if results.nextCursorMark == self.mark:
            raise StopIteration
        self.mark = results.nextCursorMark
        self.batch = results.docs

    def select(self):
        kwargs = dict(cursorMark=self.mark,
                      rows=BATCH_SIZE,
                      sort=SORT,
                      **self.kwargs)
        return self.solr.search(str(self.query), **kwargs)
