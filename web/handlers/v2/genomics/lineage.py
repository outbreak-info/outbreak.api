from web.handlers.genomics.base import BaseHandler


class LineageHandler(BaseHandler):

    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "name": {"type": str, "default": None},
        "size": {"type": int, "default": None},
    }

    async def _get(self):
        query_str = self.get_argument("name", None)
        size = self.get_argument("size", None)
        query = {
            "size": 0,
            "query": {"wildcard": {"pangolin_lineage": {"value": query_str}}},
            "aggs": {"lineage": {"terms": {"field": "pangolin_lineage", "size": 10000}}},
        }
        resp = await self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "lineage", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        flattened_response = [{"name": i["key"], "total_count": i["doc_count"]} for i in buckets]
        if size:
            try:
                size = int(size)
            except Exception:
                return {"success": False, "results": [], "errors": "Invalide size value"}
            flattened_response = sorted(flattened_response, key=lambda x: -x["total_count"])
            flattened_response = flattened_response[:size]
        resp = {"success": True, "results": flattened_response}
        return resp
