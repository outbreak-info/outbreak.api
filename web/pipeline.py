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

    
    def _apply_extras(self, search, options):

        search = super()._apply_extras(search, options)

        if options._type:
            search = search.filter('term', **{'@type':options._type})

        return search


class ResourceTransform(ESResultTransform):
    """
    TODO
    """
