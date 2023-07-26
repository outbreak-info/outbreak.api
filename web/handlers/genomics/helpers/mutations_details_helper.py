def create_query_filter(mutations=""):
    print("##### params")
    print(mutations)
    mutations = mutations.replace(":","\\:")
    query_filters = "mutation.keyword: ({})".format(mutations)
    return query_filters

def create_query(mutations=""):
    query_filters = create_query_filter(mutations=mutations)
    query = {
        "size": 0,
        "query": {
            "query_string": {
            "query": query_filters # Ex: "mutation.keyword: \"ORF1a:A735A\" OR \"ORF1a:P3395H\""
            }
        },
        "aggs": {
            "by_name": {
            "terms": {
                "field": "mutation.keyword"
            },
            "aggs": {
                "by_nested": {
                "top_hits": {
                    "size": 1
                }
                }
            }
            }
        }
    }
    return query

def parse_response(resp = {}):
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
            flattened_response.append(tmp)
    return flattened_response
