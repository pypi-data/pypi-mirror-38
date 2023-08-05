# solr-dsl

A high-level library for querying Solr with Python. Built on the lower-level Pysolr.

## Example

```
from pysolr import Solr
from solr_dsl import Search

solr = Solr('http://localhost:8983/solr/test')

query = (Field('doc_type', 'solution') &
         Range("date", "2018-01-01T00:00:00Z", "now"))
search = Search(solr, query)

for document in search.scan():
    ...
```
