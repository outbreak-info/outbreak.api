from typing import Dict


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    params["query_str"] = args.name if args.name else None
    params["size"] = args.size if args.size else None
    return params


def create_query(params: Dict = None) -> Dict:
    query = {
        "size": 0,
        "query": {"wildcard": {"pangolin_lineage": {"value": params["query_str"]}}},
        "aggs": {"lineage": {"terms": {"field": "pangolin_lineage", "size": 10000}}},
    }
    return query


def parse_response(resp: Dict = None, size: int = None) -> Dict:
    path_to_results = ["aggregations", "lineage", "buckets"]
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    flattened_response = [{"name": i["key"], "total_count": i["doc_count"]} for i in buckets]
    if size:
        try:
            size = int(size)
        except Exception:
            return {"success": False, "results": [], "errors": "Invalide size value"}
        flattened_response = sorted(flattened_response, key=lambda x: -x["total_count"])
        flattened_response = flattened_response[:size]
    return flattened_response
