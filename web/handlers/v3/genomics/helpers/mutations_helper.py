from typing import Dict


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    mutations = args.name
    params["mutations"] = mutations
    return params


def create_query_filter(params: Dict = None) -> Dict:
    mutations = params["mutations"].replace(":", "\\:")
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
        "aggs": {"mutations": {"terms": {"field": "mutation", "size": 10000}}},
    }
    return query


def parse_response(resp: Dict = None) -> Dict:
    path_to_results = [
        "aggregations",
        "mutations",
        "buckets",
    ]
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    flattened_response = [{"name": i["key"], "total_count": i["doc_count"]} for i in buckets]
    return flattened_response
