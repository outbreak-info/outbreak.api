import re
from typing import Dict

import pandas as pd

from web.handlers.v3.genomics.util import (
    calculate_proportion,
    create_query_filter,
    parse_location_id_to_query,
)


def params_adapter(args: Dict = None) -> Dict:
    params = {}

    if args.q is not None:
        params["q"] = args.q or None

        queries_delimiter = "|"
        params["q_list"] = args.q.split(queries_delimiter) if args.q is not None else []

        params["query_string_list"] = []
        for q in params["q_list"]:
            q_formatted = q.replace("lineages", "pangolin_lineage")
            keywords = ["mutations", "pangolin_lineage"]
            pattern = rf'({"|".join(keywords)}):|:'
            q_formatted = re.sub(
                pattern, lambda match: match.group(0) if match.group(1) else r"\:", q_formatted
            )
            params["query_string_list"].append(q_formatted)

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

    query_filters = create_query_filter(lineages=None, mutations=mutation, locations=None)
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
    query["aggs"]["lineage"]["aggs"]["mutations"]["filter"] = query_obj

    # query["aggs"]["lineage"]["aggs"]["mutations"]["filter"] = create_nested_mutation_query(
    #     mutations=mutation
    # )
    return query


def create_query_q(query_filter: str = None, params: Dict = None, size: int = None) -> Dict:
    query = {
        "size": 0,
        "aggs": {
            "lineage": {
                "terms": {"field": "pangolin_lineage", "size": size},
                "aggs": {
                    "mutations": {
                        "filter": {"bool": {"must": [{"query_string": {"query": query_filter}}]}}
                    },
                    "filter_by_pangolin_lineage": {
                        "bucket_selector": {
                            "buckets_path": {"totalDocCount": "mutations._count"},
                            "script": "params.totalDocCount > 0",
                        }
                    },
                },
            }
        },
    }

    if params["location_id"] is not None:
        query["query"] = parse_location_id_to_query(params["location_id"])

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
