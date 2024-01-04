from elasticsearch_dsl import Search, Q
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

        immport          =  Q('term',  **{ "curatedBy.name": "ImmPort" })
        health_condition =  Q('term',  **{ "healthCondition.name": "covid-19" })
        dockstore        =  Q('terms', **{ 'curatedBy.name': [ 'Dockstore', 'biotools' ]})
        topic_cat        =  Q('term',  **{ 'topicCategory.name': 'COVID-19' })
        other            = ~Q('terms', **{ 'curatedBy.name': ['ImmPort', 'Dockstore', 'biotools', 'Zenodo'] })
        zenodo           =  Q('term',  **{ 'curatedBy.name': 'Zenodo'})
        keyword          =  Q('term',  **{ 'keywords': 'COVID-19'})

        search = search.query('bool', filter=[(immport & health_condition) | (dockstore & topic_cat) | (zenodo & keyword) | other])

        if options._type:
            search = search.filter('term', **{'@type': options._type})

        return search
