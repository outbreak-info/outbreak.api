from typing import Dict


def params_adapter(args):
    params = {}
    mutations = args.mutations
    params["mutations"] = mutations
    return params


def create_query_filter(params: Dict = None) -> Dict:
    mutations = params["mutations"].replace(":", "\\:")
    query_filters = "mutation: ({})".format(mutations)
    return query_filters


def create_query(params: Dict = None) -> Dict:
    query_filters = create_query_filter(params)
    query = {
        "size": 0,
        "query": {
            "query_string": {
                "query": query_filters  # Ex: "mutation: \"ORF1a:A735A\" OR \"ORF1a:P3395H\""
            }
        },
        "aggs": {
            "by_name": {
                "terms": {"field": "mutation"},
                "aggs": {"by_nested": {"top_hits": {"size": 1}}},
            }
        },
    }
    return query


def parse_response(resp: Dict = None) -> Dict:
    path_to_results = ["aggregations", "by_name", "buckets"]
    buckets = resp
    for i in path_to_results:
        buckets = buckets[i]
    flattened_response = []
    for i in buckets:
        for j in i["by_nested"]["hits"]["hits"]:
            tmp = j["_source"]
            for k in ["change_length_nt", "codon_num", "pos"]:
                if k in tmp and tmp[k] != "None":
                    tmp[k] = int(float(tmp[k]))
            # TODO: These .pop could be removed after deleting them from datasource
            tmp.pop("is_synyonymous", None)
            tmp.pop("id", None)
            flattened_response.append(tmp)
    return flattened_response
