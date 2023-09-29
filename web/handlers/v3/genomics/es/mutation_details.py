from typing import Dict

from elasticsearch_dsl import A, Q, Search

from web.handlers.v3.genomics.util import escape_special_characters


def create_query_filter(params: Dict = None) -> Dict:
    mutations = escape_special_characters(params["mutations"])
    query_filters = "mutation: ({})".format(mutations)
    return query_filters


def create_query(params: Dict = None) -> Dict:
    # Create a Search object
    s = Search()

    # Create a query filter using the create_query_filter function
    query_filters = create_query_filter(params)

    # Define the query using query_string
    q = Q("query_string", query=query_filters)

    # Apply the query to the Search object
    s = s.query(q)

    # Define the aggregations
    s.aggs.bucket("by_name", "terms", field="mutation").bucket("by_nested", A("top_hits", size=1))

    # Set the size to 0
    s = s.extra(size=0)

    # Convert the Search object to a dictionary (Elasticsearch DSL)
    query = s.to_dict()

    return query
