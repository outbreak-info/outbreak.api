from elasticsearch_dsl import Search
from biothings.web.query import ESQueryBuilder


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
                    ],
                    "default_operator": "AND"
                }
            }
        }
        search = Search()
        search = search.update_from_dict(query)

        return search

    def apply_extras(self, search, options):

        search = super().apply_extras(search, options)

        if options._type:
            search = search.filter('term', **{'@type': options._type})

        return search
