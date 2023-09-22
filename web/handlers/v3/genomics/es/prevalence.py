from web.handlers.v3.genomics.util import escape_special_characters

from elasticsearch_dsl import Search, Q
from typing import Dict


def create_query_filter(params: Dict = None) -> Dict:
    lineages = params["pangolin_lineage"]
    mutations = params["mutations"]
    filters = []

    if lineages is None and mutations is None:
        return "*"

    if lineages is not None and len(lineages) > 0:
        lineages = params["pangolin_lineage"]
        lineages = "pangolin_lineage: ({})".format(lineages)
        filters.append(lineages)
    if mutations is not None and len(mutations) > 0:
        mutations = params["mutations"]
        mutations = escape_special_characters(mutations)
        mutations = "mutations: ({})".format(mutations)
        filters.append(mutations)
    query_filters = " AND ".join(filters)
    return query_filters


def create_query(params: Dict = None, size: int = None):
    s = Search()

    if params is None:
        params = {}

    # Create a terms aggregation on "date_collected"
    s.aggs.bucket("prevalence", "terms", field="date_collected", size=size)

    # Create a filter aggregation for "lineage_count"
    lineage_count_filter = Q("query_string", query=create_query_filter(params))
    s.aggs["prevalence"].bucket("lineage_count", "filter", filter=lineage_count_filter)

    s = s.extra(size=0)

    return s.to_dict()
