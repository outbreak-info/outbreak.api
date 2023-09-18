import asyncio

from web.handlers.v3.genomics.base import BaseHandlerV3
import web.handlers.v3.genomics.helpers.cumulative_prevalence_by_location_helper as helper

from web.handlers.genomics.util import (
    create_iterator,
)


class CumulativePrevalenceByLocationHandler(BaseHandlerV3):
    name = "lineage-by-sub-admin-most-recent"
    kwargs = dict(BaseHandlerV3.kwargs)
    kwargs["GET"] = {
        "pangolin_lineage": {"type": str, "required": True},
        "detected": {"type": bool, "default": False},
        "mutations": {"type": str, "default": None},
        "location_id": {"type": str, "default": None},
        "ndays": {"type": int, "default": None, "min": 1},
    }

    async def _get(self):
        params = helper.params_adapter(self.args)
        parsed_resp = {}

        # for query_lineage, query_mutation in create_iterator(
        #     params["query_pangolin_lineage"], params["query_mutations"]
        # ):
        #     admin_level, query = helper.create_query(params, query_lineage, query_mutation, self.size)
        #     resp = await self.asynchronous_fetch(query)

        #     buckets = resp["aggregations"]["sub_date_buckets"]["buckets"]
        #     # Get all paginated results
        #     while "after_key" in resp["aggregations"]["sub_date_buckets"]:
        #         query["aggs"]["sub_date_buckets"]["composite"]["after"] = resp["aggregations"][
        #             "sub_date_buckets"
        #         ]["after_key"]
        #         resp = await self.asynchronous_fetch(query)
        #         buckets.extend(resp["aggregations"]["sub_date_buckets"]["buckets"])
        #     parsed_resp.update(helper.parse_response(resp, params, admin_level, query_lineage, buckets, self.size))

        async def process_query(query_lineage, query_mutation):
            admin_level, query = helper.create_query(params, query_lineage, query_mutation, self.size)
            resp = await self.asynchronous_fetch_lineages(query)
            buckets = resp["aggregations"]["sub_date_buckets"]["buckets"]
            # Get all paginated results
            while "after_key" in resp["aggregations"]["sub_date_buckets"]:
                query["aggs"]["sub_date_buckets"]["composite"]["after"] = resp["aggregations"][
                    "sub_date_buckets"
                ]["after_key"]
                resp = await self.asynchronous_fetch_lineages(query)
                buckets.extend(resp["aggregations"]["sub_date_buckets"]["buckets"])
            parsed_resp.update(helper.parse_response(resp, params, admin_level, query_lineage, buckets, self.size))

        tasks = [process_query(query_lineage, query_mutation) for query_lineage, query_mutation in create_iterator(params["query_pangolin_lineage"], params["query_mutations"])]
        await asyncio.gather(*tasks)

        return {"success": True, "results": parsed_resp}
