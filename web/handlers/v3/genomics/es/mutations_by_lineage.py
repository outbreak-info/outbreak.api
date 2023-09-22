from typing import Dict


from web.handlers.v3.genomics.util import (
    create_query_filter,
    parse_location_id_to_query,
)


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
