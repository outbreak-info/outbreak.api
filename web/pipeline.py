import re

from biothings.utils.web.es_dsl import AsyncSearch
from biothings.web.pipeline import ESQueryBuilder, ESResultTransform


class QueryBuilder(ESQueryBuilder):
    '''
    Assign weights to different fields.
    '''

    def default_string_query(self, q, options):

        query = {
            "query": {
                "query_string": {
                    "query": q,
                    "fields": [
                        "name^4",
                        "interventions.name^3",
                        "description",
                        "all"
                    ]
                }
            }
        }
        search = AsyncSearch()
        search = search.update_from_dict(query)
        return search


class ResourceTransform(ESResultTransform):
    """
    TODO
    """

    def transform_hit(self, path, doc, options):

        if path == '':
            _index = doc.pop('_index')
            doc.pop('_type', None)    # not available by default on es7
            doc.pop('sort', None)     # added when using sort
            doc.pop('_node', None)    # added when using explain
            doc.pop('_shard', None)   # added when using explain
            if 'zenodo' in _index:
                # simplify id
                doc['_id'] = 'zenodo.' + doc.pop('_id').split('.')[-1]
                # fix fake list
                if 'keywords' in doc and len(doc['keywords']) == 1:
                    doc['keywords'] = re.split(r', |,|; |;', doc['keywords'][0])
            # add more source customizations here
