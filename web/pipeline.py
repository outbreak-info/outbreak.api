import re

from biothings.utils.web.es_dsl import AsyncSearch
from biothings.web.pipeline import ESQueryBuilder, ESResultTransform


class QueryBuilder(ESQueryBuilder):
    '''
    Assign weights to different fields.
    '''

    def default_string_query(self, q, options):
        search = AsyncSearch()
        
        """
        if q == '__all__':
            search = search.query()

        elif q == '__any__' and self.allow_random_query:
            search = search.query('function_score', random_score={})
            
        else:  # elasticsearch default
        """
        query = { "query": {
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

        search = search.query("query_string", query=str(query))
        
        return search

    
    def _apply_extras(self, search, options):

        search = super()._apply_extras(search, options)

        if options._type:
            search = search.filter('term', **{'@type':options._type})

        return search

class ResourceTransform(ESResultTransform):
    pass
