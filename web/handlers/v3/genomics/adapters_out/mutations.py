from typing import Dict


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
