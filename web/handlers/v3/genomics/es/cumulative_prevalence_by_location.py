from typing import Dict, List

from web.handlers.genomics.util import (
    parse_location_id_to_query,
)


def create_mutation_query(location_id=None, lineages=None, mutations=None):
    # For multiple lineages and mutations: (Lineage 1 AND mutation 1 AND mutation 2..) OR (Lineage 2 AND mutation 1 AND mutation 2..) ...
    query_obj = {"bool": {"should": []}}
    bool_should = []
    for i in lineages:
        bool_must = {"bool": {"must": []}}
        bool_must["bool"]["must"].append({"term": {"pangolin_lineage": i}})
        bool_should.append(bool_must)
    bool_mutations = []
    for i in mutations:
        bool_mutations.append({"term": {"mutations": i}})
    if len(bool_mutations) > 0:  # If mutations specified
        if len(bool_should) > 0:  # If lineage and mutations specified
            for i in bool_should:
                i["bool"]["must"].extend(bool_mutations)
            query_obj["bool"]["should"] = bool_should
        else:  # If only mutations are specified
            query_obj = {"bool": {"must": bool_mutations}}
    else:  # If only lineage specified
        query_obj["bool"]["should"] = bool_should
    parse_location_id_to_query(location_id, query_obj)
    return query_obj


def create_query(
    params: Dict = None, query_lineage: str = "", query_mutation: List = None, size: int = None
) -> Dict:
    query = {
        "size": 0,
        "aggs": {
            "sub_date_buckets": {
                "composite": {
                    "size": 10000,
                    "sources": [{"date_collected": {"terms": {"field": "date_collected"}}}],
                },
                "aggregations": {"lineage_count": {"filter": {}}},
            }
        },
    }
    if params["query_location"] is not None:  # Global
        query["query"] = parse_location_id_to_query(params["query_location"])
    admin_level = 0
    if params["query_location"] is None:
        query["aggs"]["sub_date_buckets"]["composite"]["sources"].extend(
            [
                {"sub": {"terms": {"field": "country"}}},
                {"sub_id": {"terms": {"field": "country_id"}}},
            ]
        )
        admin_level = 0
    elif len(params["query_location"].split("_")) == 2:
        query["aggs"]["sub_date_buckets"]["composite"]["sources"].extend(
            [
                {"sub_id": {"terms": {"field": "location_id"}}},
                {"sub": {"terms": {"field": "location"}}},
            ]
        )
        admin_level = 2
    elif len(params["query_location"].split("_")) == 1:
        query["aggs"]["sub_date_buckets"]["composite"]["sources"].extend(
            [
                {"sub_id": {"terms": {"field": "division_id"}}},
                {"sub": {"terms": {"field": "division"}}},
            ]
        )
        admin_level = 1
    query_lineages = query_lineage.split(" OR ") if query_lineage is not None else []
    query_obj = create_mutation_query(
        location_id=params["query_location"], lineages=query_lineages, mutations=query_mutation
    )
    query["aggs"]["sub_date_buckets"]["aggregations"]["lineage_count"]["filter"] = query_obj

    return admin_level, query
