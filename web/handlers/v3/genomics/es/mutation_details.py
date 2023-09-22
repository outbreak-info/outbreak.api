from typing import Dict
from web.handlers.v3.genomics.util import escape_special_characters


def create_query_filter(params: Dict = None) -> Dict:
    mutations = escape_special_characters(params["mutations"])
    query_filters = "mutation: ({})".format(mutations)
    return query_filters


def create_query(params: Dict = None) -> Dict:
    query_filters = create_query_filter(params)
    query = {
        "size": 0,
        "query": {
            "query_string": {
                "query": query_filters  # Ex: "mutation: \"ORF1a:A735A\" OR \"ORF1a:P3395H\""
            }
        },
        "aggs": {
            "by_name": {
                "terms": {"field": "mutation"},
                "aggs": {"by_nested": {"top_hits": {"size": 1}}},
            }
        },
    }
    return query
