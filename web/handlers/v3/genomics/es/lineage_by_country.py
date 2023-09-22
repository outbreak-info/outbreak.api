from typing import Dict

from web.handlers.v3.genomics.util import create_query_filter


def create_query(params: Dict = None, size: int = None) -> Dict:
    query = {
        "aggs": {
            "prevalence": {
                "filter": {},
                "aggs": {"country": {"terms": {"field": "country", "size": size}}},
            }
        }
    }
    lineages = params["pangolin_lineage"] if params["pangolin_lineage"] else ""
    mutations = params["mutations"] if params["mutations"] else ""
    query_filters = create_query_filter(lineages=lineages, mutations=mutations, locations=None)
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
    query["aggs"]["prevalence"]["filter"] = query_obj
    return query
