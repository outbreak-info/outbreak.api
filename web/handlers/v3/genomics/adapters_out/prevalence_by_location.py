from typing import Dict

from web.handlers.v3.genomics.util import (
    create_query_filter_key,
    transform_prevalence,
)


def parse_response(resp: Dict = None, idx: int = 0, params: Dict = None) -> Dict:
    results = {}
    path_to_results = ["aggregations", "prevalence", "count", "buckets"]
    resp = transform_prevalence(resp, path_to_results, params["cumulative"])
    lineages = []
    if params["pangolin_lineage"] is not None and len(params["pangolin_lineage"])>0:
        lineages = (
            params["pangolin_lineage"][idx] if params["pangolin_lineage"][idx] is not None else ""
        )
    mutations = params["mutations"] if params["mutations"] is not None else ""
    res_key = create_query_filter_key(
        lineages=lineages, mutations=mutations, locations=params["location_id"]
    )
    results[res_key] = resp
    return results


def parse_response_q(resp: Dict = None, idx: int = 0, params: Dict = None) -> Dict:
    results = {}
    path_to_results = ["aggregations", "prevalence", "count", "buckets"]
    resp = transform_prevalence(resp, path_to_results, params["cumulative"])
    res_key = params["q_list"][idx]
    results[res_key] = resp
    return results
