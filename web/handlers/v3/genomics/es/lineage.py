from typing import Dict

from elasticsearch_dsl import Q, Search


def create_query(params: Dict = None) -> Dict:
    # Create a Search object
    s = Search()

    # Define a query
    q = Q("wildcard", pangolin_lineage=params["query_str"])

    # Apply the query to the search object
    s = s.query(q)

    # Define an aggregation
    s.aggs.bucket("lineage", "terms", field="pangolin_lineage", size=10000)

    # Set the size to 0
    s = s.extra(size=0)

    # Convert the Search object to a dictionary (Elasticsearch DSL)
    query = s.to_dict()

    return query
