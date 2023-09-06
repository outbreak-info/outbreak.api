from typing import Dict


def params_adapter(args):
    params = {}
    params["pangolin_lineage"] = args.pangolin_lineage or None
    params["mutations"] = args.mutations or None
    params["cumulative"] = args.cumulative
    return params


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
        mutations = mutations.replace(":", "\\:")
        mutations = "mutations: ({})".format(mutations)
        filters.append(mutations)
    query_filters = " AND ".join(filters)
    return query_filters


def create_query(params: Dict = None, size: int = None):
    query_filters = create_query_filter(params)
    query = {
        "size": 0,
        "aggs": {
            "prevalence": {
                "terms": {"field": "date_collected", "size": size},
                "aggs": {
                    "lineage_count": {
                        "filter": {
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
                    }
                },
            }
        },
    }
    return query
