from web.handlers.genomics.base import BaseHandler
from web.handlers.genomics.util import parse_location_id_to_query


class SubmissionLagHandler(BaseHandler):
    name = "collection-submission"
    kwargs = dict(BaseHandler.kwargs)
    kwargs["GET"] = {
        "location_id": {"type": str, "default": None},
    }

    async def _get(self):
        query_location = self.args.location_id
        query = {
            "aggs": {
                "date_collected_submitted_buckets": {
                    "composite": {
                        "size": 10000,
                        "sources": [
                            {"date_collected": {"terms": {"field": "date_collected"}}},
                            {"date_submitted": {"terms": {"field": "date_submitted"}}},
                        ],
                    }
                }
            }
        }
        if query_location is not None:
            query["query"] = parse_location_id_to_query(query_location)
        resp = await self.asynchronous_fetch(query)
        path_to_results = ["aggregations", "date_collected_submitted_buckets", "buckets"]
        buckets = resp
        for i in path_to_results:
            buckets = buckets[i]
        while "after_key" in resp["aggregations"]["date_collected_submitted_buckets"]:
            query["aggs"]["date_collected_submitted_buckets"]["composite"]["after"] = resp[
                "aggregations"
            ]["date_collected_submitted_buckets"]["after_key"]
            resp = await self.asynchronous_fetch(query)
            buckets.extend(resp["aggregations"]["date_collected_submitted_buckets"]["buckets"])
        flattened_response = [
            {
                "date_collected": i["key"]["date_collected"],
                "date_submitted": i["key"]["date_submitted"],
                "total_count": i["doc_count"],
            }
            for i in buckets
        ]
        resp = {"success": True, "results": flattened_response}
        return resp
