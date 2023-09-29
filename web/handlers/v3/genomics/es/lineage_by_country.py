from typing import Dict

from elasticsearch_dsl import Q, Search

from web.handlers.v3.genomics.util import create_query_filter


def create_query(params: Dict = None, size: int = None) -> Dict:
    # Create a Search object
    s = Search()

    # Create query filters using create_query_filter function
    lineages = params.get("pangolin_lineage", "")
    mutations = params.get("mutations", "")
    query_filters = create_query_filter(lineages=lineages, mutations=mutations, locations=None)

    # Define the main aggregation for country terms
    s.aggs.bucket(
        "prevalence", "filter", filter=Q("bool", must=[Q("query_string", query=query_filters)])
    )

    # Define the sub-aggregation for country terms
    s.aggs["prevalence"].bucket("country", "terms", field="country", size=10000)

    # Convert the Search object to a dictionary (Elasticsearch DSL)
    query = s.to_dict()

    return query
