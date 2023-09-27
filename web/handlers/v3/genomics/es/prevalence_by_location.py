from typing import Dict

from web.handlers.v3.genomics.util import escape_special_characters, parse_location_id_to_query


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


def create_query_filter(lineages="", mutations="", locations=""):
    filters = []
    if lineages and len(lineages) > 0:
        lineages = "pangolin_lineage: {}".format(lineages)
        filters.append(lineages)
    if mutations and len(mutations) > 0:
        mutations = escape_special_characters(mutations)
        mutations = "mutations: {}".format(mutations)
        filters.append(mutations)
    query_filters = " AND ".join(filters)

    if not lineages and not mutations and not locations:
        query_filters = "*"
    return query_filters


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

    lineages = []
    if params["pangolin_lineage"] is not None and len(params["pangolin_lineage"]) > 0:
        lineages = (
            params["pangolin_lineage"][idx] if params["pangolin_lineage"][idx] is not None else ""
        )
        lineages = lineages.split(" OR ") if lineages is not None else []

    mutations = params["query_mutations"] if params["query_mutations"] is not None else ""

    query_obj = create_mutation_query(
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
