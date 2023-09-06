from typing import Dict

import pandas as pd

from web.handlers.v3.genomics.util import (
    calculate_proportion,
    create_nested_mutation_query,
    parse_location_id_to_query,
)


def params_adapter(args):
    params = {}
    params["pangolin_lineage"] = args.pangolin_lineage or None
    params["mutations"] = args.mutations or None
    params["mutations_list"] = args.mutations.split(",") if args.mutations is not None else []
    params["location_id"] = args.location_id or None
    params["frequency"] = args.frequency
    return params


def create_query(mutation: str = None, params: Dict = None, size: int = None) -> Dict:
    query = {
        "size": 0,
        "aggs": {
            "lineage": {
                "terms": {"field": "pangolin_lineage", "size": size},
                "aggs": {"mutations": {"filter": {}}},
            }
        },
    }
    if params["location_id"] is not None:
        query["query"] = parse_location_id_to_query(params["location_id"])
    if params["pangolin_lineage"] is not None:
        if "query" in query:  # Only query added will be bool for location
            query["query"]["bool"]["must"].append(
                {"term": {"pangolin_lineage": params["pangolin_lineage"]}}
            )
        else:
            query["query"] = {"term": {"pangolin_lineage": params["pangolin_lineage"]}}
    query["aggs"]["lineage"]["aggs"]["mutations"]["filter"] = create_nested_mutation_query(
        mutations=mutation
    )
    return query


def parse_response(resp: Dict = None, mutation: str = None, params: Dict = None) -> Dict:
    results = {}
    path_to_results = ["aggregations", "lineage", "buckets"]
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    flattened_response = []
    for i in buckets:
        if not i["mutations"]["doc_count"] > 0 or i["key"] == "none":
            continue
        flattened_response.append(
            {
                "pangolin_lineage": i["key"],
                "lineage_count": i["doc_count"],
                "mutation_count": i["mutations"]["doc_count"],
            }
        )
    df_response = pd.DataFrame(flattened_response)
    if df_response.shape[0] > 0:
        prop = calculate_proportion(df_response["mutation_count"], df_response["lineage_count"])
        df_response.loc[:, "proportion"] = prop[0]
        df_response.loc[:, "proportion_ci_lower"] = prop[1]
        df_response.loc[:, "proportion_ci_upper"] = prop[2]
    if "proportion" in df_response:
        df_response = df_response[df_response["proportion"] >= params["frequency"]]
    results[mutation] = df_response.to_dict(orient="records")
    return results
