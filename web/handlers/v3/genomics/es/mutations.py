from typing import Dict

from elasticsearch_dsl import Q, Search

from web.handlers.v3.genomics.util import escape_special_characters


def create_query_filter(params: Dict = None) -> Dict:
    mutations = escape_special_characters(params["mutations"])
    query_filters = "mutations: ({})".format(mutations)
    return query_filters


def create_query(params: Dict = None) -> Dict:
    # Create a Search object
    s = Search()

    # Create query filters using create_query_filter function
    query_filters = create_query_filter(params)

    # Define the query using query_string
    q = Q("query_string", query=query_filters)

    # Apply the query to the Search object
    s = s.query(q)

    # Define the aggregation for mutations terms
    s.aggs.bucket("mutations", "terms", field="mutations", size=10000)

    # Set the size to 0
    s = s.extra(size=0)

    # Convert the Search object to a dictionary (Elasticsearch DSL)
    query = s.to_dict()

    return query
