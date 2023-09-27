from typing import Dict


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
            tmp.pop("count", None)
            tmp.pop("id", None)
            flattened_response.append(tmp)
    return flattened_response
