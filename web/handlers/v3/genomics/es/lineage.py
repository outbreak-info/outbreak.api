from typing import Dict


def create_query(params: Dict = None) -> Dict:
    query = {
        "size": 0,
        "query": {"wildcard": {"pangolin_lineage": {"value": params["query_str"]}}},
        "aggs": {"lineage": {"terms": {"field": "pangolin_lineage", "size": 10000}}},
    }
    return query
