from typing import Dict

from web.handlers.v3.genomics.util import escape_special_characters


def create_query_filter(lineages: str = "", mutations: str = "") -> Dict:
    filters = []
    if len(lineages) > 0:
        lineages = "pangolin_lineage: ({})".format(lineages)
        filters.append(lineages)
    if len(mutations) > 0:
        mutations = escape_special_characters(mutations)
        mutations = "mutations: ({})".format(mutations)
        filters.append(mutations)
    query_filters = " AND ".join(filters)
    return query_filters


def create_query(lineages: str = "", mutations: str = "") -> Dict:
    query_filters = create_query_filter(lineages=lineages, mutations=mutations)
    query = {
        "size": 0,
        "track_total_hits": True,
        "query": {
            "bool": {
                "filter": [
                    {
                        "query_string": {
                            "query": query_filters  # Ex: (pangolin_lineage : BA.2) AND (mutations : NOT(MUTATION) OR MUTATION)
                        }
                    }
                ]
            }
        },
        "aggs": {"mutations": {"terms": {"field": "mutations", "size": 10000}}},
    }
    return query


def create_query_q(query_filters: str = "", size: int = 10000) -> Dict:
    query = {
        "size": 0,
        "track_total_hits": True,
        "query": {
            "bool": {
                "filter": [
                    {
                        "query_string": {
                            "query": query_filters  # Ex: (pangolin_lineage : BA.2) AND (mutations : NOT(MUTATION) OR MUTATION)
                        }
                    }
                ]
            }
        },
        "aggs": {"mutations": {"terms": {"field": "mutations", "size": size}}},
    }
    return query
