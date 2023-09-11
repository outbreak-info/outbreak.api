import re
from typing import Dict

from web.handlers.v3.genomics.util import (
    create_nested_mutation_query,
    create_query_filter_key,
    parse_location_id_to_query,
    transform_prevalence,
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

        # params["location_id"] = re.search(r'location_id:(\w+)', args.q)
        # params["cumulative"] = re.search(r'cumulative:(\w+)', args.q)
        # params["min_date"] = re.search(r'min_date:(\w+)', args.q)
        # params["max_date"] = re.search(r'max_date:(\w+)', args.q)

    params["pangolin_lineage"] = (
        args.pangolin_lineage.split(",") if args.pangolin_lineage is not None else []
    )

    params["mutations"] = args.mutations or None
    params["location_id"] = args.location_id or None
    params["cumulative"] = args.cumulative
    params["min_date"] = args.min_date or None
    params["max_date"] = args.max_date or None

    return params


def create_query(idx: int = None, params: Dict = None, size: int = None) -> Dict:
    query = {
        "size": 0,
        "aggs": {
            "prevalence": {
                "filter": {"bool": {"must": []}},
                "aggs": {
                    "count": {
                        "terms": {"field": "date_collected", "size": size},
                        "aggs": {"lineage_count": {"filter": {}}},
                    }
                },
            }
        },
    }

    date_range_filter = {"query": {"range": {"date_collected": {}}}}
    if params["max_date"]:
        date_range_filter["query"]["range"]["date_collected"]["lte"] = params["max_date"]
    if params["min_date"]:
        date_range_filter["query"]["range"]["date_collected"]["gte"] = params["min_date"]
    if params["max_date"] or params["min_date"]:
        query.update(date_range_filter)

    parse_location_id_to_query(params["location_id"], query["aggs"]["prevalence"]["filter"])

    lineages = (
        params["pangolin_lineage"][idx] if params["pangolin_lineage"][idx] is not None else ""
    )
    mutations = params["mutations"] if params["mutations"] is not None else ""
    query_obj = create_nested_mutation_query(
        lineages=lineages, mutations=mutations, location_id=params["location_id"]
    )
    query["aggs"]["prevalence"]["aggs"]["count"]["aggs"]["lineage_count"]["filter"] = query_obj

    return query


def create_query_q(idx: int = None, params: Dict = None, size: int = None) -> Dict:
    query = {
        "size": 0,
        "aggs": {
            "prevalence": {
                "filter": {"bool": {"must": []}},
                "aggs": {
                    "count": {
                        "terms": {"field": "date_collected", "size": size},
                        "aggs": {"lineage_count": {"filter": {}}},
                    }
                },
            }
        },
    }

    date_range_filter = {"query": {"range": {"date_collected": {}}}}
    if params["max_date"]:
        date_range_filter["query"]["range"]["date_collected"]["lte"] = params["max_date"]
    if params["min_date"]:
        date_range_filter["query"]["range"]["date_collected"]["gte"] = params["min_date"]
    if params["max_date"] or params["min_date"]:
        query.update(date_range_filter)

    parse_location_id_to_query(params["location_id"], query["aggs"]["prevalence"]["filter"])
    query_obj = {
        "bool": {
            "must": [
                {
                    "query_string": {
                        "query": params["query_string_list"][
                            idx
                        ]  # Ex: "(pangolin_lineage:BA.2) AND (mutations: S\\:E484K OR S\\:L18F)"
                    }
                }
            ]
        }
    }

    query["aggs"]["prevalence"]["aggs"]["count"]["aggs"]["lineage_count"]["filter"] = query_obj

    return query


def parse_response(resp: Dict = None, idx: int = 0, params: Dict = None) -> Dict:
    results = {}
    path_to_results = ["aggregations", "prevalence", "count", "buckets"]
    resp = transform_prevalence(resp, path_to_results, params["cumulative"])
    lineages = (
        params["pangolin_lineage"][idx] if params["pangolin_lineage"][idx] is not None else ""
    )
    mutations = params["mutations"] if params["mutations"] is not None else ""
    # TODO: Trying to keep a similar behavior for `res_key` for now.
    res_key = create_query_filter_key(
        lineages=lineages, mutations=mutations, locations=params["location_id"]
    )
    # res_key = res_key.replace("pangolin_lineage: ", "")
    # res_key = res_key.replace("mutations: ", "")
    # res_key = res_key.replace("country_id: ", "")
    # res_key = res_key.replace("\\", "")
    # # res_key = res_key[1:-1]
    results[res_key] = resp
    return results


def parse_response_q(resp: Dict = None, idx: int = 0, params: Dict = None) -> Dict:
    results = {}
    path_to_results = ["aggregations", "prevalence", "count", "buckets"]
    resp = transform_prevalence(resp, path_to_results, params["cumulative"])
    res_key = params["q_list"][idx]
    results[res_key] = resp
    return results
