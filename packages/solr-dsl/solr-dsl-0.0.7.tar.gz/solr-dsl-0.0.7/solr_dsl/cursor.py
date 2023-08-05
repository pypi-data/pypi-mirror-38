BATCH_SIZE = 100
SORT = "date desc, id asc"


class Cursor:

    def __init__(self, solr, query):
        self.solr = solr
        self.query = query
        self.mark = "*"
        self.batch = []
        self.position = 0

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
        return self.solr.search(self.query,
                                cursorMark=self.mark,
                                rows=BATCH_SIZE,
                                sort=SORT)
