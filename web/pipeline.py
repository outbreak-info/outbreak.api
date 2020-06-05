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
