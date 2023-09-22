from typing import Dict

import pandas as pd

from web.handlers.v3.genomics.util import (
    calculate_proportion,
)


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


def parse_response_q(resp: Dict = None, idx: int = 0, params: Dict = None) -> Dict:
    results = {}
    mutation_key = params["q_list"][idx]

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
    results[mutation_key] = df_response.to_dict(orient="records")
    return results
