from typing import Dict

from web.handlers.v3.genomics.util import create_query_filter


def params_adapter(args: Dict = None) -> Dict:
    params = {}
    params["pangolin_lineage"] = args.pangolin_lineage or None
    params["mutations"] = args.mutations or None
    return params


def create_query(params: Dict = None, size: int = None) -> Dict:
    query = {
        "aggs": {
            "prevalence": {
                "filter": {},
                "aggs": {"country": {"terms": {"field": "country", "size": size}}},
            }
        }
    }
    # query_mutations = query_mutations.split(",") if query_mutations is not None else []
    # query_pangolin_lineage = query_pangolin_lineage.split(",") if query_pangolin_lineage is not None else []
    lineages = params["pangolin_lineage"] if params["pangolin_lineage"] else ""
    mutations = params["mutations"] if params["mutations"] else ""
    # query_obj = create_nested_mutation_query(lineages=lineages, mutations=mutations)
    query_filters = create_query_filter(
        lineages=lineages, mutations=mutations, locations=None
    )
    query_obj = {
        "bool": {
            "must": [
                {
                    "query_string": {
                        "query": query_filters  # Ex: "(pangolin_lineage:BA.2) AND (mutations: S\\:E484K OR S\\:L18F)"
                    }
                }
            ]
        }
    }
    query["aggs"]["prevalence"]["filter"] = query_obj
    return query


def parse_response(resp: Dict = None, size: int = None) -> Dict:
    path_to_results = ["aggregations", "prevalence", "country", "buckets"]
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    flattened_response = [{"key": i["key"], "doc_count": i["doc_count"]} for i in buckets]
    if size:
        try:
            size = int(size)
        except Exception:
            return {"success": False, "results": [], "errors": "Invalide size value"}
        flattened_response = sorted(flattened_response, key=lambda x: -x["total_count"])
        flattened_response = flattened_response[:size]
    return flattened_response
