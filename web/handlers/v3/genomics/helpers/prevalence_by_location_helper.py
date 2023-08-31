from typing import Dict
from web.handlers.v3.genomics.util import (
    create_nested_mutation_query,
    create_query_filter,
    parse_location_id_to_query,
    transform_prevalence,
)

def params_adapter(args):
    params = {}
    # params["pangolin_lineage"] = args.pangolin_lineage or None
    params["pangolin_lineage"] = (
        args.pangolin_lineage.split(",") if args.pangolin_lineage is not None else []
    )
    params["mutations"] = args.mutations or None
    params["location_id"] = args.location_id or None
    params["cumulative"] = args.cumulative
    params["min_date"] = args.min_date or None
    params["max_date"] = args.max_date or None
    return params

def create_query(idx, params, size):
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

    lineages = params["pangolin_lineage"][idx] if params["pangolin_lineage"][idx] is not None else ""
    mutations = params["mutations"] if params["mutations"] is not None else ""
    query_obj = create_nested_mutation_query(
        lineages=lineages, mutations=mutations, location_id=params["location_id"]
    )
    query["aggs"]["prevalence"]["aggs"]["count"]["aggs"]["lineage_count"][
        "filter"
    ] = query_obj

    return query

def parse_response(resp: Dict = None, idx: int = 0, params: Dict = None):
    results = {}
    path_to_results = ["aggregations", "prevalence", "count", "buckets"]
    resp = transform_prevalence(resp, path_to_results, params["cumulative"])
    lineages = params["pangolin_lineage"][idx] if params["pangolin_lineage"][idx] is not None else ""
    mutations = params["mutations"] if params["mutations"] is not None else ""
    # TODO: What should be returned as `res_key`?
    # res_key = None
    # if len(query_pangolin_lineage) > 0:
    #     res_key = " OR ".join(lineages)
    # if len(query_mutations) > 0:
    #     res_key = (
    #         "({}) AND ({})".format(res_key, " AND ".join(query_mutations))
    #         if res_key is not None
    #         else " AND ".join(query_mutations)
    #     )
    # TODO: Trying to keep a similar behavior for `res_key` for now.
    res_key = create_query_filter(lineages=lineages, mutations=mutations, locations=params["location_id"])
    res_key = res_key.replace("pangolin_lineage: ", "")
    res_key = res_key.replace("mutations: ", "")
    res_key = res_key.replace("country_id: ", "")
    res_key = res_key.replace("\\", "")
    # res_key = res_key[1:-1]
    results[res_key] = resp
    return results
