from typing import Dict

from elasticsearch_dsl import Q, Search

from web.handlers.v3.genomics.util import escape_special_characters


def create_query_base(query_filters: str = "", size: int = 10000) -> Dict:
    # Create a Search object
    s = Search()

    # Define the query using bool and filter
    q = Q("bool", filter=Q("query_string", query=query_filters))

    # Apply the query to the Search object
    s = s.query(q)

    # Define the aggregations
    s.aggs.bucket("mutations", "terms", field="mutations", size=size)

    # Set size and track_total_hits
    s = s.extra(size=0, track_total_hits=True)

    # Convert the Search object to a dictionary (Elasticsearch DSL)
    query = s.to_dict()

    return query


def create_query_filter(lineages: str = "", mutations: str = "") -> Dict:
    filters = []
    if len(lineages) > 0:
        lineages = escape_special_characters(lineages)
        lineages = "pangolin_lineage: ({})".format(lineages)
        filters.append(lineages)
    if len(mutations) > 0:
        mutations = escape_special_characters(mutations)
        mutations = "mutations: ({})".format(mutations)
        filters.append(mutations)
    query_filters = " AND ".join(filters)
    return query_filters


def create_query(lineages: str = "", mutations: str = "") -> Dict:
    query_filters = create_query_filter(lineages=lineages, mutations=mutations)
    query = create_query_base(query_filters=query_filters, size=10000)
    return query


def create_query_q(query_filters: str = "", size: int = 10000) -> Dict:
    query = create_query_base(query_filters=query_filters, size=size)
    return query
