from web.handlers.genomics.base import BaseHandler


class MutationDetailsHandler(BaseHandler):
    name = "mutation-details"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {"mutations": {"type": str, "default": None}}

    async def _get(self):
        mutations = self.args.mutations
        mutations = mutations.split(",") if mutations is not None else []
        query = {
            "size": 0,
            "aggs": {
                "by_mutations": {
                    "nested": {"path": "mutations"},
                    "aggs": {
                        "inner": {
                            "filter": {
                                "bool": {
                                    "should": [
                                        {"match": {"mutations.mutation": i}} for i in mutations
                                    ]
                                }
                            },
                            "aggs": {
                                "by_name": {
                                    "terms": {"field": "mutations.mutation"},
                                    "aggs": {"by_nested": {"top_hits": {"size": 1}}},
                                }
                            },
                        }
                    },
                }
            },
        }
        resp = await self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "by_mutations", "inner", "by_name", "buckets"]
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
        resp = {"success": True, "results": flattened_response}
        return resp
