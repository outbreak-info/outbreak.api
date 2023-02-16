from web.handlers.genomics.base import BaseHandler


class MutationHandler(BaseHandler):
    name = "mutations"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "name": {"type": str, "required": True},
    }

    async def _get(self):
        query_str = self.args.name
        query = {
            "size": 0,
            "aggs": {
                "mutations": {
                    "nested": {"path": "mutations"},
                    "aggs": {
                        "mutation_filter": {
                            "filter": {"wildcard": {"mutations.mutation": {"value": query_str}}},
                            "aggs": {
                                "count_filter": {
                                    "terms": {"field": "mutations.mutation", "size": 10000}
                                }
                            },
                        }
                    },
                }
            },
        }
        resp = await self.asynchronous_fetch(query)
        path_to_results = [
            "aggregations",
            "mutations",
            "mutation_filter",
            "count_filter",
            "buckets",
        ]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = [{"name": i["key"], "total_count": i["doc_count"]} for i in buckets]
        resp = {"success": True, "results": flattened_response}
        return resp
